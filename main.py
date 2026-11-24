#!/usr/bin/env python3
"""Deliver the front page for news-image-20261124.

The page itself (entry.png) is drawn at build time by build.py. This
entry point only ships it: it opens the file next to this script,
checks that it really is the 1024x1024 PNG we built (magic bytes,
IHDR dimensions, 1 MiB cap), and writes the identical bytes into
MAKEFUN_OUTPUT_DIR. Standard library only — no Pillow, no network,
no fonts, no randomness.
"""
import os
import struct
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = "entry.png"
BYTE_LIMIT = 1024 * 1024
WANT_W, WANT_H = 1024, 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def load_png(path):
    """Read a PNG and return (bytes, width, height) after header checks."""
    with open(path, "rb") as handle:
        blob = handle.read()
    if blob[:8] != PNG_MAGIC:
        raise SystemExit("entry.png: bad PNG signature")
    if blob[12:16] != b"IHDR":
        raise SystemExit("entry.png: first chunk is not IHDR")
    w, h = struct.unpack(">II", blob[16:24])
    return blob, w, h


def deliver(blob, width, height):
    """Write the validated bytes into MAKEFUN_OUTPUT_DIR/entry.png."""
    if (width, height) != (WANT_W, WANT_H):
        raise SystemExit(
            f"entry.png: {width}x{height}, want {WANT_W}x{WANT_H}"
        )
    if len(blob) > BYTE_LIMIT:
        raise SystemExit(
            f"entry.png: {len(blob)} bytes exceeds {BYTE_LIMIT}"
        )
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, FILE_NAME)
    with open(target, "wb") as handle:
        handle.write(blob)
    print(f"delivered {FILE_NAME}: {width}x{height}, "
          f"{len(blob)} bytes -> {target}")
    return 0


def run():
    source = os.path.join(BASE, FILE_NAME)
    blob, width, height = load_png(source)
    return deliver(blob, width, height)


if __name__ == "__main__":
    sys.exit(run())
