"""The documents and small files of the pack: the reliability charter (exported by the house PDF writer), the incident
and change register, the two configuration files as the serving stack keeps them, and the three files the analysis
does not use (the ranking model's offline replay, its feature importance table and its release log). The charter
files what a feature group's quarterly cost is and where the line sits; the configuration files state structure.
None of them says how any estimate is made."""
import datetime as dt
import os
import sys

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts",
                       "writers")
sys.path.insert(0, WRITERS)
sys.path.insert(0, HERE)
import officepdf as O  # noqa: E402
import core as C  # noqa: E402
import world as WL  # noqa: E402

F = WL.FILES
DSEED = 910402
CEST = dt.timezone(dt.timedelta(hours=2))

CHARTER = [
    ("1. Purpose", [
        "1.1 The ranking model that orders search results reads feature groups that other teams build and serve. This "
        "charter sets which feature groups their owning teams harden as tier one dependencies of search in 2027, and "
        "what tier one requires of them.",
        "1.2 It replaces the 2025 list, which was drawn up by the platform team from the incident register.",
    ]),
    ("2. How the list is drawn", [
        "2.1 The 2027 tier one list is drawn on the third quarter of 2026, 1 July to 30 September 2026, by the "
        "business days of the search conversion mart.",
        "2.2 A feature group is every feature the registry holds under one group name. The registry holds seven.",
        "2.3 The list is put to the platform's third-quarter reliability review and takes effect on 1 January 2027.",
    ]),
    ("3. A feature group's quarterly cost", [
        "3.1 Search conversion is the orders attributed to search sessions divided by the search sessions, in per "
        "cent. A difference between two search conversions is stated in percentage points.",
        "3.2 A feature group is in normal service when each of its sources refreshes on its schedule and the "
        "services it is read from answer.",
        "3.3 A feature group's quarterly cost is the difference between two search conversions, each taken over all "
        "search sessions of the quarter in the six markets: the search conversion those sessions would have had with "
        "the feature group in normal service to every service that reads it, less the search conversion as served.",
        "3.4 The cost of several feature groups together is the sum of their costs. A month's cost is the same "
        "quantity taken over that month's search sessions.",
    ]),
    ("4. The tier one line", [
        "4.1 A feature group whose quarterly cost is 0.05 percentage points or more goes on the tier one list.",
        "4.2 A feature group whose quarterly cost is below 0.05 percentage points keeps its present tier.",
    ]),
    ("5. What tier one requires", [
        "5.1 The owning team of a tier one feature group carries a staffed on-call rota for it, round the clock, "
        "from 1 January 2027.",
        "5.2 The owning team agrees a freshness objective for the group with the platform team by 31 January 2027 "
        "and reports against it each month.",
        "5.3 A change to a tier one feature group's sources, store or schedule goes through the platform's change "
        "review before release.",
        "5.4 The platform team budgets each tier one feature group at one and a half engineer-years in 2027. A "
        "team whose group is on the list may ask the Search Leadership Group for the head count in the November "
        "planning round.",
    ]),
    ("6. Review", [
        "6.1 The charter is reviewed each September. The line in section 4 may be changed only by the Search "
        "Leadership Group.",
    ]),
]


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.8, leading=13.6, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.4, leading=16.8, spaceAfter=3)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.4, leading=13.8,
                        spaceBefore=8, spaceAfter=3, keepWithNext=1)
    return body, h1, h2


def charter(target):
    body, h1, h2 = _styles()
    title = "Ranking Platform Reliability Charter 2027"
    story = [Paragraph(title, h1),
             Paragraph("%s, Search and Discovery. Paper SLG-26-19, approved by the Search Leadership Group on "
                       "15 September 2026." % WL.SHORT, body),
             Spacer(1, 4)]
    for head, paras in CHARTER:
        story.append(Paragraph(head, h2))
        for p in paras:
            story.append(Paragraph(p, body))
    story.append(Spacer(1, 8))
    story.append(Paragraph("%s<br/>Head of Ranking Platform" % WL.PEOPLE["platform_lead"], body))
    O.build(os.path.join(target, F["charter"]), story, title=title, author=WL.PEOPLE["platform_lead"],
            subject="Tier one dependencies of search, 2027", footer="SLG-26-19 Ranking Platform Reliability Charter 2027",
            created=dt.datetime(2026, 9, 16, 9, 48, tzinfo=CEST), modified=dt.datetime(2026, 9, 16, 9, 48, tzinfo=CEST),
            producer="LibreOffice 25.8", font="Liberation Sans")


