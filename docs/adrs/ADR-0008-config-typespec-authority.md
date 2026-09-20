# ADR-0008: TypeSpec authority for PCB SVG and Toon configuration

Status: accepted for the PCB SVG/Toon migration authorized on 2026-09-11.

PCB SVG and Toon share the versioned `pcb.svg.config` wire family. Its authored structure,
static SVG/Toon defaults, preset/theme values and JSONC field help now live in
`src/tsp/altium_cruncher/config`. The TypeSpec schema projection generates the
canonical schema, Python TypedDicts/resources, TypeScript declarations, standalone
browser validator and field reference. Generated artifacts are checked in for
normal Python installation and editor consumption and must not be edited by hand.

The standard schema projection contains all structural information needed for
this config family. A second custom catalog emitter is unnecessary here. The
generation adapter interprets the small `x-acr-*` annotation vocabulary and fails
on unsupported Python type shapes/inheritance. It has no sibling-repository or
private-package dependency. TypeSpec compiler/emitter are pinned together at
1.16.0; a clean install of the reference's 1.14.0 pair failed to load the emitter.

Authored configuration is a partial override. The transport codecs preserve
absence, explicit nulls, false/zero/empty values and intentional extension fields.
They never insert defaults or use the resolved configuration's `to_dict` for an
editor round trip. JSONC syntax remains the existing parser/formatter's concern;
the object codecs do not preserve arbitrary source comments or whitespace.

Mutable Python configuration dataclasses remain the resolved application API.
Their preset merging, normalization, derived names/paths, layer lookup and
rendering methods are behavioral code. Their static defaults and field help
consume generated resources. Python callers using dataclass construction,
replacement and mutation retain that API; generated transport types describe
the authored wire object instead. Structural decoding runs at the CLI file
boundary, not for each layer or primitive.

## Compatibility decisions

- The initial migration kept the `a0` ID because the old schema's required root
  fields did not describe documented partial Toon inputs; these fields became optional.
- Additive public fields advance the `a` revision. The issue-67 regional-surface,
  bend-line and silkscreen policy additions therefore make
  `pcb.svg.config.a1` the current authoring target. `pcb.svg.config.a0` remains
  accepted as an additive predecessor and its durable schema path remains published.
  A breaking or replacement shape starts at `b0`; it must not silently reuse an
  `a` discriminator.
- Keep allowed null resets/inheritance and existing boolean/numeric spellings,
  case/whitespace handling and projection/layer aliases at their relevant fields.
  Native/board-specific layer interpretation remains semantic validation.
- Known style objects and custom style groups remain extensible. Root extension
  fields and layer-output extensions are retained by transport codecs; the
  existing renderer may ignore fields it does not consume.
- Reject nonfinite/non-JSON transport values instead of silently changing them
  during serialization. File validation can report malformed settings earlier
  than render preparation. This does not make the mutable dataclass constructor
  a strict transport decoder.
- PNG export was removed before release at the user's request. SVG is the only
  Toon output. The shared config rejects the former `global.png` block; raster
  conversion belongs to consumers.

The discriminator versions the authored wire object, not renderer internals or
defaults alone. A preset/default behavior change is still documented and tested,
but does not by itself create a new wire revision. Loading an `a0` file does not
rewrite it during rendering; newly generated and explicitly resolved configs use
`a1`.

## Validator portability

Canonical typed values use Draft 2020-12 constraints. Legacy numeric strings need
the `x-acr-input` extension to enforce the numeric range and finiteness of their
interpreted value. Ordinary JSON Schema engines ignore this keyword: for example,
they can accept `margin_mm:"-1"` lexically while the full codecs reject it. The
supported Python codec and bundled browser validator implement that extension.
Consumers needing exact CLI structural validation should use those codecs, not
assume a stock schema engine supplies legacy coercion semantics. Semantic preset,
board/layer and enabled-view checks still run in Python after structural decoding.

## Scope and release

PCB SVG/Toon and the shared SchDoc/PcbDoc/project creation family are migrated.
The [creation guide](../design/creation-config-authority.md) records its native-ID,
truthiness and corrected required-field boundaries. On 2026-09-12 the user
extended this decision to all Cruncher-owned JSON/JSONC contracts: remaining
workflow configs, output schemas and the local interface inventory now follow
the same authority. See the [complete inventory](../design/public-contract-authority.md)
for the 45 roots and explicit upstream boundaries. The existing standalone
public repository owns both sources and generated artifacts; no private export
stage or separately published npm package is introduced. Node is required for
development/regeneration, not for installed CLI use. CI and release workflows
verify generation, typed consumption and shared Python/browser examples.
