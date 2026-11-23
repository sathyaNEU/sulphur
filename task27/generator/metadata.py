"""Emit leak-free task27/metadata.json recording as_of, distractors, and file provenance (Arch 2)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import pack as PK  # noqa: E402

SRC = (
    "generated deterministically by the build's physical North Sea refrigerated import network "
    "simulator (Weserfrucht Import GmbH, seed 2701; no external or public data)"
)
LIC = "proprietary, fictional organisation"

META = {
    "as_of": "2027-01-19",
    "decision": "2026 cold-chain non-carrier delay attribution and EUR 1.75M 2027 corridor carrier-remediation capital allocation under Charter RC-2027",
    "deliverables": [
        "a CSV",
        "a spreadsheet",
        "a short slide deck",
    ],
    "distractor_files": [
        PK.FILES["dist_bunker"],
        PK.FILES["dist_maut"],
    ],
    "files": {
        PK.FILES["bip_notices"]: {
            "covers": "2026 EU TRACES border phytosanitary inspection electronic notices at CHED consignment level",
            "license": LIC,
            "pulled": "2027-01-12",
            "source": SRC,
        },
        PK.FILES["disputes"]: {
            "covers": "2026 counterparty commercial detention and demurrage dispute credit close-out workbook",
            "license": LIC,
            "pulled": "2027-01-12",
            "source": SRC,
        },
        PK.FILES["dc_inv"]: {
            "covers": "2026 daily facility-level pallet inventory on hand and capacity across the four inland cold stores",
            "license": LIC,
            "pulled": "2027-01-13",
            "source": SRC,
        },
        PK.FILES["milestones"]: {
            "covers": "2026 container-level import lifecycle timestamps, corridor assignments, stage excess container-days, and TMS exception codes",
            "license": LIC,
            "pulled": "2027-01-14",
            "source": SRC,
        },
        PK.FILES["consignments"]: {
            "covers": "2026 customs bill-of-lading register linking containers to vessels, CHED lots, origins, and declared cargo weights",
            "license": LIC,
            "pulled": "2027-01-12",
            "source": SRC,
        },
        PK.FILES["chambers"]: {
            "covers": "Inland distribution center thermal chamber bay capacities, temperature setpoints, and 2026 opening stocks",
            "license": LIC,
            "pulled": "2026-12-19",
            "source": SRC,
        },
        PK.FILES["portal"]: {
            "covers": "2026-2027 daily port-by-ocean-line empty-container return portal booking confirmations and quota-closed rejection counts",
            "license": LIC,
            "pulled": "2027-01-19",
            "source": SRC,
        },
        PK.FILES["turnin"]: {
            "covers": "2026 physical empty-depot gate arrival and turn-in event log across North Sea port depots",
            "license": LIC,
            "pulled": "2027-01-14",
            "source": SRC,
        },
        PK.FILES["crosswalk"]: {
            "covers": "Legacy-to-canonical identifier crosswalk for retail store codes and regional drayage carriers",
            "license": LIC,
            "pulled": "2026-09-18",
            "source": SRC,
        },
        PK.FILES["dist_maut"]: {
            "covers": "2026-2027 German federal Autobahn LKW-Maut per-km toll rates and port-to-DC highway distances",
            "license": LIC,
            "pulled": "2026-12-04",
            "source": SRC,
        },
        PK.FILES["budgets_2027"]: {
            "covers": "Approved 2027 corridor package budgets, capture rates, corridor growth and port capacity factors, and daily detention tariffs",
            "license": LIC,
            "pulled": "2026-11-25",
            "source": SRC,
        },
        PK.FILES["dist_bunker"]: {
            "covers": "2026 weekly Rotterdam and Hamburg marine bunker fuel spot indices and EU ETS surcharges",
            "license": LIC,
            "pulled": "2027-01-08",
            "source": SRC,
        },
        PK.FILES["shuttles"]: {
            "covers": "2026 every-3-day Nordbahn corridor block-train departures, booked and loaded slots, rollovers, short-consist and loco derate events, wagon counts, and weighbridge tonnage",
            "license": LIC,
            "pulled": "2027-01-12",
            "source": SRC,
        },
        PK.FILES["skus"]: {
            "covers": "Fresh-produce SKU catalog mapping SKUs to produce families, thermal zones, and case-to-pallet conversion factors",
            "license": LIC,
            "pulled": "2026-12-22",
            "source": SRC,
        },
        PK.FILES["port_yard"]: {
            "covers": "2026 daily North Sea port terminal reefer-yard utilization, container lifts, and crane hours",
            "license": LIC,
            "pulled": "2027-01-11",
            "source": SRC,
        },
        PK.FILES["pallets"]: {
            "covers": "2026 daily SKU-level inbound and outbound warehouse movements across all four inland cold stores",
            "license": LIC,
            "pulled": "2027-01-13",
            "source": SRC,
        },
        PK.FILES["charter"]: {
            "covers": "Weserfrucht Cold-Chain Detention and Demurrage Charter RC-2027 (Rev 3) defining network scope, tariff tables, 2027 projection rules, budget-cap selection rule, and tracker filing format",
            "license": LIC,
            "pulled": "2026-11-18",
            "source": SRC,
        },
    },
}


def write(out_path=None):
    out_path = out_path or os.path.join(TASK_DIR, "metadata.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(META, f, indent=1, sort_keys=True)
    return out_path


if __name__ == "__main__":
    p = write()
    print("Wrote", p)
