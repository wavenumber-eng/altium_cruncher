# Altium Cruncher Public Repo Migration Plan

Status: bootstrap in progress
Last updated: 2026-05-26

## Goal

Move `altium_cruncher` out of the private `toolz` monorepo into the public
repository at <https://github.com/wavenumber-eng/altium_cruncher>.

The standalone repo should be the public source of truth. Unlike
`altium-monkey`, it should not use a generated public-release/export flow.

The package is an application/CLI for users who want Altium utilities without
writing Python. It should consume the public `altium-monkey` package as a real
downstream dependency, ideally tracking the latest released date version.

## Product Direction

`altium_cruncher` should prioritize command parity first:

1. inventory current commands from `toolz/altium_cruncher`;
2. migrate or reimplement stable commands in the standalone repo;
3. add installable console entry points;
4. add tests and CI for each migrated command;
5. remove the private `toolz` package only after the public repo is viable.

Compact JSON output is a central product direction because exposing Altium
design data in machine-consumable form is one of the main reasons this tool
exists. However, the first migration milestone should not block on designing a
complete design-query JSON contract. Initial command migration should preserve
clean output boundaries, stable exit codes, and structured error behavior so
the richer JSON contract can be promoted later.

## Repository Contract

The standalone public repo should include:

- `pyproject.toml`;
- `src/altium_cruncher/`;
- `tests/`;
- `rack.toml` and Rack strata manifests;
- `README.md`;
- `LICENSE`;
- `CONTRIBUTING.md`;
- issue templates;
- pull-request template;
- GitHub Actions CI for Windows, macOS, and Linux.
- `docs/adrs/` for architecture decision records;
- `docs/design/` for interface, command, data-flow, and format design
  documentation;
- `contracts/` for machine-readable schemas and contract examples where a
  command exposes stable JSON or config formats.

One of the first ADRs must define versioning, tagging, release, and
traceability policy. It should align with the current Geometer-style package
discipline:

- date-versioned Python package releases;
- explicit PyPI publish flow;
- annotated Git tags for released source commits;
- release notes or changelog expectations;
- compatibility policy for public commands, JSON outputs, and config formats;
- rules for when direct PRs can be released.

The preferred release workflow should be GitHub-driven rather than a local-only
Twine ritual:

- PR and push CI run Rack tests, `L99_signoff`, package build, clean-install
  tests, and `twine check`;
- `main` is protected and requires passing CI before merge;
- release publishing uses GitHub Actions with PyPI Trusted Publishing / OIDC
  where possible, not long-lived local PyPI tokens;
- releases are triggered from a protected tag or GitHub Release, using tags such
  as `vYYYY.M.D`;
- release jobs verify package version metadata matches the tag;
- release jobs verify release notes/changelog mention the version;
- release jobs build wheel/sdist from the tagged source and publish to PyPI;
- local Twine upload remains an emergency/manual fallback, not the normal path.

The likely package and entry-point names are:

- distribution: `altium-cruncher`;
- import package: `altium_cruncher`;
- console script: `altium-cruncher`.

The package should be easy to install with `uv tool install`, producing normal
executable entry points on Windows, macOS, and Linux. Nuitka or PyInstaller
packaging can be evaluated later, but the first packaging target should be a
normal Python package with console scripts.

`altium-cruncher` remains AGPL-3.0-or-later because it imports and depends on
AGPL `altium-monkey` for normal operation. A permissive license is appropriate
for independent parser/helper packages such as `easyeda-monkey`, but not for
this combined application package.

## Workspace Installer Integration

The standalone package must also work through the WN workspace setup/update
flow, not only through direct developer commands.

`wn-hw` integration is a first-release blocker:

- add a standalone `altium_cruncher` repo/dependency entry to the workspace
  manifest when the public repo is ready to consume;
- install the released package with pinned `uv tool install --force`
  invocations;
- allow editable `uv tool install --force --editable <checkout>` overrides for
  local development;
- ensure the resulting script/executable directory is on PATH after
  `setup.ps1`/`setup.sh` and after `update.ps1`/`update.sh`;
- standardize workspace workflows on the single public console name
  `altium-cruncher`; the import/module name remains `altium_cruncher`;
- add an installer test that starts from the workspace shell and runs
  `altium-cruncher --version`;
- remove old `uv run --project ... toolz/altium_cruncher` assumptions from
  WN docs/scripts only after the standalone executable path is verified.

## Dependency Policy

`altium_cruncher` is an application package, so it can carry richer dependencies
than core `altium-monkey`, but these tools still minimize dependencies.
New runtime, optional, and test-only dependencies need explicit justification in
the commit, PR, or linked plan.

Expected direct dependencies include:

- public `altium-monkey`;
- `wn-geometer` where command features need geometry support;
- other application-level libraries as needed.

The package must not import private `toolz` modules. `wn-hw` should eventually
clone/use this standalone repo as an external dependency, similar to
`geometer`.

New public commands should keep the top-level CLI as an orchestrator. Command
specific parser setup, command behavior, output formatting, and command-specific
imports belong in command modules, including simple commands.

## Test Strategy

The standalone repo should use `wn-rack` for tests and signoff.

Tests must run from the repo's own `tests/` folder. Fixtures must be
redistributable; initial candidates should come from the existing
`altium-monkey` public-release examples/assets where practical.

Initial Rack shape:

- `L0_foundation`: package import, version, CLI help, console entry point;
- `L1_command_manifest`: every registered command has docs, help, and test
  ownership;
