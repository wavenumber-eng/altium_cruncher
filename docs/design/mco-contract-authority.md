# MCO contract authoring and consumption

Each of the 35 built-in operations has its own TypeSpec file under
`src/tsp/altium_cruncher/mco/operations`. For example,
`pcbdoc-add_text.tsp` declares `PcbdocAddTextArgs` and
`PcbdocAddTextOperation`. `common.tsp` owns shared fields, coordinates, mutation
paths and nested styles. `main.tsp` composes operations into the ordered container.
`defaults.tsp` owns the starter document and JSONC help.

The same declarations generate JSON Schemas, Python TypedDicts, TypeScript types,
browser validation and the metadata used by `mco list`. Required/optional catalog
fields come directly from the argument models. Static argument defaults declared
in TypeSpec feed the corresponding Python fallbacks; contextual names, native
enum defaults and native stack construction remain execution behavior.

## Adding an operation

1. Add its argument model and tagged operation model in `operations/`. Reuse
   shared shapes where their semantics match. Put canonical name, group and
   summary in the operation's `x-acr-operation` annotation. Optional args may
   still contain required nested fields. Keep absence and explicit null distinct.
2. Import it and add it to `BuiltinOperation` in `main.tsp`. The `op` literals
   declare supported names/aliases; internal CAD handler dictionary spellings
   are not automatically public aliases.
3. Implement/register its Python handler in the MCO handler map. Contract and
   handler names must match. Read declared static defaults using the canonical
   handler name, even when a caller registers that handler under another name.
4. Run generation and focused consumer/execution checks:

```powershell
npm run generate:contracts
npm run check:contracts
npm run check:typescript
npm run check:browser
uv run --extra test pytest -q tests/test_mco_contract.py tests/test_mco.py
```

The pinned Node toolchain is development-only. Installed Python users need no
TypeSpec compiler. The source distribution includes TypeSpec/tooling, and the
wheel includes generated Python models, schemas and metadata.

## Containers and consumers

The public [authored schema](../contracts/mco_input.a0.schema.json) accepts either
an object with `operations` or a raw operation array. Empty arrays are valid.
The optional schema is `altium_cruncher.mco.a0`; omission/null remain supported.
Operations have `op`, optional `id`, `message`, `on_fail`, and operation-specific
`args`. Omitted args mean an empty object at execution; `args:null` is invalid.

```python
from altium_cruncher.contracts.mco import decode_mco, encode_mco

authored = decode_mco({
    "schema": "altium_cruncher.mco.a0",
    "operations": [{"op": "mco.message", "args": {"text": "Hello"}}],
})
text = encode_mco(authored)
```

The generated Python module `altium_cruncher.contracts.generated.mco_input`
exports each argument/operation type plus `BuiltinOperation`, `McoDocument` and
`McoInput`. TypeScript consumers use `decodeMco`, `encodeMco`, `BuiltinOperation`
and `McoDocument` from `src/ts/altium_cruncher_config/index.ts`:

```typescript
const operations: BuiltinOperation[] = [{
  op: "pcbdoc.add_text",
  args: {
    file: "board.PcbDoc", output_file: "labelled.PcbDoc",
    text: "REV A", position_mils: [100, 100], height_mils: 40,
  },
}];
const document: McoDocument = {operations};
const validated = decodeMco(document);
```

Use the built-in-only union when statically narrowing arguments by `op`. A custom
operation branch necessarily has a string name in language types; the runtime
codec additionally excludes reserved built-in names from that branch. Custom
operation arguments remain open and are validated by their registered handlers.

Both codecs validate all supplied built-in arguments without inserting defaults
or modifying authored fields. They retain extension data and reject nonfinite or
non-JSON values. They do not preserve arbitrary JSONC source formatting/comments
and do not perform CAD semantic or filesystem validation.

## Execution compatibility

Execution deliberately starts with the
[envelope schema](../contracts/mco_envelope.a0.schema.json). It preserves existing
fallback IDs (`op1`, `op2`, ...), checks duplicates after assigning those IDs, and
leaves `on_fail` target/loop checks at execution time. Reached live built-ins
validate args inside the failure-result boundary, so errors can still recover
through `on_fail`; skipped rows are not preflighted. Native stack-input conflict
diagnostics retain their existing precedence.

Custom handlers and replacements retain their own contracts. Existing dry runs
retain their partial handler checks; use `decode_mco`/`decodeMco` for full structural
preflight. Programmatic execution still permits tuple/named-tuple coordinates and
opaque custom values, while authored JSON codecs require JSON arrays/values.
Integral JSON numbers in native enum/id positions are normalized on the execution
copy; input objects stay unchanged.

MCO booleans are strict, unlike creation-config truthiness. Native enum names and
IDs remain subject to installed Altium Monkey semantics. Existing exceptions for
numeric board/sheet fields and mechanical-kind booleans are retained. Nullable
model outlines and presence-sensitive `z_mils` precedence are preserved.

The catalog now includes previously omitted text/barcode, mutation output-path,
component source-link and style fields. PCB text `height_mils` is required;
arrangement `designators` and STEP-export `layer` are optional. The unused
`inverted_box` field is no longer advertised, though unknown extension fields
continue to survive transport. The `message` and `fail` execution aliases are now
listed explicitly. Canonical operation names and starter JSONC are unchanged.

`pcbdoc.export_layer_step` owns its MCO wrapper fields and highlights. Additional
fixture options are validated by the TypeSpec-owned STEP config codec before
`PcbLayerStepConfig` resolves domain options. MCO transport fields are removed
before delegated config validation. Result objects also have TypeSpec authority;
see the complete public contract inventory.

The generated [field reference](mco-config-fields.md), per-root metadata and
`tests/fixtures/mco-contract-vectors.json` support future editor work. Browser
conformance builds a browser-target bundle without external imports and executes
it in Node; it is not a UI automation test. See
[ADR-0009](../adrs/ADR-0009-mco-operation-contracts.md) for the boundary decision.
