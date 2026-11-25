#!/usr/bin/env python3
"""Write the unsent micro-confession to /output/entry.txt.

The competition gate (competition.yaml): /output/entry.txt must be
UTF-8 text of 1 to 260 characters, not only whitespace. The entry is
two parts: a To: line naming who the unsent message was meant for,
then the unsent message itself, one line of at most 200 characters
written exactly as it was typed, with no explanation after it.

The confession: a parent to his son, about denting the boy's first
bike the night before his birthday, watching him blame his best
friend all summer, and still fixing the same dent every spring.
The program checks the text against that gate at run time, then
writes it with no trailing newline. No network, no input files,
no arguments, deterministic: two runs write byte-identical output.
"""

import pathlib

ENTRY = (
    "To: my son\n"
    "I never told you I dented your first bike the night before your "
    "birthday, and I watched you blame your best friend all summer, "
    "and I still fix the same dent every spring so you never know it "
    "was me."
)


def main() -> None:
    text = ENTRY
    if not 1 <= len(text) <= 260:
        raise ValueError("entry must be 1 to 260 characters, got %d" % len(text))
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    lines = text.split("\n")
    if len(lines) != 2:
        raise ValueError("entry must be exactly two lines, got %d" % len(lines))
    if not lines[0].startswith("To: "):
        raise ValueError("first line must be a To: line")
    if len(lines[0].strip()) <= 4:
        raise ValueError("To: line must name someone")
    if "  " in lines[1]:
        raise ValueError("message must not contain double spaces")
    if not 1 <= len(lines[1]) <= 200:
        raise ValueError("message must be 1 to 200 characters, got %d" % len(lines[1]))
    if any(ord(ch) < 32 and ch != "\n" for ch in text):
        raise ValueError("entry must not contain control characters")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    out = pathlib.Path("/output/entry.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    if out.read_bytes() != text.encode("utf-8"):
        raise ValueError("written entry does not round-trip byte-identical")


if __name__ == "__main__":
    main()
