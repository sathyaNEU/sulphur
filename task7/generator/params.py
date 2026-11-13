"""The world's constants: Platte Ridge Public Power District, a fictional public power district in east-central Nebraska,
and its 2027 voltage optimization program. Time is local standard time (CST, UTC-6) at 15-minute resolution over 2026."""
import datetime as dt

SEED = 3077
YEAR = 2026
Q = 96                                  # quarter-hours a day
ND = 365
NQ = ND * Q
T0 = dt.datetime(2026, 1, 1)
NF = 24
VNOM = 120.0                            # volts on a 120 V base
VMIN = 114.0                            # ANSI C84.1 Range A service minimum
MARGIN = 1.0                            # the program standard's margin above it
DVMAX = 0.04 * VNOM                     # the most the voltage optimization equipment takes off (volts)
TAP = 0.00625 * VNOM                    # one LTC step: 5/8 percent
KV = 12.47
TRIAL_DV = 0.04 * VNOM                  # the trial's on-day reduction
TRIAL_MONTHS = ((4, 1), (5, 31), (10, 1), (10, 31))
LOSS_RATE_REPORT = 0.061                # the 2025 annual report's distribution losses
PRICE = 48.0                            # USD per MWh, the board's 2027 avoided energy cost
ANNUITY = 9.4                           # the standard's present-value factor, 15 years at 6.5 percent
# energy response exponents (per unit power change per per unit voltage change) once thermostats have recovered,
# and in the first quarter-hour after a step
KE = dict(Z=1.6, P=0.05, I=1.0, TH=0.0, HP=0.8, AC=0.8)
KI = dict(Z=1.6, P=0.05, I=1.0, TH=2.0, HP=0.8, AC=0.8)
TAU_TH = 0.6                            # hours: thermostatic loads recover with this time constant
SUBSTATIONS = ["Ashgrove", "Cedar Bluff", "Elm Creek", "Fairview", "Gibbon Road", "Hollister"]
COST_SCALE = 0.80                       # the capital plan's unit costs (2026 dollars)
