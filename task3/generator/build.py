"""task3 architecture 3: cut the pack into a folder from the clean truth."""
import os

import numpy as np

import docs
import mapimg
import pack as K
import params as P
import world as W

FILES = {
    "transducers": "PW-1_constant_rate_2026-09_transducers.csv",
    "baro": "barologger_BL-2231_2026-09.csv",
    "notes": "PW-1_constant_rate_2026-09_field_readings.xlsx",
    "step": "PW-1_step_drawdown_2026-08-27.csv",
    "mor": "harlow_springs_MOR_well_production_2009-2026.csv",
    "msmw": "mill_street_MW_water_levels_2008-2026.csv",
    "network": "cvwcd_network_water_levels_2005-2026.csv",
    "register": "cvwcd_well_register.xlsx",
    "rule": "CVWCD_Rule_WR-4_groundwater_withdrawal_permits.pdf",
    "application": "reidel_road_WR-4_application_requested_schedules.pdf",
    "logs": "drillers_logs_corrin_valley_wells.pdf",
    "map": "CVWCD_bedrock_surface_plate3_harlow_reach.png",
    "quality": "PW-1_raw_water_quality_2026-09.xlsx",
}


def build_pack(target, seed=P.SEED):
    os.makedirs(target, exist_ok=True)
    truth = W.build(seed)
    rng = np.random.default_rng(seed + 1)
    p = {k: os.path.join(target, v) for k, v in FILES.items()}
    n = {}
    n[FILES["transducers"]] = K.write_test(p, truth, rng)["rows"]
    K.write_step_test(p["step"], rng)
    n[FILES["mor"]] = K.write_mor(p["mor"], truth, rng)
    n[FILES["msmw"]] = K.write_msmw(p["msmw"], truth, rng)
    n[FILES["network"]] = K.write_network(p["network"], truth, rng)
    K.write_register(p["register"])
    K.write_water_quality(p["quality"], rng)
    docs.rule_wr4(p["rule"])
    docs.application_summary(p["application"])
    docs.drillers_logs(p["logs"])
    mapimg.draw(p["map"])
    return n, truth
