#!/usr/bin/env python3
"""Convert an lcov report (from `llvm-cov export -format=lcov`) into SonarQube generic coverage XML.

Usage: lcov-to-sonar.py coverage.lcov <repo-root> <relative-source-prefix> > out.xml
Only files under <relative-source-prefix> (e.g. Packages/Core/Sources) are kept.
"""
import os
import sys
from xml.sax.saxutils import quoteattr


def main() -> None:
    lcov_path, repo_root, prefix = sys.argv[1], os.path.realpath(sys.argv[2]), sys.argv[3]
    files: dict[str, dict[int, bool]] = {}
    current = None
    with open(lcov_path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line.startswith("SF:"):
                path = os.path.relpath(os.path.realpath(line[3:]), repo_root)
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
