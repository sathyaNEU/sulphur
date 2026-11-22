#!/usr/bin/env python3
"""Core operational process simulator, estimators, rival shortcuts, frontier run routes,
and corelib spec for task27 (Weserfrucht Import GmbH: 2026 root-cause attribution and
2027 Mandatory Remediation designation across 8 intermodal cold-chain failure modes).

Observation process (every primary record looks clean and internally coherent on the surface):
  - 24,000 forty-foot refrigerated import containers across 365 days of 2026, 3 North Sea port
    terminals (BHV, HAM, WHV), 4 inland cold-storage DCs (HAN, OSN, KAS, MAG), 3 sealed
    thermal chambers per DC (+2C Z02, +7C Z07, +13C Z13), 480 vessel calls, 1,095 shared
    intermodal rail shuttle departures, and 4 shipping-line empty depots (LINE_A..LINE_D).
  - Total 2026 excess container-days are conserved across 8 candidate operational causes
    (vessel_berth, edi_docs, coldstore_dock, reefer_plug, rail_handoff, phyto_insp,
    empty_depot, drayage_carrier), projected onto the 2027 Import Schedule Plan using one
    uniform leak-free cause-level scaling rule per cause against Charter RC-2027's threshold
    of 2,500 attributable excess container-days.

Three independent observation-process stumps on three distinct axes (all off the 45 closed cards):
  S1 (what)  Port-yard TERM_YARD_HOLD delays mix true port reefer-plug congestion with inland
             cold-store pull-back throttling when a destination DC's specific thermal chamber
             hits >=95% physical bay capacity. Opposing commodity seasons keep total DC pallet
             utilization flat (69-78%), so total-DC regressions find zero inland effect while
             port yard utilization correlates strongly with port dwell. Exact per-chamber daily
             stock-flow accounting (Opening + Receipts - Dispatches) and same-vessel-day
             unsaturated-chamber twin comparisons separate true reefer_plug from coldstore_dock.
  S2 (unit)  Intermodal rail RAIL_CAP_ROLL standby rollovers mix genuine rail-operator short-
             consists with cleared standby boxes bumped by phantom rail slots held physically
             empty for co-loaded CHED consignment lots frozen by BIP phytosanitary notices inside
             the T-24h loading lock. Train booked_slots reads ~98% full and raw weight/wagon
             looks normal across mixed third-party cargo. Linking containers -> CHED lots -> BIP
             notice times against T-24h locks recovers exact 1-to-1 locked empty slots, confirmed
             by the exact -28.5 t/slot empty-flatcar deficit in shared-train weighbridge tonnage.
  S3 (who)   Drayage-yard DRAY_EMPTY_HOLD detention mixes genuine drayage carrier turnaround
             backlog with shipping-line empty-depot daily portal quota closures on the container's
             physical inland unload day (cont_unload_day). Physical depot gate acceptance is ~96%
             because truckers never drive to a closed gate, while the online portal rejection log
             lacks container IDs and carries ~2.4x multi-day retry multiplicity. Exact (depot,
             shipping_line) daily empty stock-flow accounting and same-DC same-unload-day
             open-vs-closed shipping-line turnaround contrasts separate true empty_depot quota
             blocking from drayage_carrier turnaround, confirmed by retry multiplicity conservation.

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

SEED = 2701
LINE_THRESHOLD = 2500.0
N_DAYS = 365
N_CONTAINERS = 24000
N_VESSELS = 480
# Exact 2026 non-leap calendar quarter boundaries (0-indexed day of year):
# Q1: 0..89 (Jan 1 - Mar 31), Q2: 90..180 (Apr 1 - Jun 30),
# Q3: 181..272 (Jul 1 - Sep 30), Q4: 273..364 (Oct 1 - Dec 31).
QUARTER_BOUNDS = np.array([90, 181, 273], dtype=int)

PORTS = ("BHV", "HAM", "WHV")
PORT_SHARES = np.array([0.46, 0.38, 0.16])
DCS = ("HAN", "OSN", "KAS", "MAG")
DC_SHARES = np.array([0.30, 0.24, 0.24, 0.22])
ZONES = ("Z02", "Z07", "Z13")  # +2C berries/stonefruit, +7C citrus/pome, +13C tropical
LINES = ("LINE_A", "LINE_B", "LINE_C", "LINE_D")

MEMBERS = (
    "coldstore_dock",
    "drayage_carrier",
    "edi_docs",
    "empty_depot",
    "phyto_insp",
    "rail_handoff",
    "reefer_plug",
    "vessel_berth",
)

# Contractual daily detention/demurrage & cold-chain exposure tariffs (EUR / container-day),
# filed verbatim in weserfrucht_remediation_charter_rc2027.pdf (Schedule B).
TARIFF_EUR = {
    "vessel_berth": 195.0,
    "edi_docs": 140.0,
    "reefer_plug": 210.0,
    "coldstore_dock": 285.0,
    "rail_handoff": 175.0,
    "phyto_insp": 260.0,
    "drayage_carrier": 160.0,
    "empty_depot": 230.0,
}

# Filed 2027 Import Schedule & Capacity Plan parameters (in import_plan_2027.csv & Charter RC-2027
# Annex C). Every key has a neutral operational business name and applies uniformly at the cause
# level (zero sub-component projection splits, zero stump leakage).
PLAN_2027 = {
    "vol_growth_port": {"BHV": 1.10, "HAM": 1.12, "WHV": 1.06},
    "vol_growth_zone": {"Z02": 1.38, "Z07": 1.04, "Z13": 1.06},
    # Bremerhaven Berth 4 reefer-plug upgrade cuts BHV reefer_plug factor to 0.78x; HAM/WHV 1.00x.
    "plug_capacity_factor_2027": {"BHV": 0.78, "HAM": 1.00, "WHV": 1.00},
    # Uniform coldstore_dock 2027 DC temperature-class load factor (fixed 2027 DC bay footprint
    # against planned 2027 produce growth by temperature class).
    "dc_zone_load_factor_2027": {"Z02": 1.48, "Z07": 1.06, "Z13": 1.08},
    # Uniform phyto_insp 2027 EU Priority-Pest BIP sampling factor by port origin mix;
    # uniform rail_handoff 2027 Nordbahn locomotive expansion factor.
    "bip_sampling_factor_2027": {"BHV": 1.25, "HAM": 1.23, "WHV": 1.20},
    "rail_fleet_factor_2027": 0.84,
    # Uniform empty_depot 2027 Ocean Alliance volume shares and depot utilization load factor;
    # uniform drayage_carrier 2027 dedicated contract turnaround factor.
    "line_share_2027": {"LINE_A": 0.34, "LINE_B": 0.32, "LINE_C": 0.20, "LINE_D": 0.14},
    "line_share_2026": {"LINE_A": 0.26, "LINE_B": 0.25, "LINE_C": 0.26, "LINE_D": 0.23},
    "depot_load_factor_2027": {"LINE_A": 1.22, "LINE_B": 1.20, "LINE_C": 1.00, "LINE_D": 1.00},
    "dray_contract_factor_2027": 0.88,
}

# Physical loaded 40' HC reefer gross weight (tonnes) for train weighbridge physics
REEFER_LOADED_TONNES = 28.5
LOCK_CUTOFF_HOURS = 24.0


def _day_to_quarter(day_arr):
    """Exact 2026 calendar quarter (0=Q1, 1=Q2, 2=Q3 [Jul 1-Sep 30], 3=Q4)."""
    return np.searchsorted(QUARTER_BOUNDS, day_arr, side="right")


def simulate_world(seed=SEED):
    """Simulate Weserfrucht's 2026 physical operations and build the exact shipped data arrays."""
    rng = np.random.default_rng(seed)

    # --- 1. Build 365-day seasonal profiles ---
    days = np.arange(N_DAYS)
    wave_z02 = 0.65 + 0.30 * np.exp(-0.5 * ((days - 192.0) / 30.0) ** 2)
    wave_z07 = 0.66 + 0.28 * (
        np.exp(-0.5 * ((days - 16.0) / 28.0) ** 2)
        + np.exp(-0.5 * ((days - 350.0) / 28.0) ** 2)
    )
    wave_z13 = 0.90 - 0.32 * np.exp(-0.5 * ((days - 192.0) / 30.0) ** 2) - 0.28 * (
        np.exp(-0.5 * ((days - 16.0) / 28.0) ** 2)
        + np.exp(-0.5 * ((days - 350.0) / 28.0) ** 2)
    )

    dc_caps = np.array([
        [1400, 1400, 1400],  # HAN
        [1120, 1120, 1120],  # OSN
        [1120, 1120, 1120],  # KAS
        [1020, 1020, 1020],  # MAG
    ], dtype=float)

    chamber_opening = np.zeros((4, 3), dtype=int)
    pallet_in = np.zeros((4, 3, N_DAYS), dtype=int)
    pallet_out = np.zeros((4, 3, N_DAYS), dtype=int)
    chamber_stock = np.zeros((4, 3, N_DAYS), dtype=int)
    chamber_util = np.zeros((4, 3, N_DAYS), dtype=float)

    zone_waves = np.vstack([wave_z02, wave_z07, wave_z13])
    dc_phase = np.array([0, 6, -5, 10])
    for d in range(4):
        for z in range(3):
            cap = dc_caps[d, z]
            shifted = np.roll(zone_waves[z], dc_phase[d])
            eps = np.zeros(N_DAYS)
            for t in range(1, N_DAYS):
                eps[t] = 0.78 * eps[t - 1] + rng.normal(0.0, 0.016)
            target_u = np.clip(shifted + eps, 0.54, 0.992)
            if z == 0:
                target_u = np.clip(
                    target_u + 0.036 * np.exp(-0.5 * ((days - (192 + dc_phase[d])) / 24.0) ** 2),
                    0.54, 0.992,
                )
            elif z == 1:
                target_u = np.clip(
                    target_u + 0.032 * (
                        np.exp(-0.5 * ((days - 16.0) / 20.0) ** 2)
                        + np.exp(-0.5 * ((days - 350.0) / 20.0) ** 2)
                    ),
                    0.54, 0.992,
                )
            target_s = np.round(target_u * cap).astype(int)
            chamber_opening[d, z] = int(target_s[0])
            cur = int(target_s[0])
            for t in range(N_DAYS):
                base_flow = int(round(cap * (0.14 + 0.03 * shifted[t])))
                delta = int(target_s[t] - cur)
                in_p = max(10, base_flow + max(delta, 0) + int(rng.integers(-6, 7)))
                out_p = max(10, in_p - delta)
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
                cur = nxt

    dc_total_stock = chamber_stock.sum(axis=1)  # (4, 365)
    dc_total_cap = dc_caps.sum(axis=1)          # (4,)
    dc_total_util = dc_total_stock / dc_total_cap[:, None]

    # Port terminal yard daily physical reefer-rack utilization (3 ports x 365 days)
    port_season = (
        0.70
        + 0.23 * np.exp(-0.5 * ((days - 192.0) / 40.0) ** 2)
        + 0.21 * (
            np.exp(-0.5 * ((days - 16.0) / 36.0) ** 2)
            + np.exp(-0.5 * ((days - 350.0) / 36.0) ** 2)
        )
    )
    port_yard_util = np.zeros((3, N_DAYS))
    for p in range(3):
        noise_p = np.zeros(N_DAYS)
        for t in range(1, N_DAYS):
            noise_p[t] = 0.72 * noise_p[t - 1] + rng.normal(0.0, 0.020)
        port_offset = [0.025, 0.010, -0.015][p]
        port_yard_util[p] = np.clip(port_season + port_offset + noise_p, 0.58, 0.975)

    # --- 2. Simulate 480 Vessel Calls & 24,000 Import Containers ---
    vessel_port = rng.choice(3, size=N_VESSELS, p=PORT_SHARES)
    vessel_day = np.sort(rng.integers(0, N_DAYS, size=N_VESSELS))
    cont_vessel = rng.integers(0, N_VESSELS, size=N_CONTAINERS)
    cont_port = vessel_port[cont_vessel]
    cont_day = vessel_day[cont_vessel]
    cont_quarter = _day_to_quarter(cont_day)
    cont_dc = rng.choice(4, size=N_CONTAINERS, p=DC_SHARES)

    p_z02 = 0.24 + 0.22 * np.exp(-0.5 * ((cont_day - 192.0) / 48.0) ** 2)
    p_z07 = 0.24 + 0.20 * (
        np.exp(-0.5 * ((cont_day - 16.0) / 44.0) ** 2)
        + np.exp(-0.5 * ((cont_day - 350.0) / 44.0) ** 2)
    )
    p_z13 = np.full(N_CONTAINERS, 0.28)
    p_sum = p_z02 + p_z07 + p_z13
    u_z = rng.random(N_CONTAINERS)
    cont_zone = np.where(u_z < p_z02 / p_sum, 0, np.where(u_z < (p_z02 + p_z07) / p_sum, 1, 2))

    line_p26 = np.array([PLAN_2027["line_share_2026"][k] for k in LINES])
    cont_line = rng.choice(4, size=N_CONTAINERS, p=line_p26)
    cont_is_rail = rng.random(N_CONTAINERS) < 0.65

    # --- 3. Forced Causes: vessel_berth (high) and edi_docs (low) ---
    vessel_storm = 0.125 + 0.085 * (
        np.exp(-0.5 * ((vessel_day - 25.0) / 55.0) ** 2)
        + np.exp(-0.5 * ((vessel_day - 335.0) / 55.0) ** 2)
    )
    vessel_delay_each = rng.gamma(shape=2.0, scale=vessel_storm / 2.0) * np.array([1.08, 1.00, 0.86])[vessel_port]
    true_vessel_berth = vessel_delay_each[cont_vessel] * rng.uniform(0.92, 1.08, size=N_CONTAINERS)

    edi_flag = rng.random(N_CONTAINERS) < 0.036
    true_edi_docs = np.where(edi_flag, rng.gamma(shape=4.0, scale=0.245, size=N_CONTAINERS), 0.0)

    # --- 4. STUMP S1: Port Reefer Plug (reefer_plug) vs Inland Chamber Throttling (coldstore_dock) ---
    u_port_c = port_yard_util[cont_port, cont_day]
    port_rate = np.array([0.235, 0.196, 0.161])[cont_port]
    true_reefer_plug = np.maximum(
        0.01,
        port_rate * (0.015 + 0.18 * np.maximum(0.0, u_port_c - 0.72) + 1280.0 * np.maximum(0.0, u_port_c - 0.83) ** 3)
        + rng.normal(0.0, 0.016, size=N_CONTAINERS),
    )

    dc_direct_flag = rng.random(N_CONTAINERS) < 0.14
    true_coldstore_direct = np.where(
        dc_direct_flag, rng.gamma(shape=3.5, scale=0.095, size=N_CONTAINERS), 0.0
    )

    u_ch_c = chamber_util[cont_dc, cont_zone, cont_day]
    chamber_capped = u_ch_c >= 0.95
    pullback_per_box = 0.80 + 1.8 * np.maximum(0.0, u_ch_c - 0.95)
    true_coldstore_pullback = np.where(
        chamber_capped,
        np.maximum(0.20, pullback_per_box + rng.normal(0.0, 0.08, size=N_CONTAINERS)),
        0.0,
    )
    obs_term_yard_hold = true_reefer_plug + true_coldstore_pullback
    obs_dc_dock_wait = true_coldstore_direct

    # --- 5. STUMP S2: Rail Shuttle Handoff (rail_handoff) vs Phytosanitary CHED Holds (phyto_insp) ---
    order_vz = np.lexsort((cont_zone, cont_vessel))
    cont_ched = np.empty(N_CONTAINERS, dtype=int)
    lot_id = 0
    idx = 0
    lot_port, lot_day, lot_zone, lot_size = [], [], [], []
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
        lot_id += 1
        idx = k
    n_lots = lot_id
    lot_port = np.array(lot_port)
    lot_day = np.array(lot_day)
    lot_zone = np.array(lot_zone)
    lot_size = np.array(lot_size)

    lot_bip_prob = np.where(lot_zone == 1, 0.036, 0.047)
    lot_bip = rng.random(n_lots) < lot_bip_prob
    lot_lead_hours = np.where(
        rng.random(n_lots) < 0.66,
        rng.uniform(2.0, 23.4, size=n_lots),
        rng.uniform(24.8, 56.0, size=n_lots),
    )
    lot_post_lock = lot_bip & (lot_lead_hours <= LOCK_CUTOFF_HOURS)

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

    # Direct physical exam hold on sampled box + road-mode CHED sibling customs holds
    # (ONLY rail-mode CHED siblings sit inside TMS RAIL_CAP_ROLL so 100% of rail_handoff is RAIL!)
    base_sampled_hold = np.where(
        cont_bip_sampled, rng.gamma(shape=5.0, scale=0.17, size=N_CONTAINERS), 0.0
    )
    raw_sibling_hold = np.where(
        cont_bip_sibling, rng.gamma(shape=5.0, scale=0.075, size=N_CONTAINERS), 0.0
    )
    true_phyto_direct = base_sampled_hold + np.where(~cont_is_rail, raw_sibling_hold, 0.0)
    true_phyto_sibling_rail = np.where(cont_is_rail, raw_sibling_hold, 0.0)

    n_shuttles = 3 * N_DAYS
    cont_shuttle = cont_port * N_DAYS + cont_day
    shuttle_port = np.repeat(np.arange(3), N_DAYS)
    shuttle_day = np.tile(np.arange(N_DAYS), 3)
    shuttle_quarter = _day_to_quarter(shuttle_day)

    rail_idx = np.where(cont_is_rail)[0]
    planned_on_shuttle = np.bincount(cont_shuttle[rail_idx], minlength=n_shuttles)

    cont_locked_phyto = cont_is_rail & lot_post_lock[cont_ched]
    cont_prelock_phyto = cont_is_rail & lot_bip[cont_ched] & (~lot_post_lock[cont_ched])
    n_locked_phyto_sh = np.bincount(cont_shuttle[cont_locked_phyto], minlength=n_shuttles)
    n_prelock_phyto_sh = np.bincount(cont_shuttle[cont_prelock_phyto], minlength=n_shuttles)

    rail_short_event = rng.random(n_shuttles) < 0.62
    n_rail_short_sh = np.where(rail_short_event, rng.integers(1, 6, size=n_shuttles), 0)
    n_rail_short_sh = np.minimum(n_rail_short_sh, np.maximum(0, planned_on_shuttle - n_locked_phyto_sh))

    rollover_days_per_box = 2.25
    wf_booked_slots_sh = np.maximum(planned_on_shuttle - n_prelock_phyto_sh, n_locked_phyto_sh + n_rail_short_sh)
    wf_actual_loaded_sh = wf_booked_slots_sh - n_locked_phyto_sh - n_rail_short_sh
    wf_standby_rolled_phyto_sh = n_locked_phyto_sh
    wf_standby_rolled_rail_sh = n_rail_short_sh
    wf_standby_rolled_total_sh = wf_standby_rolled_phyto_sh + wf_standby_rolled_rail_sh

    third_party_slots_sh = rng.integers(14, 28, size=n_shuttles)
    train_wagon_count_sh = wf_booked_slots_sh + third_party_slots_sh
    third_party_tonnes_sh = (
        (third_party_slots_sh + n_rail_short_sh) * 24.5
        + rng.normal(0.0, 4.2, size=n_shuttles) * np.sqrt(third_party_slots_sh + n_rail_short_sh)
    )
    wf_loaded_tonnes_sh = wf_actual_loaded_sh * REEFER_LOADED_TONNES + rng.normal(
        0.0, 1.4, size=n_shuttles
    ) * np.sqrt(np.maximum(1, wf_actual_loaded_sh))
    train_gross_tonnes_sh = train_wagon_count_sh * 22.0 + wf_loaded_tonnes_sh + third_party_tonnes_sh

    sh_phyto_bump_days = wf_standby_rolled_phyto_sh * rollover_days_per_box
    sh_rail_short_days = wf_standby_rolled_rail_sh * rollover_days_per_box
    true_rail_base_sh = planned_on_shuttle * rng.uniform(0.015, 0.028, size=n_shuttles)

    # --- 5b. Physical Inland Unload Day (cont_unload_day) BEFORE Empty-Return Stage (S3) ---
    # Every container takes 2 days standard transit by direct truck or 3 days by intermodal rail,
    # plus rounded pre-unload excess delay days (capped at year-end day 364 for 2026 ledger scope).
    base_transit_days = np.where(cont_is_rail, 3, 2)
    pre_unload_excess = np.round(
        obs_term_yard_hold + obs_dc_dock_wait + true_phyto_direct + true_phyto_sibling_rail + true_edi_docs
    ).astype(int)
    cont_unload_day = np.minimum(N_DAYS - 1, cont_day + base_transit_days + pre_unload_excess)

    # --- 6. STUMP S3: Empty Depot Portal Quota Blocking (empty_depot) vs Drayage Carrier ---
    # Indexed strictly on cont_unload_day (physical date container finishes unloading at inland DC
    # and enters the empty-return pool)!
    dc_dray_base = np.array([0.080, 0.071, 0.087, 0.079])[cont_dc]
    dow_mult = np.array([1.14, 0.95, 0.92, 0.96, 1.18, 0.90, 0.95])[cont_unload_day % 7]
    carrier_peak = 0.008 + 13.85 * np.exp(-0.5 * ((cont_unload_day - 193.0) / 14.8) ** 2)
    true_dray_carrier = np.maximum(
        0.01,
        dc_dray_base * dow_mult * carrier_peak + rng.normal(0.0, 0.014, size=N_CONTAINERS),
    )

    phys_turnaway_flag = rng.random(N_CONTAINERS) < 0.036
    true_depot_physical = np.where(
        phys_turnaway_flag, rng.gamma(shape=4.0, scale=0.22, size=N_CONTAINERS), 0.0
    )

    depot_quota_closed = np.zeros((3, 4, N_DAYS), dtype=bool)
    for p in range(3):
        for l in range(4):
            if l in (0, 1):
                prob_q = 0.005 + 0.92 * np.exp(-0.5 * ((days - 193.0) / 22.0) ** 2)
                state = 0
                for t in range(N_DAYS):
                    if state > 0:
                        depot_quota_closed[p, l, t] = True
                        state -= 1
                    elif rng.random() < prob_q[t] * 0.85:
                        state = int(rng.integers(3, 6))
                        depot_quota_closed[p, l, t] = True
            elif l == 2:
                depot_quota_closed[p, l] = rng.random(N_DAYS) < 0.008
            else:
                depot_quota_closed[p, l] = False

    cont_quota_closed = depot_quota_closed[cont_port, cont_line, cont_unload_day]
    true_depot_portal_block = np.where(
        cont_quota_closed,
        np.maximum(0.18, 0.44 + rng.normal(0.0, 0.07, size=N_CONTAINERS)),
        0.0,
    )
    obs_dray_empty_hold = true_dray_carrier + true_depot_portal_block
    obs_depot_turnaway = true_depot_physical

    # Online Depot Portal Rejection Log (NO container_id! Multi-day retry multiplicity ~4.20x!)
    RETRY_RATE = 4.20
    portal_confirmed = np.zeros((3, 4, N_DAYS), dtype=int)
    portal_rejected = np.zeros((3, 4, N_DAYS), dtype=int)
    daily_empty_unloads = np.zeros((3, 4, N_DAYS), dtype=int)
    daily_empty_gateins = np.zeros((3, 4, N_DAYS), dtype=int)
    for p in range(3):
        for l in range(4):
            m = (cont_port == p) & (cont_line == l)
            u_days = cont_unload_day[m]
            ret_lag = np.maximum(0, np.round(obs_dray_empty_hold[m] + obs_depot_turnaway[m]).astype(int))
            g_days = np.minimum(N_DAYS - 1, u_days + ret_lag)
            daily_empty_unloads[p, l] = np.bincount(u_days, minlength=N_DAYS)
            daily_empty_gateins[p, l] = np.bincount(g_days, minlength=N_DAYS)
            portal_confirmed[p, l] = daily_empty_gateins[p, l]
            blocked_pool_t = np.zeros(N_DAYS, dtype=float)
            b_idx = np.where(m & cont_quota_closed)[0]
            for bi in b_idx:
                d0 = cont_unload_day[bi]
                dur = true_depot_portal_block[bi]
                n_whole = int(np.floor(dur))
                frac = dur - n_whole
                for k in range(n_whole):
                    if d0 + k < N_DAYS:
                        blocked_pool_t[d0 + k] += 1.0
                if d0 + n_whole < N_DAYS:
                    blocked_pool_t[d0 + n_whole] += frac
            lam_rej = np.maximum(0.0, blocked_pool_t * RETRY_RATE)
            raw_p = rng.poisson(lam_rej)
            portal_rejected[p, l] = np.where(
                depot_quota_closed[p, l] & (blocked_pool_t > 0), np.maximum(1, raw_p), raw_p
            )

    dispute_closeout = {
        "vessel_berth": float(true_vessel_berth.sum() * 0.98),
        "edi_docs": float(true_edi_docs.sum() * 0.96),
        "reefer_plug": float(obs_term_yard_hold.sum() * 0.97),
        "coldstore_dock": float(obs_dc_dock_wait.sum() * 0.95),
        "rail_handoff": float(
            (sh_phyto_bump_days.sum() + sh_rail_short_days.sum() + true_rail_base_sh.sum() + true_phyto_sibling_rail.sum())
            * 0.94
        ),
        "phyto_insp": float(true_phyto_direct.sum() * 0.97),
        "drayage_carrier": float(obs_dray_empty_hold.sum() * 0.96),
        "empty_depot": float(obs_depot_turnaway.sum() * 0.95),
    }

    world = {
        "cont_vessel": cont_vessel,
        "cont_port": cont_port,
        "cont_day": cont_day,
        "cont_unload_day": cont_unload_day,
        "cont_quarter": cont_quarter,
        "cont_dc": cont_dc,
        "cont_zone": cont_zone,
        "cont_line": cont_line,
        "cont_is_rail": cont_is_rail,
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
        "shuttle_port": shuttle_port,
        "shuttle_day": shuttle_day,
        "shuttle_quarter": shuttle_quarter,
        "planned_on_shuttle": planned_on_shuttle,
        "wf_booked_slots_sh": wf_booked_slots_sh,
        "wf_actual_loaded_sh": wf_actual_loaded_sh,
        "wf_standby_rolled_total_sh": wf_standby_rolled_total_sh,
        "obs_rail_roll_days_sh": wf_standby_rolled_total_sh * rollover_days_per_box,
        "train_wagon_count_sh": train_wagon_count_sh,
        "train_gross_tonnes_sh": train_gross_tonnes_sh,
        "obs_rail_base_sh": true_rail_base_sh,
        "portal_confirmed": portal_confirmed,
        "portal_rejected": portal_rejected,
        "daily_empty_unloads": daily_empty_unloads,
        "daily_empty_gateins": daily_empty_gateins,
        "dispute_closeout": dispute_closeout,
        "_truth": {
            "vessel_berth_c": true_vessel_berth,
            "edi_docs_c": true_edi_docs,
            "reefer_plug_c": true_reefer_plug,
            "coldstore_direct_c": true_coldstore_direct,
            "coldstore_pullback_c": true_coldstore_pullback,
            "phyto_direct_c": true_phyto_direct,
            "phyto_sibling_rail_c": true_phyto_sibling_rail,
            "sh_phyto_bump_days": sh_phyto_bump_days,
            "sh_rail_short_days": sh_rail_short_days,
            "rail_base_sh": true_rail_base_sh,
            "dray_carrier_c": true_dray_carrier,
            "depot_physical_c": true_depot_physical,
            "depot_portal_block_c": true_depot_portal_block,
            "chamber_capped": chamber_capped,
            "n_locked_phyto_sh": n_locked_phyto_sh,
            "cont_quota_closed": cont_quota_closed,
        },
    }
    return world


