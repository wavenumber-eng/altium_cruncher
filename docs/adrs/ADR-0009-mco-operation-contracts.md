# ADR-0009: MCO operation and container contracts

Status: accepted for the user-authorized MCO migration, 2026-09-11.

MCO is an ordered execution program with extensible handlers. Its argument
contract cannot be promoted by applying one strict document decoder before
execution: doing so would reject skipped operations, intercept errors that should
follow `on_fail`, and constrain caller-supplied handlers.

Author each built-in operation and its arguments in its own TypeSpec file under
`src/tsp/altium_cruncher/mco/operations`. Compose them with shared fields and
argument models into `BuiltinOperation`, then the document/raw-array container.
The operation's `op` literal determines its argument type. Derive the existing
operation catalog from these definitions rather than a parallel Python list of
required and optional arguments. Python keeps an explicit handler map with an
exact source-contract coverage check.

Publish two structural roots. `McoInput` validates all authored built-in arguments
for editor/preflight use. `McoEnvelopeInput` validates only the ordered container,
operation names, IDs, messages, branch targets and args-object shape. Execution
uses the envelope, assigns fallback IDs and checks duplicates as before. Reached
live built-ins validate their arguments inside the existing failure-result
boundary. Skipped operations, custom/replacement handlers, and the existing
partial dry-run path retain their prior behavior.

The authored codecs require finite JSON and preserve authored fields. The
programmatic execution path continues to allow tuple coordinates and opaque custom
argument values. Native integer representations are normalized only in changed
built-in argument subtrees after validation; untouched tuples, named tuples and
custom extensions retain their values/identity. Static handler defaults are
looked up by the handler's canonical contract name, so registering a built-in
handler under a custom alias remains valid.

Keep extension fields open. Custom operation names exclude reserved built-in
names and the existing `message`/`fail` aliases in the JSON validator, preventing
invalid built-ins from escaping validation. TypeScript cannot express arbitrary
strings excluding a finite set of literals, so consumers use `BuiltinOperation`
for static discriminated narrowing and the codec for full document validation.

Preserve the `altium_cruncher.mco.a0` wire tag and result serialization. This slice
does not promote result DTOs or the entire fixture-export config: the STEP export
operation documents its delegation to `PcbLayerStepConfig`. Native CAD semantics,
contextual defaults, file lifecycle and control flow remain handwritten behavior.
