"""Cross-runtime regressions found by independent contract review."""
import json
from pathlib import Path
from copy import deepcopy

import pytest

from altium_cruncher.contracts.generated.public import decode_contract

ROOT = Path(__file__).resolve().parents[1]
VECTORS = json.loads((ROOT / "tests/fixtures/workflow-contract-vectors.json").read_text())


@pytest.mark.parametrize("vector", VECTORS, ids=lambda value: value["name"])
def test_shared_workflow_vector(vector):
    original = deepcopy(vector["value"])
    if vector["valid"]:
        assert decode_contract(vector["contract"], vector["value"]) == original
    else:
        with pytest.raises(ValueError):
            decode_contract(vector["contract"], vector["value"])
    assert vector["value"] == original


def test_every_public_schema_has_generated_authority_and_local_references():
    catalog = json.loads((ROOT / "src/py/altium_cruncher/contracts/generated/catalog.json").read_text())
    catalog_schemas = {
        schema
        for row in catalog
        for schema in (row["schema"], *row.get("compatibility_schemas", ()))
    }
    assert catalog_schemas == {
        path.relative_to(ROOT).as_posix() for path in (ROOT / "docs/contracts").glob("*.schema.json")
    }
    for row in catalog:
        assert (ROOT / row["source"]).is_file()
        for schema_path in (row["schema"], *row.get("compatibility_schemas", ())):
            schema = json.loads((ROOT / schema_path).read_text())
            def visit(value):
                if isinstance(value, dict):
                    if "$ref" in value:
                        assert value["$ref"].startswith("#/$defs/")
                        assert value["$ref"].split("/")[-1] in schema["$defs"]
                    for child in value.values():
                        visit(child)
                elif isinstance(value, list):
                    for child in value:
                        visit(child)
            visit(schema)
    decode_contract("interface_design_manifest", json.loads((ROOT / "docs/contracts/interface_design_manifest.a0.json").read_text()))


def test_bom_prefix_fallback_and_owned_defaults():
    from altium_cruncher.bom_pnp_model import BomPnpConfig
    from altium_cruncher.contracts.workflows import workflow_metadata

    assert BomPnpConfig.from_mapping({"bom": {"prefix_order": ["TP", "R"]}}).prefix_order == ("TP", "R")
    assert BomPnpConfig.from_mapping({}).to_json_obj() == BomPnpConfig().to_json_obj()
    assert BomPnpConfig().to_json_obj() == workflow_metadata("bom_pnp_config", "resolved-defaults")
