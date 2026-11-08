"""Cut task1's target.zip and golden.zip as a desktop zip tool in Berlin writes them (reduce-house-fixes H1): each
entry's time is its file's own last save (a workbook's or document's modified stamp, a PDF's date), and an export with
no stamp of its own takes the time of the pull that wrote it. Run after build.py and deliverables.py.

    python3 task1/generator/zips.py
"""
import datetime as dt
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import postprocess as PP  # noqa: E402

UTC = dt.timezone.utc
# the exports were pulled on the morning of 3 November 2026, one after another; the plan catalogue was last edited
# with the autumn promotion
EXPORTS = {
    "members_export_2026-11-03.csv": dt.datetime(2026, 11, 3, 7, 40, 12, tzinfo=UTC),
    "billing_events_2022-01_2026-10.csv": dt.datetime(2026, 11, 3, 7, 46, 51, tzinfo=UTC),
    "lesson_activity_monthly_2022-01_2026-10.csv": dt.datetime(2026, 11, 3, 7, 52, 7, tzinfo=UTC),
    "tutor_directory_2026-11-03.csv": dt.datetime(2026, 11, 3, 7, 54, 33, tzinfo=UTC),
    "signup_attribution_2022-01_2026-10.csv": dt.datetime(2026, 11, 3, 7, 58, 19, tzinfo=UTC),
    "nps_in_app_responses_2026-01_2026-10.csv": dt.datetime(2026, 11, 3, 8, 3, 44, tzinfo=UTC),
    "ecb_euro_reference_rates_2022-01_2026-11.csv": dt.datetime(2026, 11, 3, 8, 21, 5, tzinfo=UTC),
    "eurostat_edat_aes_l21_foreign_languages_known.csv": dt.datetime(2026, 11, 3, 8, 26, 38, tzinfo=UTC),
    "plans_and_promotions.json": dt.datetime(2026, 9, 29, 14, 7, 26, tzinfo=UTC),
}


def main():
    for folder, out in (("target", "target.zip"), ("golden", "golden.zip")):
        src = os.path.join(TASK, folder)
        PP.own_mtimes(src, EXPORTS)
        PP.zip_folder(src, os.path.join(TASK, out), zone="Europe/Berlin")
        print("cut", out)


if __name__ == "__main__":
    main()
