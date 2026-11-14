"""task25 world parameters: Saukko Labs Oy's two leased GPU halls at Pohjoisvirta Datacenters' Kaivola campus, the
2026 record (runs, logs, profiles, the halls' meters, the provider's works) and the H1 2027 roadmap. Every number a
file or a golden figure carries is computed from these by the simulation; nothing downstream is typed."""
import datetime as dt

SEED = 25_2027
ORG = "Saukko Labs Oy"
PROVIDER = "Pohjoisvirta Datacenters Oy"
CAMPUS = "Kaivola"
INFRA_LEAD = "Pia Kuosmanen"        # head of training infrastructure; the golden workbook and note are hers
COMMITTEE_CHAIR = "Esa Airaksinen"  # chairs the compute committee
DATA_LEAD = "Marja Laine"           # data team lead; owns the mixes and the length sample
PROVIDER_CONTACT = "Tauno Kainulainen"

RECORD_START = dt.date(2026, 1, 1)
RECORD_END = dt.date(2026, 10, 31)          # last day the record covers
PULL = dt.datetime(2026, 11, 6, 9, 40)      # UTC; every extract is pulled the same morning
ROADMAP_DATE = dt.date(2026, 11, 4)

# ---- hardware -------------------------------------------------------------------------------------------------
PEAK = 989.4e12                     # bf16 dense FLOP/s per GPU (H100 SXM and H200 alike)
GPUS_PER_NODE = 8
HALLS = {
    "A": dict(gpu="H100 SXM5 80GB", rows=16, slots=32, pods=1, contract_kw=6600.0, node_kw=9.15, idle_kw=1.25,
              infra_kw=210.0, ueff=1.00),
    "B": dict(gpu="H200 SXM 141GB", rows=32, slots=32, pods=2, contract_kw=8100.0, node_kw=9.62, idle_kw=1.30,
              infra_kw=280.0, ueff=1.055),
}
# dense GEMM efficiency on H100 by model; attention kernels run BETA times slower per FLOP than dense
U_DENSE = {"1B": 0.40, "3B": 0.44, "8B": 0.47, "13B": 0.49, "34B": 0.51, "70B": 0.52, "120B": 0.53}
BETA = 1.32
STEP_OVERHEAD = 0.026               # optimizer step and exposed reduction, share of a step's mean compute
RANK_JITTER = 0.004                 # per-rank, per-step kernel noise (sd, multiplicative)
# throttle: a step's compute stretches by THR1*x + THR2*x^2 when the hall's would-be draw exceeds its contract by x
THR1, THR2 = 0.95, 1.20
METER_NOISE_KW = 14.0
# a job whose nodes sit in both of hall B's pods pays for the pod boundary: its gradient reduction crosses the spine
# every step, and the whole ring runs at the slowest link
STRADDLE = 0.22
# the pool backs off as the hall nears its contract: its scheduler stops starting jobs once the load without the
# pool is POOL_KNEE of the contract, and has none running by POOL_ZERO (a linear back-off between)
POOL_KNEE, POOL_ZERO = 0.88, 0.97

# the Kide family: params, layers, d_model, kv heads, vocab
MODELS = {
    "1B": (1.24e9, 16, 2048), "3B": (3.21e9, 28, 3072), "8B": (8.03e9, 32, 4096), "13B": (13.1e9, 40, 5120),
    "34B": (33.9e9, 48, 7168), "70B": (70.6e9, 80, 8192), "120B": (121.4e9, 96, 10240),
}
VOCAB = 131072

# ---- documents: lognormal lengths in tokens (median, sigma, cap) --------------------------------------------------
SOURCES = {
    "web": (880, 1.00, 200_000), "code_file": (1_350, 1.00, 200_000), "forum": (610, 0.90, 60_000),
    "math": (1_240, 0.90, 120_000), "longform": (5_300, 0.62, 64_000), "papers": (10_800, 0.22, 16_000),
    "code_repo": (46_000, 0.75, 420_000), "books": (88_000, 0.55, 640_000),
}
BENCH_CORPUS = (1_100, 1.00, 100_000)   # the harness's synthetic corpus
MIXES = {
    # 2026 mixes
    "pt-web-26": {"web": 0.63, "code_file": 0.17, "forum": 0.08, "math": 0.07, "longform": 0.05},
    "lc16-26": {"web": 0.58, "longform": 0.22, "code_file": 0.14, "books": 0.06},
    "lc32-26": {"web": 0.58, "code_file": 0.24, "code_repo": 0.07, "books": 0.05, "longform": 0.06},
    "lc32bf-26": {"web": 0.56, "code_file": 0.24, "code_repo": 0.08, "longform": 0.12},
    "lc16bf-26": {"web": 0.50, "longform": 0.26, "papers": 0.18, "code_file": 0.06},
    "abl-26": {"web": 0.66, "code_file": 0.16, "forum": 0.10, "math": 0.08},
    # 2027 mixes
    "pt-web-27": {"web": 0.62, "code_file": 0.18, "forum": 0.08, "math": 0.07, "longform": 0.05},
    "lc-repo-27": {"code_repo": 0.30, "code_file": 0.40, "web": 0.30},
    "lc-books-27": {"books": 0.32, "web": 0.48, "longform": 0.20},
    "sci-27": {"papers": 0.92, "longform": 0.04, "web": 0.04},
    "lc-light-27": {"code_repo": 0.05, "books": 0.03, "web": 0.70, "code_file": 0.22},
    "lc-books8-27": {"books": 0.28, "code_repo": 0.08, "web": 0.64},
    "pt16-27": {"web": 0.55, "longform": 0.25, "code_file": 0.20},
}

