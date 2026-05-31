"""CAD-oriented MCO operations."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path
from typing import TYPE_CHECKING, cast

from altium_cruncher.altium_cruncher_mco import (
    McoExecutionContext,
    McoOperationHandler,
    McoOperationResult,
    McoOperationSpec,
)

if TYPE_CHECKING:
    from altium_cruncher.altium_cruncher_pcb_layer_step import PcbLayerStepHighlight
    from altium_monkey import AltiumPcbDoc, AltiumSchDoc


@dataclass(frozen=True, slots=True)
class FileMutationPaths:
    """Input and output paths for an operation that rewrites one CAD file."""

    input_file: Path
    output_file: Path


PcbPoint = tuple[float, float]


def _op_schdoc_add_wire(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    paths = _mutation_paths(spec.args, context)
    points = _required_points(spec.args, "points_mils", minimum=2)
    if context.dry_run:
        return _dry_run_result(spec, paths, {"points": len(points)})

    from altium_monkey import SchPointMils, make_sch_wire

    schdoc = _open_schdoc_for_mutation(paths, context)
    schdoc.add_object(
        make_sch_wire(
            points_mils=[SchPointMils.from_mils(x, y) for x, y in points],
        )
    )
    _mark_schdoc_dirty(context, paths)
    return _success_result(spec, paths, {"points": len(points)})


def _op_schdoc_add_net_label(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    paths = _mutation_paths(spec.args, context)
    text = _required_string(spec.args, "text")
    location = _required_point(spec.args, "location_mils")
    if context.dry_run:
        return _dry_run_result(spec, paths, {"text": text})

    from altium_monkey import SchPointMils, make_sch_net_label

    schdoc = _open_schdoc_for_mutation(paths, context)
    schdoc.add_object(
        make_sch_net_label(
            location_mils=SchPointMils.from_mils(*location),
            text=text,
        )
    )
    _mark_schdoc_dirty(context, paths)
    return _success_result(spec, paths, {"text": text})


def _op_schdoc_add_component(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    paths = _mutation_paths(spec.args, context)
    library_path = _path_from_arg(spec.args, "library", context)
    symbol = _required_string(spec.args, "symbol")
    designator = _required_string(spec.args, "designator")
    position = _required_point(spec.args, "position_mils")
    if context.dry_run:
        return _dry_run_result(
            spec,
            paths,
            {
                "library": str(library_path.resolve()),
                "symbol": symbol,
                "designator": designator,
            },
        )

    schdoc = _open_schdoc_for_mutation(paths, context)
    schdoc.add_component_from_library(
        library_path,
        symbol,
        designator,
        int(round(position[0])),
        int(round(position[1])),
        orientation=int(_optional_float(spec.args, "orientation", 0.0)),
        is_mirrored=_optional_bool(spec.args, "mirrored", False),
        part_id=int(_optional_float(spec.args, "part_id", 1.0)),
        display_mode=int(_optional_float(spec.args, "display_mode", 0.0)),
    )
    component = schdoc.components[-1]
    design_item_id = _optional_string(spec.args, "design_item_id", None)
    if design_item_id is not None:
        setattr(component, "design_item_id", design_item_id)
    for name, value in (_optional_string_dict(spec.args, "parameters") or {}).items():
        getattr(component, "add_parameter")(name, value)
    footprint_model = _optional_string(spec.args, "footprint_model", None)
    if footprint_model is not None:
        getattr(component, "add_footprint")(
            footprint_model,
            description=_optional_string(spec.args, "footprint_description", ""),
            library_name=_optional_string(spec.args, "footprint_library", ""),
        )
    _apply_schematic_text_style(component, spec.args, "designator_style")
    _apply_schematic_text_style(component, spec.args, "comment_style")
    _mark_schdoc_dirty(context, paths)
    return _success_result(
        spec,
        paths,
        {
            "library": str(library_path.resolve()),
            "symbol": symbol,
            "designator": designator,
        },
    )


def _op_pcbdoc_add_text(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    paths = _mutation_paths(spec.args, context)
    text = _required_string(spec.args, "text")
    position = _required_point(spec.args, "position_mils")
    height = _required_float(spec.args, "height_mils")
    layer = _pcb_layer(spec.args.get("layer"), default="TOP_OVERLAY")
    rotation_degrees = _optional_float(spec.args, "rotation_degrees", 0.0)
    stroke_width_mils = _optional_float(spec.args, "stroke_width_mils", 10.0)
    font_kind = _pcb_text_kind(spec.args.get("font_kind"))
    font_name = _optional_string(spec.args, "font_name", "Arial")
    bold = _optional_bool(spec.args, "bold", False)
    italic = _optional_bool(spec.args, "italic", False)
    is_comment = _optional_bool(spec.args, "is_comment", False)
    is_designator = _optional_bool(spec.args, "is_designator", False)
    is_mirrored = _optional_bool(spec.args, "is_mirrored", False)
    is_inverted = _optional_bool(spec.args, "is_inverted", False)
    inverted_margin_mils = _optional_float(spec.args, "inverted_margin_mils", 0.0)
    use_inverted_rectangle = _optional_bool(
        spec.args,
        "use_inverted_rectangle",
        False,
    )
    inverted_rectangle_size_mils = _optional_number_pair(
        spec.args,
        "inverted_rectangle_size_mils",
    )
    is_frame = _optional_bool(spec.args, "is_frame", False)
    frame_size_mils = _optional_number_pair(spec.args, "frame_size_mils")
    text_justification = _pcb_text_justification(
        spec.args.get("text_justification")
    )
    barcode_kind = _pcb_barcode_kind(spec.args.get("barcode_kind"))
    barcode_render_mode = _pcb_barcode_render_mode(
        spec.args.get("barcode_render_mode")
    )
    barcode_full_size_mils = _optional_number_pair(
        spec.args,
        "barcode_full_size_mils",
    )
    barcode_margin_mils = _optional_number_pair(
        spec.args,
        "barcode_margin_mils",
        default=(20.0, 20.0),
    )
    barcode_min_width_mils = _optional_float(spec.args, "barcode_min_width_mils", 0.0)
    barcode_show_text = _optional_bool(spec.args, "barcode_show_text", True)
    barcode_inverted = _optional_bool(spec.args, "barcode_inverted", True)
    if context.dry_run:
        return _dry_run_result(
            spec,
            paths,
            {
                "text": text,
                "font_kind": getattr(font_kind, "value", str(font_kind)),
                "text_justification": (
                    None
                    if text_justification is None
                    else getattr(text_justification, "name", str(text_justification))
                ),
            },
        )

    pcbdoc = _open_pcbdoc_for_mutation(paths, context)
    pcbdoc.add_text(
        text=text,
        position_mils=position,
        height_mils=height,
        layer=layer,
        rotation_degrees=rotation_degrees,
        stroke_width_mils=stroke_width_mils,
        font_kind=font_kind,
        font_name=font_name,
        bold=bold,
        italic=italic,
        is_comment=is_comment,
        is_designator=is_designator,
        is_mirrored=is_mirrored,
        is_inverted=is_inverted,
        inverted_margin_mils=inverted_margin_mils,
        use_inverted_rectangle=use_inverted_rectangle,
        inverted_rectangle_size_mils=inverted_rectangle_size_mils,
        is_frame=is_frame,
        frame_size_mils=frame_size_mils,
        text_justification=text_justification,
        barcode_kind=barcode_kind,
        barcode_render_mode=barcode_render_mode,
        barcode_full_size_mils=barcode_full_size_mils,
        barcode_margin_mils=barcode_margin_mils,
        barcode_min_width_mils=barcode_min_width_mils,
        barcode_show_text=barcode_show_text,
        barcode_inverted=barcode_inverted,
    )
    _mark_pcbdoc_dirty(context, paths)
    return _success_result(spec, paths, {"text": text})


def _op_pcbdoc_add_component(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    paths = _mutation_paths(spec.args, context)
    library_path = _path_from_arg(spec.args, "library", context)
    footprint_name = _required_string(spec.args, "footprint")
    designator = _required_string(spec.args, "designator")
    position = _required_point(spec.args, "position_mils")
    if context.dry_run:
        return _dry_run_result(
            spec,
            paths,
            {
                "library": str(library_path.resolve()),
                "footprint": footprint_name,
                "designator": designator,
            },
        )

    from altium_monkey import AltiumPcbLib

    pcblib = AltiumPcbLib.from_file(library_path)
    footprint = _pcblib_footprint(pcblib, footprint_name, library_path)
    pcbdoc = _open_pcbdoc_for_mutation(paths, context)
    pcbdoc.add_component_from_pcblib(
        footprint,
        designator=designator,
        position_mils=position,
        layer=_pcb_layer(spec.args.get("layer"), default="TOP"),
        rotation_degrees=_optional_float(spec.args, "rotation_degrees", 0.0),
        source_footprint_library=_optional_string(
            spec.args,
            "source_footprint_library",
            str(library_path),
        ),
        comment_text=_optional_string(spec.args, "comment_text", None),
        comment_visible=_optional_bool(spec.args, "comment_visible", False),
        component_parameters=_optional_string_dict(spec.args, "component_parameters"),
        pad_nets=_optional_string_dict(spec.args, "pad_nets"),
        source_pcblib=pcblib,
    )
    _mark_pcbdoc_dirty(context, paths)
    return _success_result(
        spec,
        paths,
        {
            "library": str(library_path.resolve()),
            "footprint": footprint_name,
            "designator": designator,
        },
    )


def _op_pcbdoc_add_track(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    paths = _mutation_paths(spec.args, context)
    start = _required_point(spec.args, "start_mils")
    end = _required_point(spec.args, "end_mils")
    width = _required_float(spec.args, "width_mils")
    if context.dry_run:
        return _dry_run_result(spec, paths, {"width_mils": width})

    pcbdoc = _open_pcbdoc_for_mutation(paths, context)
    pcbdoc.add_track(
        start,
        end,
        width_mils=width,
        layer=_pcb_layer(spec.args.get("layer"), default="TOP"),
        net=_optional_string(spec.args, "net", None),
    )
    _mark_pcbdoc_dirty(context, paths)
    return _success_result(spec, paths, {"width_mils": width})


def _op_pcbdoc_add_arc(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    paths = _mutation_paths(spec.args, context)
    center = _required_point(spec.args, "center_mils")
    radius = _required_float(spec.args, "radius_mils")
    if context.dry_run:
        return _dry_run_result(spec, paths, {"radius_mils": radius})

    pcbdoc = _open_pcbdoc_for_mutation(paths, context)
    pcbdoc.add_arc(
        center_mils=center,
        radius_mils=radius,
        start_angle_degrees=_required_float(spec.args, "start_angle_degrees"),
        end_angle_degrees=_required_float(spec.args, "end_angle_degrees"),
        width_mils=_required_float(spec.args, "width_mils"),
        layer=_pcb_layer(spec.args.get("layer"), default="TOP"),
        net=_optional_string(spec.args, "net", None),
    )
    _mark_pcbdoc_dirty(context, paths)
    return _success_result(spec, paths, {"radius_mils": radius})


def _op_pcbdoc_add_pad(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    paths = _mutation_paths(spec.args, context)
    designator = _required_string(spec.args, "designator")
    position = _required_point(spec.args, "position_mils")
    if context.dry_run:
        return _dry_run_result(spec, paths, {"designator": designator})

    pcbdoc = _open_pcbdoc_for_mutation(paths, context)
    pcbdoc.add_pad(
        designator=designator,
        position_mils=position,
        width_mils=_required_float(spec.args, "width_mils"),
        height_mils=_required_float(spec.args, "height_mils"),
        layer=_pcb_layer(spec.args.get("layer"), default="TOP"),
        shape=_pad_shape(spec.args.get("shape")),
        rotation_degrees=_optional_float(spec.args, "rotation_degrees", 0.0),
        hole_size_mils=_optional_float(spec.args, "hole_size_mils", 0.0),
        plated=_optional_bool_or_none(spec.args, "plated"),
        net=_optional_string(spec.args, "net", None),
        solder_mask_expansion_mils=_optional_float_or_none(
            spec.args,
            "solder_mask_expansion_mils",
        ),
        paste_mask_expansion_mils=_optional_float_or_none(
            spec.args,
            "paste_mask_expansion_mils",
        ),
    )
    pad = pcbdoc.pads[-1]
    _set_optional_attr(
        pad,
        "is_tenting_top",
        _optional_bool_or_none(spec.args, "tenting_top"),
    )
    _set_optional_attr(
        pad,
        "is_tenting_bottom",
        _optional_bool_or_none(spec.args, "tenting_bottom"),
    )
    _set_optional_attr(
        pad,
        "soldermask_expansion_mode",
        _optional_int_or_none(spec.args, "solder_mask_expansion_mode"),
    )
    _set_optional_attr(
        pad,
        "pastemask_expansion_mode",
        _optional_int_or_none(spec.args, "paste_mask_expansion_mode"),
    )
    _mark_pcbdoc_dirty(context, paths)
    return _success_result(spec, paths, {"designator": designator})


def _op_pcbdoc_add_via(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    paths = _mutation_paths(spec.args, context)
    position = _required_point(spec.args, "position_mils")
    if context.dry_run:
        return _dry_run_result(spec, paths, {"position_mils": list(position)})

    pcbdoc = _open_pcbdoc_for_mutation(paths, context)
    pcbdoc.add_via(
        position_mils=position,
        diameter_mils=_required_float(spec.args, "diameter_mils"),
        hole_size_mils=_required_float(spec.args, "hole_size_mils"),
        layer_start=_pcb_layer(spec.args.get("layer_start"), default="TOP"),
        layer_end=_pcb_layer(spec.args.get("layer_end"), default="BOTTOM"),
        net=_optional_string(spec.args, "net", None),
    )
    _mark_pcbdoc_dirty(context, paths)
    return _success_result(spec, paths, {"position_mils": list(position)})


def _op_pcbdoc_add_fill(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    paths = _mutation_paths(spec.args, context)
    corner1 = _required_point(spec.args, "corner1_mils")
    corner2 = _required_point(spec.args, "corner2_mils")
    if context.dry_run:
        return _dry_run_result(spec, paths, {"corner1_mils": list(corner1)})

    pcbdoc = _open_pcbdoc_for_mutation(paths, context)
    pcbdoc.add_fill(
        corner1,
        corner2,
        rotation_degrees=_optional_float(spec.args, "rotation_degrees", 0.0),
        layer=_pcb_layer(spec.args.get("layer"), default="TOP"),
        net=_optional_string(spec.args, "net", None),
    )
    _mark_pcbdoc_dirty(context, paths)
    return _success_result(spec, paths, {"corner1_mils": list(corner1)})


def _op_pcbdoc_add_region(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    paths = _mutation_paths(spec.args, context)
    outline_points = _required_points(spec.args, "outline_points_mils", minimum=3)
    if context.dry_run:
        return _dry_run_result(spec, paths, {"points": len(outline_points)})

    pcbdoc = _open_pcbdoc_for_mutation(paths, context)
    pcbdoc.add_region(
        outline_points_mils=outline_points,
        layer=_pcb_layer(spec.args.get("layer"), default="TOP"),
        hole_points_mils=_optional_hole_points(spec.args),
        is_keepout=_optional_bool(spec.args, "is_keepout", False),
        keepout_restrictions=int(_optional_float(spec.args, "keepout_restrictions", 0)),
        net=_optional_string(spec.args, "net", None),
    )
    _mark_pcbdoc_dirty(context, paths)
    return _success_result(spec, paths, {"points": len(outline_points)})


def _op_pcbdoc_create_user_union(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    paths = _mutation_paths(spec.args, context)
    name = _required_string(spec.args, "name")
    if context.dry_run:
        return _dry_run_result(spec, paths, {"name": name})

    pcbdoc = _open_pcbdoc_for_mutation(paths, context)
    members = _union_members(pcbdoc, spec.args.get("members", "all"))
    created = pcbdoc.create_user_union(name, members)
    _mark_pcbdoc_dirty(context, paths)
    return _success_result(
        spec,
        paths,
        {
            "name": getattr(created, "name", name),
            "union_index": int(getattr(created, "union_index", 0)),
            "member_count": int(getattr(created, "member_count", 0)),
        },
    )


def _op_pcbdoc_export_layer_step(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    input_file = _path_from_arg(spec.args, "file", context)
    output_file = _path_from_arg(spec.args, "output_file", context)
    overwrite = _optional_bool(spec.args, "overwrite", False)
    if output_file.exists() and not overwrite:
        raise FileExistsError(f"Output already exists: {output_file}")
    if context.dry_run:
        return McoOperationResult.succeeded(
            spec,
            spec.message or f"{spec.op} dry run",
            outputs={
                "file": str(input_file),
                "step_file": str(output_file),
                "manifest_file": str(output_file.with_suffix(".json")),
                "highlight_count": len(_pcb_layer_step_highlights(spec.args)),
            },
        )

    from altium_monkey import AltiumPcbDoc
    from altium_cruncher.altium_cruncher_pcb_layer_step import (
        PcbLayerStepOptions,
        export_pcb_layer_step,
        resolve_pcb_layer_selector,
    )

    context.flush_documents()
    defaults = PcbLayerStepOptions(
        layer=resolve_pcb_layer_selector(spec.args.get("layer"))
    )
    options = PcbLayerStepOptions(
        layer=defaults.layer,
        thickness_mm=_optional_float(
            spec.args,
            "thickness_mm",
            defaults.thickness_mm,
        ),
        z_mm=_optional_float(spec.args, "z_mm", defaults.z_mm),
        copper_color=_optional_string(
            spec.args,
            "copper_color",
            defaults.copper_color,
        )
        or defaults.copper_color,
        outline_width_mm=_optional_float(
            spec.args,
            "outline_width_mm",
            defaults.outline_width_mm,
        ),
        outline_color=_optional_string(
            spec.args,
            "outline_color",
            defaults.outline_color,
        )
        or defaults.outline_color,
        include_copper=_optional_bool(
            spec.args,
            "include_copper",
            defaults.include_copper,
        ),
        include_board_outline=_optional_bool(
            spec.args,
            "include_board_outline",
            defaults.include_board_outline,
        ),
        include_poured_polygons=_optional_bool(
            spec.args,
            "include_poured_polygons",
            defaults.include_poured_polygons,
        ),
        cut_holes=_optional_bool(spec.args, "cut_holes", defaults.cut_holes),
        fuse_copper=_optional_bool(spec.args, "fuse_copper", defaults.fuse_copper),
        fuse_board_outline=_optional_bool(
            spec.args,
            "fuse_board_outline",
            defaults.fuse_board_outline,
        ),
        arc_segments=int(
            _optional_float(spec.args, "arc_segments", float(defaults.arc_segments))
        ),
        highlights=_pcb_layer_step_highlights(spec.args),
    )
    result = export_pcb_layer_step(
        AltiumPcbDoc.from_file(input_file),
        output_file,
        options=options,
        board_name=_optional_string(spec.args, "board_name", input_file.stem),
        source_input=str(input_file),
    )
    return McoOperationResult.succeeded(
        spec,
        spec.message or f"{spec.op} wrote {result.output_path.name}",
        outputs={
            "file": str(input_file),
            "step_file": str(result.output_path),
            "manifest_file": str(result.manifest_path),
            "layer": result.layer,
            "highlight_count": len(options.highlights),
        },
    )


def _pcb_layer_step_highlights(
    args: Mapping[str, object],
) -> tuple["PcbLayerStepHighlight", ...]:
    value = args.get("highlights", [])
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ValueError("Field 'highlights' must be an array")
    return tuple(_pcb_layer_step_highlight(item) for item in value)


def _pcb_layer_step_highlight(
    value: object,
) -> "PcbLayerStepHighlight":
    from altium_cruncher.altium_cruncher_pcb_layer_step import PcbLayerStepHighlight

    if not isinstance(value, dict):
        raise ValueError("Field 'highlights' must contain objects")
    pad_geometries = value.get("pad_geometries", [])
    if not isinstance(pad_geometries, list):
        raise ValueError("Field 'highlights[].pad_geometries' must be an array")
    return PcbLayerStepHighlight(
        id=_required_string(value, "id"),
        name=_optional_string(value, "name", None),
        color=_required_string(value, "color"),
        pad_geometries=tuple(
            dict(geometry) for geometry in pad_geometries if isinstance(geometry, dict)
        ),
        z_offset_mm=_optional_float(value, "z_offset_mm", 0.001),
        thickness_mm=_optional_float(value, "thickness_mm", 0.01),
    )


def _mutation_paths(
    args: Mapping[str, object],
    context: McoExecutionContext,
) -> FileMutationPaths:
    input_file = _path_from_arg(args, "file", context)
    output_value = _optional_string(args, "output_file", None)
    overwrite = _optional_bool(args, "overwrite", False)
    if output_value is None and not overwrite:
        raise ValueError("CAD mutation operations require output_file or overwrite=true")
    output_file = input_file if output_value is None else _resolve_path(output_value, context)
    if output_file.exists() and output_file != input_file and not overwrite:
        raise FileExistsError(f"Output already exists: {output_file}")
    return FileMutationPaths(input_file=input_file, output_file=output_file)


def _success_result(
    spec: McoOperationSpec,
    paths: FileMutationPaths,
    outputs: Mapping[str, object],
) -> McoOperationResult:
    payload = {"file": str(paths.output_file.resolve()), **dict(outputs)}
    return McoOperationResult.succeeded(
        spec,
        spec.message or f"{spec.op} wrote {paths.output_file.name}",
        outputs=payload,
    )


def _dry_run_result(
    spec: McoOperationSpec,
    paths: FileMutationPaths,
    outputs: Mapping[str, object],
) -> McoOperationResult:
    payload = {"file": str(paths.output_file.resolve()), **dict(outputs)}
    return McoOperationResult.succeeded(
        spec,
        spec.message or f"{spec.op} dry run",
        outputs=payload,
    )


def _open_schdoc_for_mutation(
    paths: FileMutationPaths,
    context: McoExecutionContext,
) -> "AltiumSchDoc":
    from altium_monkey import AltiumSchDoc

    return cast(
        "AltiumSchDoc",
        context.open_document_for_mutation(
            "schdoc",
            paths.input_file,
            paths.output_file,
            load=lambda path: AltiumSchDoc(path),
            save=_save_document_to_path,
        ),
    )


def _open_pcbdoc_for_mutation(
    paths: FileMutationPaths,
    context: McoExecutionContext,
) -> "AltiumPcbDoc":
    from altium_monkey import AltiumPcbDoc

    return cast(
        "AltiumPcbDoc",
        context.open_document_for_mutation(
            "pcbdoc",
            paths.input_file,
            paths.output_file,
            load=AltiumPcbDoc.from_file,
            save=_save_document_to_path,
        ),
    )


def _mark_schdoc_dirty(
    context: McoExecutionContext,
    paths: FileMutationPaths,
) -> None:
    context.mark_document_dirty("schdoc", paths.output_file)


def _mark_pcbdoc_dirty(
    context: McoExecutionContext,
    paths: FileMutationPaths,
) -> None:
    context.mark_document_dirty("pcbdoc", paths.output_file)


def _save_document_to_path(document: object, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    getattr(document, "save")(output_file)


def _path_from_arg(
    args: Mapping[str, object],
    name: str,
    context: McoExecutionContext,
) -> Path:
    return _resolve_path(_required_string(args, name), context)


def _resolve_path(value: str, context: McoExecutionContext) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (context.work_dir / path).resolve()


def _required_string(args: Mapping[str, object], name: str) -> str:
    value = args.get(name)
    if not isinstance(value, str) or not value:
        raise ValueError(f"Field {name!r} must be a non-empty string")
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


def _optional_bool(args: Mapping[str, object], name: str, default: bool) -> bool:
    value = args.get(name)
    if value is None:
        return default
    if not isinstance(value, bool):
        raise ValueError(f"Field {name!r} must be a boolean")
    return value


def _optional_bool_or_none(args: Mapping[str, object], name: str) -> bool | None:
    value = args.get(name)
    if value is None:
        return None
    if not isinstance(value, bool):
        raise ValueError(f"Field {name!r} must be a boolean")
    return value


def _optional_string_dict(
    args: Mapping[str, object],
    name: str,
) -> dict[str, str] | None:
    value = args.get(name)
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError(f"Field {name!r} must be an object")
    result: dict[str, str] = {}
    for key, item in value.items():
        if not isinstance(key, str) or not isinstance(item, str):
            raise ValueError(f"Field {name!r} must contain string keys and values")
        result[key] = item
    return result


def _optional_mapping(
    args: Mapping[str, object],
    name: str,
) -> Mapping[str, object] | None:
    value = args.get(name)
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError(f"Field {name!r} must be an object")
    return value


def _required_float(args: Mapping[str, object], name: str) -> float:
    value = args.get(name)
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise ValueError(f"Field {name!r} must be numeric")
    return float(value)


def _optional_float(
    args: Mapping[str, object],
    name: str,
    default: float,
) -> float:
    value = args.get(name)
    return default if value is None else _required_float(args, name)


def _optional_float_or_none(args: Mapping[str, object], name: str) -> float | None:
    value = args.get(name)
    return None if value is None else _required_float(args, name)


def _optional_int_or_none(args: Mapping[str, object], name: str) -> int | None:
    value = args.get(name)
    if value is None:
        return None
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"Field {name!r} must be an integer")
    return value


def _optional_int_or_string(
    args: Mapping[str, object],
    name: str,
    default: int | str,
) -> int | str:
    value = args.get(name)
    if value is None:
        return default
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, str) and value:
        return value
    raise ValueError(f"Field {name!r} must be an integer or non-empty string")


def _required_point(args: Mapping[str, object], name: str) -> PcbPoint:
    value = args.get(name)
    if not isinstance(value, list | tuple) or len(value) != 2:
        raise ValueError(f"Field {name!r} must be a two-number array")
    return (_point_number(value[0], name), _point_number(value[1], name))


def _required_points(
    args: Mapping[str, object],
    name: str,
    *,
    minimum: int,
) -> list[PcbPoint]:
    value = args.get(name)
    if not isinstance(value, list) or len(value) < minimum:
        raise ValueError(f"Field {name!r} must contain at least {minimum} points")
    return [_point_from_sequence(point, name) for point in value]


def _optional_hole_points(args: Mapping[str, object]) -> list[list[PcbPoint]] | None:
    value = args.get("hole_points_mils")
    if value is None:
        return None
    if not isinstance(value, list):
        raise ValueError("Field 'hole_points_mils' must be an array")
    return [_hole_ring_points(hole) for hole in value]


def _hole_ring_points(value: object) -> list[PcbPoint]:
    if not isinstance(value, list):
        raise ValueError("Field 'hole_points_mils' must contain point arrays")
    return [_point_from_sequence(point, "hole_points_mils") for point in value]


def _point_from_sequence(value: object, name: str) -> PcbPoint:
    if not isinstance(value, list | tuple) or len(value) != 2:
        raise ValueError(f"Field {name!r} must contain two-number point arrays")
    return (_point_number(value[0], name), _point_number(value[1], name))


def _point_number(value: object, name: str) -> float:
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise ValueError(f"Field {name!r} points must be numeric")
    return float(value)


def _optional_number_pair(
    args: Mapping[str, object],
    name: str,
    *,
    default: PcbPoint | None = None,
) -> PcbPoint | None:
    value = args.get(name)
    if value is None:
        return default
    return _point_from_sequence(value, name)


def _pcb_layer(value: object, *, default: str) -> object:
    from altium_monkey import PcbLayer

    if value is None:
        value = default
    if isinstance(value, int) and not isinstance(value, bool):
        return PcbLayer(value)
    if isinstance(value, str):
        return _enum_by_label(PcbLayer, value)
    raise ValueError("PCB layer must be a string name or native integer id")


def _pad_shape(value: object) -> object:
    from altium_monkey import PadShape

    if value is None:
        return PadShape.RECTANGLE
    if isinstance(value, int) and not isinstance(value, bool):
        return PadShape(value)
    if isinstance(value, str):
        return _enum_by_label(PadShape, value)
    raise ValueError("Pad shape must be a string name or native integer id")


def _pcb_text_kind(value: object) -> object:
    from altium_monkey import PcbTextKind

    if value is None:
        return PcbTextKind.STROKE
    if isinstance(value, str):
        normalized = value.strip().replace(" ", "_").replace("-", "_").upper()
        normalized = {"TRUE_TYPE": "TRUETYPE"}.get(normalized, normalized)
        if normalized in PcbTextKind.__members__:
            return PcbTextKind[normalized]
        try:
            return PcbTextKind(value.strip().lower())
        except ValueError as exc:
            raise ValueError(
                "PCB text font_kind must be stroke, truetype, or barcode"
            ) from exc
    raise ValueError("PCB text font_kind must be a string")


def _pcb_text_justification(value: object) -> object | None:
    from altium_monkey import PcbTextJustification

    if value is None:
        return None
    if isinstance(value, int) and not isinstance(value, bool):
        return PcbTextJustification(value)
    if isinstance(value, str):
        return _enum_by_label(PcbTextJustification, value)
    raise ValueError("PCB text_justification must be a string name or native integer id")


def _pcb_barcode_kind(value: object) -> object:
    from altium_monkey import PcbBarcodeKind

    if value is None:
        return PcbBarcodeKind.CODE_39
    if isinstance(value, int) and not isinstance(value, bool):
        return PcbBarcodeKind(value)
    if isinstance(value, str):
        return _enum_by_label(PcbBarcodeKind, value)
    raise ValueError("PCB barcode_kind must be a string name or native integer id")


def _pcb_barcode_render_mode(value: object) -> object:
    from altium_monkey import PcbBarcodeRenderMode

    if value is None:
        return PcbBarcodeRenderMode.BY_FULL_WIDTH
    if isinstance(value, int) and not isinstance(value, bool):
        return PcbBarcodeRenderMode(value)
    if isinstance(value, str):
        return _enum_by_label(PcbBarcodeRenderMode, value)
    raise ValueError(
        "PCB barcode_render_mode must be a string name or native integer id"
    )


def _enum_by_label(enum_type: type[IntEnum], value: str) -> IntEnum:
    normalized = value.strip().replace(" ", "_").replace("-", "_").upper()
    layer_aliases = {"TOP_LAYER": "TOP", "BOTTOM_LAYER": "BOTTOM"}
    normalized = layer_aliases.get(normalized, normalized)
    if normalized in enum_type.__members__:
        return enum_type[normalized]
    return enum_type(int(value))


def _pcblib_footprint(
    pcblib: object,
    footprint_name: str,
    library_path: Path,
) -> object:
    footprints = list(getattr(pcblib, "footprints", []) or [])
    for footprint in footprints:
        if str(getattr(footprint, "name", "") or "") == footprint_name:
            return footprint
    available = [str(getattr(footprint, "name", "") or "") for footprint in footprints]
    raise ValueError(
        f"Footprint {footprint_name!r} not found in {library_path}. "
        f"Available footprints: {available}"
    )


def _apply_schematic_text_style(
    component: object,
    args: Mapping[str, object],
    field_name: str,
) -> None:
    style = _optional_mapping(args, field_name)
    if style is None:
        return
    position = style.get("position_mils")
    x: int | None = None
    y: int | None = None
    if position is not None:
        point = _point_from_sequence(position, f"{field_name}.position_mils")
        x = int(round(point[0]))
        y = int(round(point[1]))
    method_name = (
        "set_designator_style"
        if field_name == "designator_style"
        else "set_comment_style"
    )
    getattr(component, method_name)(
        x=x,
        y=y,
        font_name=_optional_string(style, "font_name", "Arial"),
        font_size=int(_optional_float(style, "font_size", 12.0)),
        bold=_optional_bool(style, "bold", field_name == "designator_style"),
    )


def _set_optional_attr(obj: object, name: str, value: object | None) -> None:
    if value is not None:
        setattr(obj, name, value)


def _union_members(pcbdoc: object, spec: object) -> list[object]:
    if spec == "all" or spec is None:
        return _all_union_members(pcbdoc)
    raise ValueError("Only members='all' is supported by pcbdoc.create-user-union")


def _all_union_members(pcbdoc: object) -> list[object]:
    members: list[object] = []
    for collection in _union_member_collections():
        members.extend(list(getattr(pcbdoc, collection, []) or []))
    return members


def _union_member_collections() -> tuple[str, ...]:
    return (
        "components",
        "pads",
        "vias",
        "tracks",
        "arcs",
        "fills",
        "regions",
        "shapebased_regions",
        "texts",
        "component_bodies",
        "shapebased_component_bodies",
    )


CAD_MCO_OPERATIONS: dict[str, McoOperationHandler] = {
    "schdoc.add-wire": _op_schdoc_add_wire,
    "schdoc.add-net-label": _op_schdoc_add_net_label,
    "schdoc.add-component": _op_schdoc_add_component,
    "pcbdoc.add-text": _op_pcbdoc_add_text,
    "pcbdoc.add-component": _op_pcbdoc_add_component,
    "pcbdoc.add-track": _op_pcbdoc_add_track,
    "pcbdoc.add-arc": _op_pcbdoc_add_arc,
    "pcbdoc.add-pad": _op_pcbdoc_add_pad,
    "pcbdoc.add-via": _op_pcbdoc_add_via,
    "pcbdoc.add-fill": _op_pcbdoc_add_fill,
    "pcbdoc.add-region": _op_pcbdoc_add_region,
    "pcbdoc.create-user-union": _op_pcbdoc_create_user_union,
    "pcbdoc.export-layer-step": _op_pcbdoc_export_layer_step,
}
