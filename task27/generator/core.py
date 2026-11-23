#!/usr/bin/env python3
"""Core operational process simulator, open-book estimators, rival shortcuts, frontier run routes,
and v4-hardened corelib spec for task27 Architecture 2 (Weserfrucht Import GmbH: 2027 Corridor
Carrier-Remediation Capital Allocation under a fixed EUR 1.75M budget cap).

Six North Sea port-to-DC refrigerated import corridors compete for a fixed EUR 1.75M 2027 carrier
and terminal remediation budget, ranked descending by projected 2027 Benefit-Cost Ratio (BCR =
avoidable carrier-controllable detention & demurrage EUR per EUR of corridor remediation cost).
Every corridor budget sits between EUR 520k and EUR 590k, so any 3 corridors fit (<= EUR 1.74M)
and no 4 corridors fit (>= EUR 2.19M); greedy-by-BCR and optimal integer knapsack select the
exact same top-3 funded corridors.

Every operational mechanism is openly disclosed in Charter RC-2027 Rev 3 (zero hidden catches,
zero dead zones, zero zero-variance constants, realistic SNR ~ 2.5-3.5 across all stages):
  S1 (what)  Asymmetric convex chamber-load hysteresis: inland DC sealed thermal chambers
             (+2C Z02, +7C Z07, +13C Z13) throttle port-yard call-offs progressively above 78%
             utilization, ~3.6x more steeply during stock build-up (net_pallet_flow > 0) than
             during drawdown (net_pallet_flow <= 0), while opposing produce seasons keep total
             DC occupancy flat (69-78%). Both binary >=92%/95% cutoffs and symmetric linear slopes
             mis-attribute coldstore_dock vs reefer_plug and flip BHV-KAS.
  S2 (unit)  Open-book joint separation of terminal-varying BIP rail locks vs correlated peak
             Nordbahn locomotive derates and short-consist wagon cuts: continuous Gamma BIP
             notice lead times (0 dead zones) trigger smooth terminal-specific booking locks
             (BHV ~18h, HAM ~26h, WHV ~14h) with stochastic rollover pass-through (~0.70, so
             rolled < locked occurs ~30% of the time), overlapping correlated peak-day Nordbahn
             short-consist cuts, noisy Gamma rollover durations (CV ~0.30), and noisy mixed-cargo
             train weighbridge mass (R^2 ~0.92). Naive BIP cross-tabs and fixed-24h 1-to-1 rules
             fail; only joint multivariate estimation recovers phyto_insp vs rail_handoff and
             flips HAM-MAG / HAM-HAN.
  S3 (when)  Cumulative multi-day empty-depot backlog queue outliving portal closures: daily
             (port, shipping_line) unreturned-empty queues rebuilt from unloads minus gate-ins
             swell during portal quota closures and drain slowly over 4-7 open-portal days
             (portal_rejected == 0), scaling with inland corridor distance. Binary portal-closure
             contrasts (portal_rejected > 0 vs == 0) contaminate the control group with drain days,
             miss ~45% of depot-caused delay, and flip BHV-HAN.

All three stumps couple directly into ALL SIX corridors' 2027 carrier-controllable exposure and
BCR (100% coupled ask matrix, 0 un-stumped figures, 0 ECF rollups), while each stump owns one
strictly independent 2026 Critical Component.

Run:
    python3 task27/generator/core.py
    python3 task27/generator/core.py --detail --forcing
"""
import itertools
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, ".agents", "skills", "stumping"))
import corelib  # noqa: E402

SEED = 2702
BUDGET_CAP_EUR = 1_750_000.0
TOP_K = 3
N_DAYS = 365
N_QUEUE_DAYS = N_DAYS + 18  # 2026-01-01 through 2027-01-18 (<= 2027-01-22 as_of, zero Dec 31 clamp)
N_CONTAINERS = 24000
N_VESSELS = 480
QUARTER_BOUNDS = np.array([90, 181, 273], dtype=int)

PORTS = ("BHV", "HAM", "WHV")
DCS = ("HAN", "OSN", "KAS", "MAG")
ZONES = ("Z02", "Z07", "Z13")
LINES = ("LINE_A", "LINE_B", "LINE_C", "LINE_D")

# Six active North Sea port-to-DC refrigerated import corridors (100% of network)
CORRIDORS = ("BHV-HAN", "BHV-KAS", "BHV-OSN", "HAM-HAN", "HAM-MAG", "WHV-OSN")
CORR_PORT = np.array([0, 0, 0, 1, 1, 2], dtype=int)  # BHV, BHV, BHV, HAM, HAM, WHV
CORR_DC = np.array([0, 2, 1, 0, 3, 1], dtype=int)    # HAN, KAS, OSN, HAN, MAG, OSN
CORR_SHARES = np.array([0.185, 0.185, 0.155, 0.175, 0.170, 0.130])
CORR_DIST_KM = np.array([155.0, 295.0, 175.0, 150.0, 255.0, 165.0])

# Filed 2027 corridor carrier-remediation program budgets & contractual capture rates
# Every 3-corridor subset <= 1,740k <= 1,750k cap; every 4-corridor subset >= 2,190k > 1,750k cap.
CORR_BUDGET_EUR = {
    "BHV-HAN": 575_000.0,
    "BHV-KAS": 570_000.0,
    "BHV-OSN": 560_000.0,
    "HAM-HAN": 585_000.0,
    "HAM-MAG": 565_000.0,
    "WHV-OSN": 560_000.0,
}
CORR_CAPTURE_RATE = {
    "BHV-HAN": 0.78,
    "BHV-KAS": 0.78,
    "BHV-OSN": 0.80,
    "HAM-HAN": 0.80,
    "HAM-MAG": 0.78,
    "WHV-OSN": 0.82,
}

TARIFF_EUR = {
    "reefer_plug": 210.0,
    "rail_handoff": 175.0,
    "drayage_carrier": 160.0,
    "coldstore_dock": 285.0,
    "phyto_insp": 260.0,
    "empty_depot": 230.0,
    "vessel_berth": 195.0,
    "edi_docs": 140.0,
}

PLAN_2027 = {
    "vol_growth_corridor": {
        "BHV-HAN": 1.12,
        "BHV-KAS": 1.15,
        "BHV-OSN": 1.18,
        "HAM-HAN": 1.22,
        "HAM-MAG": 1.14,
        "WHV-OSN": 1.16,
    },
    "plug_capacity_factor_2027": {"BHV": 0.92, "HAM": 1.05, "WHV": 1.00},
    "rail_fleet_factor_2027": {"BHV": 0.94, "HAM": 0.96, "WHV": 0.92},
    "dray_contract_factor_2027": {"BHV": 0.95, "HAM": 0.98, "WHV": 0.96},
    "dc_zone_load_factor_2027": {"Z02": 1.32, "Z07": 1.08, "Z13": 1.06},
    "bip_sampling_factor_2027": {"BHV": 1.18, "HAM": 1.22, "WHV": 1.15},
    "depot_load_factor_2027": {"LINE_A": 1.24, "LINE_B": 1.20, "LINE_C": 1.02, "LINE_D": 1.00},
}

REEFER_LOADED_TONNES = 28.5
PORT_LOCK_MID_H = np.array([16.0, 28.0, 12.0])  # BHV ~16h, HAM ~28h, WHV ~12h (distinct from naive 24h)
PORT_LOCK_WIDTH_H = 1.7


def _day_to_quarter(day_arr):
    return np.searchsorted(QUARTER_BOUNDS, day_arr, side="right")


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -30.0, 30.0)))


def _asym_sawtooth(days, period, rise_frac, phase=0.0):
    """Smooth asymmetric sawtooth wave in [-1, 1]: rise_frac > 0.5 gives long filling limbs,
    rise_frac < 0.5 gives fast intakes followed by long slow drawdown limbs."""
    u = ((days + phase) % period) / float(period)
    r = float(rise_frac)
    w = np.where(u < r, -1.0 + 2.0 * (u / r), 1.0 - 2.0 * ((u - r) / (1.0 - r)))
    return w


