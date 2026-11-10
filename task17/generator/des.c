/* The gpu partition's scheduler as a pure function of its inputs: jobs (eligible time, nodes, requested walltime,
 * true run time, checkpoint interval, dependency and follow-up links), node outage intervals and maintenance windows.
 * First come first served by eligible time with backfill on requested walltime (conservative: every queued job up to
 * bf_max gets a reservation; EASY: only the head of the queue), whole nodes allocated lowest-numbered first. A node
 * going down kills the job on it, which is requeued at its original place in the queue after a short hold and
 * restarts from its last checkpoint. No randomness lives here: every draw is made in Python and passed in.
 *
 * Times are hours (double). States: 0 COMPLETED, 1 TIMEOUT, 2 FAILED, 3 CANCELLED, 4 NODE_FAIL (a killed segment).
 */
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

typedef struct { double t; int type; int a; int b; } Event;
/* event types, in tie order: 0 outage end, 1 maintenance end, 2 arrival, 3 requeue release, 4 job end,
   5 outage start, 6 maintenance start */

typedef struct {
    Event *h; int n, cap;
} Heap;

static void heap_push(Heap *H, double t, int type, int a, int b) {
    if (H->n == H->cap) { H->cap = H->cap ? H->cap * 2 : 1024; H->h = realloc(H->h, H->cap * sizeof(Event)); }
    int i = H->n++;
    H->h[i].t = t; H->h[i].type = type; H->h[i].a = a; H->h[i].b = b;
    while (i > 0) {
        int p = (i - 1) / 2;
        Event *x = &H->h[i], *y = &H->h[p];
        if (y->t < x->t || (y->t == x->t && (y->type < x->type || (y->type == x->type && y->a <= x->a)))) break;
        Event tmp = *x; *x = *y; *y = tmp; i = p;
    }
}

static int ev_less(const Event *x, const Event *y) {
    if (x->t != y->t) return x->t < y->t;
    if (x->type != y->type) return x->type < y->type;
    return x->a < y->a;
}

static Event heap_pop(Heap *H) {
    Event top = H->h[0];
    H->h[0] = H->h[--H->n];
    int i = 0;
    for (;;) {
        int l = 2 * i + 1, r = l + 1, m = i;
        if (l < H->n && ev_less(&H->h[l], &H->h[m])) m = l;
        if (r < H->n && ev_less(&H->h[r], &H->h[m])) m = r;
        if (m == i) break;
        Event tmp = H->h[i]; H->h[i] = H->h[m]; H->h[m] = tmp; i = m;
    }
    return top;
}

typedef struct { double t; int d; } Bp;   /* a breakpoint of the availability profile */

typedef struct {
    int n_nodes, n_jobs, n_out, n_maint, mode, bf_max;
    double hold;
    const double *submit; const int *nodes; const double *wall; const double *dur; const double *ckpt;
    const int *dep; const int *after; const double *after_delay; const int *endstate;
    const int *out_node; const double *out_start; const double *out_end;
    const double *m_start; const double *m_end;
    /* runtime */
    double *elig; double *remaining; int *restarts; int *epoch; double *seg_start; uint64_t *mask;
    int *status;            /* 0 not yet submitted, 1 queued, 2 running, 3 done, 4 held, 5 waiting on dependency */
    double *first_start; double *final_end; int *final_state; double *nh; double *rework; double *sub_out;
    int *node_job; int *node_down;
    int *q; int qn, qcap;
    Heap H;
    int *dep_head, *dep_next;        /* dependents of a job: singly linked lists */
    int *fol_head, *fol_next;        /* follow-up submissions of a job */
    /* segments */
    int seg_n, seg_cap; int *seg_job, *seg_no, *seg_state; double *seg_s, *seg_e; uint64_t *seg_mask;
    Bp *prof; int pn, pcap;
    int next_maint;                  /* index of the next maintenance window not yet ended */
} Sim;

static void q_insert(Sim *S, int j) {
    if (S->qn == S->qcap) { S->qcap = S->qcap ? S->qcap * 2 : 1024; S->q = realloc(S->q, S->qcap * sizeof(int)); }
    int lo = 0, hi = S->qn;
    double k = S->elig[j];
    while (lo < hi) {
        int mid = (lo + hi) / 2, m = S->q[mid];
        if (S->elig[m] < k || (S->elig[m] == k && m < j)) lo = mid + 1; else hi = mid;
    }
    memmove(S->q + lo + 1, S->q + lo, (S->qn - lo) * sizeof(int));
    S->q[lo] = j; S->qn++;
    S->status[j] = 1;
}

static void q_remove_at(Sim *S, int pos) {
    memmove(S->q + pos, S->q + pos + 1, (S->qn - pos - 1) * sizeof(int));
    S->qn--;
}

