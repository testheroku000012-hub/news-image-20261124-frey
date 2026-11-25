#!/usr/bin/env python3
"""Entry point for THE WORLD TODAY -- news-image-20261124 v2.

Copies the rendered entry.png shipped in this repository to the output
directory the grader provides. Standard library only, no network,
deterministic: the bytes written are exactly the bytes shipped, so
two runs produce identical output.
"""
import os
import shutil
import struct
import sys

PNG_SIG = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576


def validate_png(data):
    """Check the shipped file is a whole 1024x1024 PNG under 1 MiB."""
    assert data[:8] == PNG_SIG, "not a PNG file"
    assert len(data) <= MAX_BYTES, "entry.png over 1 MiB: %d" % len(data)
    width, height = struct.unpack(">II", data[16:24])
    assert (width, height) == (1024, 1024), "not 1024x1024: %dx%d" % (
        width, height)
    return len(data)


def output_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "output")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as fh:
        data = fh.read()
    size = validate_png(data)
    dst_dir = output_dir()
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote %s (%d bytes)" % (dst, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
