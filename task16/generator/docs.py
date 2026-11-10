"""The group's own documents in the pack: the meeting notes that carry the shortlist, the shortlist sheet, the
trainer's defaults file and the launch script of the last week's batch."""
import datetime as dt

import openpyxl
from openpyxl.styles import Alignment, Font

import infra as I
import params as P
import sweep as S

ROUTE_WORD = {"nA": "expert", "nB": "contractor", "nC": "map transfer"}


def _points(c):
    parts = []
    for k in ("nA", "nB", "nC"):
        if c[k]:
            parts.append("{:,} {}".format(c[k], ROUTE_WORD[k]))
    return " + ".join(parts)


def _lr(c):
    return "to be set" if c["lr"] is None else ("%.0e" % c["lr"]).replace("e-0", "e-")


def hours(c):
    n = c["nA"] + c["nB"] + c["nC"]
    steps = int(round(P.EPOCHS * n / P.BATCH))
    return steps, steps * I.STEP_SECONDS[c["width"]] / 3600.0


def notes(path):
    rows = "\n".join("| %s | %d | %s | %s |" % (c["key"], c["width"], _points(c), _lr(c)) for c in S.SHORTLIST)
    text = """# MML group meeting, Thursday 5 November 2026

Present: Helene, Magne, Tor. Apologies: Ragnhild (at sea until the 12th).

## 1. NSSMP 2027 training slots

Proposals are due Friday 20 November at noon. Helene went through the call text again:

- Each team gets one reserved slot of up to 120 hours on the programme's GPU node in February. The proposal names one
  training configuration for it. It is trained once, with the recipe the proposal states, and the programme scores
  the final checkpoint on the verified benchmark: mean log loss over the 20,000 grab-sample points.
- The form asks for the expected benchmark log loss of that final checkpoint and a range we expect the result to fall
  in four times out of five. Teams are ranked on the expected value, and a team whose result lands outside its own
  range drops a place in the 2028 ranking.
- Our pilot quota of 32 benchmark uploads ran out on 23 October. Nothing more can be scored before the slots are
  awarded.

We keep our standard recipe for the slot: batch 128, twelve epochs, cosine schedule with 3 per cent warm-up, the final
checkpoint, no early stopping.

## 2. Shortlist

Agreed to choose among four configurations. All fit the slot on Tor's timings (shortlist sheet).

| Opt. | Width | Labels | LR |
|---|---|---|---|
%s

- Lyngvær's lot 1 (128,000 points) came in the week of 19 October and is all the contractor labelling in this
  year's budget. Lots 2 to 4 are not funded.
- Map-transfer shards are prepared for all 1,024,000 points (Tor, end of August).
- The 1024-wide job in week 43 ran out of walltime at about 70 per cent of its schedule, so option A still needs a
  learning rate.
- B, C and D use the rates we took for 512 and 256 after the week 42 check.

## 3. Actions

- Magne: expected benchmark loss and range for all four options, and which one to name, to Helene by Tuesday 10
  November.
- Tor: exports from the tracking server, the scheduler and the checkpoint store into the shared folder (done 4
  November).
- Helene: proposal text once Magne's figures are in.

## 4. Other business

- Ragnhild's September transects from Nordkappbanken will not be interpreted before January, so they are not in any
  option.
- Tor will ask IT about the scratch quota again. One item dump was lost to it in week 42.
""" % rows
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def shortlist(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Shortlist"
    head = ["Option", "Width", "Expert points", "Contractor points", "Map-transfer points", "Epochs",
            "Batch size", "Steps", "Learning rate", "s/step (g1)", "Hours on one GPU"]
    ws.append(head)
    for c in S.SHORTLIST:
        steps, h = hours(c)
        ws.append([c["key"], c["width"], c["nA"], c["nB"], c["nC"], P.EPOCHS, P.BATCH, steps,
                   None if c["lr"] is None else c["lr"], I.STEP_SECONDS[c["width"]], round(h, 1)])
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    widths = [8, 9, 11, 11, 13, 8, 8, 9, 10, 13, 10]
    for i, w in enumerate(widths):
        ws.column_dimensions[chr(65 + i)].width = w
    for r in range(2, 2 + len(S.SHORTLIST)):
        for col in "CDEH":
            ws["%s%d" % (col, r)].number_format = "#,##0"
        ws["I%d" % r].number_format = "0.0E+00"
        ws["J%d" % r].number_format = "0.00"
        ws["K%d" % r].number_format = "0.0"
    ws.freeze_panes = "B2"
    ws2 = wb.create_sheet("Slot")
    ws2.append(["Programme slot (hours)", 120])
    ws2.append(["Slot month", "February 2027"])
    ws2.append(["Proposal deadline", "20 November 2026, 12:00"])
    ws2.append(["Timings taken from", "our own g1 nodes, week 40 to 44 jobs"])
    ws2.column_dimensions["A"].width = 26
    ws2.column_dimensions["B"].width = 34
    wb.save(path)


def defaults(path):
    text = """# sedinet trainer defaults, rev d92a7c4
model:
  features: 32
  classes: 10
  hidden_layers: 2
  width: 128
  activation: relu
optim:
  name: adam
  betas: [0.9, 0.999]
  lr: 1.0e-3
  schedule: cosine
  warmup_frac: 0.03
train:
  batch_size: 128
  epochs: 12
  shuffle: per_epoch
  checkpoint_every: 2000
  keep_checkpoints: all
  resume_from: last_checkpoint
eval:
  split: dev_split_items.csv
  every_steps: 250
  metrics: [log_loss, accuracy]
  dump_item_loss: final_checkpoint
logging:
  tracking_uri: http://tracking.mml.internal:5000
  every_steps: 20
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def launch(jobs, path):
    """The batch script of the last week, as Magne ran it (the two wide trials went on two days later by hand)."""
    lines = ["#!/bin/bash", "# vendor label trials, week 44", "# usage: bash launch_vendor_trials.sh", "set -euo pipefail", "",
             "PART=gpu-preempt",
             'submit () { sbatch -p "$PART" --gres=gpu:1 -t 24:00:00 -J "$1" train.sbatch "${@:2}"; sleep 3; }', ""]
    vend = [j for j in jobs if j["stage"] == "vend" and j["train"]["width"] == 128 and "relaunch_of" not in j]
    for j in sorted(vend, key=lambda j: j["submit"]):
        t = j["train"]
        args = ["--width %d" % t["width"], "--lr %s" % ("%.0e" % t["lr"]).replace("e-0", "e-")]
        for flag, k in (("--exp", "nA"), ("--ctr", "nB"), ("--map", "nC")):
            if t.get(k):
                args.append("%s 0-%d" % (flag, t[k] // P.SHARD - 1))
        args.append("--seed %d" % t["seed"])
        lines.append("submit %s %s" % (j["name"], " ".join(args)))
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
