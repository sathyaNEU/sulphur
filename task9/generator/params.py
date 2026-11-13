"""task9 (architecture 3): the world's constants. Varnholt Halbleiter GmbH, Fab 2 (Dresden), a 300 mm automotive line.

Everything a mechanism needs is here, in the units the fab uses; world.py simulates the process from these and pack.py
writes the records the fab keeps. Nothing in the pack is written from this file directly except the documents' own
stated values (the ramp plan, the product sheet, the cost inputs, the line list)."""
import datetime as dt

SEED = 9033
TZ = "Europe/Berlin"
FIRM = "Varnholt Halbleiter GmbH"
FAB = "Fab 2"

# ---- calendar (local time)
EPOCH = dt.datetime(2025, 11, 3, 0, 0)          # day 0 of the simulation
FIRST_START = dt.datetime(2025, 11, 10)          # first lot start in the record
LAST_START = dt.datetime(2026, 9, 14)            # last production start that sorts before the pull
SORT_FROM = dt.datetime(2026, 1, 1)
SORT_TO = dt.datetime(2026, 10, 31, 23, 59)
PULL = dt.datetime(2026, 11, 6, 7, 40)           # the yield team's pull
BASE = (dt.datetime(2026, 1, 1), dt.datetime(2026, 3, 31, 23, 59))   # the prompt's baseline sort window
WIN = (dt.datetime(2026, 6, 1), dt.datetime(2026, 9, 30, 23, 59))     # the prompt's shortfall sort window
REVIEW = dt.date(2026, 11, 24)

# ---- the changes the record carries (process time)
T_SHOWERHEAD = dt.datetime(2026, 4, 6, 13, 20)   # DP2B showerhead SH-300-B replaced by SH-300-C (PM)
T_CM3_TUNE = dt.datetime(2026, 5, 11, 9, 5)       # CM3 ILD0 recipe rev 8: zone 5 pressure up
T_VFD_DOWN = dt.datetime(2026, 6, 2, 9, 40)       # SDS-OX1 loop pump VFD 51.5 Hz -> 38 Hz (energy project EP-114)
T_STANDBY_ON = dt.datetime(2026, 8, 10, 14, 5)    # VFD fault: standby pump P-02B at fixed full speed
T_STANDBY_OFF = dt.datetime(2026, 8, 24, 16, 30)  # VFD repaired, back on P-02A at 38 Hz
T_CHEM_LIFE = dt.datetime(2026, 7, 1, 6, 0)       # ECN-2026-0417: PGC T3 spike every 10 lots, change every 24 h
T_SDS_UPGRADE = dt.datetime(2026, 4, 21, 10, 15)  # SDS controller firmware: flow logged in gpm from here (texture)
T_MES_UPGRADE = dt.datetime(2026, 3, 2, 5, 0)     # MES upgrade: lot IDs written without the dot from here (texture)

# ---- products (die in mm; gross die computed on the grid; gate is the gate-oxide area per die relative to VX40)
PRODUCTS = {
    "VX40": dict(w=9.80, h=8.60, gate=1.00, polish_s=62.0, rf_s=92.0, recipe="CT-STD-11", design=0.986,
                 route="VX40-R7", kind="automotive MCU, 55 nm eFlash", value=9.80),
    "VP12": dict(w=7.20, h=6.10, gate=0.48, polish_s=58.0, rf_s=88.0, recipe="CT-STD-11", design=0.991,
                 route="VP12-R4", kind="power management IC", value=3.10),
    "VR90": dict(w=18.20, h=17.60, gate=1.70, polish_s=76.0, rf_s=186.0, recipe="CT-DEEP-07", design=0.981,
                 route="VR90-R1", kind="77 GHz radar SoC", value=41.00),
}
TEST_VEHICLE = "VR90-T"   # VR90's front-end test vehicle: runs to contact etch and M1, characterised at the design centre
WAFER_R = 150.0
EDGE_EXCL = 3.0           # mm: a die is printed and probed only if all four corners sit within 147 mm
LOT = 25

# lots started per week by product (production), and the test vehicle's starts by month
STARTS_PER_WEEK = {"VX40": 7, "VP12": 5}
TV_PER_WEEK = {2: 1, 3: 2, 4: 2, 5: 3, 6: 5, 7: 5, 8: 6, 9: 5}   # month -> VR90-T lots a week (2026)

# ---- tools at the five steps that matter, and the steps around them (the route's other tools carry nothing)
BENCHES = ["WB-1", "WB-2"]
DEP_TOOLS = ["DP1", "DP2", "DP3"]          # chambers A and B each; wafers alternate A/B by slot
CMP_TOOLS = ["CM1", "CM2", "CM3", "CM4"]
ETCH_TOOLS = ["ET1", "ET2", "ET3"]         # chambers A and B each
ETCH_CHAMBERS = [t + c for t in ETCH_TOOLS for c in "AB"]
DEP_CHAMBERS = [t + c for t in DEP_TOOLS for c in "AB"]
TV_CHAMBERS = ["ET1B", "ET3A"]             # the chambers qualified for CT-DEEP-07

# dispatch: DP2 sits in bay 3 beside CM3, so DP2's lots go to CM3 when it is free
CMP_AFFINITY = {"DP1": [0.30, 0.30, 0.10, 0.30], "DP2": [0.14, 0.13, 0.60, 0.13], "DP3": [0.30, 0.25, 0.15, 0.30]}

