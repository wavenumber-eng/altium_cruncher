# PCB illustrations

```powershell
acr toon board.PrjPcb --theme white
acr toon board.PrjPcb --side top
acr toon board.PrjPcb --assembly --variant "production"
```

The command creates an editable `toon.config` beside the input,
then reuses it. It exports top and mirrored bottom SVG files.
Use `--side top|bottom|both` to select the board surfaces.
`--write-config PATH` writes a config and exits. Raster conversion is left to
consumers; the command has no PNG, DPI, pixel-width or background options.
Remove `global.png` from older experimental configs.


`--all-variants` exports base plus named project variants to separate folders.
Variant DNP bodies/projected labels are omitted while copper and silkscreen stay;
parameter overrides feed special strings. Alternate-part model substitutions
currently produce an explicit unsupported error. See the
[command contract](../../docs/design/cli/toon.html) for details.

For SVG performance measurements, use `--timings output/timings.json`.
The default four workers handle unique native model requests. `--workers 1`
selects serial execution; `--cache-dir PATH` selects a persistent model/artwork
cache and `--no-cache` disables disk reuse. Project parameters and variants remain
available without loading schematic geometry. Timings include project/board
loading, layers, views and variants; parent durations include their children.

# Solder-mask film

For an outline behind projected assembly designators, add this style globally
or under a view's `styles`:

```json
"assembly_designators": {
  "color": "#FF0000",
  "stroke_color": "#FFFFFF",
  "stroke_width_mm": 0.1
}
```

The full stroke width is in board millimetres; `0` disables it (the general
default). It paints behind the letters, preserving their red interiors, and
does not change their placement or fitted size. The outline remains part of the SVG artwork.
The review helper now generates base plus every named project variant, with
top/bottom illustration and assembly SVG outputs shown on the same page.

```powershell
uv run altium-cruncher pcb-svg board.PcbDoc --config examples/pcb-svg/soldermask-film.config.json -o output/film
```

This config exports top and mirrored bottom film views. `color: "auto"` reads
each side's saved Altium 3D solder-mask color, with a green fallback. Set a CSS
color such as `"#176B3A"` to override it. `opacity` ranges from 0 to 1 and defaults
to 1. Put a `styles.soldermask_film` object inside a view for a per-view override.

Film subtracts saved mask apertures and physical board cutouts/NPTH holes from
the board profile. Apertures are transparent. Copper and silkscreen can be
added explicitly as other layers in the view's draw order.

To add physical drill and slot boundaries and cutout edges, use
`drill-preview.config.json` in the same command. It draws thin black hole
outlines at the actual bore dimensions, with unfilled centers, and keeps
tented vias covered. It does not add copper. The `drills` and `slots` styles
expose `outline`, `outline_width_mm`, and `respect_tenting`; existing configs
keep their filled drill marks unless these options are selected.

`copper-preview.config.json` adds copper underneath the film using the existing
`TOP` layer. Its four views compare pads alone, pads with tracks/arcs/via lands,
and white/green film at different opacities. The gold `#DFC951` is RT_SUPER_C1's
saved 3D copper display color; edit the normal copper style colors to change it.
`soldermask_film.opacity` controls how much covered copper shows through. Board
and drill clipping remain enabled. Copper polygons/fills are disabled in this
example so the pads and routing can be reviewed separately.

