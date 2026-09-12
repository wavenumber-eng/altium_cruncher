"""Generated from src/tsp/altium_cruncher/config/mate-config.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

CurrentMate = TypedDict("CurrentMate", {
    "output": NotRequired["Output"],
    "libraries": NotRequired["Libraries | None"],
    "known_parts": NotRequired["KnownParts | None"],
    "pcb_designators": NotRequired["Designators | None"],
    "artifacts": NotRequired["Artifacts"],
    "schema": "Literal[\"altium_cruncher.mate.config.a0\"]",
    "source": NotRequired["CurrentMate_source"],
    "validation": NotRequired["Validation"],
    "projections": NotRequired["list[Projection]"],
    "board_projection": NotRequired["BoardProjection"],
}, extra_items="object")

LegacyMate = TypedDict("LegacyMate", {
    "output": NotRequired["Output"],
    "libraries": NotRequired["Libraries | None"],
    "known_parts": NotRequired["KnownParts | None"],
    "pcb_designators": NotRequired["Designators | None"],
    "artifacts": NotRequired["Artifacts"],
    "schema": NotRequired["Literal[\"altium_cruncher.mate.legacy.a0\"] | None"],
    "source": NotRequired["LegacyMate_source"],
    "marker": NotRequired["LegacyMate_marker"],
    "placement": NotRequired["LegacyMate_placement"],
    "pcb_labels": NotRequired["Labels | None"],
    "selection": NotRequired["LegacyMate_selection"],
    "board_projection": NotRequired["BoardProjection | None"],
}, extra_items="object")

Output = TypedDict("Output", {
    "backend": NotRequired["Literal[\"altium\"] | None"],
    "output_dir": NotRequired["str | None"],
    "project_name": NotRequired["str | None"],
    "schematic_filename": NotRequired["str | None"],
    "schematic_sheet_style": NotRequired["str | None"],
    "board_filename": NotRequired["str | None"],
    "project_filename": NotRequired["str | None"],
    "origin": NotRequired["str | None"],
    "overwrite": NotRequired["bool | None"],
    "layer_stack_template": NotRequired["str | None"],
    "board_outline": NotRequired["OutputOutline | None"],
    "board_outline_mils": NotRequired["Bounds | None"],
    "board_origin_mils": NotRequired["Point | None"],
}, extra_items="object")

Libraries = TypedDict("Libraries", {
    "roots": NotRequired["str | StringArray | None"],
    "recursive": NotRequired["bool | None"],
}, extra_items="object")

KnownParts = TypedDict("KnownParts", {
    "manifest": NotRequired["str | None"],
    "cache_dir": NotRequired["str | None"],
}, extra_items="object")

Designators = TypedDict("Designators", {
    "enabled": NotRequired["bool | None"],
    "placement": NotRequired["Literal[\"above_component\"] | None"],
    "offset_mils": NotRequired["Pair | None"],
    "width_factor": NotRequired["float | None"],
    "style": NotRequired["TextStyle"],
}, extra_items="object")

Artifacts = TypedDict("Artifacts", {
    "pcb_layer_step": NotRequired["LayerStepArtifact | None"],
}, extra_items="object")

Validation = TypedDict("Validation", {
    "source_side": NotRequired["Literal[\"infer_single_side\"] | Literal[\"any\"] | Literal[\"none\"] | Literal[\"top\"] | Literal[\"bottom\"] | None"],
    "allow_side_agnostic_through_hole": NotRequired["bool | None"],
    "side_agnostic_kinds": NotRequired["StringArray | None"],
}, extra_items="object")

Projection = TypedDict("Projection", {
    "id": NotRequired["str | None"],
    "source": NotRequired["SourceSelector | None"],
    "select": NotRequired["Projection_select"],
    "actions": NotRequired["list[ProjectionAction]"],
}, extra_items="object")

BoardProjection = TypedDict("BoardProjection", {
    "outline": NotRequired["BoardProjection_outline"],
    "cutouts": NotRequired["BoardProjection_cutouts"],
}, extra_items="object")

Labels = TypedDict("Labels", {
    "side": NotRequired["Literal[\"left\"] | Literal[\"right\"] | Literal[\"board_left\"] | Literal[\"board_right\"] | None"],
    "offset_mils": NotRequired["Pair | None"],
    "box_size_mils": NotRequired["Pair | None"],
    "center_box_on_target": NotRequired["bool | None"],
    "row_spacing_mils": NotRequired["float | None"],
    "column_spacing_mils": NotRequired["float | None"],
    "auto_width_padding_mils": NotRequired["float | None"],
    "enabled": NotRequired["bool | None"],
    "style": NotRequired["TextStyle"],
}, extra_items="object")

SelectedBoard = TypedDict("SelectedBoard", {
    "board_key": NotRequired["str"],
    "pcb_path": NotRequired["str"],
    "components": NotRequired["list[SelectedComponent]"],
    "free_pads": NotRequired["list[SelectedPad]"],
    "board_outline_mils": NotRequired["Bounds | None"],
    "board_outline": NotRequired["InputOutline | None"],
}, extra_items="object")

OutputOutline = TypedDict("OutputOutline", {
    "mode": NotRequired["Literal[\"source_bounds\"] | Literal[\"match_source_bounds\"] | Literal[\"match_bounds\"] | Literal[\"source_bounds_with_margin\"] | Literal[\"source_bounds_plus_margin\"] | Literal[\"padded_rectangle\"] | Literal[\"padded_source_bounds\"] | None"],
    "margin_mils": NotRequired["Nonnegative | Margins"],
}, extra_items="object")

Bounds = TypedDict("Bounds", {
    "left": "float",
    "bottom": "float",
    "right": "float",
    "top": "float",
}, closed=True)

Point = TypedDict("Point", {
    "x": "float",
    "y": "float",
}, closed=True)

TextStyle = TypedDict("TextStyle", {
    "height_mils": NotRequired["float | None"],
    "layer": NotRequired["str | int | None"],
    "font_kind": NotRequired["str | None"],
    "font_name": NotRequired["str | None"],
    "bold": NotRequired["bool | None"],
    "italic": NotRequired["bool | None"],
    "stroke_width_mils": NotRequired["float | None"],
    "text_justification": NotRequired["str | int | None"],
    "is_inverted": NotRequired["bool | None"],
    "inverted_margin_mils": NotRequired["float | None"],
    "use_inverted_rectangle": NotRequired["bool | None"],
    "is_frame": NotRequired["bool | None"],
    "header_height_mils": NotRequired["float | None"],
    "header_stroke_width_mils": NotRequired["float | None"],
    "rotation_degrees": NotRequired["float | None"],
    "stroke_font_type": NotRequired["str | int | None"],
    "is_comment": NotRequired["bool | None"],
    "is_designator": NotRequired["bool | None"],
    "is_mirrored": NotRequired["bool | None"],
    "barcode_kind": NotRequired["str | int | None"],
    "barcode_render_mode": NotRequired["str | int | None"],
    "barcode_full_size_mils": NotRequired["Pair | None"],
    "barcode_margin_mils": NotRequired["Pair | None"],
    "barcode_min_width_mils": NotRequired["float | None"],
    "barcode_show_text": NotRequired["bool | None"],
    "barcode_inverted": NotRequired["bool | None"],
}, extra_items="object")

LayerStepArtifact = TypedDict("LayerStepArtifact", {
    "thickness_mm": NotRequired["float"],
    "z_mm": NotRequired["float"],
    "copper_color": NotRequired["Color"],
    "outline_width_mm": NotRequired["float"],
    "outline_color": NotRequired["Color"],
    "board_cutout_color": NotRequired["Color"],
    "include_board_cutouts": NotRequired["bool"],
    "include_copper": NotRequired["bool"],
    "include_board_outline": NotRequired["bool"],
    "include_poured_polygons": NotRequired["bool"],
    "cut_holes": NotRequired["bool"],
    "drill_hole_mode": NotRequired["DrillMode"],
    "max_boolean_drill_cuts": NotRequired["int"],
    "drill_hole_color": NotRequired["Color"],
    "drill_plated_hole_color": NotRequired["Color"],
    "drill_non_plated_hole_color": NotRequired["Color"],
    "drill_overlay_thickness_mm": NotRequired["float"],
    "drill_minimum_diameter_mm": NotRequired["float"],
    "drill_hole_shape": NotRequired["DrillShape"],
    "drill_ring_width_mm": NotRequired["float"],
    "drill_plated_ring_shape": NotRequired["PlatedRingShape"],
    "drill_selected_component_mode": NotRequired["DrillScopedMode"],
    "drill_other_component_mode": NotRequired["DrillScopedMode"],
    "drill_free_pad_mode": NotRequired["DrillScopedMode"],
    "drill_via_mode": NotRequired["DrillScopedMode"],
    "fuse_copper": NotRequired["bool"],
    "fuse_board_outline": NotRequired["bool"],
    "arc_segments": NotRequired["int"],
    "include_tracks": NotRequired["bool"],
    "include_arcs": NotRequired["bool"],
    "include_fills": NotRequired["bool"],
    "include_regions": NotRequired["bool"],
    "include_vias": NotRequired["bool"],
    "include_component_pads": NotRequired["bool"],
    "include_free_pads": NotRequired["bool"],
    "include_designators": NotRequired["StringList"],
    "board_outline": NotRequired["BoardOutline"],
    "features": NotRequired["Features"],
    "drills": NotRequired["Drills"],
    "enabled": NotRequired["bool | None"],
    "source_layer": NotRequired["str | None"],
    "insert_in_output": NotRequired["bool | InsertArtifact | None"],
    "highlights": NotRequired["list[Highlight] | None"],
}, extra_items="object")

SourceSelector = TypedDict("SourceSelector", {
    "object": NotRequired["str | None"],
    "type": NotRequired["str | None"],
    "kind": NotRequired["str | StringArray | None"],
    "kinds": NotRequired["str | StringArray | None"],
    "designators": NotRequired["str | StringArray | None"],
    "hole_size_mils": NotRequired["MilRange | None"],
    "plated": NotRequired["bool | None"],
}, extra_items="object")

Graphics = TypedDict("Graphics", {
    "enabled": NotRequired["bool | None"],
    "layer": NotRequired["str | None"],
    "stroke_width_mils": NotRequired["float"],
}, extra_items="object")

SelectedComponent = TypedDict("SelectedComponent", {
    "mate_projection_id": NotRequired["str | None"],
    "mate_part_role": NotRequired["str | None"],
    "mate_component": NotRequired["MateComponentSettings | None"],
    "mate_pcb_label": NotRequired["Labels | None"],
    "mate_reference_graphics": NotRequired["ReferenceGraphics | None"],
    "source_power_port": NotRequired["InputPowerPort | None"],
    "source_pad_geometries": NotRequired["list[InputPadGeometry] | None"],
    "designator": NotRequired["str"],
    "kind": NotRequired["str"],
    "layer": NotRequired["str"],
    "footprint": NotRequired["str"],
    "x_mils": NotRequired["float"],
    "y_mils": NotRequired["float"],
    "net_name": NotRequired["str | None"],
}, extra_items="object")

SelectedPad = TypedDict("SelectedPad", {
    "mate_projection_id": NotRequired["str | None"],
    "mate_part_role": NotRequired["str | None"],
    "mate_component": NotRequired["MateComponentSettings | None"],
    "mate_pcb_label": NotRequired["Labels | None"],
    "mate_reference_graphics": NotRequired["ReferenceGraphics | None"],
    "source_power_port": NotRequired["InputPowerPort | None"],
    "source_pad_geometries": NotRequired["list[InputPadGeometry] | None"],
    "designator": NotRequired["str"],
    "kind": NotRequired["str"],
    "x_mils": NotRequired["float"],
    "y_mils": NotRequired["float"],
    "net_name": NotRequired["str | None"],
    "width_mils": NotRequired["float"],
    "height_mils": NotRequired["float"],
    "hole_size_mils": NotRequired["float"],
    "shape": NotRequired["int"],
    "layer": NotRequired["int"],
    "rotation_degrees": NotRequired["float"],
}, extra_items="object")

InputOutline = TypedDict("InputOutline", {
    "vertices": "list[InputVertex]",
    "closed": NotRequired["bool"],
    "cutouts": NotRequired["list[InputOutline | list[InputVertex]] | None"],
}, extra_items="object")

Margins = TypedDict("Margins", {
    "left": NotRequired["float"],
    "bottom": NotRequired["float"],
    "right": NotRequired["float"],
    "top": NotRequired["float"],
}, extra_items="object")

BoardOutline = TypedDict("BoardOutline", {
    "color": NotRequired["Color"],
    "cutout_color": NotRequired["Color"],
    "cutouts_color": NotRequired["Color"],
    "cutouts": NotRequired["bool"],
    "width_mm": NotRequired["float"],
    "fuse": NotRequired["bool"],
}, closed=True)

Features = TypedDict("Features", {
    "defaults": NotRequired["FeatureDefaults"],
    "tracks": NotRequired["FeatureSwitch"],
    "traces": NotRequired["FeatureSwitch"],
    "arcs": NotRequired["FeatureSwitch"],
    "fills": NotRequired["FeatureSwitch"],
    "polygons": NotRequired["FeatureSwitch"],
    "poured_polygons": NotRequired["FeatureSwitch"],
    "regions": NotRequired["FeatureSwitch"],
    "shapebased_regions": NotRequired["FeatureSwitch"],
    "vias": NotRequired["FeatureSwitch"],
    "component_pads": NotRequired["FeaturesComponentPads"],
    "free_pads": NotRequired["FeatureSwitch"],
}, closed=True)

Drills = TypedDict("Drills", {
    "mode": NotRequired["DrillMode"],
    "minimum_diameter_mm": NotRequired["float"],
    "shape": NotRequired["DrillShape"],
    "color": NotRequired["Color"],
    "plated_color": NotRequired["Color"],
    "non_plated_color": NotRequired["Color"],
    "ring_width_mm": NotRequired["float"],
    "plated_ring_shape": NotRequired["PlatedRingShape"],
    "selected_component_mode": NotRequired["DrillScopedMode"],
    "other_component_mode": NotRequired["DrillScopedMode"],
    "free_pad_mode": NotRequired["DrillScopedMode"],
    "via_mode": NotRequired["DrillScopedMode"],
    "overlay_thickness_mm": NotRequired["float"],
}, closed=True)

InsertArtifact = TypedDict("InsertArtifact", {
    "enabled": NotRequired["bool | None"],
    "name": NotRequired["str | None"],
    "layer": NotRequired["str | None"],
    "side": NotRequired["str | None"],
    "location_mils": NotRequired["Pair | None"],
    "z_mm": NotRequired["float | None"],
    "rotation_z_degrees": NotRequired["float | None"],
    "opacity": NotRequired["float | None"],
    "bounds_mils": NotRequired["Bounds | BoundsArray | None"],
}, extra_items="object")

Highlight = TypedDict("Highlight", {
    "projection": "str",
    "name": NotRequired["str | None"],
    "color": NotRequired["str | None"],
    "z_offset_mm": NotRequired["float | None"],
    "thickness_mm": NotRequired["float | None"],
}, extra_items="object")

MilRange = TypedDict("MilRange", {
    "min": NotRequired["float | None"],
    "max": NotRequired["float | None"],
}, extra_items="object")

ComponentAction = TypedDict("ComponentAction", {
    "part": NotRequired["str | None"],
    "role": NotRequired["str | None"],
    "description": NotRequired["str | None"],
    "symbol_name": NotRequired["str | None"],
    "footprint_name": NotRequired["str | None"],
    "designator_prefix": NotRequired["str | None"],
    "signal_pad_designator": NotRequired["str | None"],
    "kind": "Literal[\"mate_component\"]",
}, extra_items="object")

ReferenceAction = TypedDict("ReferenceAction", {
    "kind": "Literal[\"reference_graphics\"]",
    "shape": NotRequired["Literal[\"source_pad_outline\"] | Literal[\"destination_pad_outline\"] | None"],
    "layer": NotRequired["str | None"],
    "enabled": NotRequired["bool | None"],
    "style": NotRequired["ReferenceStyle"],
}, extra_items="object")

LabelAction = TypedDict("LabelAction", {
    "kind": "Literal[\"label\"]",
    "enabled": NotRequired["bool | None"],
    "style": NotRequired["TextStyle | None"],
    "text": NotRequired["str | None"],
    "value": NotRequired["str | None"],
    "placement": NotRequired["LabelPlacement | None"],
}, extra_items="object")

MateComponentSettings = TypedDict("MateComponentSettings", {
    "kind": NotRequired["Literal[\"mate_component\"]"],
    "part": NotRequired["str | None"],
    "role": NotRequired["str | None"],
    "description": NotRequired["str | None"],
    "symbol_name": NotRequired["str | None"],
    "footprint_name": NotRequired["str | None"],
    "designator_prefix": NotRequired["str | None"],
    "signal_pad_designator": NotRequired["str | None"],
}, extra_items="object")

ReferenceGraphics = TypedDict("ReferenceGraphics", {
    "enabled": NotRequired["bool | None"],
    "layer": NotRequired["str | None"],
    "shape": NotRequired["Literal[\"source_pad_outline\"] | Literal[\"destination_pad_outline\"] | None"],
    "style": NotRequired["ReferenceStyle"],
}, extra_items="object")

InputPowerPort = TypedDict("InputPowerPort", {
    "text": NotRequired["str | None"],
    "style": NotRequired["str | None"],
    "show_net_name": NotRequired["bool"],
}, extra_items="object")

InputPadGeometry = TypedDict("InputPadGeometry", {
    "x_mils": NotRequired["float"],
    "y_mils": NotRequired["float"],
    "width_mils": NotRequired["float"],
    "height_mils": NotRequired["float"],
    "shape": NotRequired["int"],
    "layer": NotRequired["int"],
    "rotation_degrees": NotRequired["float"],
    "corner_radius_mils": NotRequired["float"],
}, extra_items="object")

InputVertex = TypedDict("InputVertex", {
    "x_mils": "float",
    "y_mils": "float",
    "segment": NotRequired["Literal[\"line\"] | Literal[\"arc\"] | None"],
    "center_mils": NotRequired["Pair"],
    "radius_mils": NotRequired["float"],
    "start_angle_degrees": NotRequired["float"],
    "end_angle_degrees": NotRequired["float"],
}, extra_items="object")

FeatureDefaults = TypedDict("FeatureDefaults", {
    "color": NotRequired["Color"],
}, closed=True)

ReferenceStyle = TypedDict("ReferenceStyle", {
    "mode": NotRequired["str | None"],
    "outline_count": NotRequired["int | None"],
    "clearance_mils": NotRequired["float"],
    "outline_spacing_mils": NotRequired["float"],
    "stroke_width_mils": NotRequired["float"],
}, extra_items="object")

LabelPlacement = TypedDict("LabelPlacement", {
    "side": NotRequired["Literal[\"left\"] | Literal[\"right\"] | Literal[\"board_left\"] | Literal[\"board_right\"] | None"],
    "offset_mils": NotRequired["Pair | None"],
    "box_size_mils": NotRequired["Pair | None"],
    "center_box_on_target": NotRequired["bool | None"],
    "row_spacing_mils": NotRequired["float | None"],
    "column_spacing_mils": NotRequired["float | None"],
    "auto_width_padding_mils": NotRequired["float | None"],
}, extra_items="object")

FeatureSwitchOption2 = TypedDict("FeatureSwitchOption2", {
    "enabled": NotRequired["bool"],
    "color": NotRequired["Color"],
    "step_body_name": NotRequired["str"],
    "thickness_bias_mm": NotRequired["float"],
}, closed=True)

ComponentPads = TypedDict("ComponentPads", {
    "enabled": NotRequired["bool"],
    "mode": NotRequired["Literal[\"none\"] | Literal[\"all\"] | Literal[\"matching_designators\"]"],
    "include_designators": NotRequired["StringList"],
    "color": NotRequired["Color"],
    "step_body_name": NotRequired["str"],
    "thickness_bias_mm": NotRequired["float"],
    "highlight_rules": NotRequired["HighlightRules"],
}, closed=True)

HighlightRulesValueItem = TypedDict("HighlightRulesValueItem", {
    "designators": "StringList",
    "color": "Color",
    "step_body_name": NotRequired["str"],
}, closed=True)

CurrentMate_source = TypedDict("CurrentMate_source", {
    "board": NotRequired["str | None"],
    "pcbdoc": NotRequired["str | None"],
    "project_context": NotRequired["Literal[\"auto\"] | Literal[\"none\"] | Literal[\"schematic\"] | None"],
}, closed=True)

LegacyMate_source = TypedDict("LegacyMate_source", {
    "dut": NotRequired["str | None"],
}, closed=True)

LegacyMate_marker = TypedDict("LegacyMate_marker", {
    "enabled": NotRequired["bool | None"],
    "text": NotRequired["str | None"],
    "position_mils": NotRequired["Pair | None"],
    "height_mils": NotRequired["float | None"],
    "layer": NotRequired["str | None"],
}, closed=True)

LegacyMate_placement = TypedDict("LegacyMate_placement", {
    "source_mount_side": NotRequired["str | None"],
    "offset_mils": NotRequired["Pair | None"],
    "mirror_x": NotRequired["bool | None"],
    "mirror_y": NotRequired["bool | None"],
    "mirror_origin_mils": NotRequired["Pair | None"],
}, closed=True)

LegacyMate_selection = TypedDict("LegacyMate_selection", {
    "boards": NotRequired["list[SelectedBoard]"],
}, closed=True)

Projection_select = TypedDict("Projection_select", {
    "components": NotRequired["SourceSelector"],
    "free_pads": NotRequired["SourceSelector"],
}, closed=True)

BoardProjection_outline = TypedDict("BoardProjection_outline", {
    "graphics": NotRequired["Graphics"],
}, closed=True)

BoardProjection_cutouts = TypedDict("BoardProjection_cutouts", {
    "graphics": NotRequired["Graphics"],
    "scope": NotRequired["Literal[\"all\"] | Literal[\"interior\"] | None"],
    "actual_cutouts": NotRequired["bool | None"],
    "layer": NotRequired["str | None"],
}, closed=True)

MateConfigInput = CurrentMate | LegacyMate
RecordUnknown = dict[str, object]
Pair = list[float]
StringArray = list[str]
ProjectionAction = ComponentAction | ReferenceAction | LabelAction
Nonnegative = float
Color = str
DrillMode = Literal["auto"] | Literal["cut"] | Literal["overlay"] | Literal["none"]
DrillShape = Literal["solid"] | Literal["ring"]
PlatedRingShape = Literal["annulus"]
DrillScopedMode = Literal["inherit"] | Literal["cut"] | Literal["overlay"] | Literal["none"]
StringList = str | list[str]
FeatureSwitch = bool | FeatureSwitchOption2
FeaturesComponentPads = bool | ComponentPads
BoundsArray = list[float]
HighlightRules = list[HighlightRulesValueItem]
