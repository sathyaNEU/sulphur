"""task9: the pack's documents, in their owners' own genres. The operations wiki defines what a replacement is, the two
health-pull policies and the decommissioning programme; the Kestrel field guide describes serial numbers and
firmware; the vendor datasheets state reliability claims. None of them says how to forecast anything.
"""
import params as P

WIKI = """# Drive operations: definitions and policies

Owner: {rel} (fleet reliability). Last edited 2026-09-02.

## What counts as a replacement

A **replacement** is a data drive taken out of a vault slot because it failed or because a health policy pulled it.
Two removal reasons count:

- `FAIL`: the drive stopped responding, dropped out of its array or failed a read-back. Reactive.
- `PULL`: the drive was removed by the health policy in force on the day (below). Proactive.

A drive removed with its vault (`DECOM`) is not a replacement. A removed drive whose serial is back in a slot within
30 days of the removal was not a failure (a reseat or a cable fault): count the removal out and the drive as in
service throughout. Boot SSDs and the QA burn-in vault (QA-01) are not data drives.

## Health-pull policies

| Policy | In force | Pull when |
|---|---|---|
| P1 | until 2025-05-31 | SMART 5 (reallocated sectors) above 50, or SMART 197 (pending sectors) above 10 |
| P2 | from 2025-06-01 | P1's rules, or SMART 187 (reported uncorrectable) above 0, or SMART 5 above 20 |

Pulls are scheduled by the site teams; a pulled drive is replaced from the site's spares like a failed one.

## Spares

Each site holds spares by drive family. Orders are placed a quarter ahead (one-quarter lead time); see
procurement_and_costs.yaml for stock on hand and unit costs.

## Vault decommissioning

Vaults of families past their service life are scheduled for retirement at the operations reviews (DECOM_REVIEW in
vault_events). A retired vault's drives are removed with reason `DECOM` over a few weeks; its data is migrated first.

## DC-3

DC-3 joined the fleet with the Brightstore acquisition; its racks were moved into Halden's inventory on 2024-03-01.
""".format(rel=P.PEOPLE["reliability"])

KESTREL = dict(
    title="Kestrel Data Products: field guide to serial numbers and firmware",
    intro=("This guide is for field engineers servicing Kestrel enterprise drives. It describes how to read a drive's "
           "serial number and which firmware a drive left the factory with."),
    serial=("A Kestrel serial number has thirteen characters: the letters KS; a two-letter plant code (TH for Ayutthaya, "
            "MY for Penang); four digits giving the year and ISO week the drive was built (YYWW); and a five-digit "
            "sequence number within the plant and week. Example: KSTH2214 03817 was built in Ayutthaya in 2022, week 14. "
            "Some customer systems print the serial with dashes between the groups (KS-TH-2214-03817); the characters "
            "are the same."),
    firmware_rows=[("KS10 family", "KS10.3.2", "all builds"),
                   ("HX18 family", "HX8.1.4", "builds to 2024 week 9"),
                   ("HX18 family", "HX8.2.0", "builds from 2024 week 10 to 2024 week 30"),
                   ("HX18 family", "HX8.2.3", "builds from 2024 week 31")],
    support=("Firmware is not updated in the field except under a Kestrel service bulletin. Power-on hours are reported "
             "in SMART attribute 9 by HX18 drives; KS10 drives report it only to Kestrel's own diagnostic agent."),
)

DATASHEETS = [
    ("Meridian MD8000NM", "8 TB", "2.0 million hours", "0.44%"),
    ("Meridian MD14TNM", "14 TB", "2.5 million hours", "0.35%"),
    ("Meridian MD16TNM", "16 TB", "2.5 million hours", "0.35%"),
    ("Tamsin TS20000E", "20 TB", "2.5 million hours", "0.35%"),
    ("Tamsin TS22000E", "22 TB", "2.5 million hours", "0.35%"),
    ("Tamsin TS24000E", "24 TB", "2.5 million hours", "0.35%"),
    ("Kestrel HX18T8A", "18 TB", "2.5 million hours", "0.35%"),
    ("Kestrel KS10T0A", "10 TB", "2.0 million hours", "0.44%"),
    ("Borealis VB12000", "12 TB", "2.0 million hours", "0.44%"),
]
