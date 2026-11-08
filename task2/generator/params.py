"""task2 architecture 4: the Mount Carrow world, every constant in one place.

The truth: gold grades in the Stage 5 cutback follow a lognormal field with a long structure (about 60 m across, 24
m vertically), a short one (about 9 m) and a large nugget at sample scale. Ironbark sells Stage 5's high-grade ore
(5 m by 5 m by 2.5 m mining blocks at 2.0 g/t or more) to Tallowood's Yarrabin mill and must commit a contained-gold
tier for 2027 and 2028. The drilling is a 25 m grid with 12.5 m infill where the first holes ran high."""
import math

SEED = 20261108
AS_OF = "2026-11-06"

# the grid of the truth: 2.5 m cells over 300 m (east) by 400 m (north) by 100 m (down from RL 400)
D = 2.5
NX, NY, NZ = 120, 160, 40
TOP_RL = 400.0
GRID_E0, GRID_N0 = 1000.0, 2000.0           # mine grid of the cell origin
MGA_SHIFT = (339250.0, 6601480.0)           # MGA94 zone 51 = mine grid + shift (the 2022 conversion)

# grade field: log-grade = MU + S_LONG * long + S_SHORT * short (+ the sample nugget)
MU = math.log(0.70)
S_LONG, R_LONG, AN_LONG = 0.50, 60.0, 0.4
S_SHORT, R_SHORT, AN_SHORT = 0.40, 9.0, 0.6
S_NUG_1M = 0.80               # multiplicative scatter of a 1 m sample about its cell
S_ASSAY = 0.10                # the laboratory's own scatter (field duplicates carry both)

# drilling
GRID_SPACING = 25.0
INFILL_SPACING = 12.5
INFILL_TRIGGER = 1.35          # mean grade (g/t) of the nearest 2019-2021 holes that drew the 2022-2024 infill

# the decision
SMU = (5.0, 5.0, 2.5)
CUT = 2.5
TIERS = [("A", 75), ("B", 125), ("C", 200)]   # contained gold, thousand ounces, at the cut-off
OZ = 31.1035

# Stage 5 design: flitch k (k = 0 at RL 400 to 397.5) is a rectangle on the mine grid stepping in each flitch
S5_TOP = (1012.0, 1288.0, 2012.0, 2388.0)
S5_STEP = 0.75
S5_FLITCHES = 38               # RL 400 down to RL 305

# weathering (RL of the base of oxide and of transitional, smooth surfaces) and densities (t/m3)
OX_BASE = 373.0
TR_BASE = 359.0
DENSITY = {"OX": 2.12, "TR": 2.47, "FR": 2.75}
