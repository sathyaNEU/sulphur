"""Train the pilot (and, with 'truth', the author-side truth runs). Idempotent: jobs already on disk are skipped."""
import os, sys, time
os.environ["OMP_NUM_THREADS"] = "1"
import runner as R, sweep as S

if __name__ == "__main__":
    which = sys.argv[1:] or ["pilot"]
    t0 = time.time()
    if "pilot" in which:
        R.run_all([j["train"] for j in S.pilot_specs()])
        print("pilot trained, %.0fs" % (time.time() - t0), flush=True)
    if "truth" in which:
        R.run_all([j["train"] for j in S.truth_specs()] + [j["train"] for j in S.clean_truth_specs()])
        print("truth trained, %.0fs" % (time.time() - t0), flush=True)
