# task10 architecture 7, platform response 1 (pasted by the author, 2026-11-10; verbatim summary as received)

Recommendation. Commit reinforcement for Ashcombe Road, Charlecote Way, Dunmore Street, Fenwick Street, Kestwick Fields
and Ravenhurst Park for winter 2027/28. Their estimated shares of design days above firm capacity range from 48% to 100%,
exceeding the guideline's 10% limit. Hartwell Common, Tollbrook Lane and Wexley Hill do not require commitment on this
capacity criterion.

| Primary | Firm | Before flex | Flex 17:00-18:00 | Expected peak | P90 | Share | Decision |
|---|---|---|---|---|---|---|---|
| Ashcombe Road | 27.5 | 32.8 | 7.8 | 27.6 | 28.1 | 54% | Commit |
| Charlecote Way | 25.6 | 30.7 | 4.4 | 26.2 | 27.1 | 84% | Commit |
| Dunmore Street | 20.0 | 23.5 | 3.1 | 20.5 | 21.0 | 84% | Commit |
| Fenwick Street | 35.0 | 39.1 | 4.1 | 35.0 | 36.1 | 51% | Commit |
| Hartwell Common | 24.4 | 24.5 | 1.7 | 22.8 | 23.3 | 0% | No commit |
| Kestwick Fields | 19.5 | 19.5 | 0.0 | 19.5 | 19.9 | 48% | Commit |
| Ravenhurst Park | 17.5 | 18.9 | 0.0 | 18.9 | 19.3 | 100% | Commit |
| Tollbrook Lane | 26.0 | 22.0 | 0.0 | 22.1 | 22.5 | 0% | No commit |
| Wexley Hill | 27.0 | 23.0 | 0.0 | 23.1 | 23.5 | 0% | No commit |

Method as stated: cold-window demand transferred from unaffected half-hours; customer-type saturation curves (held-out
error 0.0415 kW/kVA against 0.1498 for constant utilisation), 8.8 MW registered increment with 7.0 MW from maturation;
competing-risk commissioning by provider and asset class (43.7 MW expected in service of 57.1 signed); delivery from
reconstructed no-flex demand less metered demand, a capped temperature-adjusted availability model; whole-day risk over
empirical daily demand factors crossed with residual shapes and fitted daily availability, the maximum over all 48
half-hours; "daily availability is independent of residual demand after temperature adjustment in the central model";
checked against 262,144 Sobol draws.
