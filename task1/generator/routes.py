"""Every route the build prices, by name: the golden, each defensible rival (the fork table's SF16 to SF18 and the
method choices beside them) and each hurried shortcut, as variants of passes.golden on one pack."""
import passes as PS

REPS = 2000
RIVAL_REPS = 1000
SEED = 11

RIVALS = {
    "uplift by size band": {"uplift_form": "bands"},
    "utilisation in bins": {"util_form": "bins"},
    "no utilisation term in the exit model": {"util_form": "none"},
    "April excess from the last two months": {"team": "golden_last2"},
    "April excess as an exponential with a floor": {"team": "golden_expfit"},
    "win odds by stage and deal age": {"pipe_keys": ("stage", "agb")},
    "deal creation over the trailing eighteen months": {"creation_window": 18},
    "Team calendar index by quarter": {"season": "quarter"},
    "Team calendar index smoothed": {"season": "smooth"},
    "own drift over 12 months": {"drift_window": 12},
    "own drift over 18 months": {"drift_window": 18},
    "each account's trailing true-up rate": {"expansion": "acc"},
}

HURRIED = {
    "band without the estimation uncertainty": {"param_unc": False},
    "an assumed common factor of 0.25 added": {"common": 0.25},
    "mean uplift applied flat": {"uplift_flat": True},
    "list rise applied flat": {"uplift_list": True},
    "pooled renewal rates": {"util": False, "sib": False, "first": False},
    "accounts drawn independently": {"independent": True},
    "Team rates since April": {"team": "recent_pooled"},
    "Team rates of the last three months": {"team": "last3_pooled"},
    "Team rates of the trailing twelve months": {"team": "trailing12"},
    "Team rates before April": {"team": "long_pooled"},
    "CRM stage probabilities": {"crm": True},
    "trailing run-rate of new ARR": {"runrate": True},
    "win odds by stage alone": {"stage_only": True},
    "the book's trailing true-up rate near seats": {"expansion": "runrate"},
}

CAREFUL = {"uplift_flat": True, "util": False, "sib": False, "first": False, "team": "last3_pooled", "crm": True,
           "independent": True, "expansion": "acc"}


def golden(B):
    return PS.golden(B, reps=REPS, seed=SEED)


def run(B, table, reps=RIVAL_REPS):
    return {k: PS.golden(B, reps=reps, seed=SEED, variant=v) for k, v in table.items()}


# the largest single hints, each executed on the careful but hurried pass: the one step it corrects
HINTS = {
    "old open deals rarely close, so the CRM's stage odds overstate the pipeline": {"crm": False},
    "large contracts negotiate the price rise down at renewal": {"uplift_flat": False},
    "seat cuts and exits at renewal follow how many people use the product, first renewals most":
        {"util": True, "first": True},
    "accounts in one parent group leave together": {"sib": True, "independent": False},
    "the extra Team exits after April are fading": {"team": "golden"},
    "seat additions follow each account's own growth in users": {"expansion": "drift"},
}


def careful_with(fix):
    v = dict(CAREFUL)
    v.update(fix)
    return v