PIPELINE = """service: search-results
revision: "2026-09-28"
owner_team: Ranking Platform
markets: [DE, NL, SE, BE, AT, DK]
request:
  timeout_ms: 900
  overrides:
    source: experiment-platform
    resolved_by: user_id_hash
    feature_ablation:
      applied_at: [rank, rerank]
      schedule: monthly_per_feature_group
      run_days: 14
    component_holdout:
      applied_at: [render]
      run_days: 42
stages:
  - name: retrieve
    backend: search-index
    replica: per_market
    candidates: 1500
  - name: rank
    model: ranker-v7
    pass: first
    feature_groups: [match, price, trend, seller]
    on_missing_value: group_default
    output: ordered_page
  - name: page_cache
    cluster: per_serving_region
    key: [market, device, query_normalised, filters, page_number]
    ttl_seconds: 720
    ttl_history:
      - until: "2026-06-09"
        ttl_seconds: 300
    read: every_request
    write: requests_without_overrides
    purge_on: catalogue_reindex
  - name: rerank
    model: ranker-v7
    pass: second
    scope: per_request
    feature_groups: [stock, promise, history]
    on_missing_value: group_default
  - name: render
    components:
      - name: delivery_promise_badge
        feature_groups: [promise]
        on_missing_value: suppress
      - name: price_match_label
        feature_groups: [price]
        on_missing_value: suppress
      - name: buy_again_strip
        feature_groups: [history]
        on_missing_value: suppress
      - name: rating_stars
        feature_groups: []
      - name: sponsored_slot
        feature_groups: []
      - name: filter_rail
        feature_groups: []
logging:
  sessions: edge
  orders: nightly_attribution
"""

STORE = """store: feature-store
revision: "2026-08-31"
owner_team: Ranking Platform
defaults:
  on_expiry: serve_group_default
  on_missing: serve_group_default
groups:
  stock:
    backing: stock-snapshot
    refresh:
      trigger: chain_feed_sync
      interval_minutes: 15
    validity_hours: 2
  price:
    backing: price-batch
    refresh:
      trigger: daily_batch
      at_utc: "04:00"
    validity_hours: 36
    replication: per_serving_region
  trend:
    backing: trend-counters
    refresh:
      trigger: stream_window
      window_hours: 1
    validity_hours: 6
  seller:
    backing: seller-score
    refresh:
      trigger: nightly_run
      scope: sellers_with_newly_settled_orders
      effective_at_utc: "00:00"
    validity_hours: 120
request_time:
  promise:
    service: promise-api
    timeout_ms: 120
  history:
    service: profile-store
    timeout_ms: 60
  match:
    service: search-index
    replica: per_market
"""


def configs(target):
    open(os.path.join(target, F["pipeline"]), "w", newline="\n").write(PIPELINE)
    open(os.path.join(target, F["store"]), "w", newline="\n").write(STORE)


def _day(d, hh, mm):
    return dt.datetime.combine(WL.date_of(d), dt.time(hh, mm))


