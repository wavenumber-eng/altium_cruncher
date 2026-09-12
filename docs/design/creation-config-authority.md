# Document creation config authoring and consumption

TypeSpec owns the SchDoc create, PcbDoc create and project skeleton config
contracts. Edit `src/tsp/altium_cruncher/config/creation.tsp` for fields and
constraints and `creation-defaults.tsp` for shared static config defaults and
JSONC help. Standalone roots and project children share the same document models.
Existing a0 schema IDs, paths and config file names remain unchanged.

Run the same toolchain as PCB SVG/Toon:

```powershell
npm ci --ignore-scripts
npm run generate:contracts
npm run check:contracts
npm run check:typescript
npm run check:browser
uv run --extra test pytest -q tests/test_creation_config_contract.py
```

`main.tsp` includes all migrated families, including the later MCO slice.
Generation checks all owned artifacts without rewriting files. Each root has a
public schema, packaged Python schema/metadata/DTO, TypeScript types/schema/
metadata/browser validator and field guide:
[SchDoc](schdoc-create-config-fields.md),
[PcbDoc](pcbdoc-create-config-fields.md),
[project skeleton](project-skeleton-config-fields.md).

The installed Python CLI needs no Node toolchain. Each of the three JSONC file
loaders now uses the generated structural contract before existing MCO compilation.
Applications can use the same presence-preserving codecs:

```python
from altium_cruncher.contracts.creation import (
    decode_project_skeleton_config,
    encode_project_skeleton_config,
)

config = decode_project_skeleton_config({
    "schema": "altium_cruncher.project_skeleton.a0",
    "project": {"file": "demo.PrjPcb"},
    "schematics": [],
    "pcb": None,
})
text = encode_project_skeleton_config(config)
```

The equivalent TypeScript exports are `decodeProjectSkeletonConfig`,
`encodeProjectSkeletonConfig` and `ProjectSkeletonConfigInput` from
`src/ts/altium_cruncher_config/index.ts`. SchDoc and PcbDoc use the corresponding
`SchdocCreate` and `PcbdocCreate` names. Nested types are available from each
generated module. Browser validators are bundled without external imports;
conformance builds a browser-target bundle and executes it in Node, without a UI.

## Structure and behavior

Codecs check required fields and supplied values without inserting defaults or
coercing them. Omitted optional fields, allowed nulls, empty arrays and extension
data survive editing and saving. Required root fields stay required; a project
must supply `schematics`, but `[]` creates no sheets, and absent/null `pcb` creates
no board. Project parameter values retain their authored JSON shape; the existing
Python adapter converts them to strings when building MCO operations.

Default annotations describe template values or adapter fallbacks. For example,
the generated template includes a 3000 by 2000 mil outline, while an authored PCB
config that omits `board_outline_mils` does not request an outline. The codec must
not add that template outline. Contextual filenames, copper-layer count expansion,
dielectric distribution, named native mechanical-profile rows and enum references
remain in the Python document/profile code. This slice does not generate an MCO
contract or migrate the native profile catalog into TypeSpec.

Structural validation does not replace native checks for valid enum IDs, stack
geometry/counts, existing template files, or the mutually exclusive stack-input
rule. Public direct Python MCO builders retain their behavioral API; the generated
file codecs are the structural boundary.

## Compatibility decisions

- Existing null resets, empty project sheet lists and case/whitespace/hyphen
  mechanical-profile spellings are accepted. The old schemas missed some of these.
- Creation booleans preserve their existing Python truthiness semantics. In
  particular, a nonempty string such as `"false"` is true. Prefer JSON `true` or
  `false`; creation does not use SVG's yes/no parser.
- Rigid stacks require the dielectric array and each dielectric's name, material,
  thickness and dielectric constant because MCO already requires them. Invalid
  configs now fail at file loading instead of later during document creation.
  Omitted/null mode selects `generated_rigid`; empty mode is invalid.
- Copper `component_placement`/`copper_orientation` and dielectric `loss_tangent`
  are explicit fields. Historical copper `thickness_mils` and dielectric `dk`/
  `type_code` remain accepted extension data but are ignored by creation; use
  `copper_thickness_mils`, `dielectric_constant` and `dielectric_type` respectively.
- Flat mechanical pairs retain nullable `pair_index`. Presence of either `top`
  or `bottom` selects grouped form, requiring both complete sides. Separate
  `mechanical_layer_kinds` rows accept integer enum IDs as well as strings;
  inline layer/pair-side kind fields require strings as before.
- Integral JSON numbers such as `pair_index: 1.0` are accepted. Creation adapters
  normalize relevant enum/id fields to Python integers in the emitted MCO copy.
  Authored values remain unchanged. This resolves the JSON/JavaScript-versus-Python
  integer representation mismatch without relaxing the raw MCO API.
- Nonfinite and non-JSON transport values are rejected by both codecs.

Shared conformance cases are in `tests/fixtures/creation-config-vectors.json`.
Existing command tests cover MCO generation and generated-document readback.
