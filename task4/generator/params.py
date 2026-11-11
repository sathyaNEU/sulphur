"""task4 architecture 10: the world's constants. Vehkasalon Liikenne Oy (a municipally owned regional bus operator
in the Finnish lake district), its Niittylä depot, 48 weekday blocks, a six-bus electric pilot, and the 2027 order."""
import datetime as dt

SEED = 41007
PRIORITY_SEED = 2                    # the planner's order inside each zone
ORG = "Vehkasalon Liikenne Oy"
DEPOT = "Niittylä"
TOWN = "Vehkasalo"
DSO = "Vehkasalon Sähköverkko Oy"
DEALER = "Pohjanmaan Bussihuolto Oy"
EMAKE, EMODEL = "Lintula", "L12E"
PEOPLE = {"planner": "Simo Virta", "fleet": "Eveliina Pajunen", "dealer": "Juhani Nousiainen", "dso": "Kaarina Peltola"}

START, END = dt.date(2024, 1, 1), dt.date(2026, 10, 31)      # the operating records
ASOF = dt.date(2026, 11, 6)
TEMP_START = dt.date(2016, 1, 1)
NEW_CODES_FROM = dt.date(2025, 8, 11)                          # the planning system's new block codes
EBUS_BATCH = {1201: dt.date(2025, 3, 3), 1202: dt.date(2025, 3, 3), 1203: dt.date(2025, 3, 3),
              1204: dt.date(2025, 6, 2), 1205: dt.date(2025, 6, 2), 1206: dt.date(2025, 6, 2)}
E_USABLE_PILOT = 480.0        # kWh, the pilot buses' usable battery when new (the same model family as the quoted one)
E_USABLE_2027 = 480.0         # kWh, the quoted 2027 model
SHARE = 0.85                  # the standard's limit share
DESIGN_T = -15.0              # the design day's daily mean, degrees C
SUPPLY_KW = 690.0             # the charging installation's capacity in the night period (the connection agreement)
NIGHT_FROM, NIGHT_TO = 21 * 60, 7 * 60   # the night period, local time: charging only between these
CHARGER_KW = 150.0
ETA_CHARGE = 0.945            # energy into the traction battery over the energy the charger takes at the connection point
COND_BASE = 0.35              # kW while plugged in and released: the bus's 24 V system, the BMS and the outlet's own standby
COND_SLOPE = 0.15             # kW per degree of the night below COND_T0: the traction battery held at its charging temperature
COND_T0 = 5.0                 # degrees C, the night's mean below which the battery's thermal management heats
REF_YEAR = (dt.date(2025, 11, 1), dt.date(2026, 10, 31))     # the twelve months for the diesel figures
FUEL_KWH_PER_L = 9.8          # HVO / diesel, lower heating value
BURNER_EFF = 0.9157   # 35 kW at 3.9 l/h, the heater's own rating

# battery-electric energy (the physics the pilot buses obey)
E0, E_CLIMB, E_DIFF = 0.76, 0.012, 0.75     # kWh per km: base, per m/km of climb, per unit of difficulty
P_AUX = 2.2                                  # kW: lights, compressor, steering, electronics, over the block's hours
T_IN, UA = 19.0, 0.36                        # cabin set point and heat loss, kW per K
P_CAP_PILOT = 8.0                            # kW thermal, the pilot buses' electric heating capacity
FUEL_HEATER_ON = 1.0                         # the pilot's fuel heater is enabled below this ambient
HP_FLOOR_T = -10.0                           # heat pump range: COP falls to 1.0 at and below this
# diesel energy (the diesel buses obey)
R0, R_CLIMB, R_DIFF = 29.5, 0.40, 25.0       # l per 100 km: base, per m/km, per unit of difficulty
H_IDLE = 0.45                                # l per hour at stops and layovers (engine off on long layovers)
ENGINE_HEAT = 9.0                            # kW of waste heat available for the cabin
UA_DIESEL = 0.40
TANK_L = {"Volvo 8900LE": 320, "Scania Citywide LE": 300, "VDL Citea LLE": 310}
