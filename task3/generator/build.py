"""task3 architecture 4: cut the pack into a folder from the clean truth."""
import os

import numpy as np

import docs
import mapimg
import pack as K
import params as P
import world as W

FILES = {
    "results": "corlinden_raw_water_nitrate_results_1988-2026.csv",
    "pumping": "corlinden_well_pumping_daily_2009-2026.csv",
    "network": "ravell_county_groundwater_network_samples_1990-2026.csv",
    "sites": "ravell_county_groundwater_network_sites.xlsx",
    "landcover": "ravell_county_parcel_land_cover_1986-2026.csv",
    "whpa": "sallow_road_wellhead_protection_plan_2019.pdf",
    "attrs": "sallow_road_WHPA_parcel_attributes_2019.xlsx",
    "map": "sallow_road_WHPA_zones_figure3_2019.png",
    "ages": "ravell_county_groundwater_age_survey_2019.xlsx",
    "plan": "corlinden_water_supply_plan_2025.pdf",
    "logs": "sallow_road_well_construction_records.pdf",
    "spcap": "corlinden_well_specific_capacity_2008-2026.xlsx",
    "fert": "ravell_county_fertilizer_sales_1990-2025.csv",
}


def build_pack(target, seed=P.SEED):
    os.makedirs(target, exist_ok=True)
    truth = W.build(seed)
    rng = np.random.default_rng(seed + 1)
    K.assign_ids(truth, rng)
    p = {k: os.path.join(target, v) for k, v in FILES.items()}
    n = {}
    pump = K.pumping(truth, rng)
    truth["pump"] = pump
    n[FILES["results"]] = K.utility_results(p["results"], truth, pump, rng)
    n[FILES["pumping"]] = K.pumping_csv(p["pumping"], pump, rng)
    n[FILES["network"]] = K.network_samples(p["network"], truth, rng)
    n[FILES["sites"]] = K.network_sites(p["sites"], truth, rng)
    n[FILES["landcover"]] = K.land_cover(p["landcover"], truth, rng)
    n[FILES["attrs"]] = K.whpa_attributes(p["attrs"], truth, rng)
    n[FILES["ages"]] = K.age_survey(p["ages"], truth, rng)
    K.specific_capacity(p["spcap"], rng)
    n[FILES["fert"]] = K.fertilizer_sales(p["fert"], rng)
    docs.whpa_report(p["whpa"], truth)
    docs.supply_plan(p["plan"])
    docs.well_logs(p["logs"])
    mapimg.draw(p["map"])
    return n, truth
