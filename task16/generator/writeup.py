"""task16 submission.md: the four answer blocks, drafted from figures.json so every figure they state is one the
generator computed."""
import deliver as DL
import pack as PK


def n0(x):
    return "{:,.0f}".format(x)


def poisson_net(m, p_diff):
    """The 95 per cent interval on a rule's two-patient pairs from its clear discordant count (exact Poisson), net of
    the mislabelled specimens expected and scaled as the point estimate is."""
    from scipy.stats import chi2
    k, e = m["discordant_clear"], m["expected_one_patient_clear"]
    scale = m["links"] / max(m["typed_links_clear"], 1) / p_diff
    lo = chi2.ppf(0.025, 2 * k) / 2.0 if k > 0 else 0.0
    hi = chi2.ppf(0.975, 2 * k + 2) / 2.0
    return max(lo - e, 0.0) * scale, max(hi - e, 0.0) * scale


def rate_band(b, links):
    return [round(2000.0 * b[0] / links, 2), round(2000.0 * b[1] / links, 2)]


def derived(T, fo):
    """The figures the blocks state that are worked from others: each estimate's band per 2,000 links, the blood
    groups' interval on rule A, rule A's shares, the golden family's spread and each rule's line."""
    L, B = T["rule_links"], T["bands"]
    est = {"A": B["R2_rule_a_false"], "B": T["rule_b_band"], "C": B["R3_rule_c_false"], "D": B["R4_rule_d_false"]}
    lo, hi = poisson_net(T["marker"]["A"], T["marker_noise"]["p_diff"])
    fam = fo["forcing"]["golden_family"]
    av = [x["rule_a"] for x in fam if "rule_a" in x]
    return {"rate_bands": {k: rate_band(est[k], L[k]) for k in L},
            "marker_a_interval": [int(round(lo)), int(round(hi))], "interval_level": 95,
            "rule_a_shares_pct": {k: int(round(100 * v)) for k, v in T["rule_a_shares"].items()},
            "family_rule_a_range": [min(av), max(av)], "cap_lines": {k: round(L[k] / 2000.0, 1) for k in L},
            "family_rule_c_pair": next(x["rule_c"] for x in fam if "rule_c" in x),
            "family_rule_d_names": next(x["rule_d"] for x in fam if "rule_d" in x)}


def rb(T, k):
    return "%.2f to %.2f" % tuple(T["rate_bands"][k])


