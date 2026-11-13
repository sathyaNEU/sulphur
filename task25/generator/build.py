"""The build entry point gates.py calls: the whole chain, as make.py runs it (--out builds into a scratch folder)."""
import sys

import make

if __name__ == "__main__":
    make.main(sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None)