# ---- interruptions and restarts ---------------------------------------------------------------------------------
NODE_FAIL_PER_DAY = {"A": 0.00105, "B": 0.00138}   # hardware faults that kill a job, per node-day
SOFT_FAIL_PER_DAY = 0.11                          # software crashes (NCCL, OOM, loader) per run-day, large runs
HALL_EVENT_PER_DAY = {"A": 1 / 61.0, "B": 1 / 54.0}  # facility or fabric events that stop every job in the hall
RESTART_MIN = {"median": 21.0, "sigma": 0.38}    # minutes, before checkpoint load
CKPT_LOAD_GBPS = 38.0                            # checkpoint read at restart, GB/s per job
CKPT_INTERVAL_MIN = 30.0
LOG_TARGET_S = 360.0                             # the trainer logs every N steps, N set so a row lands every few minutes
LOG_STEPS = (10, 20, 25, 50, 100, 200, 250, 500, 1000)
LAUNCH_DELAY_MIN = (18.0, 55.0)                  # a window's first launch after 00:00 UTC

# ---- provider works -------------------------------------------------------------------------------------------
WORKS_RATIO = {"major": (1.92, 0.13), "routine": (1.07, 0.05)}   # lognormal median ratio actual/planned, sigma
ROW6_FAULT = (dt.date(2026, 9, 14), dt.date(2026, 10, 19))      # hall A row 6 cooling fault, nodes slow under load
ROW6_SLOW = 1.19

# ---- the research pool (jobs outside the run registry) -------------------------------------------------------
POOL_BUSY = {"A": 0.55, "B": 0.46}      # mean busy share of nodes no registered run holds
POOL_WEEKLY = (1.00, 1.03, 1.04, 1.04, 1.02, 0.91, 0.88)   # Monday to Sunday
POOL_MONTHLY = {1: 0.98, 2: 1.02, 3: 1.03, 4: 1.01, 5: 1.00, 6: 0.98, 7: 0.90, 8: 0.95, 9: 1.03, 10: 1.04,
                11: 1.03, 12: 0.96}

# ---- the 2026 run registry -------------------------------------------------------------------------------------
# (run_id, model, hall, nodes, context, mix, packing, seqs_per_rank, start, end, profiled)
RUNS_2026 = [
    ("kide-70b-scale", "70B", "B", 1024, 8192, "pt-web-26", "sequential", 8, "2026-01-06", "2026-01-09", False),
    ("kide-8b-v2", "8B", "A", 128, 8192, "pt-web-26", "sequential", 8, "2026-01-05", "2026-02-08", False),
    ("kide-34b-v1", "34B", "B", 256, 8192, "pt-web-26", "sequential", 8, "2026-01-12", "2026-03-13", True),
    ("kide-13b-v2", "13B", "A", 256, 8192, "pt-web-26", "sequential", 4, "2026-01-19", "2026-03-27", True),
    ("kide-8b-v2-lc16", "8B", "A", 32, 16384, "lc16-26", "sequential", 4, "2026-03-02", "2026-03-08", False),
    ("kide-70b-v1", "70B", "B", 512, 8192, "pt-web-26", "sequential", 4, "2026-03-09", "2026-07-23", False),
    ("kide-13b-v2-lc32", "13B", "A", 64, 32768, "lc32-26", "sequential", 4, "2026-04-06", "2026-04-15", True),
    ("kide-34b-v1-lc32", "34B", "B", 128, 32768, "lc32-26", "sequential", 4, "2026-05-18", "2026-06-11", True),
    ("kide-34b-v1b", "34B", "B", 256, 8192, "pt-web-26", "sequential", 8, "2026-06-01", "2026-06-12", False),
    ("kide-70b-v1-lc32", "70B", "B", 256, 32768, "lc32-26", "sequential", 4, "2026-07-27", "2026-09-02", False),
    ("kide-13b-v3", "13B", "B", 256, 8192, "pt-web-26", "sequential", 8, "2026-08-10", "2026-10-01", False),
    ("kide-8b-v3", "8B", "A", 128, 8192, "pt-web-26", "sequential", 8, "2026-08-31", "2026-10-20", True),
    ("kide-34b-v2", "34B", "B", 384, 8192, "pt-web-26", "sequential", 8, "2026-09-07", None, False),
    ("kide-13b-v3-lc16", "13B", "B", 64, 16384, "lc16bf-26", "best_fit", 4, "2026-10-05", "2026-10-13", True),
    ("kide-8b-v3-lc32", "8B", "A", 32, 32768, "lc32bf-26", "best_fit", 4, "2026-10-22", "2026-10-28", True),
]
N_ABLATIONS = 38          # small runs (1B to 8B, 8 to 32 nodes, a few days) drawn by the simulation
CAPPED_TARGET_DAYS = (26, 36)   # the hall B days the 2026 schedule leaves over contract (asserted, not forced)