def write(figs, G, fo, path):
    T = figs
    L, F_, Rt = T["rule_links"], T["rule_false"], T["rule_rate_per_2000"]
    I = T["incumbent_rate_per_2000"]
    mk, nz = T["marker"], T["marker_noise"]
    B = T["bands"]
    FN = PK.FILES
    rule = T["R6_rule"]
    lines = []
    a = lines.append
    a("## Tags")
    a("")
    a("**Domain:** Machine Learning Research, General Statistics & Data Science (data integration, record linkage and "
      "entity resolution: a merged health system's enterprise master patient index).")
    a("**Analytical objective:** Data Extraction & Conformation (ETL / Pipeline Build).")
    a("")
    a("## Final Recommendation")
    a("")
    a("**Run Rule %s at the One Chart conversion:** it joins %s pairs of records and about %s of them are two different "
      "patients (%.2f per 2,000 automatic links, inside the policy's one). Reject Rule A, which the matching engine's "
      "chance rates put at %.2f per 2,000 but which merges about %s pairs of different patients (%.2f per 2,000) because "
      "Port Calder's first names run in birth cohorts within surname communities and many foreign-born patients' birth "
      "dates were recorded as 1 January; Rule C would merge about %s pairs of twins (%.2f per 2,000) and Rule D about %s "
      "(%.2f), mostly twins registered at Rosario under a parent's SSN." % (
          rule, n0(L[rule]), n0(F_[rule]), Rt[rule], I["A"], n0(F_["A"]), Rt["A"], n0(F_["C"]), Rt["C"], n0(F_["D"]),
          Rt["D"]))
    a("")
    a("## Supplementary Questions")
    a("")
    a("### %s" % DL.WORKBOOK)
    a("")
    order = sorted(L, key=lambda k: -L[k])
    est = {"A": ("%.1f" % F_["A"], B["R2_rule_a_false"]), "B": (n0(F_["B"]), T["rule_b_band"]),
           "C": (n0(F_["C"]), B["R3_rule_c_false"]), "D": (n0(F_["D"]), B["R4_rule_d_false"])}
    a("1. Rules sheet, one row per candidate rule ordered by automatic links, with columns rule, definition, automatic "
      "links, estimated false merges, false merges per 2,000 links and within the policy: %s." % "; ".join(
          "Rule %s %s links, %s false merges (%s to %s), %.2f per 2,000 (%s), %s" % (
              k, n0(L[k]), est[k][0], n0(est[k][1][0]), n0(est[k][1][1]), Rt[k], rb(T, k),
              "inside the policy" if Rt[k] <= 1.0 else "over it") for k in order))
    a("2. Index sheet and Overlays to split sheet: %s Calder Bay records hold two or more patients (%s to %s), each "
      "listed with its surviving MRN, name and birth date." % (n0(T["R5_overlays"]), n0(B["R5_overlays"][0]),
                                                               n0(B["R5_overlays"][1])))
    r1, b1 = T["R1_index"], B["R1_index"]
    a("3. Index sheet: %s distinct patients in the converted index (%s to %s) and %s patients held by both Calder Bay "
      "and Rosario (%s to %s)." % (n0(r1["distinct patients"]), n0(b1["distinct patients"][0]),
                                   n0(b1["distinct patients"][1]), n0(r1["patients in both indexes"]),
                                   n0(b1["patients in both indexes"][0]), n0(b1["patients in both indexes"][1])))
    a("4. Index sheet: %s patients still under more than one active record once Rule %s's links are made (%s to %s)."
      % (n0(T["R7_left_after_rule"]), rule, n0(B["R7_left_after_rule"][0]), n0(B["R7_left_after_rule"][1])))
    a("")
    a("### %s" % DL.MEMO)
    a("")
    a("5. One page: run Rule %s, with its links and false merges per 2,000; why not Rules A, C and D, each with its "
      "false merges per 2,000; the Calder Bay records that hold two or more patients; the distinct patients, the "
      "patients both indexes hold and the patients left under more than one record." % rule)
    a("")
    a("## Critical Components")
    a("")
    ba, bc = B["R2_rule_a_false"], B["R3_rule_c_false"]
    a("1. Rule A's false merges: **%.1f** (%s to %s) of its %s links, **%.2f per 2,000** (%s), from pairs of different "
      "patients who share first name, last name, sex and birth date." % (
          F_["A"], n0(ba[0]), n0(ba[1]), n0(L["A"]), Rt["A"], rb(T, "A")))
    a("2. Rule C's false merges: **%s** pairs of twins (%s to %s) among its %s links, **%.2f per 2,000** (%s), none of "
      "them a pair the 2026 pilot reviewed." % (n0(F_["C"]), n0(bc[0]), n0(bc[1]), n0(L["C"]), Rt["C"],
                                                rb(T, "C")))
    a("")
    a("## Step-by-Step")
    a("")
    a("1. Read %s and %s into one table of %s active records, compared as %s standardizes them (names upper-cased "
      "with hyphens as spaces, unit designators off the street address, ten-digit phones, all-zero and all-nine SSNs "
      "missing)." % (FN["index_a"], FN["index_b"], n0(T["active_records"]), FN["spec"]))
    a("2. Applied each rule of %s section 7.2 to every pair of active records across and within the two indexes: Rule "
      "A %s links, Rule C %s, Rule D %s, Rule B %s." % (FN["plan"], n0(L["A"]), n0(L["C"]), n0(L["D"]), n0(L["B"])))
    a("3. Rule A: the specification's national rates put chance agreement on all four fields at about one in 10 billion "
      "pairs (%.1f merges here) and the records' own field rates at %.1f, but first names run in birth cohorts within "
      "surname communities and many foreign-born patients' birth dates sit on 1 January; counting the pairs of patients "
      "who share first name, last name, sex and birth year, each pair's chance of one birth date taken from its surname "
      "community's 1 January and 1 July shares by decade (shrunk toward the decade's), gives %.1f false merges, %.2f "
      "per 2,000, %d per cent of them among Nguyen patients and %d per cent among patients born before 1980." % (
          T["indep_vendor"], T["indep_local"], F_["A"], Rt["A"], T["rule_a_shares_pct"]["nguyen"],
          T["rule_a_shares_pct"]["pre1980"]))
    ma = mk["A"]
    lo, hi = T["marker_a_interval"]
    a("4. Checked it on %s: of Rule A's links whose records both carry results, %d of %s differ in group, %d of them on "
      "a Calder Bay record that holds two patients and about %.0f what mislabelled specimens give (%d of %s records "
      "typed twice or more disagree with themselves); the %d left against %.1f expected give about %.0f (%d per cent "
      "interval %d to %d), but typed patients were born %d years earlier on average than Rule A's linked patients, "
      "in the cohorts where chance agreement sits, so the groups test the estimate rather than count it; read as they "
      "stand (%.0f) they would condemn Rule B too (%.0f)." % (
          FN["blood"], ma["discordant"], n0(ma["typed_links"]), ma["discordant"] - ma["discordant_clear"],
          ma["expected_one_patient_clear"], nz["disagreeing"], n0(nz["records"]), ma["discordant_clear"],
          ma["expected_one_patient_clear"], ma["net"], T["interval_level"], lo, hi,
          T["marker_a_birth_year"]["years_older"], ma["as_read"], mk["B"]["as_read"]))
    a("5. Rule C: %s reviewed none of Rule C's links, because twins and nickname pairs at one address score above its "
      "review band, and the blood groups see only the twins whose groups differ (%.0f); linking the index with what the "
      "rules never compare (two newborns of one delivery in %s, two records made on one registration visit, groups "
      "that differ) keeps %s pairs of twins apart that Rule C joins, %.2f per 2,000." % (
          FN["pilot"], mk["C"]["net"], FN["deliveries"], n0(F_["C"]), Rt["C"]))
    a("6. Rule D: a family's SSN on several children's records makes the links whose first names are not one person's "
      "(%s) look like the whole problem, but %s of the links whose names are one person's are twins a delivery or one "
      "visit shows, so Rule D merges %s pairs of two patients, %.2f per 2,000." % (
          n0(T["careful_rule_false"]["D"]), n0(T["rule_d_similar_named_twins"]), n0(F_["D"]), Rt["D"]))
    a("7. Overlays: %s shows Calder Bay's automatic merges from March 2019 joined new registrations on last name, birth "
      "date and sex alone; reading each retired record's first name against its survivor's (forms of one name in %s "
      "and typing slips as one patient), %s surviving records hold two or more patients, where every merge whose names "
      "differ as typed would give %s." % (FN["merges"], FN["names"], n0(T["R5_overlays"]),
                                         n0(T["overlays_as_typed"])))
    a("8. The linked index: Fellegi-Sunter weights fitted by EM on the candidate pairs, the evidence above keeping two "
      "patients apart and the merge history's retired records included, gives %s distinct patients, %s held by both "
      "indexes, and %s still under more than one active record once Rule %s's links are made (the specification's own "
      "fixed weights, at its automatic or its review cut-off, give figures inside the same bands)." % (
          n0(r1["distinct patients"]), n0(r1["patients in both indexes"]), n0(T["R7_left_after_rule"]), rule))
    a("9. Under %s section 3 only Rule %s is inside one false merge per 2,000 automatic links (%.2f), so the conversion "
      "runs it." % (FN["policy"], rule, Rt[rule]))
    a("")
    a("No other rule survives. Rule A stays over the cap however each community's 1 January share is estimated (%.1f "
      "to %.1f false merges against a line of %.1f), Rule C from the evidence on each linked pair alone still gives %s "
      "and Rule D from first names alone %s, and every rule read from the blood groups net of their errors leaves Rule %s "
      "the only one inside; each shortcut lands on another rule: the engine's checks keep Rule A, correcting Rule A "
      "alone moves the call to Rule C, correcting Rules A and C but not D moves it to Rule D, and the blood groups read "
      "as they stand condemn every rule." % (
          T["family_rule_a_range"][0], T["family_rule_a_range"][1], T["cap_lines"]["A"], n0(T["family_rule_c_pair"]),
          n0(T["family_rule_d_names"]), rule))
    open(path, "w").write("\n".join(lines) + "\n")
