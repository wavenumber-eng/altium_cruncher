# Altium Cruncher

Command-line tools for working with Altium projects, schematics, boards and
libraries on Windows, macOS and Linux. Export SVGs, generate BOM and pick-and-place
files, extract library assets, and inspect or modify designs.

## Install uv

[uv](https://docs.astral.sh/uv/) installs the application and manages its Python
runtime and dependencies.

On Windows, open PowerShell and run:

```powershell
powershell -ExecutionPolicy Bypass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

On macOS or Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart your terminal after installing uv.

## Install Altium Cruncher

To install the published package:

```sh
uv tool install altium-cruncher
uv tool update-shell
```

To install directly from GitHub, with Git installed:

```sh
uv tool install --force "git+https://github.com/wavenumber-eng/altium_cruncher.git@main"
uv tool update-shell
```

For a specific branch, tag or commit, replace `main` in the URL with that
reference. Both installation methods provide the same command names:
`altium-cruncher` and its shorter alias, `acr`.

Open a new terminal if the command is not found, then verify the installation:

```sh
acr version
acr --help
```

## Update

For an installation from PyPI:

```sh
uv tool upgrade altium-cruncher
```

For an installation from a GitHub branch, rerun the install command with
`--reinstall-package` to refresh the source:

```sh
uv tool install --force --reinstall-package altium-cruncher "git+https://github.com/wavenumber-eng/altium_cruncher.git@main"
```

Use the same branch reference you selected when installing.

## Use

Get help for any command:

```sh
acr pcb-svg --help
acr bom --help
```

For example, export a board SVG or a project BOM:

```sh
acr pcb-svg board.PcbDoc
acr bom project.PrjPcb
```

See the [command guide](docs/design/command-inventory.md) for the complete command
list and links to individual usage instructions. Some commands, such as launching
Altium Designer and running OutJobs, require Altium Designer on Windows.

## Uninstall

```sh
uv tool uninstall altium-cruncher
```

## Documentation

- [Command reference](docs/design/cli/index.html)
- [Examples](examples/)
- [Development and testing](docs/build.md)
- [Contributing](CONTRIBUTING.md)
- [Architecture](docs/design/architecture-porting-guide.md)
- [Release notes](CHANGELOG.md)

Altium Cruncher is licensed under [AGPL-3.0-or-later](LICENSE).
