"""Dependency-free Python signoff for the Altium Cruncher package.

Mirrors the spirit of the private altium_monkey L9 lane (see toolz/altium_monkey
AGENTS.md: "Always Types in python. Avoid Any, prefer objects" and "we strive
for a radon cyclic complexity test of A or B in all new code"). Five lanes:

1. file-too-large: hard caps on Python source file line count and byte size.
2. complexity: per-function cyclomatic complexity. New functions must be radon
   A or B (<= 10). Existing offenders are grandfathered through a baseline
   that ratchets downward only.
3. annotation-missing: every non-self/cls parameter and every return must be
   annotated. Existing offenders are grandfathered through the baseline.
4. any-count: total `Any` annotation occurrences across the scanned tree must
   not exceed the baseline value. Use --update-baseline after intentional
   reductions.
5. duplicate-functions: exact body-hash duplicates beyond the baseline groups
   are blocked. Tiny bodies are skipped to avoid trivial-stub noise.

The script is AST-only. It does not import the inspected files, does not require
radon or mypy, and is meant to run from CI and pre-commit alike.
"""

from __future__ import annotations

import argparse
import ast
import fnmatch
import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path


DEFAULT_INCLUDES: tuple[str, ...] = (
    "__init__.py",
    "src/py/altium_cruncher/**/*.py",
    "tests/support_scripts/**/*.py",
)
DEFAULT_EXCLUDES: tuple[str, ...] = (
    "**/__pycache__/**",
    "**/_build/**",
)
DEFAULT_MAX_FILE_LINES = 2500
DEFAULT_MAX_FILE_BYTES = 100_000
DEFAULT_NEW_CODE_MAX_COMPLEXITY = 10  # radon B
DEFAULT_DUPLICATE_MIN_STATEMENTS = 5
COMPLEXITY_RANK_LIMITS: tuple[tuple[int, str], ...] = (
    (5, "A"),
    (10, "B"),
    (20, "C"),
    (30, "D"),
    (40, "E"),
)
SELF_PARAM_NAMES: frozenset[str] = frozenset({"self", "cls"})


def complexity_rank(value: int) -> str:
    for limit, rank in COMPLEXITY_RANK_LIMITS:
        if value <= limit:
            return rank
    return "F"


@dataclass(frozen=True)
class FunctionRecord:
    qualname: str
    path: str
    name: str
    line: int
    complexity: int
    is_dunder: bool
    is_private: bool
    annotation_missing_params: tuple[str, ...]
    annotation_missing_return: bool
    body_hash: str
    body_statement_count: int


@dataclass(frozen=True)
class FileRecord:
    path: str
    line_count: int
    byte_count: int
    any_count: int
    functions: tuple[FunctionRecord, ...]


