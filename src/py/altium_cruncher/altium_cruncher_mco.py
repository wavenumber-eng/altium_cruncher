"""Monkey Change Order execution helpers for altium_cruncher."""

from __future__ import annotations

import json
import shutil
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path

MCO_SCHEMA = "wn.altium_cruncher.mco.v1"
JsonObject = dict[str, object]


DocumentLoader = Callable[[Path], object]
DocumentSaver = Callable[[object, Path], None]


@dataclass(slots=True)
class _CachedDocument:
    document: object
    output_file: Path
    save: DocumentSaver
    dirty: bool = False


@dataclass(slots=True)
class McoDocumentSession:
    """Run-scoped cache for CAD documents mutated by MCO operations."""

    _documents: dict[tuple[str, Path], _CachedDocument] = field(default_factory=dict)

    def open_for_mutation(
        self,
        kind: str,
        input_file: Path,
        output_file: Path,
        *,
        load: DocumentLoader,
        save: DocumentSaver,
    ) -> object:
        input_path = input_file.resolve()
        output_path = output_file.resolve()
        output_key = (kind, output_path)
        cached_output = self._documents.get(output_key)
        if cached_output is not None:
            return cached_output.document

        if input_path != output_path:
            self.flush_path(kind, input_path)

        input_key = (kind, input_path)
        cached_input = self._documents.get(input_key)
        if cached_input is not None and input_path == output_path:
            return cached_input.document

        document = load(input_path)
        self._documents[output_key] = _CachedDocument(
            document=document,
            output_file=output_path,
            save=save,
        )
        return document

    def mark_dirty(self, kind: str, output_file: Path) -> None:
        key = (kind, output_file.resolve())
        cached = self._documents.get(key)
        if cached is None:
            raise ValueError(f"MCO document is not open: {output_file}")
        cached.dirty = True

    def flush_path(self, kind: str, output_file: Path) -> None:
        cached = self._documents.get((kind, output_file.resolve()))
        if cached is not None:
            self._flush_cached(cached)

    def flush_all(self) -> None:
        for cached in self._documents.values():
            self._flush_cached(cached)

    def invalidate_paths(self, paths: Sequence[Path]) -> None:
        resolved = {path.resolve() for path in paths}
        for key in list(self._documents):
            if key[1] in resolved:
                del self._documents[key]

    def _flush_cached(self, cached: _CachedDocument) -> None:
        if not cached.dirty:
            return
        cached.output_file.parent.mkdir(parents=True, exist_ok=True)
        cached.save(cached.document, cached.output_file)
        cached.dirty = False


@dataclass(frozen=True, slots=True)
class McoExecutionContext:
    """Runtime context shared by MCO operations."""

    work_dir: Path
    dry_run: bool = False
    document_session: McoDocumentSession = field(
        default_factory=McoDocumentSession,
        compare=False,
        repr=False,
    )

    def open_document_for_mutation(
        self,
        kind: str,
        input_file: Path,
        output_file: Path,
        *,
        load: DocumentLoader,
        save: DocumentSaver,
    ) -> object:
        """Open or reuse a CAD document for this MCO run."""
        return self.document_session.open_for_mutation(
            kind,
            input_file,
            output_file,
            load=load,
            save=save,
        )

    def mark_document_dirty(self, kind: str, output_file: Path) -> None:
        """Mark a run-scoped document dirty so it is flushed on exit."""
        self.document_session.mark_dirty(kind, output_file)

    def flush_documents(self) -> None:
        """Flush all dirty run-scoped documents."""
        self.document_session.flush_all()

    def flush_document(self, kind: str, output_file: Path) -> None:
        """Flush one dirty run-scoped document, if it is open."""
        self.document_session.flush_path(kind, output_file)

    def invalidate_documents(self, paths: Sequence[Path]) -> None:
        """Forget cached documents after an operation rewrites them directly."""
        self.document_session.invalidate_paths(paths)


@dataclass(frozen=True, slots=True)
class McoOperationSpec:
    """One parsed MCO operation."""

    operation_id: str
    op: str
    args: JsonObject
    on_fail: str | None = None
    message: str | None = None


@dataclass(frozen=True, slots=True)
class McoOperationResult:
    """Result from one MCO operation."""

    operation_id: str
    op: str
    status: str
    message: str
    outputs: JsonObject
    error: str | None = None

    @property
    def is_ok(self) -> bool:
        return self.status == "ok"

    @classmethod
    def succeeded(
        cls,
        spec: McoOperationSpec,
        message: str,
        *,
        outputs: Mapping[str, object] | None = None,
    ) -> "McoOperationResult":
        return cls(
            operation_id=spec.operation_id,
            op=spec.op,
            status="ok",
            message=message,
            outputs=dict(outputs or {}),
        )

    @classmethod
    def failed(
        cls,
        spec: McoOperationSpec,
        message: str,
        *,
        error: str | None = None,
        outputs: Mapping[str, object] | None = None,
    ) -> "McoOperationResult":
        return cls(
            operation_id=spec.operation_id,
            op=spec.op,
            status="fail",
            message=message,
            outputs=dict(outputs or {}),
            error=error or message,
        )

    def to_dict(self) -> JsonObject:
        payload: JsonObject = {
            "op": self.op,
            "id": self.operation_id,
            "status": self.status,
            "message": self.message,
            "outputs": dict(self.outputs),
        }
        if self.error is not None:
            payload["error"] = self.error
        return payload


