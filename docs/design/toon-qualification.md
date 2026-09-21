# Toon qualification and performance reference

Implementation and cleanup completed on 2026-09-12. This records the qualified
behavior and measurement method for future maintenance and the Rust port.
Publication is a separate release action; this closeout did not publish a
Cruncher package or tag.

## Durable implementation references

- [Toon command](cli/toon.html): editable configuration, project discovery,
  variants, top/bottom and assembly presets, progress, timings and cache controls.
- [PCB SVG command](cli/pcb-svg.html): composable illustration, designator,
  solder-mask film and substrate layers, styles, coordinate metadata and durable
  generated-group replacement.
- [Architecture and Rust port guide](architecture-porting-guide.md): CLI
  workflows, source immutability, native boundaries, body ordering, ordinary
  assembly-label pad fallback and behavioral tests. Toon views that co-compose
  component illustration omit projected labels for model-less parts.
- [Public contract authority](public-contract-authority.md): all 45 Cruncher
  JSON/JSONC roots, generated Python and browser bindings, ownership boundaries
  and compatibility rules. The GUI editor remains separate work.

The qualified runtime uses Python 3.14, Altium Monkey 2026.9.12 and Geometer
2026.9.11; EasyEDA Monkey requires 2026.9.11 or newer. Fast HLR detail and Fast
Mesh Shadow remain defaults. Toon exports SVG only; raster conversion belongs to
consumers. The test extra retains a rasterizer for selected SVG pixel assertions.

## Performance method and findings

Use `tests/support_scripts/profile_pcb_svg.py` for synchronous phase attribution
and repeat-view byte comparisons. Use `profile_svg_workers.py` for whole-board
worker experiments. Keep ordinary wall-clock runs separate from instrumented
runs: cProfile includes overhead and can misattribute background stderr-reader
time to Geometer shutdown. Explicit wall timers previously measured millisecond
shutdowns where profiler stacks appeared to show seconds.

Record project, board, variant, side and layer durations using the command's
timing report. Nested layer durations overlap their parent view/job durations;
do not sum them. Compare identical inputs, presets, worker counts, dependency
versions, warnings and output SVGs. Distinguish disabled caches, cache fill and
warm model/artwork caches from the operating system's file cache. Dependency
changes can invalidate the native cache even when the output directory is named
"warm". Measure memory as well as time when increasing worker count; sampled
aggregate RSS counts shared pages.

The implemented reuse has several levels: board contexts and primitive indexes,
physical/film and silk fragments, per-model native results, component artwork,
and final population filtering. Complete warm component artwork bypasses native
tessellation, mesh transforms and appearance hashing. Variants reuse compatible
work and filter population at composition time. Cache failures remain misses and
native failures retry; neither is persisted as successful empty artwork.

Toon loads PrjPcb metadata without eagerly parsing schematics, preserving project
parameters, variants and special-string context. Other commands retain their
existing full-design defaults. The upstream source-provenance removal is
consumed directly; Cruncher adds no snapshot compatibility path.

Native work uses bounded separate Geometer processes, default four workers.
Worker completion order does not change source-order diagnostics or SVG paint
order. Increasing the count is machine/workload dependent. The Windows native
build audit found optimized Geometer and cached OCCT Release builds, not an
accidental Debug build; compile parallelism is distinct from render concurrency.
Geometer's illustration optimizations are consumed in 2026.9.11. Future native
work should measure IPC, validation, visibility, color fusion, line generation
and serialization separately while preserving the qualified geometry and style.

For historical scale, these single warm-cache SVG-only qualification samples
used Python 3.14.6, Monkey/Geometer 2026.9.11 and four workers, before the corrected
Monkey 2026.9.12 consumption:

| Board | SVGs | Whole command |
| --- | ---: | ---: |
| RT Super C1, base and both variants | 6 | 4.218 s |
| Loz Old Man | 2 | 5.297 s |
| NXP FRDM i.MX93 | 2 | 17.104 s |
| OV Tech Pi.MX8 | 2 | 10.745 s |

All 12 outputs and ordered model warnings matched their reference. The corrected
Monkey 2026.9.12 qualification also preserved those 12 SVG/warning comparisons.
These are historical samples, not medians, performance guarantees or benchmarks
of the final cleanup. Do not add gains from separate development checkpoints.
Existing NXP L713 candidate-limit and OV U16 JSON-size-limit failures remain
partial-render warnings and affect warm timings because failed models retry.
Alternate-part model substitution remains unsupported.

The discarded raster experiment found a combined benefit from a local resvg
level-3 build and a smaller SVG dimension rewrite, with matching pixels. It did
not isolate those savings and did not ship an optimized wheel or cross-platform
build pipeline. Reopening raster support requires a separate decision.

## Cleanup and correctness evidence

The original Python hygiene gate reported 148 findings: four module-size,
37 complexity, 106 annotation and one Any-count finding. Cleanup removed all
148 without changing the baseline. Any annotations fell from 204 to 190 against
the existing cap of 192. Shared command services and typed rendering/cache
boundaries are described in the architecture guide; legacy dispatch seams remain
explicitly documented rather than hidden behind a claim of complete redesign.

Independent reviews covered every CLI registration/dispatch row, contract
coverage, model/cache ownership and component/view geometry. Cache decoders now
reject malformed scales, coordinates, triangle/material indexes and array
lengths before returning a hit; seven regression cases protect recovery.

The final durable-SVG fix refreshes the generator-owned scene transform when
mirror settings or canvas width change, removes the reflection when disabled,
and wraps legacy root-level groups. It preserves user scene attributes,
annotations and wrappers. Five regression cases cover these transitions and
unchanged settings; four failed before the fix. The artifact/view/Toon suite
passes 60 tests, and independent review found no blocking issue.

Combined cleanup validation passed 639 standalone tests with one optional skip
and all 13 Rack subtests: 83 tests, zero failures and one skip. TypeSpec freshness
covered 454 artifacts across 45 roots; TypeScript and all 124 browser vectors
passed. Wheel/sdist build, Twine, installed-console smoke and development-standard
checks passed. Focused checks and packaging are refreshed after the final SVG
fix. The new transition tests use small in-memory XML and no native models.

Real RT Super C1 checks exercised all three populations, both sides and assembly
labels. Repeat views and cold/warm jobs produced byte-identical SVGs. The warm
job hit both complete component-artwork entries and started zero native clients.
The review generator produced 12 plain/assembly SVG views for the same project.

Local evidence is under `output/contracts-migration/cleanup-*` and
`output/contracts-migration/toon-closeout-*`; profiling artifacts are under
`output/profiling/`. These ignored machine-local files are not package contents.
Working notes were preserved locally in `output/plan-closeout/toon-release.zip`
before retiring the completed plan according to
[ADR-0004](../adrs/ADR-0004-documentation-lifecycle-and-release-boundary.md).
