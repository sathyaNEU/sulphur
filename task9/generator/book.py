"""task9: the sleeve's own book and paperwork (authored positions on real market values).

Two confirmations a month since July 2021, each a 12-month S&P 500 variance swap struck at the Cboe 1-Year
Volatility Index close of the sale date; the dealers' daily valuations, the collateral they called and the
settlements they paid follow from the real closes. The only authored numbers are the positions themselves and the
small differences between a dealer's implied volatility and the published term structure.
"""
import hashlib
from statistics import NormalDist

import numpy as np
import pandas as pd

import market as MK
import params as P
import swaps as SW

_ND = NormalDist()


def unit(*key):
    """A uniform draw fixed by its key (no generator state, so every build gives the same value)."""
    h = hashlib.blake2b("|".join(str(k) for k in key).encode(), digest_size=8).digest()
    return (int.from_bytes(h, "big") + 0.5) / 2.0 ** 64


def noise(*key):
    return _ND.inv_cdf(unit(*key))


class Book:
    def __init__(self, mk):
        self.mk = mk
        self.ladder = SW.Ladder(mk, P.OLD_MAT, start=pd.Timestamp(P.SLEEVE_FIRST[0], P.SLEEVE_FIRST[1], 1), last_sale=P.REVIEW)
        self.trades, self.dead = self._trades()
        self.val = self._valuations()
        self.ledger = self._ledger()

    # ---- the confirmations
    def _trades(self):
        mk = self.mk
        rows, dead = [], []
        bss, acm = 412877, 0
        order = 2104380
        ay, am, adealer, awrong = P.AMENDED
        ny, nm, nold, nnew, nwhen = P.NOVATED
        for i, s in enumerate(self.ladder.t.itertuples()):
            order += 260 + int(2300 * unit("order-month", i))
            for leg, dealer in enumerate(P.PAIRS[i % 3]):
                order += 1 + int(3 * unit("order-leg", i, leg))
                if dealer == "BSS":
                    bss += 37 + int(900 * unit("bssref", i, leg))
                    ref = "BSS-EQD-%06d" % bss
                elif dealer == "ACM":
                    acm += 1
                    ref = "ACM/VS/%s/%04d" % (s.sale.strftime("%y%m"), 2000 + 7 * acm + int(5 * unit("acmref", i)))
                else:
                    ref = "WXVAR%s%03d" % (s.sale.strftime("%Y%m%d"), 100 + int(880 * unit("wxbref", i, leg)))
                row = dict(ticket=str(order), sale=s.sale, expiry=s.expiry, dealer=dealer, dealer_ref=ref, vega=float(P.OLD_CONF_VEGA),
                           k=float(s.k), n=int(s.n), rv=s.rv, month=(s.sale.year, s.sale.month), novated_from=None,
                           novation_date=pd.NaT, old_ref=None, remark="")
                if (s.sale.year, s.sale.month) == (ay, am) and dealer == adealer:
                    # booked at ten times its size, corrected on a new ticket the next morning
                    dead.append(dict(row, vega=float(awrong), status="SUPERSEDED",
                                     remark="Booked in error; superseded by order %d" % (order + 41)))
                    row["ticket"] = str(order + 41)
                    row["remark"] = "Amends order %d (vega notional)" % order
                    order += 41
                if (s.sale.year, s.sale.month) == (ny, nm) and dealer == nold:
                    dead.append(dict(row, status="NOVATED"))
                    row.update(novated_from=nold, novation_date=nwhen, old_ref=ref, dealer=nnew, old_ticket=str(order),
                               dealer_ref="BSS-EQD-%06d" % (412877 + 51000 + int(900 * unit("novref"))))
                rows.append(row)
        t = pd.DataFrame(rows)
        # the novated confirmation is re-booked on the day of the novation, so its order number sits there in the sequence
        j = t.index[t.novated_from.notna()][0]
        before = t[(t.sale < nwhen) & (t.index != j)].ticket.astype(int).max()
        new_order = before + 57 + int(150 * unit("novation"))
        old_order = t.at[j, "old_ticket"]
        t.at[j, "ticket"] = str(new_order)
        t.at[j, "remark"] = "Novated in from %s; original terms, order %s" % (P.DEALERS[nold]["short"], old_order)
        dead[0]["remark"] = "Novated to %s effective %s; see order %d" % (P.DEALERS[nnew]["short"], nwhen.strftime("%m/%d/%Y"), new_order)
        t = t.drop(columns=["old_ticket"])
        t["settled"] = t.expiry <= P.REVIEW
        t["rv_cap"] = np.minimum(t.rv, SW.CAP * t.k)
        t["settle_amt"] = np.where(t.settled, np.round(t.vega * SW.pay(t.k, t.rv), 2), np.nan)
        t["settle_date"] = [mk.sched[mk.pos(e) + 2] for e in t.expiry]
        t["status"] = np.where(t.settled, "SETTLED", "LIVE")
        return t, pd.DataFrame(dead)

    def open(self):
        return self.trades[~self.trades.settled].copy()

    # ---- the dealers' daily valuations, to the last month end
    def _valuations(self):
        mk = self.mk
        C = mk.curve()
        days = mk.days
        cum = mk.cum.values
        dnum = days.values.astype("datetime64[D]").astype(int)
        last = mk.pos(P.STATEMENT)
        out = []
        for s in self.trades.itertuples():
            i0, i1 = mk.pos(s.sale), mk.pos(s.expiry)
            j = np.arange(i0 + 1, min(i1, last + 1))
            if not len(j):
                continue
            n_e, n_r = (j - i0).astype(float), (i1 - j).astype(float)
            acc = 1e4 * 252.0 * (cum[j] - cum[i0]) / n_e                 # realised variance to date
            cal = np.clip(int(np.datetime64(s.expiry, "D").astype(int)) - dnum[j], 0, MK.TMAX)
            base = C[j, cal]
            d = days[j]
            dealer = np.array([s.dealer] * len(j), dtype=object)
            ref = np.array([s.dealer_ref] * len(j), dtype=object)
            if s.novated_from:
                before = d < s.novation_date
                dealer[before] = s.novated_from
                ref[before] = s.old_ref
            eps = np.array([P.DEALER_BIAS[dl] + P.DEALER_DAY_SD * noise("day", dl, dd.date()) + P.DEALER_SWAP_SD * noise("swap", dl, dd.date(), s.dealer_ref)
                            for dl, dd in zip(dealer, d)])
            variance = np.array([P.DEALERS[dl]["basis"] == "VARIANCE" for dl in dealer])
            # what each dealer prints: volatility to four and two decimals, or variance to two decimals
            realized = np.where(variance, np.round(acc, 2), np.round(np.sqrt(acc), 4))
            implied = np.where(variance, np.round((base + eps) ** 2, 2), np.round(base + eps, 2))
            rvar = np.where(variance, realized, realized ** 2)
            ivar = np.where(variance, implied, implied ** 2)
            w = np.minimum((n_e * rvar + n_r * ivar) / (n_e + n_r), (SW.CAP * s.k) ** 2)
            mtm = np.round(s.vega * (s.k * s.k - w) / (2.0 * s.k), 0)
            out.append(pd.DataFrame(dict(date=d, ticket=s.ticket, dealer=dealer, dealer_ref=ref, vega=s.vega, k=s.k, n_e=n_e.astype(int),
                                         n_r=n_r.astype(int), realized=realized, implied=implied, base_iv=base, mtm=mtm)))
        v = pd.concat(out, ignore_index=True)
        return v.sort_values(["date", "dealer", "dealer_ref"]).reset_index(drop=True)

    # ---- the collateral the dealers held, day by day
    def _ledger(self):
        g = self.val.groupby(["date", "dealer"]).mtm.sum().unstack("dealer").fillna(0.0)
        g = g.reindex(columns=list(P.DEALERS)).fillna(0.0)
        posted = (np.ceil(np.maximum(0.0, -g) / P.COLL_ROUND) * P.COLL_ROUND)
        rows = []
        for dl in P.DEALERS:
            prev = 0.0
            for d in g.index:
                rows.append(dict(date=d, dealer=dl, exposure=float(g.at[d, dl]), posted=float(posted.at[d, dl]), movement=float(posted.at[d, dl] - prev)))
                prev = float(posted.at[d, dl])
        return pd.DataFrame(rows).sort_values(["date", "dealer"]).reset_index(drop=True)

    def statement(self, dealer, date=None):
        """The dealer's lines at a statement date: the confirmations it holds open that day."""
        date = date or P.STATEMENT
        v = self.val[(self.val.date == date) & (self.val.dealer == dealer)]
        return v.merge(self.trades[["ticket", "sale", "expiry"]], on="ticket").sort_values("sale").reset_index(drop=True)
