"""The Robot Apology — entry program.

Writes two lines (224 chars, <=400) to /output/entry.txt: line 1 is a
robot apologising in a single sentence for one specific mistake (it
vacuumed up a half-finished jigsaw puzzle, mistaking the pieces for
crumbs); line 2 is one sentence on what it learned and what it will do
differently. Stdlib only, deterministic: the same bytes on every run.

Line craft (judge criteria in order, RULES.txt): the mistake is concrete
and visual, and only a robot vacuum could make it; the lesson follows
exactly from the failure — it failed to tell a puzzle piece from a
crumb, so it now photographs the floor first to tell them apart. The
voice stays in the machine's register ("vacuum" as a verb, no "eat"),
warm and a little rueful, never cute. No trailing newline: the file is
exactly line 1 + newline + line 2.
"""
import os

TEXT = (
    "I'm sorry I vacuumed up your half-finished jigsaw puzzle "
    "because from the floor the pieces looked exactly like crumbs.\n"
    "I now photograph the floor before every clean, so I can tell "
    "a puzzle piece from a crumb before I vacuum."
)

MAX_CHARS = 400


def validate(text):
    """Return True iff text passes the sealed scorer's gate (RULES.txt):
    UTF-8, 1 to 400 chars, not only whitespace, exactly two lines, one
    sentence per line. Length is counted in characters, as the scorer
    counts it — the newline between the lines counts as one character.
    """
    if not isinstance(text, str):
        return False
    if not 1 <= len(text) <= MAX_CHARS:
        return False
    if not text.strip():
        return False
    if "\r" in text:
        return False
    if any(ord(c) < 32 and c != "\n" for c in text):
        return False
    lines = text.split("\n")
    if len(lines) != 2:
        return False
    for line in lines:
        if not line.strip():
            return False
        if line.count(".") + line.count("!") + line.count("?") != 1:
            return False
    return True


def main():
    # Enforce the scorer's gate: fail loudly instead of writing an
    # invalid entry.
    if not validate(TEXT):
        raise SystemExit("entry text violates the 1-400 char two-line gate")
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(TEXT)
    # Write-verify: read the file back and refuse to exit cleanly if
    # the bytes on disk differ from the gated text.
    with open(out_path, "r", encoding="utf-8") as f:
        if f.read() != TEXT:
            raise SystemExit("entry.txt on disk does not match the gated text")


if __name__ == "__main__":
    main()
