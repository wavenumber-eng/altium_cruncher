"""Rack tests for shared output path template resolution."""

from __future__ import annotations

from pathlib import PurePosixPath

import pytest

from altium_cruncher.output_path_templates import (
    MissingOutputPathParameterError,
    OutputPathTemplateError,
    resolve_output_expression,
    resolve_output_name,
    resolve_output_relative_path,
)


_PROJECT_PARAMETERS = {
    "Revision": "1",
    "RevisionMinor": "0",
    "PartNumberPCB": "175-TEST-PCB",
    "PartNumberPCBA": "830-TEST-PCBA",
    "Title": "node test array",
}


def test_concat_expression_builds_release_folder_from_project_parameters() -> None:
    """Verify Altium-style string-plus-parameter path expressions."""
    expression = (
        "'releases/rev' + Revision + '.' + RevisionMinor + '/' + "
        "PartNumberPCBA + ' - ' + Title + ' rev' + Revision + '.' + "
        "RevisionMinor + ' - assy'"
    )

    resolved = resolve_output_relative_path(expression, _PROJECT_PARAMETERS)

    assert resolved == PurePosixPath(
        "releases/rev1.0/830-TEST-PCBA - node test array rev1.0 - assy"
    )


def test_variant_name_token_resolves_current_processed_variant() -> None:
    """Verify the reserved VariantName token is supplied at runtime."""
    expression = "'releases/' + VariantName + '/' + PartNumberPCB"

    resolved = resolve_output_relative_path(
        expression,
        _PROJECT_PARAMETERS,
        variant_name="B4",
    )

    assert resolved == PurePosixPath("releases/B4/175-TEST-PCB")


def test_brace_template_supports_command_tokens_and_project_parameters() -> None:
    """Verify brace templates for non-Altium-style config strings."""
    template = "{Command}/{VariantName}/{PartNumberPCB}-{OutputKind}"

    resolved = resolve_output_relative_path(
        template,
        _PROJECT_PARAMETERS,
        variant_name="base",
        tokens={"Command": "pnp", "OutputKind": "json"},
    )

    assert resolved == PurePosixPath("pnp/base/175-TEST-PCB-json")


def test_output_name_rejects_path_separators() -> None:
    """Verify filename-only resolution cannot accidentally create subfolders."""
    with pytest.raises(OutputPathTemplateError, match="path separators"):
        resolve_output_name("'{PartNumberPCB}/pnp.csv'", _PROJECT_PARAMETERS)


def test_missing_parameter_can_raise_or_resolve_empty() -> None:
    """Verify missing parameter policy is explicit."""
    with pytest.raises(MissingOutputPathParameterError, match="Missing"):
        resolve_output_expression("'release/' + Missing", _PROJECT_PARAMETERS)

    assert (
        resolve_output_expression(
            "'release/' + Missing + '/pnp'",
            _PROJECT_PARAMETERS,
            missing="empty",
        )
        == "release//pnp"
    )


def test_relative_output_path_sanitizes_invalid_filename_characters() -> None:
    """Verify generated path parts are safe on Windows, macOS, and Linux."""
    parameters = dict(_PROJECT_PARAMETERS)
    parameters["Title"] = "daplink: duo*?"

    resolved = resolve_output_relative_path(
        "'releases/' + PartNumberPCBA + ' - ' + Title",
        parameters,
    )

    assert resolved == PurePosixPath("releases/830-TEST-PCBA - daplink_ duo__")


def test_relative_output_path_rejects_absolute_and_traversal_paths() -> None:
    """Verify generated output paths cannot escape the selected output root."""
    with pytest.raises(OutputPathTemplateError, match="relative"):
        resolve_output_relative_path("'/release'", _PROJECT_PARAMETERS)

    with pytest.raises(OutputPathTemplateError, match="drive prefix"):
        resolve_output_relative_path("'C:\\release'", _PROJECT_PARAMETERS)

    with pytest.raises(OutputPathTemplateError, match="traversal"):
        resolve_output_relative_path("'release/../pnp'", _PROJECT_PARAMETERS)


def test_relative_output_path_normalizes_backslashes() -> None:
    """Verify Windows-style separators normalize to the common relative path form."""
    resolved = resolve_output_relative_path(
        "'releases\\rev' + Revision + '\\' + VariantName",
        _PROJECT_PARAMETERS,
        variant_name="A",
    )

    assert resolved == PurePosixPath("releases/rev1/A")