def incidents(W, target):
    rng = np.random.default_rng(DSEED)
    P = WL.PEOPLE
    rows = [
        (12, 9, 40, 12, "change", "ranking model", "ranker-v7.1 monthly retrain released", P["mlops"]),
        (23, 2, 15, 23, "incident", "partner feeds", "chn-08 feed credentials rotated by partner without notice", P["feeds"]),
        (40, 10, 5, 40, "change", "ranking model", "ranker-v7.2 monthly retrain released", P["mlops"]),
        (52, 14, 30, 53, "incident", "click stream", "broker disk pressure, two partitions behind for a day", P["streams"]),
        (68, 9, 55, 68, "change", "ranking model", "ranker-v7.3 monthly retrain released", P["mlops"]),
        (97, 7, 20, 113, "incident", "competitive pricing",
         "price batch not replicated to fra2 on seven nights between 8 and 23 April (replication credential expiring and renewed late)",
         P["pricing"]),
        (99, 9, 30, 99, "change", "ranking model", "ranker-v7.4 monthly retrain released", P["mlops"]),
        (131, 10, 10, 131, "change", "ranking model", "ranker-v7.5 monthly retrain released", P["mlops"]),
        (138, 8, 5, 147, "incident", "monitoring",
         "status monitor lost part of its probe pool 19 to 25 May; the week's trend and match rows reloaded 28 May", P["sre"]),
        (153, 11, 0, 153, "change", "seller quality", "seller-score job moved to the common logging library", P["sellers"]),
        (159, 13, 45, 159, "change", "edge", "search result page cache lifetime raised from 5 to 12 minutes (edge cost programme)", P["edge"]),
        (162, 9, 50, 162, "change", "ranking model", "ranker-v7.6 monthly retrain released", P["mlops"]),
        (186, 6, 30, 186, "change", "partner feeds", "feed gateway gw2 in service; chains 01, 04, 07, 10 and 12 moved to it", P["feeds"]),
        (187, 15, 20, 262, "incident", "partner feeds", "gw2 stalls under load, feeds of the moved chains stopping together; open until the pool was resized on 19 September", P["feeds"]),
        (188, 5, 10, 227, "incident", "competitive pricing", "crawl-de-at batch failing on some nights after layout changes at the crawled sites", P["pricing"]),
        (190, 9, 15, 190, "change", "ranking model", "ranker-v7.7 monthly retrain released", P["mlops"]),
        (193, 22, 40, 269, "incident", "click stream", "consumer lag on several partitions after the broker upgrade; lag episodes lasting a day or more", P["streams"]),
        (194, 6, 50, 267, "incident", "seller quality", "seller-score nightly run not completing in its window; closed when the worker pool was resized", P["sellers"]),
        (196, 16, 5, None, "incident", "competitive pricing", "crawl-benelux batch failing on some nights (proxy pool exhaustion)", P["pricing"]),
        (200, 8, 25, None, "incident", "delivery promise", "promise-api error rate raised since the carrier rate-card release", P["delivery"]),
        (183, 7, 30, None, "incident", "search index", "index replica for SE restarting under memory pressure, an hour or more at a time", P["index"]),
        (222, 10, 0, 245, "change", "shopper profiles", "profile store re-shard, 11 August to 3 September; read errors raised while shards move", P["profiles"]),
        (223, 9, 35, 223, "change", "ranking model", "ranker-v7.8 monthly retrain released", P["mlops"]),
        (251, 9, 20, 251, "change", "ranking model", "ranker-v7.9 monthly retrain released", P["mlops"]),
        (258, 14, 10, 258, "change", "experiment platform", "assignment service certificates renewed", P["experiments"]),
    ]
    u = W["u"]
    near = np.minimum(np.roll(u, 1, axis=1), np.roll(u, -1, axis=1))           # the lower of the two days beside it
    for d in np.nonzero((u - near > 0.12).all(axis=0))[0]:
        rows.append((int(d), int(rng.integers(5, 9)), int(rng.integers(0, 60)), int(d), "change", "edge",
                     "search result page cache flushed after catalogue re-index", P["edge"]))
    rows.sort(key=lambda r: (r[0], r[1], r[2]))
    wb = Workbook()
    ws = wb.active
    ws.title = "register"
    ws.append(["ref", "kind", "opened", "closed", "system", "title", "owner"])
    no = {"incident": 4180, "change": 9320}
    for d, hh, mm, d1, kind, system, title, owner in rows:
        no[kind] += int(rng.integers(3, 40))
        closed = None if d1 is None else (_day(d1, min(hh + int(rng.integers(1, 6)), 23), int(rng.integers(0, 60))))
        ws.append(["%s-%d" % ("INC" if kind == "incident" else "CHG", no[kind]), kind, _day(d, hh, mm), closed, system, title, owner])
    for c in ws[1]:
        c.font = Font(bold=True)
    for row in ws.iter_rows(min_row=2):
        row[2].number_format = row[3].number_format = "yyyy-mm-dd hh:mm"
        row[5].alignment = Alignment(wrap_text=True, vertical="top")
    for i, wd in enumerate([11, 10, 17, 17, 20, 78, 22]):
        ws.column_dimensions[chr(65 + i)].width = wd
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = "A1:G%d" % (len(rows) + 1)
    wb.save(os.path.join(target, F["incidents"]))
    return len(rows)


FEATURES = {
    "match": ["bm25_title", "bm25_description", "bm25_brand", "exact_phrase_title", "query_category_match", "synonym_hits",
              "title_coverage", "attribute_match_count", "spelling_distance", "semantic_similarity", "brand_intent_match",
              "model_number_match"],
    "price": ["price_vs_lowest_competitor", "price_vs_median_competitor", "competitor_count", "price_rank_in_category",
              "days_since_price_change", "price_gap_pct", "is_cheapest", "competitor_in_stock_share"],
    "trend": ["clicks_6h", "clicks_24h", "add_to_cart_6h", "ctr_6h_vs_7d", "query_click_share_6h", "category_momentum",
              "new_listing_boost", "search_volume_6h"],
    "seller": ["seller_quality_score", "late_dispatch_rate", "cancellation_rate", "return_rate", "dispute_rate",
               "review_score_90d", "response_time_p50"],
    "stock": ["in_stock_nearby", "stores_with_stock", "stock_depth_band", "click_and_collect_available", "nearest_store_km",
              "restock_expected_days"],
    "promise": ["promised_delivery_days", "next_day_eligible", "delivery_fee_band", "evening_slot_available",
                "promise_confidence"],
    "history": ["bought_before", "category_affinity", "brand_affinity", "price_band_affinity", "days_since_last_order",
                "viewed_recently", "wishlist_hit"],
    "query": ["query_length", "query_is_navigational", "query_frequency_band", "query_category_entropy", "has_brand_token",
              "has_size_token", "query_language"],
    "catalogue": ["listing_age_days", "image_count", "has_video", "title_length", "attribute_completeness",
                  "category_depth", "review_count", "review_score", "variant_count", "is_bundle"],
    "context": ["hour_of_day", "day_of_week", "device", "market", "is_logged_in", "page_number", "is_promo_day"],
}


