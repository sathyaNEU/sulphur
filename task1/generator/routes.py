"""The named methods the effort passes and the rivals run: each is the golden's code with choices changed."""
import models

CAREFUL = dict(su_price="period", completion="channel", rise_window=(27, 28), rise_bands="pooled", link=(),
               ret_proxy=False)
SINGLE = {
    "completion on each channel's older starts": dict(completion="channel"),
    "no full-price term at the intro's end": dict(su_price="period"),
    "the 2025 rise read from April, pooled": dict(rise_window=(27, 28), rise_bands="pooled"),
    "returns on the customer number only": dict(link=()),
    "no returns": dict(returns=False),
}
PAIRS = {
    "careful, reading used": dict(su_price="period", rise_window=(27, 28), rise_bands="pooled", link=(), ret_proxy=False),
    "careful, households linked": dict(su_price="period", completion="channel", rise_window=(27, 28),
                                       rise_bands="pooled"),
    "careful, full price carried": dict(completion="channel", rise_window=(27, 28), rise_bands="pooled", link=(),
                                        ret_proxy=False),
    "careful, rise months left out": dict(su_price="period", completion="channel", drop_rise_months=True,
                                          rise_window=(27, 28), rise_bands="pooled", link=(), ret_proxy=False),
    "careful, the 2025 rise read in full": dict(su_price="period", completion="channel", link=(), ret_proxy=False),
}
RIVALS = {
    "a time trend in the end-of-intro model": dict(su_trend=True),
    "the rise against the same months a year before": dict(rise_baseline="yoy"),
    "tenure as a smooth decay": dict(tenure_form="decay"),
    "titles in the hazard": dict(hz_title=True),
    "reading in the end-of-intro model": dict(su_proxy=True),
    "the rise's window to June": dict(rise_window=(26, 27, 28, 29)),
    "reading taken linearly": dict(proxy_form="linear"),
    "reading in bands": dict(proxy_form="bins"),
    "reading with a square term": dict(proxy_form="quad"),
    "discount depth and intro length": dict(su_form="depth"),
    "returns on the payment fingerprint": dict(link=("fingerprint",)),
    "returns on the address": dict(link=("address",)),
    "the offer in the leaving model": dict(hz_offer=True),
    "the price at the intro's end in the leaving model": dict(hz_price=True),
}


PROBES = {"the newest starts calibrated on their own months, no reading": dict(completion="channel",
                                                                             completion_cohort=True)}


def route(name):
    if name == "golden":
        return models.GOLD
    if name == "careful":
        return models.opts(**CAREFUL)
    if name in SINGLE:
        return models.opts(**SINGLE[name])
    if name in PAIRS:
        return models.opts(**PAIRS[name])
    if name in PROBES:
        return models.opts(**PROBES[name])
    return models.opts(**RIVALS[name])