- `L2_assets`: redistributable fixture discovery and asset-integrity checks;
- `L3_commands`: fixture-backed command tests;
- `L4_outputs`: structured/golden output checks for selected stable commands;
- `L9_cross_platform`: path handling, Unicode filenames, output folders, and
  OS-specific install/runtime behavior;
- `L99_signoff`: type coverage, complexity checks, command coverage, docs
  links, PEP 257-style docstring coverage, design/contract documentation
  coverage, contract conformance tests, no private paths, no `toolz` imports,
  package build/install tests.

The signoff model should copy the useful shape from the in-progress
`data_models` worktree:

- ADRs record architecture choices and compatibility policy;
- `docs/design/` records durable interface and data-flow design;
- `contracts/` stores stable schema/config artifacts;
- contract conformance helpers live in tests and are reused by command tests;
- L99 checks prevent new public surfaces from landing without matching docs,
  contracts, and tests.
- public dataclasses and major interfaces require design documentation with
  rationale, purpose, test requirements, working definition, and Rack test
  ownership.

All package functions and methods should have PEP 257-style docstrings. Public
interfaces, command output formats, JSON config files, and any stable compact
JSON payloads must have corresponding design docs and conformance tests before
they are treated as release-ready.

Before migrating commands, perform an evidence pass:

- inventory existing `toolz/altium_cruncher` commands;
- inventory private `toolz-tests` coverage for those commands;
- identify reusable public fixtures from `altium_monkey_public`;
- identify private-corpus-only tests that need replacement fixtures;
- map each command to existing coverage, missing coverage, public fixture
  availability, and dependency blockers.

## Command Coverage Guardrails

The repo should have a command manifest used by tests and CI.

Every public command should have:

- manifest entry;
- CLI help test;
- docs or README coverage;
- at least one behavioral test, or an explicit waiver with rationale.

`L99_signoff` should fail when a new public command is added without the
required manifest/test/doc coverage.

## Shared CLI Help Requirements

The command-line interface should be readable for users who are discovering the
tool from the executable alone.

Top-level help behavior:

- bare `altium-cruncher` and `altium-cruncher --help` should report the package
  version before the help text;
- the version line, usage block, and command list should have enough blank
  space to scan easily in a terminal;
- command names should be listed alphabetically;
- the help text should clearly state how to get command-specific help, for
  example `altium-cruncher <command> --help`.

Command-specific help behavior:

- every `altium-cruncher <command> --help` output should report the package
  version;
- command help should keep options grouped and spaced so required arguments,
  output controls, config controls, and command-specific behavior are easy to
  distinguish;
- command design docs should mirror the help shape: usage, arguments/options,
  output, config/contracts, and tests.

Required tests:

- top-level CLI test verifies version is present in bare and `--help` output;
- command manifest/help test verifies command ordering is alphabetical;
- per-command help tests verify version text and guidance are present for every
  manifest command;
- installed-console test verifies the same behavior from the generated
  `altium-cruncher` executable, not only `python -m altium_cruncher`.

## Shared Output Naming Requirements

Commands that create files should share one output-naming resolver instead of
hard-coding filename patterns in each command. This should cover both filename
templates and output-folder path templates.

Required behavior:

- apply to output-producing commands including `svg`, `sch-svg`, `pcb-svg`,
  `netlist`, `bom`, `pnp`, and the planned `jlc` meta command;
- support config-controlled filename and output-folder templates with stable
  placeholders such as command name, project stem, source stem, variant, layer,
  view name, output kind, and extension;
- support an expression form that can concatenate fixed string fragments and
  `PrjPcb` project parameters into one resolved relative folder path or file
  name;
- allow placeholders or expression terms to read `PrjPcb` project parameters
  so company/project metadata can control generated paths;
- reserve `VariantName` as the runtime token for the currently processed
  variant, including base/vanilla variant handling;
- use Altium OutJob release path expressions as reference material. For
  example, the inspected `job.OutJob` composes paths from literals plus
  project parameters such as `Revision`, `RevisionMinor`, `PartNumberPCB`,
  `PartNumberPCBA`, and `Title`;
- define behavior for missing project parameters, with either explicit fallback
  text or a clear validation error based on config;
- default generated template results to relative paths rooted under the
  command output root; absolute paths should require explicit command/config
  opt-in if they are ever supported;
- sanitize generated filenames consistently across Windows, macOS, and Linux;
- include the resolved output names in machine-readable manifests when a
  command emits a manifest;
- implement this as common code with focused unit tests rather than duplicating
  string replacement logic in each command;
- document this once in a shared design document and reference it from each
  command design doc that supports configurable naming;
- include contract tests for literal-only templates, parameter substitution,
  mixed literal/parameter expressions, `VariantName`, missing parameters,
  invalid path characters, path traversal rejection, and cross-platform path
  separator normalization.

## SVG Command Family

The first public command set keeps all three SVG commands:

- `sch-svg`: schematic and schematic-library SVG output;
- `pcb-svg`: PCB SVG output, including layer views and assembly views;
- `svg`: convenience command that runs `sch-svg`, `pcb-svg`, or both based on
  input type. Its help text should state this plainly and avoid implying it is
  a separate renderer.

Required SVG follow-up:

- review `svg` help so it clearly says it runs both schematic and PCB SVG
  commands where applicable;
- add/confirm fixture-backed coverage that `svg <project.PrjPcb>` creates both
  schematic SVG output and PCB SVG output;
- review `pcb-svg` assembly-view rendering with HLR/geometer enabled;
- choose a redistributable public test project with embedded 3D models and
  verify assembly SVG output is created and non-empty;
