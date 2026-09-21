# Kame IMU rigid-flex fixture

This fixture contains only `Kame_IMU.PcbDoc`, copied byte-for-byte from the
repository-owner-supplied `Sample - Kame_IMU` project on 2026-09-20. Project,
schematic, output-job, BOM, drawing, report, and project-structure files are
intentionally excluded because Toon can exercise this board from its PcbDoc.
See `source-manifest.json` for the source hash and import authorization.

The source-aware layer-stack query resolves 51 components and three valid board
regions with no invalid regions:

- rigid region `A` uses substack `Rigid1` at 34.1479 mil;
- rigid region `C` uses substack `Rigid2` at 34.1479 mil;
- flex region `B` uses substack `Flex` at 6.3391 mil.

Use this with `bluetooth_sentinel_flex` for the Gate 5 flat rigid-flex Toon
review. The renderer does not fold flex geometry; bend lines remain virtual
drafting graphics. Generated SVGs and galleries belong under ignored `temp/`
or `output/` paths, not beside the committed input.
