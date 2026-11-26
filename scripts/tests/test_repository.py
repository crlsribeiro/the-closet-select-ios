"""Regression tests for the pipeline and repository configuration.

Every bug found in CI or configuration gets a test here, the same way app bugs
get a Swift regression test. Run locally with:

    python3 -m unittest discover -s scripts/tests -v
"""
import re
import subprocess
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = sorted((ROOT / ".github" / "workflows").glob("*.yml"))


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def is_git_ignored(relative_path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "--no-index", "-q", relative_path],
        cwd=ROOT,
        check=False,
    )
    return result.returncode == 0


class GitIgnoreRegressionTests(unittest.TestCase):
    """Bug: a broad 'coverage/' rule ignored scripts/coverage/, so CI could not find the scripts."""

    def test_scripts_folder_is_never_ignored(self):
        for path in ["scripts/coverage/xccov-to-sonar.sh", "scripts/coverage/new-tool.py", "scripts/tests/x.py"]:
            with self.subTest(path=path):
                self.assertFalse(is_git_ignored(path), f"{path} must be committed")

    def test_generated_reports_are_ignored(self):
        for path in ["coverage/app.xml", "TestResults.xcresult", "TheClosetSelect.xcodeproj"]:
            with self.subTest(path=path):
                self.assertTrue(is_git_ignored(path), f"{path} is generated and must not be committed")

    def test_every_script_used_by_a_workflow_exists(self):
        for workflow in WORKFLOWS:
            for script in set(re.findall(r"scripts/[\w./-]+", workflow.read_text(encoding="utf-8"))):
                with self.subTest(workflow=workflow.name, script=script):
                    self.assertTrue((ROOT / script).exists(), f"{workflow.name} uses missing {script}")


class WorkflowSecurityRegressionTests(unittest.TestCase):
    """Bug: the Sonar token was visible to every step and expressions were used inside scripts."""

    def steps(self):
        for workflow in WORKFLOWS:
            for job_name, job in load_yaml(workflow)["jobs"].items():
                for step in job.get("steps", []):
                    yield workflow.name, job_name, step

    def test_run_scripts_do_not_interpolate_expressions(self):
        for workflow, job, step in self.steps():
            if "run" in step:
                with self.subTest(workflow=workflow, job=job, step=step.get("name")):
                    self.assertNotIn("${{", step["run"], "pass values through env: instead")

    def test_secrets_are_only_exposed_to_the_step_that_needs_them(self):
        for workflow in WORKFLOWS:
            data = load_yaml(workflow)
            scopes = [("workflow", data.get("env", {}))]
            scopes += [(name, job.get("env", {})) for name, job in data["jobs"].items()]
            for scope, env in scopes:
                for key, value in env.items():
                    with self.subTest(workflow=workflow.name, scope=scope, key=key):
                        is_presence_check = re.fullmatch(r"\$\{\{\s*secrets\.\w+\s*!=\s*''\s*}}", str(value))
                        self.assertTrue("secrets." not in str(value) or is_presence_check,
                                        "secrets belong in a step-level env")


class SupplyChainRegressionTests(unittest.TestCase):
    """Sonar vulnerabilities: actions referenced by movable tags and dependencies resolved without a lock."""

    def workflow_lines(self):
        for workflow in WORKFLOWS:
            for number, line in enumerate(workflow.read_text(encoding="utf-8").splitlines(), start=1):
                yield workflow.name, number, line

    def test_actions_are_pinned_to_a_full_commit_sha(self):
        for workflow, number, line in self.workflow_lines():
            match = re.search(r"uses:\s*([^\s#]+)", line)
            if match and not match.group(1).startswith("./"):
                with self.subTest(workflow=workflow, line=number):
                    self.assertRegex(match.group(1), r"@[0-9a-f]{40}$", "pin the action to a commit SHA")

    def test_swift_package_commands_use_resolved_versions(self):
        for workflow, number, line in self.workflow_lines():
            if re.search(r"\bswift (build|test)\b", line):
                with self.subTest(workflow=workflow, line=number):
                    self.assertIn("--force-resolved-versions", line)

    def test_pip_installs_are_pinned(self):
        for workflow, number, line in self.workflow_lines():
            if "pip install" in line:
                packages = [arg for arg in line.split("pip install", 1)[1].split() if not arg.startswith("-")]
                for package in packages:
                    with self.subTest(workflow=workflow, line=number, package=package):
                        self.assertIn("==", package)


class DependabotRegressionTests(unittest.TestCase):
    """Bug: Dependabot opened pull requests directly against main."""

    def test_every_update_targets_develop(self):
        config = load_yaml(ROOT / ".github" / "dependabot.yml")
        for update in config["updates"]:
            with self.subTest(ecosystem=update["package-ecosystem"]):
                self.assertEqual(update.get("target-branch"), "develop")


if __name__ == "__main__":
    unittest.main()