# ---- mechanism 1: the oxide slurry loop SDS-OX1 (taps in loop order: distance along the loop from the day tank, m)
LOOP_ORDER = ["CM2", "CM4", "CM1", "CM3"]
TAP_M = {"CM2": 64.0, "CM4": 148.0, "CM1": 231.0, "CM3": 318.0}
LOOP_M = 402.0
V_NOM, V_LOW, V_STANDBY = 1.62, 1.02, 1.86     # m/s
AGGLOM = 0.0019        # per second of residence: large particles grow ~exp(AGGLOM * t_res)
SETTLE_V = 1.30        # below it the loop settles and agglomeration doubles in the slow sections
SETTLE_GAIN = 2.6
LPC_TANK = 1650.0      # counts/mL > 0.56 um at the tank outlet, fresh tote
LPC_TANK_AGE = 0.11    # per day of tote age
TOTE_DAYS = (2.1, 3.0)
POU_DAYS = 21.0        # point-of-use filter change interval (planned)
POU_PASS0, POU_PASS_DAY = 0.34, 0.021
SCR_BASE = 18.2        # scratches per wafer at pass 1.0, per 60 s polish, at the reference count
SCR_REF = 1700.0       # counts/mL
SCR_POW = 2.15          # scratching agglomerates grow faster than the count above the cut
SCR_KILL = 0.62
SCR_LEN_MM = 0.9       # median micro-scratch length

# ---- mechanism 2: the pre-gate clean bath (tank T3, 52 L) metals
BATH_L = 52.0
SPIKE_L = 6.0
C_FRESH = 0.22         # ppb after a change
DRAG_PPB = 0.0043      # ppb per wafer of drag-in (all lots through the tank)
SPRING = dict(spike_lots=6, change_h=12)
SUMMER = dict(spike_lots=10, change_h=24)
BG_LOTS_PER_DAY = {"WB-1": 26.0, "WB-2": 23.5}   # other lots through each bench (the fab's other products)
Q1_LOTS_PER_DAY = 31.0                            # the ramp plan's bench loading for Q1 2027
C_TH = 1.25            # ppb above which gate-oxide integrity degrades
GOI_K = 0.060         # kill probability per die per ppb^1.2 above the threshold, at gate 1.0
GOI_EXP = 1.2

# ---- mechanism 3: the ILD0 edge profile (DP2B's new showerhead thick, CM3's rev 8 zone 5 removes more)
ILD_NOM = 605.0        # nm deposited
REMOVE_NOM = 300.0
DP2B_EDGE = 33.0       # nm thicker at the edge with SH-300-C
CM3_EDGE = 35.0        # nm more removal at the edge with rev 8
EDGE_R0 = 118.0        # mm: the profile starts here
EDGE_POW = 1.6
TOL_THICK, TOL_THIN = 14.0, 14.0     # nm: the process window each side
EDGE_SCALE = 7.0       # nm: kill rises as 1 - exp(-(offset beyond the window) / scale)
KILL_THICK, KILL_THIN = 0.70, 0.48
CHAMBER_STATIC = {"DP1A": 2.0, "DP1B": -1.5, "DP2A": 0.5, "DP2B": 1.0, "DP3A": -2.5, "DP3B": 1.5}
CMP_STATIC = {"CM1": 1.5, "CM2": -2.0, "CM3": 0.5, "CM4": 1.0}
EDGE_NOISE = 5.5

# ---- mechanism 4: contact-etch polymer (equivalent RF seconds: RF seconds times the recipe's polymer factor)
CHEM = {"CT-STD-11": 1.0, "CT-STD-09": 1.0, "CT-DEEP-07": 1.70}
CLEAN_WAFERS = 2400
L_TH = 196000.0
FLAKE_A = 13.0          # particle adders per wafer at (excess/1e4)^1.5 = 1
FLAKE_POW = 1.5
PRT_BASE = 3.0
PRT_KILL = 0.33
ETCH_WAFERS_PER_WEEK = 640.0     # each chamber's loading (all products)
Q1_TV_SHARE = 0.21               # VR90's share of ET1B and ET3A in Q1 2027 under the ramp plan

# ---- mechanism 5: random defects (line-wide), clustered
D0 = 0.122             # defects per cm2 (killer) at the baseline
ALPHA_WAFER = 1.5      # gamma shape of the wafer-to-wafer multiplier
ALPHA_REGION = 0.62    # gamma shape of the within-wafer regional multiplier (regions of about 40 mm)
REGION_MM = 40.0
DRIFT_WEEKS = 0.06     # week-to-week variation of the line's defect level (sd of log multiplier, no trend)

# ---- the ramp plan for Q1 2027 (as filed)
PLAN = dict(commitment_units=412000, assembly=0.992, final_test=0.981, vfd_hz=38.0, chem_life="ECN-2026-0417",
            cm3_harmonise=dt.date(2027, 1, 4), dp2b_part="SH-300-C", etch_clean_wafers=2400,
            vr90_chambers=TV_CHAMBERS, bench_lots_per_day=Q1_LOTS_PER_DAY, vr90_lots_per_week=12)

PEOPLE = {"yield": "Gitte Ullrich", "cmp": "Matthias Hertrampf", "fac": "Sofia Sorgatz", "wet": "Hüseyin Siering",
          "etch": "Detlev Lindau", "plan": "Isabelle Hamann", "fin": "Gunhild Scheibe", "lab": "Oswald Dobes",
          "dep": "Andrei Dörr", "maint": "Roy Heuser"}
TECHS = ["R. Heuser", "M. Schleich", "O. Fliegner", "A. Beckmann", "M. Atzler", "W. Zimmer"]
FAC_STAFF = {"chem": "S. Sorgatz", "day": "H. Kaul", "night": "E. Schacht"}     # facilities: distribution, day shift, on call
LAB_STAFF = ["O. Dobes", "C. Mülichen"]                                       # the lab's ICP-MS rota, week about
SHIFT_LEADS = ["F. Döring", "A. Bohlander", "R. Walter", "D. Mende"]          # FT2 crews A to D