`board-preview.config.json` adds top and bottom silkscreen to these surface
views, including component graphics, designators and board artwork. It also
enables saved copper fills and poured regions in the same gold as the routing.
Copper text also uses the existing text renderer, including embedded TrueType fonts,
and follows the `copper_traces` style. These use Altium's saved copper geometry; the exporter does not repour polygons. Bottom
views are mirrored for viewing from underneath. The saved-white versions use
dark silk (`#434343`, RT's saved silk color); the green versions use white silk.
Film opacity is 85% for saved-white and 90% for green. This config exports the
complete illustrated boards through `pcb-svg`.

The board perimeter is a black line. Set
`global.styles.board_outline.line_width_mm` to change its thickness (0.25 mm
in this example); view styles can override it. The stroke scales with the board.

The board preview draws drill holes and slots as solid fills without outline
strokes. Configure `styles.drills.plated_color` / `non_plated_color` and the
corresponding `styles.slots` colors; the preview presets use light gray (`#D3D3D3`) for both.

`styles.board_cutouts.scope` selects `all` (the general SVG default) or
`interior` (used by this board preview). Interior reuses Mate's existing
containment filter to exclude panelization contours that touch/cross the board
boundary or lie outside it. The same selection applies to copper clipping,
film apertures and cutout artwork. Original cutout curves are preserved.
`BOARD_CUTOUTS` uses the reference pcb-autodoc hatch and fitted-label behavior.
Outline, hatch and label have independent colors and opacity. This preview uses
the reference's muted assembly colors: `color: "#555555"` with
`outline_opacity: 0.25`, `hatch_color: "#777777"` with `hatch_opacity: 0.18`,
and `label_color: "#444444"` with `label_opacity: 0.25`.
Hatch lines are 0.12 mm wide, spaced 1 mm apart at 45 degrees; configure these
through `hatch_line_width_mm`, `hatch_spacing_mm` and `hatch_angle_deg`.

Set `label: "CUTOUT"` to label the openings; the general SVG default is an empty
label. Text fits inside the actual contour using `label_fill_ratio` (0.72) and
`label_max_font_size_mm` (3.0). Vertical text must fit at least 25% larger than
horizontal after the font cap (`label_rotation_min_gain: 0.25`). Labels smaller than 0.2 mm are omitted. Bottom
labels are counter-mirrored for readability. Set `hatch: false` and `label: ""`
to suppress those annotations. Existing cutout curves and interior filtering remain.

To compose both surfaces with the experimental native component illustrations
and update the fixed RT review page, run:

```powershell
uv run --no-sync python tests/support_scripts/pcb_board_review.py
```

Refresh `tests/assets/projects/rt_super_c1/output/pcb-svg/illustration-review/index.html`.
The script caches model tessellations and component illustrations, then places
repeated SVGs with `defs`/`use`. All bodies of a multipart component render
together. Orientation, material and viewing side remain part of the SVG cache;
separate components paint in visible-side height order.

To add other repository samples to that same page:

```powershell
uv run --no-sync python tests/support_scripts/pcb_board_review.py --projects bunny_brain goomba hydroscope
```

Each sample's SVGs and render report go under its own
`output/pcb-svg/illustration-review/` directory. The fixed review page gathers
the available sample pairs. `--theme` accepts `green`, `saved`, `black`, `white`, or `all`
(saved and green). With no theme override, RT_SUPER_C1 and Bunny use white;
Goomba and Hydroscope use black. Other designs default to saved and green. Black uses `#000000` film at 90% opacity with
white silkscreen; white uses off-white `#EEEEEE` film at 90% opacity with black silkscreen.
The other themes use the example config's colors and opacity.
The script uses the normal PCB project loader, including sibling `.PrjPcb`
discovery for a `.PcbDoc` input. Project parameters and the saved current
`VariantName` resolve text and barcode content on all layers, including the
openings in solder-mask film. Each project variant filters DNP component bodies and projected designators.
Alternate-model substitutions remain unsupported and are reported explicitly.

For an external board with its own review page:

```powershell
uv run --no-sync python tests/support_scripts/pcb_board_review.py --pcbdoc "D:/boards/example.PcbDoc" --output output/pcb-svg/example-review --theme black
```

To select the project explicitly, use `--prjpcb "D:/boards/example.PrjPcb"`.
Add `--pcbdoc "example.PcbDoc"` when the project contains multiple boards.

Open `output/pcb-svg/example-review/index.html`. This leaves the sample gallery
separate and reads the external design without copying it into test assets.

`illustration-preview.config.json` is a simple top/bottom illustration preset.
`assembly-illustration-preview.config.json` adds autodoc-fitted red designators
and suppresses saved silk designators. It draws no additional HLR layer.

```powershell
uv run altium-cruncher pcb-svg board.PrjPcb --config examples/pcb-svg/assembly-illustration-preview.config.json -o output/preview
```

`ILLUSTRATION_TOP/BOTTOM` and `ASSEMBLY_DESIGNATORS_TOP/BOTTOM` work through the
normal layer/view system. `styles.illustration` controls line width and opacity;
`styles.assembly_designators` controls color, opacity, fill ratio and maximum font
size. The fit defaults match autodoc (0.8 fill, 2.5 mm cap). A model-less part uses
its electrical-pad envelope for the label and adds no fabricated illustration.
Unplated locating holes supply the envelope only when no eligible electrical pads
exist; plated through-hole pads remain included. Flagged Altium testpoint pads
use the same eligibility exception as the copper renderer.

The presets include metadata. Component groups carry component indices, UIDs,
designators, side and geometry source. The enrichment JSON includes
`virtual_component_layers` with symbol/body details and designator fits, plus the
actual viewBox and scene reflection. See the component-layer schema under
`docs/contracts`. A renderer caches its native geometry, symbols, fitted labels
and completed component layers across views; reloading a PCB starts a new job.
The internal review page now shows only complete boards: plain and illustrated
assembly pairs. Cutout fixtures, component closeups and intermediate surface
comparisons are omitted from the page. RT_SUPER_C1 and Bunny use the white
theme (`#EEEEEE` mask, black silk); Goomba and Hydroscope use black mask.
Board preview perimeters are 0.25 mm black lines.