- keep at least one test that exercises normal PCB layer SVG output so HLR work
  cannot regress existing layer rendering.

## PCB Layer STEP Command

`pcb-layer-step` stays in the first public command set.

Fixture corpus requirements:

- all `altium-cruncher` command fixtures should use the same structure:
  - `input/` for source designs and configs;
  - `reference_output/` for checked-in expected artifacts where the command has
    stable output contracts;
  - `output/` for transient local/test output only;
- copied `altium-monkey` public-release projects need to be restructured into
  this convention and should gain reference-generation jobs before their
  outputs are treated as golden references;
- per-command tests may use the same fixture families differently, but the
  folder shape should stay consistent.

Required source fixtures:

- copy from private test corpus:
  - `C:\eli\wn_test_corpus\altium\common\real_world_pcbdoc\cricket-node`;
  - `C:\eli\wn_test_corpus\altium\common\real_world_pcbdoc\node_test_array`;
- copy/restructure from public `altium-monkey` examples:
  - `C:\eli\altium_monkey_public\examples\assets\projects\hydroscope`;
  - `C:\eli\altium_monkey_public\examples\assets\projects\loz-old-man`;
  - `C:\eli\altium_monkey_public\examples\assets\projects\rt_super_c1`;
  - `C:\eli\altium_monkey_public\examples\assets\projects\goomba`;
  - `C:\eli\altium_monkey_public\examples\assets\projects\bunny_brain`.

Initial `pcb-layer-step` coverage:

- use `cricket-node`;
- generate bottom-layer copper STEP;
- document and test color control:
  - copper color: `#3D85C6`;
  - board outline color: `#CCCCCC`;
- verify the command creates a non-empty STEP artifact and any stable report or
  manifest output expected for the command;
- later golden/reference checks should compare against `reference_output/` once
  the reference-generation job is in place.

## BOM Command

`bom` stays in the first public command set and is a key command, not a
placeholder. The current standalone command is a thin CSV/JSON/XLSX emitter;
the public release target is closer to the older `bom_cruncher` application
behavior, but self-contained inside `altium-cruncher` and without private
`toolz` or `data_models` imports.

Reference material:

- old BOM application code in
  `C:\eli\agent-worktrees\lib_cruncher_panel_monkey\appz\bom_cruncher`;
- old grouping/fallback logic in `bom_cruncher.processing.grouping`;
- old Altium component-kind filtering tests in
  `bom_cruncher/tests/L0_foundation/test_componentkind_filtering.py`;
- alias and policy data in
  `C:\eli\agent-worktrees\altium_monkey_cpp\wn-hw\config\library-policy.json`.

Required outputs:

- always emit raw JSON that preserves the parsed component data used for the
  BOM decision process;
- emit grouped JSON BOM output with stable schema/version metadata;
- emit JLC BOM output;
- emit XLSX BOM output grouped by designator/line item.

Required processing model:

- introduce helper code/data structures for normalized BOM rows and grouped
  BOM line items instead of leaving grouping embedded in the CLI command;
- support schematic-derived BOM data, PCB-derived BOM data, and merged
  schematic+PCB data as explicit source modes;
- support configurable output fields for every emitted format;
- support canonical parameter names plus aliases so projects with messy
  parameters such as `mpn`, `MPN`, and `Manufacturer Part Number` resolve to
  the same meaning;
- use or adapt the `wn-hw` library-policy alias concepts, but package the
  public command so it is self-contained and can run without a private
  workspace checkout;
- keep a traceable normalization path so the raw input parameter and canonical
  field selected for each line can be audited from JSON output.

Required config behavior:

- use a JSON config with an explicit schema/type field such as
  `wn.altium_cruncher.bom.config.v1`;
- auto-generate `bom.config` in the working folder when no config exists;
- accept `--config <path>` so a project can keep multiple BOM configs;
- look for the default config name when `--config` is omitted;
- define output enablement, output field sets, canonical fields, field aliases,
  grouping keys, source mode, inclusion/exclusion rules, DNP policy, variant
  policy, and PCB line-item behavior;
- include a machine-readable contract/schema under `contracts/` and a matching
  design document under `docs/design/cli/bom.html`.

Required PCB line item behavior:

- config can add the PCB itself as a BOM line item;
- config can provide PCB part number, description, and other fields directly;
- config can alternatively name a `PrjPcb` project parameter as the source for
  the PCB part number or other PCB fields.

Required DNP and inclusion behavior:

- config can include or exclude DNP components;
- config can place DNP lines at the end of the XLSX, in a separate DNP section,
  or immediately below the matching populated line item;
- when populated and DNP components share the same part identity, support the
  split-line representation, for example seven populated zero-ohm resistors on
  one line and three DNP zero-ohm resistors directly below;
- config can process no variant, one named variant, or all variants including
  the vanilla/base design;
- config controls inclusion rules for component type and parameters, including
  mechanical, graphical, no-BOM, and other Altium component-kind or flag-driven
  decisions.

Required BOM fixtures/tests:

- use `node_test_array` as a required fixture because it exercises
  hierarchical sheet instances and resolved designators;
- validate the generated BOM against Altium-generated CSV reference output
  where the reference is distributable;
- add focused tests for alias resolution, grouping fallback, output field
  selection, DNP placement policies, variant selection, component-kind
  filtering, PCB line-item insertion, and the invariant that raw JSON is always
  emitted;
- put fixtures in the standard `input/`, `reference_output/`, and transient
  `output/` shape.

## PnP Command

