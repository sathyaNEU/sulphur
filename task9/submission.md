## Tags

**Domain:** Machine Learning Research, General Statistics & Data Science (Interpretability: feature attribution, probing, mechanistic analysis).
**Analytical objective:** Root-Cause Analysis.

## Final Recommendation

Take the conditioner disk out of the full PM under Rev G and change it after 1,570 wafers of its own use on PU-1 and PU-2 and after 1,200 on PU-3 and PU-4, which saves about USD 288,000 a year against Rev F as it stands: the disk's own wear carries 96.5 per cent of the edge ring's loss of 1.32 points of mean sort yield since April, and the high-downforce pair's disks reach the ring's onset at 910 wafers against 1,300. Rejected: one count for all four units (1,368 wafers, USD 12,452 a year worse), a return to Rev E (USD 74,464 a year worse), and any change to the pad or the retaining ring, which carry none of the loss beyond the pad's 3.5 per cent on top of the disk's.

## Supplementary Questions

### tessaline_fab2_edge_ring_review.pptx

1. The loss on wafers sorted 1 April to 31 August 2026: 1.32 points of mean wafer sort yield (band 1.23 to 1.41), each wafer's outermost-zone fails above its own interior fail rate plus the zone's fallout at a fresh disk, over all 24,445 sorted wafers with a retest replacing its first pass. The deck opens on it and charts the loss by sort month (January to March already at 0.28 points).
2. Good die lost by product, in a table beside that chart: P-A 209,000 (band 192,000 to 226,000), P-B 21,000 (19,000 to 23,000), P-C 316,000 (291,000 to 341,000), about USD 353,000 at the cost inputs' die values.
3. The causes ranked by their share of that loss, in a table: the conditioner disk's wear 96.5 per cent (band 92 per cent to 100 per cent), the pad's life on top of it 3.5 per cent (0 per cent to 8 per cent), and the retaining ring (-1.0 per cent), DEP-3 (0.2 per cent), SC-4 (-0.1 per cent) and the deposition chambers' RF hours (0.4 per cent) at none, each within 2.5 per cent of zero, with the evidence that rules each out (the six ring-only swaps, DEP-3's routing to PU-3 and PU-4, SC-4's start a week after Rev F).
4. Each unit's usage at which the loss starts, in wafers of the disk's own use, and the climb after it in points of the outermost sort zone's fail rate per 1,000 wafers: PU-1 1,300 wafers (band 1,100 to 1,490) and 17.0 points per 1,000 wafers (14.4 to 19.5); PU-2 1,300 wafers (band 1,100 to 1,490) and 17.0 points per 1,000 wafers (14.4 to 19.5); PU-3 910 wafers (band 770 to 1,050) and 21.2 points per 1,000 wafers (18.0 to 24.4); PU-4 910 wafers (band 770 to 1,050) and 21.2 points per 1,000 wafers (18.0 to 24.4); charted as the zone's excess against disk use for each downforce pair.
5. The shares of the loss, as a bar chart: 23 per cent that the 2,000-wafer rule would have cost anyway (band 20 per cent to 26 per cent), 34 per cent that Rev F's move to 2,800 added (31 per cent to 37 per cent) and 43 per cent that the EW-118 waiver's retained disks added (40 per cent to 46 per cent), each rule run on each unit's own polish sequence.
6. Each unit's change count for the disk once Rev G takes it out of the full PM, in a table: PU-1 and PU-2 1,570 wafers (band 1,440 to 1,700), PU-3 and PU-4 1,200 (1,100 to 1,300).
7. The yearly saving against Rev F as it stands: USD 288,000 (band USD 265,000 to USD 311,000), USD 85,698 on PU-1 and PU-2 and USD 202,564 on PU-3 and PU-4, at 58,500 wafers a year split by each unit's share since 1 June, beside each unit's cost per wafer under both specs.

## Critical Components

1. The ring's loss, 1.32 points of mean wafer sort yield from April to August, measured on every wafer against the fallout a fresh disk leaves, not against the band's level before April (1.06).
2. The dose on the disk's own use, by downforce pair: the loss starts at 1,300 wafers on PU-1 and PU-2 and climbs 17.0 points per 1,000 wafers, and at 910 and 21.2 on PU-3 and PU-4.
3. The rules' shares, each rule run on each unit's own wafers: 23 per cent the 2,000-wafer rule's own exposure, 34 per cent Rev F's extension, 43 per cent the EW-118 retained disks.

## Step-by-Step

1. Clean the records: the latest sort record per wafer, product aliases mapped, the MES's wafer-level chamber steps joined to the units' polish record, and each part's use counted from its own last replacement in the maintenance log's parts text (the EW-118 PMs keep the disk, the unscheduled swaps change one part), blank counters placed on the unit's polish record.
2. Measure the ring on every wafer as the outermost zone's fails above its interior rate plus the zone's fallout on disks short of their onset: 1.32 points. The classifier's EDGE_RING wafers alone give 1.13, and the band's level before April as the baseline gives 1.06, because the ring already cost 0.28 points from January to March.
3. Fit the outermost zone's excess on a hinge in the disk's own use, with the pad's life on the slope, one fit per downforce pair: onsets 1,300 and 910 wafers. One fit over the fleet gives 1,090 for every unit; wafers since the full PM put the onsets at 1,680 and 1,380.
4. Attribute the loss with each disk life's own slope beside the retaining ring, DEP-3, SC-4 and the RF hours: the disk 96.5 per cent, the pad 3.5 per cent, the rest none. Read wafer by wafer, the joint fit gives the retaining ring 4.6 per cent, which the six ring-only swaps refute; tool commonality points at PU-3 and PU-4 and DEP-3, which is routing.
5. Run the 2,000-wafer rule, Rev F and the actual history on each unit's own polish sequence and read the ring off the pair's curve: 23 per cent, 34 per cent and 43 per cent. Slicing the observed loss at 2,000 and 2,800 wafers of disk use gives 18 per cent, 40 per cent and 42 per cent.
6. Set each pair's count where the disk's cost per wafer (its USD 5,720 change and the good die the ring takes at the summer's mix) is lowest: 1,570 and 1,200 wafers. A dose from zero gives 1,097 and 868; moving the full PM instead gives 2,033 and 1,777.
7. Price the saving against Rev F's own 2,800-wafer cycle with the waiver ended: USD 288,000 a year. The summer's own loss rate taken as Rev F's gives USD 780,933, because it carries the retained disks.

No other conclusion survives: every sound reading of the fallout, the pairs, the weights and the mix keeps the loss between 1.23 and 1.41 points, the counts inside 8 per cent and the saving between USD 265,000 and USD 311,000, while each shortcut lands outside: the classifier and the pre-April baseline under-measure the loss, the wafer-level fit gives the retaining ring a share its swaps deny, slicing mis-splits the rules, and the summer's rate nearly triples the saving.