static void seg_add(Sim *S, int j, int no, double s, double e, int st, uint64_t m) {
    if (S->seg_n == S->seg_cap) {
        S->seg_cap = S->seg_cap ? S->seg_cap * 2 : 4096;
        S->seg_job = realloc(S->seg_job, S->seg_cap * sizeof(int));
        S->seg_no = realloc(S->seg_no, S->seg_cap * sizeof(int));
        S->seg_state = realloc(S->seg_state, S->seg_cap * sizeof(int));
        S->seg_s = realloc(S->seg_s, S->seg_cap * sizeof(double));
        S->seg_e = realloc(S->seg_e, S->seg_cap * sizeof(double));
        S->seg_mask = realloc(S->seg_mask, S->seg_cap * sizeof(uint64_t));
    }
    int i = S->seg_n++;
    S->seg_job[i] = j; S->seg_no[i] = no; S->seg_state[i] = st; S->seg_s[i] = s; S->seg_e[i] = e; S->seg_mask[i] = m;
}

static int free_count(Sim *S) {
    int c = 0;
    for (int k = 0; k < S->n_nodes; k++) if (!S->node_down[k] && S->node_job[k] < 0) c++;
    return c;
}

static void start_job(Sim *S, int j, double t) {
    int need = S->nodes[j];
    uint64_t m = 0;
    for (int k = 0; k < S->n_nodes && need > 0; k++) {
        if (!S->node_down[k] && S->node_job[k] < 0) { S->node_job[k] = j; m |= (uint64_t)1 << k; need--; }
    }
    S->mask[j] = m;
    S->status[j] = 2;
    S->seg_start[j] = t;
    if (S->first_start[j] < 0) S->first_start[j] = t;
    double run = S->remaining[j] < S->wall[j] ? S->remaining[j] : S->wall[j];
    S->epoch[j]++;
    heap_push(&S->H, t + run, 4, j, S->epoch[j]);
}

static void prof_add(Sim *S, double t, int d) {
    if (S->pn + 1 >= S->pcap) { S->pcap = S->pcap ? S->pcap * 2 : 512; S->prof = realloc(S->prof, S->pcap * sizeof(Bp)); }
    int lo = 0, hi = S->pn;
    while (lo < hi) { int mid = (lo + hi) / 2; if (S->prof[mid].t <= t) lo = mid + 1; else hi = mid; }
    memmove(S->prof + lo + 1, S->prof + lo, (S->pn - lo) * sizeof(Bp));
    S->prof[lo].t = t; S->prof[lo].d = d; S->pn++;
}

/* earliest t' >= t such that at least w nodes are available throughout [t', t' + W) under the profile */
static double earliest(Sim *S, double t, int free_now, int w, double W) {
    int avail = free_now;
    double cand = t;
    int ok = avail >= w;
    for (int i = 0; i < S->pn; i++) {
        double tau = S->prof[i].t;
        if (ok && tau - cand >= W) return cand;
        int before = avail;
        avail += S->prof[i].d;
        while (i + 1 < S->pn && S->prof[i + 1].t == tau) { i++; avail += S->prof[i].d; }
        if (avail >= w) {
            if (!ok) { cand = tau; ok = 1; }
        } else {
            ok = 0;
        }
        (void)before;
    }
    return ok ? cand : 1e18;
}

static void schedule(Sim *S, double t) {
    if (S->qn == 0) return;
    int fr = free_count(S);
    /* the profile: running jobs' walltime ends, maintenance windows ahead */
    S->pn = 0;
    for (int k = 0; k < S->n_nodes; k++) {
        int j = S->node_job[k];
        if (j >= 0 && S->mask[j] & ((uint64_t)1 << k)) {
            /* count each running job once: at its lowest node */
            int lowest = __builtin_ctzll(S->mask[j]);
            if (lowest == k) prof_add(S, S->seg_start[j] + S->wall[j], S->nodes[j]);
        }
    }
    for (int i = S->next_maint; i < S->n_maint; i++) {
        if (S->m_end[i] <= t) continue;
        prof_add(S, S->m_start[i] > t ? S->m_start[i] : t, -S->n_nodes);
        prof_add(S, S->m_end[i], S->n_nodes);
    }
    int tested = 0, reserved_head = 0;
    int pos = 0;
    while (pos < S->qn && tested < S->bf_max) {
        int j = S->q[pos];
        tested++;
        int w = S->nodes[j];
        double W = S->wall[j];
        double ts = earliest(S, t, fr, w, W);
        if (ts == t) {
            q_remove_at(S, pos);
            start_job(S, j, t);
            fr -= w;
            /* its walltime end joins the profile */
            prof_add(S, t + W, w);
            continue;
        }
        if (S->mode == 1 || !reserved_head) {
            if (ts < 1e17) { prof_add(S, ts, -w); prof_add(S, ts + W, w); }
            reserved_head = 1;
        }
        pos++;
    }
}

