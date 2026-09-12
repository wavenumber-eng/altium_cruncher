"""Generated from src/tsp/altium_cruncher/mco/main.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

McoDocument = TypedDict("McoDocument", {
    "schema": NotRequired["Literal[\"altium_cruncher.mco.a0\"] | None"],
    "operations": "list[BuiltinOperation | CustomOperation]",
}, extra_items="object")

CustomOperation = TypedDict("CustomOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "McoString",
    "args": NotRequired["RecordUnknown"],
}, extra_items="object")

FileCopyOperation = TypedDict("FileCopyOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"file.copy\"]",
    "args": "FileCopyArgs",
}, extra_items="object")

McoFailOperation = TypedDict("McoFailOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"mco.fail\"] | Literal[\"fail\"]",
    "args": NotRequired["McoFailArgs"],
}, extra_items="object")

McoMessageOperation = TypedDict("McoMessageOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"mco.message\"] | Literal[\"message\"]",
    "args": NotRequired["McoMessageArgs"],
}, extra_items="object")

PcbdocAddArcOperation = TypedDict("PcbdocAddArcOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"pcbdoc.add_arc\"]",
    "args": "PcbdocAddArcArgs",
}, extra_items="object")

PcbdocAddComponentOperation = TypedDict("PcbdocAddComponentOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"pcbdoc.add_component\"]",
    "args": "PcbdocAddComponentArgs",
}, extra_items="object")

PcbdocAddEmbedded3dModelOperation = TypedDict("PcbdocAddEmbedded3dModelOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"pcbdoc.add_embedded_3d_model\"]",
    "args": "PcbdocAddEmbedded3dModelArgs",
}, extra_items="object")

PcbdocAddFillOperation = TypedDict("PcbdocAddFillOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"pcbdoc.add_fill\"]",
    "args": "PcbdocAddFillArgs",
}, extra_items="object")

PcbdocAddPadOperation = TypedDict("PcbdocAddPadOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"pcbdoc.add_pad\"]",
    "args": "PcbdocAddPadArgs",
}, extra_items="object")

PcbdocAddRegionOperation = TypedDict("PcbdocAddRegionOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"pcbdoc.add_region\"]",
    "args": "PcbdocAddRegionArgs",
}, extra_items="object")

PcbdocAddTextOperation = TypedDict("PcbdocAddTextOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"pcbdoc.add_text\"]",
    "args": "PcbdocAddTextArgs",
}, extra_items="object")

PcbdocAddTrackOperation = TypedDict("PcbdocAddTrackOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"pcbdoc.add_track\"]",
    "args": "PcbdocAddTrackArgs",
}, extra_items="object")

PcbdocAddViaOperation = TypedDict("PcbdocAddViaOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"pcbdoc.add_via\"]",
    "args": "PcbdocAddViaArgs",
}, extra_items="object")

PcbdocArrangeDesignatorsOperation = TypedDict("PcbdocArrangeDesignatorsOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"pcbdoc.arrange_designators\"]",
    "args": "PcbdocArrangeDesignatorsArgs",
}, extra_items="object")

PcbdocCreateOperation = TypedDict("PcbdocCreateOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"pcbdoc.create\"]",
    "args": "PcbdocCreateArgs",
}, extra_items="object")

PcbdocCreateUserUnionOperation = TypedDict("PcbdocCreateUserUnionOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"pcbdoc.create_user_union\"]",
    "args": "PcbdocCreateUserUnionArgs",
}, extra_items="object")

PcbdocExportLayerStepOperation = TypedDict("PcbdocExportLayerStepOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"pcbdoc.export_layer_step\"]",
    "args": "PcbdocExportLayerStepArgs",
}, extra_items="object")

PcblibAddFootprintOperation = TypedDict("PcblibAddFootprintOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"pcblib.add_footprint\"]",
    "args": "PcblibAddFootprintArgs",
}, extra_items="object")

PcblibCreateOperation = TypedDict("PcblibCreateOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"pcblib.create\"]",
    "args": "PcblibCreateArgs",
}, extra_items="object")

ProjectAddDocumentOperation = TypedDict("ProjectAddDocumentOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"project.add_document\"]",
    "args": "ProjectAddDocumentArgs",
}, extra_items="object")

ProjectAddParameterOperation = TypedDict("ProjectAddParameterOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"project.add_parameter\"]",
    "args": "ProjectAddParameterArgs",
}, extra_items="object")

ProjectAddVariantOperation = TypedDict("ProjectAddVariantOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"project.add_variant\"]",
    "args": "ProjectAddVariantArgs",
}, extra_items="object")

ProjectAddVariantDnpOperation = TypedDict("ProjectAddVariantDnpOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"project.add_variant_dnp\"]",
    "args": "ProjectAddVariantDnpArgs",
}, extra_items="object")

ProjectCloneVariantOperation = TypedDict("ProjectCloneVariantOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"project.clone_variant\"]",
    "args": "ProjectCloneVariantArgs",
}, extra_items="object")

ProjectCreateOperation = TypedDict("ProjectCreateOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"project.create\"]",
    "args": "ProjectCreateArgs",
}, extra_items="object")

ProjectDeleteVariantOperation = TypedDict("ProjectDeleteVariantOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"project.delete_variant\"]",
    "args": "ProjectDeleteVariantArgs",
}, extra_items="object")

ProjectListVariantsOperation = TypedDict("ProjectListVariantsOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"project.list_variants\"]",
    "args": "ProjectListVariantsArgs",
}, extra_items="object")

ProjectRenameVariantOperation = TypedDict("ProjectRenameVariantOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"project.rename_variant\"]",
    "args": "ProjectRenameVariantArgs",
}, extra_items="object")

ProjectToggleVariantDnpOperation = TypedDict("ProjectToggleVariantDnpOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"project.toggle_variant_dnp\"]",
    "args": "ProjectToggleVariantDnpArgs",
}, extra_items="object")

SchdocAddComponentOperation = TypedDict("SchdocAddComponentOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"schdoc.add_component\"]",
    "args": "SchdocAddComponentArgs",
}, extra_items="object")

SchdocAddNetLabelOperation = TypedDict("SchdocAddNetLabelOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"schdoc.add_net_label\"]",
    "args": "SchdocAddNetLabelArgs",
}, extra_items="object")

SchdocAddPowerPortOperation = TypedDict("SchdocAddPowerPortOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"schdoc.add_power_port\"]",
    "args": "SchdocAddPowerPortArgs",
}, extra_items="object")

SchdocAddWireOperation = TypedDict("SchdocAddWireOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"schdoc.add_wire\"]",
    "args": "SchdocAddWireArgs",
}, extra_items="object")

SchdocCreateOperation = TypedDict("SchdocCreateOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"schdoc.create\"]",
    "args": "SchdocCreateArgs",
}, extra_items="object")

SchlibAddSymbolOperation = TypedDict("SchlibAddSymbolOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"schlib.add_symbol\"]",
    "args": "SchlibAddSymbolArgs",
}, extra_items="object")

SchlibCreateOperation = TypedDict("SchlibCreateOperation", {
    "id": NotRequired["str | None"],
    "message": NotRequired["str | None"],
    "on_fail": NotRequired["str | None"],
    "op": "Literal[\"schlib.create\"]",
    "args": "SchlibCreateArgs",
}, extra_items="object")

FileCopyArgs = TypedDict("FileCopyArgs", {
    "source": "McoString",
    "destination": "McoString",
    "overwrite": NotRequired["bool | None"],
}, extra_items="object")

McoFailArgs = TypedDict("McoFailArgs", {
    "message": NotRequired["str | None"],
}, extra_items="object")

McoMessageArgs = TypedDict("McoMessageArgs", {
    "text": NotRequired["str | None"],
}, extra_items="object")

PcbdocAddArcArgs = TypedDict("PcbdocAddArcArgs", {
    "file": "McoString",
    "output_file": NotRequired["str | None"],
    "overwrite": NotRequired["bool | None"],
    "center_mils": "PointMils",
    "radius_mils": "float",
    "start_angle_degrees": "float",
    "end_angle_degrees": "float",
    "width_mils": "float",
    "layer": NotRequired["str | int | None"],
    "net": NotRequired["str | None"],
}, extra_items="object")

PcbdocAddComponentArgs = TypedDict("PcbdocAddComponentArgs", {
    "file": "McoString",
    "output_file": NotRequired["str | None"],
    "overwrite": NotRequired["bool | None"],
    "library": "McoString",
    "footprint": "McoString",
    "designator": "McoString",
    "position_mils": "PointMils",
    "layer": NotRequired["str | int | None"],
    "source_unique_id": NotRequired["str | None"],
    "source_hierarchical_path": NotRequired["str | None"],
    "source_component_library": NotRequired["str | None"],
    "source_lib_reference": NotRequired["str | None"],
    "source_description": NotRequired["str | None"],
    "channel_offset": NotRequired["int | None"],
    "comment_text": NotRequired["str | None"],
    "component_parameters": NotRequired["RecordString | None"],
    "pad_nets": NotRequired["RecordString | None"],
    "rotation_degrees": NotRequired["float | None"],
    "source_footprint_library": NotRequired["str | None"],
    "comment_visible": NotRequired["bool | None"],
    "source_designator": NotRequired["str | None"],
}, extra_items="object")

PcbdocAddEmbedded3dModelArgs = TypedDict("PcbdocAddEmbedded3dModelArgs", {
    "file": "McoString",
    "output_file": NotRequired["str | None"],
    "overwrite": NotRequired["bool | None"],
    "model_file": "McoString",
    "model_name": NotRequired["str | None"],
    "name": NotRequired["str | None"],
    "layer": NotRequired["str | int | None"],
    "side": NotRequired["str | int | None"],
    "location_mils": NotRequired["PointMils | None"],
    "rotation_x_degrees": NotRequired["float | None"],
    "rotation_y_degrees": NotRequired["float | None"],
    "rotation_z_degrees": NotRequired["float | None"],
    "z_mm": NotRequired["float | None"],
    "bounds_mils": NotRequired["BoundsObject | BoundsArray | None"],
    "projection_outline_mils": NotRequired["RegionPoints | None"],
    "overall_height_mils": NotRequired["float | None"],
    "opacity": NotRequired["float | None"],
    "z_mils": NotRequired["float"],
}, extra_items="object")

PcbdocAddFillArgs = TypedDict("PcbdocAddFillArgs", {
    "file": "McoString",
    "output_file": NotRequired["str | None"],
    "overwrite": NotRequired["bool | None"],
    "corner1_mils": "PointMils",
    "corner2_mils": "PointMils",
    "rotation_degrees": NotRequired["float | None"],
    "layer": NotRequired["str | int | None"],
    "net": NotRequired["str | None"],
}, extra_items="object")

PcbdocAddPadArgs = TypedDict("PcbdocAddPadArgs", {
    "file": "McoString",
    "output_file": NotRequired["str | None"],
    "overwrite": NotRequired["bool | None"],
    "designator": "McoString",
    "position_mils": "PointMils",
    "width_mils": "float",
    "height_mils": "float",
    "shape": NotRequired["str | int | None"],
    "corner_radius_percent": NotRequired["float | None"],
    "rotation_degrees": NotRequired["float | None"],
    "hole_size_mils": NotRequired["float | None"],
    "plated": NotRequired["bool | None"],
    "layer": NotRequired["str | int | None"],
    "net": NotRequired["str | None"],
    "solder_mask_expansion_mils": NotRequired["float | None"],
    "paste_mask_expansion_mils": NotRequired["float | None"],
    "tenting_top": NotRequired["bool | None"],
    "tenting_bottom": NotRequired["bool | None"],
    "solder_mask_expansion_mode": NotRequired["int | None"],
    "paste_mask_expansion_mode": NotRequired["int | None"],
}, extra_items="object")

PcbdocAddRegionArgs = TypedDict("PcbdocAddRegionArgs", {
    "file": "McoString",
    "output_file": NotRequired["str | None"],
    "overwrite": NotRequired["bool | None"],
    "outline_points_mils": "RegionPoints",
    "layer": NotRequired["str | int | None"],
    "hole_points_mils": NotRequired["list[list[PointMils]] | None"],
    "is_keepout": NotRequired["bool | None"],
    "keepout_restrictions": NotRequired["float | None"],
    "net": NotRequired["str | None"],
    "is_board_cutout": NotRequired["bool | None"],
}, extra_items="object")

PcbdocAddTextArgs = TypedDict("PcbdocAddTextArgs", {
    "file": "McoString",
    "output_file": NotRequired["str | None"],
    "overwrite": NotRequired["bool | None"],
    "text": "McoString",
    "position_mils": "PointMils",
    "layer": NotRequired["str | int | None"],
    "height_mils": "float",
    "font_kind": NotRequired["str | None"],
    "font_name": NotRequired["str | None"],
    "bold": NotRequired["bool | None"],
    "italic": NotRequired["bool | None"],
    "rotation_degrees": NotRequired["float | None"],
    "stroke_width_mils": NotRequired["float | None"],
    "is_comment": NotRequired["bool | None"],
    "is_designator": NotRequired["bool | None"],
    "is_mirrored": NotRequired["bool | None"],
    "is_inverted": NotRequired["bool | None"],
    "inverted_margin_mils": NotRequired["float | None"],
    "use_inverted_rectangle": NotRequired["bool | None"],
    "inverted_rectangle_size_mils": NotRequired["PointMils | None"],
    "is_frame": NotRequired["bool | None"],
    "frame_size_mils": NotRequired["PointMils | None"],
    "barcode_full_size_mils": NotRequired["PointMils | None"],
    "barcode_margin_mils": NotRequired["PointMils | None"],
    "barcode_min_width_mils": NotRequired["float | None"],
    "barcode_show_text": NotRequired["bool | None"],
    "barcode_inverted": NotRequired["bool | None"],
    "text_justification": NotRequired["str | int | None"],
    "barcode_kind": NotRequired["str | int | None"],
    "barcode_render_mode": NotRequired["str | int | None"],
}, extra_items="object")

PcbdocAddTrackArgs = TypedDict("PcbdocAddTrackArgs", {
    "file": "McoString",
    "output_file": NotRequired["str | None"],
    "overwrite": NotRequired["bool | None"],
    "start_mils": "PointMils",
    "end_mils": "PointMils",
    "width_mils": "float",
    "layer": NotRequired["str | int | None"],
    "net": NotRequired["str | None"],
}, extra_items="object")

PcbdocAddViaArgs = TypedDict("PcbdocAddViaArgs", {
    "file": "McoString",
    "output_file": NotRequired["str | None"],
    "overwrite": NotRequired["bool | None"],
    "position_mils": "PointMils",
    "diameter_mils": "float",
    "hole_size_mils": "float",
    "layer_start": NotRequired["str | int | None"],
    "layer_end": NotRequired["str | int | None"],
    "net": NotRequired["str | None"],
}, extra_items="object")

PcbdocArrangeDesignatorsArgs = TypedDict("PcbdocArrangeDesignatorsArgs", {
    "file": "McoString",
    "output_file": NotRequired["str | None"],
    "overwrite": NotRequired["bool | None"],
    "designators": NotRequired["list[McoString] | None"],
    "placement": NotRequired["str | None"],
    "offset_mils": NotRequired["PointMils | None"],
    "height_mils": NotRequired["float | None"],
    "layer": NotRequired["str | int | None"],
    "stroke_width_mils": NotRequired["float | None"],
    "width_factor": NotRequired["float | None"],
    "bold": NotRequired["bool | None"],
    "italic": NotRequired["bool | None"],
    "font_name": NotRequired["str | None"],
    "font_kind": NotRequired["str | None"],
}, extra_items="object")

PcbdocCreateArgs = TypedDict("PcbdocCreateArgs", {
    "file": "McoString",
    "layer_stack_template": NotRequired["str | None"],
    "rigid_stack": NotRequired["RigidLayerStack | None"],
    "stackupx_file": NotRequired["McoString | None"],
    "board_outline_mils": NotRequired["BoardOutlineMils | None"],
    "board_origin_mils": NotRequired["OriginMils | None"],
    "sheet_frame_mils": NotRequired["SheetFrameMils | None"],
    "mechanical_layer_profile": NotRequired["str | None"],
    "mechanical_layers": NotRequired["list[McoMechanicalLayer] | None"],
    "mechanical_layer_pairs": NotRequired["list[McoMechanicalPair] | None"],
    "mechanical_layer_kinds": NotRequired["list[McoMechanicalKind] | None"],
    "overwrite": NotRequired["bool | None"],
}, extra_items="object")

PcbdocCreateUserUnionArgs = TypedDict("PcbdocCreateUserUnionArgs", {
    "file": "McoString",
    "output_file": NotRequired["str | None"],
    "overwrite": NotRequired["bool | None"],
    "name": "McoString",
    "members": NotRequired["Literal[\"all\"] | None"],
}, extra_items="object")

PcbdocExportLayerStepArgs = TypedDict("PcbdocExportLayerStepArgs", {
    "file": "McoString",
    "output_file": "McoString",
    "layer": NotRequired["str | int | None"],
    "board_name": NotRequired["str | None"],
    "highlights": NotRequired["list[LayerStepHighlight] | None"],
    "overwrite": NotRequired["bool | None"],
}, extra_items="object")

PcblibAddFootprintArgs = TypedDict("PcblibAddFootprintArgs", {
    "file": "McoString",
    "output_file": NotRequired["str | None"],
    "overwrite": NotRequired["bool | None"],
    "name": "McoString",
    "height": NotRequired["str | None"],
    "description": NotRequired["str | None"],
    "item_guid": NotRequired["str | None"],
    "revision_guid": NotRequired["str | None"],
    "parameters": NotRequired["RecordString | None"],
    "primitive_parameters": NotRequired["RecordString | None"],
}, extra_items="object")

PcblibCreateArgs = TypedDict("PcblibCreateArgs", {
    "file": "McoString",
    "overwrite": NotRequired["bool | None"],
}, extra_items="object")

ProjectAddDocumentArgs = TypedDict("ProjectAddDocumentArgs", {
    "file": "McoString",
    "document": "McoString",
    "unique_id": NotRequired["str | None"],
}, extra_items="object")

ProjectAddParameterArgs = TypedDict("ProjectAddParameterArgs", {
    "file": "McoString",
    "name": "McoString",
    "value": "McoString",
}, extra_items="object")

ProjectAddVariantArgs = TypedDict("ProjectAddVariantArgs", {
    "file": "McoString",
    "name": "McoString",
    "unique_id": NotRequired["str | None"],
    "allow_fabrication": NotRequired["bool | None"],
    "current": NotRequired["bool | None"],
}, extra_items="object")

ProjectAddVariantDnpArgs = TypedDict("ProjectAddVariantDnpArgs", {
    "file": "McoString",
    "variant": "McoString",
    "designator": "McoString",
    "unique_id": NotRequired["str | None"],
    "alternate_part": NotRequired["str | None"],
}, extra_items="object")

ProjectCloneVariantArgs = TypedDict("ProjectCloneVariantArgs", {
    "file": "McoString",
    "source_name": "McoString",
    "name": "McoString",
    "unique_id": NotRequired["str | None"],
    "allow_fabrication": NotRequired["bool | None"],
    "current": NotRequired["bool | None"],
}, extra_items="object")

ProjectCreateArgs = TypedDict("ProjectCreateArgs", {
    "file": "McoString",
    "name": NotRequired["str | None"],
    "project_name": NotRequired["str | None"],
    "overwrite": NotRequired["bool | None"],
}, extra_items="object")

ProjectDeleteVariantArgs = TypedDict("ProjectDeleteVariantArgs", {
    "file": "McoString",
    "name": "McoString",
}, extra_items="object")

ProjectListVariantsArgs = TypedDict("ProjectListVariantsArgs", {
    "file": "McoString",
}, extra_items="object")

ProjectRenameVariantArgs = TypedDict("ProjectRenameVariantArgs", {
    "file": "McoString",
    "name": "McoString",
    "new_name": "McoString",
}, extra_items="object")

ProjectToggleVariantDnpArgs = TypedDict("ProjectToggleVariantDnpArgs", {
    "file": "McoString",
    "variant": "McoString",
    "designator": "McoString",
    "unique_id": NotRequired["str | None"],
    "alternate_part": NotRequired["str | None"],
}, extra_items="object")

SchdocAddComponentArgs = TypedDict("SchdocAddComponentArgs", {
    "file": "McoString",
    "output_file": NotRequired["str | None"],
    "overwrite": NotRequired["bool | None"],
    "library": "McoString",
    "symbol": "McoString",
    "designator": "McoString",
    "position_mils": "PointMils",
    "unique_id": NotRequired["str | None"],
    "design_item_id": NotRequired["str | None"],
    "footprint_model": NotRequired["str | None"],
    "footprint_library": NotRequired["str | None"],
    "parameters": NotRequired["RecordString | None"],
    "orientation": NotRequired["float | None"],
    "mirrored": NotRequired["bool | None"],
    "part_id": NotRequired["float | None"],
    "display_mode": NotRequired["float | None"],
    "designator_style": NotRequired["SchematicTextStyle | None"],
    "comment_style": NotRequired["SchematicTextStyle | None"],
    "footprint_description": NotRequired["str | None"],
}, extra_items="object")

SchdocAddNetLabelArgs = TypedDict("SchdocAddNetLabelArgs", {
    "file": "McoString",
    "output_file": NotRequired["str | None"],
    "overwrite": NotRequired["bool | None"],
    "text": "McoString",
    "location_mils": "PointMils",
    "orientation": NotRequired["str | int | None"],
    "justification": NotRequired["str | int"],
}, extra_items="object")

SchdocAddPowerPortArgs = TypedDict("SchdocAddPowerPortArgs", {
    "file": "McoString",
    "output_file": NotRequired["str | None"],
    "overwrite": NotRequired["bool | None"],
    "text": "McoString",
    "location_mils": "PointMils",
    "style": NotRequired["str | int"],
    "orientation": NotRequired["str | int | None"],
    "show_net_name": NotRequired["bool | None"],
}, extra_items="object")

SchdocAddWireArgs = TypedDict("SchdocAddWireArgs", {
    "file": "McoString",
    "output_file": NotRequired["str | None"],
    "overwrite": NotRequired["bool | None"],
    "points_mils": "WirePoints",
}, extra_items="object")

SchdocCreateArgs = TypedDict("SchdocCreateArgs", {
    "file": "McoString",
    "template": NotRequired["McoString | None"],
    "sheet_style": NotRequired["str | None"],
    "apply_template_visual_sheet_settings": NotRequired["bool | None"],
    "custom_sheet_mils": NotRequired["CustomSheetMils | None"],
    "overwrite": NotRequired["bool | None"],
}, extra_items="object")

SchlibAddSymbolArgs = TypedDict("SchlibAddSymbolArgs", {
    "file": "McoString",
    "name": "McoString",
    "description": NotRequired["str | None"],
}, extra_items="object")

SchlibCreateArgs = TypedDict("SchlibCreateArgs", {
    "file": "McoString",
    "overwrite": NotRequired["bool | None"],
}, extra_items="object")

BoundsObject = TypedDict("BoundsObject", {
    "left": "float",
    "bottom": "float",
    "right": "float",
    "top": "float",
}, extra_items="object")

RigidLayerStack = TypedDict("RigidLayerStack", {
    "mode": NotRequired["Literal[\"generated_rigid\"] | None"],
    "name": NotRequired["str | None"],
    "copper_layers": "list[CopperLayer]",
    "dielectrics_between": "list[DielectricLayer]",
}, extra_items="object")

BoardOutlineMils = TypedDict("BoardOutlineMils", {
    "left": "float | bool",
    "bottom": "float | bool",
    "right": "float | bool",
    "top": "float | bool",
}, extra_items="object")

OriginMils = TypedDict("OriginMils", {
    "x": "float | bool",
    "y": "float | bool",
}, extra_items="object")

SheetFrameMils = TypedDict("SheetFrameMils", {
    "x": "float | bool",
    "y": "float | bool",
    "width": "float | bool",
    "height": "float | bool",
}, extra_items="object")

McoMechanicalLayer = TypedDict("McoMechanicalLayer", {
    "layer": "McoString",
    "name": NotRequired["str | None"],
    "enabled": NotRequired["bool | None"],
}, extra_items="object")

McoMechanicalPair = TypedDict("McoMechanicalPair", {
    "layer_1": "McoString",
    "layer_2": "McoString",
    "pair_index": NotRequired["int | None"],
}, extra_items="object")

McoMechanicalKind = TypedDict("McoMechanicalKind", {
    "layer": "McoString",
    "kind": "str | int | bool",
}, extra_items="object")

LayerStepHighlight = TypedDict("LayerStepHighlight", {
    "id": "McoString",
    "name": NotRequired["str | None"],
    "color": "McoString",
    "pad_geometries": NotRequired["list[object]"],
    "z_offset_mm": NotRequired["float | None"],
    "thickness_mm": NotRequired["float | None"],
}, extra_items="object")

SchematicTextStyle = TypedDict("SchematicTextStyle", {
    "position_mils": NotRequired["PointMils | None"],
    "font_name": NotRequired["str | None"],
    "font_size": NotRequired["float | None"],
    "bold": NotRequired["bool | None"],
    "justification": NotRequired["str | int | None"],
    "hidden": NotRequired["bool | None"],
    "visible": NotRequired["bool | None"],
}, extra_items="object")

CustomSheetMils = TypedDict("CustomSheetMils", {
    "width": "float | bool",
    "height": "float | bool",
}, extra_items="object")

CopperLayer = TypedDict("CopperLayer", {
    "name": "NonemptyString",
    "copper_thickness_mils": NotRequired["float | None"],
    "thickness_mils": NotRequired["object"],
    "component_placement": NotRequired["int | None"],
    "copper_orientation": NotRequired["int | None"],
}, extra_items="object")

DielectricLayer = TypedDict("DielectricLayer", {
    "name": "NonemptyString",
    "material": "NonemptyString",
    "thickness_mils": "float",
    "dielectric_constant": "float",
    "dk": NotRequired["object"],
    "dielectric_type": NotRequired["int | None"],
    "type_code": NotRequired["object"],
    "loss_tangent": NotRequired["float | None"],
}, extra_items="object")

BuiltinOperation = FileCopyOperation | McoFailOperation | McoMessageOperation | PcbdocAddArcOperation | PcbdocAddComponentOperation | PcbdocAddEmbedded3dModelOperation | PcbdocAddFillOperation | PcbdocAddPadOperation | PcbdocAddRegionOperation | PcbdocAddTextOperation | PcbdocAddTrackOperation | PcbdocAddViaOperation | PcbdocArrangeDesignatorsOperation | PcbdocCreateOperation | PcbdocCreateUserUnionOperation | PcbdocExportLayerStepOperation | PcblibAddFootprintOperation | PcblibCreateOperation | ProjectAddDocumentOperation | ProjectAddParameterOperation | ProjectAddVariantOperation | ProjectAddVariantDnpOperation | ProjectCloneVariantOperation | ProjectCreateOperation | ProjectDeleteVariantOperation | ProjectListVariantsOperation | ProjectRenameVariantOperation | ProjectToggleVariantDnpOperation | SchdocAddComponentOperation | SchdocAddNetLabelOperation | SchdocAddPowerPortOperation | SchdocAddWireOperation | SchdocCreateOperation | SchlibAddSymbolOperation | SchlibCreateOperation
McoInput = McoDocument | list[BuiltinOperation | CustomOperation]
RecordUnknown = dict[str, object]
McoString = str
PointMils = list[float]
RecordString = dict[str, str]
BoundsArray = list[float]
RegionPoints = list[PointMils]
WirePoints = list[PointMils]
NonemptyString = str
