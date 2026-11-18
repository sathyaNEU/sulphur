"""The nouns and the calendar laid over the core's arrays: Tessel Market's people, teams, chains, sources, shards,
serving regions and file names. Nothing here moves a dial of generator/core.py."""
import datetime as dt
from zoneinfo import ZoneInfo

import core as C

ORG = "Tessel Market B.V."
SHORT = "Tessel Market"
UTC = dt.timezone.utc
LOCAL = ZoneInfo("Europe/Amsterdam")
DAY0 = dt.datetime(2026, 1, 1, tzinfo=UTC)
ASOF = dt.date(2026, 10, 12)                      # the day the records were extracted

# drawn by guard.py names --geo Netherlands --seed 9104
PEOPLE = {
    "platform_lead": "Aylin Haack",               # head of the ranking platform, signs the charter
    "analyst": "Zoey Mahieu",                     # reliability analyst, author of the deliverables
    "director": "Milo Veenendaal",                # director of search, last editor of the workbook
    "experiments": "Lorenzo Stoffel",             # experiment platform
    "feeds": "Jaylinn Smits",                     # partner feeds
    "pricing": "Alicia Boers",                    # competitor pricing
    "delivery": "Suus Koster",                    # delivery promise service
    "profiles": "Cornelia Hollander",             # profile store
    "streams": "Maarten Nieuwstraten",            # click stream
    "sellers": "Sem Gerrits",                     # seller quality
    "index": "Boaz Everts",                       # search index
    "edge": "Amir Keijzer",                       # edge and caching
    "sre": "Mats Stuivenberg",                    # site reliability, keeps the incident register
    "mlops": "Mehmet Miltenburg",                 # ranking model operations
}
TEAMS = {"stock": "Partner Feeds", "promise": "Delivery Promise", "price": "Competitive Pricing",
         "history": "Shopper Profiles", "trend": "Click Stream", "seller": "Seller Quality", "match": "Search Index"}
OWNER = {"stock": "feeds", "promise": "delivery", "price": "pricing", "history": "profiles", "trend": "streams",
         "seller": "sellers", "match": "index"}
GROUP_NAME = {"stock": "store stock", "promise": "delivery promise", "price": "competitor price",
              "history": "shopper history", "trend": "trending clicks", "seller": "seller quality",
              "match": "text match"}
COMPONENT = {"promise": "delivery_promise_badge", "price": "price_match_label", "history": "buy_again_strip"}
MART_KEY = {"DE": "DEU", "NL": "NLD", "SE": "SWE", "BE": "BEL", "AT": "AUT", "DK": "DNK"}
COUNTRY = {"DE": "Germany", "NL": "Netherlands", "SE": "Sweden", "BE": "Belgium", "AT": "Austria", "DK": "Denmark"}
CURRENCY = {"DE": "EUR", "NL": "EUR", "SE": "SEK", "BE": "EUR", "AT": "EUR", "DK": "DKK"}
LAUNCHED = {"DE": 2017, "NL": 2014, "SE": 2019, "BE": 2016, "AT": 2020, "DK": 2021}
SITE = {m: "tesselmarket.%s" % m.lower() for m in C.MARKETS}
REGIONS = ("ams1", "fra2")                        # fra2 is the region that missed April's batches
CHAINS = ["Lindeveld", "Oosterkamp Wonen", "Vaartkade", "Kastanjehof", "Maasoever", "Zilverberk", "Nordlys Hem",
          "Havsvik", "Dammtor Haus", "Rheinfeld Markt", "Steinacher", "Almgren & Dal", "Bergstrand", "Soendervang"]
MIGRATING = (0, 3, 6, 9, 11)
GATEWAY_DAY = 186                                 # 6 July: the five chains' feeds move to the new gateway
SOURCES = ["crawl-de-at", "crawl-benelux", "partner-api-nordics", "affiliate-feed", "marketplace-listings"]
FILES = {
    "sessions": "edge_search_sessions_hourly_2026.csv",
    "mart": "mart_search_conversion_daily_2026.csv",
    "status": "feature_status_hourly_2026.csv",
    "gaps": "chain_feed_gaps_2026.csv",
    "batches": "competitor_price_batch_runs_2026.csv",
    "lags": "clickstream_lag_episodes_2026.csv",
    "scoring": "seller_score_runs_2026.csv",
    "seller_traffic": "seller_search_traffic_monthly_2026.csv",
    "shares": "feature_source_traffic_2026.xlsx",
    "experiments": "experiment_platform_export_2026.sqlite",
    "cache": "edge_page_cache_daily_2026.csv",
    "render": "component_render_hourly_2026.csv",
    "registry": "feature_registry.csv",
    "pipeline": "search_pipeline.yaml",
    "store": "feature_store.yaml",
    "markets": "markets.csv",
    "regions": "serving_regions.csv",
    "promo": "promo_calendar_2026.csv",
    "incidents": "incident_and_change_register_2026.xlsx",
    "charter": "ranking_platform_reliability_charter_2027.pdf",
    "replay": "ranker_offline_replay_2026q3.xlsx",
    "importance": "ranker_v7_feature_importance.csv",
    "releases": "ranker_release_log_2026.txt",
}
UNUSED = ("replay", "importance", "releases")


def date_of(day):
    return (DAY0 + dt.timedelta(days=int(day))).date()


def hour_utc(h):
    return (DAY0 + dt.timedelta(hours=int(h))).strftime("%Y-%m-%dT%H:00:00Z")


def stamp_utc(hours):
    """Hours from the start of the year (a float) as a UTC time to the second."""
    return (DAY0 + dt.timedelta(seconds=int(round(hours * 3600.0)))).strftime("%Y-%m-%dT%H:%M:%SZ")


def stamp_local(hours):
    """The same instant on the wall clock in Utrecht, with its offset."""
    t = (DAY0 + dt.timedelta(seconds=int(round(hours * 3600.0)))).astimezone(LOCAL)
    s = t.strftime("%Y-%m-%dT%H:%M:%S%z")
    return s[:-2] + ":" + s[-2:]


def shard_of(group, k, day=None):
    if group == "stock":
        if k in MIGRATING and day is not None and day >= GATEWAY_DAY:
            return "gw2/chn-%02d" % (k + 1)
        return "feed/chn-%02d" % (k + 1)
    if group == "price":
        return "batch/%s" % SOURCES[k]
    if group == "trend":
        return "clicks/p%02d" % k
    if group == "match":
        return "index/replica-%s" % C.MARKETS[k].lower()
    return {"promise": "promise-api", "history": "profile-store", "seller": "seller-score/nightly"}[group]
