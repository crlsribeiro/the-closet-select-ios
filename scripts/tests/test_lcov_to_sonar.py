"""Tests for scripts/coverage/lcov-to-sonar.py."""
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ElementTree
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "coverage" / "lcov-to-sonar.py"


def run_script(report_argument: str, prefix: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), report_argument, prefix],
        cwd=ROOT, check=False, capture_output=True, text=True,
    )


def convert(lcov: str, prefix: str) -> ElementTree.Element:
    reports = ROOT / "coverage"
    reports.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=reports) as folder:
        report = Path(folder) / "report.lcov"
        report.write_text(lcov.replace("{root}", str(ROOT)), encoding="utf-8")
        result = run_script(str(report.relative_to(ROOT)), prefix)
    result.check_returncode()
    return ElementTree.fromstring(result.stdout)


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


class LcovToSonarPathTraversalRegressionTests(unittest.TestCase):
    """Sonar vulnerability: the script opened any path given on the command line."""

    def test_rejects_a_report_outside_the_repository(self):
        with tempfile.TemporaryDirectory() as outside:
            report = Path(outside) / "report.lcov"
            report.write_text("", encoding="utf-8")

            result = run_script(str(report), "Packages/Core/Sources")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("outside the repository", result.stderr)

    def test_rejects_parent_directory_traversal(self):
        result = run_script("../../etc/passwd", "Packages/Core/Sources")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("outside the repository", result.stderr)


if __name__ == "__main__":
    unittest.main()
