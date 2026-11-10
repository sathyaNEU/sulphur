"""task9: generator/effort.json, the client's effort test computed from the generator's own passes on the cut pack.

Three passes, each a named method run end to end by analysis.py on the shipped files (nothing here reads the prompt):

  quick     the agencies' copula (the economy's year and one sector factor), every default losing the average of
            the default years whose workouts have all closed (MP-RN-2 4.1), no sponsor house: the obvious file and the
            first account that fits
  careful   what a frontier run does unprompted: every file conformed, sponsor ownership rebuilt from the deal file,
            a probit on rating and years since the buyout, the house's year fitted into the copula, the sectors whose
            yearly default rates swing hardest given larger sector factors of their own, and one recovery for every
            default from the default years whose workouts have all closed
  thorough  the golden: each sector's loading on the shared year, the house's year on the latent scale, each
            default's recovery on its house-year's shock across the house's whole book, the shocks carried into the
            simulation

attach(F) adds each result's golden to figures.json under its own key (effort.py ties every result to the answer
blocks' figure) and returns the effort.json document.
"""
import math

NAMES = {"KL": "Kestrel Lane", "OS": "Ostvale"}
YEARS = [2027, 2028, 2029, 2030, 2031]


def _need(d):
    return {"%s %s" % (k, t): d[k]["need_pct"][i] for k in ("KL", "OS") for i, t in enumerate(("1", "0.5"))}


def _path(d):
    return {"%s %d" % (k, y): d[k]["by_year_pct"][i] for k in ("KL", "OS") for i, y in enumerate(YEARS)}


def _el(d):
    return {k: d[k]["el_pct"] for k in ("KL", "OS")}


def _span(vals, unit, pad=0.0):
    lo, hi = min(vals), max(vals)
    return [round(math.floor(lo / unit + 1e-9) * unit - pad, 6), round(math.ceil(hi / unit - 1e-9) * unit + pad, 6)]


