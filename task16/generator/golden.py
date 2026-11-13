"""task16: the pack read back the way an analyst reads it. Both patient indexes in one standardized record table, the
merge history, the blood bank results, the delivery log, the death notices, the engine's name equivalence table and
the pilot's reviewed pairs."""
import os
import re
import unicodedata

import numpy as np
import pandas as pd

import pack as PK

UNIT = re.compile(r"\s+(APT|UNIT|STE|SUITE|#|LOT|TRLR|BLDG)\b.*$")


def std_name(s):
    if not isinstance(s, str):
        return ""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().upper().replace("-", " ")
    s = re.sub(r"[^A-Z ]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def std_addr(s):
    if not isinstance(s, str) or not s.strip():
        return ""
    s = s.upper().strip()
    s = UNIT.sub("", s)
    return re.sub(r"\s+", " ", s)


def std_phone(s):
    d = re.sub(r"\D", "", s) if isinstance(s, str) else ""
    return d if len(d) == 10 else ""


def std_ssn(s):
    d = re.sub(r"\D", "", s) if isinstance(s, str) else ""
    return d if len(d) == 9 and d not in ("000000000", "999999999") else ""


def load(target):
    f = lambda k: os.path.join(target, PK.FILES[k])
    rd = lambda k: pd.read_csv(f(k), dtype=str, keep_default_na=False)
    a, b = rd("index_a"), rd("index_b")
    ra = pd.DataFrame(dict(
        sys="A", mrn=a["MRN"], first=a["FIRST_NAME"].map(std_name), last=a["LAST_NAME"].map(std_name),
        dob=pd.to_datetime(a["DOB"], format="%m/%d/%Y"), sex=a["SEX"], addr=a["ADDRESS"].map(std_addr),
        phone=a["HOME_PHONE"].map(std_phone), ssn=a["SSN"].map(std_ssn),
        created=pd.to_datetime(a["REG_DATE"], format="%m/%d/%Y %H:%M"),
        last_act=pd.to_datetime(a["LAST_ACTIVITY"], format="%m/%d/%Y")))
    rb = pd.DataFrame(dict(
        sys="B", mrn=b["PATIENT_ID"], first=b["PAT_FNAME"].map(std_name), last=b["PAT_LNAME"].map(std_name),
        dob=pd.to_datetime(b["BIRTH_DT"]), sex=b["GENDER_CD"], addr=b["STREET_ADDR"].map(std_addr),
        phone=b["PHONE_NUM"].map(std_phone), ssn=b["SSN_NUM"].map(std_ssn),
        created=pd.to_datetime(b["CREATED_TS"]), last_act=pd.to_datetime(b["LAST_ENC_DT"])))
    R = pd.concat([ra, rb], ignore_index=True)
    F = dict(R=R, index_a=a, index_b=b, merges=rd("merges"), blood=rd("blood"), deliveries=rd("deliveries"),
             names=rd("names"),
             pilot=pd.read_excel(f("pilot"), header=2, dtype=str, keep_default_na=False))
    return F
