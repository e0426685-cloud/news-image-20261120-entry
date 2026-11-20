"""news-image-20261120 entrypoint (Python 3.13, standard library only).

The front page for Friday 20 November 2026 is committed in this repo as
entry.png (drawn by tools/build_image.py). This program is what the grader
runs: it reads that picture, checks it against the competition's gate (a
complete PNG or JPEG, no more than 1 MiB and 1024x1024 px), and writes it
unchanged to $MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png in the
grading container). It only copies bytes, so two runs produce identical
output.

Local check:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import struct
import sys
from pathlib import Path

BYTE_CAP = 1_048_576
PNG_SIG = b"\x89PNG\r\n\x1a\n"
JPG_SIG = b"\xff\xd8\xff"
PNG_TAIL = b"IEND\xaeB`\x82"


def read_entry() -> bytes:
    """Load entry.png from beside this file; refuse anything off-gate."""
    here = Path(__file__).resolve().parent
    blob = (here / "entry.png").read_bytes()
    if len(blob) == 0:
        raise SystemExit("entry.png is empty")
    if len(blob) > BYTE_CAP:
        raise SystemExit(f"entry.png is {len(blob)} bytes, above the 1 MiB cap")
    if blob.startswith(PNG_SIG):
        if not blob.endswith(PNG_TAIL):
            raise SystemExit("entry.png is a truncated PNG (no IEND chunk)")
        width, height = struct.unpack(">II", blob[16:24])
        if width > 1024 or height > 1024:
            raise SystemExit(f"entry.png is {width}x{height}, above the 1024 cap")
        print(f"entry.png is a {width}x{height} PNG ({len(blob)} bytes)")
    elif blob.startswith(JPG_SIG):
        if not blob.endswith(b"\xff\xd9"):
            raise SystemExit("entry.png is a truncated JPEG (no EOI marker)")
        print(f"entry.png is a JPEG ({len(blob)} bytes)")
    else:
        raise SystemExit("entry.png starts with neither the PNG nor JPEG magic")
    return blob


def write_output(blob: bytes) -> Path:
    """Write the picture to the output directory and prove it matches."""
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    dest.write_bytes(blob)
    if dest.read_bytes() != blob:
        raise SystemExit("the written entry.png differs from the source")
    return dest


def run() -> int:
    blob = read_entry()
    dest = write_output(blob)
    print(f"wrote {dest} ({len(blob)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(run())
