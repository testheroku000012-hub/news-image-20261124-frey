#!/usr/bin/env python3
"""Entry point for news-image-20261124 — THE WORLD TODAY.

Ships the front page (entry.png), which build.py draws at build time with
Pillow, into MAKEFUN_OUTPUT_DIR. This file uses only the standard library:
no third-party packages, no network access, no fonts at runtime. It reads
the PNG header first (signature + IHDR width/height) and refuses to copy
anything that is not a 1024x1024 PNG under the 1 MiB cap.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_NAME = "entry.png"
MAX_BYTES = 1024 * 1024
EXPECT_W, EXPECT_H = 1024, 1024


def read_png(path):
    with open(path, "rb") as fh:
        data = fh.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("not a PNG file: bad signature")
    if data[12:16] != b"IHDR":
        raise SystemExit("not a PNG file: first chunk is not IHDR")
    width, height = struct.unpack(">II", data[16:24])
    return data, width, height


def main():
    src = os.path.join(HERE, SRC_NAME)
    data, width, height = read_png(src)
    if (width, height) != (EXPECT_W, EXPECT_H):
        raise SystemExit(
            f"bad dimensions {width}x{height}, expected "
            f"{EXPECT_W}x{EXPECT_H}"
        )
    if len(data) > MAX_BYTES:
        raise SystemExit(
            f"entry.png too large: {len(data)} bytes > {MAX_BYTES}"
        )
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, SRC_NAME)
    with open(dst, "wb") as fh:
        fh.write(data)
    print(f"copied {SRC_NAME}: {width}x{height}, {len(data)} bytes -> {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
