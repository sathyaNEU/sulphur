"""Read the shipped files back into the frames the forecast runs on, handling every export's mess: the billing
system's re-exported lines once, a credited line replaced by its re-issue and the credit note dropped, onboarding fees
kept apart; the Team plan's failed card payments dropped for the paid re-issue; the pipeline archive's re-run
snapshot rows once; stages, dates and months read from the files' own text. Reads only target/."""
import datetime as dt
import os

import numpy as np
import pandas as pd

import params as P

STAGES = {s: i for i, s in enumerate(P.STAGES)}
LINE_TYPES = {"Subscription - new": "new", "Subscription - renewal": "renewal", "Seat true-up": "true_up",
              "Onboarding fee": "onboarding_fee"}


def month_index(s):
    d = pd.to_datetime(s)
    return (d.dt.year - P.M0_YEAR) * 12 + d.dt.month - P.M0_MONTH


def find(target, prefix):
    hits = [f for f in sorted(os.listdir(target)) if f.startswith(prefix)]
    assert len(hits) == 1, (prefix, hits)
    return os.path.join(target, hits[0])


def contract_lines(target, dedupe=True, credits=True, fees=True):
    """dedupe, credits and fees switch each handling off for the checks' mishandled variants."""
    raw = pd.read_csv(find(target, "billing_contract_lines"), dtype={"credits_line_id": "Int64"})
    L = raw.drop_duplicates() if dedupe else raw
    if dedupe:
        assert L["line_id"].is_unique
    if credits:
        credited = set(L["credits_line_id"].dropna().astype(int))
        L = L[(L["line_type"] != "Credit note") & ~L["line_id"].isin(credited)].copy()
    else:
        L = L[L["line_type"] != "Credit note"].copy()
    if not fees:
        L = L.copy()
        L.loc[L["line_type"] == "Onboarding fee", "line_type"] = "Subscription - new"
    out = pd.DataFrame({
        "acc": L["billing_account"].values,
        "type": L["line_type"].map(LINE_TYPES).values,
        "m": month_index(L["service_start"]).values,
        "day": pd.to_datetime(L["service_start"]).dt.day.values,
        "seats": np.where(L["line_type"] == "Onboarding fee", 0, L["quantity"]).astype(int),
        "price": L["unit_price"].astype(float).values,
        "cur": L["currency"].values,
        "start": pd.to_datetime(L["service_start"]).values,
    })
    out["opening"] = out["start"] < pd.Timestamp(P.M0_YEAR, P.M0_MONTH, 1)
    return out.drop(columns="start").reset_index(drop=True), raw


def team_invoices(target, paid_only=True):
    raw = pd.read_csv(find(target, "team_invoices"))
    T = raw[raw["status"] == "paid"] if paid_only else raw.drop_duplicates(["team_account", "period_start"],
                                                                             keep="first")
    out = pd.DataFrame({"acc": T["team_account"].values, "m": month_index(T["period_start"]).values,
                        "day": pd.to_datetime(T["period_start"]).dt.day.values,
                        "members": T["active_members"].astype(int).values,
                        "seats": T["seats_billed"].astype(int).values, "cur": T["currency"].values})
    assert not out.duplicated(["acc", "m"]).any()
    return out.reset_index(drop=True), raw


def load(target, dedupe=True, credits=True, fees=True, paid_only=True, snap_dedupe=True, dated_links=True):
    lines, raw_lines = contract_lines(target, dedupe, credits, fees)
    team, raw_team = team_invoices(target, paid_only)
    act = pd.read_csv(find(target, "workspace_monthly_activity"))
    ws = pd.DataFrame({"ws": act["workspace_id"].values,
                       "m": month_index(act["month"] + "-01").values, "active": act["active_users"].values})
    lk = pd.read_csv(find(target, "workspace_account_links"))
    wmap = pd.DataFrame({"ws": lk["workspace_id"].values, "owner": lk["account_id"].values,
                         "from": month_index(lk["linked_from"]).values,
                         "to": month_index(lk["linked_to"]).values})
    if not dated_links:
        # every workspace read as belonging to its latest account throughout
        wmap = wmap.sort_values("from").groupby("ws").tail(1).assign(**{"from": -999, "to": np.nan})
    crm = pd.read_excel(find(target, "crm_accounts_export"), sheet_name="Accounts")
    cur_of = lines.groupby("acc")["cur"].first()
    acc = pd.DataFrame({"acc": crm["Billing account"].values,
                        "parent": np.where(crm["Parent account ID"].isna(), crm["Billing account"],
                                           crm["Parent account ID"]),
                        "source": np.where(crm["Lead source"] == "Team upgrade", "upgrade", "sales"),
                        "start": month_index(crm["Customer since"].astype(str)).values})
    acc["cur"] = acc["acc"].map(cur_of).fillna("EUR")
    acc = acc.sort_values("acc").reset_index(drop=True)
    sn = pd.read_csv(find(target, "pipeline_snapshots"))
    sn = sn.drop_duplicates() if snap_dedupe else sn
    m = month_index(sn["snapshot_date"]).values
    snap = pd.DataFrame({"id": sn["opportunity_id"].values, "m": m,
                         "created": month_index(sn["created_date"]).values,
                         "stage": sn["stage"].map(STAGES).values,
                         "mis": m - month_index(sn["stage_entered"]).values,
                         "seats": sn["seats_quoted"].astype(int).values, "cur": sn["currency"].values})
    assert not snap_dedupe or not snap.duplicated(["id", "m"]).any()
    cl = pd.read_csv(find(target, "opportunities_closed"))
    closed = pd.DataFrame({"id": cl["opportunity_id"].values, "created": month_index(cl["created_date"]).values,
                           "stage": cl["last_stage"].map(STAGES).values,
                           "outcome": np.where(cl["outcome"] == "Closed Won", "won", "lost"),
                           "m": month_index(cl["close_date"]).values,
                           "acc": cl["billing_account"].where(cl["outcome"] == "Closed Won").values,
                           "seats": cl["seats_quoted"].astype(int).values, "cur": cl["currency"].values})
    tl = lk[lk["plan"] == "Team"].sort_values("linked_from").groupby("account_id")["workspace_id"].first()
    first = team.sort_values("m").groupby("acc").first()
    tacc = pd.DataFrame({"acc": first.index, "start": first["m"].values, "cur": first["cur"].values})
    tacc["ws"] = tacc["acc"].map(tl)
    return {"lines": lines, "team": team, "ws": ws, "wmap": wmap, "snap": snap, "closed": closed, "acc": acc,
            "tacc": tacc, "raw_lines": raw_lines, "raw_team": raw_team}