static void end_dependents(Sim *S, int j, double t) {
    for (int d = S->dep_head[j]; d >= 0; d = S->dep_next[d]) {
        if (S->status[d] == 5) {
            S->elig[d] = t > S->submit[d] ? t : S->submit[d];
            q_insert(S, d);
        }
    }
    for (int f = S->fol_head[j]; f >= 0; f = S->fol_next[f]) {
        if (S->status[f] == 0) {
            double st = t + S->after_delay[f];
            S->sub_out[f] = st;
            heap_push(&S->H, st, 2, f, 0);
        }
    }
}

static void kill_on_node(Sim *S, int k, double t) {
    int j = S->node_job[k];
    if (j < 0) return;
    double e = t - S->seg_start[j];
    double done = 0.0;
    if (S->ckpt[j] > 0) done = floor(e / S->ckpt[j] + 1e-9) * S->ckpt[j];
    if (done > S->remaining[j]) done = S->remaining[j];
    S->rework[j] += (e - done) * S->nodes[j];
    S->nh[j] += e * S->nodes[j];
    seg_add(S, j, S->restarts[j], S->seg_start[j], t, 4, S->mask[j]);
    for (int n = 0; n < S->n_nodes; n++) if (S->node_job[n] == j) S->node_job[n] = -1;
    S->remaining[j] -= done;
    S->restarts[j]++;
    S->epoch[j]++;                     /* the pending end event is stale */
    S->status[j] = 4;
    heap_push(&S->H, t + S->hold, 3, j, 0);
}

static void run(Sim *S, double t_end) {
    int N = S->n_jobs;
    for (int j = 0; j < N; j++) {
        S->status[j] = 0; S->first_start[j] = -1; S->final_end[j] = -1; S->final_state[j] = -1;
        S->restarts[j] = 0; S->epoch[j] = 0; S->nh[j] = 0; S->rework[j] = 0; S->remaining[j] = S->dur[j];
        S->mask[j] = 0; S->elig[j] = S->submit[j]; S->sub_out[j] = S->submit[j];
        S->dep_head[j] = -1; S->fol_head[j] = -1;
    }
    for (int j = N - 1; j >= 0; j--) {
        if (S->dep[j] >= 0) { S->dep_next[j] = S->dep_head[S->dep[j]]; S->dep_head[S->dep[j]] = j; }
        if (S->after[j] >= 0) { S->fol_next[j] = S->fol_head[S->after[j]]; S->fol_head[S->after[j]] = j; }
    }
    for (int k = 0; k < S->n_nodes; k++) { S->node_job[k] = -1; S->node_down[k] = 0; }
    S->H.n = 0; S->qn = 0; S->seg_n = 0; S->next_maint = 0;
    for (int j = 0; j < N; j++) if (S->after[j] < 0) heap_push(&S->H, S->submit[j], 2, j, 0);
    for (int i = 0; i < S->n_out; i++) { heap_push(&S->H, S->out_start[i], 5, i, 0); heap_push(&S->H, S->out_end[i], 0, i, 0); }
    for (int i = 0; i < S->n_maint; i++) { heap_push(&S->H, S->m_start[i], 6, i, 0); heap_push(&S->H, S->m_end[i], 1, i, 0); }
    while (S->H.n) {
        Event ev = heap_pop(&S->H);
        double t = ev.t;
        if (t > t_end) break;
        int need_sched = 0;
        /* drain every event at this instant in tie order, scheduling once afterwards */
        for (;;) {
            if (ev.type == 2) {                               /* arrival */
                int j = ev.a;
                if (S->dep[j] >= 0 && S->status[S->dep[j]] != 3) { S->status[j] = 5; }
                else {
                    double de = S->dep[j] >= 0 ? S->final_end[S->dep[j]] : -1;
                    S->elig[j] = de > S->submit[j] ? de : t;
                    if (S->elig[j] < t) S->elig[j] = t;
                    q_insert(S, j);
                }
                need_sched = 1;
            } else if (ev.type == 3) {                        /* requeue release */
                q_insert(S, ev.a);
                need_sched = 1;
            } else if (ev.type == 4) {                        /* job end */
                int j = ev.a;
                if (ev.b == S->epoch[j] && S->status[j] == 2) {
                    double e = t - S->seg_start[j];
                    int st = S->remaining[j] <= S->wall[j] + 1e-9 ? S->endstate[j] : 1;
                    S->nh[j] += e * S->nodes[j];
                    seg_add(S, j, S->restarts[j], S->seg_start[j], t, st, S->mask[j]);
                    for (int n = 0; n < S->n_nodes; n++) if (S->node_job[n] == j) S->node_job[n] = -1;
                    S->status[j] = 3; S->final_end[j] = t; S->final_state[j] = st;
                    end_dependents(S, j, t);
                    need_sched = 1;
                }
            } else if (ev.type == 5) {                        /* outage start */
                int k = S->out_node[ev.a];
                kill_on_node(S, k, t);
                S->node_down[k]++;
            } else if (ev.type == 0) {                        /* outage end */
                int k = S->out_node[ev.a];
                if (S->node_down[k] > 0) S->node_down[k]--;
                need_sched = 1;
            } else if (ev.type == 6) {                        /* maintenance start: everything drained */
                for (int k = 0; k < S->n_nodes; k++) { kill_on_node(S, k, t); S->node_down[k]++; }
            } else if (ev.type == 1) {                        /* maintenance end */
                for (int k = 0; k < S->n_nodes; k++) if (S->node_down[k] > 0) S->node_down[k]--;
                S->next_maint = ev.a + 1;
                need_sched = 1;
            }
            if (S->H.n == 0 || S->H.h[0].t > t) break;
            ev = heap_pop(&S->H);
        }
        if (need_sched) schedule(S, t);
    }
}

