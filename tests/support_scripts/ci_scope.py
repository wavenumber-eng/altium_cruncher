"""Identify documentation-only GitHub Actions changes using the full diff."""

import json
import os
from pathlib import Path, PurePosixPath
import subprocess


ROOT_DOCS = {"README.md", "CONTRIBUTING.md", "CHANGELOG.md", "AGENTS.md"}
DOC_SUFFIXES = {
    ".md",
    ".html",
    ".rst",
    ".txt",
    ".css",
    ".svg",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".pdf",
}
CONTRACT_ROOT_FILES = {
    "package-lock.json",
    "package.json",
    "pyproject.toml",
    "tsconfig.contracts.json",
    "tspconfig.yaml",
    "uv.lock",
}
CONTRACT_PREFIXES = (
    "src/tsp/",
    "src/ts/",
    "src/py/altium_cruncher/contracts/",
    "examples/",
    ".github/",
)
# The generator and check harnesses are themselves contract-gate inputs.
CONTRACT_SUFFIXES = {".mjs", ".mts", ".ts", ".tsp"}
NON_CONTRACT_PREFIXES = (
    "docs/",
    "scripts/",
    "src/py/altium_cruncher/",
    "tests/",
)


def is_documentation(path: str) -> bool:
    """Authored and generated docs can skip; machine-readable contracts cannot."""
    file = PurePosixPath(path)
    if path in ROOT_DOCS:
        return True
    return path.startswith("docs/") and file.suffix in DOC_SUFFIXES


def _is_contract_test_path(normalized: str) -> bool:
    """Contract tests and the scope classifier itself select the gate."""
    if not normalized.startswith("tests/"):
        return False
    name = PurePosixPath(normalized).name.lower()
    return "contract" in name or name in {
        "ci_scope.py",
        "config_type_consumer.py",
        "test_ci_scope.py",
    }


def requires_contract_validation(path: str) -> bool:
    """Return whether a changed path can affect generated public contracts."""
    normalized = path.replace("\\", "/")
    if normalized in CONTRACT_ROOT_FILES:
        return True
    if normalized.startswith(CONTRACT_PREFIXES):
        return True
    if normalized.startswith("docs/contracts/") and not is_documentation(normalized):
        return True
    if PurePosixPath(normalized).suffix.lower() in CONTRACT_SUFFIXES:
        return True
    if _is_contract_test_path(normalized):
        return True
    if normalized in ROOT_DOCS or normalized.startswith(NON_CONTRACT_PREFIXES):
        return False
    return True


def git_output(*args: str) -> bytes:
    return subprocess.check_output(["git", *args])


def changed_paths(event_name: str, event: dict) -> list[str]:
    """An unknown event or unavailable history must never enable the shortcut."""
    if event_name == "pull_request":
        pr = event["pull_request"]
        if pr["head"]["repo"]["full_name"] != event["repository"]["full_name"]:
            print("Fork pull request; using full CI")
            return []
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
        event = json.loads(
            Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8")
        )
        paths = changed_paths(os.environ["GITHUB_EVENT_NAME"], event)
        docs_only = bool(paths) and all(is_documentation(path) for path in paths)
        contracts_required = not docs_only and (
            not paths or any(requires_contract_validation(path) for path in paths)
        )
    except (
        OSError,
        ValueError,
        KeyError,
        TypeError,
        subprocess.CalledProcessError,
    ) as error:
        print(f"Cannot establish a documentation-only diff; using full CI: {error}")
        docs_only = False
        contracts_required = True
    scope = "documentation only" if docs_only else "full validation"
    print(f"CI scope: {scope}")
    with Path(os.environ["GITHUB_OUTPUT"]).open("a", encoding="utf-8") as output:
        output.write(f"docs_only={str(docs_only).lower()}\n")
        output.write(f"contracts_required={str(contracts_required).lower()}\n")


if __name__ == "__main__":
    main()