def simulate_world(seed=SEED):
    """Simulate Weserfrucht's 2026 physical operations with balanced 3-stump magnitudes (~4,500-5,200 c-days each),
    realistic operational noise, zero dead zones, and zero zero-variance constants."""
    rng = np.random.default_rng(seed)
    days = np.arange(N_DAYS)

    # --- 1. Build 365-day sealed thermal chamber stocks & net flows (4 DCs x 3 zones) ---
    wave_z02 = (
        0.67
        + 0.25 * np.exp(-0.5 * ((days - 185.0) / 40.0) ** 2)
        + 0.15 * np.exp(-0.5 * ((days - 105.0) / 24.0) ** 2)
    )
    wave_z07 = (
        0.66
        + 0.25 * (
            np.exp(-0.5 * ((days - 28.0) / 34.0) ** 2)
            + np.exp(-0.5 * ((days - 335.0) / 34.0) ** 2)
        )
        + 0.13 * np.exp(-0.5 * ((days - 265.0) / 26.0) ** 2)
    )
    wave_z13 = np.clip(2.22 - wave_z02 - wave_z07, 0.50, 0.92)

    dc_caps = np.array([
        [1440, 1380, 1360],  # HAN (dc=0)
        [1150, 1110, 1090],  # OSN (dc=1: bulk storage hub -> fast intake, long slow drawdown limbs)
        [1140, 1120, 1080],  # KAS (dc=2: regional peak hub -> long high-util filling limbs)
        [1050, 1010, 980],   # MAG (dc=3)
    ], dtype=float)
    dc_load_shift = np.array([-0.024, 0.056, 0.062, -0.020])
    dc_phase = np.array([0, 8, -6, 12])
    # Realistic hub dispatch regimes: KAS builds steadily (rise_frac=0.82), OSN receives sharp intakes & draws down slowly (rise_frac=0.10)
    dc_rise_frac = np.array([0.48, 0.10, 0.82, 0.48])

    chamber_opening = np.zeros((4, 3), dtype=int)
    pallet_in = np.zeros((4, 3, N_DAYS), dtype=int)
    pallet_out = np.zeros((4, 3, N_DAYS), dtype=int)
    chamber_stock = np.zeros((4, 3, N_DAYS), dtype=int)
    chamber_util = np.zeros((4, 3, N_DAYS), dtype=float)
    chamber_net_flow = np.zeros((4, 3, N_DAYS), dtype=int)

    zone_waves = np.vstack([wave_z02, wave_z07, wave_z13])
    for d in range(4):
        for z in range(3):
            cap = dc_caps[d, z]
            # Z13 offsets both Z02 and Z07 shifts so aggregate dc_total_util stays flat across all 4 DCs!
            shifted = np.roll(zone_waves[z], dc_phase[d]) + (dc_load_shift[d] if z < 2 else -2.0 * dc_load_shift[d])
            cyc = 0.068 * _asym_sawtooth(days, period=28, rise_frac=dc_rise_frac[d], phase=9 * d + 7 * z)
            eps = np.zeros(N_DAYS)
            eps[0] = rng.normal(0.0, 0.010)
            for t in range(1, N_DAYS):
                eps[t] = 0.72 * eps[t - 1] + rng.normal(0.0, 0.0045)
            raw_tu = np.maximum(0.40 + rng.uniform(0.0, 0.015, size=N_DAYS), shifted + cyc + eps)
            target_u = np.where(raw_tu > 0.955, 0.955 + 0.032 * np.tanh((raw_tu - 0.955) / 0.032), raw_tu)
            target_s = np.round(target_u * cap).astype(int)
            chamber_opening[d, z] = int(target_s[0])
            cur = int(target_s[0])
            for t in range(N_DAYS):
                base_flow = int(round(cap * (0.14 + 0.03 * shifted[t])))
                delta = int(target_s[t] - cur)
                in_p = max(12, base_flow + max(delta, 0) + int(rng.integers(-5, 6)))
                out_p = max(12, in_p - delta)
                nxt = cur + in_p - out_p
                if nxt > int(cap):
                    out_p += nxt - int(cap)
                    nxt = int(cap)
                if nxt < 0:
                    in_p += -nxt
                    nxt = 0
                pallet_in[d, z, t] = in_p
                pallet_out[d, z, t] = out_p
                chamber_stock[d, z, t] = nxt
                chamber_util[d, z, t] = nxt / cap
                chamber_net_flow[d, z, t] = in_p - out_p
                cur = nxt

    dc_total_stock = chamber_stock.sum(axis=1)
    dc_total_cap = dc_caps.sum(axis=1)
    dc_total_util = dc_total_stock / dc_total_cap[:, None]

    # Port terminal daily physical reefer-rack utilization (3 ports x 365 days)
    port_season = (
        0.70
        + 0.20 * np.exp(-0.5 * ((days - 188.0) / 42.0) ** 2)
        + 0.18 * (
            np.exp(-0.5 * ((days - 26.0) / 38.0) ** 2)
            + np.exp(-0.5 * ((days - 338.0) / 38.0) ** 2)
        )
    )
    port_yard_util = np.zeros((3, N_DAYS))
    for p in range(3):
        noise_p = np.zeros(N_DAYS)
        noise_p[0] = rng.normal(0.0, 0.025)
        for t in range(1, N_DAYS):
            noise_p[t] = 0.72 * noise_p[t - 1] + rng.normal(0.0, 0.022)
        port_offset = [0.020, 0.015, -0.005][p]
        raw_u = np.maximum(0.55 + rng.uniform(0.0, 0.02, size=N_DAYS), port_season + port_offset + noise_p)
        port_yard_util[p] = np.where(raw_u > 0.935, 0.935 + 0.042 * np.tanh((raw_u - 0.935) / 0.042), raw_u)

    # --- 2. Simulate 480 Vessel Calls & 24,000 Import Containers across 6 Corridors ---
    port_shares = np.array([CORR_SHARES[CORR_PORT == p].sum() for p in range(3)])
    vessel_port = rng.choice(3, size=N_VESSELS, p=port_shares)
    vessel_day = np.sort(rng.integers(0, N_DAYS, size=N_VESSELS))
    cont_vessel = rng.integers(0, N_VESSELS, size=N_CONTAINERS)
    cont_port = vessel_port[cont_vessel]
    cont_day = vessel_day[cont_vessel]
    cont_quarter = _day_to_quarter(cont_day)

    cont_corr = np.zeros(N_CONTAINERS, dtype=int)
    for p in range(3):
        c_idx = np.where(CORR_PORT == p)[0]
        probs = CORR_SHARES[c_idx] / CORR_SHARES[c_idx].sum()
        mask = cont_port == p
        cont_corr[mask] = rng.choice(c_idx, size=int(mask.sum()), p=probs)
    cont_dc = CORR_DC[cont_corr]

    p_z02 = 0.25 + 0.22 * np.exp(-0.5 * ((cont_day - 185.0) / 48.0) ** 2) + np.where(cont_corr == 1, 0.25, 0.0)
    p_z07 = 0.25 + 0.20 * (
        np.exp(-0.5 * ((cont_day - 28.0) / 44.0) ** 2)
        + np.exp(-0.5 * ((cont_day - 335.0) / 44.0) ** 2)
    ) + np.where(cont_corr == 1, 0.22, 0.0)
    p_z13 = np.where(cont_corr == 1, 0.08, 0.28)
    p_sum = p_z02 + p_z07 + p_z13
    u_z = rng.random(N_CONTAINERS)
    cont_zone = np.where(u_z < p_z02 / p_sum, 0, np.where(u_z < (p_z02 + p_z07) / p_sum, 1, 2))

    # Shipping line mix: BHV-HAN heaviest on LINE_A/B (S3 opens BHV-HAN); WHV-OSN dray-dominant with moderate LINE_A/B
    cont_line = np.zeros(N_CONTAINERS, dtype=int)
    line_mix_by_corr = np.array([
        [0.62, 0.34, 0.02, 0.02],  # BHV-HAN (S3 opens BHV-HAN!)
        [0.14, 0.13, 0.37, 0.36],  # BHV-KAS
        [0.08, 0.08, 0.42, 0.42],  # BHV-OSN
        [0.08, 0.08, 0.42, 0.42],  # HAM-HAN
        [0.13, 0.13, 0.37, 0.37],  # HAM-MAG
        [0.14, 0.13, 0.37, 0.36],  # WHV-OSN (dray-dominant winner: port-level S3-over/s3_raw drop WHV-OSN; low LINE_A/B keeps reflex low!)
    ])
    for c in range(6):
        mc = cont_corr == c
        cont_line[mc] = rng.choice(4, size=int(mc.sum()), p=line_mix_by_corr[c])

    rail_p = np.array([0.74, 0.72, 0.70, 0.84, 0.92, 0.70])[cont_corr]
    cont_is_rail = rng.random(N_CONTAINERS) < rail_p

    # --- 3. Non-pool background stages (vessel_berth & edi_docs) ---
    vessel_storm = 0.12 + 0.08 * (
        np.exp(-0.5 * ((vessel_day - 25.0) / 55.0) ** 2)
        + np.exp(-0.5 * ((vessel_day - 335.0) / 55.0) ** 2)
    )
    vessel_delay_each = rng.gamma(shape=2.0, scale=vessel_storm / 2.0) * np.array([1.06, 1.00, 0.88])[vessel_port]
    true_vessel_berth = vessel_delay_each[cont_vessel] * rng.uniform(0.88, 1.12, size=N_CONTAINERS)
    edi_flag = rng.random(N_CONTAINERS) < 0.036
    true_edi_docs = np.where(edi_flag, rng.gamma(shape=4.0, scale=0.24, size=N_CONTAINERS), 0.0)

    # --- 4. STUMP S1: Asymmetric Convex Chamber-Load Hysteresis (~6,600 c-days total) ---
    # Channel-dominant golden winners (~1.11-1.14 BCR):
    #   BHV-OSN = plug-dominant (S1-over & sym_lin crash BHV-OSN)
    #   HAM-HAN = rail-dominant (S2-over & S2_1f crash HAM-HAN)
    #   WHV-OSN = drayage-dominant (S3-over & s3_raw crash WHV-OSN)
    # False-alarm non-funded corridors (~0.96-0.99 BCR):
    #   BHV-KAS (opened by S1), HAM-MAG (opened by S2), BHV-HAN (opened by S3)
    u_port_c = port_yard_util[cont_port, cont_day]
    corr_plug_mult = np.array([1.48, 1.52, 2.75, 0.90, 1.62, 1.32])[cont_corr]
    plug_mean = corr_plug_mult * (
        0.070
        + 0.55 * np.maximum(0.0, u_port_c - 0.70)
        + 15.0 * np.maximum(0.0, u_port_c - 0.80) ** 2
    )
    true_reefer_plug = np.maximum(0.005, plug_mean * rng.gamma(shape=10.0, scale=1.0 / 10.0, size=N_CONTAINERS))

    dc_direct_flag = rng.random(N_CONTAINERS) < 0.15
    true_coldstore_direct = np.where(dc_direct_flag, rng.gamma(shape=3.5, scale=0.10, size=N_CONTAINERS), 0.0)

    # Asymmetric convex chamber pull-back: smooth onset at u_ch > 0.78 (NO 95% binary cliff!),
    # ~7.5x steeper when filling (net_flow > 0) than when draining (net_flow <= 0).
    u_ch_c = chamber_util[cont_dc, cont_zone, cont_day]
    nf_c = chamber_net_flow[cont_dc, cont_zone, cont_day]
    ex_u = np.maximum(0.0, u_ch_c - 0.78)
    is_filling = nf_c > 0
    pb_mean = np.where(
        is_filling,
        3.90 * ex_u + 68.0 * (ex_u ** 2),
        0.30 * ex_u + 2.5 * (ex_u ** 2),
    )
    true_coldstore_pullback = np.where(
        ex_u > 1e-6,
        pb_mean * rng.gamma(shape=9.5, scale=1.0 / 9.5, size=N_CONTAINERS),
        0.0,
    )
    obs_term_yard_hold = true_reefer_plug + true_coldstore_pullback
    obs_dc_dock_wait = true_coldstore_direct

    # --- 5. STUMP S2: Open-Book Joint Separation of Terminal-Varying BIP Locks vs Overlapping Short-Consists ---
    order_vz = np.lexsort((cont_zone, cont_vessel))
    cont_ched = np.empty(N_CONTAINERS, dtype=int)
    lot_id = 0
    idx = 0
    lot_port, lot_day, lot_zone, lot_size, lot_corr = [], [], [], [], []
    while idx < N_CONTAINERS:
        sz = int(rng.choice([2, 3, 4, 5, 6], p=[0.12, 0.25, 0.30, 0.23, 0.10]))
        end = min(idx + sz, N_CONTAINERS)
        v0, z0 = cont_vessel[order_vz[idx]], cont_zone[order_vz[idx]]
        k = idx + 1
        while k < end and cont_vessel[order_vz[k]] == v0 and cont_zone[order_vz[k]] == z0:
            k += 1
        members_idx = order_vz[idx:k]
        cont_ched[members_idx] = lot_id
        lot_port.append(vessel_port[v0])
        lot_day.append(vessel_day[v0])
        lot_zone.append(z0)
        lot_size.append(k - idx)
        lot_corr.append(int(np.bincount(cont_corr[members_idx]).argmax()))
        lot_id += 1
        idx = k
    n_lots = lot_id
    lot_port = np.array(lot_port)
    lot_day = np.array(lot_day)
    lot_zone = np.array(lot_zone)
    lot_size = np.array(lot_size)
    lot_corr = np.array(lot_corr)

    # Shared seasonal congestion drives BOTH BIP exam surges AND Nordbahn short-consist cuts (real confounding!)
    sh_season_peak = (
        0.45
        + 0.85 * np.exp(-0.5 * ((days - 188.0) / 38.0) ** 2)
        + 0.75 * (
            np.exp(-0.5 * ((days - 28.0) / 34.0) ** 2)
            + np.exp(-0.5 * ((days - 336.0) / 34.0) ** 2)
        )
    )
    # High BIP exposure on HAM-MAG (corr 4 -> S2 opens HAM-MAG!), early-notice BIP on HAM-HAN (S2-over & S2_1f hit HAM-HAN!)
    corr_bip_boost = np.array([0.11, 0.08, 0.08, 0.24, 0.44, 0.09])[lot_corr]
    lot_bip_prob = np.clip(corr_bip_boost * (0.65 + 0.50 * sh_season_peak[lot_day]), 0.04, 0.54)
    lot_bip = rng.random(n_lots) < lot_bip_prob

    # Continuous smooth Gamma lead times across [1.5h, 72h] — ZERO dead zones!
    # HAM-HAN has earlier phytosanitary pre-clearance notices (Gamma scale 15.0 -> strong S2-over & S2_1f sensitivity)
    lot_gamma_scale = np.where(lot_corr == 3, 15.0, np.where(lot_corr == 4, 6.8, 9.6))
    lot_lead_hours = np.clip(rng.gamma(shape=2.4, scale=lot_gamma_scale, size=n_lots), 1.5, 72.0)

    # Terminal-varying smooth logistic lock probability (BHV ~16h, HAM ~28h, WHV ~12h)
    lot_lock_prob = _sigmoid((PORT_LOCK_MID_H[lot_port] - lot_lead_hours) / PORT_LOCK_WIDTH_H)
    lot_locked = lot_bip & (rng.random(n_lots) < lot_lock_prob)

    cont_bip_sampled = np.zeros(N_CONTAINERS, dtype=bool)
    cont_bip_sibling = np.zeros(N_CONTAINERS, dtype=bool)
    lot_first_seen = np.zeros(n_lots, dtype=bool)
    for i in range(N_CONTAINERS):
        lid = cont_ched[i]
        if lot_bip[lid]:
            if not lot_first_seen[lid]:
                cont_bip_sampled[i] = True
                lot_first_seen[lid] = True
            else:
                cont_bip_sibling[i] = True

    base_sampled_hold = np.where(cont_bip_sampled, rng.gamma(shape=4.5, scale=0.18, size=N_CONTAINERS), 0.0)
    raw_sibling_hold = np.where(cont_bip_sibling, rng.gamma(shape=4.5, scale=0.075, size=N_CONTAINERS), 0.0)
    true_phyto_direct = base_sampled_hold + np.where(~cont_is_rail, raw_sibling_hold, 0.0)
    true_phyto_sibling_rail = np.where(cont_is_rail, raw_sibling_hold, 0.0)

    # Scheduled intermodal reefer block trains depart every 3 days per corridor (122 departures/corridor = 732 shuttles;
    # ~30-45 Weserfrucht rail boxes per active departure -> realistic block-train load and <1% standby censoring!)
    n_slots = (N_DAYS + 2) // 3
    n_shuttles = 6 * n_slots
    cont_shuttle = cont_corr * n_slots + (cont_day // 3)
    shuttle_corr = np.repeat(np.arange(6), n_slots)
    shuttle_port = CORR_PORT[shuttle_corr]
    shuttle_day = np.minimum(N_DAYS - 1, np.tile(np.arange(n_slots) * 3 + 1, 6))
    shuttle_quarter = _day_to_quarter(shuttle_day)

    rail_idx = np.where(cont_is_rail)[0]
    planned_on_shuttle = np.bincount(cont_shuttle[rail_idx], minlength=n_shuttles)

    cont_locked_phyto = cont_is_rail & lot_locked[cont_ched]
    cont_prelock_phyto = cont_is_rail & lot_bip[cont_ched] & (~lot_locked[cont_ched])
    n_locked_phyto_sh = np.bincount(cont_shuttle[cont_locked_phyto], minlength=n_shuttles)
    n_prelock_phyto_sh = np.bincount(cont_shuttle[cont_prelock_phyto], minlength=n_shuttles)

    elig_rail_mask = cont_is_rail & (~lot_bip[cont_ched])
    n_elig_rail_sh = np.bincount(cont_shuttle[elig_rail_mask], minlength=n_shuttles)

    # Stochastic BIP lock -> standby roll pass-through (~0.66, NOT deterministic 1-to-1!)
    p_bip_pass = 0.66
    raw_bip_rolls = rng.binomial(n_locked_phyto_sh, p_bip_pass)
    wf_standby_rolled_phyto_sh = np.minimum(raw_bip_rolls, n_elig_rail_sh)

    # Correlated genuine Nordbahn short-consist & locomotive cuts (HAM-HAN rail-dominant!)
    # Strong shared peak-day confounding with BIP surges breaks bivariate n_24 OLS (one_fact_crosstab)!
    sh_peak = sh_season_peak[shuttle_day]
    has_wf = (planned_on_shuttle > 0).astype(float)
    corr_rail_cap_mult = np.array([1.05, 0.85, 0.58, 2.75, 0.72, 0.58])[shuttle_corr]
    bip_day_intensity = np.minimum(6.0, n_locked_phyto_sh.astype(float))
    loco_derate_sh = np.minimum(
        4,
        rng.poisson(has_wf * corr_rail_cap_mult * (0.08 + 0.16 * sh_peak + 0.24 * bip_day_intensity)),
    )
    consist_wagons_short_sh = np.minimum(
        10,
        rng.poisson(has_wf * corr_rail_cap_mult * (0.48 + 0.88 * sh_peak + 1.10 * bip_day_intensity)),
    )

    lam_rail_short = has_wf * (0.50 * consist_wagons_short_sh + 1.05 * loco_derate_sh)
    raw_rail_short = rng.poisson(lam_rail_short)
    rem_elig = np.maximum(0, n_elig_rail_sh - wf_standby_rolled_phyto_sh)
    wf_standby_rolled_rail_sh = np.minimum(raw_rail_short, rem_elig)
    wf_standby_rolled_total_sh = wf_standby_rolled_phyto_sh + wf_standby_rolled_rail_sh

    # Pre-departure confirmed bookings = planned minus pre-lock cancellations (no reverse causality!)
    wf_booked_slots_sh = np.maximum(0, planned_on_shuttle - n_prelock_phyto_sh)
    empty_locked_slots_sh = np.minimum(wf_booked_slots_sh, n_locked_phyto_sh)
    wf_actual_loaded_sh = np.maximum(
        0, wf_booked_slots_sh - np.maximum(wf_standby_rolled_total_sh, empty_locked_slots_sh)
    )

    # Realistic noisy train weighbridge gross tonnage (R^2 ~ 0.93-0.95, NEVER 0.9997!)
    third_party_slots_sh = rng.integers(14, 30, size=n_shuttles)
    train_wagon_count_sh = np.maximum(12, wf_booked_slots_sh + third_party_slots_sh - consist_wagons_short_sh)
    tp_loaded = np.maximum(0, train_wagon_count_sh - wf_actual_loaded_sh - empty_locked_slots_sh)
    third_party_tonnes_sh = (
        tp_loaded * 24.5 + rng.normal(0.0, 42.0, size=n_shuttles) * np.sqrt(np.maximum(1, tp_loaded))
    )
    wf_loaded_tonnes_sh = (
        wf_actual_loaded_sh * REEFER_LOADED_TONNES
        + rng.normal(0.0, 3.0, size=n_shuttles) * np.sqrt(np.maximum(1, wf_actual_loaded_sh))
    )
    train_gross_tonnes_sh = train_wagon_count_sh * 22.0 + wf_loaded_tonnes_sh + third_party_tonnes_sh

    # Stochastic Gamma rollover durations (mean 3.25 d, SD 0.96 d, CV 0.30 — matches every-3-day shuttle cadence!)
    cont_rolled_rail = np.zeros(N_CONTAINERS, dtype=bool)
    cont_rolled_is_bip = np.zeros(N_CONTAINERS, dtype=bool)
    cont_rail_base = np.where(cont_is_rail, rng.gamma(shape=3.0, scale=0.025 / 3.0, size=N_CONTAINERS), 0.0)
    cont_rail_roll_dur = np.zeros(N_CONTAINERS, dtype=float)

    elig_by_sh = [[] for _ in range(n_shuttles)]
    for ci in np.where(elig_rail_mask)[0]:
        elig_by_sh[cont_shuttle[ci]].append(ci)
    for s in range(n_shuttles):
        k_tot = int(wf_standby_rolled_total_sh[s])
        k_bip = int(wf_standby_rolled_phyto_sh[s])
        if k_tot > 0:
            pool = np.array(elig_by_sh[s], dtype=int)
            chosen = rng.choice(pool, size=k_tot, replace=False)
            cont_rolled_rail[chosen] = True
            if k_bip > 0:
                cont_rolled_is_bip[chosen[:k_bip]] = True
            cont_rail_roll_dur[chosen] = rng.gamma(shape=11.0, scale=3.25 / 11.0, size=k_tot)

    cont_rail_excess = cont_rail_base + cont_rail_roll_dur
    true_phyto_bump_c = np.where(cont_rolled_is_bip, cont_rail_roll_dur, 0.0)
    true_rail_short_c = np.where(cont_rolled_rail & (~cont_rolled_is_bip), cont_rail_roll_dur, 0.0)

    # --- 5b. Physical Inland Unload Day ---
    base_transit_days = np.where(cont_is_rail, 3, 2)
    pre_unload_excess = np.round(
        obs_term_yard_hold
        + obs_dc_dock_wait
        + true_phyto_direct
        + true_phyto_sibling_rail
        + true_edi_docs
        + cont_rail_excess
    ).astype(int)
    cont_unload_day = np.minimum(N_QUEUE_DAYS - 8, cont_day + base_transit_days + pre_unload_excess)

    # --- 6. STUMP S3: Exact Stock-Flow Conservation Empty-Depot Backlog Queue Outliving Portal Closures (~5,600 c-days) ---
    # Genuine carrier-controllable drayage turnaround congestion (WHV-OSN strongly drayage-dominant!)
    corr_dray_mult = np.array([1.22, 1.05, 0.85, 0.80, 1.02, 5.45])[cont_corr]
    dow_mult = np.array([1.14, 0.94, 0.92, 0.96, 1.18, 0.90, 0.96])[cont_unload_day % 7]
    carrier_season = (
        0.105
        + 0.36 * np.exp(-0.5 * ((cont_unload_day - 190.0) / 30.0) ** 2)
        + 0.16 * np.exp(-0.5 * ((cont_unload_day - 325.0) / 28.0) ** 2)
    )
    dray_mean = corr_dray_mult * dow_mult * carrier_season
    true_dray_carrier = np.maximum(0.005, dray_mean * rng.gamma(shape=10.0, scale=1.0 / 10.0, size=N_CONTAINERS))

    phys_turnaway_flag = rng.random(N_CONTAINERS) < 0.036
    true_depot_physical = np.where(
        phys_turnaway_flag, rng.gamma(shape=4.0, scale=0.22, size=N_CONTAINERS), 0.0
    )

    daily_empty_unloads = np.zeros((3, 4, N_QUEUE_DAYS), dtype=int)
    for p in range(3):
        for l in range(4):
            m = (cont_port == p) & (cont_line == l)
            daily_empty_unloads[p, l] = np.bincount(cont_unload_day[m], minlength=N_QUEUE_DAYS)

    # Episodic 3-4 day portal closure bursts separated by 10-15 open days so ~60% of backlog delay occurs on OPEN drain days!
    depot_quota_closed = np.zeros((3, 4, N_QUEUE_DAYS), dtype=bool)
    for p in range(3):
        for l in range(4):
            if l in (0, 1):
                prob_q = (0.056 if p in (0, 2) else 0.040) + (0.082 if p in (0, 2) else 0.058) * (
                    np.exp(-0.5 * ((days - 192.0) / 45.0) ** 2)
                    + 0.65 * np.exp(-0.5 * ((days - 60.0) / 32.0) ** 2)
                    + 0.65 * np.exp(-0.5 * ((days - 315.0) / 32.0) ** 2)
                )
                state = 0
                cool = 0
                for t in range(N_DAYS):
                    if state > 0:
                        depot_quota_closed[p, l, t] = True
                        state -= 1
                    elif cool > 0:
                        cool -= 1
                    elif rng.random() < prob_q[t]:
                        state = int(rng.integers(3, 5))
                        cool = int(rng.integers(10, 15))
                        depot_quota_closed[p, l, t] = True
            elif l == 2:
                depot_quota_closed[p, l, :N_DAYS] = rng.random(N_DAYS) < 0.015

    # Exact physical depot gate-in conservation:
    # Each day t, depot accepts min(queue + unloads, daily_gate_cap) empty gate-ins; remaining unreturned empties
    # stay in queue_stock[t] = cumsum(daily_empty_unloads - daily_empty_gateins). Zero artificial lag or measurement noise!
    daily_empty_gateins = np.zeros((3, 4, N_QUEUE_DAYS), dtype=int)
    portal_confirmed = np.zeros((3, 4, N_QUEUE_DAYS), dtype=int)
    portal_rejected = np.zeros((3, 4, N_QUEUE_DAYS), dtype=int)
    queue_stock = np.zeros((3, 4, N_QUEUE_DAYS), dtype=float)
    queue_days_norm = np.zeros((3, 4, N_QUEUE_DAYS), dtype=float)
    for p in range(3):
        for l in range(4):
            arr_s = daily_empty_unloads[p, l]
            mu_global = max(1.5, float(arr_s[:N_DAYS].mean()))
            q = 0
            for t in range(N_QUEUE_DAYS):
                lo_t, hi_t = max(0, t - 10), min(N_QUEUE_DAYS, t + 11)
                local_mu = max(1.0, float(arr_s[lo_t:hi_t].mean()))
                avail = q + int(arr_s[t])
                if depot_quota_closed[p, l, t]:
                    # Quota closure restricts depot gate-in intake to ~18% of local demand -> builds 2.5-4 days backlog
                    cap_t = int(round(0.18 * local_mu))
                    gate_in = min(avail, max(0, cap_t))
                else:
                    # Open portal clears current-day demand plus ~38% extra catch-up -> drains backlog over 5-7 OPEN days!
                    cap_t = int(round(max(float(arr_s[t]), local_mu) + 0.38 * local_mu))
                    gate_in = min(avail, max(int(arr_s[t]), cap_t))
                q = avail - gate_in
                daily_empty_gateins[p, l, t] = gate_in
                portal_confirmed[p, l, t] = gate_in
                queue_stock[p, l, t] = float(q)
                queue_days_norm[p, l, t] = float(q) / mu_global
                if depot_quota_closed[p, l, t] and q > 0:
                    portal_rejected[p, l, t] = max(1, int(rng.poisson(max(1.0, q * 1.35))))

    # Observable stock-flow unreturned-empty queue rebuilt strictly from unloads - gate-ins (exact conservation!)
    obs_queue_stock = np.zeros((3, 4, N_QUEUE_DAYS), dtype=float)
    obs_queue_days = np.zeros((3, 4, N_QUEUE_DAYS), dtype=float)
    for p in range(3):
        for l in range(4):
            bal = np.cumsum(daily_empty_unloads[p, l] - daily_empty_gateins[p, l]).astype(float)
            obs_queue_stock[p, l] = bal
            obs_queue_days[p, l] = bal / max(1.0, float(daily_empty_unloads[p, l, :N_DAYS].mean()))

    # True empty_depot delay scales linearly with end-of-day normalized backlog queue depth Q_days x linear corridor haul factor
    q_c = queue_days_norm[cont_port, cont_line, cont_unload_day]
    dist_scale = 1.0 + 0.0022 * (CORR_DIST_KM[cont_corr] - 150.0)
    depot_q_mean = 0.68 * q_c * dist_scale
    true_depot_portal_block = np.where(
        q_c > 1e-6,
        depot_q_mean * rng.gamma(shape=10.0, scale=1.0 / 10.0, size=N_CONTAINERS),
        0.0,
    )
    obs_dray_empty_hold = true_dray_carrier + true_depot_portal_block
    obs_depot_turnaway = true_depot_physical

    world = {
        "N_QUEUE_DAYS": N_QUEUE_DAYS,
        "cont_vessel": cont_vessel,
        "cont_corr": cont_corr,
        "cont_port": cont_port,
        "cont_day": cont_day,
        "cont_unload_day": cont_unload_day,
        "cont_quarter": cont_quarter,
        "cont_dc": cont_dc,
        "cont_zone": cont_zone,
        "cont_line": cont_line,
        "cont_is_rail": cont_is_rail,
        "cont_rolled_rail": cont_rolled_rail,
        "cont_rail_excess": cont_rail_excess,
        "cont_rail_base": cont_rail_base,
        "cont_rail_roll_dur": cont_rail_roll_dur,
        "cont_ched": cont_ched,
        "cont_shuttle": cont_shuttle,
        "cont_bip_sampled": cont_bip_sampled,
        "obs_vessel_berth": true_vessel_berth,
        "obs_edi_docs": true_edi_docs,
        "obs_term_yard_hold": obs_term_yard_hold,
        "obs_dc_dock_wait": obs_dc_dock_wait,
        "obs_phyto_hold_direct": true_phyto_direct,
        "obs_phyto_sibling_tms_rail": true_phyto_sibling_rail,
        "obs_dray_empty_hold": obs_dray_empty_hold,
        "obs_depot_turnaway": obs_depot_turnaway,
        "port_yard_util": port_yard_util,
        "dc_total_stock": dc_total_stock,
        "dc_total_cap": dc_total_cap,
        "dc_total_util": dc_total_util,
        "dc_caps": dc_caps,
        "chamber_opening": chamber_opening,
        "pallet_in": pallet_in,
        "pallet_out": pallet_out,
        "lot_port": lot_port,
        "lot_day": lot_day,
        "lot_zone": lot_zone,
        "lot_size": lot_size,
        "lot_bip": lot_bip,
        "lot_lead_hours": lot_lead_hours,
        "shuttle_corr": shuttle_corr,
        "shuttle_port": shuttle_port,
        "shuttle_day": shuttle_day,
        "shuttle_quarter": shuttle_quarter,
        "planned_on_shuttle": planned_on_shuttle,
        "wf_booked_slots_sh": wf_booked_slots_sh,
        "wf_actual_loaded_sh": wf_actual_loaded_sh,
        "wf_standby_rolled_total_sh": wf_standby_rolled_total_sh,
        "loco_derate_sh": loco_derate_sh,
        "consist_wagons_short_sh": consist_wagons_short_sh,
        "train_wagon_count_sh": train_wagon_count_sh,
        "train_gross_tonnes_sh": train_gross_tonnes_sh,
        "portal_confirmed": portal_confirmed,
        "portal_rejected": portal_rejected,
        "daily_empty_unloads": daily_empty_unloads,
        "daily_empty_gateins": daily_empty_gateins,
        "obs_queue_stock": obs_queue_stock,
        "obs_queue_days": obs_queue_days,
        "_truth": {
            "reefer_plug_c": true_reefer_plug,
            "coldstore_direct_c": true_coldstore_direct,
            "coldstore_pullback_c": true_coldstore_pullback,
            "phyto_direct_c": true_phyto_direct,
            "phyto_sibling_rail_c": true_phyto_sibling_rail,
            "phyto_bump_c": true_phyto_bump_c,
            "rail_short_c": true_rail_short_c,
            "rail_base_c": cont_rail_base,
            "dray_carrier_c": true_dray_carrier,
            "depot_physical_c": true_depot_physical,
            "depot_portal_block_c": true_depot_portal_block,
            "n_locked_phyto_sh": n_locked_phyto_sh,
            "wf_standby_rolled_phyto_sh": wf_standby_rolled_phyto_sh,
            "wf_standby_rolled_rail_sh": wf_standby_rolled_rail_sh,
            "queue_days_norm": queue_days_norm,
            "depot_quota_closed": depot_quota_closed,
        },
    }
    return world


def _reconstruct_chambers(w):
    stock = np.zeros((4, 3, N_DAYS), dtype=float)
    net_flow = np.zeros((4, 3, N_DAYS), dtype=float)
    for d in range(4):
        for z in range(3):
            nf = (w["pallet_in"][d, z] - w["pallet_out"][d, z]).astype(float)
            net_flow[d, z] = nf
            stock[d, z] = w["chamber_opening"][d, z] + np.cumsum(nf)
    assert np.allclose(stock.sum(axis=1), w["dc_total_stock"]), "Stock-flow conservation failed!"
    return stock / w["dc_caps"][:, :, None], net_flow


def _reconstruct_depot_queue(w):
    """Reconstruct normalized daily unreturned-empty backlog queue (in days of flow) per (port, line)
    by exact stock-flow conservation: cumsum(daily_empty_unloads - daily_empty_gateins) / mean_daily_unloads."""
    n_q = w["N_QUEUE_DAYS"]
    q_days = np.zeros((3, 4, n_q), dtype=float)
    for p in range(3):
        for l in range(4):
            bal = np.maximum(0.0, np.cumsum(w["daily_empty_unloads"][p, l] - w["daily_empty_gateins"][p, l]).astype(float))
            mu = max(1.0, float(w["daily_empty_unloads"][p, l, :N_DAYS].mean()))
            q_days[p, l] = bal / mu
    return q_days


def _demean_by_group(arr, grp, n_grp):
    cnt = np.bincount(grp, minlength=n_grp).astype(float)
    cnt_safe = np.maximum(cnt, 1.0)
    if arr.ndim == 1:
        sm = np.bincount(grp, weights=arr, minlength=n_grp)
        return arr - (sm / cnt_safe)[grp]
    out = np.empty_like(arr, dtype=float)
    for j in range(arr.shape[1]):
        sm = np.bincount(grp, weights=arr[:, j], minlength=n_grp)
        out[:, j] = arr[:, j] - (sm / cnt_safe)[grp]
    return out


def estimate_s1(w, mode="golden", hinge=0.78, fe="vessel", spec_form="quad"):
    """Estimate S1 split of obs_term_yard_hold into reefer_plug (carrier) vs coldstore_pullback (DC)."""
    y = w["obs_term_yard_hold"]
    n = len(y)
    if mode in ("hurried", "direct", "calibrated"):
        return y.copy(), np.zeros(n), {"asym_gap_h": 0.0}
    if mode == "hedge":
        pb = y * 0.14
        return y - pb, pb, {"asym_gap_h": 2.5}
    if mode == "rigorous":
        # Rigorous aggregate-DC check: tests aggregate dc_total_util excess above the 0.78 congestion threshold!
        # Because opposing produce seasons hold aggregate DC util flat in 69-78%, this finds ~0 DC pullback.
        u_dc = w["dc_total_util"][w["cont_dc"], w["cont_day"]]
        ex_dc = np.maximum(0.0, u_dc - 0.78)
        c_dum = np.column_stack([(w["cont_corr"] == c).astype(float) for c in range(1, 6)])
        Xr = np.column_stack([ex_dc, c_dum])
        Xd = _demean_by_group(Xr, w["cont_vessel"], N_VESSELS)
        yd = _demean_by_group(y, w["cont_vessel"], N_VESSELS)
        b, _, _, _ = np.linalg.lstsq(Xd, yd, rcond=None)
        pb = np.clip(max(0.0, float(b[0])) * ex_dc, 0.0, y * 0.5)
        return y - pb, pb, {"asym_gap_h": 0.0}

    ch_util, ch_nf = _reconstruct_chambers(w)
    u_ch = ch_util[w["cont_dc"], w["cont_zone"], w["cont_day"]]
    nf = ch_nf[w["cont_dc"], w["cont_zone"], w["cont_day"]]
    is_fill = (nf > 0).astype(float)
    is_drain = (nf <= 0).astype(float)
    bm = (u_ch >= 0.84) & (u_ch <= 0.94)

    if mode in ("over", "generous"):
        cut = 0.80 if mode == "over" else 0.82
        pb = np.where(u_ch >= cut, y, 0.0)
        gap_h = float((pb[bm & (nf > 0)].mean() - pb[bm & (nf <= 0)].mean()) * 24.0)
        return y - pb, pb, {"asym_gap_h": gap_h}

    if mode in ("cutoff_95", "one_fact_sym"):
        # 1-step post-hint shortcut: binary >= 0.92 (or 0.95) threshold cut (misses smooth 78-92% ramp & hysteresis!)
        cut = 0.95 if mode == "cutoff_95" else 0.92
        hi = u_ch >= cut
        lo = u_ch < 0.85
        grp = w["cont_vessel"]
        cnt = np.bincount(grp[lo], minlength=N_VESSELS)
        sm = np.bincount(grp[lo], weights=y[lo], minlength=N_VESSELS)
        gbase = np.where(cnt > 0, sm / np.maximum(1, cnt), y[lo].mean())[grp]
        pb = np.where(hi, np.maximum(0.0, y - gbase), 0.0)
        gap_h = float((pb[bm & (nf > 0)].mean() - pb[bm & (nf <= 0)].mean()) * 24.0)
        return y - pb, pb, {"asym_gap_h": gap_h}

    if mode == "cutoff_sym_lin":
        # Symmetric linear FE fit (controls for vessel & corridor, but ignores filling-vs-draining asymmetry & convexity!)
        ex = np.maximum(0.0, u_ch - 0.78)
        c_dum = np.column_stack([(w["cont_corr"] == c).astype(float) for c in range(1, 6)])
        Xs = np.column_stack([ex, c_dum])
        Xd = _demean_by_group(Xs, w["cont_vessel"], N_VESSELS)
        yd = _demean_by_group(y, w["cont_vessel"], N_VESSELS)
        b, _, _, _ = np.linalg.lstsq(Xd, yd, rcond=None)
        pb = np.clip(max(0.0, float(b[0])) * ex, 0.0, y)
        return y - pb, pb, {"asym_gap_h": 0.0}

    if fe == "port_day":
        grp = w["cont_port"] * N_DAYS + w["cont_day"]
        n_grp = 3 * N_DAYS
    elif fe == "corr_week":
        grp = w["cont_corr"] * 53 + (w["cont_day"] // 7)
        n_grp = 6 * 53
    else:
        grp = w["cont_vessel"]
        n_grp = N_VESSELS

    ex = np.maximum(0.0, u_ch - hinge)
    if spec_form == "bins":
        edges = [0.78, 0.83, 0.88, 0.92, 0.96, 1.05]
        cols = []
        for lo_e, hi_e in zip(edges[:-1], edges[1:]):
            ind = ((u_ch >= lo_e) & (u_ch < hi_e)).astype(float)
            cols.append(ind * is_fill)
            cols.append(ind * is_drain)
        X = np.column_stack(cols)
    elif spec_form == "spline":
        ex2 = np.maximum(0.0, u_ch - 0.86)
        ex3 = np.maximum(0.0, u_ch - 0.92)
        X = np.column_stack([
            ex * is_fill, ex2 * is_fill, ex3 * is_fill,
            ex * is_drain, ex2 * is_drain, ex3 * is_drain,
        ])
    else:
        X = np.column_stack([
            ex * is_fill, (ex ** 2) * is_fill,
            ex * is_drain, (ex ** 2) * is_drain,
        ])

    c_dum = np.column_stack([(w["cont_corr"] == c).astype(float) for c in range(1, 6)])
    X_full = np.column_stack([X, c_dum])
    Xd = _demean_by_group(X_full, grp, n_grp)
    yd = _demean_by_group(y, grp, n_grp)

    if spec_form == "huber":
        b, _, _, _ = np.linalg.lstsq(Xd, yd, rcond=None)
        for _ in range(8):
            res = yd - Xd @ b
            sc = np.median(np.abs(res)) * 1.4826 + 1e-6
            wt = np.where(np.abs(res) <= 1.345 * sc, 1.0, 1.345 * sc / np.maximum(np.abs(res), 1e-9))
            b, _, _, _ = np.linalg.lstsq(Xd * np.sqrt(wt)[:, None], yd * np.sqrt(wt), rcond=None)
    else:
        b, _, _, _ = np.linalg.lstsq(Xd, yd, rcond=None)

    b_ch = np.maximum(0.0, b[:X.shape[1]])
    pred_pb = np.maximum(0.0, X @ b_ch)
    rem = y - X_full @ b
    cnt_g = np.maximum(1.0, np.bincount(grp, minlength=n_grp).astype(float))
    fe_hat = (np.bincount(grp, weights=rem, minlength=n_grp) / cnt_g)[grp]
    pred_base = np.maximum(0.02, fe_hat + X_full[:, X.shape[1]:] @ b[X.shape[1]:])
    pb = np.where(pred_pb > 0.0, y * (pred_pb / (pred_pb + pred_base)), 0.0)
    gap_h = float((pb[bm & (nf > 0)].mean() - pb[bm & (nf <= 0)].mean()) * 24.0)
    return y - pb, pb, {"asym_gap_h": gap_h}


def estimate_s2(w, mode="golden", method="smooth_logistic", cut_shift=0.0):
    """Estimate S2 split of rail rollover days between rail_handoff (carrier) and phyto_insp (BIP)."""
    obs_sib = w["obs_phyto_sibling_tms_rail"]
    rail_base = w["cont_rail_base"]
    roll_dur = w["cont_rail_roll_dur"]
    rolled_sh = w["wf_standby_rolled_total_sh"].astype(float)
    n_sh = len(rolled_sh)

    sh_roll_days = np.bincount(w["cont_shuttle"], weights=roll_dur, minlength=n_sh)
    sh_base_days = np.bincount(w["cont_shuttle"], weights=rail_base, minlength=n_sh)
    sh_sib_days = np.bincount(w["cont_shuttle"], weights=obs_sib, minlength=n_sh)

    if mode in ("hurried", "direct", "calibrated"):
        return sh_roll_days + sh_base_days + sh_sib_days, np.zeros(n_sh), np.zeros(n_sh), {"bip_slope": 0.0}
    if mode == "hedge":
        frac = 0.14
        return sh_roll_days * (1 - frac) + sh_base_days, sh_roll_days * frac, sh_sib_days, {"bip_slope": 0.14}
    if mode == "rigorous":
        return sh_roll_days + sh_base_days, np.zeros(n_sh), sh_sib_days, {"bip_slope": 0.0}

    is_rail = w["cont_is_rail"]
    lot_bip = w["lot_bip"]
    lot_lead = w["lot_lead_hours"]
    cont_ched = w["cont_ched"]
    sh_id = w["cont_shuttle"]
    sh_port = w["shuttle_port"]

    if mode == "one_fact_crosstab":
        # 1-step post-hint shortcut: bivariate regression on fixed-24h BIP count WITHOUT controlling for
        # overlapping consist_wagons_short and loco_derate_sh (confounded by shared peak congestion!)
        bip_24 = is_rail & lot_bip[cont_ched] & (lot_lead[cont_ched] <= 24.0)
        n_24 = np.bincount(sh_id[bip_24], minlength=n_sh).astype(float)
        active = w["planned_on_shuttle"] > 0
        Xb = np.column_stack([np.ones(n_sh), n_24])
        bb, _, _, _ = np.linalg.lstsq(Xb[active], rolled_sh[active], rcond=None)
        bip_hat_1f = n_24 * max(0.0, float(bb[1]))
        rail_hat_1f = np.maximum(0.05, np.full(n_sh, max(0.05, float(bb[0]))))
        bip_share = np.where(
            (rolled_sh > 0) & (bip_hat_1f > 0),
            bip_hat_1f / (bip_hat_1f + rail_hat_1f),
            0.0,
        )
        bip_days = sh_roll_days * bip_share
        return sh_roll_days - bip_days + sh_base_days, bip_days, sh_sib_days, {"bip_slope": float(bb[1])}

    if mode in ("over", "generous", "cutoff_any_bip"):
        lim = 32.0 if mode == "cutoff_any_bip" else (48.0 if mode == "over" else 36.0)
        bip_any = is_rail & lot_bip[cont_ched] & (lot_lead[cont_ched] <= lim)
        has_bip = np.bincount(sh_id[bip_any], minlength=n_sh) > 0
        bip_days = np.where(has_bip, sh_roll_days, 0.0)
        return sh_roll_days - bip_days + sh_base_days, bip_days, sh_sib_days, {"bip_slope": 1.35}

    cons_short = w["consist_wagons_short_sh"].astype(float)
    loco_der = w["loco_derate_sh"].astype(float)
    booked = w["wf_booked_slots_sh"].astype(float)
    active = w["planned_on_shuttle"] > 0

    if method == "binned_lead":
        # Non-parametric port-by-lead-time bins (reference category: non-BIP and early-notice > 32h)
        edges = [0.0, 12.0, 16.0, 22.0, 28.0, 32.0]
        bip_cols = []
        for p in range(3):
            for lo_e, hi_e in zip(edges[:-1], edges[1:]):
                mk = is_rail & lot_bip[cont_ched] & (w["cont_port"] == p) & (lot_lead[cont_ched] >= lo_e) & (lot_lead[cont_ched] < hi_e)
                bip_cols.append(np.bincount(sh_id[mk], minlength=n_sh).astype(float))
        Xb = np.column_stack(bip_cols)
        Xc = np.column_stack([np.ones(n_sh), cons_short, loco_der])
        X = np.column_stack([Xb, Xc])
        b, _, _, _ = np.linalg.lstsq(X[active], rolled_sh[active], rcond=None)
        b_bins = np.maximum(0.0, b[:Xb.shape[1]])
        bip_hat = Xb @ b_bins
        rail_hat = np.maximum(0.02, Xc @ b[Xb.shape[1]:])
        bip_slope = float(np.mean([b_bins[0], b_bins[5], b_bins[10]]))
    else:
        cuts = []
        for p in range(3):
            mp = active & (sh_port == p)
            best_c, best_rss = 20.0, 1e18
            for cand in (10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0, 26.0, 28.0, 30.0, 32.0):
                if method == "hard_step":
                    mk = is_rail & lot_bip[cont_ched] & (lot_lead[cont_ched] <= cand)
                    lk = np.bincount(sh_id[mk], minlength=n_sh).astype(float)
                else:
                    lp_c = _sigmoid((cand - lot_lead[cont_ched]) / 1.8)
                    lk = np.bincount(sh_id, weights=np.where(is_rail & lot_bip[cont_ched], lp_c, 0.0), minlength=n_sh)
                Xp = np.column_stack([np.ones(mp.sum()), lk[mp], cons_short[mp], loco_der[mp]])
                bp, _, _, _ = np.linalg.lstsq(Xp, rolled_sh[mp], rcond=None)
                rss = float(np.sum((rolled_sh[mp] - Xp @ bp) ** 2))
                if rss < best_rss:
                    best_rss, best_c = rss, cand
            cuts.append(best_c + cut_shift)

        if method == "hard_step":
            mk_lk = is_rail & lot_bip[cont_ched] & (lot_lead[cont_ched] <= np.array(cuts)[w["cont_port"]])
            n_lk = np.bincount(sh_id[mk_lk], minlength=n_sh).astype(float)
        else:
            lp = _sigmoid((np.array(cuts)[w["cont_port"]] - lot_lead[cont_ched]) / 1.8)
            wt_lk = np.where(is_rail & lot_bip[cont_ched], lp, 0.0)
            n_lk = np.bincount(sh_id, weights=wt_lk, minlength=n_sh)

        n_lk_p = np.column_stack([n_lk * (sh_port == p) for p in range(3)])
        ctrl = [np.ones(n_sh), cons_short, loco_der]
        if method == "booked_ctrl":
            ctrl.append(booked)
        if method == "month_fe":
            mo = np.minimum(11, w["shuttle_day"] // 31)
            ctrl += [(mo == m).astype(float) for m in range(1, 12)]
            ctrl += [(w["shuttle_corr"] == c).astype(float) for c in range(1, 6)]

        if method == "pooled_slope":
            X = np.column_stack([n_lk] + ctrl)
            k_b = 1
        else:
            X = np.column_stack([n_lk_p] + ctrl)
            k_b = 3

        Xa, ya = X[active], rolled_sh[active]
        if method == "huber":
            b, _, _, _ = np.linalg.lstsq(Xa, ya, rcond=None)
            for _ in range(8):
                res = ya - Xa @ b
                sc = np.median(np.abs(res)) * 1.4826 + 1e-6
                wt = np.where(np.abs(res) <= 1.345 * sc, 1.0, 1.345 * sc / np.maximum(np.abs(res), 1e-9))
                b, _, _, _ = np.linalg.lstsq(Xa * np.sqrt(wt)[:, None], ya * np.sqrt(wt), rcond=None)
        elif method == "poisson_irls":
            b = np.maximum(0.05, np.linalg.lstsq(Xa, ya, rcond=None)[0])
            for _ in range(10):
                mu = np.maximum(0.15, Xa @ b)
                w_ir = 1.0 / mu
                b, _, _, _ = np.linalg.lstsq(Xa * np.sqrt(w_ir)[:, None], ya * np.sqrt(w_ir), rcond=None)
        else:
            b, _, _, _ = np.linalg.lstsq(Xa, ya, rcond=None)

        b_bip = np.maximum(0.0, b[:k_b])
        bip_hat = X[:, :k_b] @ b_bip
        rail_hat = np.maximum(0.02, X[:, k_b:] @ b[k_b:])
        bip_slope = float(np.mean(b_bip))

    # Exact Poisson-thinning posterior share E[X_bip | rolled_sh] = rolled_sh * lam_bip / (lam_bip + lam_rail)
    # Zero Jensen clipping attenuation bias!
    bip_share = np.where(
        (rolled_sh > 0) & (bip_hat > 0),
        bip_hat / np.maximum(bip_hat + rail_hat, 1e-9),
        0.0,
    )
    bip_days = sh_roll_days * bip_share
    rail_days = sh_roll_days - bip_days + sh_base_days
    return rail_days, bip_days, sh_sib_days, {"bip_slope": bip_slope}


def estimate_s3(w, mode="golden", fe="dc_week", spec_form="linear"):
    """Estimate S3 split of obs_dray_empty_hold between drayage_carrier (carrier) and empty_depot (ocean line)."""
    y = w["obs_dray_empty_hold"]
    n = len(y)
    u_day = w["cont_unload_day"]
    rej_c = w["portal_rejected"][w["cont_port"], w["cont_line"], u_day]

    if mode in ("hurried", "direct", "rigorous", "calibrated"):
        return y.copy(), np.zeros(n), {"drain_gap_h": 0.0}
    if mode == "hedge":
        blk = y * 0.14
        return y - blk, blk, {"drain_gap_h": 1.5}

    q_grid = _reconstruct_depot_queue(w)
    q_c = q_grid[w["cont_port"], w["cont_line"], u_day]
    op = rej_c == 0
    hi_q = op & (q_c >= 0.8)
    lo_q = op & (q_c < 0.15)

    if mode == "one_fact_binary":
        # 1-step post-hint shortcut: binary portal_rejected > 0 on unload day!
        closed = rej_c > 0
        open_q = ~closed
        grp = w["cont_dc"] * w["N_QUEUE_DAYS"] + u_day
        max_k = 4 * w["N_QUEUE_DAYS"]
        cnt = np.bincount(grp[open_q], minlength=max_k)
        sm = np.bincount(grp[open_q], weights=y[open_q], minlength=max_k)
        dc_mu = np.array([y[open_q & (w["cont_dc"] == d)].mean() for d in range(4)])
        base_c = np.where(cnt[grp] > 0, sm[grp] / np.maximum(1, cnt[grp]), dc_mu[w["cont_dc"]])
        blk = np.where(closed, np.maximum(0.0, y - base_c), 0.0)
        return y - blk, blk, {"drain_gap_h": 0.0}

    if mode in ("over", "generous", "cutoff_raw"):
        # Over-correction / port-aggregated raw cutoff: flags ALL containers at a port whenever port-level
        # depot backlog exceeds threshold (ignoring shipping-line isolation and wiping genuine carrier drayage!)
        q_port_grid = q_grid.sum(axis=1)
        rej_port_grid = w["portal_rejected"].sum(axis=1)
        q_p = q_port_grid[w["cont_port"], u_day]
        rej_p = rej_port_grid[w["cont_port"], u_day]
        cut = 0.25 if mode == "over" else (0.35 if mode == "generous" else 0.55)
        blk = np.where((rej_p > 0) | (q_p >= cut), y, 0.0)
        dh = float((blk[hi_q].mean() - blk[lo_q].mean()) * 24.0) if (np.any(hi_q) and np.any(lo_q)) else 0.0
        return y - blk, blk, {"drain_gap_h": dh}

    if fe == "dc_day":
        grp = w["cont_dc"] * w["N_QUEUE_DAYS"] + u_day
        n_grp = 4 * w["N_QUEUE_DAYS"]
    elif fe == "port_day":
        grp = w["cont_port"] * w["N_QUEUE_DAYS"] + u_day
        n_grp = 3 * w["N_QUEUE_DAYS"]
    elif fe == "corr_week":
        grp = w["cont_corr"] * 56 + (u_day // 7)
        n_grp = 6 * 56
    else:
        grp = w["cont_dc"] * 56 + (u_day // 7)
        n_grp = 4 * 56

    if spec_form == "quad":
        X = np.column_stack(
            [q_c * (w["cont_corr"] == c) for c in range(6)]
            + [(q_c ** 2) * (w["cont_corr"] == c) for c in range(6)]
        )
    elif spec_form == "dist_param":
        dist_f = (CORR_DIST_KM[w["cont_corr"]] - 150.0) / 100.0
        X = np.column_stack([q_c, q_c * dist_f])
    else:
        X = np.column_stack([q_c * (w["cont_corr"] == c) for c in range(6)])

    if fe == "harmonic":
        t_rad = 2.0 * np.pi * (u_day % N_DAYS) / 365.0
        ctrl = [(w["cont_corr"] == c).astype(float) for c in range(6)]
        ctrl += [((u_day % 7) == wd).astype(float) for wd in range(1, 7)]
        for h in (1, 2, 3, 4):
            ctrl += [np.sin(h * t_rad), np.cos(h * t_rad)]
        X_full = np.column_stack([X] + ctrl)
        b, _, _, _ = np.linalg.lstsq(X_full, y, rcond=None)
        b_q = np.maximum(0.0, b[:X.shape[1]])
        pred_blk = np.maximum(0.0, X @ b_q)
        pred_base = np.maximum(0.02, X_full[:, X.shape[1]:] @ b[X.shape[1]:])
    else:
        c_dum = np.column_stack([(w["cont_corr"] == c).astype(float) for c in range(1, 6)])
        dow_dum = np.column_stack([((u_day % 7) == wd).astype(float) for wd in range(1, 7)])
        X_full = np.column_stack([X, c_dum, dow_dum])
        Xd = _demean_by_group(X_full, grp, n_grp)
        yd = _demean_by_group(y, grp, n_grp)
        if spec_form == "huber":
            b, _, _, _ = np.linalg.lstsq(Xd, yd, rcond=None)
            for _ in range(8):
                res = yd - Xd @ b
                sc = np.median(np.abs(res)) * 1.4826 + 1e-6
                wt = np.where(np.abs(res) <= 1.345 * sc, 1.0, 1.345 * sc / np.maximum(np.abs(res), 1e-9))
                b, _, _, _ = np.linalg.lstsq(Xd * np.sqrt(wt)[:, None], yd * np.sqrt(wt), rcond=None)
        else:
            b, _, _, _ = np.linalg.lstsq(Xd, yd, rcond=None)
        b_q = np.maximum(0.0, b[:X.shape[1]])
        pred_blk = np.maximum(0.0, X @ b_q)
        rem = y - X_full @ b
        cnt_g = np.maximum(1.0, np.bincount(grp, minlength=n_grp).astype(float))
        fe_hat = (np.bincount(grp, weights=rem, minlength=n_grp) / cnt_g)[grp]
        pred_base = np.maximum(0.02, fe_hat + X_full[:, X.shape[1]:] @ b[X.shape[1]:])

    # Proportional Gamma posterior share (strictly inside [0, y] with zero clipping attenuation bias!)
    blk = np.where(pred_blk > 0.0, y * (pred_blk / (pred_blk + pred_base)), 0.0)
    dh = float((blk[hi_q].mean() - blk[lo_q].mean()) * 24.0) if (np.any(hi_q) and np.any(lo_q)) else 0.0
    return y - blk, blk, {"drain_gap_h": dh}


def _residual_orthogonality_error(w, plug_c, rail_sh, dray_c):
    """Two-sided parameter-free physical diagnostic computed strictly from observables (observes_target: False):
    For each mechanism, checks BOTH (a) orthogonality of residual carrier delay to non-carrier drivers
    (catches under-correction / direct / rigorous / 1-step shortcuts), AND (b) preservation of genuine
    carrier-driver sensitivity on overlap days compared to clean baseline days (catches over-correction /
    generous / raw cutoffs that zero out real carrier delay):
      (F1) S1: residual plug filling-vs-draining gap in [0.84, 0.94] chamber util + port-yard-util slope preservation on u_ch >= 0.82
      (F2) S2: port-weighted residual rail partial slopes on locked, cross-24h window & early-notice BIP lots + consist_wagons_short preservation
      (F3) S3: residual drayage open-portal drain gap (rej==0) + baseline preservation on q >= 0.30 days."""
    ch_u, ch_nf = _reconstruct_chambers(w)
    u_ch_c = ch_u[w["cont_dc"], w["cont_zone"], w["cont_day"]]
    nf_c = ch_nf[w["cont_dc"], w["cont_zone"], w["cont_day"]]
    bm = (u_ch_c >= 0.84) & (u_ch_c <= 0.94)
    p_dm = _demean_by_group(plug_c, w["cont_vessel"] * 6 + w["cont_corr"], N_VESSELS * 6)
    f1_asym_h = abs(float((p_dm[bm & (nf_c > 0)].mean() - p_dm[bm & (nf_c <= 0)].mean()) * 24.0))

    # F1b: genuine port_yard_util response preserved on u_ch >= 0.82 vs clean u_ch < 0.78 days
    u_port = w["port_yard_util"][w["cont_port"], w["cont_day"]]
    lo_ch = u_ch_c < 0.78
    hi_ch = u_ch_c >= 0.82
    x_p = np.maximum(0.0, u_port - 0.80) ** 2
    b_lo = float(np.cov(x_p[lo_ch], plug_c[lo_ch])[0, 1] / max(1e-9, np.var(x_p[lo_ch])))
    b_hi = float(np.cov(x_p[hi_ch], plug_c[hi_ch])[0, 1] / max(1e-9, np.var(x_p[hi_ch])))
    f1_pres = max(0.0, (b_lo - b_hi) / max(1.0, abs(b_lo)))

    # F2a: low-variance pooled locked-BIP slope + 1-df constructive cross-24h contrast (HAM 24-28h minus BHV 16-24h) + early BIP
    n_sh = len(rail_sh)
    active = w["planned_on_shuttle"] > 0
    sh_base = np.bincount(w["cont_shuttle"], weights=w["cont_rail_base"], minlength=n_sh)
    res_roll_days = rail_sh - sh_base
    is_bip_rail = w["cont_is_rail"] & w["lot_bip"][w["cont_ched"]]
    lead_c = w["lot_lead_hours"][w["cont_ched"]]
    cut_c = PORT_LOCK_MID_H[w["cont_port"]]
    n_lk = np.bincount(w["cont_shuttle"][is_bip_rail & (lead_c <= cut_c)], minlength=n_sh).astype(float)
    n_bhv_mid = np.bincount(w["cont_shuttle"][is_bip_rail & (w["cont_port"] == 0) & (lead_c > 16.0) & (lead_c <= 24.0)], minlength=n_sh).astype(float)
    n_ham_mid = np.bincount(w["cont_shuttle"][is_bip_rail & (w["cont_port"] == 1) & (lead_c > 24.0) & (lead_c <= 28.0)], minlength=n_sh).astype(float)
    n_cross24 = n_ham_mid - n_bhv_mid
    n_early = np.bincount(w["cont_shuttle"][is_bip_rail & (lead_c > cut_c + 4.0)], minlength=n_sh).astype(float)
    cs = w["consist_wagons_short_sh"].astype(float)
    ld = w["loco_derate_sh"].astype(float)
    bk = w["wf_booked_slots_sh"].astype(float)
    X2 = np.column_stack([np.ones(n_sh), n_lk, n_cross24, n_early, cs, ld, bk])
    b2, _, _, _ = np.linalg.lstsq(X2[active], res_roll_days[active], rcond=None)
    # Also check preservation of consist_wagons_short slope on BIP-present shuttles against full-sample observable slope
    sh_tot_roll = np.bincount(w["cont_shuttle"], weights=w["cont_rail_roll_dur"], minlength=n_sh)
    b_tot_cs = float(np.linalg.lstsq(X2[active], sh_tot_roll[active], rcond=None)[0][4])
    has_bip_sh = np.bincount(w["cont_shuttle"][is_bip_rail], minlength=n_sh) > 0
    m1 = active & has_bip_sh
    Xcs1 = np.column_stack([np.ones(m1.sum()), cs[m1], ld[m1], n_lk[m1]])
    b_cs1 = float(np.linalg.lstsq(Xcs1, res_roll_days[m1], rcond=None)[0][1])
    f2_err = (
        abs(float(b2[1]))
        + 1.2 * abs(float(b2[2]))
        + abs(float(b2[3]))
        + 1.8 * max(0.0, b_tot_cs - b_cs1)
    )

    # F3a: residual carrier drayage open-portal drain gap + baseline preservation on q >= 0.30 days
    q_obs = _reconstruct_depot_queue(w)[w["cont_port"], w["cont_line"], w["cont_unload_day"]]
    rej_obs = w["portal_rejected"][w["cont_port"], w["cont_line"], w["cont_unload_day"]]
    op = rej_obs == 0
    d_dm = _demean_by_group(dray_c, w["cont_corr"] * 56 + (w["cont_unload_day"] // 7), 6 * 56)
    f3_drain_h = abs(float((d_dm[op & (q_obs >= 0.8)].mean() - d_dm[op & (q_obs < 0.15)].mean()) * 24.0))
    f3_drop_h = max(0.0, float((d_dm[op & (q_obs < 0.15)].mean() - d_dm[q_obs >= 0.30].mean()) * 24.0))

    return f1_asym_h * 20.0 + f1_pres * 220.0 + f2_err * 220.0 + f3_drain_h * 20.0 + f3_drop_h * 40.0


def evaluate_corridors(w, plug_c, pb_c, rail_sh, bip_bump_sh, sib_sh, dray_c, dep_blk_c, opts=None):
    opts = opts or {}
    m_s1 = opts.get("mult_s1", 1.0)
    m_s2 = opts.get("mult_s2", 1.0)
    m_s3 = opts.get("mult_s3", 1.0)
    m_base = opts.get("mult_base", 1.0)

    if m_s1 != 1.0:
        pb_eff = np.clip(pb_c * m_s1, 0.0, w["obs_term_yard_hold"])
        plug_eff = w["obs_term_yard_hold"] - pb_eff
    else:
        pb_eff, plug_eff = pb_c, plug_c

    if m_s2 != 1.0:
        tot_sh_roll = np.bincount(w["cont_shuttle"], weights=w["cont_rail_roll_dur"], minlength=len(rail_sh))
        base_sh = np.bincount(w["cont_shuttle"], weights=w["cont_rail_base"], minlength=len(rail_sh))
        bip_eff = np.clip(bip_bump_sh * m_s2, 0.0, tot_sh_roll)
        rail_eff = (tot_sh_roll - bip_eff) + base_sh
    else:
        bip_eff, rail_eff = bip_bump_sh, rail_sh

    if m_s3 != 1.0:
        dep_eff = np.clip(dep_blk_c * m_s3, 0.0, w["obs_dray_empty_hold"])
        dray_eff = w["obs_dray_empty_hold"] - dep_eff
    else:
        dep_eff, dray_eff = dep_blk_c, dray_c

    bcrs = {}
    avoid_eur = {}
    cc_days_27 = {}
    for c_idx, cname in enumerate(CORRIDORS):
        p_name = PORTS[CORR_PORT[c_idx]]
        vg = PLAN_2027["vol_growth_corridor"][cname] * m_base
        mc = w["cont_corr"] == c_idx
        ms = w["shuttle_corr"] == c_idx

        rp_27 = float(plug_eff[mc].sum()) * vg * PLAN_2027["plug_capacity_factor_2027"][p_name]
        rh_27 = float(rail_eff[ms].sum()) * vg * PLAN_2027["rail_fleet_factor_2027"][p_name]
        dr_27 = float(dray_eff[mc].sum()) * vg * PLAN_2027["dray_contract_factor_2027"][p_name]

        gross_eur = (
            rp_27 * TARIFF_EUR["reefer_plug"]
            + rh_27 * TARIFF_EUR["rail_handoff"]
            + dr_27 * TARIFF_EUR["drayage_carrier"]
        )
        av_eur = gross_eur * CORR_CAPTURE_RATE[cname]
        cc_days_27[cname] = rp_27 + rh_27 + dr_27
        avoid_eur[cname] = av_eur
        bcrs[cname] = av_eur / CORR_BUDGET_EUR[cname]

    return {
        "members": bcrs,
        "avoid_eur": avoid_eur,
        "cc_days_27": cc_days_27,
        "C1_coldstore_pullback_2026": float(pb_eff.sum()),
        "C2_phyto_rail_roll_2026": float(bip_eff.sum()),
        "C3_depot_backlog_2026": float(dep_eff.sum()),
        "fal_err": _residual_orthogonality_error(w, plug_eff, rail_eff, dray_eff),
    }


def _truth_eval(w):
    t = w["_truth"]
    n_sh = len(w["shuttle_corr"])
    rail_sh = np.bincount(w["cont_shuttle"], weights=t["rail_short_c"] + t["rail_base_c"], minlength=n_sh)
    bip_sh = np.bincount(w["cont_shuttle"], weights=t["phyto_bump_c"], minlength=n_sh)
    sib_sh = np.bincount(w["cont_shuttle"], weights=t["phyto_sibling_rail_c"], minlength=n_sh)
    return evaluate_corridors(
        w, t["reefer_plug_c"], t["coldstore_pullback_c"],
        rail_sh, bip_sh, sib_sh,
        t["dray_carrier_c"], t["depot_portal_block_c"],
    )


def _run_combo(w, s1_kw, s2_kw, s3_kw, opts=None):
    rp, pb, m1 = estimate_s1(w, **s1_kw)
    rh, bb, sb, m2 = estimate_s2(w, **s2_kw)
    dr, db, m3 = estimate_s3(w, **s3_kw)
    res = evaluate_corridors(w, rp, pb, rh, bb, sb, dr, db, opts=opts)
    res["meta"] = {**m1, **m2, **m3}
    return res


def build_spec(seed=SEED):
    w = simulate_world(seed)
    tr = _truth_eval(w)
    gold = _run_combo(w, {"mode": "golden"}, {"mode": "golden"}, {"mode": "golden"})

    fam_configs = [
        ("S1: binned non-param", {"mode": "golden", "spec_form": "bins"}, {"mode": "golden"}, {"mode": "golden"}),
        ("S1: piecewise spline", {"mode": "golden", "spec_form": "spline"}, {"mode": "golden"}, {"mode": "golden"}),
        ("S1: Huber robust FE", {"mode": "golden", "spec_form": "huber"}, {"mode": "golden"}, {"mode": "golden"}),
        ("S1: port-day FE", {"mode": "golden", "fe": "port_day"}, {"mode": "golden"}, {"mode": "golden"}),
        ("S1: corr-week FE", {"mode": "golden", "fe": "corr_week"}, {"mode": "golden"}, {"mode": "golden"}),
        ("S1: hinge 0.76", {"mode": "golden", "hinge": 0.76}, {"mode": "golden"}, {"mode": "golden"}),
        ("S1: hinge 0.80", {"mode": "golden", "hinge": 0.80}, {"mode": "golden"}, {"mode": "golden"}),
        ("S2: Poisson IRLS", {"mode": "golden"}, {"mode": "golden", "method": "poisson_irls"}, {"mode": "golden"}),
        ("S2: Huber robust", {"mode": "golden"}, {"mode": "golden", "method": "huber"}, {"mode": "golden"}),
        ("S2: binned lead (no cut)", {"mode": "golden"}, {"mode": "golden", "method": "binned_lead"}, {"mode": "golden"}),
        ("S2: hard step cut", {"mode": "golden"}, {"mode": "golden", "method": "hard_step"}, {"mode": "golden"}),
        ("S2: month+corr FE", {"mode": "golden"}, {"mode": "golden", "method": "month_fe"}, {"mode": "golden"}),
        ("S2: pooled slope", {"mode": "golden"}, {"mode": "golden", "method": "pooled_slope"}, {"mode": "golden"}),
        ("S2: booked-slot ctrl", {"mode": "golden"}, {"mode": "golden", "method": "booked_ctrl"}, {"mode": "golden"}),
        ("S3: dc-day FE", {"mode": "golden"}, {"mode": "golden"}, {"mode": "golden", "fe": "dc_day"}),
        ("S3: port-day FE", {"mode": "golden"}, {"mode": "golden"}, {"mode": "golden", "fe": "port_day"}),
        ("S3: corr-week FE", {"mode": "golden"}, {"mode": "golden"}, {"mode": "golden", "fe": "corr_week"}),
        ("S3: harmonic OLS", {"mode": "golden"}, {"mode": "golden"}, {"mode": "golden", "fe": "harmonic"}),
        ("S3: Huber robust FE", {"mode": "golden"}, {"mode": "golden"}, {"mode": "golden", "spec_form": "huber"}),
        ("S3: distance param", {"mode": "golden"}, {"mode": "golden"}, {"mode": "golden", "spec_form": "dist_param"}),
        ("Joint: spline+poisson+dcday", {"mode": "golden", "spec_form": "spline"},
         {"mode": "golden", "method": "poisson_irls"}, {"mode": "golden", "fe": "dc_day"}),
    ]
    fam_runs = [(nm, _run_combo(w, k1, k2, k3)) for nm, k1, k2, k3 in fam_configs]

    combos = [c for r in (1, 2, 3) for c in itertools.combinations(("S1", "S2", "S3"), r)]
    lat_runs = {}
    for c in combos:
        k1 = {"mode": "hurried"} if "S1" in c else {"mode": "golden"}
        k2 = {"mode": "hurried"} if "S2" in c else {"mode": "golden"}
        k3 = {"mode": "hurried"} if "S3" in c else {"mode": "golden"}
        lat_runs["+".join(c)] = _run_combo(w, k1, k2, k3)

    direct = _run_combo(w, {"mode": "direct"}, {"mode": "direct"}, {"mode": "direct"})
    rigorous = _run_combo(w, {"mode": "rigorous"}, {"mode": "rigorous"}, {"mode": "rigorous"})
    generous = _run_combo(w, {"mode": "generous"}, {"mode": "generous"}, {"mode": "generous"})
    hedge = _run_combo(w, {"mode": "hedge"}, {"mode": "hedge"}, {"mode": "hedge"})
    cutoff = _run_combo(w, {"mode": "cutoff_95"}, {"mode": "cutoff_any_bip"}, {"mode": "one_fact_binary"})

    s1_over = _run_combo(w, {"mode": "over"}, {"mode": "golden"}, {"mode": "golden"})
    s2_over = _run_combo(w, {"mode": "golden"}, {"mode": "over"}, {"mode": "golden"})
    s3_over = _run_combo(w, {"mode": "golden"}, {"mode": "golden"}, {"mode": "over"})

    s1_one_fact = _run_combo(w, {"mode": "one_fact_sym"}, {"mode": "golden"}, {"mode": "golden"})
    s2_one_fact = _run_combo(w, {"mode": "golden"}, {"mode": "one_fact_crosstab"}, {"mode": "golden"})
    s3_one_fact = _run_combo(w, {"mode": "golden"}, {"mode": "golden"}, {"mode": "one_fact_binary"})

    cut_s1_lin = _run_combo(w, {"mode": "cutoff_sym_lin"}, {"mode": "golden"}, {"mode": "golden"})
    cut_s3_raw = _run_combo(w, {"mode": "golden"}, {"mode": "golden"}, {"mode": "cutoff_raw"})

    members = {}
    for c in CORRIDORS:
        members[c] = {
            "truth": tr["members"][c],
            "golden": gold["members"][c],
            "family": [r["members"][c] for _, r in fam_runs],
            "routes": {
                "direct": direct["members"][c],
                "rigorous": rigorous["members"][c],
            },
        }

    stumps = {
        "S1": {
            "axis": "what",
            "opens": "BHV-KAS",
            "said_out_loud": "inland DC thermal chambers pull back containers at the port yard more steeply when filling than when draining",
            "steps_left": 4,
            "precedents": ["L26", "L28", "L38", "N36"],
            "sides": {"over": s1_over["members"]},
            "one_fact_shortcut": {
                "members": s1_one_fact["members"],
                "component": s1_one_fact["C1_coldstore_pullback_2026"],
            },
        },
        "S2": {
            "axis": "unit",
            "opens": "HAM-MAG",
            "said_out_loud": "late EU BIP inspection notices lock booked rail slots with terminal-specific cutoffs and overlap Nordbahn short-consist cuts",
            "steps_left": 4,
            "precedents": ["L03", "L07", "L48", "N07"],
            "sides": {"over": s2_over["members"]},
            "one_fact_shortcut": {
                "members": s2_one_fact["members"],
                "component": s2_one_fact["C2_phyto_rail_roll_2026"],
            },
        },
        "S3": {
            "axis": "when",
            "opens": "BHV-HAN",
            "said_out_loud": "ocean-line empty-depot portal closures build multi-day return queues that outlive portal reopening across inland corridors",
            "steps_left": 4,
            "precedents": ["N14", "N27", "L56", "L57"],
            "sides": {"over": s3_over["members"]},
            "one_fact_shortcut": {
                "members": s3_one_fact["members"],
                "component": s3_one_fact["C3_depot_backlog_2026"],
            },
        },
    }

    lattice = {k: r["members"] for k, r in lat_runs.items()}

    figures = []
    for fid, key in (
        ("C1_coldstore_pullback_2026", "C1_coldstore_pullback_2026"),
        ("C2_phyto_rail_roll_2026", "C2_phyto_rail_roll_2026"),
        ("C3_depot_backlog_2026", "C3_depot_backlog_2026"),
    ):
        figures.append({
            "id": fid,
            "block": "component",
            "golden": gold[key],
            "family": [r[key] for _, r in fam_runs],
            "lattice": {k: r[key] for k, r in lat_runs.items()},
            "routes": {
                "rigorous": rigorous[key],
                "generous": generous[key],
                "hedge": hedge[key],
                "cutoff": cutoff[key],
            },
        })

    for c in CORRIDORS:
        figures.append({
            "id": "BCR_" + c.replace("-", "_"),
            "block": "ask",
            "member": c,
            "ecf": False,
        })

    spec = {
        "task": "task27",
        "v4_hardened": True,
        "call": "top_k",
        "k": TOP_K,
        "members": members,
        "stumps": stumps,
        "lattice": lattice,
        "figures": figures,
        "falsification": {
            "check": "Combined observable residual orthogonality error (F1 residual plug filling-vs-draining gap & rack-slope preservation, F2 residual rail BIP-lock & cross-24h slopes & consist preservation, F3 residual drayage open-portal drain gap & baseline preservation)",
            "observes_target": False,
            "truth": 0.0,
            "golden": gold["fal_err"],
            "rivals": {
                "direct": direct["fal_err"],
                "rigorous": rigorous["fal_err"],
                "generous": generous["fal_err"],
                "hedge": hedge["fal_err"],
                "cutoff": cutoff["fal_err"],
                "S1_one_fact": s1_one_fact["fal_err"],
                "S2_one_fact": s2_one_fact["fal_err"],
                "S3_one_fact": s3_one_fact["fal_err"],
            },
        },
        "run_routes": {
            "generous": generous["members"],
            "calibrated": {"none": "no shipped file observes true carrier-controllable split or any stump quantity directly"},
            "hedge": hedge["members"],
            "cutoff": cutoff["members"],
            "cutoff:s1_sym_lin": cut_s1_lin["members"],
            "cutoff:s1_one_fact": s1_one_fact["members"],
            "cutoff:s2_one_fact": s2_one_fact["members"],
            "cutoff:s3_one_fact": s3_one_fact["members"],
            "cutoff:s3_raw": cut_s3_raw["members"],
        },
    }
    return w, tr, gold, fam_runs, lat_runs, spec


def check_forcing(w, gold):
    g_top = tuple(sorted(sorted(CORRIDORS, key=lambda c: (-gold["members"][c], c))[:TOP_K]))
    best_eur, best_set = -1.0, None
    for r in range(1, len(CORRIDORS) + 1):
        for comb in itertools.combinations(CORRIDORS, r):
            if sum(CORR_BUDGET_EUR[c] for c in comb) <= BUDGET_CAP_EUR:
                tot = sum(gold["avoid_eur"][c] for c in comb)
                if tot > best_eur:
                    best_eur, best_set = tot, tuple(sorted(comb))
    print(f"Greedy top-{TOP_K}: {g_top}; Knapsack opt: {best_set} (EUR {best_eur:,.0f}); MATCH={g_top == best_set}")

    t = w["_truth"]
    locked_pos = t["n_locked_phyto_sh"] > 0
    lt_cnt = int((w["wf_standby_rolled_total_sh"][locked_pos] < t["n_locked_phyto_sh"][locked_pos]).sum())
    n_lk_sh = int(locked_pos.sum())
    rolled_nz = w["cont_rail_roll_dur"][w["cont_rolled_rail"]]
    print(f"S2 realism: locked shuttles={n_lk_sh}, rolled<locked={lt_cnt} ({100*lt_cnt/max(1,n_lk_sh):.1f}%), "
          f"roll_dur mean={rolled_nz.mean():.3f} sd={rolled_nz.std():.3f} CV={rolled_nz.std()/rolled_nz.mean():.3f}")
    Xw = np.column_stack([
        np.ones(len(w["shuttle_corr"])),
        w["train_wagon_count_sh"],
        w["wf_booked_slots_sh"],
        t["n_locked_phyto_sh"],
        w["consist_wagons_short_sh"],
    ])
    bw, _, _, _ = np.linalg.lstsq(Xw, w["train_gross_tonnes_sh"], rcond=None)
    rw = w["train_gross_tonnes_sh"] - Xw @ bw
    r2_w = 1.0 - np.var(rw) / np.var(w["train_gross_tonnes_sh"])
    print(f"S2 weighbridge OLS: locked_slope={bw[3]:.2f} t/slot, R^2={r2_w:.4f}, resid_sd={rw.std():.1f} t")

    ok_all = (g_top == best_set)
    for label, opts in (
        ("S1 -15%", {"mult_s1": 0.85}),
        ("S1 +15%", {"mult_s1": 1.15}),
        ("S2 -15%", {"mult_s2": 0.85}),
        ("S2 +15%", {"mult_s2": 1.15}),
        ("S3 -15%", {"mult_s3": 0.85}),
        ("S3 +15%", {"mult_s3": 1.15}),
        ("base -15%", {"mult_base": 0.85}),
        ("base +15%", {"mult_base": 1.15}),
    ):
        pr = _run_combo(w, {"mode": "golden"}, {"mode": "golden"}, {"mode": "golden"}, opts=opts)
        ptop = tuple(sorted(sorted(CORRIDORS, key=lambda c: (-pr["members"][c], c))[:TOP_K]))
        hold = ptop == g_top
        ok_all &= hold
        print(f"  Stress {label:10s}: {'HOLD' if hold else 'FLIP'} {ptop} | "
              + " ".join(f"{c}:{pr['members'][c]:.2f}" for c in CORRIDORS))
    print("FORCING:", "PASS" if ok_all else "FAIL")
    return ok_all


if __name__ == "__main__":
    w, tr, gold, fam_runs, lat_runs, spec = build_spec(SEED)
    if "--detail" in sys.argv or "--forcing" in sys.argv:
        print("Components (truth vs golden):")
        for k in ("C1_coldstore_pullback_2026", "C2_phyto_rail_roll_2026", "C3_depot_backlog_2026"):
            print(f"  {k}: truth={tr[k]:.1f}, golden={gold[k]:.1f}")
        print("Corridor BCRs (truth vs golden):")
        for c in CORRIDORS:
            print(f"  {c}: truth={tr['members'][c]:.3f}, golden={gold['members'][c]:.3f}, "
                  f"avoid_eur={gold['avoid_eur'][c]:,.0f}, budget={CORR_BUDGET_EUR[c]:,.0f}")
        check_forcing(w, gold)
    sys.exit(corelib.run(spec))
