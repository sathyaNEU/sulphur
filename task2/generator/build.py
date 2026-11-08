"""task2 architecture 4: cut the pack into a folder from the clean truth."""
import os

import numpy as np

import docs
import pack as K
import params as P
import planimg
import world as W

FILES = {
    "collars": "MC_drillhole_collars.csv",
    "assays": "MC_drillhole_assays.csv",
    "qaqc": "MC_qaqc_results_2019-2024.csv",
    "density": "MC_bulk_density.csv",
    "weathering": "MC_weathering_logs.csv",
    "design": "MC_stage5_design_flitches.csv",
    "terms": "Yarrabin_OPA_2027-2028_term_sheet.pdf",
    "plan": "MC_2027_mine_plan_summary.pdf",
    "map": "MC_stage5_drilling_plan.png",
    "metallurgy": "MC_metallurgical_testwork_2025.xlsx",
    "survey": "MC_stage4_survey_pickup_2026-09.csv",
}


def build_pack(target, seed=P.SEED):
    os.makedirs(target, exist_ok=True)
    truth = W.build(seed)
    p = {k: os.path.join(target, v) for k, v in FILES.items()}
    n = K.write_all(p, truth)
    rng = np.random.default_rng(seed + 7)
    K.write_metallurgy(p["metallurgy"], rng)
    K.write_survey(p["survey"], rng)
    docs.term_sheet(p["terms"])
    docs.plan_summary(p["plan"], len(truth["holes"]))
    planimg.draw(p["map"], truth["holes"], K.hole_ids(truth["holes"]))
    return n, truth
