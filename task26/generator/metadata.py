"""Write task26/metadata.json outside target/: clean provenance, as_of date, and unlabelled distractor list,
with zero leaks of estimation methods or stumps."""
import json

import docs
import pack as PK


def write(path):
    F = PK.FILES
    DF = docs.FILES
    sim_src = ("generated deterministically by the build's physical 66/22 kV distribution grid simulator "
               "(Vesterdal Nett AS, seed 2635; no external or public data)")
    meta = {
        "task": "task26",
        "as_of": "2027-01-20",
        "organisation": "Vesterdal Nett AS (fictional regional electric distribution network operator in western Norway)",
        "decision": "2027-2029 firm-capacity relief schedule across in-scope 66/22 kV distribution substations under Planning Standard NS-2026",
        "deliverables": [
            "a spreadsheet",
            "a CSV",
        ],
        "stated_inputs": [
            "85.0",
            "85.0%",
            "100.0",
            "100.0%",
            "2026",
            "2027-2029",
            "15-minute",
        ],
        "distractor_files": [
            F["dist_light"],
            F["dist_dga"],
            DF["tariff"],
        ],
        "files": {
            F["scada_sub"]: {
                "covers": "2026 hourly zone-substation SCADA active power, 22 kV LV bus voltage, and LTC tap step exports",
                "pulled": "2027-01-12",
                "license": "proprietary, fictional organisation",
                "source": sim_src,
            },
            F["gsp_v"]: {
                "covers": "2026 hourly 66 kV bus voltage recordings at regional 132/66 kV Grid Supply Points",
                "pulled": "2027-01-12",
                "license": "proprietary, fictional organisation",
                "source": sim_src,
            },
            F["cor_lines"]: {
                "covers": "Regional 66 kV radial sub-transmission line topology, segment lengths, and per-kilometer impedances",
                "pulled": "2026-11-12",
                "license": "proprietary, fictional organisation",
                "source": sim_src,
            },
            F["scada_fdr"]: {
                "covers": "2026 hourly 22 kV feeder SCADA active load log",
                "pulled": "2027-01-12",
                "license": "proprietary, fictional organisation",
                "source": sim_src,
            },
            F["fdr_m15"]: {
                "covers": "2026 periodic peak demand register resets by 22 kV circuit",
                "pulled": "2027-01-08",
                "license": "proprietary, fictional organisation",
                "source": sim_src,
            },
            F["bus_vph"]: {
                "covers": "2026 hourly three-phase 22 kV substation bus voltage measurements",
                "pulled": "2027-01-12",
                "license": "proprietary, fictional organisation",
                "source": sim_src,
            },
            F["ami_db"]: {
                "covers": "2026 heating-season single-phase AMI voltage, active power, and reactive power telemetry database",
                "pulled": "2027-01-14",
                "license": "proprietary, fictional organisation",
                "source": sim_src,
            },
            F["ref_pq"]: {
                "covers": "Autumn 2026 main-bay active-power interval metering log for selected modernized substations",
                "pulled": "2026-11-05",
                "license": "proprietary, fictional organisation",
                "source": sim_src,
            },
            F["ref_tracer"]: {
                "covers": "2025 field phase-tracer commissioning log for AMI-metered laterals on modernized substations",
                "pulled": "2025-12-05",
                "license": "proprietary, fictional organisation",
                "source": sim_src,
            },
            F["rev_xlsx"]: {
                "covers": "2026 monthly settled substation revenue meter active and net reactive energy totals",
                "pulled": "2027-01-11",
                "license": "proprietary, fictional organisation",
                "source": sim_src,
            },
            F["tx_xlsx"]: {
                "covers": "Substation transformer Firm N-1 MVA ratings, nameplate impedances, tap step settings, and feeder registry",
                "pulled": "2026-11-12",
                "license": "proprietary, fictional organisation",
                "source": sim_src,
            },
            F["gis_lat"]: {
                "covers": "GIS single-phase lateral asset connectivity, metering tier, and annual billed energy table",
                "pulled": "2026-12-18",
                "license": "proprietary, fictional organisation",
                "source": sim_src,
            },
            F["xwalk"]: {
                "covers": "2024 DMS migration crosswalk between legacy feeder IDs and SCADA feeder IDs",
                "pulled": "2024-11-18",
                "license": "proprietary, fictional organisation",
                "source": sim_src,
            },
            F["class_pf"]: {
                "covers": "Engineering manual nominal power factors by customer class",
                "pulled": "2024-04-11",
                "license": "proprietary, fictional organisation",
                "source": sim_src,
            },
            F["ctx_2025"]: {
                "covers": "2025 annual energy delivered and customer count summary by substation",
                "pulled": "2026-02-14",
                "license": "proprietary, fictional organisation",
                "source": sim_src,
            },
            DF["standard"]: {
                "covers": "Network Planning Standard NS-2026 governing 66/22 kV substation firm capacity and 2027-2029 relief tiers",
                "pulled": "2026-03-18",
                "license": "proprietary, fictional organisation",
                "source": sim_src,
            },
            F["dist_light"]: {
                "covers": "2026 municipal streetlighting circuit inventory",
                "pulled": "2027-01-07",
                "license": "proprietary, fictional organisation",
                "source": sim_src,
            },
            F["dist_dga"]: {
                "covers": "2026 quarterly transformer insulating-oil dissolved gas analysis laboratory results",
                "pulled": "2026-11-27",
                "license": "proprietary, fictional organisation",
                "source": sim_src,
            },
            DF["tariff"]: {
                "covers": "2026 published retail and commercial distribution network tariff schedule",
                "pulled": "2025-11-24",
                "license": "proprietary, fictional organisation",
                "source": sim_src,
            },
        },
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=1, sort_keys=True)
        f.write("\n")
