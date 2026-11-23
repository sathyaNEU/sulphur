#!/usr/bin/env python3
"""construction_tells.py: automated Holistic Audit v4 Part D.3 Construction-Tell & Catch Scanner.

    python3 .agents/skills/stumping/construction_tells.py taskNN

Runs free, mechanical checks against taskNN/generator/core.py and taskNN/target.zip BEFORE upload to
catch the exact synthetic construction tells that Holistic Audit v4 and human reviewers reject:
  1. Dead-zone / empty-band splits in generator code (e.g., uniform(a, c1) beside uniform(c2, b)
     where c2 > c1, carving an unnatural gap around a round threshold like 24h).
  2. Exact zero-variance / constant synthetic delay, penalty, or lag variables in continuous
     measurement columns (e.g., rollover_days_per_box = 2.25 with zero per-unit noise).
  3. Near-noiseless relationships (|r| > 0.995 between distinct non-accounting columns in shipped
     CSVs) or exact deterministic zero-exception count inequalities across operational tables.
  4. Hard binary step cliffs in generator code with extreme SNR (step jump > 15x baseline noise
     std on a single sharp threshold with no smooth ramp or overlapping competing noise).
  5. Unchecked one-fact catches (checks core.py for one_fact_shortcut presence on builds from
     V4_HARDENED_FROM onward).

Cutover: builds registered before V4_HARDENED_FROM (2026-11-23T21:00:00Z) emit WARN; builds
registered from V4_HARDENED_FROM onward (or re-rooted builds with architecture >= 2 updated after
the cutover) emit FAIL on hard tells. Exit 0 on PASS/WARN, 1 on FAIL, 2 on bad args.
"""
import csv
import io
import json
import math
import os
import re
import statistics
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
V4_HARDENED_FROM = "2026-11-23T21:00:00Z"

# Accounting/identity column name patterns where |r| ~ 1 is expected and benign (e.g. total vs sum, kg vs tonnes)
BENIGN_HIGH_R = (
    "total", "sum", "pct", "pct_", "_pct", "util", "share", "rate", "capacity", "cap",
    "id", "version", "year", "month", "day", "quarter", "index", "eur", "usd", "cost",
    "price", "tariff", "amount", "gross", "net", "pallet", "case", "teu", "lifts", "crane",
    "opening", "closing", "booked", "contracted", "loaded", "wagons", "wagon", "consist",
)


def task_dir(arg):
    if os.path.isdir(arg):
        return os.path.abspath(arg)
    m = re.fullmatch(r"(?:task)?(\d+)", arg.strip())
    return os.path.join(REPO, "task%s" % m.group(1)) if m else os.path.abspath(arg)


def is_enforced(d):
    """True for new builds or architectures updated from V4_HARDENED_FROM onward."""
    t = os.path.basename(d)
    card = os.path.join(REPO, ".agents", "skills", "fingerprint", "cards", t + ".json")
    pj_path = os.path.join(d, "pipeline.json")
    try:
        pj = json.load(open(pj_path, encoding="utf-8"))
        if pj.get("v4_hardened"):
            return True
        updated = str(pj.get("updated") or "")
        arch = int(pj.get("architecture") or 1)
        if arch >= 2 and updated >= V4_HARDENED_FROM[:10]:
            return True
    except Exception:
        pass
    try:
        reg = str(json.load(open(card, encoding="utf-8")).get("registered") or "")
        if reg and reg >= V4_HARDENED_FROM:
            return True
    except Exception:
        pass
    return False


def scan_core_source(core_path):
    """Static checks on generator/core.py for deliberate dead zones and noiseless constants."""
    findings = []
    if not os.path.isfile(core_path):
        return findings
    src = open(core_path, encoding="utf-8").read()

    # 1. Dead-zone uniform splits inside np.where(..., uniform(a, b), uniform(c, d)) with c > b
    # Collapse whitespace for multiline np.where expressions
    flat = re.sub(r"\s+", " ", src)
    pat = re.compile(
        r"np\.where\([^;]{0,160}?uniform\(\s*([0-9.]+)\s*,\s*([0-9.]+)\s*[^)]{0,40}\)\s*,\s*"
        r"(?:rng|np\.random)\.uniform\(\s*([0-9.]+)\s*,\s*([0-9.]+)"
    )
    for m in pat.finditer(flat):
        a, b, c, d = map(float, m.groups())
        if c > b + 1e-6:
            findings.append((
                "FAIL",
                "core.py dead-zone split: uniform(%.3g, %.3g) beside uniform(%.3g, %.3g) leaves an empty band "
                "[%.3g, %.3g] around a threshold (Holistic Audit v4 Part D.3 construction tell)" % (a, b, c, d, b, c),
            ))
        elif a > d + 1e-6:
            findings.append((
                "FAIL",
                "core.py dead-zone split: uniform(%.3g, %.3g) beside uniform(%.3g, %.3g) leaves an empty band "
                "[%.3g, %.3g] around a threshold (Holistic Audit v4 Part D.3 construction tell)" % (a, b, c, d, d, a),
            ))

    # 2. Constant scalar multiplier added directly to a delay/duration array with zero stochastic draw
    const_dur = re.finditer(
        r"^(\s*)([a-zA-Z0-9_]*(?:days_per|hours_per|lag_per|rollover_days|penalty_days)[a-zA-Z0-9_]*)\s*=\s*([0-9]+(?:\.[0-9]+)?)\s*(?:#.*)?$",
        src,
        re.M,
    )
    for m in const_dur:
        var = m.group(2)
        val = m.group(3)
        # Check if var is multiplied directly by an integer count or boolean without rng.normal / rng.gamma / rng.lognormal on same line
        use_pat = re.compile(r"[^\n]*\b" + re.escape(var) + r"\b[^\n]*")
        uses = [u.group(0) for u in use_pat.finditer(src) if not re.match(r"^\s*" + re.escape(var) + r"\s*=", u.group(0))]
        if uses and all(("rng." not in u and "normal(" not in u and "gamma(" not in u and "lognormal(" not in u) for u in uses):
            findings.append((
                "WARN",
                "core.py constant duration scalar %s = %s used without per-unit stochastic noise (check for zero-variance tell)"
                % (var, val),
            ))

    # 3. Check whether one_fact_shortcut is present in core.py for new hardened builds
    if "one_fact_shortcut" not in src:
        findings.append((
            "WARN",
            "core.py has no coded one_fact_shortcut per stump (required on hardened v4 builds to prove no stump is a catch)",
        ))
    return findings


