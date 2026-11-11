"""The simulator's own expected 2027 loss ratios, which no file holds: each quote since 1 February 2026 (the sampled
unsold ones at their weight) replayed at a change with its true expected claims cost, at the conversion its new rank
carries. Printed for the design note's Pinned line; nothing graded reads it.

    python3 truth.py
"""
import datetime as dt
import io
import os
import sys
from contextlib import redirect_stdout

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as G  # noqa: E402
import methods as M  # noqa: E402
import params as P  # noqa: E402
import world as W  # noqa: E402


def main():
    with redirect_stdout(io.StringIO()):
        B = W.build(P.SEED)
    Q = B["Q"]
    cur = np.array([x >= dt.date(2026, 2, 1) for x in Q["date"]])
    prop = G.PROPOSAL_U25
    for seg in ("u25", "mid", "o65"):
        m = cur & (Q["seg"] == seg)
        gross, net, mu, comp = Q["gross"][m], Q["net"][m], Q["mu"][m], Q["comp_all"][m]
        w = np.where(Q["kind"][m] == "sold", 1.0, 50.0)

        def lr(L, move=M.MARKET):
            rank = 1 + (comp * (1 + move) < (gross * (1 + L))[:, None]).sum(1)
            p = P.P_SHOP * W.PR[rank - 1]
            return (w * p * mu).sum() * (1 + M.INFL) / (w * p * net * (1 + L)).sum()
        rise = next(k for k in range(61) if lr(k / 100) <= M.TARGET)
        sel = lr(prop) / (lr(0.0) / (1 + prop))
        print("%s: true smallest rise %+d; at the team's %+d the loss ratio runs %.1f per cent above the same base "
              "with the won book held fixed" % (seg, rise, round(prop * 100), (sel - 1) * 100))
    with redirect_stdout(io.StringIO()):
        D = G.prepare(os.path.join(os.path.dirname(HERE), "target"))
        S = G.segment(D, "u25")
    gsel = S["lr"](prop) / (S["lr"](0.0) / (1 + prop))
    print("golden: at the team's %+d the under-25 loss ratio runs %.1f per cent above the same base held fixed"
          % (round(prop * 100), (gsel - 1) * 100))


if __name__ == "__main__":
    main()
