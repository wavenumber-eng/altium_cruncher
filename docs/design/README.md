# Design Documentation

This folder records durable command, interface, data-flow, and format design
notes.

The master HTML entry point is `index.html`. Command design docs live under
`cli/`, API/interface design docs live under `api/`, and all public design HTML
uses `styles.css`.

Public JSON outputs, command config files, and stable machine-consumable
contracts should have design documentation here and conformance tests under
`tests/`.

L99 signoff enforces:

- every command in `docs/contracts/command_manifest.v0.json` has
  `docs/design/cli/<command>.html`;
- every command doc declares usage, arguments, output, tests, and config
  contract status;
- every public dataclass and every listed major interface has a design-doc
  section with Rack test ownership.

Current design notes:

- `command-inventory.md` - migrated command list and coverage status.
- `dependency-audit.md` - private workspace dependency references to address
  during the standalone migration.
- `quality-signoff-status.md` - current release-gate status and pyright backlog.

CLI install, command layout, licensing boundary, and dependency discipline are
defined in `docs/adrs/ADR-0002-cli-install-and-dependency-discipline.md`.
Design-doc and test-ownership signoff is defined in
`docs/adrs/ADR-0005-design-doc-and-test-ownership-signoff.md`.
