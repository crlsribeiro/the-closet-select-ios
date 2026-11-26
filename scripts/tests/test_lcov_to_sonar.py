"""Tests for scripts/coverage/lcov-to-sonar.py."""
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ElementTree
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "coverage" / "lcov-to-sonar.py"


def convert(lcov: str, prefix: str) -> ElementTree.Element:
    with tempfile.TemporaryDirectory() as folder:
        report = Path(folder) / "report.lcov"
        report.write_text(lcov.replace("{root}", str(ROOT)), encoding="utf-8")
        output = subprocess.run(
            [sys.executable, str(SCRIPT), str(report), str(ROOT), prefix],
            check=True, capture_output=True, text=True,
        ).stdout
    return ElementTree.fromstring(output)


def lines_of(element: ElementTree.Element) -> dict:
    return {
        int(line.get("lineNumber")): line.get("covered") == "true"
        for line in element.iter("lineToCover")
    }


class LcovToSonarTests(unittest.TestCase):
    def test_keeps_only_files_under_the_prefix_with_relative_paths(self):
        report = convert(
            "SF:{root}/Packages/Core/Sources/Core/A.swift\nDA:1,1\nend_of_record\n"
            "SF:/usr/lib/swift/Other.swift\nDA:1,1\nend_of_record\n",
            "Packages/Core/Sources",
        )

        self.assertEqual([file.get("path") for file in report], ["Packages/Core/Sources/Core/A.swift"])

    def test_line_is_covered_if_any_record_hit_it(self):
        report = convert(
            "SF:{root}/Packages/Core/Sources/Core/A.swift\nDA:3,0\nDA:3,2\nDA:4,0\nend_of_record\n",
            "Packages/Core/Sources",
        )

        self.assertEqual(lines_of(report), {3: True, 4: False})

    def test_empty_report_is_valid_xml(self):
        report = convert("", "Packages/Core/Sources")

        self.assertEqual(report.tag, "coverage")
        self.assertEqual(len(report), 0)


if __name__ == "__main__":
    unittest.main()