@dataclass(frozen=True, slots=True)
class McoExecutionResult:
    """Top-level MCO execution report."""

    ok: bool
    dry_run: bool
    results: tuple[McoOperationResult, ...]

    def to_dict(self) -> JsonObject:
        return {
            "schema": MCO_SCHEMA,
            "ok": self.ok,
            "dry_run": self.dry_run,
            "results": [result.to_dict() for result in self.results],
        }


McoOperationHandler = Callable[
    [McoOperationSpec, McoExecutionContext],
    McoOperationResult,
]


@dataclass(frozen=True, slots=True)
class McoOperationInfo:
    """Public metadata for one supported MCO operation."""

    name: str
    handler: McoOperationHandler
    group: str
    summary: str
    required_args: tuple[str, ...] = ()
    optional_args: tuple[str, ...] = ()
    aliases: tuple[str, ...] = ()

    def to_dict(self) -> JsonObject:
        payload: JsonObject = {
            "op": self.name,
            "group": self.group,
            "summary": self.summary,
            "required_args": list(self.required_args),
            "optional_args": list(self.optional_args),
        }
        if self.aliases:
            payload["aliases"] = list(self.aliases)
        return payload


def mco_operation(
    op: str,
    operation_id: str,
    message: str,
    args: Mapping[str, object] | None = None,
    *,
    on_fail: str | None = None,
) -> JsonObject:
    """Build an MCO operation object using the canonical field order."""
    payload: JsonObject = {
        "op": op,
        "id": operation_id,
        "message": message,
        "args": dict(args or {}),
    }
    if on_fail is not None:
        payload["on_fail"] = on_fail
    return payload


def strip_jsonc_comments(text: str) -> str:
    """Remove JSONC comments while preserving quoted string contents."""
    output: list[str] = []
    index = 0
    in_string = False
    escaped = False
    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""
        if in_string:
            output.append(char)
            escaped, in_string = _jsonc_string_state(char, escaped, in_string)
            index += 1
            continue
        if char == '"':
            in_string = True
            output.append(char)
            index += 1
            continue
        if char == "/" and next_char == "/":
            index = _skip_line_comment(text, index + 2)
            continue
        if char == "/" and next_char == "*":
            index = _skip_block_comment(text, index + 2)
            continue
        output.append(char)
        index += 1
    return "".join(output)


def strip_jsonc_trailing_commas(text: str) -> str:
    """Remove trailing object/array commas outside quoted strings."""
    output: list[str] = []
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            output.append(char)
            escaped, in_string = _jsonc_string_state(char, escaped, in_string)
            continue
        if char == '"':
            in_string = True
            output.append(char)
            continue
        if char in "]}":
            _drop_trailing_comma(output)
        output.append(char)
    return "".join(output)


def loads_jsonc(text: str) -> object:
    """Load JSON with comments and trailing commas."""
    without_comments = strip_jsonc_comments(text)
    normalized = strip_jsonc_trailing_commas(without_comments)
    return json.loads(normalized)


def load_jsonc_file(path: Path | str) -> object:
    """Load a JSONC file from disk."""
    input_path = Path(path)
    return loads_jsonc(input_path.read_text(encoding="utf-8-sig"))


def parse_mco_operations(payload: object) -> list[McoOperationSpec]:
    """Parse a root MCO document or raw operation array."""
    raw_operations = _raw_operation_items(payload)
    operations = [
        _parse_mco_operation(raw_operation, index)
        for index, raw_operation in enumerate(raw_operations, start=1)
    ]
    _validate_operation_ids(operations)
    return operations


def execute_mco_file(
    path: Path | str,
    *,
    dry_run: bool = False,
    registry: Mapping[str, McoOperationHandler] | None = None,
) -> McoExecutionResult:
    """Load and execute an MCO file."""
    input_path = Path(path).resolve()
    context = McoExecutionContext(work_dir=input_path.parent, dry_run=dry_run)
    return execute_mco(load_jsonc_file(input_path), context, registry=registry)


def execute_mco(
    payload: object,
    context: McoExecutionContext,
    *,
    registry: Mapping[str, McoOperationHandler] | None = None,
) -> McoExecutionResult:
    """Execute an already-loaded MCO payload."""
    operations = parse_mco_operations(payload)
    handlers = dict(DEFAULT_MCO_OPERATIONS)
    if registry is not None:
        handlers.update(registry)
    result = _execute_operations(operations, context, handlers)
    return _flush_context_documents(context, result)


def available_mco_operations() -> list[str]:
    """Return the registered public MCO operation names."""
    return [info.name for info in mco_operation_catalog()]


def mco_operation_catalog() -> tuple[McoOperationInfo, ...]:
    """Return public MCO operations with metadata."""
    return tuple(
        sorted(
            DEFAULT_MCO_OPERATION_INFO.values(),
            key=lambda info: (info.group, info.name),
        )
    )


def write_mco_template(path: Path | str, *, overwrite: bool = False) -> Path:
    """Write an editable JSONC MCO template."""
    output_path = Path(path)
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"MCO file already exists: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(_mco_template_text(), encoding="utf-8")
    return output_path.resolve()


def _jsonc_string_state(
    char: str,
    escaped: bool,
    in_string: bool,
) -> tuple[bool, bool]:
    if escaped:
        return (False, in_string)
    if char == "\\":
        return (True, in_string)
    if char == '"':
        return (False, False)
    return (False, in_string)


def _skip_line_comment(text: str, index: int) -> int:
    while index < len(text) and text[index] not in "\r\n":
        index += 1
    return index


