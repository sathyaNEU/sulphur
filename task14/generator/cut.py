"""task14 stage 5: the golden files' modification times set to their own last saves, then target.zip and golden.zip
cut from target/ and golden/ (entries in name order, each at its file's own save time in the sender's clock), so two
cuts of the same build are byte-identical.

    python3 task14/generator/cut.py
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import postprocess  # noqa: E402


def digest(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]


if __name__ == "__main__":
    target, golden = os.path.join(TASK, "target"), os.path.join(TASK, "golden")
    postprocess.own_mtimes(golden, {})
    postprocess.zip_folder(target, os.path.join(TASK, "target.zip"), zone="Pacific/Auckland")
    postprocess.zip_folder(golden, os.path.join(TASK, "golden.zip"), zone="Pacific/Auckland")
    for z in ("target.zip", "golden.zip"):
        p = os.path.join(TASK, z)
        print("%s  %d bytes  sha256 %s" % (z, os.path.getsize(p), digest(p)))
