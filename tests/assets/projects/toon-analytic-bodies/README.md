# Toon analytic bodies

Generated Gate 6 fixture for component-owned Altium analytic 3D bodies.

- Input: `input/toon_analytic_bodies.PcbDoc`
- Generator: `tests/support_scripts/generate_toon_analytic_bodies.py`
- Semantic inventory: `semantic-inventory.json`
- Provenance and content identity: `source-manifest.json`

Regenerate from the repository root:

```powershell
uv run python tests/support_scripts/generate_toon_analytic_bodies.py
```

The fixture contains no third-party design content. It intentionally includes
top/bottom bodies, all supported analytic model types, Z interactions,
through-board geometry, edge/cutout overhangs, partial opacity, and a
zero-opacity omission control.
