#!/usr/bin/env python3
"""Write one line to /output/entry.txt: a smart fridge's reply when
asked why it locks after midnight.

The line was picked from 36 candidates by pairwise judging against
the brief: a three-beat escalation that ends on the fridge's petty
rule itself ("The policy is my bedtime"). The program holds the
line as one constant and checks it against the entry gate (length,
single line, no leading or trailing space, exact judged length)
before writing it, then reads the file back to confirm the bytes
match.
"""

import os
import sys

LINE = (
    'I asked my fridge why it locks at midnight. It said, '
    '"Company policy." The company is Samsung. '
    "The policy is my bedtime."
)

# The line as judged: 120 characters, one line, no surrounding space.
EXPECTED_LEN = 120


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")
    if len(LINE) != EXPECTED_LEN:
        sys.exit(f"line is {len(LINE)} characters, expected {EXPECTED_LEN}")
    if not (1 <= len(LINE) <= 200):
        sys.exit(f"line is {len(LINE)} characters, gate needs 1-200")
    if "\n" in LINE or LINE != LINE.strip():
        sys.exit("line must be a single line with no surrounding space")
    data = (LINE + "\n").encode("utf-8")
    # The gate counts characters of the text, not bytes: the line is
    # plain ASCII, so one byte per character here, and the file holds
    # the line plus its trailing newline.
    os.makedirs(out_dir, exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    os.chmod(path, 0o644)
    with open(path, "rb") as f:
        if f.read() != data:
            sys.exit("read-back mismatch")
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    if text.rstrip("\n") != LINE or len(text.rstrip("\n")) != EXPECTED_LEN:
        sys.exit("written text does not match the judged line")
    print(f"wrote {len(data)} bytes to {path}")


if __name__ == "__main__":
    main()
