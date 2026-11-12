# task4 architecture 12, holistic audit (returned, pasted by the author on 2026-11-12)

Cut audited: READY commit 3795da7, target.zip 8bd9892f7f054b07, golden.zip 7459e2f2b331c98c.

> Your package is strong analytical work. The removal ledger reconciles exactly to the October report (391 removals
> across 16 parts), and the landings-versus-hours split (+19% / -13%) really does move the starter-generator, brake
> and bleed-valve forecasts.
>
> The problem is that the holdings per part number are not forced by the inputs. Your buy quantities depend on a Bodø
> shop turnaround of about 29 days in July and August 2027. Calibrating a day-by-day replay to the 2024-2026
> turnarounds (12.2 days mean) gives a productive fraction near 0.85. Run on the 2025 roster, that replay gives 12 to
> 17 days in July and August, and a change of 0.015 in the fraction swings the result widely. No 2027 roster is
> shipped. For the starter-generator alone, 17 days needs 6 spares, 29 days needs 9, and a saturated shop needs 13.
> Likewise, VHF at 25 removals (against roughly 33 from a plain hours-scaled rate) rests on choosing the 4-year window
> and treating aircraft-driven repeats as non-recurring, and no document pins either choice.
>
> To fix this, ship the 2027 shop roster and absence plan, and state the capacity basis in the standard (for example,
> the productive hours per technician day). Add a sentence to the standard fixing the rate window and the treatment of
> repeat removals traced to one aircraft. Then re-derive the holdings and the 35-removal saving under those pins.

Repair: see the design note's Draw ("Repair after the holistic audit") and the RESHIPPED commit.
