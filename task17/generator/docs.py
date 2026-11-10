"""The centre's documents: the allocation policy for the gpu partition (version 3), the 2027 partition plan, both
PDFs written the way the committee's office writes them (a Word document exported by LibreOffice Writer), and the
scheduler configuration history the systems group keeps as a text file."""
import datetime as dt

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

import officepdf as O
import params as P

CET = dt.timezone(dt.timedelta(hours=1))
CEST = dt.timezone(dt.timedelta(hours=2))
POLICY_TITLE = "Allocation policy for the gpu partition, version 3"
PLAN_TITLE = "Partition plan 2027: gpu partition of the sturmvogel cluster"


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.8, leading=13.6, spaceAfter=6)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, leading=14,
                        spaceBefore=8, spaceAfter=4, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8.2, leading=10.8, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4, leading=10.2)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


POLICY = [
    ("1. Scope", [
        "This policy governs the yearly allocation round for the gpu partition of the sturmvogel cluster: how the "
        "partition's service level is measured, how a round's grants are capped and how requests above the cap are "
        "cut. It applies to every project of the state's universities that holds or requests a grant of node-hours "
        "on the partition.",
    ]),
    ("2. Measures", [
        "2.1 The queue wait of a job is the time from the job becoming eligible to run to its first start.",
        "2.2 The jobs of a window are the gpu partition's jobs that became eligible in the window, taken in the "
        "centre's local time (Europe/Berlin), under either quality of service, and that ran. A job cancelled before "
        "it started is not a job of the window.",
        "2.3 A job is one entry in the scheduler's accounting, identified by its job id and its submission. A job "
        "that the scheduler requeues after a node failure is the same job, however many times it ran.",
        "2.4 The node-hours of a job are the nodes allocated to it multiplied by the hours it ran, summed over every "
        "run. The node-hours of a window are the node-hours of its jobs. Nodes are allocated whole.",
        "2.5 An outage is a node unavailable to the scheduler outside a maintenance window of the published "
        "calendar, whatever the reason. Outages are classed as software (the node is restored by a reboot), hardware "
        "(a part is replaced) and rack infrastructure (a switch or a power distribution unit shared by the nodes of "
        "a rack). Node-days lost are the node-days of outage.",
        "2.6 A multi-node outage is four or more nodes of one rack unavailable at the same time; the share of "
        "node-days lost in multi-node outages is the share lost while that was the case.",
        "2.7 Run-time statistics are taken over the jobs that completed or reached their time limit; jobs that "
        "failed or were cancelled are left out. A job's run time is its elapsed time, and a job that reached its "
        "limit ran for its limit.",
    ]),
    ("3. The allocation round", [
        "3.1 Service level. The partition meets its service level over a window when the 90th percentile of the "
        "queue wait of the window's jobs is at most %d hours." % 4,
        "3.2 The service level of a round is judged over its allocation year, 1 January to 31 December.",
        "3.3 The cap. The grants of a round are capped at the largest multiple of %s node-hours whose expected use "
        "meets the service level over the allocation year with a probability of at least %d per cent. The expected "
        "use of a grant is the share of granted node-hours that grants of the same standing, first year of funding "
        "or continuing, used in the completed allocation years on record, as the centre's accounting records it."
        % ("10,000", 80),
        "3.4 What the outcomes carry. The probability in 3.3 is taken over the outcomes of the allocation year as "
        "the record supports them: the jobs and their run times, the node failures and their repairs as they vary "
        "from year to year, and the uncertainty of every rate estimated from the record. No allowance is made beyond "
        "what the record shows.",
        "3.5 Requests above the cap are cut pro rata: every request is reduced by the same share, so that the "
        "grants sum to the cap.",
        "3.6 Procedure. Requests for the coming year are due by 31 October. The committee's recommendation goes to "
        "the centre's board in December, and grants run from 1 January. A project's grant is a limit on its "
        "node-hours for the year; unused node-hours lapse.",
    ]),
    ("4. Review", [
        "4.1 This policy is reviewed each year after the round. Version 3 adds 2.5 to 2.7 and 3.4 and restates 3.3 "
        "with the standing of a grant. Comments to the chair of the allocation committee.",
    ]),
]


def policy(path):
    body, h1, h2, small, cell = _styles()
    s = [Paragraph("%s, Allocation committee" % P.ORG, small),
         Paragraph(POLICY_TITLE, h1),
         Paragraph("Adopted by the allocation committee on 11 December 2025, after the 2026 round was decided; in "
                   "force from the 2027 round. Replaces version 2 (December 2024). Chair: Carolin Hofig.", small),
         Spacer(1, 4)]
    for head, paras in POLICY:
        s.append(Paragraph(head, h2))
        for p in paras:
            s.append(Paragraph(p, body))
    O.build(path, s, POLICY_TITLE, "Carolin Hofig", "Allocation policy, gpu partition",
            "%s | Allocation policy v3" % P.ORG_SHORT, dt.datetime(2025, 12, 11, 15, 42, tzinfo=CET),
            dt.datetime(2025, 12, 12, 9, 6, tzinfo=CET), producer="LibreOffice 25.8.3.2")


