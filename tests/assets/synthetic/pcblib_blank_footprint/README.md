# Blank PcbLib Footprint Fixture

This synthetic fixture is generated through the public MCO-backed command:

```powershell
uv run python -m altium_cruncher pcblib create `
  tests\assets\synthetic\pcblib_blank_footprint\blank_footprint.PcbLib `
  --footprint BLANK_FOOTPRINT `
  --emit-mco tests\assets\synthetic\pcblib_blank_footprint\blank_footprint.mco.json `
  --force
```

The checked-in MCO is the fixture provenance. The PcbLib intentionally starts
with one blank footprint so it can be opened in Altium and annotated with
additional footprint parameters for future regression work.
