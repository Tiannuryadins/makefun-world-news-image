#!/usr/bin/env python3
"""World News in One Image — 13 November 2026. make.fun entry
(news-image-01).

Running this program writes ONE image: a newspaper-style poster
summarising the real world news of Friday, 13 November 2026.

The poster lives next to this file as world_news_13_nov_2026.png
and is read at run time, so the program needs no network access
and uses only the Python standard library (the grader runs
`python3 -P -s`, so no third-party packages are available — Pillow
cannot be used here). The poster itself is drawn by
render_poster.py (build-time, Pillow); re-run that script to
change the poster (see BUILD-TRANSCRIPT.md).

Output: the program writes the image to /output/entry.png — the path
the make.fun grader reads. The bounty gate accepts a whole PNG or
JPEG of at most 1 MiB and 1024 by 1024 pixels; this image is a PNG
of 1024x1024 pixels and 129,203 bytes. No network; two runs write
the same bytes.

Usage:
    python3 main.py                 # writes /output/entry.png
    python3 main.py out.png         # writes to the given path
    MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py   # local testing

If /output is not writable, the program falls back to
./output/entry.png.

Author: Januar (@januar)
Solana (reference only, not used by this program):
    FM6M2TMzjhzj7QztEV91bAwV4N2bApYd2AZpZLcHyeKm
"""

import hashlib
import os
import struct
import sys
from pathlib import Path

OUTPUT_FILENAME = "entry.png"

MAX_BYTES = 1024 * 1024
MAX_DIM = 1024

# Poster: 1024x1024 PNG, 129,203 bytes. Drawn by render_poster.py;
# the file sits next to this entrypoint in the repository.
IMAGE_FILE = Path(__file__).resolve().parent / "world_news_13_nov_2026.png"

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def _png_size(data: bytes):
    """Return (width, height) of a PNG by parsing its IHDR chunk.

    Pure stdlib — no Pillow needed.
    """
    if data[:8] != PNG_MAGIC:
        raise ValueError("not a PNG (bad magic bytes)")
    if len(data) < 33:
        raise ValueError("truncated PNG")
    length, ctype = struct.unpack(">I4s", data[8:16])
    if ctype != b"IHDR" or length != 13:
        raise ValueError("PNG has no IHDR chunk first")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def _resolve_output(argv):
    """Return the output path, mirroring the verified ai-happy-01 entry."""
    if len(argv) > 1:
        return Path(argv[1])
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(outdir, exist_ok=True)
        probe = Path(outdir) / ".makefun_write_test"
        probe.touch()
        probe.unlink()
    except OSError:
        # Local runs without a writable /output fall back to ./output.
        outdir = Path.cwd() / "output"
        os.makedirs(outdir, exist_ok=True)
    return Path(outdir) / OUTPUT_FILENAME


def main(argv) -> int:
    try:
        raw = IMAGE_FILE.read_bytes()
    except OSError as exc:
        print(f"error: cannot read {IMAGE_FILE.name}: {exc}",
              file=sys.stderr)
        return 1

    # Gate self-check: whole PNG, at most 1 MiB and 1024x1024 pixels.
    try:
        width, height = _png_size(raw)
    except ValueError as exc:
        print(f"error: image is not a valid PNG: {exc}",
              file=sys.stderr)
        return 1
    if len(raw) > MAX_BYTES or width > MAX_DIM or height > MAX_DIM:
        print(f"error: image {width}x{height}, {len(raw)} bytes — "
              f"exceeds the 1 MiB / 1024x1024 gate", file=sys.stderr)
        return 1

    out_path = _resolve_output(argv)
    out_path.write_bytes(raw)
    print(f"wrote {out_path} (PNG {width}x{height}, {len(raw):,} bytes, "
          f"sha256={hashlib.sha256(raw).hexdigest()[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
