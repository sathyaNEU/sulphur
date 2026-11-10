"""The world's records as clean tables: the frames the pack's files carry before any export mess is applied, and the
frames golden.load() rebuilds from the shipped files."""
import pandas as pd

import params as P
import sim


def frames(w):
    L = w.log
    lines = pd.DataFrame(L["lines"])
    lines["opening"] = lines.get("opening", False)
    lines["opening"] = lines["opening"].fillna(False).astype(bool)
    team = pd.DataFrame(L["team_inv"])
    ws = pd.DataFrame(L["ws"])
    wmap = pd.DataFrame(L["ws_map"])
    snap = pd.DataFrame(L["snap"])
    closed = pd.DataFrame([{"id": o["id"], "created": o["created"], "stage": o["stage"],
                            "outcome": o["closed"][0], "m": o["closed"][1],
                            "acc": o["closed"][2] if o["closed"][0] == "won" else None,
                            "seats": o["quote_seats"], "cur": o["cur"]} for o in L["opp_closed"]])
    acc = pd.DataFrame([{"acc": a["id"], "parent": a["parent"], "source": a["source"], "start": a["start"],
                         "cur": a["cur"]} for a in w.bus])
    par = pd.DataFrame([{"parent": p["id"], "group": p["group"]} for p in w.parents])
    tacc = pd.DataFrame([{"acc": t["id"], "start": t["start"], "cur": t["cur"], "ws": t["ws"]["id"]} for t in w.team])
    return {"lines": lines, "team": team, "ws": ws, "wmap": wmap, "snap": snap, "closed": closed, "acc": acc,
            "par": par, "tacc": tacc}