/* Entry point. Returns the number of segments written (capped at seg_max) or -1 on a bad argument. */
int simulate(int n_nodes, int n_jobs, const double *submit, const int *nodes, const double *wall, const double *dur,
             const double *ckpt, const int *dep, const int *after, const double *after_delay, const int *endstate,
             int n_out, const int *out_node, const double *out_start, const double *out_end,
             int n_maint, const double *m_start, const double *m_end,
             int mode, int bf_max, double hold, double t_end,
             double *first_start, double *final_end, int *final_state, int *restarts, double *nh, double *rework,
             double *sub_out,
             int seg_max, int *seg_job, int *seg_no, int *seg_state, double *seg_s, double *seg_e, uint64_t *seg_mask) {
    if (n_nodes < 1 || n_nodes > 64) return -1;
    Sim S; memset(&S, 0, sizeof(S));
    S.n_nodes = n_nodes; S.n_jobs = n_jobs; S.n_out = n_out; S.n_maint = n_maint; S.mode = mode; S.bf_max = bf_max;
    S.hold = hold;
    S.submit = submit; S.nodes = nodes; S.wall = wall; S.dur = dur; S.ckpt = ckpt; S.dep = dep; S.after = after;
    S.after_delay = after_delay; S.endstate = endstate;
    S.out_node = out_node; S.out_start = out_start; S.out_end = out_end; S.m_start = m_start; S.m_end = m_end;
    S.elig = malloc(n_jobs * sizeof(double)); S.remaining = malloc(n_jobs * sizeof(double));
    S.restarts = restarts; S.epoch = malloc(n_jobs * sizeof(int)); S.seg_start = malloc(n_jobs * sizeof(double));
    S.mask = malloc(n_jobs * sizeof(uint64_t)); S.status = malloc(n_jobs * sizeof(int));
    S.first_start = first_start; S.final_end = final_end; S.final_state = final_state; S.nh = nh; S.rework = rework;
    S.sub_out = sub_out;
    S.node_job = malloc(n_nodes * sizeof(int)); S.node_down = malloc(n_nodes * sizeof(int));
    S.dep_head = malloc(n_jobs * sizeof(int)); S.dep_next = malloc(n_jobs * sizeof(int));
    S.fol_head = malloc(n_jobs * sizeof(int)); S.fol_next = malloc(n_jobs * sizeof(int));
    run(&S, t_end);
    int n = S.seg_n < seg_max ? S.seg_n : seg_max;
    memcpy(seg_job, S.seg_job, n * sizeof(int)); memcpy(seg_no, S.seg_no, n * sizeof(int));
    memcpy(seg_state, S.seg_state, n * sizeof(int)); memcpy(seg_s, S.seg_s, n * sizeof(double));
    memcpy(seg_e, S.seg_e, n * sizeof(double)); memcpy(seg_mask, S.seg_mask, n * sizeof(uint64_t));
    int total = S.seg_n;
    free(S.elig); free(S.remaining); free(S.epoch); free(S.seg_start); free(S.mask); free(S.status);
    free(S.node_job); free(S.node_down); free(S.dep_head); free(S.dep_next); free(S.fol_head); free(S.fol_next);
    free(S.q); free(S.H.h); free(S.prof);
    free(S.seg_job); free(S.seg_no); free(S.seg_state); free(S.seg_s); free(S.seg_e); free(S.seg_mask);
    return total;
}
