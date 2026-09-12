"""Protect the docs shortcut from hiding executable or contract changes."""

import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from support_scripts import ci_scope


class CiScopeTests(unittest.TestCase):
    def test_documentation_allowlist(self):
        for path in (
            "README.md", "CONTRIBUTING.md", "docs/plans/topic/plan.md",
            "docs/design/cli/toon.html", "docs/design/toon-config-fields.md",
            "docs/contracts/example.md", "docs/generated/style.css", "docs/images/board.png",
        ):
            with self.subTest(path=path):
                self.assertTrue(ci_scope.is_documentation(path))
        for path in (
            "src/py/README.md", "docs/contracts/config.schema.json",
            "docs/governance/artifacts.toml", "docs/viewer.js",
            ".github/workflows/ci.yml", "pyproject.toml", "uv.lock", "tests/test_example.py",
        ):
            with self.subTest(path=path):
                self.assertFalse(ci_scope.is_documentation(path))

    def test_manual_runs_and_empty_diffs_use_full_ci(self):
        self.assertEqual(ci_scope.changed_paths("workflow_dispatch", {}), [])
        self.assert_output([], "false")

    def test_mixed_changes_use_full_ci(self):
        self.assert_output(["README.md", "src/py/example.py"], "false")
        self.assert_output(["docs/contracts/config.schema.json"], "false")

    def test_documentation_changes_skip_heavy_jobs(self):
        self.assert_output(["README.md", "docs/build.md", "docs/design/toon-config-fields.md"], "true")

    def test_missing_history_uses_full_ci(self):
        self.assert_output(subprocess.CalledProcessError(128, "git"), "false")

    def assert_output(self, paths, expected):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            event = root / "event.json"
            event.write_text(json.dumps({}), encoding="utf-8")
            output = root / "output.txt"
            env = {"GITHUB_EVENT_PATH": str(event), "GITHUB_EVENT_NAME": "push", "GITHUB_OUTPUT": str(output)}
            with patch.dict(os.environ, env), patch.object(ci_scope, "changed_paths") as changed:
                if isinstance(paths, Exception):
                    changed.side_effect = paths
                else:
                    changed.return_value = paths
                ci_scope.main()
            self.assertEqual(output.read_text(encoding="utf-8"), f"docs_only={expected}\n")

    def test_real_git_diff_includes_both_sides_of_renames_and_all_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            def git(*args):
                return subprocess.check_output(["git", "-C", directory, *args]).decode().strip()

            git("init", "-q")
            git("config", "user.name", "CI test")
            git("config", "user.email", "ci@example.invalid")
            (root / "code.py").write_text("original code\n", encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "initial")
            base = git("rev-parse", "HEAD")
            (root / "docs").mkdir()
            (root / "code.py").rename(root / "docs" / "moved.md")
            for index in range(305):
                (root / "docs" / f"page-{index}.md").write_text("prose\n", encoding="utf-8")
            git("add", "-A")
            git("commit", "-qm", "rename and docs")
            head = git("rev-parse", "HEAD")

            def local_git(*args):
                return subprocess.check_output(["git", "-C", directory, *args])

            with patch.object(ci_scope, "git_output", side_effect=local_git):
                push_paths = ci_scope.changed_paths("push", {"before": base, "after": head})
                pr_paths = ci_scope.changed_paths("pull_request", {"pull_request": {"base": {"sha": base}, "head": {"sha": head}}})
            self.assertEqual(push_paths, pr_paths)
            self.assertEqual(len(push_paths), 307)
            self.assertIn("code.py", push_paths)
            self.assertIn("docs/moved.md", push_paths)
            self.assertFalse(all(ci_scope.is_documentation(path) for path in push_paths))


if __name__ == "__main__":
    unittest.main()