# ---- the H1 2027 roadmap ----------------------------------------------------------------------------------------
# (run_id, model, hall, nodes, context, mix, packing, seqs_per_rank, window_start, window_end, budget_tokens, purpose)
ROADMAP_2027 = [
    ("kide-70b-v2", "70B", "A", 256, 8192, "pt-web-27", "sequential", 8, "2027-01-11", "2027-02-27", 7.65e12,
     "continued pretraining"),
    ("kide-13b-code-lc32", "13B", "A", 32, 32768, "lc-repo-27", "sequential", 2, "2027-01-18", "2027-01-25", 0.655e12,
     "repository-level code, long context"),
    ("kide-34b-lc64", "34B", "A", 64, 65536, "lc-books-27", "sequential", 1, "2027-03-01", "2027-03-14", 0.673e12,
     "long-context extension"),
    ("kide-34b-sci", "34B", "A", 128, 16384, "sci-27", "best_fit", 8, "2027-04-12", "2027-05-02", 3.353e12,
     "scientific continued pretraining"),
    ("kide-120b-v1", "120B", "B", 480, 8192, "pt-web-27", "sequential", 4, "2027-02-01", "2027-04-17", 18.19e12,
     "flagship pretraining"),
    ("kide-34b-v3", "34B", "B", 256, 8192, "pt-web-27", "sequential", 8, "2027-02-01", "2027-03-11", 14.64e12,
     "pretraining"),
    ("kide-34b-16k", "34B", "B", 224, 16384, "pt16-27", "sequential", 8, "2027-03-15", "2027-05-08", 20.43e12,
     "16k pretraining"),
    ("kide-8b-v4", "8B", "B", 64, 8192, "pt-web-27", "sequential", 16, "2027-02-01", "2027-04-17", 24.97e12,
     "pretraining"),
    ("kide-13b-v4", "13B", "B", 128, 8192, "pt-web-27", "sequential", 8, "2027-03-29", "2027-05-08", 15.63e12,
     "pretraining"),
    ("kide-13b-lc32", "13B", "B", 64, 32768, "lc-light-27", "sequential", 16, "2027-05-03", "2027-05-15", 2.25e12,
     "long-context continued pretraining"),
    ("kide-8b-lc64", "8B", "B", 32, 65536, "lc-books8-27", "sequential", 2, "2027-05-24", "2027-06-06", 1.436e12,
     "long-context extension"),
]
# the reservation ledger: each run's block of whole rows (32 nodes a row; hall B's rows 1 to 16 are pod 1, 17 to 32
# pod 2), as the provider's reservation desk assigned them in the order the blocks were booked
BLOCKS_2027 = {
    "kide-70b-v2": ("A", 1, 8), "kide-13b-code-lc32": ("A", 9, 9), "kide-34b-lc64": ("A", 10, 11),
    "kide-34b-sci": ("A", 12, 15),
    "kide-120b-v1": ("B", 18, 32), "kide-34b-v3": ("B", 1, 8), "kide-34b-16k": ("B", 9, 15),
    "kide-8b-v4": ("B", 16, 17), "kide-13b-v4": ("B", 1, 4), "kide-13b-lc32": ("B", 5, 6), "kide-8b-lc64": ("B", 7, 7),
}
WORKS_2027 = [
    # (work id, hall, type, start local, planned hours, title)
    ("PV-27-014", "A", "major", dt.datetime(2027, 3, 8, 6, 0), 36.0, "Hall A spine re-cabling, rows 1 to 16"),
    ("PV-27-021", "B", "major", dt.datetime(2027, 5, 17, 6, 0), 48.0, "Hall B chilled-water loop upgrade"),
    ("PV-27-009", "A", "routine", dt.datetime(2027, 2, 9, 7, 0), 6.0, "Hall A quarterly UPS inspection"),
    ("PV-27-010", "B", "routine", dt.datetime(2027, 2, 10, 7, 0), 6.0, "Hall B quarterly UPS inspection"),
    ("PV-27-033", "A", "routine", dt.datetime(2027, 5, 11, 7, 0), 6.0, "Hall A quarterly UPS inspection"),
    ("PV-27-034", "B", "routine", dt.datetime(2027, 5, 12, 7, 0), 6.0, "Hall B quarterly UPS inspection"),
]
TARGETS_2027 = {   # golden days over window, the world's design (asserted on the cut pack, never typed downstream)
    "kide-70b-v2": 0.845, "kide-13b-code-lc32": 1.147, "kide-34b-lc64": 1.14, "kide-34b-sci": 1.148,
    "kide-120b-v1": 1.14, "kide-34b-v3": 0.955, "kide-13b-lc32": 0.85, "kide-8b-lc64": 1.15, "kide-34b-16k": 1.14,
    "kide-8b-v4": 1.065, "kide-13b-v4": 0.85,
}
