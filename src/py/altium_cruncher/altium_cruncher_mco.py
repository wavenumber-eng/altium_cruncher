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
            "id": self.operation_id,
            "op": self.op,
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
class ProjectSkeletonArgs:
    """Validated arguments for project.create-skeleton."""

    output_dir: Path
    project_name: str
    schematic_filename: str | None
    board_filename: str | None
    project_filename: str | None
    layer_stack_template: str
    overwrite: bool
    board_outline_mils: tuple[float, ...] | None
    sheet_frame_mils: tuple[float, ...] | None
    documents: tuple[str, ...]


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
    return sorted(DEFAULT_MCO_OPERATIONS)


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
    operation_id = _optional_string(raw, "id", f"op{index}")
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
    text = _optional_string(spec.args, "message", spec.message or "requested failure")
    return McoOperationResult.failed(spec, text)


def _op_create_project_skeleton(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    options = _parse_project_skeleton_args(spec.args, context)
    output_paths = _project_skeleton_output_paths(options)
    existing = [path for path in output_paths.values() if path.exists()]
    if existing and not options.overwrite:
        paths = ", ".join(str(path) for path in existing)
        return McoOperationResult.failed(spec, f"Output already exists: {paths}")
    if context.dry_run:
        return McoOperationResult.succeeded(
            spec,
            spec.message or "project skeleton dry run",
            outputs=_stringified_paths(output_paths),
        )

    from altium_monkey.altium_project_bootstrap_builder import ProjectBootstrapBuilder

    context.invalidate_documents(list(output_paths.values()))
    builder = ProjectBootstrapBuilder(
        options.project_name,
        schematic_filename=options.schematic_filename,
        board_filename=options.board_filename,
        project_filename=options.project_filename,
        layer_stack_template=options.layer_stack_template,
    )
    for document in options.documents:
        builder.project_builder.add_document(document)
    if options.board_outline_mils is not None:
        builder.set_board_outline_rectangle_mils(*options.board_outline_mils)
    if options.sheet_frame_mils is not None:
        builder.set_board_sheet_frame_mils(*options.sheet_frame_mils)
    written = builder.save(options.output_dir)
    context.invalidate_documents(list(output_paths.values()))
    return McoOperationResult.succeeded(
        spec,
        spec.message or "created project skeleton",
        outputs={
            "output_dir": str(written.output_dir.resolve()),
            "project": str(written.project_path.resolve()),
            "schematic": str(written.schematic_path.resolve()),
            "board": str(written.board_path.resolve()),
        },
    )


def _parse_project_skeleton_args(
    args: Mapping[str, object],
    context: McoExecutionContext,
) -> ProjectSkeletonArgs:
    project_name = _optional_string(args, "project_name", "debug_plate")
    return ProjectSkeletonArgs(
        output_dir=_optional_path(args, "output_dir", context.work_dir / "output", context),
        project_name=project_name,
        schematic_filename=_optional_string(args, "schematic_filename", None),
        board_filename=_optional_string(args, "board_filename", None),
        project_filename=_optional_string(args, "project_filename", None),
        layer_stack_template=_optional_string(args, "layer_stack_template", "2-layer"),
        overwrite=_optional_bool(args, "overwrite", False),
        board_outline_mils=_optional_number_object(
            args,
            "board_outline_mils",
            ("left", "bottom", "right", "top"),
        ),
        sheet_frame_mils=_optional_number_object(
            args,
            "sheet_frame_mils",
            ("x", "y", "width", "height"),
        ),
        documents=tuple(_optional_string_list(args, "documents")),
    )


def _project_skeleton_output_paths(options: ProjectSkeletonArgs) -> dict[str, Path]:
    project = options.project_filename or f"{options.project_name}.PrjPcb"
    schematic = options.schematic_filename or f"{options.project_name}.SchDoc"
    board = options.board_filename or f"{options.project_name}.PcbDoc"
    return {
        "output_dir": options.output_dir,
        "project": options.output_dir / project,
        "schematic": options.output_dir / schematic,
        "board": options.output_dir / board,
    }


def _stringified_paths(paths: Mapping[str, Path]) -> JsonObject:
    return {name: str(path.resolve()) for name, path in paths.items()}


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


def _optional_path(
    args: Mapping[str, object],
    name: str,
    default: Path,
    context: McoExecutionContext,
) -> Path:
    value = _optional_string(args, name, None)
    raw_path = default if value is None else Path(value)
    if raw_path.is_absolute():
        return raw_path.resolve()
    return (context.work_dir / raw_path).resolve()


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


def _optional_string_list(
    args: Mapping[str, object],
    name: str,
) -> list[str]:
    value = args.get(name)
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"Field {name!r} must be an array")
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item:
            raise ValueError(f"Field {name!r} must contain non-empty strings")
        result.append(item)
    return result


def _mco_template_text() -> str:
    return (
        "{\n"
        f'  "schema": "{MCO_SCHEMA}",\n'
        "  // MCO operations execute in order. Use on_fail to jump to another id.\n"
        '  "operations": [\n'
        "    {\n"
        '      "id": "create_debug_plate_skeleton",\n'
        '      "op": "project.create-skeleton",\n'
        '      "message": "Create a blank debug-plate project",\n'
        '      "args": {\n'
        '        "output_dir": "output/debug-plate",\n'
        '        "project_name": "debug_plate",\n'
        '        "overwrite": false,\n'
        '        "board_outline_mils": {\n'
        '          "left": 0,\n'
        '          "bottom": 0,\n'
        '          "right": 3000,\n'
        '          "top": 2000,\n'
        "        }\n"
        "      }\n"
        "    }\n"
        "  ]\n"
        "}\n"
    )


def _default_mco_operations() -> dict[str, McoOperationHandler]:
    from altium_cruncher.altium_cruncher_mco_cad_ops import CAD_MCO_OPERATIONS

    return {
        "mco.message": _op_message,
        "message": _op_message,
        "mco.fail": _op_fail,
        "fail": _op_fail,
        "file.copy": _op_copy_file,
        "project.create-skeleton": _op_create_project_skeleton,
        **CAD_MCO_OPERATIONS,
    }


DEFAULT_MCO_OPERATIONS: dict[str, McoOperationHandler] = _default_mco_operations()