def unused(W, target):
    rng = np.random.default_rng(DSEED + 1)
    # ---- the offline replay: ranking quality on logged queries with one feature group left out
    wb = Workbook()
    ws = wb.active
    ws.title = "replay_2026q3"
    ws.append(["feature_group", "market", "queries_replayed", "ndcg_at_10_all_features", "ndcg_at_10_group_left_out",
               "mrr_all_features", "mrr_group_left_out"])
    pull = {"stock": 0.031, "promise": 0.009, "price": 0.017, "history": 0.022, "trend": 0.012, "seller": 0.019,
            "match": 0.094}
    for j in C.GROUPS:
        for m, mk in enumerate(C.MARKETS):
            base = 0.612 + 0.012 * rng.standard_normal()
            mrr = 0.471 + 0.010 * rng.standard_normal()
            d = pull[j] * np.exp(rng.normal(0, 0.18))
            ws.append([j, mk, int(40000 * C.MK_W[m] / 0.09 * rng.uniform(0.9, 1.1)), round(base, 4), round(base - d, 4),
                       round(mrr, 4), round(mrr - 0.8 * d * np.exp(rng.normal(0, 0.1)), 4)])
    for c in ws[1]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, wd in enumerate([14, 9, 12, 14, 14, 12, 12]):
        ws.column_dimensions[chr(65 + i)].width = wd
    ws.freeze_panes = "A2"
    wb.save(os.path.join(target, F["replay"]))
    # ---- the model's feature importance table
    rows = []
    wgt = {"match": 30, "catalogue": 14, "price": 9, "trend": 8, "seller": 7, "stock": 9, "promise": 4, "history": 8,
           "query": 6, "context": 5}
    for g, feats in FEATURES.items():
        share = rng.dirichlet(np.full(len(feats), 1.2)) * wgt[g]
        for f, s in zip(feats, share):
            rows.append((f, g, round(float(s), 3), int(rng.integers(40, 2600))))
    rows.sort(key=lambda r: -r[2])
    with open(os.path.join(target, F["importance"]), "w", newline="") as fh:
        fh.write("feature,feature_group,gain_pct,splits\r\n")
        for r in rows:
            fh.write("%s,%s,%.3f,%d\r\n" % r)
    # ---- the release log
    rel = [("7.0", "2025-11-18", "Two-pass ranker. First pass on text match, price, trend and seller features; second pass per request on stock, delivery promise and shopper history. 77 features."),
           ("7.1", "2026-01-13", "Monthly retrain on 90 days of search logs to 31 December. No feature change."),
           ("7.2", "2026-02-10", "Monthly retrain to 31 January. No feature change."),
           ("7.3", "2026-03-10", "Monthly retrain to 28 February. No feature change."),
           ("7.4", "2026-04-10", "Monthly retrain to 31 March. No feature change. Offline NDCG@10 0.611."),
           ("7.5", "2026-05-12", "Monthly retrain to 30 April. No feature change."),
           ("7.6", "2026-06-12", "Monthly retrain to 31 May. No feature change. Serving image moved to the new base."),
           ("7.7", "2026-07-10", "Monthly retrain to 30 June. No feature change."),
           ("7.8", "2026-08-12", "Monthly retrain to 31 July. No feature change. Offline NDCG@10 0.613."),
           ("7.9", "2026-09-09", "Monthly retrain to 31 August. No feature change.")]
    with open(os.path.join(target, F["releases"]), "w", newline="\n") as fh:
        fh.write("ranker release log, 2026\nmaintained by ranking model operations (%s)\n\n" % WL.PEOPLE["mlops"])
        for v, d, note in rel:
            fh.write("ranker-v%s  released %s\n  %s\n\n" % (v, d, note))


def write_all(W, target):
    charter(target)
    configs(target)
    n = incidents(W, target)
    unused(W, target)
    return n


if __name__ == "__main__":
    write_all(C.make_world(), sys.argv[1])
