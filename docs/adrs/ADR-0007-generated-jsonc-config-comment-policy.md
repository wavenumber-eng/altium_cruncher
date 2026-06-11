# ADR-0007: Generated JSONC Config Comment Policy

Status: accepted
Date: 2026-06-11

## Context

`altium-cruncher` commands generate editable configuration files that are used
directly by developers, downstream tools, and agents. Plain JSON templates are
valid, but they make option discovery depend on external documentation and are
easy to mis-edit when a nested section mirrors another command's config
contract.

The project already accepts JSONC for hand-edited configs. Generated config
templates should take advantage of that by carrying the same intent and allowed
value guidance that lives in the design documents and schemas.

## Decision

Human-editable generated config templates use JSONC and include comments for
every public config member.

The policy applies to:

- command-level default config templates;
- generated seed configs intended to be edited before execution;
- nested config sections embedded inside another generated config.

Comments should explain purpose, units, allowed values, and ownership boundary
where that is not obvious from the key name. If a nested section is generated
from another command's default config contract, it must either render the
field-level comments for that section or explicitly reuse the same documented
comment source.

String or enum-like fields must list the accepted values in the generated
comment. Free-form strings should say they are free-form and describe the
expected syntax instead.

Config dataclasses or parser models must expose field help through a local help
registry, dataclass metadata, or an equivalent source that feeds the shared
JSONC renderer in `altium_cruncher.config_json`. Command-specific string
assembly for editable config templates is not allowed except for introductory
header prose and examples.

Machine-readable contracts remain strict JSON Schema files under
`docs/contracts/`. Derived runtime artifacts such as MCO files may remain plain
JSON unless they are intended to be hand-authored or hand-edited.

## Consequences

Generated config tests should parse the JSONC output and should assert comments
exist around important public sections and enum fields when drift would be easy.

When adding a new config option, update the dataclass/parser behavior, schema,
design doc, and generated JSONC comments together.
