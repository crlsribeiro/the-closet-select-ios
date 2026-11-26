"""Tests for scripts/coverage/lcov-to-sonar.py."""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ElementTree
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "coverage" / "lcov-to-sonar.py"

_spec = importlib.util.spec_from_file_location("lcov_to_sonar", SCRIPT)
lcov_to_sonar = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lcov_to_sonar)


def convert(lcov: str, prefix: str) -> ElementTree.Element:
    files = lcov_to_sonar.parse_lcov(lcov.replace("{root}", str(ROOT)).splitlines(), ROOT, prefix)
    return ElementTree.fromstring(lcov_to_sonar.to_sonar_xml(files))


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


class CommandLineTests(unittest.TestCase):
    def run_main(self, *arguments: str) -> int:
        return lcov_to_sonar.main(["lcov-to-sonar.py", *arguments])

    def test_wrong_number_of_arguments_returns_usage_error(self):
        self.assertEqual(self.run_main("only-one"), 2)

    def test_converts_a_report_inside_the_repository(self):
        reports = ROOT / "coverage"
        reports.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=reports) as folder:
            report = Path(folder) / "report.lcov"
            report.write_text(f"SF:{ROOT}/Packages/Core/Sources/Core/A.swift\nDA:1,1\nend_of_record\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(report.relative_to(ROOT)), "Packages/Core/Sources"],
                cwd=ROOT, check=True, capture_output=True, text=True,
            )

        self.assertIn('path="Packages/Core/Sources/Core/A.swift"', result.stdout)


class LcovToSonarPathTraversalRegressionTests(unittest.TestCase):
    """Sonar vulnerability: the script opened any path given on the command line."""

    def test_rejects_a_report_outside_the_repository(self):
        with tempfile.TemporaryDirectory() as outside, self.assertRaises(lcov_to_sonar.OutsideRepositoryError):
            lcov_to_sonar.resolve_inside(ROOT, str(Path(outside) / "report.lcov"))

    def test_rejects_parent_directory_traversal(self):
        with self.assertRaises(lcov_to_sonar.OutsideRepositoryError):
            lcov_to_sonar.resolve_inside(ROOT, "../../etc/passwd")

    def test_command_line_refuses_paths_outside_the_repository(self):
        self.assertEqual(lcov_to_sonar.main(["lcov-to-sonar.py", "../../etc/passwd", "Packages"]), 1)


if __name__ == "__main__":
    unittest.main()