def attach(F):
    G, M, rg = F["golden"], F["band_members"], F["rungs"]
    F["result_house_share"] = F["house_share"]
    F["result_os_loading"] = G["OS"]["loading"]
    F["result_link_slope"] = F["link"]["bh"]
    F["result_kl_p5"] = G["KL"]["p5_pct"]
    F["result_os_p5"] = G["OS"]["p5_pct"]
    F["result_need"] = _need(G)
    F["result_path"] = _path(G)
    F["result_el"] = _el(G)
    AB = F["ask_bands"]
    need_b = {"%s %s" % (k, t): AB[k]["need"][i] for k in ("KL", "OS") for i, t in enumerate(("1", "0.5"))}
    path_b = {"%s %d" % (k, y): AB[k]["by_year"][i] for k in ("KL", "OS") for i, y in enumerate(YEARS)}
    el_b = {k: AB[k]["el"] for k in ("KL", "OS")}
    hs = [m["house_share"] for m in M] + [F["house_share"]]
    lo_ = [m["loading_OS"] for m in M] + [G["OS"]["loading"]]
    sl = [m["link"][2] for m in M] + [F["link"]["bh"]]
    kb, ob = AB["KL"]["p5"], AB["OS"]["p5"]
    quick, careful = F["default_path"], rg["sector_independent_one_lgd"]
    S = F["sectors"]
    res = [
        dict(id="R1", name="the house-year's share of each standing", graded_as="Component 1",
             figure="result_house_share", depends=[], independent="", golden=F["house_share"],
             band=_span(hs, 0.01, 0.02), partly=_span(hs, 0.01, 0.10),
             passes=dict(quick=None, careful=F["estimates"]["ah"], thorough=F["house_share"])),
        dict(id="R2", name="Ostvale's loading on the economy's year", graded_as="Component 2",
             figure="result_os_loading", depends=[], independent="", golden=G["OS"]["loading"],
             band=_span(lo_, 0.01, 0.02), partly=_span(lo_, 0.01, 0.08),
             passes=dict(quick=F["estimates"]["am"],
                         careful=dict(value=S["pooled_l"], grade="partly",
                                      why="names the five sectors whose yearly default rates swing hardest and gives "
                                          "each a larger factor of its own, so their bad years arrive one sector at a "
                                          "time while the economy's year keeps one pooled loading (%.3f)" % S["pooled_l"]),
                         thorough=G["OS"]["loading"])),
        dict(id="R3", name="recovery per unit of the house-year's shock", graded_as="Component 3",
             figure="result_link_slope", depends=["R1"], independent="", golden=F["link"]["bh"],
             band=_span(sl, 0.01, 0.02), partly=_span(sl, 0.01, 0.08),
             passes=dict(quick=0.0, careful=0.0, thorough=F["link"]["bh"])),
        dict(id="R4", name="Kestrel Lane's five-year chance of loss", graded_as="Ask 2",
             figure="result_kl_p5", depends=["R1", "R3"], independent="", golden=G["KL"]["p5_pct"],
             band=kb, partly=[1.0, round(2 * kb[1], 1)],
             passes=dict(quick=quick["KL"]["p5_pct"], careful=careful["KL"]["p5_pct"], thorough=G["KL"]["p5_pct"])),
        dict(id="R5", name="Ostvale's five-year chance of loss", graded_as="Ask 2",
             figure="result_os_p5", depends=["R1", "R2", "R3"], independent="", golden=G["OS"]["p5_pct"],
             band=ob, partly=[1.0, round(2 * ob[1], 1)],
             passes=dict(quick=quick["OS"]["p5_pct"], careful=careful["OS"]["p5_pct"], thorough=G["OS"]["p5_pct"])),
        dict(id="R6", name="the recommendation", graded_as="Recommendation", figure="call",
             depends=["R4", "R5"], independent="", golden=F["call"],
             passes=dict(quick=quick["call"], careful=careful["call"], thorough=F["call"])),
        dict(id="R7", name="the subordination for 1 and 0.5 per cent", graded_as="Ask 4", figure="result_need",
             depends=["R1", "R2", "R3"], independent="", golden=F["result_need"], bands=need_b,
             passes=dict(quick=_need(quick), careful=_need(careful), thorough=F["result_need"])),
        dict(id="R8", name="the chance by each year end", graded_as="Ask 5", figure="result_path",
             depends=["R1", "R2", "R3"], independent="", golden=F["result_path"], bands=path_b,
             passes=dict(quick=_path(quick), careful=_path(careful), thorough=F["result_path"])),
        dict(id="R9", name="each portfolio's expected credit loss", graded_as="Ask 3", figure="result_el",
             depends=["R1", "R3"], independent="", golden=F["result_el"], bands=el_b,
             passes=dict(quick=_el(quick), careful=_el(careful), thorough=F["result_el"])),
    ]
    hk, ho = rg["sector_independent"], rg["sector_one_lgd"]
    hints = [
        dict(sentence="a sponsor house in a bad year lets its defaulted companies go for less, across the whole of its "
                      "book", rescues=[r for r, ok in (("R3", True),
                                                         ("R4", kb[0] <= hk["KL"]["p5_pct"] <= kb[1]),
                                                         ("R5", ob[0] <= hk["OS"]["p5_pct"] <= ob[1])) if ok]),
        dict(sentence="the capital-goods, building, freight, chemicals and car-parts companies default together in the "
                      "economy's bad years", rescues=[r for r, ok in (("R2", True),
                                                                      ("R5", ob[0] <= ho["OS"]["p5_pct"] <= ob[1])) if ok]),
        dict(sentence="companies held by one sponsor house default in the same years", rescues=[]),
    ]
    cw = rg["count_whole_book"]
    inb = lambda v, b: b[0] - 1e-9 <= v <= b[1] + 1e-9
    both = [("R2", True), ("R4", inb(cw["KL"]["p5_pct"], kb)), ("R5", inb(cw["OS"]["p5_pct"], ob)),
            ("R6", cw["call"] == F["call"]),
            ("R7", all(inb(v, need_b[c]) for c, v in _need(cw).items())),
            ("R8", all(inb(v, path_b[c]) for c, v in _path(cw).items())),
            ("R9", all(inb(v, el_b[c]) for c, v in _el(cw).items()))]
    hints.append(dict(sentence="defaults and recoveries cluster in a sponsor house's year, and five sectors load on the "
                               "economy", rescues=[r for r, ok in both if ok],
                      route="recovery read off each house-year's co-defaults across the house's whole book, with the "
                            "sector loadings and the house's year in the copula"))
    routes = [dict(name="the golden: sector loadings, the house's year, recovery on the house-year's shock",
                   answer=F["call"], golden=True)]
    routes.append(dict(name="the agencies' copula, one average loss", answer=F["default_path"]["call"],
                       KL=F["default_path"]["KL"]["p5_pct"], OS=F["default_path"]["OS"]["p5_pct"]))
    for key, label in (("house_pooled_lgd", "the house's year in the copula, one average loss"),
                       ("house_year_link", "recovery tied to the economy's year"),
                       ("sector_one_lgd", "the sector loadings, one average loss"),
                       ("sector_independent_one_lgd", "larger sector factors of their own, one average loss"),
                       ("house_link_pooled", "recovery on the house-year's shock, one pooled loading"),
                       ("sector_independent", "recovery on the house-year's shock, larger sector factors of their own"),
                       ("count_in_portfolio", "recovery read off the co-defaults among each note's own loans")):
        routes.append(dict(name=label, answer=rg[key]["call"], KL=rg[key]["KL"]["p5_pct"], OS=rg[key]["OS"]["p5_pct"]))
    return dict(results=res, hints=hints, routes=routes,
                weights=dict(recommendation=14, components=24, asks=55, instruction=7))
