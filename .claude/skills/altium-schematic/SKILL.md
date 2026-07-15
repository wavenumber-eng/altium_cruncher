---
name: altium-schematic
description: Read Altium schematics and projects (.PrjPcb / .SchDoc) so Claude can answer questions about the circuit — components, nets, pin-level connectivity, BOM, and sheet hierarchy. Use whenever the user asks about an Altium design in this workspace.
---

# altium-schematic

Lets Claude reason about Altium designs through the
[`altium-cruncher`](https://github.com/wavenumber-eng/altium_cruncher) CLI.
The `query` command exposes targeted subcommands so you load only the slice of
design data relevant to the user's question into context — not the whole
400KB+ design JSON.

## When to use

Trigger this skill when the user asks anything about an Altium design in the
workspace, for example:

- "what's connected to U7 pin C9?"
- "list every IC on the codec sheet"
- "which nets cross between sheets?"
- "what's the BOM for the PCBA_Build variant?"
- "what does this schematic do?"

If you don't know which `.PrjPcb` they mean, run `find . -name '*.PrjPcb'` and
ask if there's more than one.

## Prerequisite

The `altium-cruncher` CLI must be available. In an `altium-cruncher` repo
clone, prefix commands with `uv run` so they use the project environment.
Elsewhere, install the tool with `uv tool install altium-cruncher` (see the
README) and call `altium-cruncher` directly.

## How to invoke

`query` subcommands print exactly one JSON payload to stdout. Errors print a
one-line message to stderr with exit code 1. Each subcommand accepts the
project as a positional path (or `--project`); with neither, it auto-detects a
single `.PrjPcb` in the current working directory.

```bash
altium-cruncher query <subcommand> [project.PrjPcb] [options]
```

### Recommended starting point: `summary`

Always run `summary` first when you encounter a project for the first time in
a session. It's small and gives you sheet names, component/net counts,
component-type breakdown, power nets, and variants — everything you need to
plan follow-up queries.

```bash
altium-cruncher query summary path/to/Foo.PrjPcb
```

### Subcommands

| Subcommand    | What it returns                                              | Typical question it answers                |
| ------------- | ------------------------------------------------------------ | ------------------------------------------ |
| `query summary`     | Project overview: sheets, counts, power nets, variants       | "What's in this project?"                  |
| `query components`  | Filtered component list with `--designator`/`--sheet`/`--type`/`--value-contains` (brief rows by default; `--full` for everything) | "List the ICs on the regulator sheet."     |
| `query nets`        | Net listing, or full terminal list with `--name NET`. Use `--contains` for substring match. | "What's on the SDA net?" / "Find P5V*."    |
| `query connections` | Per-pin connectivity for a designator (`query connections U7 [--pin C9]`) | "What's wired to U7 pin C9?"               |
| `query sheet`       | Single `.SchDoc` inspection (no project needed)              | "What does this one sheet contain?"        |

### Related commands for bigger asks

- **BOM:** `altium-cruncher bom project.PrjPcb --format generic-json -o <dir>`
  writes `<Project>_bom.json`; add `--variant <name>` for variant BOMs.
- **Notes:** `altium-cruncher notes project.PrjPcb -o <dir>` extracts
  schematic note objects, text frames, and free text to structured JSON.
- **Variants:** `altium-cruncher variants list project.PrjPcb --json` shows
  variants with DNP and parameter changes.
- **Everything at once:** `altium-cruncher dr project.PrjPcb -o <dir>` writes
  the full agent-facing design-review bundle (design JSON, document JSON,
  notes, schematic SVGs, PCB copper SVGs). Large — only when you truly need
  the whole design or its SVGs.

### Notes

- **Pin identifiers can be alphanumeric** (`C9`, `D8`, `1`, `A1`). Pass them
  as strings to `--pin`.
- **Designators come from project-level annotation.** A bare `.SchDoc`
  inspected via `query sheet` may show empty designators; use
  `query summary`/`query components` on the parent `.PrjPcb` instead.
- **Hierarchical designs work** — the netlist resolves nets across sheets,
  and `query components` reports `sheet` per component so you can scope by
  sheet.
- **The summary's `power_and_ground_nets`** is heuristic (named nets touching
  POWER-type pins, plus GND/VSS substrings). Use `query nets --contains P5V`
  etc. to find rails it missed.

## Strategy for circuit reasoning

For "explain what this circuit does" type questions, do not dump the full
design JSON. Instead:

1. `query summary` to learn sheet names and counts.
2. `query components --sheet <name>` per sheet to see what's on each one.
3. `query nets` to see all named signals.
4. `query connections <main IC designator>` to see how the central part is
   wired.
5. Pull individual nets with `query nets --name <X>` only when needed.

This keeps your context window small and your answers grounded in actual
design data rather than guesses from filenames.

## Example session

User: "What does the dongle do? It's in DONGLE_V2_RELEASED_DESIGN_FILES."

```bash
# 1. Orient yourself
altium-cruncher query summary DONGLE_V2_RELEASED_DESIGN_FILES/Dongle_PRJ.PrjPcb
# → 4 sheets (top + tap_off, codec, regulators), 103 parts, 63 nets,
#   power: P5V0, P3V3_CODEC, P2V5_MIC, P2V5_SPK, GND

# 2. What's on the codec sheet?
altium-cruncher query components DONGLE_V2_RELEASED_DESIGN_FILES/Dongle_PRJ.PrjPcb \
    --sheet Dongle_Sheet2_Codec.SchDoc
# → DA7212-01UM2 (audio codec) + I²C pull-ups + decoupling

# 3. How is the codec wired?
altium-cruncher query connections U7 \
    --project DONGLE_V2_RELEASED_DESIGN_FILES/Dongle_PRJ.PrjPcb
# → SDA/SCL out to J4 with R34/R35 pull-ups, audio I/O to LINE_TAP, etc.
```

Synthesize that into a circuit explanation. Cite designators and net names so
the user can verify against the schematic.
