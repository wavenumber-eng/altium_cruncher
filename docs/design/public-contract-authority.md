# Public contract authority

TypeSpec under `src/tsp/altium_cruncher` owns every Cruncher public JSON/JSONC
configuration and output schema. This includes partial inputs, current and
supported legacy Mate inputs, generated manifests, embedded SVG metadata,
reports and the existing unversioned array outputs. Wire tags, paths and output
shapes are preserved. The Python CLI does not require Node.

The generated [catalog](../../src/ts/altium_cruncher_config/generated/catalog.json)
lists all 46 roots, their authored sources, current schemas, compatibility
schemas and validators. The PCB SVG root declares both its current A1 schema
and its frozen A0 predecessor without creating a second runtime codec. Generation
rejects duplicate names and any public `docs/contracts/*.schema.json` that lacks
a TypeSpec source. All published references are bundled locally; validation
does not fetch schemas from the network.

## Inventory

Producer and adapter names below refer to `src/py/altium_cruncher`. Config roots
live in `src/tsp/altium_cruncher/config`, operation inputs in `mco`, and other
roots in `outputs`. Each catalog entry links the exact source and JSON Schema.

| Roots (catalog stems) | Producer or consumer |
| --- | --- |
| `pcb_svg_config` | `altium_cruncher_pcb_svg_config`, SVG and Toon commands |
| `schdoc_create_config`, `pcbdoc_create_config`, `project_skeleton_config` | `altium_cruncher_document_configs`, `altium_cruncher_cmd_prjpcb` |
| `bom_pnp_config` | `bom_pnp_model`; BOM, PnP, JLC and MegaMaid |
| `clean_config` | `altium_clean`, `altium_pcblib_clean`; both schema tags |
| `pcb_layer_step_config` | `altium_cruncher_pcb_layer_step`; shared export settings also used by Mate |
| `mate_config`, `mate_parts_input` | `altium_cruncher_mate`, `altium_cruncher_mate_parts`; current and legacy authored inputs |
| `mco_input`, `mco_envelope` | `altium_cruncher_mco`, `altium_cruncher_mco_cad_ops`; authored arguments and deferred execution envelope |
| `design_review_manifest` | `altium_cruncher_design_review` |
| `megamaid_manifest` | `altium_cruncher_cmd_megamaid`; typed nested artifact sections |
| `schematic_svg_manifest`, `schematic_svg_enrichment` | `altium_cruncher_cmd_sch_svg`; Design b0 links and embedded metadata |
| `pcb_svg_manifest`, `pcb_svg_enrichment`, `pcb_svg_component_layers` | `altium_cruncher_cmd_pcb_svg`, `altium_cruncher_pcb_svg_a0_renderer`, `altium_cruncher_pcb_svg_component_layers` |
| `pcb_svg_timings` | `pcb_svg_render_job`; nullable absent cache statistics |
| `toon_warning_report` | `toon_diagnostics`, `altium_cruncher_cmd_toon`; deterministic nonfatal diagnostic report |
| `notes` | `altium_cruncher_cmd_notes` |
| `variants_list` | `altium_cruncher_prjpcb_variants` |
| `intlib_extract` | `altium_cruncher_cmd_extract._intlib_extract_manifest` |
| `outjob_run` | `altium_cruncher_cmd_outjob` |
| `json_dump`, `json_dump_manifest` | `altium_cruncher_json_dump`; document wrappers and batch manifest |
| `mate_inspection`, `mate_parts_manifest` | `altium_cruncher_mate`, `altium_cruncher_mate_parts` |
| `libraries_scan` | `altium_cruncher_mate_libraries` |
| `mco_execution`, `mco_operations`, `mco_builtin_result` | `altium_cruncher_mco`, `altium_cruncher_mco_cad_ops` |
| `bom_normalized`, `bom_grouped`, `bom_array`, `bom_legacy`, `pnp` | `bom_pnp_model`, `altium_cruncher_cmd_bom` |
| `pcb_layer_step` | `altium_cruncher_pcb_layer_step._build_manifest` |
| `easyeda_models`, `easyeda_footprint_report`, `easyeda_symbol_report` | `altium_cruncher_cmd_easyeda_import`, `easyeda_altium_footprint`, `easyeda_altium_symbol` |
| `installs`, `launch`, `profiles`, `profiles_clean` | `altium_environment`, corresponding command modules |
| `interface_design_manifest` | Documentation interface inventory, consumed by `test_L99_004_interface_design_docs.py` |

