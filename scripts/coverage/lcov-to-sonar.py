#!/usr/bin/env python3
"""Convert an lcov report (from `llvm-cov export -format=lcov`) into SonarQube generic coverage XML.

Run from the repository root:
    lcov-to-sonar.py coverage/core.lcov Packages/Core/Sources > coverage/core.xml

Only files under the given source prefix are kept. The report must be inside the repository.
"""
import os
import sys
from pathlib import Path
from xml.sax.saxutils import quoteattr


def resolve_inside(root: Path, candidate: str) -> Path:
    """Resolve a user-supplied path and refuse anything outside the repository (path traversal)."""
    path = (root / candidate).resolve()
    if not path.is_relative_to(root):
        sys.exit(f"error: {candidate} is outside the repository")
    return path


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit("usage: lcov-to-sonar.py <report.lcov> <source-prefix>")
    root = Path.cwd().resolve()
    lcov_path = resolve_inside(root, sys.argv[1])
    prefix = sys.argv[2]

    files: dict[str, dict[int, bool]] = {}
    current = None
    with lcov_path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line.startswith("SF:"):
                path = os.path.relpath(os.path.realpath(line[3:]), root)
                current = files.setdefault(path, {}) if path.startswith(prefix) else None
            elif line.startswith("DA:") and current is not None:
                number, count = line[3:].split(",")[:2]
                current[int(number)] = current.get(int(number), False) or int(count) > 0
            elif line == "end_of_record":
                current = None

    print('<coverage version="1">')
    for path, lines in sorted(files.items()):
        print(f"  <file path={quoteattr(path)}>")
        for number, covered in sorted(lines.items()):
            print(f'    <lineToCover lineNumber="{number}" covered="{str(covered).lower()}"/>')
        print("  </file>")
    print("</coverage>")


if __name__ == "__main__":
    main()