`pnp` stays in the first public command set. The current command emits CSV or
JSON from a `PrjPcb`; the release target should make it a first-class
pick-and-place/CPL exporter that shares as much normalized component data and
sorting logic with `bom` as practical.

Current behavior to preserve:

- input is a `.PrjPcb`, with current working-directory auto-detection when no
  file is supplied;
- output folder defaults under `output/pnp`;
- `--variant`, `--all-variants`, `--units mm|mils`, `--exclude-no-bom`,
  `--format csv|json`, and `--output` remain supported;
- output rows include designator, comment, layer, footprint, center X/Y,
  rotation, description, and component parameters.

Reference material:

- core extraction API: `AltiumDesign.to_pnp(...)`;
- current public CLI command:
  `src/py/altium_cruncher/altium_cruncher_cmd_pnp.py`;
- core PnP behavior tests:
  `toolz-tests/suites/altium_monkey/tests/L5_sch_tools/test_L5_007_bom.py`;
- existing CLI/native parity shape:
  `toolz-tests/suites/altium_monkey/tests/L6_pcb_foundation/test_L6_048_pcbdoc_cpp_cli_bom_pnp_parity.py`;
- design JSON PnP inclusion test:
  `toolz-tests/suites/altium_monkey/tests/L7_pcb_comprehensive_interop/test_L7_023_design_json_pnp.py`;
- older placement export, JLC CPL, and natural designator sorting logic in
  `C:\eli\agent-worktrees\altium_monkey_cpp\appz\bom_cruncher`.

Required processing model:

- introduce a shared BOM/PnP normalization layer so PCB-derived BOM JSON and
  PnP JSON are derived from the same component/placement records;
- keep the raw JSON output machine-consumable and schema-versioned;
- support CSV, JSON, and XLSX output for standard pick-and-place;
- support JLC CPL output, with JLC naming and columns aligned to the older
  `bom_cruncher.export.jlcpcb.export__jlc_cpl` behavior;
- support configurable units, at minimum `mm` and `mils`;
- support sorting modes:
  - natural designator order such as `R1`, `R2`, `R10`;
  - group by top then bottom;
  - group by bottom then top;
  - configurable designator-prefix order so users can choose category ordering
    such as capacitors before inductors;
- use the same variant, DNP, no-BOM, graphical/mechanical component, field
  alias, and source-mode policy concepts as the BOM command wherever the data
  overlaps.

Required JLC meta command:

- add a `jlc` meta command after the BOM/PnP shared data layer is stable;
- `jlc` generates both JLC BOM and JLC CPL from one project/config invocation;
- it should reuse the `bom` and `pnp` implementation paths rather than
  duplicating extraction, filtering, aliasing, or sorting logic;
- tests should prove the `jlc` output is equivalent to running the matching
  `bom` and `pnp` JLC modes independently.

Required fixtures/tests:

- use `node_test_array` as the required first fixture because it exercises a
  hierarchical design and resolved designators;
- compare CLI CSV and JSON output against `AltiumDesign.to_pnp(...)` using the
  same shape as the existing L6 parity test;
- include variant `B4` coverage for `node_test_array`;
- validate required fields, numeric positions, normalized `top`/`bottom`
  layers, unit conversion, and `--exclude-no-bom` behavior;
- validate top/bottom grouping and natural designator sorting;
- add tests for configurable designator-prefix ordering;
- add tests for XLSX output once the formatter is implemented;
- add tests for JLC CPL fields and the planned `jlc` meta command;
- consider old `bom_cruncher/tests/test_cases/altium/node-test-array/pnp_reference`
  as a candidate source of Altium-generated reference outputs after
  redistribution review.

## Netlist Command

`netlist` stays in the first public command set as-is for the first release.
It is a key machine-consumable output command.

Required follow-up:

- preserve the current behavior that emits full Altium design JSON from
  `AltiumDesign.to_json()`;
- keep support for `.SchDoc` and `.PrjPcb` inputs plus current auto-detection;
- keep the `--no-indexes` option;
- add or confirm design-doc and manifest coverage so L99 treats the command as
  intentionally public and release-owned.

## Extract Command

`extract` stays in the first public command set. It is the command-line wrapper
around the core Altium Monkey extraction APIs and should be tested with the same
discipline as the underlying extraction logic.

Current behavior to preserve:

- `.SchDoc` input extracts symbols to split and/or combined `SchLib` output;
- `.PcbDoc` input extracts embedded footprints to split and/or combined
  `PcbLib` output;
- `.PrjPcb` input fans out schematic extraction under `schlib/` and PCB
  extraction under `pcblib/`;
- `.IntLib` input extracts embedded source library files from the integrated
  library package using the core `AltiumIntLib` API;
- no file argument auto-detects a project or a single PCB document from the
  working directory;
- `--split`, `--combined`, `--output`, and `--debug` remain supported.

New IntLib source-extraction requirements:

- add command-line coverage for extracting individual source files from an
  `.IntLib`;
- use `AltiumIntLib.extract_sources(...)` rather than reimplementing OLE stream
  extraction in the CLI;
- preserve original source filenames where the IntLib records them, with a
  deterministic fallback for unnamed streams;
- write an extraction manifest that records source kind, stream path, output
  path, and any parse metadata available from the core API;
- write the companion `.LibPkg` generated by the core API by default;
- consider a source-kind filter after the first stable slice, for example
  `all`, `schlib`, `pcblib`, and `pcb3dlib`;
- keep this as part of `extract`; do not add a separate public command unless
  the interface becomes materially different from the existing extraction
  workflow.

