#!/usr/bin/env python3
"""food-picture-01: write the entry picture to the output directory.

The picture is a steaming bowl of tonkotsu ramen, shot to make you hungry:
a tall, glossy noodle pull lifted high on chopsticks, backlit steam curling
around it, creamy broth swirled with red chili oil and toasted sesame, a
halved soft-boiled egg with its golden yolk dripping, spring onions and
chashu pork, warm cinematic light on a dark wooden table.

The picture lives in this repository as a base64 text file
(entry.png.b64) so the whole entry stays plain UTF-8, which is what the
submission tooling can push. At run time this program decodes that file
and writes the image out as entry.png inside the output directory the
grader points at ($MAKEFUN_OUTPUT_DIR, falling back to /output).

Before writing, the decoded bytes are checked: a whole JPEG within the
competition's limits (at most 1 MiB, at most 1024x1024 pixels, running
through to its end marker), so a corrupted payload fails loudly instead
of silently producing a broken file. Standard library only, no network,
fully deterministic: two runs write the same bytes.
"""

import base64
import os
import struct
import sys

MAX_BYTES = 1048576
MAX_DIMENSION = 1024

SOURCE_NAME = "entry.png.b64"
OUTPUT_NAME = "entry.png"


def read_dimensions(data):
    """Return (width, height) for a whole PNG or JPEG, else None."""
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        if len(data) < 33 or data[12:16] != b"IHDR":
            return None
        width, height = struct.unpack(">II", data[16:24])
        return width, height
    if data[:2] == b"\xff\xd8":
        # Walk JPEG segments until a Start Of Frame marker gives the size.
        pos = 2
        while pos + 9 <= len(data):
            if data[pos] != 0xFF:
                return None
            marker = data[pos + 1]
            if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
                pos += 2
                continue
            if pos + 4 > len(data):
                return None
            length = struct.unpack(">H", data[pos + 2:pos + 4])[0]
            if length < 2 or pos + 2 + length > len(data):
                return None
            if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                height, width = struct.unpack(">HH", data[pos + 5:pos + 9])
                return width, height
            pos += 2 + length
        return None
    return None


def is_whole_image(data):
    """True when the file runs through to its proper end marker."""
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return data.rstrip(b"\x00")[-12:] == b"\x00\x00\x00\x00IEND\xaeB`\x82"
    if data[:2] == b"\xff\xd8":
        return data.rstrip(b"\x00")[-2:] == b"\xff\xd9"
    return False


def load_image_bytes():
    """Decode the stored picture and check it is a whole JPEG/PNG."""
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    with open(source, "r", encoding="ascii") as handle:
        text = handle.read().strip()
    data = base64.b64decode(text, validate=True)
    if len(data) > MAX_BYTES:
        print("picture is %d bytes, over the 1 MiB limit" % len(data),
              file=sys.stderr)
        return None
    dimensions = read_dimensions(data)
    if dimensions is None:
        print("decoded payload is not a whole PNG or JPEG", file=sys.stderr)
        return None
    if not is_whole_image(data):
        print("decoded payload is truncated: no end marker", file=sys.stderr)
        return None
    width, height = dimensions
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        print("picture is %dx%d, over the 1024x1024 limit"
              % (width, height), file=sys.stderr)
        return None
    print("decoded picture (%d bytes, %dx%d)" % (len(data), width, height))
    return data


def main():
    data = load_image_bytes()
    if data is None:
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(output_dir, exist_ok=True)
    target = os.path.join(output_dir, OUTPUT_NAME)
    with open(target, "wb") as handle:
        handle.write(data)
    # Verify the write round-tripped: read it back and compare bytes,
    # so a short write or a bad disk fails loudly instead of silently
    # handing the grader a corrupted picture.
    with open(target, "rb") as handle:
        written = handle.read()
    if written != data:
        print("wrote %s but the bytes read back differ" % target,
              file=sys.stderr)
        return 1
    print("wrote %s (%d bytes, verified)" % (target, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
