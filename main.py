#!/usr/bin/env python3
"""Entry program: publish the 19 November 2026 world-news image.

The front page this entry submits ships in this repository as
entry.png (drawn by render.py). This program only puts a byte-for-byte
copy of it where the grader looks: the directory named by
MAKEFUN_OUTPUT_DIR, or /output when that variable is absent. It uses
the Python 3.13 standard library only, touches no network, and every
run writes exactly the same bytes.
"""

import os
from pathlib import Path

IMAGE_NAME = "entry.png"


def output_directory():
    """Directory the grader expects the image in for this run."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def publish():
    here = Path(__file__).resolve().parent
    payload = (here / IMAGE_NAME).read_bytes()
    destination = output_directory()
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / IMAGE_NAME
    target.write_bytes(payload)
    if target.read_bytes() != payload:
        raise RuntimeError(f"{IMAGE_NAME} was not written whole")


if __name__ == "__main__":
    publish()
