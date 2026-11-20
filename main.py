"""Entry for make.fun's news-image-20261120 bounty (Python 3.13, stdlib only).

The repository holds the finished front page as entry.png, rendered from the
world news of Friday 20 November 2026 by tools/build_image.py. This program
is the graded entrypoint: it validates the picture against the competition
gate (a whole PNG or JPEG, at most 1 MiB) and writes it, byte for byte, to
<output>/entry.png, where <output> is $MAKEFUN_OUTPUT_DIR locally and
/output in the grader's container. It runs twice and both runs must produce
identical bytes, so it does nothing but read, check and copy the one file.

Run locally:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import sys
from pathlib import Path

MAX_BYTES = 1_048_576  # the gate's 1 MiB cap
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


def load_picture() -> bytes:
    """Read entry.png beside this file and check it passes the gate's shape."""
    picture_path = Path(__file__).resolve().parent / "entry.png"
    data = picture_path.read_bytes()
    if not data:
        raise SystemExit("entry.png is empty")
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry.png is {len(data)} bytes, over the 1 MiB gate cap")
    if not (data.startswith(PNG_MAGIC) or data.startswith(JPEG_MAGIC)):
        raise SystemExit("entry.png is neither a PNG nor a JPEG by its first bytes")
    if data.startswith(PNG_MAGIC) and not data.endswith(b"IEND\xaeB`\x82"):
        raise SystemExit("entry.png does not end with a PNG IEND chunk")
    return data


def main() -> int:
    data = load_picture()
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / "entry.png"
    target.write_bytes(data)
    if target.read_bytes() != data:
        raise SystemExit("written entry.png does not match the source bytes")
    print(f"wrote {target} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
