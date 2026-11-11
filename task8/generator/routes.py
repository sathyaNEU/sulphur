"""task8: the named methods the effort passes and the rivals run, each the golden's code with choices changed."""
import results as R

# what a careful but hurried run does unprompted: every file cleaned and joined, Quill put on the Lexis basis through
# KS2 by the textbook chained equipercentile link (KS2 to Lexis on every Lexis academy's students, the July
# transition day's sittings among them), the Brightway trial's pairs taken as they stand and the July sittings taken
# as entry reading
CAREFUL = dict(gain="none", july="none", ref="all")

SINGLE = {
    "the other tests' standardised scores read as Lexis scores": dict(quill="nominal", brightway="nominal"),
    "the trial's pairs as they stand": dict(gain="none"),
    "the July sittings as entry reading": dict(july="none", ref="all"),
    "Quill predicted from KS2 by regression": dict(quill="regression"),
}
PAIRS = {
    "careful, the trial's second sitting corrected": dict(july="none", ref="all"),
    "careful, the July sittings brought to September": dict(gain="none"),
    "careful, Quill by regression instead": dict(gain="none", july="none", quill="regression", ref="all"),
}
RIVALS = {
    "no presmoothing": dict(degree=0),
    "presmoothing to four moments": dict(degree=4),
    "presmoothing to eight moments": dict(degree=8),
    "the gain from the median gaps": dict(gain_stat="median"),
    "the trial link from the fixed-order academies alone": dict(trial_academies="fixed"),
    "the July level from the median residual": dict(dip_stat="median"),
    "the July level from a regression on KS2": dict(july="regression"),
    "Quill by frequency estimation": dict(quill="fe"),
    "re-sits after a failed or short session taken down by the gain": dict(resit="gain"),
}
# routes the data rule out, kept to show where they land
RULED_OUT = {
    "presmoothing to two moments": dict(degree=2),
    "Brightway through KS2 rather than the trial": dict(brightway="ks2"),
    "the trial linked linearly": dict(brightway="trial_linear"),
    "every test standardised within the trust": dict(quill="zscore", brightway="zscore"),
}


def route(name):
    if name == "golden":
        return R.GOLD
    if name == "careful":
        return R.opts(**CAREFUL)
    for table in (SINGLE, PAIRS, RIVALS, RULED_OUT):
        if name in table:
            return R.opts(**table[name])
    raise KeyError(name)