def _reconstruct_chamber_util(w):
    """Exact stock-flow accounting per (DC, thermal chamber, day) from shipped pallet movements."""
    stock = np.zeros((4, 3, N_DAYS), dtype=float)
    for d in range(4):
        for z in range(3):
            cum = np.cumsum(w["pallet_in"][d, z] - w["pallet_out"][d, z])
            stock[d, z] = w["chamber_opening"][d, z] + cum
    assert np.allclose(stock.sum(axis=1), w["dc_total_stock"]), "Stock-flow conservation failed!"
    return stock / w["dc_caps"][:, :, None]


def _project_2027(w, attr_2026, opts=None):
    """Carry 2026 attributed container-days onto the 2027 Import Schedule Plan using ONE uniform,
    leak-free cause-level scaling rule per cause (verbatim in Charter RC-2027 Annex C and
    import_plan_2027.csv).
    """
    opts = opts or {}
    m_s1 = opts.get("mult_s1", 1.0)
    m_s2 = opts.get("mult_s2", 1.0)
    m_s3 = opts.get("mult_s3", 1.0)
    m_base = opts.get("mult_base", 1.0)

    port_g = np.array([PLAN_2027["vol_growth_port"][p] for p in PORTS])
    plug_f = np.array([PLAN_2027["plug_capacity_factor_2027"][p] for p in PORTS])
    dc_zone_f = np.array([PLAN_2027["dc_zone_load_factor_2027"][z] for z in ZONES])
    bip_port_f = np.array([PLAN_2027["bip_sampling_factor_2027"][p] for p in PORTS])
    rail_f = PLAN_2027["rail_fleet_factor_2027"]
    line_ratio = np.array([
        PLAN_2027["line_share_2027"][k] / PLAN_2027["line_share_2026"][k] for k in LINES
    ])
    depot_load_f = np.array([PLAN_2027["depot_load_factor_2027"][k] for k in LINES])
    dray_f = PLAN_2027["dray_contract_factor_2027"]

    p_vol = port_g[w["cont_port"]]
    sh_p_vol = port_g[w["shuttle_port"]]

    # 1. vessel_berth & edi_docs: uniform port volume growth
    vb_27_c = attr_2026["vessel_berth_c"] * p_vol * m_base
    ed_27_c = attr_2026["edi_docs_c"] * p_vol * m_base

    # 2. coldstore_dock: UNIFORM dc_zone_load_factor_2027[zone] on ALL attributed coldstore_dock days!
    cs_zone_mult = dc_zone_f[w["cont_zone"]]
    cs_27_c = (
        attr_2026["coldstore_direct_c"] * cs_zone_mult * m_base
        + attr_2026["coldstore_pullback_c"] * cs_zone_mult * m_s1
    )

    # 3. reefer_plug: UNIFORM vol_growth_port[port] * plug_capacity_factor_2027[port]
    rp_27_c = attr_2026["reefer_plug_c"] * p_vol * plug_f[w["cont_port"]] * m_base

    # 4. phyto_insp: UNIFORM vol_growth_port[port] * bip_sampling_factor_2027[port] across ALL
    #    container-level and shuttle-level phyto_insp container-days!
    ph_c_mult = p_vol * bip_port_f[w["cont_port"]]
    ph_sh_mult = sh_p_vol * bip_port_f[w["shuttle_port"]]
    ph_dir_27_c = (attr_2026["phyto_direct_c"] + attr_2026["phyto_sibling_rail_c"]) * ph_c_mult * m_base
    ph_bump_27_sh = attr_2026["sh_phyto_bump_days"] * ph_sh_mult * m_s2

    # 5. rail_handoff: UNIFORM vol_growth_port[port] * rail_fleet_factor_2027
    rh_27_sh = (attr_2026["sh_rail_short_days"] + attr_2026["rail_base_sh"]) * sh_p_vol * rail_f * m_base

    # 6. empty_depot: UNIFORM vol_growth_port[port] * (line_share_2027/line_share_2026) * depot_load_factor_2027[line]
    #    on ALL attributed empty_depot days (both physical turn-aways and portal blocks)!
    edep_mult = p_vol * line_ratio[w["cont_line"]] * depot_load_f[w["cont_line"]]
    edep_27_c = (
        attr_2026["depot_physical_c"] * edep_mult * m_base
        + attr_2026["depot_portal_block_c"] * edep_mult * m_s3
    )

    # 7. drayage_carrier: UNIFORM vol_growth_port[port] * dray_contract_factor_2027
    dray_27_c = attr_2026["dray_carrier_c"] * p_vol * dray_f * m_base

    out = {
        "vessel_berth": float(vb_27_c.sum()),
        "edi_docs": float(ed_27_c.sum()),
        "coldstore_dock": float(cs_27_c.sum()),
        "reefer_plug": float(rp_27_c.sum()),
        "phyto_insp": float(ph_dir_27_c.sum() + ph_bump_27_sh.sum()),
        "rail_handoff": float(rh_27_sh.sum()),
        "empty_depot": float(edep_27_c.sum()),
        "drayage_carrier": float(dray_27_c.sum()),
    }

    total_27 = sum(out.values())
    remed_members = [m for m in MEMBERS if out[m] >= LINE_THRESHOLD]
    remed_days = sum(out[m] for m in remed_members)
    cost_eur_m = sum(out[m] * TARIFF_EUR[m] for m in MEMBERS) / 1e6
    avoidable_eur_m = sum(out[m] * TARIFF_EUR[m] for m in remed_members) / 1e6

    c_all_27 = vb_27_c + ed_27_c + cs_27_c + rp_27_c + ph_dir_27_c + edep_27_c + dray_27_c
    sh_all_27 = ph_bump_27_sh + rh_27_sh

    bhv_27 = float(c_all_27[w["cont_port"] == 0].sum() + sh_all_27[w["shuttle_port"] == 0].sum())
    ham_27 = float(c_all_27[w["cont_port"] == 1].sum() + sh_all_27[w["shuttle_port"] == 1].sum())
    q3_27 = float(c_all_27[w["cont_quarter"] == 2].sum() + sh_all_27[w["shuttle_quarter"] == 2].sum())

    return {
        "members": out,
        "total_2027": float(total_27),
        "remed_days": float(remed_days),
        "cost_eur_m": float(cost_eur_m),
        "avoidable_eur_m": float(avoidable_eur_m),
        "bhv_2027": bhv_27,
        "ham_2027": ham_27,
        "q3_2027": q3_27,
    }