@dataclass
class Baseline:
    schema: int = 1
    max_file_lines: int = DEFAULT_MAX_FILE_LINES
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES
    max_new_code_complexity: int = DEFAULT_NEW_CODE_MAX_COMPLEXITY
    file_lines_offenders: dict[str, int] = field(default_factory=dict)
    file_bytes_offenders: dict[str, int] = field(default_factory=dict)
    complexity_offenders: dict[str, int] = field(default_factory=dict)
    annotation_missing_offenders: list[str] = field(default_factory=list)
    any_count_total: int = 0
    duplicate_groups: list[dict[str, object]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "Baseline":
        return cls(
            schema=int(payload.get("schema", 1) or 1),
            max_file_lines=int(payload.get("max_file_lines", DEFAULT_MAX_FILE_LINES)),
            max_file_bytes=int(payload.get("max_file_bytes", DEFAULT_MAX_FILE_BYTES)),
            max_new_code_complexity=int(
                payload.get("max_new_code_complexity", DEFAULT_NEW_CODE_MAX_COMPLEXITY)
            ),
            file_lines_offenders=dict(payload.get("file_lines_offenders", {}) or {}),
            file_bytes_offenders=dict(payload.get("file_bytes_offenders", {}) or {}),
            complexity_offenders=dict(payload.get("complexity_offenders", {}) or {}),
            annotation_missing_offenders=list(
                payload.get("annotation_missing_offenders", []) or []
            ),
            any_count_total=int(payload.get("any_count_total", 0) or 0),
            duplicate_groups=list(payload.get("duplicate_groups", []) or []),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": self.schema,
            "max_file_lines": self.max_file_lines,
            "max_file_bytes": self.max_file_bytes,
            "max_new_code_complexity": self.max_new_code_complexity,
            "file_lines_offenders": dict(sorted(self.file_lines_offenders.items())),
            "file_bytes_offenders": dict(sorted(self.file_bytes_offenders.items())),
            "complexity_offenders": dict(sorted(self.complexity_offenders.items())),
            "annotation_missing_offenders": sorted(self.annotation_missing_offenders),
            "any_count_total": self.any_count_total,
            "duplicate_groups": sorted(
                (
                    {
                        "hash": str(group.get("hash", "")),
                        "members": sorted(list(group.get("members", []) or [])),
                    }
                    for group in self.duplicate_groups
                ),
                key=lambda group: str(group.get("hash", "")),
            ),
        }


@dataclass(frozen=True)
class Finding:
    rule: str
    qualname: str
    message: str
    value: int = 0
    baseline: int = 0
    severity: str = "error"


class _ComplexityVisitor(ast.NodeVisitor):
    """Approximates radon cyclomatic complexity for one function body.

    Radon counts: each branch point (if/elif/for/while/except/assert), each
    boolean operator chain length minus one, each comprehension `if`, ternary
    expressions, lambdas, and match cases. Nested functions are scored
    independently and skipped here.
    """

    def __init__(self) -> None:
        self.score = 1

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        return

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        return

    def visit_If(self, node: ast.If) -> None:
        self.score += 1
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        self.score += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self.score += 1
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        self.score += 1
        self.generic_visit(node)

    def visit_Try(self, node: ast.Try) -> None:
        self.score += len(node.handlers)
        self.generic_visit(node)

    def visit_TryStar(self, node: ast.AST) -> None:
        handlers = getattr(node, "handlers", []) or []
        self.score += len(handlers)
        self.generic_visit(node)

    def visit_Assert(self, node: ast.Assert) -> None:
        self.score += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        if len(node.values) >= 2:
            self.score += len(node.values) - 1
        self.generic_visit(node)

    def visit_IfExp(self, node: ast.IfExp) -> None:
        self.score += 1
        self.generic_visit(node)

    def visit_comprehension(self, node: ast.comprehension) -> None:
        self.score += len(node.ifs)
        self.generic_visit(node)

    def visit_Lambda(self, node: ast.Lambda) -> None:
        self.score += 1

    def visit_Match(self, node: ast.Match) -> None:
        self.score += len(node.cases)
        self.generic_visit(node)


def _function_complexity(node: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    visitor = _ComplexityVisitor()
    for stmt in node.body:
        visitor.visit(stmt)
    return visitor.score


def _strip_docstring_statements(body: list[ast.stmt]) -> list[ast.stmt]:
    if not body:
        return []
    first = body[0]
    if (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
    ):
        return body[1:]
    return body


def _function_body_hash(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
) -> tuple[str, int]:
    body = _strip_docstring_statements(node.body)
    if not body:
        return ("", 0)
    # Use ast.unparse (canonical source) rather than ast.dump so the digest is
    # stable across Python versions; ast.dump output gains new node fields
    # between releases (e.g., type_params in 3.12+) which made baselines
    # generated under one interpreter fail when the test ran under another.
    canonical = "\n".join(ast.unparse(stmt) for stmt in body)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]
    return (digest, len(body))


def _annotation_missing(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
) -> tuple[tuple[str, ...], bool]:
    args = node.args
    missing_params: list[str] = []
    seen: set[str] = set()
    arg_groups: list[list[ast.arg]] = [
        list(getattr(args, "posonlyargs", []) or []),
        list(args.args or []),
        list(args.kwonlyargs or []),
    ]
    for group in arg_groups:
        for arg in group:
            if arg.arg in SELF_PARAM_NAMES and arg.annotation is None:
                continue
            if arg.annotation is None and arg.arg not in seen:
                missing_params.append(arg.arg)
                seen.add(arg.arg)
    if args.vararg is not None and args.vararg.annotation is None:
        missing_params.append(f"*{args.vararg.arg}")
    if args.kwarg is not None and args.kwarg.annotation is None:
        missing_params.append(f"**{args.kwarg.arg}")
    missing_return = node.returns is None
    return (tuple(missing_params), missing_return)


def _count_any_in_node(node: ast.AST | None) -> int:
    if node is None:
        return 0
    count = 0
    for sub in ast.walk(node):
        if isinstance(sub, ast.Name) and sub.id == "Any":
            count += 1
            continue
        if isinstance(sub, ast.Attribute) and sub.attr == "Any":
            count += 1
    return count


def _count_any_in_module(tree: ast.Module) -> int:
    count = 0
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            count += _count_any_in_node(node.returns)
            args = node.args
            for arg in (
                list(getattr(args, "posonlyargs", []) or [])
                + list(args.args or [])
                + list(args.kwonlyargs or [])
            ):
                count += _count_any_in_node(arg.annotation)
            if args.vararg is not None:
                count += _count_any_in_node(args.vararg.annotation)
            if args.kwarg is not None:
                count += _count_any_in_node(args.kwarg.annotation)
            continue
        if isinstance(node, ast.AnnAssign):
            count += _count_any_in_node(node.annotation)
            continue
        if isinstance(node, ast.arg):
            continue
    return count


def _walk_function_records(tree: ast.Module, rel_path: str) -> list[FunctionRecord]:
    records: list[FunctionRecord] = []

    def visit(node: ast.AST, scope_parts: tuple[str, ...]) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                scope = scope_parts + (child.name,)
                qualified = f"{rel_path}::{'.'.join(scope)}"
                complexity = _function_complexity(child)
                missing_params, missing_return = _annotation_missing(child)
                body_hash, body_statements = _function_body_hash(child)
                records.append(
                    FunctionRecord(
                        qualname=qualified,
                        path=rel_path,
                        name=child.name,
                        line=child.lineno,
                        complexity=complexity,
                        is_dunder=(
                            child.name.startswith("__")
                            and child.name.endswith("__")
                        ),
                        is_private=(
                            child.name.startswith("_")
                            and not (
                                child.name.startswith("__")
                                and child.name.endswith("__")
                            )
                        ),
                        annotation_missing_params=missing_params,
                        annotation_missing_return=missing_return,
                        body_hash=body_hash,
                        body_statement_count=body_statements,
                    )
                )
                visit(child, scope)
            elif isinstance(child, ast.ClassDef):
                visit(child, scope_parts + (child.name,))
            else:
                visit(child, scope_parts)

    visit(tree, ())
    return records


def _relative_path(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _collect_files(
    root: Path, includes: list[str], excludes: list[str]
) -> list[Path]:
    seen: dict[Path, None] = {}
    for pattern in includes:
        for path in root.glob(pattern):
            if path.is_file() and path.suffix == ".py":
                seen[path.resolve()] = None
    output: list[Path] = []
    for path in sorted(seen):
        rel = _relative_path(path, root)
        if any(fnmatch.fnmatch(rel, pat.replace("\\", "/")) for pat in excludes):
            continue
        output.append(path)
    return output


def _analyze_file(path: Path, root: Path) -> FileRecord:
    rel = _relative_path(path, root)
    text = path.read_text(encoding="utf-8")
    line_count = text.count("\n") + (0 if text.endswith("\n") else 1)
    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError as err:
        raise SystemExit(f"py_signoff: failed to parse {rel}: {err}") from err
    functions = tuple(_walk_function_records(tree, rel))
    any_count = _count_any_in_module(tree)
    return FileRecord(
        path=rel,
        line_count=line_count,
        byte_count=path.stat().st_size,
        any_count=any_count,
        functions=functions,
    )


def _evaluate_file_measure(
    rec: FileRecord,
    *,
    rule: str,
    label: str,
    value: int,
    cap: int,
    grandfathered: int | None,
    findings: list[Finding],
) -> int | None:
    if value <= cap:
        return None
    if grandfathered is None:
        findings.append(
            Finding(
                rule=rule,
                qualname=rec.path,
                message=f"{rec.path} has {value} {label} (cap {cap}, no baseline entry)",
                value=value,
                baseline=cap,
            )
        )
        return value
    if value > grandfathered:
        findings.append(
            Finding(
                rule=rule,
                qualname=rec.path,
                message=f"{rec.path} grew to {value} {label} (baseline {grandfathered})",
                value=value,
                baseline=grandfathered,
            )
        )
    return min(value, grandfathered)


def _evaluate_file_size_caps(
    files: list[FileRecord],
    baseline: Baseline,
    findings: list[Finding],
) -> tuple[dict[str, int], dict[str, int]]:
    file_lines_offenders: dict[str, int] = {}
    file_bytes_offenders: dict[str, int] = {}
    for rec in files:
        line_offender = _evaluate_file_measure(
            rec,
            rule="file-lines",
            label="lines",
            value=rec.line_count,
            cap=baseline.max_file_lines,
            grandfathered=baseline.file_lines_offenders.get(rec.path),
            findings=findings,
        )
        if line_offender is not None:
            file_lines_offenders[rec.path] = line_offender

        byte_offender = _evaluate_file_measure(
            rec,
            rule="file-bytes",
            label="bytes",
            value=rec.byte_count,
            cap=baseline.max_file_bytes,
            grandfathered=baseline.file_bytes_offenders.get(rec.path),
            findings=findings,
        )
        if byte_offender is not None:
            file_bytes_offenders[rec.path] = byte_offender
    return file_lines_offenders, file_bytes_offenders


def _evaluate(
    files: list[FileRecord],
    baseline: Baseline,
    duplicate_min_statements: int,
) -> tuple[Baseline, list[Finding]]:
    findings: list[Finding] = []

    file_lines_offenders, file_bytes_offenders = _evaluate_file_size_caps(
        files,
        baseline,
        findings,
    )

    # Complexity.
    complexity_offenders: dict[str, int] = {}
    for rec in files:
        for fn in rec.functions:
            if fn.complexity <= baseline.max_new_code_complexity:
                continue
            grandfathered = baseline.complexity_offenders.get(fn.qualname)
            if grandfathered is None:
                findings.append(
                    Finding(
                        rule="complexity",
                        qualname=fn.qualname,
                        message=(
                            f"{fn.qualname} has cyclomatic complexity "
                            f"{fn.complexity} (rank {complexity_rank(fn.complexity)}, "
                            f"new-code limit {baseline.max_new_code_complexity})"
                        ),
                        value=fn.complexity,
                        baseline=baseline.max_new_code_complexity,
                    )
                )
                complexity_offenders[fn.qualname] = fn.complexity
                continue
            if fn.complexity > grandfathered:
                findings.append(
                    Finding(
                        rule="complexity",
                        qualname=fn.qualname,
                        message=(
                            f"{fn.qualname} complexity grew from "
                            f"{grandfathered} to {fn.complexity}"
                        ),
                        value=fn.complexity,
                        baseline=grandfathered,
                    )
                )
            complexity_offenders[fn.qualname] = min(fn.complexity, grandfathered)

    # Annotation strictness.
    annotation_offenders: list[str] = []
    baseline_annotation_set = set(baseline.annotation_missing_offenders)
    for rec in files:
        for fn in rec.functions:
            if not fn.annotation_missing_params and not fn.annotation_missing_return:
                continue
            annotation_offenders.append(fn.qualname)
            if fn.qualname in baseline_annotation_set:
                continue
            missing_parts: list[str] = []
            if fn.annotation_missing_params:
                missing_parts.append(
                    f"params [{', '.join(fn.annotation_missing_params)}]"
                )
            if fn.annotation_missing_return:
                missing_parts.append("return")
            findings.append(
                Finding(
                    rule="annotation-missing",
                    qualname=fn.qualname,
                    message=(
                        f"{fn.qualname} missing annotations: "
                        f"{'; '.join(missing_parts)}"
                    ),
                )
            )

    # Any annotation count.
    total_any = sum(rec.any_count for rec in files)
    if total_any > baseline.any_count_total:
        findings.append(
            Finding(
                rule="any-count",
                qualname="<total>",
                message=(
                    f"`Any` annotation count grew from "
                    f"{baseline.any_count_total} to {total_any}"
                ),
                value=total_any,
                baseline=baseline.any_count_total,
            )
        )

    # Duplicate function bodies.
    bodies: dict[str, list[str]] = {}
    for rec in files:
        for fn in rec.functions:
            if not fn.body_hash:
                continue
            if fn.body_statement_count < duplicate_min_statements:
                continue
            bodies.setdefault(fn.body_hash, []).append(fn.qualname)
    current_groups: list[dict[str, object]] = []
    baseline_lookup: dict[str, set[str]] = {}
    for group in baseline.duplicate_groups:
        members = set(str(m) for m in (group.get("members") or []))
        baseline_lookup[str(group.get("hash", ""))] = members
    for body_hash, members in sorted(bodies.items()):
        if len(members) < 2:
            continue
        member_set = set(members)
        current_groups.append(
            {"hash": body_hash, "members": sorted(member_set)}
        )
        baseline_members = baseline_lookup.get(body_hash)
        if baseline_members is None:
            findings.append(
                Finding(
                    rule="duplicate-functions",
                    qualname=", ".join(sorted(member_set)),
                    message=(
                        "duplicate function body group not in baseline: "
                        f"{sorted(member_set)}"
                    ),
                )
            )
            continue
        new_members = member_set - baseline_members
        if new_members:
            findings.append(
                Finding(
                    rule="duplicate-functions",
                    qualname=", ".join(sorted(new_members)),
                    message=(
                        "duplicate function body group gained new members: "
                        f"{sorted(new_members)} (existing baseline: "
                        f"{sorted(baseline_members)})"
                    ),
                )
            )

    new_baseline = Baseline(
        schema=baseline.schema,
        max_file_lines=baseline.max_file_lines,
        max_file_bytes=baseline.max_file_bytes,
        max_new_code_complexity=baseline.max_new_code_complexity,
        file_lines_offenders=file_lines_offenders,
        file_bytes_offenders=file_bytes_offenders,
        complexity_offenders=complexity_offenders,
        annotation_missing_offenders=sorted(set(annotation_offenders)),
        any_count_total=total_any,
        duplicate_groups=current_groups,
    )
    return new_baseline, findings


def _load_baseline(path: Path | None) -> Baseline:
    if path is None or not path.exists():
        return Baseline()
    return Baseline.from_dict(json.loads(path.read_text(encoding="utf-8")))


def _save_baseline(path: Path, baseline: Baseline) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(baseline.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root for relative paths and includes.",
    )
    parser.add_argument(
        "--include",
        action="append",
        help="Glob relative to --root. May be repeated.",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Exclude glob relative to --root.",
    )
    parser.add_argument(
        "--baseline",
        type=Path,
        default=None,
        help=(
            "Path to baseline JSON. Defaults to "
            "<root>/tests/support_scripts/py_signoff_baseline.json."
        ),
    )
    parser.add_argument(
        "--update-baseline",
        action="store_true",
        help="Rewrite the baseline file from current scan output.",
    )
    parser.add_argument(
        "--max-file-lines",
        type=int,
        default=None,
        help="Override baseline file-line cap.",
    )
    parser.add_argument(
        "--max-file-bytes",
        type=int,
        default=None,
        help="Override baseline file-size cap.",
    )
    parser.add_argument(
        "--max-complexity",
        type=int,
        default=None,
        help="Override new-code complexity cap.",
    )
    parser.add_argument(
        "--duplicate-min-statements",
        type=int,
        default=DEFAULT_DUPLICATE_MIN_STATEMENTS,
        help="Minimum statement count for duplicate-detection.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=200,
        help="Maximum findings printed in text mode.",
    )
    return parser.parse_args(argv)


def _print_text(
    files: list[FileRecord],
    findings: list[Finding],
    limit: int,
) -> None:
    for finding in findings[: max(0, limit)]:
        print(
            f"{finding.qualname}: {finding.severity} "
            f"[{finding.rule}] {finding.message}"
        )
    remaining = len(findings) - max(0, limit)
    if remaining > 0:
        print(f"... {remaining} more finding(s) omitted by --limit")
    print(
        f"py_signoff: {len(findings)} finding(s) across {len(files)} file(s)."
    )


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(list(argv if argv is not None else sys.argv[1:]))
    root = args.root.resolve()
    includes = list(args.include) if args.include else list(DEFAULT_INCLUDES)
    excludes = list(DEFAULT_EXCLUDES) + list(args.exclude or [])
    baseline_path: Path = (
        args.baseline or root / "tests" / "support_scripts" / "py_signoff_baseline.json"
    )
    baseline = _load_baseline(baseline_path)
    if args.max_file_lines is not None:
        baseline.max_file_lines = args.max_file_lines
    if args.max_file_bytes is not None:
        baseline.max_file_bytes = args.max_file_bytes
    if args.max_complexity is not None:
        baseline.max_new_code_complexity = args.max_complexity

    paths = _collect_files(root, includes, excludes)
    files = [_analyze_file(path, root) for path in paths]
    new_baseline, findings = _evaluate(
        files, baseline, args.duplicate_min_statements
    )

    if args.update_baseline:
        _save_baseline(baseline_path, new_baseline)
        print(
            f"py_signoff: wrote baseline to {baseline_path} "
            f"(files={len(files)}, any_total={new_baseline.any_count_total})"
        )
        return 0

    if args.format == "json":
        payload = {
            "root": root.as_posix(),
            "files": [rec.path for rec in files],
            "finding_count": len(findings),
            "findings": [
                {
                    "rule": f.rule,
                    "qualname": f.qualname,
                    "message": f.message,
                    "value": f.value,
                    "baseline": f.baseline,
                    "severity": f.severity,
                }
                for f in findings
            ],
            "any_count_total": new_baseline.any_count_total,
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        _print_text(files, findings, args.limit)

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