Required parity sources:

- SchDoc extraction behavior should track the promoted Altium Monkey tests in
  `toolz-tests/suites/altium_monkey/tests/L5_sch_tools/test_L5_002_extract_symbols.py`;
- focused public API behavior should also cover
  `toolz/altium_monkey/tests/test_schdoc_symbol_extractor.py`;
- PcbDoc footprint extraction behavior should track
  `toolz-tests/suites/altium_monkey/tests/L7_pcb_comprehensive_interop/test_L7_006_pcbdoc_footprint_extraction.py`;
- synthesized extraction and recombine coverage should track
  `toolz-tests/suites/altium_monkey/tests/L7_pcb_comprehensive_interop/test_L7_007_pcbdoc_extract_synthesized.py`;
- IntLib source extraction behavior should track
  `toolz-tests/suites/altium_monkey/tests/L0_foundation/test_L0_016_intlib.py`
  and the public Altium Monkey example
  `examples/intlib_extract_sources/intlib_extract_sources.py`;
- CLI parity expectations should track
  `toolz-tests/suites/altium_monkey/tests/L6_pcb_foundation/test_L6_052_pcbdoc_cpp_cli_extract_parity.py`
  where applicable to the public Python CLI.

Fixture plan:

- copy the required fixture subset from `C:\eli\wn_test_corpus` only after
  proprietary-information review;
- initial SchDoc candidate fixture root:
  `C:\eli\wn_test_corpus\altium\extract_symbols`;
- initial PcbDoc candidate fixture roots include
  `C:\eli\wn_test_corpus\altium\common\pcbdoc_synthesized\case121__pcbdoc_extract_1`
  and any other extraction cases selected from the Altium Monkey promoted
  surface;
- restructure copied fixtures into the public `input/`, `reference_output/`,
  and transient `output/` convention;
- do not check in private-only corpus fixtures until they have been explicitly
  cleared for public redistribution.

Required tests:

- command help and manifest coverage;
- `.SchDoc` split extraction produces the expected symbol-file set;
- `.SchDoc` combined extraction reparses as a valid `SchLib`;
- `.PcbDoc` combined extraction reparses as a valid `PcbLib`;
- `.PcbDoc` split extraction produces the expected footprint-file set and each
  split file reparses;
- `.PrjPcb` extraction creates both `schlib/` and `pcblib/` output folders when
  the project contains both source types;
- `.IntLib` extraction writes parseable source `SchLib` and `PcbLib` files for
  a public fixture such as `RT_SUPER_C1.IntLib` or `loz-old-man.IntLib`;
- `.IntLib` extraction writes a manifest and companion `.LibPkg` with relative
  source references;
- selected golden/reference checks compare against cleared reference output
  using the same semantic comparisons as the underlying Altium Monkey tests,
  not byte-for-byte output unless the format is intentionally stable.

## Split Command

`split` stays in the first public command set. It should be tested like the
previous split command tests, but the public CLI does not need the complex
interop/native parity harness.

Current behavior to preserve:

- `.SchLib` input splits a multi-symbol library into one `SchLib` per symbol;
- `.PcbLib` input splits a multi-footprint library into one `PcbLib` per
  footprint;
- `.SchLib` supports `--pattern` for output filenames;
- `.SchLib` supports `--symbols` for filtering;
- `.PcbLib` rejects `--pattern` and `--symbols` because footprint splitting
  does not support those options today;
- `--output` controls the output folder.

Required test shape:

- use public test projects with checked-in `reference_output/` split results;
- run the public `altium-cruncher split` command, not direct library helpers;
- compare the generated output file set against the provided reference file
  set;
- reparse every generated split library and every reference split library;
- compare stable semantic content such as symbol names, footprint names, and
  selected primitive/stream counts;
- byte-for-byte comparison is not required unless a fixture is intentionally
  declared stable at that level;
- no AD25 plugin, native C++ executable, or complex interop round trip is
  required for this public command test.

Reference material:

- SchLib split behavior can follow
  `toolz-tests/suites/altium_monkey/tests/L5_sch_tools/test_L5_003_schlib_split.py`;
- SchDoc extraction split reference comparisons can be reused as a semantic
  comparison model from
  `toolz-tests/suites/altium_monkey/tests/L5_sch_tools/test_L5_002_extract_symbols.py`;
- PcbLib split behavior can follow the simple split checks in
  `toolz-tests/suites/altium_monkey/tests/L7_pcb_comprehensive_interop/test_L7_006_pcbdoc_footprint_extraction.py`.

## Merge Command

`merge` stays in the first public command set. Its public test requirements
should match the `split` command style: run the public CLI and compare the
result to provided reference outputs from cleared test projects, without the
complex interop/native parity harness.

Current behavior to preserve:

- directory input containing `SchLib` files merges to one multi-symbol
  `SchLib`;
- directory input containing `PcbLib` files merges to one multi-footprint
  `PcbLib`;
- mixed `SchLib`/`PcbLib` input directories are rejected;
- empty or missing input directories are rejected;
- `--conflicts rename`, `--conflicts skip`, and `--conflicts error` remain
  available for `SchLib`;
- `PcbLib` merge currently supports only `--conflicts rename`;
- `--output` controls the output folder.

Required test shape:

- use public test projects with checked-in merged reference libraries;
- run the public `altium-cruncher merge` command, not direct library helpers;
- reparse the generated merged library and the reference merged library;
- compare stable semantic content such as symbol names, footprint names,
  selected primitive/stream counts, and conflict-policy outcomes;
