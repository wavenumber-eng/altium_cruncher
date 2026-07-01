# Nuitka Packaging Evaluation - 2026-07-01

## Scope

This evaluation tested a Windows standalone Nuitka build for the
`altium-cruncher` `2026.7.1` release candidate, using
`altium-monkey==2026.7.1` and `wn-geometer==2026.6.10`.

## Build

Command:

```powershell
uv run --with nuitka python -m nuitka --standalone --assume-yes-for-downloads `
  --output-dir=output\nuitka `
  --output-filename=altium-cruncher-nuitka.exe `
  --include-package=altium_cruncher `
  --include-package=altium_monkey `
  --include-distribution-metadata=altium-monkey `
  --include-distribution-metadata=wn-geometer `
  src\py\altium_cruncher\__main__.py
```

Result:

- Build succeeded with Nuitka `4.1.3`, Python `3.12.12`, and MSVC `cl 14.3`.
- Build time was approximately 7.5 minutes on the local Windows workstation.
- Standalone output: `output\nuitka\__main__.dist\altium-cruncher-nuitka.exe`.
- Executable size: about 91 MB.
- Full standalone distribution size: about 125 MB across 42 files.

The first attempt to include editable `altium-cruncher` distribution metadata
failed. The working build omits that metadata and relies on the package's
internal `__version__` fallback while still including controlled dependency
metadata for `altium-monkey` and `wn-geometer`.

## Smoke Results

The standalone executable reported:

```text
altium-cruncher 2026.7.1
altium-monkey 2026.7.1
wn-geometer 2026.6.10
```

Timed smoke run:

| Command | Time |
| --- | ---: |
| Python `--version` | 0.547 s |
| Nuitka `--version` | 0.410 s |
| Python `bom --format generic-json` | 1.412 s |
| Nuitka `bom --format generic-json` | 1.453 s |
| Python `pnp --format json` | 1.503 s |
| Nuitka `pnp --format json` | 1.513 s |
| Nuitka `extract --combined` | 2.045 s |
| Nuitka `pcb-svg` | 8.254 s |
| Nuitka `megamaid` | 11.594 s |

Artifact checks:

- Nuitka BOM JSON hash matched normal Python output.
- Nuitka PnP JSON hash matched normal Python output.
- Nuitka `extract` produced `CPU.SchLib`.
- Nuitka `pcb-svg` produced SVG outputs for the public cricket-node fixture.
- Nuitka `megamaid` produced `megamaid_manifest.json` for the public Hydroscope
  fixture.

## Recommendation

Nuitka standalone packaging is viable enough to keep evaluating as a
distribution path. It does not materially accelerate the tested BOM/PnP
workflows, but it does reduce user-facing Python installation complexity and
successfully carries the current public workflow dependencies.

Next steps before making it an install path:

- Add a repeatable packaging script instead of relying on an ad-hoc command.
- Test a one-file build variant and compare startup, size, and AV/signing
  behavior.
- Run the same smoke matrix on a clean Windows machine without the development
  environment.
- Decide whether app runtime tooling installs a PyPI `uv tool`, a Nuitka
  standalone bundle, or selected native C++ accelerators.
