#!/usr/bin/env python3
"""Convert an lcov report (from `llvm-cov export -format=lcov`) into SonarQube generic coverage XML.

Run from the repository root:
    lcov-to-sonar.py coverage/core.lcov Packages/Core/Sources > coverage/core.xml

Only files under the given source prefix are kept. The report must be inside the repository.
"""
import os
import sys
from pathlib import Path
from typing import Iterable
from xml.sax.saxutils import quoteattr

Coverage = dict[str, dict[int, bool]]


class OutsideRepositoryError(ValueError):
    """Raised when a user-supplied path points outside the repository (path traversal)."""


def resolve_inside(root: Path, candidate: str) -> Path:
    """Resolve a user-supplied path and refuse anything outside the repository."""
    path = (root / candidate).resolve()
    if not path.is_relative_to(root):
        raise OutsideRepositoryError(f"{candidate} is outside the repository")
    return path


def parse_lcov(lines: Iterable[str], root: Path, prefix: str) -> Coverage:
    """Return covered state per line for every source file under `prefix`, relative to `root`."""
    files: Coverage = {}
    current = None
    for raw in lines:
        line = raw.strip()
        if line.startswith("SF:"):
            path = os.path.relpath(os.path.realpath(line[3:]), root)
            current = files.setdefault(path, {}) if path.startswith(prefix) else None
        elif line.startswith("DA:") and current is not None:
            number, count = line[3:].split(",")[:2]
            current[int(number)] = current.get(int(number), False) or int(count) > 0
        elif line == "end_of_record":
            current = None
    return files


def to_sonar_xml(files: Coverage) -> str:
    output = ['<coverage version="1">']
    for path, lines in sorted(files.items()):
        output.append(f"  <file path={quoteattr(path)}>")
        for number, covered in sorted(lines.items()):
            output.append(f'    <lineToCover lineNumber="{number}" covered="{str(covered).lower()}"/>')
        output.append("  </file>")
    output.append("</coverage>")
    return "\n".join(output)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: lcov-to-sonar.py <report.lcov> <source-prefix>", file=sys.stderr)
        return 2
    root = Path.cwd().resolve()
    try:
        report = resolve_inside(root, argv[1])
    except OutsideRepositoryError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    with report.open(encoding="utf-8") as handle:
        print(to_sonar_xml(parse_lcov(handle, root, argv[2])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