- include at least one SchLib merge reference test and one PcbLib merge
  reference test when cleared fixtures are available;
- byte-for-byte comparison is not required unless a fixture is intentionally
  declared stable at that level;
- no AD25 plugin, native C++ executable, or complex interop round trip is
  required for this public command test.

Reference material:

- SchLib merge behavior can follow
  `toolz-tests/suites/altium_monkey/tests/L5_sch_tools/test_L5_004_schlib_merge.py`;
- the previous split/merge CLI parity shape can be used as a reference from
  `toolz-tests/suites/altium_monkey/tests/L5_sch_tools/test_L5_068_schlib_cpp_cli_split_merge.py`,
  minus the native/interop requirement;
- PcbLib merge can use the recombine checks around `AltiumPcbLib.combine()` in
  `toolz-tests/suites/altium_monkey/tests/L7_pcb_comprehensive_interop/test_L7_006_pcbdoc_footprint_extraction.py`
  and
  `toolz-tests/suites/altium_monkey/tests/L7_pcb_comprehensive_interop/test_L7_007_pcbdoc_extract_synthesized.py`.

## Megamaid Command

`megamaid` stays in the first public command set and should be treated as a
showcase command. It demonstrates the value of `altium-cruncher` as a complete
project decomposition tool rather than only a collection of narrow format
helpers.

Current behavior to preserve:

- `.PrjPcb` input only;
- no file argument auto-detects a project in the working directory;
- output tree includes `schlib/combined`, `schlib/split`, `pcblib/combined`,
  `pcblib/split`, `bom`, `netlist`, `embedded_models`, `embedded_fonts`, and
  `sch_images`;
- stale megamaid-owned output subtrees are cleared on rerun while unrelated
  files in the output root are preserved;
- `megamaid_manifest.json` describes the generated artifacts and scalar counts;
- schematic embedded images, PCB embedded fonts, and PCB embedded models are
  extracted and deduplicated.

Required test shape:

- run the public `altium-cruncher megamaid` command against a cleared
  representative project fixture;
- verify the expected output tree exists and non-empty artifacts are produced;
- reparse generated combined `SchLib` and `PcbLib` outputs;
- verify BOM CSV and netlist JSON are generated;
- verify manifest schema/kind, document counts, artifact paths, and scalar
  counts;
- verify embedded image/font/model extraction when the fixture contains those
  assets;
- verify rerun cleanup removes stale megamaid-owned artifacts without deleting
  unrelated files under the selected output root;
- no native C++ parity sweep is required in the public repo, but the public
  test should still prove the command works end to end.

Reference material:

- current public-repo tests in `tests/test_megamaid_schematic_images.py`;
- old native smoke/parity expectations in
  `toolz-tests/suites/altium_monkey/tests/L6_pcb_foundation/test_L6_050_pcbdoc_cpp_cli_megamaid.py`
  and
  `toolz-tests/suites/altium_monkey/tests/L6_pcb_foundation/test_L6_051_pcbdoc_cpp_cli_megamaid_parity.py`,
  adapted to public Python CLI tests and without the native executable
  requirement.

## Clean Command

`clean` stays in the first public command set. It is useful, but it is also one
of the easiest commands to misuse because behavior is driven by JSON rules that
rewrite design files. The release bar should emphasize clear config
documentation, safe output behavior, and targeted fixture-backed command tests.

Current behavior to preserve:

- `.SchDoc`, `.SchLib`, and `.PrjPcb` use the schematic clean config schema
  `wn.altium.clean.config.v1`;
- `.PcbLib` uses the footprint-library clean config schema
  `wn.altium.pcblib.clean.config.v1`;
- omitted config auto-resolves and, if missing, writes a template then exits
  without mutating the input;
- `.PrjPcb` input applies schematic cleaning across project `SchDoc` files;
- `--output` writes a file for `SchDoc`/`SchLib`/`PcbLib` and a directory tree
  for `PrjPcb`;
- `--backup` and `--backup-path` preserve source files before writing;
- `.PcbLib` clean may discover `altium-pcblib-clean.json` from workspace config
  before falling back to an input-adjacent config.

Config documentation required before release:

- add `docs/design/cli/clean.html` with a complete command design document;
- document when `altium-clean.json` versus `altium-pcblib-clean.json` applies;
- document config auto-generation and the "template created, edit then rerun"
  behavior;
- document output and backup semantics for single files versus `PrjPcb`;
- document supported color formats, font specs, line widths, and no-ERC symbol
  values;
- document every schematic config section:
  - `normalize_pin_fonts`;
  - `normalize_symbol_body_rectangles`;
  - `normalize_power_symbols`;
  - `normalize_net_labels`;
  - `normalize_component_designators`;
  - `normalize_component_parameters`;
  - `normalize_component_free_text`;
  - `normalize_wires`;
  - `normalize_no_erc`;
  - `normalize_sheet_style`;
  - `normalize_symbol_internal_graphics_monochrome`;
- document every PcbLib config section:
  - `remove_mechanical_primitives`;
  - `remove_text_strings`;
  - `remove_regions`;
- provide machine-readable config contracts or examples under `contracts/` and
  make L99 fail if the documented schemas drift from generated templates.

Current test coverage analysis:

- `tests/L3_public_workflows/test_L3_001_public_cli_workflows.py` only checks
  that `clean` creates an `altium-clean.json` template for a copied public
  `SchDoc`;
- `tests/test_schlib_clean_order.py` directly tests helper behavior for
  SchLib body rectangle ordering and reparse safety, but it does not run the
  public CLI;
