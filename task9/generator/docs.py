"""task9: the pack's documents in their owners' own genres: the CMP module's maintenance-spec history with the waiver
text, the yield excursion ticket, finance's cost inputs and the yield system's die-geometry helper. None says how to
analyse anything.
"""
import params as P

SPEC = """# ILD-CMP preventive maintenance specification: revision history

Owner: {cmp} (CMP module engineering). Applies to polish units PU-1 to PU-4, ILD-CMP step.

| Rev | Effective | Full PM interval | Full PM scope | Pad change |
|---|---|---|---|---|
| D | 2025-02-17 | 1,800 wafers | polishing pad, conditioner disk, retaining ring; platen and carrier inspection | every 600 wafers +/- 50 |
| E | 2025-09-08 | 2,000 wafers | as Rev D | every 600 wafers +/- 50 |
| F | 2026-04-02 | 2,800 wafers | as Rev D | every 600 wafers +/- 50 |

Intervals count wafers polished on the unit since its last full PM. Rev F extends the interval on the pad supplier's
extended-life data (ECN-4471, approved by the module review on 2026-03-26).

Unscheduled part changes (a damaged conditioner disk, a chipped or worn retaining ring) are made as found and entered
in the unit's maintenance log; they do not restart the full PM count.

## Rev G (draft for the September module review)

The part found responsible for the edge ring under YE-2026-031 comes out of the full PM scope and is changed on its own
count of wafers polished since it was last replaced, the count set for each unit from the excursion review. The full PM
keeps its 2,800-wafer interval and its scope for the other parts, and pads stay at every 600 wafers +/- 50.

## Engineering waiver EW-118

Raised by {maint} on 2026-05-29. Approved for 2026-06-01 to 2026-08-14.

Conditioner disk supply is short until the supplier's August shipment. At full PMs on PU-1 to PU-4 during the waiver
period the installed conditioner disk may be retained if it passes visual inspection, for at most four full PMs in
total. Pad and retaining ring are replaced as normal. The technician records the retained disk in the PM entry.
""".format(cmp=P.PEOPLE["cmp"], maint=P.PEOPLE["maint"])

TICKET = """YIELD EXCURSION TICKET  YE-2026-031
Opened: 2026-06-15 08:42  by {yl} (Yield Engineering)
Area: Fab 2 / sort  Products: P-A, P-B, P-C
Status: OPEN  Priority: 2

Symptom: the share of wafers the defect classifier labels EDGE_RING has risen since April on all three products. Sort
maps show a ring of failing die at the wafer edge; interior yield looks normal on the same wafers.

Requested: cause, the yield it has cost, and a containment or spec action for the module review.

Notes:
2026-06-16  Commonality run requested from the yield database. (KB)
2026-06-22  Die maps added to the review set. (KB)
2026-07-30  Still open; carried to the August module review. (KB)
""".format(yl=P.PEOPLE["yield_lead"])

DIE_GEOMETRY = '''"""Fab 2 yield database: die position helpers (sort map conventions, rev 3).

Die (col, row) indices are counted from the wafer centre; col 0 / row 0 is the die whose lower-left corner sits at the
centre. Positions are in millimetres on a 300 mm wafer. Zones are radial bands of the die centre, numbered from the
centre outwards.
"""
import math

ZONE_EDGES_MM = [0, 40, 62, 80, 95, 108, 120, 136, 147]


def die_center(col, row, die_w_mm, die_h_mm, x_offset_mm=0.0, y_offset_mm=0.0):
    """Centre of die (col, row) in wafer coordinates (mm)."""
    return (col + 0.5) * die_w_mm + x_offset_mm, (row + 0.5) * die_h_mm + y_offset_mm


def die_radius(col, row, die_w_mm, die_h_mm, x_offset_mm=0.0, y_offset_mm=0.0):
    x, y = die_center(col, row, die_w_mm, die_h_mm, x_offset_mm, y_offset_mm)
    return math.hypot(x, y)


def zone_of(radius_mm):
    """Sort zone 1 to 8 for a die centre at this radius."""
    for k in range(1, len(ZONE_EDGES_MM)):
        if radius_mm < ZONE_EDGES_MM[k]:
            return k
    return len(ZONE_EDGES_MM) - 1
'''


def costs_yaml():
    c = P.COSTS
    req = c["requal_hours"] * c["tech_rate"]
    pad_all = c["pad_part"] + req + c["pad_hours"] * c["downtime_rate"]
    disk_all = c["disk_part"] + req + c["disk_hours"] * c["downtime_rate"]
    ring_all = c["ring_part"] + req + c["ring_hours"] * c["downtime_rate"]
    full_all = c["pad_part"] + c["disk_part"] + c["ring_part"] + req + c["full_pm_hours"] * c["downtime_rate"]
    L = ["# ILD-CMP cost inputs for maintenance decisions (fab finance, {fin}; updated 2026-08-28)".format(fin=P.PEOPLE["finance"]),
         "currency: USD",
         "parts:",
         "  polishing_pad: %d" % c["pad_part"],
         "  conditioner_disk: %d" % c["disk_part"],
         "  retaining_ring: %d" % c["ring_part"],
         "labour:",
         "  technician_rate_per_hour: %d" % c["tech_rate"],
         "  requalification_hours: %d        # monitor wafers and sign-off after any part change on a unit" % c["requal_hours"],
         "downtime:",
         "  unit_downtime_per_hour: %d       # lost ILD-CMP capacity, valued at the fab's marginal wafer" % c["downtime_rate"],
         "  pad_change_hours: %d" % c["pad_hours"],
         "  disk_change_hours: %d" % c["disk_hours"],
         "  ring_change_hours: %d" % c["ring_hours"],
         "  full_pm_hours: %d" % c["full_pm_hours"],
         "all_in:                            # part, requalification and downtime for one change on one unit",
         "  pad_change: %d" % pad_all,
         "  disk_change: %d" % disk_all,
         "  ring_change: %d" % ring_all,
         "  full_pm: %d                      # pad, disk and ring together" % full_all,
         "spec_changes: >",
         "  A part moved out of the full PM onto its own count is costed at its own change's all-in each time it is",
         "  changed, and the full PM then costs its all-in less that part's price.",
         "volume:",
         "  wafers_per_year_ild_cmp: %d" % c["wafers_per_year"],
         "die:"]
    for prod, p in P.PRODUCTS.items():
        L.append("  %s:" % prod)
        L.append("    value_per_good_die: %.2f" % p["value"])
    L.append("")
    return "\n".join(L), dict(pad=pad_all, disk=disk_all, ring=ring_all, full=full_all)
