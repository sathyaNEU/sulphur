"""Cuts task10/target.zip from target/: the files at the archive's root, in name order, each entry at that file's own
last save in UK local time (build.py sets the times), so two cuts of the same pack are byte-identical.
python3 task10/generator/zip_target.py"""
import hashlib
import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def main(task=TASK):
    target = os.path.join(task, "target")
    out = os.path.join(task, "target.zip")
    sys.path.insert(0, HERE)
    import postprocess as PP
    PP.zip_folder(target, out)
    h = hashlib.sha256(open(out, "rb").read()).hexdigest()
    print("target.zip sha256 %s, %d bytes" % (h, os.path.getsize(out)))
    return h


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else TASK)