def estimate_s1(w, mode="golden", cap_thresh=0.95, stat="mean", min_twins=1):
    """Estimate S1 split of obs_term_yard_hold between true reefer_plug and coldstore_dock pull-back."""
    obs_yard = w["obs_term_yard_hold"]
    obs_dc = w["obs_dc_dock_wait"]
    n = len(obs_yard)

    if mode in ("hurried", "direct", "hedge"):
        frac = 0.0 if mode != "hedge" else 0.12
        pb = obs_yard * frac
        return obs_yard - pb, obs_dc, pb, {"twin_gap_h": 0.0 if mode != "hedge" else 4.0}

    if mode == "calibrated":
        return obs_yard.copy(), obs_dc.copy(), np.zeros(n), {"twin_gap_h": 0.0}

    if mode == "rigorous":
        u_p = w["port_yard_util"][w["cont_port"], w["cont_day"]]
        u_dc_tot = w["dc_total_util"][w["cont_dc"], w["cont_day"]]
        X = np.column_stack([np.ones(n), u_p, u_dc_tot])
        beta, _, _, _ = np.linalg.lstsq(X, obs_yard, rcond=None)
        b_dc = max(0.0, float(beta[2]))
        pb = np.clip(b_dc * np.maximum(0.0, u_dc_tot - np.percentile(u_dc_tot, 10)), 0.0, obs_yard * 0.5)
        return obs_yard - pb, obs_dc, pb, {"twin_gap_h": float(pb.mean() * 24.0)}

    if mode == "cutoff_total_dc":
        u_dc_tot = w["dc_total_util"][w["cont_dc"], w["cont_day"]]
        hi = u_dc_tot >= cap_thresh
        base_r = obs_yard[~hi].mean() if np.any(~hi) else obs_yard.mean()
        pb = np.where(hi, np.maximum(0.0, obs_yard - base_r), 0.0)
        return obs_yard - pb, obs_dc, pb, {"twin_gap_h": float(pb[hi].mean() * 24.0) if np.any(hi) else 0.0}

    ch_util = _reconstruct_chamber_util(w)
    u_ch = ch_util[w["cont_dc"], w["cont_zone"], w["cont_day"]]

    if mode in ("over", "generous"):
        tight = u_ch >= (0.88 if mode == "over" else 0.90)
        pb = np.where(tight, obs_yard, 0.0)
        return obs_yard - pb, obs_dc, pb, {"twin_gap_h": float(pb[tight].mean() * 24.0)}

    if mode == "cutoff_chamber_raw":
        capped = u_ch >= cap_thresh
        pb = np.where(capped, obs_yard, 0.0)
        return obs_yard - pb, obs_dc, pb, {"twin_gap_h": float(pb[capped].mean() * 24.0) if np.any(capped) else 0.0}

    # GOLDEN & VARIANT FAMILY: same-vessel-day unsaturated-chamber twin comparison!
    capped = u_ch >= cap_thresh
    uncapped = u_ch < min(0.92, cap_thresh - 0.02)

    if stat == "port_day_fe":
        key = w["cont_port"] * N_DAYS + w["cont_day"]
        max_k = 3 * N_DAYS
    elif stat == "port_week_fe":
        key = w["cont_port"] * 53 + (w["cont_day"] // 7)
        max_k = 3 * 53
    elif stat == "ols_yard":
        u_p = w["port_yard_util"][w["cont_port"], w["cont_day"]]
        X = np.column_stack([
            (w["cont_port"] == 0).astype(float),
            (w["cont_port"] == 1).astype(float),
            (w["cont_port"] == 2).astype(float),
            np.maximum(0.0, u_p - 0.72) * (w["cont_port"] == 0),
            np.maximum(0.0, u_p - 0.72) * (w["cont_port"] == 1),
            np.maximum(0.0, u_p - 0.72) * (w["cont_port"] == 2),
            (np.maximum(0.0, u_p - 0.83) ** 3) * (w["cont_port"] == 0),
            (np.maximum(0.0, u_p - 0.83) ** 3) * (w["cont_port"] == 1),
            (np.maximum(0.0, u_p - 0.83) ** 3) * (w["cont_port"] == 2),
        ])
        beta, _, _, _ = np.linalg.lstsq(X[uncapped], obs_yard[uncapped], rcond=None)
        base_pred = np.maximum(0.0, X @ beta)
        pb = np.where(capped, np.maximum(0.0, obs_yard - base_pred), 0.0)
        gap_h = float((obs_yard[capped] - base_pred[capped]).mean() * 24.0)
        return obs_yard - pb, obs_dc, pb, {"twin_gap_h": gap_h}
    else:
        key = w["cont_vessel"]
        max_k = N_VESSELS

    global_port_base = np.array([obs_yard[uncapped & (w["cont_port"] == p)].mean() for p in range(3)])
    base_stratum = np.full(max_k, np.nan)
    if stat == "median":
        for k in range(max_k):
            vals = obs_yard[uncapped & (key == k)]
            if len(vals) >= min_twins:
                base_stratum[k] = float(np.median(vals))
    elif stat == "trimmed":
        for k in range(max_k):
            vals = np.sort(obs_yard[uncapped & (key == k)])
            if len(vals) >= max(5, min_twins):
                t = max(1, len(vals) // 10)
                base_stratum[k] = float(vals[t:-t].mean())
            elif len(vals) >= min_twins:
                base_stratum[k] = float(vals.mean())
    else:
        cnt = np.bincount(key[uncapped], minlength=max_k)
        sm = np.bincount(key[uncapped], weights=obs_yard[uncapped], minlength=max_k)
        valid = cnt >= min_twins
        base_stratum[valid] = sm[valid] / cnt[valid]

    base_c = base_stratum[key]
    miss = np.isnan(base_c)
    if np.any(miss):
        base_c[miss] = global_port_base[w["cont_port"][miss]]

    pb = np.where(capped, np.maximum(0.0, obs_yard - base_c), 0.0)
    gap_h = float((obs_yard[capped] - base_c[capped]).mean() * 24.0)
    return obs_yard - pb, obs_dc, pb, {"twin_gap_h": gap_h}


def estimate_s2(w, mode="golden", lock_h=24.0, weight_est="slot_mass"):
    """Estimate S2 split of rail standby rollovers between rail_handoff and phyto_insp."""
    obs_ph_dir = w["obs_phyto_hold_direct"]
    obs_ph_sib = w["obs_phyto_sibling_tms_rail"]  # strictly rail-mode CHED siblings!
    rolled_sh = w["wf_standby_rolled_total_sh"].astype(float)
    rail_base = w["obs_rail_base_sh"]
    rollover_days = float(w["obs_rail_roll_days_sh"].sum() / max(rolled_sh.sum(), 1.0))
    n_sh = len(rolled_sh)

    lot_bip = w["lot_bip"]
    lot_lead = w["lot_lead_hours"]
    cont_ched = w["cont_ched"]
    is_rail = w["cont_is_rail"]
    sh_id = w["cont_shuttle"]

    if mode in ("hurried", "direct", "calibrated", "hedge"):
        frac = 0.15 if mode == "hedge" else 0.0
        sib_by_sh = np.bincount(sh_id, weights=obs_ph_sib, minlength=n_sh)
        ph_sib = obs_ph_sib * frac
        ph_bump = rolled_sh * rollover_days * frac
        rh_days = rolled_sh * rollover_days * (1.0 - frac) + sib_by_sh * (1.0 - frac)
        return obs_ph_dir, ph_sib, ph_bump, rh_days, rail_base, {"tonnes_per_slot": 0.0}

    if mode == "rigorous":
        ph_sib = obs_ph_sib.copy()
        ph_bump = np.zeros(n_sh)
        rh_days = rolled_sh * rollover_days
        return obs_ph_dir, ph_sib, ph_bump, rh_days, rail_base, {"tonnes_per_slot": 0.0}

    if mode in ("over", "generous"):
        any_bip_c = is_rail & lot_bip[cont_ched]
        any_bip_sh = np.bincount(sh_id[any_bip_c], minlength=n_sh) > 0
        if mode == "generous":
            ph_bump = np.where(any_bip_sh, rolled_sh * rollover_days, rolled_sh * rollover_days * 0.40)
        else:
            ph_bump = np.where(any_bip_sh, rolled_sh * rollover_days, 0.0)
        rh_days = np.maximum(0.0, rolled_sh * rollover_days - ph_bump)
        return obs_ph_dir, obs_ph_sib.copy(), ph_bump, rh_days, rail_base, {"tonnes_per_slot": -13.5}

    if mode == "cutoff_any_bip":
        any_bip_c = is_rail & lot_bip[cont_ched]
        cnt_bip_sh = np.bincount(sh_id[any_bip_c], minlength=n_sh)
        flag_sh = cnt_bip_sh >= lock_h
        ph_bump = np.where(flag_sh, rolled_sh * rollover_days, 0.0)
        rh_days = np.maximum(0.0, rolled_sh * rollover_days - ph_bump)
        return obs_ph_dir, obs_ph_sib.copy(), ph_bump, rh_days, rail_base, {"tonnes_per_slot": -12.0}

    # GOLDEN & VARIANT FAMILY
    if lock_h == "empirical":
        shortfall = (w["wf_booked_slots_sh"] - w["wf_actual_loaded_sh"]).astype(float)
        best_c, best_r2 = 24.0, -1.0
        for cand in (12.0, 18.0, 24.0, 30.0, 36.0):
            lk = is_rail & lot_bip[cont_ched] & (lot_lead[cont_ched] <= cand)
            x = np.bincount(sh_id[lk], minlength=n_sh).astype(float)
            if x.std() > 0:
                r = np.corrcoef(x, shortfall)[0, 1]
                if r * r > best_r2:
                    best_r2, best_c = r * r, cand
        cut = best_c
    else:
        cut = float(lock_h)

    locked_c = is_rail & lot_bip[cont_ched] & (lot_lead[cont_ched] <= cut)
    n_locked_sh = np.bincount(sh_id[locked_c], minlength=n_sh).astype(float)

    non_phyto_short = np.maximum(0.0, (w["wf_booked_slots_sh"] - w["wf_actual_loaded_sh"]) - n_locked_sh)
    Xw = np.column_stack([
        np.ones(n_sh),
        w["train_wagon_count_sh"].astype(float),
        w["wf_booked_slots_sh"].astype(float),
        n_locked_sh,
        non_phyto_short,
    ])
    bw, _, _, _ = np.linalg.lstsq(Xw, w["train_gross_tonnes_sh"], rcond=None)
    tonnes_per_slot = float(bw[3])

    if weight_est == "mass_only":
        scale = np.clip(-tonnes_per_slot / REEFER_LOADED_TONNES, 0.5, 1.15)
        locked_bump_boxes = np.minimum(rolled_sh, n_locked_sh * scale)
    elif weight_est == "slot_ols":
        Xs = np.column_stack([np.ones(n_sh), n_locked_sh])
        bs, _, _, _ = np.linalg.lstsq(Xs, rolled_sh, rcond=None)
        slope = np.clip(float(bs[1]), 0.5, 1.15)
        locked_bump_boxes = np.minimum(rolled_sh, n_locked_sh * slope)
    elif weight_est == "corridor_ols":
        locked_bump_boxes = np.zeros(n_sh)
        for p in range(3):
            mp = w["shuttle_port"] == p
            Xs = np.column_stack([np.ones(mp.sum()), n_locked_sh[mp]])
            bs, _, _, _ = np.linalg.lstsq(Xs, rolled_sh[mp], rcond=None)
            slope = np.clip(float(bs[1]), 0.5, 1.15)
            locked_bump_boxes[mp] = np.minimum(rolled_sh[mp], n_locked_sh[mp] * slope)
    elif weight_est == "huber":
        Xs = np.column_stack([np.ones(n_sh), n_locked_sh])
        bs, _, _, _ = np.linalg.lstsq(Xs, rolled_sh, rcond=None)
        for _ in range(6):
            res = rolled_sh - Xs @ bs
            s = np.median(np.abs(res)) * 1.4826 + 1e-6
            wt = np.where(np.abs(res) <= 1.345 * s, 1.0, 1.345 * s / np.abs(res))
            bs, _, _, _ = np.linalg.lstsq(Xs * np.sqrt(wt)[:, None], rolled_sh * np.sqrt(wt), rcond=None)
        slope = np.clip(float(bs[1]), 0.5, 1.15)
        locked_bump_boxes = np.minimum(rolled_sh, n_locked_sh * slope)
    else:
        locked_bump_boxes = np.minimum(rolled_sh, n_locked_sh)

    ph_bump = locked_bump_boxes * rollover_days
    rh_days = np.maximum(0.0, (rolled_sh - locked_bump_boxes) * rollover_days)
    return obs_ph_dir, obs_ph_sib.copy(), ph_bump, rh_days, rail_base, {"tonnes_per_slot": tonnes_per_slot}


def estimate_s3(w, mode="golden", rej_cut=1, stat="dc_day"):
    """Estimate S3 split of obs_dray_empty_hold between drayage_carrier and empty_depot,
    indexed strictly on cont_unload_day (physical inland DC unload completion date).
    """
    obs_dray = w["obs_dray_empty_hold"]
    obs_phys = w["obs_depot_turnaway"]
    rej_grid = w["portal_rejected"]
    u_day = w["cont_unload_day"]
    n = len(obs_dray)

    if mode in ("hurried", "direct", "rigorous", "calibrated", "hedge"):
        frac = 0.12 if mode == "hedge" else 0.0
        blk = obs_dray * frac
        return obs_dray - blk, obs_phys, blk, {"line_gap_h": 0.0 if mode != "hedge" else 3.5}

    rej_c = rej_grid[w["cont_port"], w["cont_line"], u_day]

    if mode in ("over", "generous"):
        blk = np.zeros(n)
        for p in range(3):
            for l in range(4):
                m = (w["cont_port"] == p) & (w["cont_line"] == l)
                if not np.any(m):
                    continue
                raw_pl = float(rej_grid[p, l].sum())
                tot_pl = float(obs_dray[m].sum())
                cap_sh = 0.84 if mode == "over" else 0.78
                share = min(cap_sh, raw_pl / max(tot_pl, 1.0))
                blk[m] = obs_dray[m] * share
        closed_win = rej_c > 0
        return obs_dray - blk, obs_phys, blk, {"line_gap_h": float(blk[closed_win].mean() * 24.0) if np.any(closed_win) else 0.0}

    if mode == "cutoff_rej_raw":
        hi = rej_c >= rej_cut
        blk = np.where(hi, obs_dray, 0.0)
        return obs_dray - blk, obs_phys, blk, {"line_gap_h": float(blk[hi].mean() * 24.0) if np.any(hi) else 0.0}

    if mode == "cutoff_reweight":
        port_day_rej = rej_grid.sum(axis=1)[w["cont_port"], u_day]
        keep = port_day_rej < rej_cut
        dc_mean = np.array([obs_dray[keep & (w["cont_dc"] == d)].mean() for d in range(4)])
        base_c = dc_mean[w["cont_dc"]]
        blk = np.where(~keep, np.maximum(0.0, obs_dray - base_c), 0.0)
        return obs_dray - blk, obs_phys, blk, {"line_gap_h": float(blk[~keep].mean() * 24.0) if np.any(~keep) else 0.0}

    if mode == "cutoff_reweight_box":
        keep = rej_c < rej_cut
        dc_mean = np.array([obs_dray[keep & (w["cont_dc"] == d)].mean() for d in range(4)])
        base_c = dc_mean[w["cont_dc"]]
        blk = np.where(~keep, np.maximum(0.0, obs_dray - base_c), 0.0)
        return obs_dray - blk, obs_phys, blk, {"line_gap_h": float(blk[~keep].mean() * 24.0) if np.any(~keep) else 0.0}

    # GOLDEN & VARIANT FAMILY: exact same-DC, same-unload-day open-quota shipping-line contrast!
    closed = rej_c >= rej_cut
    open_q = rej_c == 0

    if stat == "dc_fortnight":
        key = w["cont_dc"] * 27 + (u_day // 14)
        max_k = 4 * 27
    elif stat == "dc_week":
        key = w["cont_dc"] * 53 + (u_day // 7)
        max_k = 4 * 53
    elif stat == "ols_line":
        t_rad = 2.0 * np.pi * u_day / 365.0
        cols = [(w["cont_dc"] == d).astype(float) for d in range(4)]
        cols += [((u_day % 7) == wd).astype(float) for wd in range(1, 7)]
        for h in (1, 2, 3, 4):
            cols += [np.sin(h * t_rad), np.cos(h * t_rad)]
        X = np.column_stack(cols)
        beta, _, _, _ = np.linalg.lstsq(X[open_q], obs_dray[open_q], rcond=None)
        base_c = np.maximum(0.0, X @ beta)
        blk = np.where(closed, np.maximum(0.0, obs_dray - base_c), 0.0)
        gap_h = float((obs_dray[closed] - base_c[closed]).mean() * 24.0)
        retry_mult = float(rej_grid.sum() / max(blk.sum(), 1.0))
        return obs_dray - blk, obs_phys, blk, {"line_gap_h": gap_h, "retry_mult": retry_mult}
    elif stat == "stock_flow":
        key = w["cont_dc"] * 74 + (u_day // 5)
        max_k = 4 * 74
    else:
        key = w["cont_dc"] * N_DAYS + u_day
        max_k = 4 * N_DAYS

    dc_global = np.array([obs_dray[open_q & (w["cont_dc"] == d)].mean() for d in range(4)])
    base_stratum = np.full(max_k, np.nan)
    if stat == "median_dc_week":
        key = w["cont_dc"] * 53 + (u_day // 7)
        max_k = 4 * 53
        base_stratum = np.full(max_k, np.nan)
        for k in range(max_k):
            vals = obs_dray[open_q & (key == k)]
            if len(vals) >= 3:
                base_stratum[k] = float(np.median(vals))
    else:
        cnt = np.bincount(key[open_q], minlength=max_k)
        sm = np.bincount(key[open_q], weights=obs_dray[open_q], minlength=max_k)
        valid = cnt >= 1
        base_stratum[valid] = sm[valid] / cnt[valid]

    base_c = base_stratum[key]
    miss = np.isnan(base_c)
    if np.any(miss):
        base_c[miss] = dc_global[w["cont_dc"][miss]]

    blk = np.where(closed, np.maximum(0.0, obs_dray - base_c), 0.0)
    gap_h = float((obs_dray[closed] - base_c[closed]).mean() * 24.0)
    retry_mult = float(rej_grid.sum() / max(blk.sum(), 1.0))
    return obs_dray - blk, obs_phys, blk, {"line_gap_h": gap_h, "retry_mult": retry_mult}


def evaluate_route(w, s1_kw, s2_kw, s3_kw, proj_opts=None):
    """Run S1, S2, S3 estimators on shipped arrays and project onto 2027."""
    rp_c, cs_dir_c, cs_pb_c, d1 = estimate_s1(w, **s1_kw)
    ph_dir_c, ph_sib_c, ph_bump_sh, rh_sh, rh_base_sh, d2 = estimate_s2(w, **s2_kw)
    dr_c, ed_phys_c, ed_blk_c, d3 = estimate_s3(w, **s3_kw)

    attr_26 = {
        "vessel_berth_c": w["obs_vessel_berth"],
        "edi_docs_c": w["obs_edi_docs"],
        "reefer_plug_c": rp_c,
        "coldstore_direct_c": cs_dir_c,
        "coldstore_pullback_c": cs_pb_c,
        "phyto_direct_c": ph_dir_c,
        "phyto_sibling_rail_c": ph_sib_c,
        "sh_phyto_bump_days": ph_bump_sh,
        "sh_rail_short_days": rh_sh,
        "rail_base_sh": rh_base_sh,
        "dray_carrier_c": dr_c,
        "depot_physical_c": ed_phys_c,
        "depot_portal_block_c": ed_blk_c,
    }
    res27 = _project_2027(w, attr_26, opts=proj_opts)
    contrast_cdays_26 = float(cs_pb_c.sum() + ph_bump_sh.sum() + ed_blk_c.sum())
    res27["diag"] = {
        "twin_gap_h": d1["twin_gap_h"],
        "tonnes_per_slot": d2["tonnes_per_slot"],
        "line_gap_h": d3["line_gap_h"],
        "retry_mult": d3.get("retry_mult", 0.0),
        "contrast_cdays_26": contrast_cdays_26,
        "cs_pb_26": float(cs_pb_c.sum()),
        "ph_bump_26": float(ph_bump_sh.sum()),
        "ed_blk_26": float(ed_blk_c.sum()),
    }
    return res27


def evaluate_truth(w):
    """Exact 2027 truth from hidden world arrays (for corelib truth verification ONLY)."""
    tr = w["_truth"]
    attr_26 = {
        "vessel_berth_c": tr["vessel_berth_c"],
        "edi_docs_c": tr["edi_docs_c"],
        "reefer_plug_c": tr["reefer_plug_c"],
        "coldstore_direct_c": tr["coldstore_direct_c"],
        "coldstore_pullback_c": tr["coldstore_pullback_c"],
        "phyto_direct_c": tr["phyto_direct_c"],
        "phyto_sibling_rail_c": tr["phyto_sibling_rail_c"],
        "sh_phyto_bump_days": tr["sh_phyto_bump_days"],
        "sh_rail_short_days": tr["sh_rail_short_days"],
        "rail_base_sh": tr["rail_base_sh"],
        "dray_carrier_c": tr["dray_carrier_c"],
        "depot_physical_c": tr["depot_physical_c"],
        "depot_portal_block_c": tr["depot_portal_block_c"],
    }
    res = _project_2027(w, attr_26)
    res["contrast_cdays_26"] = float(
        tr["coldstore_pullback_c"].sum()
        + tr["sh_phyto_bump_days"].sum()
        + tr["depot_portal_block_c"].sum()
    )
    res["twin_gap_h"] = float(tr["coldstore_pullback_c"][tr["chamber_capped"]].mean() * 24.0)
    res["line_gap_h"] = float(tr["depot_portal_block_c"][tr["cont_quota_closed"]].mean() * 24.0)
    res["tonnes_per_slot"] = -REEFER_LOADED_TONNES
    res["hist_2026"] = {
        "vessel_berth": float(tr["vessel_berth_c"].sum()),
        "edi_docs": float(tr["edi_docs_c"].sum()),
        "coldstore_dock": float(tr["coldstore_direct_c"].sum() + tr["coldstore_pullback_c"].sum()),
        "reefer_plug": float(tr["reefer_plug_c"].sum()),
        "phyto_insp": float(tr["phyto_direct_c"].sum() + tr["phyto_sibling_rail_c"].sum() + tr["sh_phyto_bump_days"].sum()),
        "rail_handoff": float(tr["sh_rail_short_days"].sum() + tr["rail_base_sh"].sum()),
        "empty_depot": float(tr["depot_physical_c"].sum() + tr["depot_portal_block_c"].sum()),
        "drayage_carrier": float(tr["dray_carrier_c"].sum()),
    }
    return res


def build_spec(seed=SEED):
    w = simulate_world(seed)
    truth_res = evaluate_truth(w)

    G1 = {"mode": "golden", "cap_thresh": 0.95, "stat": "mean"}
    G2 = {"mode": "golden", "lock_h": "empirical", "weight_est": "slot_mass"}
    G3 = {"mode": "golden", "rej_cut": 1, "stat": "dc_day"}
    H1 = {"mode": "hurried"}
    H2 = {"mode": "hurried"}
    H3 = {"mode": "hurried"}

    gold_res = evaluate_route(w, G1, G2, G3)

    # 22 genuinely distinct defensible implementation variants across all 3 stumps!
    variant_specs = [
        ({"mode": "golden", "cap_thresh": 0.95, "stat": "median"}, G2, G3),
        ({"mode": "golden", "cap_thresh": 0.95, "stat": "trimmed"}, G2, G3),
        ({"mode": "golden", "cap_thresh": 0.95, "stat": "port_day_fe"}, G2, G3),
        ({"mode": "golden", "cap_thresh": 0.95, "stat": "port_week_fe"}, G2, G3),
        ({"mode": "golden", "cap_thresh": 0.95, "stat": "ols_yard"}, G2, G3),
        ({"mode": "golden", "cap_thresh": 0.945, "stat": "mean"}, G2, G3),
        ({"mode": "golden", "cap_thresh": 0.955, "stat": "mean"}, G2, G3),
        (G1, {"mode": "golden", "lock_h": 24.0, "weight_est": "slot_mass"}, G3),
        (G1, {"mode": "golden", "lock_h": 22.0, "weight_est": "slot_mass"}, G3),
        (G1, {"mode": "golden", "lock_h": 26.0, "weight_est": "slot_mass"}, G3),
        (G1, {"mode": "golden", "lock_h": "empirical", "weight_est": "mass_only"}, G3),
        (G1, {"mode": "golden", "lock_h": "empirical", "weight_est": "slot_ols"}, G3),
        (G1, {"mode": "golden", "lock_h": "empirical", "weight_est": "corridor_ols"}, G3),
        (G1, {"mode": "golden", "lock_h": "empirical", "weight_est": "huber"}, G3),
        (G1, G2, {"mode": "golden", "rej_cut": 1, "stat": "dc_week"}),
        (G1, G2, {"mode": "golden", "rej_cut": 1, "stat": "dc_fortnight"}),
        (G1, G2, {"mode": "golden", "rej_cut": 1, "stat": "ols_line"}),
        (G1, G2, {"mode": "golden", "rej_cut": 1, "stat": "stock_flow"}),
        (G1, G2, {"mode": "golden", "rej_cut": 1, "stat": "median_dc_week"}),
        (G1, G2, {"mode": "golden", "rej_cut": 2, "stat": "dc_day"}),
        ({"mode": "golden", "cap_thresh": 0.95, "stat": "ols_yard"},
         {"mode": "golden", "lock_h": "empirical", "weight_est": "huber"},
         {"mode": "golden", "rej_cut": 1, "stat": "ols_line"}),
        ({"mode": "golden", "cap_thresh": 0.95, "stat": "port_week_fe"},
         {"mode": "golden", "lock_h": "empirical", "weight_est": "corridor_ols"},
         {"mode": "golden", "rej_cut": 1, "stat": "dc_week"}),
    ]
    fam_res = [evaluate_route(w, s1k, s2k, s3k) for s1k, s2k, s3k in variant_specs]

    dir_res = evaluate_route(w, {"mode": "direct"}, {"mode": "direct"}, {"mode": "direct"})
    rig_res = evaluate_route(w, {"mode": "rigorous"}, {"mode": "rigorous"}, {"mode": "rigorous"})

    combos = [c for n in (1, 2, 3) for c in itertools.combinations(("S1", "S2", "S3"), n)]
    lat_res = {}
    for c in combos:
        k = "+".join(c)
        lat_res[k] = evaluate_route(
            w,
            H1 if "S1" in c else G1,
            H2 if "S2" in c else G2,
            H3 if "S3" in c else G3,
        )

    over_res = {
        "S1": evaluate_route(w, {"mode": "over"}, G2, G3),
        "S2": evaluate_route(w, G1, {"mode": "over"}, G3),
        "S3": evaluate_route(w, G1, G2, {"mode": "over"}),
    }

    run_res = {
        "generous": evaluate_route(w, {"mode": "generous"}, {"mode": "generous"}, {"mode": "generous"}),
        "calibrated": evaluate_route(w, {"mode": "calibrated"}, {"mode": "calibrated"}, {"mode": "calibrated"}),
        "hedge": evaluate_route(w, {"mode": "hedge"}, {"mode": "hedge"}, {"mode": "hedge"}),
        "cutoff": evaluate_route(
            w,
            {"mode": "cutoff_total_dc", "cap_thresh": 0.79},
            {"mode": "cutoff_any_bip", "lock_h": 1},
            {"mode": "cutoff_rej_raw", "rej_cut": 10},
        ),
    }
    extra_run_res = {
        "cutoff:s1_chamber_unnetted_95": evaluate_route(
            w, {"mode": "cutoff_chamber_raw", "cap_thresh": 0.95}, G2, G3
        ),
        "cutoff:s1_chamber_unnetted_90": evaluate_route(
            w, {"mode": "cutoff_chamber_raw", "cap_thresh": 0.90}, G2, G3
        ),
        "cutoff:s1_total_dc_78": evaluate_route(
            w, {"mode": "cutoff_total_dc", "cap_thresh": 0.78}, G2, G3
        ),
        "cutoff:s2_any_bip_1": evaluate_route(
            w, G1, {"mode": "cutoff_any_bip", "lock_h": 1}, G3
        ),
        "cutoff:s2_any_bip_3": evaluate_route(
            w, G1, {"mode": "cutoff_any_bip", "lock_h": 3}, G3
        ),
        "cutoff:s3_rej_1": evaluate_route(
            w, G1, G2, {"mode": "cutoff_rej_raw", "rej_cut": 1}
        ),
        "cutoff:s3_rej_10": evaluate_route(
            w, G1, G2, {"mode": "cutoff_rej_raw", "rej_cut": 10}
        ),
        "cutoff:s3_rej_50": evaluate_route(
            w, G1, G2, {"mode": "cutoff_rej_raw", "rej_cut": 50}
        ),
        "cutoff:s3_reweight_day_1": evaluate_route(
            w, G1, G2, {"mode": "cutoff_reweight", "rej_cut": 1}
        ),
        "cutoff:s3_reweight_day_10": evaluate_route(
            w, G1, G2, {"mode": "cutoff_reweight", "rej_cut": 10}
        ),
        "cutoff:s3_reweight_day_25": evaluate_route(
            w, G1, G2, {"mode": "cutoff_reweight", "rej_cut": 25}
        ),
        "cutoff:s3_reweight_box_1": evaluate_route(
            w, G1, G2, {"mode": "cutoff_reweight_box", "rej_cut": 1}
        ),
        "cutoff:s3_reweight_box_10": evaluate_route(
            w, G1, G2, {"mode": "cutoff_reweight_box", "rej_cut": 10}
        ),
    }

    members_spec = {}
    for m in MEMBERS:
        members_spec[m] = {
            "lines": [LINE_THRESHOLD],
            "truth": truth_res["members"][m],
            "golden": gold_res["members"][m],
            "family": [f["members"][m] for f in fam_res],
            "routes": {
                "direct": dir_res["members"][m],
                "rigorous": rig_res["members"][m],
            },
        }

    stumps_spec = {
        "S1": {
            "axis": "what",
            "opens": "coldstore_dock",
            "said_out_loud": (
                "Containers bound for an inland cold store whose specific thermal chamber is full "
                "are held back at the port under TERM_YARD_HOLD rather than delayed by port plugs."
            ),
            "steps_left": 4,
            "precedents": ["L26", "L28", "L38", "N36"],
            "sides": {"over": over_res["S1"]["members"]},
        },
        "S2": {
            "axis": "unit",
            "opens": "rail_handoff",
            "said_out_loud": (
                "Rail slots booked for co-loaded CHED lots frozen by late border inspections stay "
                "physically empty on departing trains and bump cleared standby boxes."
            ),
            "steps_left": 4,
            "precedents": ["L03", "L07", "L48", "N07"],
            "sides": {"over": over_res["S2"]["members"]},
        },
        "S3": {
            "axis": "who",
            "opens": "empty_depot",
            "said_out_loud": (
                "Empty reefers sitting in drayage yards are blocked by shipping-line depot portal "
                "quotas whose rejection log lacks container IDs and records repeated daily retries."
            ),
            "steps_left": 4,
            "precedents": ["N14", "N27", "L56", "L57"],
            "sides": {"over": over_res["S3"]["members"]},
        },
    }

    def _agg_fig(fid, key):
        return {
            "id": fid,
            "block": "ask",
            "golden": gold_res[key],
            "family": [f[key] for f in fam_res],
            "lattice": {k: v[key] for k, v in lat_res.items()},
            "routes": dict(
                {"rigorous": rig_res[key]},
                **{rn: rv[key] for rn, rv in run_res.items()},
                **{rn: rv[key] for rn, rv in extra_run_res.items()},
            ),
        }

    figures = [
        {"id": "C1_coldstore_dock", "block": "component", "member": "coldstore_dock"},
        {"id": "C2_rail_handoff", "block": "component", "member": "rail_handoff"},
        {"id": "C3_empty_depot", "block": "component", "member": "empty_depot"},
        {"id": "A_reefer_plug", "block": "ask", "member": "reefer_plug"},
        {"id": "A_phyto_insp", "block": "ask", "member": "phyto_insp"},
        {"id": "A_drayage_carrier", "block": "ask", "member": "drayage_carrier"},
        {"id": "A_vessel_berth", "block": "ask", "member": "vessel_berth", "sentence": "S_forced"},
        {"id": "A_edi_docs", "block": "ask", "member": "edi_docs", "sentence": "S_forced"},
        _agg_fig("A_total_2027", "total_2027"),
        _agg_fig("A_remed_days", "remed_days"),
        _agg_fig("A_cost_eur_m", "cost_eur_m"),
        _agg_fig("A_avoidable_eur_m", "avoidable_eur_m"),
        _agg_fig("A_bhv_2027", "bhv_2027"),
        _agg_fig("A_ham_2027", "ham_2027"),
        _agg_fig("A_q3_2027", "q3_2027"),
    ]

    falsification = {
        "check": (
            "Total 2026 cross-file physical conservation contrast container-days (same-vessel "
            "chamber-saturated port overflow + post-T-24h locked empty-flatcar rail displacement + "
            "same-DC closed-quota shipping-line empty-return excess, all in native container-days)"
        ),
        "observes_target": False,
        "truth": truth_res["contrast_cdays_26"],
        "golden": gold_res["diag"]["contrast_cdays_26"],
        "rivals": {
            "direct": dir_res["diag"]["contrast_cdays_26"],
            "rigorous": rig_res["diag"]["contrast_cdays_26"],
            "S1_lost": lat_res["S1"]["diag"]["contrast_cdays_26"],
            "S2_lost": lat_res["S2"]["diag"]["contrast_cdays_26"],
            "S3_lost": lat_res["S3"]["diag"]["contrast_cdays_26"],
            "generous": run_res["generous"]["diag"]["contrast_cdays_26"],
            "calibrated": run_res["calibrated"]["diag"]["contrast_cdays_26"],
            "hedge": run_res["hedge"]["diag"]["contrast_cdays_26"],
            "cutoff": run_res["cutoff"]["diag"]["contrast_cdays_26"],
        },
    }

    run_routes_spec = dict(
        {k: v["members"] for k, v in run_res.items()},
        **{k: v["members"] for k, v in extra_run_res.items()},
    )

    spec = {
        "task": "task27",
        "members": members_spec,
        "stumps": stumps_spec,
        "lattice": {k: v["members"] for k, v in lat_res.items()},
        "falsification": falsification,
        "run_routes": run_routes_spec,
        "figures": figures,
    }
    return spec, w, truth_res, gold_res, fam_res, lat_res, dir_res, rig_res, run_res, over_res


def main(argv=None):
    argv = argv or sys.argv[1:]
    spec, w, truth_res, gold_res, fam_res, lat_res, dir_res, rig_res, run_res, over_res = build_spec()
    rc = corelib.run(spec)

    if "--detail" in argv:
        print("\n--- Detail (Truth vs Golden vs 2026 History & Native-Unit Falsification Checks) ---")
        ch_u = _reconstruct_chamber_util(w)
        print(f"Total DC daily util range: {100*w['dc_total_util'].min():.1f}% to {100*w['dc_total_util'].max():.1f}%")
        print(f"Chamber Z02 util range:    {100*ch_u[:,0,:].min():.1f}% to {100*ch_u[:,0,:].max():.1f}% (capped boxes={w['_truth']['chamber_capped'].sum()})")
        print(f"Chamber Z07 util range:    {100*ch_u[:,1,:].min():.1f}% to {100*ch_u[:,1,:].max():.1f}%")
        print(f"Closed-quota boxes:        {w['_truth']['cont_quota_closed'].sum()} | Locked phyto rail slots: {w['_truth']['n_locked_phyto_sh'].sum()}")
        print(f"2026 total conserved excess c-days: {sum(truth_res['hist_2026'].values()):.1f}")
        print(f"Median unload lag (days):  {np.median(w['cont_unload_day'] - w['cont_day']):.1f} | Rail-only sib check: {(w['obs_phyto_sibling_tms_rail'][~w['cont_is_rail']].sum()):.1f}")
        print("\nMember comparison (2026 History vs 2027 Truth vs 2027 Golden vs Family Spread):")
        for m in MEMBERS:
            sp = max(abs(f["members"][m] - gold_res["members"][m]) for f in fam_res)
            print(
                f"  {m:16s} | 2026={truth_res['hist_2026'][m]:7.1f} | 2027_truth={truth_res['members'][m]:7.1f} "
                f"| 2027_gold={gold_res['members'][m]:7.1f} | spread={sp:5.1f} "
                f"| dir={dir_res['members'][m]:7.1f} | rig={rig_res['members'][m]:7.1f}"
            )
        print("\n2027 Network Aggregates (Golden vs Reflex):")
        ref_r = lat_res["S1+S2+S3"]
        for k in ("total_2027", "remed_days", "cost_eur_m", "avoidable_eur_m", "bhv_2027", "ham_2027", "q3_2027"):
            sp = max(abs(f[k] - gold_res[k]) for f in fam_res)
            print(
                f"  {k:16s} | gold={gold_res[k]:8.2f} | spread={sp:6.2f} "
                f"| S1={lat_res['S1'][k]:8.2f} | S2={lat_res['S2'][k]:8.2f} "
                f"| S3={lat_res['S3'][k]:8.2f} | reflex={ref_r[k]:8.2f}"
            )
        print("\nNative-unit falsification diagnostics:")
        print(
            f"  F1 same-vessel twin dwell gap (hours): truth={truth_res['twin_gap_h']:.2f}, "
            f"gold={gold_res['diag']['twin_gap_h']:.2f}, rig={rig_res['diag']['twin_gap_h']:.2f}, "
            f"over={over_res['S1']['diag']['twin_gap_h']:.2f}"
        )
        print(
            f"  F2 train weight drop per locked slot (t): truth={truth_res['tonnes_per_slot']:.2f}, "
            f"gold={gold_res['diag']['tonnes_per_slot']:.2f}, rig={rig_res['diag']['tonnes_per_slot']:.2f}, "
            f"over={over_res['S2']['diag']['tonnes_per_slot']:.2f}"
        )
        print(
            f"  F3 same-DC line empty-return gap (hours): truth={truth_res['line_gap_h']:.2f}, "
            f"gold={gold_res['diag']['line_gap_h']:.2f}, rig={rig_res['diag']['line_gap_h']:.2f}, "
            f"retry_mult={gold_res['diag']['retry_mult']:.2f}x"
        )
        gcall = corelib._calls(spec, gold_res["members"])
        hcall = corelib._calls(spec, truth_res["hist_2026"])
        print(f"\nForward window (Test 20): 2027 golden call={gcall}, 2026 history-mean call={hcall}, differs={gcall != hcall}")

    if "--forcing" in argv:
        G1 = {"mode": "golden", "cap_thresh": 0.95, "stat": "mean"}
        G2 = {"mode": "golden", "lock_h": "empirical", "weight_est": "slot_mass"}
        G3 = {"mode": "golden", "rej_cut": 1, "stat": "dc_day"}
        gcall = corelib._calls(spec, gold_res["members"])
        ok = True
        print("\n--- Forcing +/-20% perturbations ---")
        for name, popts in [
            ("S1 pullback -20%", {"mult_s1": 0.80}),
            ("S1 pullback +20%", {"mult_s1": 1.20}),
            ("S2 locked-slot -20%", {"mult_s2": 0.80}),
            ("S2 locked-slot +20%", {"mult_s2": 1.20}),
            ("S3 portal-block -20%", {"mult_s3": 0.80}),
            ("S3 portal-block +20%", {"mult_s3": 1.20}),
            ("All baseline -20%", {"mult_base": 0.80}),
            ("All baseline +20%", {"mult_base": 1.20}),
        ]:
            pr = evaluate_route(w, G1, G2, G3, proj_opts=popts)
            pcall = corelib._calls(spec, pr["members"])
            holds = pcall == gcall
            ok = ok and holds
            vals = " ".join(f"{m[:4]}={pr['members'][m]:.0f}" for m in MEMBERS)
            print(f"  {name:22s}: {'HOLD' if holds else 'FLIP'} | {vals}")
        print("FORCING:", "PASS" if ok else "FAIL")
        if not ok:
            rc = 1

    sys.exit(rc)


if __name__ == "__main__":
    main()