PLAN = [
    ("1. The partition", [
        "The gpu partition keeps its 64 nodes in eight racks of eight through 2027 (four accelerators and 512 GB of "
        "memory per node, one leaf switch and two power distribution units per rack). No hardware is added or "
        "retired in 2027; the next expansion is budgeted for the 2028 round.",
    ]),
    ("2. Scheduling", [
        "The time limit of the normal quality of service rises from 48 to 96 hours on 1 April 2027, as the user "
        "committee asked in September 2026 for long training and simulation runs. The short quality of service "
        "keeps its 4 hour limit. The scheduling policy is unchanged: first come first served by eligible time with "
        "backfill on requested walltime over whole nodes, as the configuration history records it.",
    ]),
    ("3. Maintenance", [
        "Maintenance windows follow the published calendar: one regular window a month, and one two-day window in "
        "June 2027 for the cooling loop and the firmware of the leaf switches. Nodes are drained into each window "
        "and the partition is returned to service at its end.",
    ]),
    ("4. Capacity", [
        "The partition's node-hours must cover the expected use of the round's grants. The 2027 round is sized by "
        "the allocation committee under the allocation policy; this plan supplies the partition's configuration for "
        "the year.",
    ]),
    ("5. Software", [
        "The driver and CUDA stack move to the release of January 2027 in the February window; the container runtime "
        "is unchanged. The project filesystem's expansion (see the storage report) is independent of the partition.",
    ]),
]


def plan(path):
    body, h1, h2, small, cell = _styles()
    s = [Paragraph("%s, HPC systems group" % P.ORG, small),
         Paragraph(PLAN_TITLE, h1),
         Paragraph("Issued 6 October 2026 for the 2027 allocation round. Owner: the HPC systems group.", small),
         Spacer(1, 4)]
    for head, paras in PLAN:
        s.append(Paragraph(head, h2))
        for p in paras:
            s.append(Paragraph(p, body))
    O.build(path, s, PLAN_TITLE, "HPC systems group", "Partition plan 2027", "%s | Partition plan 2027" % P.ORG_SHORT,
            dt.datetime(2026, 10, 6, 11, 18, tzinfo=CEST), dt.datetime(2026, 10, 6, 16, 2, tzinfo=CEST),
            producer="LibreOffice 25.8.3.2")


def config_history(path, restarts_local):
    """slurm.conf settings that matter for scheduling, in the order they went live, with the controller restarts
    the systems group logged beside them"""
    lines = [
        "# sturmvogel: scheduler configuration history for the gpu partition",
        "# HPC systems group; one entry per change that went live, newest last. Settings not listed are unchanged.",
        "",
        "2023-02-06  production configuration",
        "  ClusterName=sturmvogel",
        "  SchedulerType=sched/backfill",
        "  SchedulerParameters=bf_continue,bf_max_job_test=%d,bf_window=5760,bf_resolution=60,bf_interval=30" % P.BF_MAX,
        "  SelectType=select/linear",
        "  PriorityType=priority/basic",
        "  JobRequeue=1",
        "  FirstJobId=%d" % P.FIRST_JOB_ID,
        "  MaxJobId=%d" % P.MAX_JOB_ID,
        "  AccountingStorageType=accounting_storage/slurmdbd",
        "  PartitionName=gpu Nodes=gpu[001-048] Default=YES MaxTime=1-00:00:00 State=UP",
        "  QOS normal  MaxWall=1-00:00:00  (sacctmgr)",
        "  QOS short   MaxWall=04:00:00  MaxJobsPerUser=40  (sacctmgr)",
        "",
        "2023-09-18  slurmctld restarted (slurmdbd upgrade 23.02.5)",
        "2024-01-08  SchedulerParameters: bf_window 5760 -> 8640; slurmctld restarted",
        "2024-06-24  GrpTRESMins enforced per account from the allocations (AccountingStorageEnforce=limits); restart",
        "2025-03-17  PartitionName=gpu Nodes=gpu[001-056]  (rack 7 in service); slurmctld restarted",
        "2025-04-07  PartitionName=gpu Nodes=gpu[001-064]  (rack 8 in service); slurmctld restarted",
        "2025-10-13  slurmctld restarted (slurm 24.11.2)",
        "2026-05-03  QOS normal MaxWall=2-00:00:00; PartitionName=gpu MaxTime=2-00:00:00; slurmctld restarted 09:00",
        "2026-08-24  slurmctld restarted (slurmdbd purge)",
    ]
    lines += ["", "# controller restarts not tied to a setting (reloads, upgrades, hangs), from the ops log:"]
    for t in restarts_local:
        lines.append("  %s" % t.strftime("%Y-%m-%d %H:%M"))
    lines += ["", "# planned: QOS normal MaxWall=4-00:00:00 from 2027-04-01 (partition plan 2027)"]
    open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