- `tests/test_pcblib_clean_config.py` tests workspace/config-path discovery for
  PcbLib clean config, but it does not apply PcbLib cleaning;
- there is not yet enough public CLI coverage for actual clean application,
  backup/output behavior, project fanout, PcbLib primitive removal, or config
  contract conformance.

Required release tests:

- keep the existing focused unit tests because they cover important internal
  edge cases cheaply;
- add a CLI test that applies a schematic clean config to a copied `SchLib`,
  writes to an output file, reparses it, and checks a small semantic result
  such as body-rectangle ordering or expected update counts;
- add a CLI test that applies clean to a copied `SchDoc` or small project and
  verifies reparse plus output/backup behavior;
- add a CLI test for `.PrjPcb` fanout when cleared fixtures are available;
- add a CLI test for `.PcbLib` clean that removes known mechanical/text/region
  noise while preserving component bodies, embedded models, keepouts, board
  cutouts, and custom-pad regions as configured;
- add config contract tests that load generated templates and verify their
  schema fields and documented keys;
- avoid byte-for-byte comparisons unless a fixture is explicitly declared
  stable at that level; semantic reparse and targeted field/primitive checks
  are the right default.

Post-release issue candidate:

- create a `clean` rule-development preview tool after the first release;
- likely shape: run clean in a temporary output tree, render before/after
  schematic or footprint previews, show changed-object counts by rule, and
  let a user iterate on JSON rules before writing back to source files;
- this should be a GUI or HTML report workflow and should not block the first
  public CLI release.

## Deferred Commands

`pcblib-footprint-3d` is broken and should not be migrated into the first public
release command set.

Required follow-up:

- remove or hide the command from the public manifest and top-level CLI before
  release;
- keep any implementation code only if it is clearly internal or quarantined
  behind a non-public/deferred status;
- do not write first-release command docs for it;
- add a future repair plan only after a redistributable PcbLib+STEP fixture and
  expected behavior are available.

## EasyEDA Commands

Some newer commands convert EasyEDA designs and currently depend on private
`toolz` `ezeda_monkey` work.

Do not allow these commands to make the public `altium_cruncher` package depend
on private modules.

Current command status:

- `easyeda-import` is a work-in-progress candidate public command for
  generating Altium library artifacts from EasyEDA/LCSC component data;
- `easyeda-review` is a work-in-progress development review command for
  fixture-wide EasyEDA-vs-Altium schematic comparison;
- `easyeda-footprint-review` is a work-in-progress development review command
  for fixture-wide EasyEDA-vs-Altium footprint comparison;
- none of these commands should be treated as release-owned until they have
  been audited and covered with fixture-backed tests.

The intended direction is to move `ezeda_monkey` out of `toolz` into its own
public repository at <https://github.com/wavenumber-eng/easyeda_monkey> and
publish it to PyPI as a normal dependency before finalizing EasyEDA behavior in
`altium-cruncher`. See `EASYEDA_MONKEY_PUBLIC_REPO_PLAN.md` for the detailed
work plan.

That package must have the same public-repo and signoff requirements as
`altium_cruncher`:

- `pyproject.toml` and installable package metadata;
- tests that run from its own repo;
- `wn-rack` strata and `L99_signoff`;
- CI on Windows, macOS, and Linux where practical;
- GitHub Actions release automation with PyPI Trusted Publishing / OIDC where
  possible;
- contributor guide, license, issue templates, and PR template;
- no private `toolz` imports in public package code;
- direct PRs allowed only through CI/signoff.
- the same date-versioning policy used by current Python packages in this
  package family.
- the same ADR/design-doc/contract-conformance and PEP 257 docstring signoff
  expectations as `altium_cruncher`.
- an early ADR for versioning, tagging, release, and traceability policy,
  aligned with the `altium_cruncher` policy.
- the same `uv tool install` CLI install pattern and dependency-minimization
  discipline.

As part of the split, audit `toolz` and `appz` for imports and workspace
dependencies that currently reach into private `ezeda_monkey` or
`altium_cruncher` source. Public-facing packages and applications should consume
the public PyPI/GitHub versions once those repos exist.

Current release policy for `altium_cruncher`:

1. finish `easyeda-monkey` setup, tests, signoff, and release first; COMPLETE
   with `easyeda-monkey==2026.5.26`;
2. keep EasyEDA commands as missing-dependency placeholders in the base
   `altium-cruncher` install until public `easyeda-monkey` is ready;
3. link `altium-cruncher` to `easyeda-monkey` through the
   `altium-cruncher[easyeda]` optional extra; IN PROGRESS;
4. add two `altium-cruncher` lanes after linking:
   - base install verifies clear missing-dependency behavior;
   - EasyEDA extra install verifies real workflows against public fixtures.

EasyEDA command audit requirements:

- run each command from the standalone CLI, not only from direct Python helpers;
- verify saved JSON input paths first so tests do not depend on live API
  availability;
- verify live API/cache behavior separately as an optional or network-marked
  path;
- prove `easyeda-import` writes a reparseable `SchLib`, writes reports, and
  writes preview artifacts when requested;
- prove `easyeda-import --footprint` or `--full` writes a reparseable `PcbLib`
  and footprint report;
- prove the review commands either generate deterministic HTML/SVG review
  artifacts from fixtures or explicitly demote them to dev/deferred status;
- keep all EasyEDA fixtures under the standard `input/`, `reference_output/`,
  and transient `output/` convention;
- L99 should fail if an EasyEDA command is public in the manifest without
  command docs, help tests, fixture-backed behavior tests, and optional-extra
  install coverage.