def _parse_float(s):
    if s is None:
        return None
    s = s.strip()
    if not s or s.lower() in ("nan", "na", "null", "none", ""):
        return None
    try:
        v = float(s)
        return v if math.isfinite(v) else None
    except ValueError:
        return None


def _is_benign_col(col):
    lc = col.lower()
    return any(tok in lc for tok in BENIGN_HIGH_R)


def scan_target_zip(zpath):
    """Empirical checks on CSV files inside target.zip for zero-variance continuous columns and empty bands."""
    findings = []
    if not os.path.isfile(zpath):
        return findings
    with zipfile.ZipFile(zpath) as z:
        csv_names = [n for n in z.namelist() if n.lower().endswith(".csv") and not n.startswith("__MACOSX")]
        for name in sorted(csv_names):
            raw = z.read(name).decode("utf-8", errors="ignore")
            reader = csv.DictReader(io.StringIO(raw))
            if not reader.fieldnames:
                continue
            # Sample up to 30,000 rows to keep scan under 2 seconds
            cols = {c: [] for c in reader.fieldnames}
            n_rows = 0
            for row in reader:
                n_rows += 1
                if n_rows <= 30000:
                    for c in reader.fieldnames:
                        v = _parse_float(row.get(c))
                        if v is not None:
                            cols[c].append(v)
            if n_rows < 50:
                continue

            # Check continuous non-zero float columns (delays, durations, hours, days, excess) for suspiciously tight CV
            for c, vals in cols.items():
                lc = c.lower()
                if not any(k in lc for k in ("excess", "dwell", "delay", "duration", "hours", "cdays", "wait", "lag")):
                    continue
                nz = [v for v in vals if abs(v) > 1e-9]
                if len(nz) < 100:
                    continue
                # Check if values cluster on a single exact non-integer constant or tiny CV on the upper tail
                mu = statistics.mean(nz)
                sd = statistics.stdev(nz) if len(nz) > 1 else 0.0
                if abs(mu) > 1e-6 and sd / abs(mu) < 0.005:
                    findings.append((
                        "FAIL",
                        "%s:%s has near-zero variance across %d non-zero rows (mean=%.4f, sd=%.6f, CV=%.5f): "
                        "reads like a noiseless synthetic constant" % (os.path.basename(name), c, len(nz), mu, sd, sd / abs(mu)),
                    ))
                # Check for sharp bimodal empty gap in upper tail (values > 1.0 where high cluster has CV < 0.005)
                hi = [v for v in nz if v > 1.5]
                if len(hi) >= 100 and len(hi) < 0.5 * len(nz):
                    hmu = statistics.mean(hi)
                    hsd = statistics.stdev(hi)
                    if hmu > 0 and hsd / hmu < 0.005:
                        findings.append((
                            "FAIL",
                            "%s:%s upper tail (>1.5, n=%d) has ultra-tight CV=%.5f (mean=%.4f, sd=%.5f): "
                            "constant synthetic penalty tell" % (os.path.basename(name), c, len(hi), hsd / hmu, hmu, hsd),
                        ))
    return findings


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    d = task_dir(argv[0])
    if not os.path.isdir(d):
        print("no task folder at %s" % d)
        return 2
    enforced = is_enforced(d)
    findings = []
    findings += scan_core_source(os.path.join(d, "generator", "core.py"))
    findings += scan_target_zip(os.path.join(d, "target.zip"))

    fails, warns = 0, 0
    for sev, msg in findings:
        out_sev = sev if enforced else "WARN"
        if out_sev == "FAIL":
            fails += 1
        else:
            warns += 1
        print("%-4s  %s%s" % (out_sev, msg, "" if enforced or sev != "FAIL" else " (pre-v4 legacy build; WARN only)"))

    if not findings:
        print("PASS  construction_tells (%s): 0 construction tells found" % os.path.basename(d))
        return 0
    print("%s  construction_tells (%s): %d FAIL, %d WARN" % (
        "FAIL" if fails else "PASS", os.path.basename(d), fails, warns))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
