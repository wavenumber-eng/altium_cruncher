# PCB SVG / Toon config authoring and consumption

Edit `src/tsp/altium_cruncher/config/pcb-svg.tsp` for wire fields and constraints,
and `defaults.tsp` for static SVG defaults, default views, Toon preset/theme values
and JSONC field help. Toon theme/preset selection and contextual overrides remain in the Python
illustration resolver. The policy is recorded in
[ADR-0008](../adrs/ADR-0008-config-typespec-authority.md).

From the repository root, using Node 24 and the pinned npm toolchain:

```powershell
npm ci --ignore-scripts
npm run generate:contracts
npm run check:contracts
npm run check:typescript
npm run check:browser
uv run --extra test pytest -q tests/test_pcb_svg_config_contract.py tests/test_toon_cli.py
```

Generation compiles TypeSpec in a temporary directory, then emits the schema,
Python/TypeScript types, resources, browser validator and
[field reference](pcb-svg-config-fields.md). `check:contracts` compares generated
content without rewriting it. Python runtime resources are included in the wheel;
the source distribution also carries the TypeSpec, TypeScript and generator.
CLI users need neither npm nor TypeSpec installed.

Python applications can use the presence-preserving transport boundary:

```python
from altium_cruncher.contracts.pcb_svg import (
    decode_pcb_svg_config,
    encode_pcb_svg_config,
)

authored = decode_pcb_svg_config({
    "global": {"styles": {"soldermask_film": {"opacity": 0.5}}},
})
text = encode_pcb_svg_config(authored)
```

For the planned web editor, import `decodePcbSvgConfig`, `encodePcbSvgConfig`
and `PcbSvgConfigInput` from `src/ts/altium_cruncher_config/index.ts` in a
TypeScript bundler. The accompanying generated schema supplies descriptions,
default annotations and field constraints. Generated metadata supplies SVG
defaults, the Toon preset/theme values and field help. The validator bundles its helpers and requires no
Node/native runtime or network schema lookup in the browser. The bounded browser
check builds that entry for a browser target, checks it has no external imports,
then exercises the shared vectors in Node; it is not a UI/browser automation test.

An editor should display inherited defaults without writing them into the user's
override. Saving the decoded object preserves its authored fields, including
extensions; resolved `PcbSvgConfig.to_dict()` is a different operation that expands
defaults and derived paths. Arrays replace prior arrays; objects merge recursively
in the Toon preset stage. View style inheritance retains its separate shallow
per-style merge. A color picker must allow values such as `auto`, and optional
fields need an unset/inherit state. Editor layout and board-dependent choices
remain consumer responsibilities.

Use the supplied codecs for legacy numeric spellings: stock Draft 2020-12
validation does not enforce the `x-acr-input` numeric-string range extension.
The codecs do not resolve boards or promise that every structurally valid config
is renderable. Toon still checks its enabled views and illustration-side rules.
The same positive/negative vectors live in
`tests/fixtures/pcb-svg-config-vectors.json`; Python and TypeScript consumers
also check optional fields and typed, extensible record values.
