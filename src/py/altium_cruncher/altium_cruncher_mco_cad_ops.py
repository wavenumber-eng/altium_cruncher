"""CAD-oriented MCO operations."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, replace
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
    from altium_monkey import (
        AltiumPcbLib,
        AltiumPcbDoc,
        AltiumSchDoc,
        TextJustification,
        TextOrientation,
    )


@dataclass(frozen=True, slots=True)
class FileMutationPaths:
    """Input and output paths for an operation that rewrites one CAD file."""

    input_file: Path
    output_file: Path


PcbPoint = tuple[float, float]
MILS_PER_MM = 1000.0 / 25.4


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
    orientation = _sch_text_orientation(spec.args.get("orientation"))
    justification = _sch_text_justification(
        spec.args.get("justification", "BOTTOM_LEFT")
    )
    if context.dry_run:
        return _dry_run_result(spec, paths, {"text": text})

    from altium_monkey import SchPointMils, make_sch_net_label

    schdoc = _open_schdoc_for_mutation(paths, context)
    schdoc.add_object(
        make_sch_net_label(
            location_mils=SchPointMils.from_mils(*location),
            text=text,
            orientation=orientation,
            justification=justification,
        )
    )
    _mark_schdoc_dirty(context, paths)
    return _success_result(spec, paths, {"text": text})


def _op_schdoc_add_power_port(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    paths = _mutation_paths(spec.args, context)
    text = _required_string(spec.args, "text")
    location = _required_point(spec.args, "location_mils")
    orientation = _sch_text_orientation(spec.args.get("orientation"))
    style = _sch_power_object_style(spec.args.get("style", "BAR"))
    show_net_name = _optional_bool(spec.args, "show_net_name", True)
    if context.dry_run:
        return _dry_run_result(spec, paths, {"text": text})

    from altium_monkey import SchPointMils, make_sch_power_port

    schdoc = _open_schdoc_for_mutation(paths, context)
    schdoc.add_object(
        make_sch_power_port(
            location_mils=SchPointMils.from_mils(*location),
            text=text,
            style=style,
            orientation=orientation,
            show_net_name=show_net_name,
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
    unique_id = _optional_string(spec.args, "unique_id", None)
    if unique_id is not None:
        setattr(component, "unique_id", unique_id)
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
    component = pcbdoc.add_component_from_pcblib(
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
    _apply_pcb_component_source_link_fields(component, spec.args)
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


def _op_pcblib_create(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    file_path = _path_from_arg(spec.args, "file", context)
    overwrite = _optional_bool(spec.args, "overwrite", False)
    if file_path.exists() and not overwrite:
        return McoOperationResult.failed(spec, f"Output already exists: {file_path}")
    outputs = {"library": str(file_path.resolve())}
    if context.dry_run:
        return McoOperationResult.succeeded(
            spec,
            spec.message or "PcbLib create dry run",
            outputs=outputs,
        )

    from altium_monkey import AltiumPcbLib

    context.invalidate_documents([file_path])
    context.open_document_for_mutation(
        "pcblib",
        file_path,
        file_path,
        load=lambda path: AltiumPcbLib(path),
        save=_save_document_to_path,
    )
    return McoOperationResult.succeeded(
        spec,
        spec.message or "created PcbLib session",
        outputs=outputs,
    )


def _op_pcblib_add_footprint(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    paths = _mutation_paths(spec.args, context)
    name = _required_string(spec.args, "name")
    height = _optional_string(spec.args, "height", "0mil") or "0mil"
    description = _optional_string(spec.args, "description", "") or ""
    item_guid = _optional_string(spec.args, "item_guid", "") or ""
    revision_guid = _optional_string(spec.args, "revision_guid", "") or ""
    parameters = _optional_string_dict(spec.args, "parameters") or {}
    primitive_parameters = (
        _optional_string_dict(spec.args, "primitive_parameters") or {}
    )
    if context.dry_run:
        return _dry_run_result(
            spec,
            paths,
            {
                "footprint": name,
                "parameters": len(parameters),
                "primitive_parameters": len(primitive_parameters),
            },
        )

    pcblib = _open_pcblib_for_mutation(paths, context)
    _reject_duplicate_pcblib_footprint(pcblib, name, paths.output_file)
    footprint = pcblib.add_footprint(
        name,
        height=height,
        description=description,
        item_guid=item_guid,
        revision_guid=revision_guid,
    )
    for parameter_name, parameter_value in parameters.items():
        footprint.set_parameter(parameter_name, parameter_value)
    for parameter_name, parameter_value in primitive_parameters.items():
        footprint.set_footprint_primitive_parameter(parameter_name, parameter_value)
    _mark_pcblib_dirty(context, paths)
    return _success_result(
        spec,
        paths,
        {
            "footprint": name,
            "parameters": len(parameters),
            "primitive_parameters": len(primitive_parameters),
        },
    )


def _apply_pcb_component_source_link_fields(
    component: object,
    args: Mapping[str, object],
) -> None:
    raw_record = getattr(component, "raw_record", None)
    if not isinstance(raw_record, dict):
        return
    _set_optional_raw_text(
        raw_record,
        "SOURCEDESIGNATOR",
        _optional_string(args, "source_designator", None),
    )
    _set_optional_raw_text(
        raw_record,
        "SOURCEUNIQUEID",
        _normalize_source_unique_id(_optional_string(args, "source_unique_id", None)),
    )
    _set_optional_raw_text(
        raw_record,
        "SOURCEHIERARCHICALPATH",
        _optional_string(args, "source_hierarchical_path", None),
    )
    _set_optional_raw_text(
        raw_record,
        "SOURCECOMPONENTLIBRARY",
        _optional_string(args, "source_component_library", None),
    )
    _set_optional_raw_text(
        raw_record,
        "SOURCELIBREFERENCE",
        _optional_string(args, "source_lib_reference", None),
    )
    source_description = _optional_string(args, "source_description", None)
    _set_optional_raw_text(raw_record, "SOURCEDESCRIPTION", source_description)
    if source_description is not None:
        setattr(component, "description", source_description)
    channel_offset = _optional_int_or_none(args, "channel_offset")
    if channel_offset is not None:
        raw_record["CHANNELOFFSET"] = str(channel_offset)


def _normalize_source_unique_id(value: str | None) -> str | None:
    if value is None or value == "":
        return value
    return value if value.startswith("\\") else f"\\{value}"


def _set_optional_raw_text(
    raw_record: dict[object, object],
    key: str,
    value: str | None,
) -> None:
    if value is not None:
        raw_record[key] = value


def _op_pcbdoc_arrange_designators(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    paths = _mutation_paths(spec.args, context)
    designators = _optional_string_list(spec.args, "designators")
    placement = _optional_string(spec.args, "placement", "above_component")
    if placement != "above_component":
        raise ValueError("pcbdoc.arrange-designators placement must be above_component")
    offset = _optional_number_pair(spec.args, "offset_mils", default=(0.0, 10.0))
    if offset is None:
        offset = (0.0, 10.0)
    height_mils = _optional_float(spec.args, "height_mils", 40.0)
    stroke_width_mils = _optional_float(spec.args, "stroke_width_mils", 8.0)
    width_factor = _optional_float(spec.args, "width_factor", 0.6)
    layer = _pcb_layer(spec.args.get("layer"), default="TOP_OVERLAY")
    layer_id = int(cast(IntEnum, layer))
    font_kind = _pcb_text_kind(spec.args.get("font_kind", "truetype"))
    font_name = _optional_string(spec.args, "font_name", "Arial") or "Arial"
    bold = _optional_bool(spec.args, "bold", True)
    italic = _optional_bool(spec.args, "italic", False)
    if context.dry_run:
        return _dry_run_result(
            spec,
            paths,
            {
                "designators": len(designators) if designators is not None else "all",
                "placement": placement,
            },
        )

    pcbdoc = _open_pcbdoc_for_mutation(paths, context)
    updated = _arrange_pcb_designators(
        pcbdoc,
        designators=designators,
        offset_mils=offset,
        height_mils=height_mils,
        stroke_width_mils=stroke_width_mils,
        width_factor=width_factor,
        layer=layer_id,
        font_kind=_pcb_text_kind_id(font_kind),
        font_name=font_name,
        bold=bold,
        italic=italic,
    )
    if updated:
        _mark_pcbdoc_dirty(context, paths)
    return _success_result(spec, paths, {"updated": updated})


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
    is_board_cutout = _optional_bool(spec.args, "is_board_cutout", False)
    if context.dry_run:
        return _dry_run_result(
            spec,
            paths,
            {"points": len(outline_points), "is_board_cutout": is_board_cutout},
        )

    pcbdoc = _open_pcbdoc_for_mutation(paths, context)
    region = pcbdoc.add_region(
        outline_points_mils=outline_points,
        layer=_pcb_layer(spec.args.get("layer"), default="TOP"),
        hole_points_mils=_optional_hole_points(spec.args),
        is_keepout=_optional_bool(spec.args, "is_keepout", False),
        keepout_restrictions=int(_optional_float(spec.args, "keepout_restrictions", 0)),
        net=_optional_string(spec.args, "net", None),
    )
    if is_board_cutout:
        _mark_region_as_board_cutout(region)
    _mark_pcbdoc_dirty(context, paths)
    return _success_result(
        spec,
        paths,
        {"points": len(outline_points), "is_board_cutout": is_board_cutout},
    )


def _mark_region_as_board_cutout(region: object) -> None:
    setattr(region, "is_board_cutout", True)
    setattr(region, "kind", 0)
    properties = getattr(region, "properties", None)
    if isinstance(properties, dict):
        properties["KIND"] = "0"
        properties["ISBOARDCUTOUT"] = "TRUE"


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
        PcbLayerStepConfig,
        export_pcb_layer_step,
    )

    context.flush_documents()
    parsed_config = PcbLayerStepConfig.from_dict(spec.args)
    options = replace(
        parsed_config.to_options(),
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


def _op_pcbdoc_add_embedded_3d_model(
    spec: McoOperationSpec,
    context: McoExecutionContext,
) -> McoOperationResult:
    paths = _mutation_paths(spec.args, context)
    model_file = _path_from_arg(spec.args, "model_file", context)
    model_name = (
        _optional_string(spec.args, "model_name", model_file.name) or model_file.name
    )
    body_name = _optional_string(spec.args, "name", model_name) or model_name
    location_mils = _optional_number_pair(
        spec.args,
        "location_mils",
        default=(0.0, 0.0),
    )
    assert location_mils is not None
    if context.dry_run:
        return _dry_run_result(
            spec,
            paths,
            {
                "model_file": str(model_file),
                "name": body_name,
                "z_mils": _model_z_mils(spec.args),
            },
        )

    pcbdoc = _open_pcbdoc_for_mutation(paths, context)
    model = pcbdoc.add_embedded_model(
        name=model_name,
        model_data=model_file.read_bytes(),
    )
    pcbdoc.add_embedded_3d_model(
        model,
        layer=_pcb_layer(spec.args.get("layer"), default="MECHANICAL_13"),
        side=_pcb_body_projection(spec.args.get("side"), default="TOP"),
        location_mils=location_mils,
        rotation_x_degrees=_optional_float(spec.args, "rotation_x_degrees", 0.0),
        rotation_y_degrees=_optional_float(spec.args, "rotation_y_degrees", 0.0),
        rotation_z_degrees=_optional_float(spec.args, "rotation_z_degrees", 0.0),
        standoff_height_mils=_model_z_mils(spec.args),
        bounds_mils=_optional_bounds_mils(spec.args, "bounds_mils"),
        projection_outline_mils=_optional_points_mils(
            spec.args,
            "projection_outline_mils",
            minimum=3,
        ),
        overall_height_mils=_optional_float_or_none(spec.args, "overall_height_mils"),
        name=body_name,
        opacity=_optional_float(spec.args, "opacity", 1.0),
    )
    _mark_pcbdoc_dirty(context, paths)
    return _success_result(
        spec,
        paths,
        {"model_file": str(model_file), "name": body_name},
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


def _open_pcblib_for_mutation(
    paths: FileMutationPaths,
    context: McoExecutionContext,
) -> "AltiumPcbLib":
    from altium_monkey import AltiumPcbLib

    return cast(
        "AltiumPcbLib",
        context.open_document_for_mutation(
            "pcblib",
            paths.input_file,
            paths.output_file,
            load=AltiumPcbLib.from_file,
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


def _mark_pcblib_dirty(
    context: McoExecutionContext,
    paths: FileMutationPaths,
) -> None:
    context.mark_document_dirty("pcblib", paths.output_file)


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


def _optional_string_list(
    args: Mapping[str, object],
    name: str,
) -> list[str] | None:
    value = args.get(name)
    if value is None:
        return None
    if not isinstance(value, list):
        raise ValueError(f"Field {name!r} must be an array")
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item:
            raise ValueError(f"Field {name!r} must contain non-empty strings")
        result.append(item)
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


def _optional_points_mils(
    args: Mapping[str, object],
    name: str,
    *,
    minimum: int,
) -> list[PcbPoint] | None:
    value = args.get(name)
    if value is None:
        return None
    if not isinstance(value, list) or len(value) < minimum:
        raise ValueError(f"Field {name!r} must contain at least {minimum} points")
    return [_point_from_sequence(point, name) for point in value]


def _optional_bounds_mils(
    args: Mapping[str, object],
    name: str,
) -> tuple[float, float, float, float] | None:
    value = args.get(name)
    if value is None:
        return None
    if isinstance(value, dict):
        return (
            _required_float(value, "left"),
            _required_float(value, "bottom"),
            _required_float(value, "right"),
            _required_float(value, "top"),
        )
    if isinstance(value, list | tuple) and len(value) == 4:
        return (
            _point_number(value[0], name),
            _point_number(value[1], name),
            _point_number(value[2], name),
            _point_number(value[3], name),
        )
    raise ValueError(
        f"Field {name!r} must be an object with left/bottom/right/top or a "
        "four-number array"
    )


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


def _pcb_body_projection(value: object, *, default: str) -> object:
    from altium_monkey import PcbBodyProjection

    if value is None:
        value = default
    if isinstance(value, int) and not isinstance(value, bool):
        return PcbBodyProjection(value)
    if isinstance(value, str):
        return _enum_by_label(PcbBodyProjection, value)
    raise ValueError("PCB body projection must be a string name or native integer id")


def _model_z_mils(args: Mapping[str, object]) -> float:
    if "z_mils" in args:
        return _required_float(args, "z_mils")
    return _optional_float(args, "z_mm", 0.0) * MILS_PER_MM


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


def _pcb_text_kind_id(value: object) -> int:
    raw = getattr(value, "value", value)
    normalized = str(raw).strip().replace(" ", "_").replace("-", "_").upper()
    normalized = {"TRUE_TYPE": "TRUETYPE"}.get(normalized, normalized)
    if normalized == "TRUETYPE":
        return 1
    if normalized == "BARCODE":
        return 2
    return 0


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


def _sch_text_orientation(value: object) -> "TextOrientation":
    from altium_monkey import TextOrientation

    if value is None:
        return TextOrientation.DEGREES_0
    if isinstance(value, int) and not isinstance(value, bool):
        return TextOrientation(value)
    if isinstance(value, str):
        normalized = value.strip().replace(" ", "_").replace("-", "_").upper()
        if normalized.startswith("DEG_"):
            normalized = "DEGREES_" + normalized.removeprefix("DEG_")
        return cast("TextOrientation", _enum_by_label(TextOrientation, normalized))
    raise ValueError("Schematic text orientation must be a string name or native integer id")


def _sch_text_justification(value: object) -> "TextJustification":
    from altium_monkey import TextJustification

    if isinstance(value, int) and not isinstance(value, bool):
        return TextJustification(value)
    if isinstance(value, str):
        return cast("TextJustification", _enum_by_label(TextJustification, value))
    raise ValueError(
        "Schematic text justification must be a string name or native integer id"
    )


def _sch_power_object_style(value: object) -> object:
    from altium_monkey import PowerObjectStyle

    if isinstance(value, int) and not isinstance(value, bool):
        return PowerObjectStyle(value)
    if isinstance(value, str):
        return _enum_by_label(PowerObjectStyle, value)
    raise ValueError("Schematic power-port style must be a string name or native integer id")


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


def _reject_duplicate_pcblib_footprint(
    pcblib: object,
    footprint_name: str,
    library_path: Path,
) -> None:
    if any(
        str(getattr(footprint, "name", "") or "") == footprint_name
        for footprint in list(getattr(pcblib, "footprints", []) or [])
    ):
        raise ValueError(f"Footprint {footprint_name!r} already exists in {library_path}")


def _apply_schematic_text_style(
    component: object,
    args: Mapping[str, object],
    field_name: str,
) -> None:
    style = _optional_mapping(args, field_name)
    if style is None:
        return
    x, y, has_position = _schematic_text_position(style, field_name)
    method_name = _schematic_text_style_method_name(field_name)
    text_record = getattr(component, method_name)(
        x=x,
        y=y,
        font_name=_optional_string(style, "font_name", "Arial"),
        font_size=int(_optional_float(style, "font_size", 12.0)),
        bold=_optional_bool(style, "bold", field_name == "designator_style"),
    )
    _apply_schematic_text_justification(text_record, style)
    _apply_schematic_text_hidden(text_record, style)
    if has_position:
        _set_optional_record_flag(text_record, "auto_position", False)


def _schematic_text_position(
    style: Mapping[str, object],
    field_name: str,
) -> tuple[int | None, int | None, bool]:
    position = style.get("position_mils")
    if position is None:
        return (None, None, False)
    point = _point_from_sequence(position, f"{field_name}.position_mils")
    return (int(round(point[0])), int(round(point[1])), True)


def _schematic_text_style_method_name(field_name: str) -> str:
    if field_name == "designator_style":
        return "set_designator_style"
    return "set_comment_style"


def _apply_schematic_text_justification(
    text_record: object,
    style: Mapping[str, object],
) -> None:
    justification = style.get("justification")
    if justification is None:
        return
    setattr(text_record, "justification", _sch_text_justification(justification))
    if hasattr(text_record, "_has_justification"):
        setattr(text_record, "_has_justification", True)


def _apply_schematic_text_hidden(
    text_record: object,
    style: Mapping[str, object],
) -> None:
    hidden: bool | None = None
    if "hidden" in style:
        hidden = _optional_bool(style, "hidden", False)
    elif "visible" in style:
        hidden = not _optional_bool(style, "visible", True)
    if hidden is not None:
        _set_optional_record_flag(text_record, "is_hidden", hidden)


def _set_optional_record_flag(
    record: object,
    name: str,
    value: bool,
) -> None:
    if not hasattr(record, name):
        return
    setattr(record, name, value)
    presence_flag = f"_has_{name}"
    if hasattr(record, presence_flag):
        setattr(record, presence_flag, True)


def _arrange_pcb_designators(
    pcbdoc: object,
    *,
    designators: list[str] | None,
    offset_mils: PcbPoint,
    height_mils: float,
    stroke_width_mils: float,
    width_factor: float,
    layer: int,
    font_kind: int,
    font_name: str,
    bold: bool,
    italic: bool,
) -> int:
    component_lookup = _component_index_by_designator(pcbdoc)
    requested = _requested_designator_keys(designators, component_lookup)
    if not requested:
        return 0

    updated = 0
    for text in _pcb_designator_texts(pcbdoc):
        target = _arrange_designator_target(pcbdoc, text, component_lookup)
        if target is None or target.key not in requested:
            continue
        bounds = _component_bounds_or_position_mils(pcbdoc, target.component_index)
        if bounds is None:
            continue
        text_width_mils = max(
            height_mils,
            float(len(target.text)) * height_mils * width_factor,
        )
        left, _bottom, right, top = bounds
        x_mils = ((left + right) / 2.0) - (text_width_mils / 2.0) + offset_mils[0]
        y_mils = top + offset_mils[1]
        _apply_pcb_designator_text_style(
            text,
            text=target.text,
            position_mils=(x_mils, y_mils),
            text_width_mils=text_width_mils,
            height_mils=height_mils,
            stroke_width_mils=stroke_width_mils,
            layer=layer,
            font_kind=font_kind,
            font_name=font_name,
            bold=bold,
            italic=italic,
        )
        updated += 1
    return updated


@dataclass(frozen=True, slots=True)
class PcbDesignatorArrangementTarget:
    component_index: int
    key: str
    text: str


def _requested_designator_keys(
    designators: list[str] | None,
    component_lookup: Mapping[str, int],
) -> set[str]:
    if designators is None:
        return set(component_lookup)
    return {designator.strip().upper() for designator in designators if designator}


def _pcb_designator_texts(pcbdoc: object) -> list[object]:
    return [
        text
        for text in list(getattr(pcbdoc, "texts", []) or [])
        if bool(getattr(text, "is_designator", False))
    ]


def _arrange_designator_target(
    pcbdoc: object,
    text: object,
    component_lookup: Mapping[str, int],
) -> PcbDesignatorArrangementTarget | None:
    designator = str(getattr(text, "text_content", "") or "").strip()
    component_index = _designator_text_component_index(
        text,
        designator,
        component_lookup,
    )
    if component_index is None:
        return None
    component_designator = _component_designator_by_index(pcbdoc, component_index)
    text_value = component_designator or designator
    key = text_value.strip().upper()
    if not key:
        return None
    return PcbDesignatorArrangementTarget(
        component_index=component_index,
        key=key,
        text=text_value,
    )


def _component_index_by_designator(pcbdoc: object) -> dict[str, int]:
    result: dict[str, int] = {}
    for index, component in enumerate(list(getattr(pcbdoc, "components", []) or [])):
        designator = str(getattr(component, "designator", "") or "").strip()
        if designator:
            result[designator.upper()] = index
    return result


def _designator_text_component_index(
    text: object,
    designator: str,
    component_lookup: Mapping[str, int],
) -> int | None:
    component_index = getattr(text, "component_index", None)
    if isinstance(component_index, int):
        return component_index
    return component_lookup.get(designator.strip().upper())


def _component_designator_by_index(pcbdoc: object, index: int) -> str | None:
    components = list(getattr(pcbdoc, "components", []) or [])
    if 0 <= index < len(components):
        designator = str(getattr(components[index], "designator", "") or "").strip()
        return designator or None
    return None


def _component_position_bounds_mils(
    pcbdoc: object,
    component_index: int,
) -> tuple[float, float, float, float] | None:
    components = list(getattr(pcbdoc, "components", []) or [])
    if not (0 <= component_index < len(components)):
        return None
    component = components[component_index]
    x_mils = _component_position_value(component, "x")
    y_mils = _component_position_value(component, "y")
    if x_mils is None or y_mils is None:
        return None
    return (x_mils - 20.0, y_mils - 20.0, x_mils + 20.0, y_mils + 20.0)


def _component_position_value(component: object, axis: str) -> float | None:
    method = getattr(component, f"get_{axis}_mils", None)
    if callable(method):
        value = _call_position_method(method)
    else:
        value = getattr(component, axis, None)
    return _coerce_mils_value(value)


def _call_position_method(method: object) -> object | None:
    try:
        return cast(Callable[[], object], method)()
    except (TypeError, ValueError):
        return None


def _coerce_mils_value(value: object) -> float | None:
    if isinstance(value, int | float) and not isinstance(value, bool):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.lower().replace("mil", "").strip())
        except ValueError:
            return None
    return None


def _component_bounds_or_position_mils(
    pcbdoc: object,
    component_index: int,
) -> tuple[float, float, float, float] | None:
    bounds = _component_bounds_mils(pcbdoc, component_index)
    if bounds is not None:
        return bounds
    return _component_position_bounds_mils(pcbdoc, component_index)


def _component_bounds_mils(
    pcbdoc: object,
    component_index: int,
) -> tuple[float, float, float, float] | None:
    xs: list[float] = []
    ys: list[float] = []
    _append_component_centered_bounds(pcbdoc, component_index, xs, ys)
    _append_component_track_bounds(pcbdoc, component_index, xs, ys)
    _append_component_arc_bounds(pcbdoc, component_index, xs, ys)
    _append_component_fill_bounds(pcbdoc, component_index, xs, ys)
    _append_component_vertex_bounds(pcbdoc, component_index, xs, ys)
    return _bounds_from_points(xs, ys)


def _append_component_centered_bounds(
    pcbdoc: object,
    component_index: int,
    xs: list[float],
    ys: list[float],
) -> None:
    for collection in ("pads", "vias"):
        for primitive in _component_primitives(pcbdoc, collection, component_index):
            _append_centered_primitive_bounds(xs, ys, primitive)


def _append_component_track_bounds(
    pcbdoc: object,
    component_index: int,
    xs: list[float],
    ys: list[float],
) -> None:
    for track in _component_primitives(pcbdoc, "tracks", component_index):
        _append_track_bounds(xs, ys, track)


def _append_component_arc_bounds(
    pcbdoc: object,
    component_index: int,
    xs: list[float],
    ys: list[float],
) -> None:
    for arc in _component_primitives(pcbdoc, "arcs", component_index):
        _append_arc_bounds(xs, ys, arc)


def _append_component_fill_bounds(
    pcbdoc: object,
    component_index: int,
    xs: list[float],
    ys: list[float],
) -> None:
    for fill in _component_primitives(pcbdoc, "fills", component_index):
        _append_fill_bounds(xs, ys, fill)


def _append_component_vertex_bounds(
    pcbdoc: object,
    component_index: int,
    xs: list[float],
    ys: list[float],
) -> None:
    for collection, attr_name in (
        ("regions", "outline_vertices"),
        ("shapebased_regions", "outline"),
        ("component_bodies", "outline"),
        ("shapebased_component_bodies", "outline"),
    ):
        for primitive in _component_primitives(pcbdoc, collection, component_index):
            _append_vertex_bounds(xs, ys, getattr(primitive, attr_name, []) or [])


def _bounds_from_points(
    xs: list[float],
    ys: list[float],
) -> tuple[float, float, float, float] | None:
    if not xs or not ys:
        return None
    return (min(xs), min(ys), max(xs), max(ys))


def _component_primitives(
    pcbdoc: object,
    collection: str,
    component_index: int,
) -> list[object]:
    return [
        primitive
        for primitive in list(getattr(pcbdoc, collection, []) or [])
        if getattr(primitive, "component_index", None) == component_index
    ]


def _append_centered_primitive_bounds(
    xs: list[float],
    ys: list[float],
    primitive: object,
) -> None:
    x_mils = _attr_float(primitive, "x_mils")
    y_mils = _attr_float(primitive, "y_mils")
    if x_mils is None or y_mils is None:
        return
    width_mils = _attr_float(primitive, "width_mils") or 0.0
    height_mils = _attr_float(primitive, "height_mils")
    if height_mils is None:
        height_mils = _attr_float(primitive, "diameter_mils") or width_mils
    xs.extend((x_mils - width_mils / 2.0, x_mils + width_mils / 2.0))
    ys.extend((y_mils - height_mils / 2.0, y_mils + height_mils / 2.0))


def _append_track_bounds(xs: list[float], ys: list[float], track: object) -> None:
    points = (
        (_attr_float(track, "start_x_mils"), _attr_float(track, "start_y_mils")),
        (_attr_float(track, "end_x_mils"), _attr_float(track, "end_y_mils")),
    )
    width = (_attr_float(track, "width_mils") or 0.0) / 2.0
    for x_mils, y_mils in points:
        if x_mils is not None and y_mils is not None:
            xs.extend((x_mils - width, x_mils + width))
            ys.extend((y_mils - width, y_mils + width))


def _append_arc_bounds(xs: list[float], ys: list[float], arc: object) -> None:
    center_x = _attr_float(arc, "center_x_mils")
    center_y = _attr_float(arc, "center_y_mils")
    radius = _attr_float(arc, "radius_mils")
    if center_x is None or center_y is None or radius is None:
        return
    width = (_attr_float(arc, "width_mils") or 0.0) / 2.0
    extent = radius + width
    xs.extend((center_x - extent, center_x + extent))
    ys.extend((center_y - extent, center_y + extent))


def _append_fill_bounds(xs: list[float], ys: list[float], fill: object) -> None:
    for name in ("pos1", "pos2"):
        x_mils = _attr_float(fill, f"{name}_x_mils")
        y_mils = _attr_float(fill, f"{name}_y_mils")
        if x_mils is not None and y_mils is not None:
            xs.append(x_mils)
            ys.append(y_mils)


def _append_vertex_bounds(
    xs: list[float],
    ys: list[float],
    vertices: object,
) -> None:
    if not isinstance(vertices, list | tuple):
        return
    for vertex in vertices:
        x_mils = _attr_float(vertex, "x_mils")
        y_mils = _attr_float(vertex, "y_mils")
        if x_mils is not None and y_mils is not None:
            xs.append(x_mils)
            ys.append(y_mils)


def _attr_float(obj: object, name: str) -> float | None:
    value = getattr(obj, name, None)
    if isinstance(value, int | float) and not isinstance(value, bool):
        return float(value)
    return None


def _apply_pcb_designator_text_style(
    text_obj: object,
    *,
    text: str,
    position_mils: PcbPoint,
    text_width_mils: float,
    height_mils: float,
    stroke_width_mils: float,
    layer: int,
    font_kind: int,
    font_name: str,
    bold: bool,
    italic: bool,
) -> None:
    to_internal_units = getattr(text_obj, "_to_internal_units")
    x_raw = int(to_internal_units(position_mils[0]))
    y_raw = int(to_internal_units(position_mils[1]))
    setattr(text_obj, "text_content", text)
    setattr(text_obj, "x", x_raw)
    setattr(text_obj, "y", y_raw)
    setattr(text_obj, "height", int(to_internal_units(height_mils)))
    setattr(text_obj, "stroke_width", int(to_internal_units(stroke_width_mils)))
    setattr(text_obj, "width", int(to_internal_units(stroke_width_mils)))
    setattr(text_obj, "layer", int(layer))
    setattr(text_obj, "font_name", font_name)
    setattr(text_obj, "barcode_font_name", font_name)
    setattr(text_obj, "rotation", 0.0)
    setattr(text_obj, "is_mirrored", False)
    setattr(text_obj, "is_inverted", False)
    setattr(text_obj, "use_inverted_rectangle", False)
    setattr(text_obj, "is_frame", False)
    setattr(text_obj, "is_designator", True)
    setattr(text_obj, "is_comment", False)
    setattr(text_obj, "textbox_rect_width", int(to_internal_units(text_width_mils)))
    setattr(text_obj, "textbox_rect_height", int(to_internal_units(height_mils)))
    setattr(text_obj, "snap_point_x", x_raw)
    setattr(text_obj, "snap_point_y", y_raw)
    setattr(text_obj, "margin_border_width", 0)
    if font_kind == 1:
        setattr(text_obj, "font_type", 1)
        setattr(text_obj, "_font_type_offset43", 1)
        setattr(text_obj, "stroke_font_type", max(1, int(getattr(text_obj, "stroke_font_type", 1))))
        setattr(text_obj, "is_bold", bool(bold))
        setattr(text_obj, "is_italic", bool(italic))
    elif font_kind == 2:
        setattr(text_obj, "font_type", 2)
        setattr(text_obj, "_font_type_offset43", 0)
        setattr(text_obj, "stroke_font_type", max(1, int(getattr(text_obj, "stroke_font_type", 1))))
        setattr(text_obj, "is_bold", bool(bold))
        setattr(text_obj, "is_italic", bool(italic))
    else:
        setattr(text_obj, "font_type", 0)
        setattr(text_obj, "_font_type_offset43", 0)
        setattr(text_obj, "stroke_font_type", max(1, int(getattr(text_obj, "stroke_font_type", 1))))
        setattr(text_obj, "is_bold", False)
        setattr(text_obj, "is_italic", False)


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
    "schdoc.add-power-port": _op_schdoc_add_power_port,
    "schdoc.add-component": _op_schdoc_add_component,
    "pcblib.create": _op_pcblib_create,
    "pcblib.add-footprint": _op_pcblib_add_footprint,
    "pcbdoc.arrange-designators": _op_pcbdoc_arrange_designators,
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
    "pcbdoc.add-embedded-3d-model": _op_pcbdoc_add_embedded_3d_model,
}
