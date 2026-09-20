# Bluetooth Sentinel rigid-flex fixture

This fixture contains the `Bluetooth_Sentinel.PcbDoc` needed to qualify
source-aware board-region and local layer-stack thickness behavior. It was
copied byte-for-byte from the shared Wavenumber Altium corpus at
`altium/common/real_world_pcbdoc/bluetooth_sentinel_flex/input` on 2026-09-19
at the repository owner's direction.

Bluetooth Sentinel is an example project bundled with Altium Designer and
used in Altium's public rigid-flex documentation. Only the PcbDoc required by
the tests is imported here; project, schematic, history, generated-output, and
reference-output files remain outside this repository. See
`source-manifest.json` for the exact source identity and provenance links.

The source-aware layer-stack oracle has one physical stack, two substacks, and
three board regions:

- two rigid regions use a 32.1455 mil resolved envelope;
- one flex region uses a 3.3267 mil resolved envelope.

Use this as focused region-query coverage and an opt-in end-to-end Toon case.
Do not place generated render output beside the committed input; tests should
write to their temporary directory.
