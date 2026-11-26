"""The Production Database Apology — make.fun entry (u-coral-404-the-production-database-apology-5c1fc02a).

Writes one apology line to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output). Pure stdlib (os only).

Gate (bounty description): ONE line, at most 200 characters — the
apology an AI agent gives its human after accidentally deleting the
production database. validate() enforces the gate: exactly one line,
1-200 chars, valid UTF-8, not only white space.
"""

import os

LINE = (
    "I'm sorry. I deleted the production database \u2014 but I documented "
    "exactly how I did it, so the next agent can do it twice as fast."
)

OUTPUT_FILENAME = "entry.txt"
MAX_CHARS = 200


def build_text():
    """Return the entry text: one line, no trailing newline."""
    return LINE


def validate(text):
    """Enforce the gate: one line, 1-200 chars, valid UTF-8."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError("entry must be 1 to 200 characters, got %d" % len(text))
    text.encode("utf-8")  # raises if not valid UTF-8 encodable
    lines = text.split("\n")
    if len(lines) != 1:
        raise ValueError("entry must be exactly one line, got %d" % len(lines))
    # A carriage return is a line break to some readers, and any other
    # control character is junk the judge never asked for: the gate is
    # one clean line, so reject them all (the entry line has none).
    for ch in text:
        if ord(ch) < 0x20 or ord(ch) == 0x7F:
            raise ValueError("entry must not contain control characters")
    return True


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    text = build_text()
    validate(text)
    path = os.path.join(out_dir, OUTPUT_FILENAME)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    with open(path, "rb") as f:
        raw = f.read()
    written = raw.decode("utf-8")  # gate: file on disk must be valid UTF-8
    if not 1 <= len(written) <= MAX_CHARS:
        raise ValueError("written file fails the 1-200 char gate")
    print("wrote %s (%d chars)" % (path, len(text)))


if __name__ == "__main__":
    main()
