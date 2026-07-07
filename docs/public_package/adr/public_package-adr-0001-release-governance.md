+++
type = "adr"
id = "public_package-adr-0001"
domain = "public_package"
status = "accepted"
title = "Release Governance Uses Public Package Metadata"
created = "2026-07-06"
requirement_refs = ["public_package-req-0001"]
+++

# Release Governance Uses Public Package Metadata

## Context

`altium-cruncher` publishes a standalone public Python package. The public
package version, changelog, release notes, command manifest, and Rack signoff
must agree before GitHub Actions can publish to PyPI.

## Decision

The package release process is governed by the date-based version in
`pyproject.toml`, the matching `src/py/altium_cruncher/_version.py` value, the
dated release note under `docs/releases/`, and the release signoff tests under
`tests/L99_signoff`.

## Consequences

Public command additions update the command manifest, CLI design docs, release
notes, focused tests, and Rack signoff before release publication.
