"""Identify documentation-only GitHub Actions changes using the full diff."""

import json
import os
from pathlib import Path, PurePosixPath
import subprocess


ROOT_DOCS = {"README.md", "CONTRIBUTING.md", "CHANGELOG.md", "AGENTS.md"}
DOC_SUFFIXES = {".md", ".html", ".rst", ".txt", ".css", ".svg", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf"}


def is_documentation(path: str) -> bool:
    """Authored and generated docs can skip; machine-readable contracts cannot."""
    file = PurePosixPath(path)
    if path in ROOT_DOCS:
        return True
    return path.startswith("docs/") and file.suffix in DOC_SUFFIXES


def git_output(*args: str) -> bytes:
    return subprocess.check_output(["git", *args])


def changed_paths(event_name: str, event: dict) -> list[str]:
    """An unknown event or unavailable history must never enable the shortcut."""
    if event_name == "pull_request":
        pr = event["pull_request"]
        head = pr["head"]["sha"]
        base = git_output("merge-base", pr["base"]["sha"], head).decode().strip()
    elif event_name == "push":
        base, head = event["before"], event["after"]
    else:
        return []
    # Disable rename detection so moving code into docs examines both paths.
    output = git_output("diff", "--name-only", "--no-renames", "-z", base, head, "--")
    return [path.decode("utf-8") for path in output.split(b"\0") if path]


def main() -> None:
    try:
        event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
        paths = changed_paths(os.environ["GITHUB_EVENT_NAME"], event)
        docs_only = bool(paths) and all(is_documentation(path) for path in paths)
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print(f"Cannot establish a documentation-only diff; using full CI: {error}")
        docs_only = False
    scope = "documentation only" if docs_only else "full validation"
    print(f"CI scope: {scope}")
    with Path(os.environ["GITHUB_OUTPUT"]).open("a", encoding="utf-8") as output:
        output.write(f"docs_only={str(docs_only).lower()}\n")


if __name__ == "__main__":
    main()
