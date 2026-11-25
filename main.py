#!/usr/bin/env python3
"""One-line office joke writer for the make.fun bounty.

The joke is fixed, so every run is identical: the program checks the
line against the bounty gate, then writes it to the requested file.
No network, no clock, no randomness, nothing to configure.
"""

import os
import sys
from pathlib import Path

JOKE = "Our printer only jams when the deadline is near, which is why I now address it as sir."
LOWER = 1
UPPER = 199
FALLBACK = Path("/output/entry.txt")


def pick_target(argv):
    """Work out where the joke goes: argument, env var, or the default."""
    if len(argv) > 1:
        return Path(argv[1])
    from_env = os.environ.get("OUTPUT_PATH")
    if from_env:
        return Path(from_env)
    return FALLBACK


def check_joke(line):
    """Check the joke against the gate and return how long it is."""
    size = len(line)
    if size < LOWER or size > UPPER:
        raise ValueError(f"joke runs {size} characters; the gate allows 1-199")
    stripped = line.strip()
    if not stripped:
        raise ValueError("joke is blank")
    if "\n" in stripped:
        raise ValueError("joke has to be one line, not several")
    if line != stripped:
        raise ValueError("joke must not start or end with a space")
    if "\u2014" in line:
        raise ValueError("joke must not hold an em dash")
    return size


def run(argv):
    """Write the joke, say what happened, and return the exit code."""
    if len(argv) > 1 and argv[1] in ("-h", "--help"):
        print(__doc__.strip())
        print("usage: python3 main.py [OUTPUT_PATH]")
        return 0
    target = pick_target(argv)
    try:
        size = check_joke(JOKE)
    except ValueError as err:
        print(err, file=sys.stderr)
        return 1
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(JOKE, encoding="utf-8")
    print(JOKE)
    print(f"wrote {size} characters to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run(sys.argv))
