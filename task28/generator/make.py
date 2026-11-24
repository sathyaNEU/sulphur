#!/usr/bin/env python3
"""Run the complete Stage 3 build pipeline for task28 in one deterministic pass:
  1. build.py -> task28/target/ (15 files, LibreOffice PDFs, postprocess XLSX, distinct mtimes)
  2. analysis.run_all -> recompute all golden, variant, lattice, forcing, and falsification numbers
  3. deliver.build_goldens_and_zips -> golden/ (XLSX + CSV), target.zip, golden.zip
  4. writeup.emit_all -> figures.json, effort.json, metadata.json, submission.md
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import analysis as AN  # noqa: E402
import build as BLD  # noqa: E402
import deliver as DEL  # noqa: E402
import writeup as WU  # noqa: E402


def main():
    target_dir = os.path.join(TASK_DIR, "target")
    print("[1/4] Building target/ ...")
    counts = BLD.build(target_dir)
    print(f"      target/ built ({len(os.listdir(target_dir))} files)")

    print("[2/4] Running analysis on shipped target/ files ...")
    res = AN.run_all(target_dir)
    print(f"      Golden call: {res['golden_slate']} | Total 2027: {res['gold_asm']['A_total_2027']:.1f} h")

    print("[3/4] Writing golden/ deliverables and cutting target.zip + golden.zip ...")
    paths = DEL.build_goldens_and_zips(TASK_DIR, res=res)
    for k, p in paths.items():
        print(f"      {k:10s} {os.path.getsize(p):10,d} bytes")

    print("[4/4] Emitting figures.json, effort.json, metadata.json, submission.md ...")
    figs, eff, meta = WU.emit_all(TASK_DIR, res=res)
    print(f"      Done. Total energy penalty {figs['A_energy_mwh']:.1f} MWh (overhaul {figs['A_overhaul_mwh']:.1f} MWh)")


if __name__ == "__main__":
    main()