## Ownership boundaries

- `command_manifest.a0.json` is an instance of a **wn-dev-std-owned** inventory
  format. Cruncher maintains its contents; it does not fork that schema into
  TypeSpec. The locally tagged interface inventory has its own TypeSpec root.
  CLI parsing remains
  argparse, with command/design-manifest parity checked by Rack.
- Direct Monkey Design b0, compiled graph, gotIR, SchDoc and SchLib payloads
  retain **Monkey's authority**. Cruncher owns wrapper fields and references.
  Its JSON-dump PCB summaries retain their historical `altium_monkey.*` wire
  tags, but their collection names and wrapper structure are modeled here.
  Reflection-derived native record contents are explicitly unknown; they must
  be consumed against the installed Monkey API, not a guessed Cruncher DTO.
- PCB SVG enrichment models Cruncher's canvas and virtual-component extension
  fields. The surrounding native SVG metadata remains Monkey-owned.
- Generic MCO execution accepts custom output dictionaries, including handlers
  that replace built-in names. `mco_builtin_result` provides separate, typed
  default-registry validation, covering success, dry-run and failure shapes.
  Consumers must choose it only when using the default handlers.
- Parameter dictionaries, custom MCO arguments/outputs and authored extension
  records are intentionally open. Known fields remain typed. Native binary CAD,
  STEP, SVG markup, CSV/XLSX cell formats and human-readable CLI logs are not
  JSON DTOs; their behavior remains in the corresponding command guide.
- Disposable model-cache records and internal artifact hashes are implementation
  details, not public contracts.

## Defaults and input semantics

Codecs validate and copy JSON. They never insert defaults, remove unknown
extension data, normalize aliases or resolve paths. Presence and null are
preserved. Python adapters perform command-specific normalization and native
operations after structural validation.

TypeSpec metadata owns templates, field help and static adapter defaults.
`domain-model-defaults` describes dataclass fallbacks independently of first-run
templates. This matters for Clean's template fonts and Mate's label placement:
creating a template can deliberately select options that an omitted field does
not enable. Geometry, variant selection, path resolution and native enum
interpretation remain adapter behavior.

## Consumer API

```python
from altium_cruncher.contracts.generated.public import decode_contract

config = decode_contract("pcb_svg_config", {"views": []})
result = decode_contract("mco_builtin_result", payload)
```

```typescript
import { decodeContract, encodeContract } from "./src/ts/altium_cruncher_config/index.js";

const config = decodeContract("pcb_svg_config", { views: [] });
const json = encodeContract("pcb_svg_config", config);
```

Python has typed overloads and TypedDicts, including inline nested objects.
TypeScript has root types, a `ContractTypes` map and browser-safe standalone
validators. Existing family-specific codec entry points remain available.
The wheel includes Python types/schemas/metadata; the sdist includes TypeSpec,
TypeScript, generation tooling, documentation and shared vectors.
The [artifact catalog](../governance/artifacts.toml) records ownership,
regeneration and distribution policy for committed generated files.

## Updating and checking

Run `npm run generate:contracts` after editing TypeSpec. Never edit generated
schemas, DTOs, validators or field guides. Register new roots in TypeSpec with
`@jsonSchema` and `x-acr-contract` metadata, then update this inventory and add
producer qualification where the shape is not already exercised.

`npm run check:contracts`, `npm run check:typescript` and
`npm run check:browser` check generation, typed consumption and shared browser
vectors. Python runs the same vectors plus actual serializer tests. MCO's
existing workflow tests validate default-registry results. Rack verifies schema
metaschemas, config templates and command/interface inventories; release checks
also build and install the wheel.