def _skip_block_comment(text: str, index: int) -> int:
    while index + 1 < len(text):
        if text[index] == "*" and text[index + 1] == "/":
            return index + 2
        index += 1
    return len(text)


def _drop_trailing_comma(output: list[str]) -> None:
    index = len(output) - 1
    while index >= 0 and output[index].isspace():
        index -= 1
    if index >= 0 and output[index] == ",":
        del output[index]


def _raw_operation_items(payload: object) -> list[object]:
    if isinstance(payload, list):
        return list(payload)
    root = _json_object(payload, "MCO root")
    schema = root.get("schema")
    if schema not in {None, MCO_SCHEMA}:
        raise ValueError(f"Unsupported MCO schema: {schema!r}")
    raw_operations = root.get("operations")
    if not isinstance(raw_operations, list):
        raise ValueError("MCO document must contain an operations array")
    return list(raw_operations)


def _parse_mco_operation(payload: object, index: int) -> McoOperationSpec:
    raw = _json_object(payload, f"MCO operation {index}")
    op = _required_string(raw, "op", f"MCO operation {index}")
    operation_id = _optional_string(raw, "id", f"op{index}") or f"op{index}"
    args = raw.get("args", {})
    message = _optional_string(raw, "message", None)
    on_fail = _optional_string(raw, "on_fail", None)
    return McoOperationSpec(
        operation_id=operation_id,
        op=op,
        args=_json_object(args, f"MCO operation {operation_id} args"),
        on_fail=on_fail,
        message=message,
    )


def _validate_operation_ids(operations: Sequence[McoOperationSpec]) -> None:
    seen: set[str] = set()
    for operation in operations:
        if operation.operation_id in seen:
            raise ValueError(f"Duplicate MCO operation id: {operation.operation_id}")
        seen.add(operation.operation_id)


def _execute_operations(
    operations: Sequence[McoOperationSpec],
    context: McoExecutionContext,
    handlers: Mapping[str, McoOperationHandler],
) -> McoExecutionResult:
    results: list[McoOperationResult] = []
    index_by_id = {
        operation.operation_id: index for index, operation in enumerate(operations)
    }
    index = 0
    steps = 0
    while index < len(operations):
        steps += 1
        if steps > len(operations):
            return _control_flow_result(context, results, "MCO on_fail loop detected")
        operation = operations[index]
        result = _run_operation(operation, context, handlers)
        results.append(result)
        if result.is_ok:
            index += 1
            continue
        if operation.on_fail is None:
            return McoExecutionResult(False, context.dry_run, tuple(results))
        if operation.on_fail not in index_by_id:
            message = f"MCO on_fail target not found: {operation.on_fail}"
            return _control_flow_result(context, results, message)
        index = index_by_id[operation.on_fail]
    return McoExecutionResult(True, context.dry_run, tuple(results))


def _control_flow_result(
    context: McoExecutionContext,
    results: list[McoOperationResult],
    message: str,
) -> McoExecutionResult:
    spec = McoOperationSpec("mco-control-flow", "mco.control-flow", {})
    results.append(McoOperationResult.failed(spec, message))
    return McoExecutionResult(False, context.dry_run, tuple(results))


def _flush_context_documents(
    context: McoExecutionContext,
    result: McoExecutionResult,
) -> McoExecutionResult:
    if context.dry_run:
        return result
    try:
        context.flush_documents()
    except Exception as exc:
        spec = McoOperationSpec("mco-flush", "mco.flush", {})
        flush_result = McoOperationResult.failed(
            spec,
            "MCO document flush failed",
            error=str(exc),
        )
        return McoExecutionResult(
            False,
            result.dry_run,
            (*result.results, flush_result),
        )
    return result


def _run_operation(
    spec: McoOperationSpec,
    context: McoExecutionContext,
    handlers: Mapping[str, McoOperationHandler],
) -> McoOperationResult:
    handler = handlers.get(spec.op)
    if handler is None:
        return McoOperationResult.failed(spec, f"Unknown MCO operation: {spec.op}")
    try:
        return handler(spec, context)
    except Exception as exc:
        return McoOperationResult.failed(
            spec,
            f"MCO operation failed: {spec.operation_id}",
            error=str(exc),
        )


def _op_message(
    spec: McoOperationSpec,
    _context: McoExecutionContext,
) -> McoOperationResult:
    text = _optional_string(spec.args, "text", spec.message or "")
    return McoOperationResult.succeeded(spec, text or "message")


def _op_fail(
    spec: McoOperationSpec,
    _context: McoExecutionContext,
) -> McoOperationResult:
    text = (
        _optional_string(spec.args, "message", spec.message or "requested failure")
        or "requested failure"
    )
    return McoOperationResult.failed(spec, text)


