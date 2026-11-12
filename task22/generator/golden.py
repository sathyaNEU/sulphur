"""task22 golden: the pack read back from target/ exactly as shipped (CSV, workbooks and PDFs), into the frames the
analysis runs on. Every graded figure is computed from these, never from the simulation."""
import os
import re
import subprocess

import pandas as pd

import pack as PK

STR = {"ServicePointID": str, "AccountNo": str, "MeterNo": str, "Date": str, "ReadDate": str, "BillDate": str,
       "Month": str, "Account": str, "Timestamp": str, "IntervalEnd": str, "DateTime": str, "Device": str}


def pdf_text(path):
    return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, check=True).stdout


def num(x):
    return float(x.replace(",", ""))


def study_table(path):
    """Tables 1 and 2 of the 2019 study, joined by feeder."""
    t1, t2 = {}, {}
    for line in pdf_text(path).splitlines():
        m = re.match(r"\s*((?:NTH|IND|APT|CHL)-\d)\s+(.*)$", line)
        if not m:
            continue
        v = [num(x) for x in re.findall(r"-?[\d,]+\.?\d*", m.group(2))]
        if len(v) == 6 and m.group(1) not in t1:
            t1[m.group(1)] = v
        elif len(v) == 6:
            t2[m.group(1)] = v
    rows = []
    for f, a in t1.items():
        b = t2[f]
        rows.append(dict(Feeder=f, Peak_MW=a[0], Energy_MWh=a[1], LoadFactor=a[2], LossFactor=a[3], Req_ohm=a[4],
                         PeakLoss_kW=a[5], Primary_MWh=b[0], NoLoad_MWh=b[1], LoadLoss_MWh=b[2], Secondary_MWh=b[3],
                         Technical_MWh=b[4], Technical_pct=b[5]))
    return pd.DataFrame(rows)


def cwp(path):
    t = pdf_text(path)
    segs = re.findall(r"OH-\d{6}", t)
    m = re.search(r"336\.4 ACSR", t)
    d = re.search(r"(January|February|March|April|May|June|July|August|September|October|November|December) "
                  r"(\d{1,2}), (20\d\d)", t[t.find("Reconductor"):])
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    iso = "%s-%02d-%02d" % (d.group(3), months.index(d.group(1)) + 1, int(d.group(2)))
    return dict(segments=sorted(set(segs)), new="336.4 ACSR" if m else None, in_service=iso)


def load(target):
    p = {k: os.path.join(target, v) for k, v in PK.FILES.items()}
    F = {"_bid": "pack:" + os.path.abspath(target)}
    F["dp"] = pd.read_csv(p["dp"], dtype=STR)
    F["scada"] = pd.read_csv(p["scada"], dtype=STR)
    F["scada"]["MW"] = pd.to_numeric(F["scada"]["MW"])
    F["scada"]["MVAR"] = pd.to_numeric(F["scada"]["MVAR"])
    F["reads"] = pd.read_csv(p["reads"], dtype=STR, keep_default_na=False, na_values=[""])
    for c in ("Register", "kWh", "RegisterRcv", "kWhRcv", "Multiplier", "Cycle"):
        F["reads"][c] = pd.to_numeric(F["reads"][c])
    F["reads"]["AccountNo"] = F["reads"]["AccountNo"].fillna("")
    F["lp_interval"] = pd.read_csv(p["lp_interval"], dtype=STR)
    F["lp_interval"]["kWh"] = pd.to_numeric(F["lp_interval"]["kWh"])
    F["oms_log"] = pd.read_csv(p["oms_log"], dtype=STR)
    F["lights_billing"] = pd.read_csv(p["lights_bill"], dtype=STR)
    F["lights_billing"]["DeemedkWh"] = pd.to_numeric(F["lights_billing"]["DeemedkWh"])
    F["lights_billing"]["Lamps"] = pd.to_numeric(F["lights_billing"]["Lamps"])
    gis = pd.read_excel(p["gis"], sheet_name=None, dtype={"ServicePointID": str})
    F["gis_segments"] = gis["Primary segments"]
    F["gis_switches"] = gis["Switches"]
    F["gis_xf"] = gis["Transformers"]
    F["gis_sp"] = gis["Service points"]
    F["gis_sp"]["ServicePointID"] = F["gis_sp"]["ServicePointID"].astype(str)
    F["xfmr_register"] = pd.read_excel(p["register"], dtype={"InstallDate": str, "RemovedDate": str})
    F["xfmr_register"]["RemovedDate"] = F["xfmr_register"]["RemovedDate"].fillna("")
    F["oms_xref"] = pd.read_excel(p["xref"])
    eng = pd.read_excel(p["eng"], sheet_name=None, header=2)
    F["conductors"] = eng["Conductors"]
    F["xfmr_losses"] = eng["Transformer losses"]
    F["lamp_watts"] = eng["Lamp input watts"]
    F["burn_hours"] = eng["Burning hours"]
    subs = pd.read_excel(p["subs"], sheet_name=None, header=2)
    F["subxf"] = subs["Power transformers"]
    F["station_service"] = subs["Station service"]
    F["station_service"]["Month"] = F["station_service"]["Month"].astype(str)
    F["lights_inventory"] = pd.read_excel(p["lights_inv"], dtype={"Account": str, "InstallDate": str,
                                                                   "LEDConversion": str})
    F["lights_inventory"]["LEDConversion"] = F["lights_inventory"]["LEDConversion"].fillna("")
    F["lights_inventory"]["LEDLampCode"] = F["lights_inventory"]["LEDLampCode"].fillna("")
    F["applications"] = pd.read_excel(p["apps"], dtype={"ServicePointID": str, "ServiceDate": str, "Requested": str})
    F["applications"]["ServicePointID"] = F["applications"]["ServicePointID"].fillna("")
    F["study2019"] = study_table(p["study"])
    F["cwp"] = cwp(p["cwp"])
    return F