## AI Skill / Assistant Workflow

The public `altium_monkey` PR
<https://github.com/wavenumber-eng/altium_monkey/pull/1> adds a project-local
Claude Code skill for reading Altium schematics through compact subcommands
such as `summary`, `components`, `nets`, `connections`, `bom`, `sheet`, and
`raw`.

That concept belongs in the `altium_cruncher` app layer rather than core
`altium-monkey`.

Preferred shape:

- implement the underlying design-query behavior as stable
  `altium-cruncher` commands;
- keep compact JSON as a supported machine-consumable mode;
- make any Codex/Claude skill a thin wrapper around the installed CLI;
- do not duplicate parsing logic inside the skill.

## Migration Phases

1. Design and inventory only.
   - Status: substantially complete for the first public bootstrap.
   - Create the migration plan.
   - Inventory commands, tests, fixtures, private dependencies, and command
     outputs.
   - Audit `toolz` and `appz` for private `altium_cruncher` and
     `ezeda_monkey` imports that need to become public package dependencies.

2. Stand up `easyeda-monkey`.
   - Status: COMPLETE. Public package `easyeda-monkey==2026.5.26` is
     published on PyPI and tagged as `easyeda-monkey/v2026.5.26`.
   - Bootstrap the public `easyeda-monkey` repo with the same docs, tests,
     Rack strata, signoff, CI, and release workflow requirements as
     `altium-cruncher`.
   - Use `easyeda-monkey` as the simpler public CI/CD proving ground for GitHub
     Actions, release tags, changelog enforcement, PyPI Trusted Publishing, and
     clean install test before relying on the same path for
     `altium-cruncher`.
   - Initial parser fixtures and tests are migrated and pass locally and in
     GitHub CI.

3. Bootstrap the public repo.
   - Status: initial local bootstrap complete; EasyEDA CI blocker is closed.
   - Add packaging, source layout, Rack tests, CI, project hygiene files, and
     a minimal CLI skeleton.
   - Add the initial versioning/tagging/release-policy ADR before the first
     package release.

4. Migrate stable commands.
   - Status: current stable command modules copied from private `toolz` and
     tested against Hydroscope for the first public slice.
   - Move commands one family at a time.
   - Add manifest entries, tests, and docs as each command lands.

5. Add command parity gates.
   - Status: initial manifest/help checks and `L3_public_workflows` are wired.
     `L99_signoff` now hard-fails missing command design docs and public
     dataclass/interface design ownership, so the next slice must add the
     missing design docs or explicitly classify interfaces as internal.
   - Shared CLI help polish is implemented: root and command help show the
     version, root commands are alphabetical, bare invocation prints help, and
     root help points to command-specific help.
   - Active execution slice: implement the shared output path/name expression
     resolver first, with focused unit tests, so SVG, netlist, BOM, PnP, and
     the planned JLC command can adopt one common output naming contract.
   - Enforce manifest/test/doc coverage.
   - Add `L99_signoff` and package build/install tests.

6. Link EasyEDA into `altium-cruncher`.
   - Status: IN PROGRESS now that `easyeda-monkey` is public.
   - Add optional dependency/extra.
   - Keep command adapters thin and covered by base-install plus extra-install
     lanes.
   - Update README, command inventory, contracts, and release notes.

7. Wire into `wn-hw`.
   - Status: not started; documented as a first-release blocker.
   - Add standalone `altium_cruncher` as a cloned dependency.
   - Update workspace scripts/configuration.
   - Ensure setup/update exposes the console executable path.
   - Add a workspace installer test for the public console script name.

8. Remove from `toolz`.
   - Status: blocked until public repo is pushed, CI is green, and app/workspace
     consumers are migrated.
   - Delete the private `toolz/altium_cruncher` package only after the public
     repo has equivalent command coverage for the selected public command set.
   - Leave a short tombstone pointing to the public repo if useful.

## First Slice Exit Criteria

The first migration slice is complete when:

- the public repo has installable package metadata;
- `uv tool install` can expose the CLI from a built wheel;
- `wn-hw` setup/update can expose the CLI executable without a manual PATH fix;
- Rack tests run from the standalone repo;
- CI runs on Windows and Linux; macOS CI is deferred until the `wn-geometer`
  mac wheel tag matches available GitHub-hosted runners;
- at least one stable command is migrated with fixture-backed coverage;
- the command inventory clearly states which commands remain private,
  deferred, or blocked.

Current local status:

- package metadata, console script, CI/release workflow, changelog, ADRs, design
  docs, and contracts are present;
- `L0_public_cli` and `L3_public_workflows` pass locally; `L99_signoff`
  intentionally remains red for the existing command/interface design-doc
  backlog that must be closed before release;
- built-wheel install test passes locally and verifies the public console
  script through PATH inside a clean venv;
- `ruff` is clean and `py_signoff` is clean; pyright remains an explicit
  backlog item rather than a hard release gate for this bootstrap slice;
- shared output path/name expression resolver is implemented with focused L0
  tests for project parameters, `VariantName`, sanitization, traversal
  rejection, and path separator normalization; the shared API design doc is
  `docs/design/api/output-path-templates.html`;
- the shared resolver is also exercised at L3 against the public Hydroscope
  `PrjPcb` fixture so real project parameters can drive release-style output
  folders;
- CLI help now prints the package version in root and command help, lists
  commands alphabetically, and points users to
  `altium-cruncher <command> --help`;
- `wn-hw` setup/update integration and public GitHub CI remain the major first
  release blockers.
