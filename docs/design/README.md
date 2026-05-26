# Design Documentation

This folder records durable command, interface, data-flow, and format design
notes.

Public JSON outputs, command config files, and stable machine-consumable
contracts should have design documentation here and conformance tests under
`tests/`.

Current design notes:

- `command-inventory.md` - migrated command list and coverage status.
- `dependency-audit.md` - private workspace dependency references to address
  during the standalone migration.
- `quality-signoff-status.md` - current release-gate status and pyright backlog.
- `wn-hw-installer-integration.md` - setup/update executable path contract.

CLI install, command layout, licensing boundary, and dependency discipline are
defined in `docs/adrs/ADR-0002-cli-install-and-dependency-discipline.md`.