def _op_project_create(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    file_path = _required_path(spec.args, "file", context)
    project_name = (
        _optional_string(spec.args, "name", None)
        or _optional_string(spec.args, "project_name", None)
        or file_path.stem
    )
    overwrite = _optional_bool(spec.args, "overwrite", False)
    if file_path.exists() and not overwrite:
        return McoOperationResult.failed(spec, f"Output already exists: {file_path}")
    outputs = {"project": str(file_path.resolve())}
    if context.dry_run:
        return McoOperationResult.succeeded(
            spec,
            spec.message or "project create dry run",
            outputs=outputs,
        )

    from altium_monkey.altium_prjpcb import AltiumPrjPcb

    context.invalidate_documents([file_path])
    file_path.parent.mkdir(parents=True, exist_ok=True)
    AltiumPrjPcb.create_minimal(project_name).save(file_path)
    context.invalidate_documents([file_path])
    return McoOperationResult.succeeded(
        spec,
        spec.message or "created project",
        outputs=outputs,
    )


def _op_project_add_document(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    project_file = _required_path(spec.args, "file", context)
    document = _required_string(spec.args, "document", spec.op)
    unique_id = _optional_string(spec.args, "unique_id", None)
    normalized = document.replace("/", "\\")
    if context.dry_run:
        return McoOperationResult.succeeded(
            spec,
            spec.message or f"add project document dry run: {document}",
            outputs={"project": str(project_file), "document": normalized},
        )
    project = _open_project_for_mutation(project_file, context)
    for existing in getattr(project, "documents", []):
        if str(existing.get("path", "")).lower() == normalized.lower():
            return McoOperationResult.succeeded(
                spec,
                spec.message or f"project document already present: {document}",
                outputs={"project": str(project_file), "document": normalized},
            )

    from altium_monkey.altium_prjpcb_builder import AltiumPrjPcbDocumentEntry

    if not context.dry_run:
        entry = AltiumPrjPcbDocumentEntry.create(
            normalized,
            unique_id=unique_id,
        )
        project.documents.append(
            {
                "path": entry.path,
                "unique_id": entry.unique_id,
                "options": list(entry.options)
                if entry.options
                else [
                    ("DocumentPath", entry.path),
                    ("DocumentUniqueId", entry.unique_id),
                ],
            }
        )
        context.mark_document_dirty("prjpcb", project_file)
    return McoOperationResult.succeeded(
        spec,
        spec.message or f"added project document {document}",
        outputs={"project": str(project_file), "document": normalized},
    )


def _op_project_add_parameter(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    project_file = _required_path(spec.args, "file", context)
    name = _required_string(spec.args, "name", spec.op)
    value = _required_string(spec.args, "value", spec.op)
    if context.dry_run:
        return McoOperationResult.succeeded(
            spec,
            spec.message or f"add project parameter dry run: {name}",
            outputs={"project": str(project_file), "name": name},
        )
    project = _open_project_for_mutation(project_file, context)
    project.set_parameter(name, value)
    context.mark_document_dirty("prjpcb", project_file)
    return McoOperationResult.succeeded(
        spec,
        spec.message or f"added project parameter {name}",
        outputs={"project": str(project_file), "name": name},
    )


def _op_project_add_variant(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    project_file = _required_path(spec.args, "file", context)
    name = _required_string(spec.args, "name", spec.op)
    unique_id = _optional_string(spec.args, "unique_id", None)
    allow_fabrication = _optional_bool(spec.args, "allow_fabrication", True)
    current = _optional_bool(spec.args, "current", False)
    if context.dry_run:
        return McoOperationResult.succeeded(
            spec,
            spec.message or f"add project variant dry run: {name}",
            outputs={"project": str(project_file), "name": name},
        )
    project = _open_project_for_mutation(project_file, context)
    project.add_variant(
        name,
        unique_id=unique_id,
        allow_fabrication=allow_fabrication,
        current=current,
    )
    context.mark_document_dirty("prjpcb", project_file)
    return McoOperationResult.succeeded(
        spec,
        spec.message or f"added project variant {name}",
        outputs={"project": str(project_file), "name": name},
    )


def _op_project_list_variants(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    project_file = _required_path(spec.args, "file", context)
    if not context.dry_run:
        context.flush_document("prjpcb", project_file)

    from altium_cruncher.altium_cruncher_prjpcb_variants import (
        summarize_project_variants,
    )

    outputs = summarize_project_variants(project_file)
    return McoOperationResult.succeeded(
        spec,
        spec.message or "listed project variants",
        outputs=outputs,
    )


def _op_project_delete_variant(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    project_file = _required_path(spec.args, "file", context)
    name = _required_string(spec.args, "name", spec.op)
    project = _project_for_variant_mutation(project_file, context)

    from altium_cruncher.altium_cruncher_prjpcb_variants import (
        delete_project_variant,
    )

    outputs = {
        "project": str(project_file),
        **delete_project_variant(project, name),
    }
    if not context.dry_run:
        context.mark_document_dirty("prjpcb", project_file)
    return McoOperationResult.succeeded(
        spec,
        spec.message or f"deleted project variant {name}",
        outputs=outputs,
    )


def _op_project_rename_variant(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    project_file = _required_path(spec.args, "file", context)
    name = _required_string(spec.args, "name", spec.op)
    new_name = _required_string(spec.args, "new_name", spec.op)
    project = _project_for_variant_mutation(project_file, context)

    from altium_cruncher.altium_cruncher_prjpcb_variants import (
        rename_project_variant,
    )

    outputs = {
        "project": str(project_file),
        **rename_project_variant(project, name, new_name),
    }
    if not context.dry_run:
        context.mark_document_dirty("prjpcb", project_file)
    return McoOperationResult.succeeded(
        spec,
        spec.message or f"renamed project variant {name} to {new_name}",
        outputs=outputs,
    )


def _op_project_clone_variant(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    project_file = _required_path(spec.args, "file", context)
    source_name = _required_string(spec.args, "source_name", spec.op)
    name = _required_string(spec.args, "name", spec.op)
    unique_id = _optional_string(spec.args, "unique_id", None)
    allow_fabrication = _optional_bool_or_none(spec.args, "allow_fabrication")
    current = _optional_bool(spec.args, "current", False)
    project = _project_for_variant_mutation(project_file, context)

    from altium_cruncher.altium_cruncher_prjpcb_variants import (
        clone_project_variant,
    )

    outputs = {
        "project": str(project_file),
        **clone_project_variant(
            project,
            source_name,
            name,
            unique_id=unique_id,
            allow_fabrication=allow_fabrication,
            current=current,
        ),
    }
    if not context.dry_run:
        context.mark_document_dirty("prjpcb", project_file)
    return McoOperationResult.succeeded(
        spec,
        spec.message or f"cloned project variant {source_name} to {name}",
        outputs=outputs,
    )


def _op_project_add_variant_dnp(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    project_file = _required_path(spec.args, "file", context)
    variant = _required_string(spec.args, "variant", spec.op)
    designator = _required_string(spec.args, "designator", spec.op)
    unique_id = _optional_string(spec.args, "unique_id", None)
    alternate_part = _optional_string(spec.args, "alternate_part", "") or ""
    project = _project_for_variant_mutation(project_file, context)

    from altium_cruncher.altium_cruncher_prjpcb_variants import (
        add_project_variant_dnp,
    )

    outputs = {
        "project": str(project_file),
        **add_project_variant_dnp(
            project,
            project_file,
            variant=variant,
            designator=designator,
            unique_id=unique_id,
            alternate_part=alternate_part,
        ),
    }
    if not context.dry_run:
        context.mark_document_dirty("prjpcb", project_file)
    return McoOperationResult.succeeded(
        spec,
        spec.message or f"added DNP {designator} to project variant {variant}",
        outputs=outputs,
    )


def _op_project_toggle_variant_dnp(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    project_file = _required_path(spec.args, "file", context)
    variant = _required_string(spec.args, "variant", spec.op)
    designator = _required_string(spec.args, "designator", spec.op)
    unique_id = _optional_string(spec.args, "unique_id", None)
    alternate_part = _optional_string(spec.args, "alternate_part", "") or ""
    project = _project_for_variant_mutation(project_file, context)

    from altium_cruncher.altium_cruncher_prjpcb_variants import (
        toggle_project_variant_dnp,
    )

    outputs = {
        "project": str(project_file),
        **toggle_project_variant_dnp(
            project,
            project_file,
            variant=variant,
            designator=designator,
            unique_id=unique_id,
            alternate_part=alternate_part,
        ),
    }
    if not context.dry_run:
        context.mark_document_dirty("prjpcb", project_file)
    action = "marked DNP" if outputs.get("dnp") else "reverted to fitted"
    return McoOperationResult.succeeded(
        spec,
        spec.message or f"{action} {designator} in project variant {variant}",
        outputs=outputs,
    )


def _op_schdoc_create(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    file_path = _required_path(spec.args, "file", context)
    overwrite = _optional_bool(spec.args, "overwrite", False)
    if file_path.exists() and not overwrite:
        return McoOperationResult.failed(spec, f"Output already exists: {file_path}")
    outputs = {"schematic": str(file_path.resolve())}
    if context.dry_run:
        return McoOperationResult.succeeded(
            spec,
            spec.message or "schematic create dry run",
            outputs=outputs,
        )

    from altium_monkey import AltiumSchDoc

    context.invalidate_documents([file_path])
    schdoc = AltiumSchDoc()
    _apply_project_skeleton_schematic_sheet_style(
        schdoc,
        _optional_string(spec.args, "sheet_style", None),
    )
    file_path.parent.mkdir(parents=True, exist_ok=True)
    schdoc.save(file_path)
    context.invalidate_documents([file_path])
    return McoOperationResult.succeeded(
        spec,
        spec.message or "created schematic",
        outputs=outputs,
    )


def _op_pcbdoc_create(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    file_path = _required_path(spec.args, "file", context)
    overwrite = _optional_bool(spec.args, "overwrite", False)
    if file_path.exists() and not overwrite:
        return McoOperationResult.failed(spec, f"Output already exists: {file_path}")
    outputs = {"board": str(file_path.resolve())}
    if context.dry_run:
        return McoOperationResult.succeeded(
            spec,
            spec.message or "board create dry run",
            outputs=outputs,
        )

    from altium_monkey import PcbDocBuilder

    context.invalidate_documents([file_path])
    builder = PcbDocBuilder()
    layer_stack_template = _optional_string(spec.args, "layer_stack_template", None)
    if layer_stack_template is not None:
        builder.set_layer_stack_template(layer_stack_template)
    board_outline_mils = _optional_number_object(
        spec.args,
        "board_outline_mils",
        ("left", "bottom", "right", "top"),
    )
    if board_outline_mils is not None:
        builder.set_outline_rectangle_mils(*board_outline_mils)
    sheet_frame_mils = _optional_number_object(
        spec.args,
        "sheet_frame_mils",
        ("x", "y", "width", "height"),
    )
    if sheet_frame_mils is not None:
        builder.set_sheet_frame_mils(*sheet_frame_mils)
    board_origin_mils = _optional_number_object(spec.args, "board_origin_mils", ("x", "y"))
    if board_origin_mils is not None:
        builder.set_origin_mils(*board_origin_mils)
    else:
        builder.set_origin_to_outline_lower_left()
    builder.set_current_view_state("2D")
    builder.set_2d_current_layer("TOP")
    builder.save(file_path)
    context.invalidate_documents([file_path])
    return McoOperationResult.succeeded(
        spec,
        spec.message or "created board",
        outputs=outputs,
    )


def _open_project_for_mutation(
    project_file: Path,
    context: McoExecutionContext,
) -> object:
    from altium_monkey.altium_prjpcb import AltiumPrjPcb

    return context.open_document_for_mutation(
        "prjpcb",
        project_file,
        project_file,
        load=lambda path: AltiumPrjPcb(path),
        save=lambda document, path: document.save(path),
    )


def _project_for_variant_mutation(
    project_file: Path,
    context: McoExecutionContext,
) -> object:
    if not context.dry_run:
        return _open_project_for_mutation(project_file, context)

    from altium_monkey.altium_prjpcb import AltiumPrjPcb

    return AltiumPrjPcb(project_file)


def _apply_project_skeleton_schematic_sheet_style(
    schdoc: object,
    sheet_style: str | None,
) -> None:
    if sheet_style is None:
        return

    from altium_monkey import SheetStyle

    sheet = getattr(schdoc, "sheet", None)
    if sheet is None:
        raise ValueError("Schematic document has no sheet record")
    normalized = sheet_style.strip().replace(" ", "_").replace("-", "_").upper()
    if normalized in SheetStyle.__members__:
        style = SheetStyle[normalized]
    else:
        style = SheetStyle(int(sheet_style))
    sheet.sheet_style = int(style)
    sheet.use_custom_sheet = False


def _op_copy_file(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    source = _required_path(spec.args, "source", context)
    destination = _required_path(spec.args, "destination", context)
    overwrite = _optional_bool(spec.args, "overwrite", False)
    if not source.exists():
        return McoOperationResult.failed(spec, f"Source file not found: {source}")
    if not source.is_file():
        return McoOperationResult.failed(spec, f"Source is not a file: {source}")
    same_file = destination.resolve() == source.resolve()
    if destination.exists() and not same_file and not overwrite:
        return McoOperationResult.failed(
            spec,
            f"Destination already exists: {destination}",
        )
    outputs = {
        "source": str(source.resolve()),
        "destination": str(destination.resolve()),
    }
    if context.dry_run:
        return McoOperationResult.succeeded(
            spec,
            spec.message or "file copy dry run",
            outputs=outputs,
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not same_file:
        shutil.copy2(source, destination)
    return McoOperationResult.succeeded(
        spec,
        spec.message or f"copied {source.name}",
        outputs=outputs,
    )


def _json_object(value: object, label: str) -> JsonObject:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return dict(value)


def _required_string(args: Mapping[str, object], name: str, label: str) -> str:
    value = args.get(name)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} field {name!r} must be a non-empty string")
    return value


def _optional_string(
    args: Mapping[str, object],
    name: str,
    default: str | None,
) -> str | None:
    value = args.get(name)
    if value is None:
        return default
    if not isinstance(value, str):
        raise ValueError(f"Field {name!r} must be a string")
    return value


def _optional_bool(
    args: Mapping[str, object],
    name: str,
    default: bool,
) -> bool:
    value = args.get(name)
    if value is None:
        return default
    if not isinstance(value, bool):
        raise ValueError(f"Field {name!r} must be a boolean")
    return value


def _optional_bool_or_none(
    args: Mapping[str, object],
    name: str,
) -> bool | None:
    value = args.get(name)
    if value is None:
        return None
    if not isinstance(value, bool):
        raise ValueError(f"Field {name!r} must be a boolean")
    return value


def _required_path(
    args: Mapping[str, object],
    name: str,
    context: McoExecutionContext,
) -> Path:
    raw_path = Path(_required_string(args, name, "file.copy"))
    if raw_path.is_absolute():
        return raw_path.resolve()
    return (context.work_dir / raw_path).resolve()


def _optional_number_object(
    args: Mapping[str, object],
    name: str,
    fields: Sequence[str],
) -> tuple[float, ...] | None:
    value = args.get(name)
    if value is None:
        return None
    raw = _json_object(value, name)
    numbers: list[float] = []
    for field_name in fields:
        field_value = raw.get(field_name)
        if not isinstance(field_value, int | float):
            raise ValueError(f"Field {name}.{field_name} must be numeric")
        numbers.append(float(field_value))
    return tuple(numbers)


def _mco_template_text() -> str:
    return (
        "{\n"
        f'  "schema": "{MCO_SCHEMA}",\n'
        "  // MCO operations execute in order. Use on_fail to jump to another id.\n"
        '  "operations": [\n'
        "    {\n"
        '      "op": "project.create",\n'
        '      "id": "create_project",\n'
        '      "message": "Create a blank Altium project",\n'
        '      "args": {\n'
        '        "file": "output/mate/mate.PrjPcb",\n'
        '        "name": "mate",\n'
        '        "overwrite": false\n'
        "      }\n"
        "    },\n"
        "    {\n"
        '      "op": "schdoc.create",\n'
        '      "id": "create_schematic",\n'
        '      "message": "Create a blank schematic",\n'
        '      "args": {\n'
        '        "file": "output/mate/mate.SchDoc",\n'
        '        "sheet_style": "D",\n'
        '        "overwrite": false\n'
        "      }\n"
        "    },\n"
        "    {\n"
        '      "op": "pcbdoc.create",\n'
        '      "id": "create_board",\n'
        '      "message": "Create a blank board",\n'
        '      "args": {\n'
        '        "file": "output/mate/mate.PcbDoc",\n'
        '        "layer_stack_template": "2-layer",\n'
        '        "overwrite": false,\n'
        '        "board_outline_mils": {\n'
        '          "left": 0,\n'
        '          "bottom": 0,\n'
        '          "right": 3000,\n'
        '          "top": 2000,\n'
        "        }\n"
        "      }\n"
        "    },\n"
        "    {\n"
        '      "op": "project.add_document",\n'
        '      "id": "add_schematic_to_project",\n'
        '      "message": "Add schematic to project",\n'
        '      "args": {\n'
        '        "file": "output/mate/mate.PrjPcb",\n'
        '        "document": "mate.SchDoc"\n'
        "      }\n"
        "    },\n"
        "    {\n"
        '      "op": "project.add_document",\n'
        '      "id": "add_board_to_project",\n'
        '      "message": "Add board to project",\n'
        '      "args": {\n'
        '        "file": "output/mate/mate.PrjPcb",\n'
        '        "document": "mate.PcbDoc"\n'
        "      }\n"
        "    }\n"
        "  ]\n"
        "}\n"
    )


def _default_mco_operation_info() -> dict[str, McoOperationInfo]:
    from altium_cruncher.altium_cruncher_mco_cad_ops import CAD_MCO_OPERATIONS

    cad = CAD_MCO_OPERATIONS
    infos = [
        McoOperationInfo(
            "mco.message",
            _op_message,
            "mco",
            "Emit a human-readable message.",
            optional_args=("text",),
        ),
        McoOperationInfo(
            "mco.fail",
            _op_fail,
            "mco",
            "Fail intentionally, usually for control-flow tests.",
            optional_args=("message",),
        ),
        McoOperationInfo(
            "file.copy",
            _op_copy_file,
            "file",
            "Copy one file into the workflow output tree.",
            required_args=("source", "destination"),
            optional_args=("overwrite",),
        ),
        McoOperationInfo(
            "project.create",
            _op_project_create,
            "project",
            "Create an empty .PrjPcb file.",
            required_args=("file",),
            optional_args=("name", "project_name", "overwrite"),
        ),
        McoOperationInfo(
            "project.add_document",
            _op_project_add_document,
            "project",
            "Append a document entry to a .PrjPcb file.",
            required_args=("file", "document"),
            optional_args=("unique_id",),
        ),
        McoOperationInfo(
            "project.add_parameter",
            _op_project_add_parameter,
            "project",
            "Set one project parameter.",
            required_args=("file", "name", "value"),
        ),
        McoOperationInfo(
            "project.add_variant",
            _op_project_add_variant,
            "project",
            "Add one project variant.",
            required_args=("file", "name"),
            optional_args=("unique_id", "allow_fabrication", "current"),
        ),
        McoOperationInfo(
            "project.add_variant_dnp",
            _op_project_add_variant_dnp,
            "project",
            "Mark one designator Not Fitted in a project variant.",
            required_args=("file", "variant", "designator"),
            optional_args=("unique_id", "alternate_part"),
        ),
        McoOperationInfo(
            "project.toggle_variant_dnp",
            _op_project_toggle_variant_dnp,
            "project",
            "Toggle one designator between fitted and Not Fitted in a project variant.",
            required_args=("file", "variant", "designator"),
            optional_args=("unique_id", "alternate_part"),
        ),
        McoOperationInfo(
            "project.clone_variant",
            _op_project_clone_variant,
            "project",
            "Clone an existing project variant under a new name.",
            required_args=("file", "source_name", "name"),
            optional_args=("unique_id", "allow_fabrication", "current"),
        ),
        McoOperationInfo(
            "project.delete_variant",
            _op_project_delete_variant,
            "project",
            "Delete one project variant.",
            required_args=("file", "name"),
        ),
        McoOperationInfo(
            "project.list_variants",
            _op_project_list_variants,
            "project",
            "List project variants, DNP rows, and parameter changes.",
            required_args=("file",),
        ),
        McoOperationInfo(
            "project.rename_variant",
            _op_project_rename_variant,
            "project",
            "Rename one project variant.",
            required_args=("file", "name", "new_name"),
        ),
        McoOperationInfo(
            "schdoc.create",
            _op_schdoc_create,
            "schdoc",
            "Create an empty schematic document.",
            required_args=("file",),
            optional_args=("sheet_style", "overwrite"),
        ),
        McoOperationInfo(
            "pcbdoc.create",
            _op_pcbdoc_create,
            "pcbdoc",
            "Create an empty PCB document.",
            required_args=("file",),
            optional_args=(
                "layer_stack_template",
                "board_outline_mils",
                "board_origin_mils",
                "sheet_frame_mils",
                "overwrite",
            ),
        ),
        McoOperationInfo(
            "schdoc.add_wire",
            cad["schdoc.add-wire"],
            "schdoc",
            "Add a schematic wire.",
            required_args=("file", "points_mils"),
            optional_args=("overwrite",),
        ),
        McoOperationInfo(
            "schdoc.add_net_label",
            cad["schdoc.add-net-label"],
            "schdoc",
            "Add a schematic net label.",
            required_args=("file", "text", "location_mils"),
            optional_args=("orientation", "overwrite"),
        ),
        McoOperationInfo(
            "schdoc.add_component",
            cad["schdoc.add-component"],
            "schdoc",
            "Insert a schematic component from a SchLib.",
            required_args=("file", "library", "symbol", "designator", "position_mils"),
            optional_args=(
                "unique_id",
                "design_item_id",
                "footprint_model",
                "footprint_library",
                "parameters",
                "designator_style",
                "overwrite",
            ),
        ),
        McoOperationInfo(
            "pcbdoc.add_text",
            cad["pcbdoc.add-text"],
            "pcbdoc",
            "Add PCB text.",
            required_args=("file", "text", "position_mils"),
            optional_args=(
                "layer",
                "height_mils",
                "font_kind",
                "font_name",
                "bold",
                "italic",
                "inverted_box",
                "overwrite",
            ),
        ),
        McoOperationInfo(
            "pcbdoc.add_component",
            cad["pcbdoc.add-component"],
            "pcbdoc",
            "Insert a PCB component from a PcbLib.",
            required_args=("file", "library", "footprint", "designator", "position_mils"),
            optional_args=(
                "layer",
                "source_unique_id",
                "source_hierarchical_path",
                "source_component_library",
                "source_lib_reference",
                "source_description",
                "channel_offset",
                "comment_text",
                "component_parameters",
                "pad_nets",
                "overwrite",
            ),
        ),
        McoOperationInfo(
            "pcbdoc.arrange_designators",
            cad["pcbdoc.arrange-designators"],
            "pcbdoc",
            "Position generated PCB designator text.",
            required_args=("file", "designators"),
            optional_args=("placement", "offset_mils", "height_mils", "layer", "overwrite"),
        ),
        McoOperationInfo(
            "pcbdoc.add_track",
            cad["pcbdoc.add-track"],
            "pcbdoc",
            "Add a PCB track.",
            required_args=("file", "start_mils", "end_mils", "width_mils"),
            optional_args=("layer", "net", "overwrite"),
        ),
        McoOperationInfo(
            "pcbdoc.add_arc",
            cad["pcbdoc.add-arc"],
            "pcbdoc",
            "Add a PCB arc.",
            required_args=(
                "file",
                "center_mils",
                "radius_mils",
                "start_angle_degrees",
                "end_angle_degrees",
                "width_mils",
            ),
            optional_args=("layer", "net", "overwrite"),
        ),
        McoOperationInfo(
            "pcbdoc.add_pad",
            cad["pcbdoc.add-pad"],
            "pcbdoc",
            "Add a free PCB pad.",
            required_args=("file", "designator", "position_mils", "width_mils", "height_mils"),
            optional_args=(
                "shape",
                "rotation_degrees",
                "hole_size_mils",
                "plated",
                "layer",
                "net",
                "solder_mask_expansion_mils",
                "paste_mask_expansion_mils",
                "tenting_top",
                "tenting_bottom",
                "solder_mask_expansion_mode",
                "paste_mask_expansion_mode",
                "overwrite",
            ),
        ),
        McoOperationInfo(
            "pcbdoc.add_via",
            cad["pcbdoc.add-via"],
            "pcbdoc",
            "Add a PCB via.",
            required_args=("file", "position_mils", "diameter_mils", "hole_size_mils"),
            optional_args=("layer_start", "layer_end", "net", "overwrite"),
        ),
        McoOperationInfo(
            "pcbdoc.add_fill",
            cad["pcbdoc.add-fill"],
            "pcbdoc",
            "Add a rectangular PCB fill.",
            required_args=("file", "corner1_mils", "corner2_mils"),
            optional_args=("rotation_degrees", "layer", "net", "overwrite"),
        ),
        McoOperationInfo(
            "pcbdoc.add_region",
            cad["pcbdoc.add-region"],
            "pcbdoc",
            "Add a PCB region.",
            required_args=("file", "outline_points_mils"),
            optional_args=(
                "layer",
                "hole_points_mils",
                "is_keepout",
                "keepout_restrictions",
                "net",
                "is_board_cutout",
                "overwrite",
            ),
        ),
        McoOperationInfo(
            "pcbdoc.create_user_union",
            cad["pcbdoc.create-user-union"],
            "pcbdoc",
            "Create a user union over generated PCB objects.",
            required_args=("file", "name"),
            optional_args=("members", "overwrite"),
        ),
        McoOperationInfo(
            "pcbdoc.export_layer_step",
            cad["pcbdoc.export-layer-step"],
            "pcbdoc",
            "Export a PCB layer STEP artifact.",
            required_args=("file", "output_file", "layer"),
            optional_args=("board_name", "z_mm", "highlights", "colors", "overwrite"),
        ),
        McoOperationInfo(
            "pcbdoc.add_embedded_3d_model",
            cad["pcbdoc.add-embedded-3d-model"],
            "pcbdoc",
            "Embed a 3D model in a PCB document.",
            required_args=("file", "model_file"),
            optional_args=(
                "model_name",
                "name",
                "layer",
                "side",
                "location_mils",
                "rotation_x_degrees",
                "rotation_y_degrees",
                "rotation_z_degrees",
                "z_mm",
                "bounds_mils",
                "projection_outline_mils",
                "overall_height_mils",
                "opacity",
                "overwrite",
            ),
        ),
    ]
    return {info.name: info for info in infos}


def _default_mco_operations(
    infos: Mapping[str, McoOperationInfo],
) -> dict[str, McoOperationHandler]:
    handlers = {info.name: info.handler for info in infos.values()}
    handlers["message"] = _op_message
    handlers["fail"] = _op_fail
    return handlers


DEFAULT_MCO_OPERATION_INFO: dict[str, McoOperationInfo] = _default_mco_operation_info()
DEFAULT_MCO_OPERATIONS: dict[str, McoOperationHandler] = _default_mco_operations(
    DEFAULT_MCO_OPERATION_INFO
)
