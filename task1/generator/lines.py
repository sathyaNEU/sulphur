"""Every 2027 line's expected value under one set of choices: the line's starts of the twelve months to the cut give
the early reading and payment routes its 2027 starts are taken to carry."""
import numpy as np

import models
import params as P
import sim


def line_inputs(pn, line):
    c, t = line
    sel = ((pn["channel"] == sim.C_IDX[c]) & (pn["title"] == sim.T_IDX[t]) & (pn["kind"] == "new")
           & ~pn["withdrawn"] & (pn["start"] > P.CUT - 12) & (pn["start"] <= P.CUT))
    routes = pn["route"][sel]
    px = pn["proxy"][sel]
    okp = ~np.isnan(px)
    # every start with an early reading, and its own route
    return px[okp], routes[okp]


def values(pn, plan, o, M=None):
    M = M or models.fit_all(pn, o)
    out = {}
    for line, spec in plan.items():
        px, rt = line_inputs(pn, line)
        out[line] = models.line_value(M, line, spec["starts"], spec["offer"], px, rt, o)
    return out, M
