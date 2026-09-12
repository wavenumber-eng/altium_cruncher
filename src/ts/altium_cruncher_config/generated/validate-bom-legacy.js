// Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit.
// validate.js
var validate = validate20;
var validate_default = validate20;
function validate21(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate21.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
  } else {
    const err0 = { instancePath, schemaPath: "#/$defs/RecordUnknown/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err0];
    } else {
      vErrors.push(err0);
    }
    errors++;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.designator !== void 0) {
      if (typeof data.designator !== "string") {
        const err1 = { instancePath: instancePath + "/designator", schemaPath: "#/properties/designator/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
    }
    if (data.value !== void 0) {
      if (typeof data.value !== "string") {
        const err2 = { instancePath: instancePath + "/value", schemaPath: "#/properties/value/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
    if (data.footprint !== void 0) {
      if (typeof data.footprint !== "string") {
        const err3 = { instancePath: instancePath + "/footprint", schemaPath: "#/properties/footprint/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.library_ref !== void 0) {
      if (typeof data.library_ref !== "string") {
        const err4 = { instancePath: instancePath + "/library_ref", schemaPath: "#/properties/library_ref/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.description !== void 0) {
      if (typeof data.description !== "string") {
        const err5 = { instancePath: instancePath + "/description", schemaPath: "#/properties/description/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.sheet !== void 0) {
      if (typeof data.sheet !== "string") {
        const err6 = { instancePath: instancePath + "/sheet", schemaPath: "#/properties/sheet/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.dnp !== void 0) {
      if (typeof data.dnp !== "boolean") {
        const err7 = { instancePath: instancePath + "/dnp", schemaPath: "#/properties/dnp/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.parameters !== void 0) {
      let data7 = data.parameters;
      if (data7 && typeof data7 == "object" && !Array.isArray(data7)) {
      } else {
        const err8 = { instancePath: instancePath + "/parameters", schemaPath: "#/$defs/RecordUnknown/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
  } else {
    const err9 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err9];
    } else {
      vErrors.push(err9);
    }
    errors++;
  }
  validate21.errors = vErrors;
  return errors === 0;
}
validate21.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate24(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate24.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.designator === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "designator" }, message: "must have required property 'designator'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.value === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "value" }, message: "must have required property 'value'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.footprint === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "footprint" }, message: "must have required property 'footprint'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.library_ref === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "library_ref" }, message: "must have required property 'library_ref'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.description === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "description" }, message: "must have required property 'description'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.sheet === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "sheet" }, message: "must have required property 'sheet'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.dnp === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "dnp" }, message: "must have required property 'dnp'" };
      if (vErrors === null) {
        vErrors = [err6];
      } else {
        vErrors.push(err6);
      }
      errors++;
    }
    if (data.parameters === void 0) {
      const err7 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "parameters" }, message: "must have required property 'parameters'" };
      if (vErrors === null) {
        vErrors = [err7];
      } else {
        vErrors.push(err7);
      }
      errors++;
    }
    if (data.canonical_fields === void 0) {
      const err8 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "canonical_fields" }, message: "must have required property 'canonical_fields'" };
      if (vErrors === null) {
        vErrors = [err8];
      } else {
        vErrors.push(err8);
      }
      errors++;
    }
    if (data.field_sources === void 0) {
      const err9 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "field_sources" }, message: "must have required property 'field_sources'" };
      if (vErrors === null) {
        vErrors = [err9];
      } else {
        vErrors.push(err9);
      }
      errors++;
    }
    if (data.designator !== void 0) {
      if (typeof data.designator !== "string") {
        const err10 = { instancePath: instancePath + "/designator", schemaPath: "#/properties/designator/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
    }
    if (data.value !== void 0) {
      if (typeof data.value !== "string") {
        const err11 = { instancePath: instancePath + "/value", schemaPath: "#/properties/value/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
    }
    if (data.footprint !== void 0) {
      if (typeof data.footprint !== "string") {
        const err12 = { instancePath: instancePath + "/footprint", schemaPath: "#/properties/footprint/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
    }
    if (data.library_ref !== void 0) {
      if (typeof data.library_ref !== "string") {
        const err13 = { instancePath: instancePath + "/library_ref", schemaPath: "#/properties/library_ref/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.description !== void 0) {
      if (typeof data.description !== "string") {
        const err14 = { instancePath: instancePath + "/description", schemaPath: "#/properties/description/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
    }
    if (data.sheet !== void 0) {
      if (typeof data.sheet !== "string") {
        const err15 = { instancePath: instancePath + "/sheet", schemaPath: "#/properties/sheet/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
    }
    if (data.dnp !== void 0) {
      if (typeof data.dnp !== "boolean") {
        const err16 = { instancePath: instancePath + "/dnp", schemaPath: "#/properties/dnp/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
    }
    if (data.parameters !== void 0) {
      let data7 = data.parameters;
      if (data7 && typeof data7 == "object" && !Array.isArray(data7)) {
        for (const key0 in data7) {
          if (typeof data7[key0] !== "string") {
            const err17 = { instancePath: instancePath + "/parameters/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/ImportedBomNormalized_RecordString/unevaluatedProperties/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err17];
            } else {
              vErrors.push(err17);
            }
            errors++;
          }
        }
      } else {
        const err18 = { instancePath: instancePath + "/parameters", schemaPath: "#/$defs/ImportedBomNormalized_RecordString/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
    }
    if (data.canonical_fields !== void 0) {
      let data9 = data.canonical_fields;
      if (data9 && typeof data9 == "object" && !Array.isArray(data9)) {
        for (const key1 in data9) {
          if (typeof data9[key1] !== "string") {
            const err19 = { instancePath: instancePath + "/canonical_fields/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/ImportedBomNormalized_RecordString/unevaluatedProperties/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err19];
            } else {
              vErrors.push(err19);
            }
            errors++;
          }
        }
      } else {
        const err20 = { instancePath: instancePath + "/canonical_fields", schemaPath: "#/$defs/ImportedBomNormalized_RecordString/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
    }
    if (data.field_sources !== void 0) {
      let data11 = data.field_sources;
      if (data11 && typeof data11 == "object" && !Array.isArray(data11)) {
        for (const key2 in data11) {
          if (typeof data11[key2] !== "string") {
            const err21 = { instancePath: instancePath + "/field_sources/" + key2.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/ImportedBomNormalized_RecordString/unevaluatedProperties/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err21];
            } else {
              vErrors.push(err21);
            }
            errors++;
          }
        }
      } else {
        const err22 = { instancePath: instancePath + "/field_sources", schemaPath: "#/$defs/ImportedBomNormalized_RecordString/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
    }
    for (const key3 in data) {
      if (key3 !== "designator" && key3 !== "value" && key3 !== "footprint" && key3 !== "library_ref" && key3 !== "description" && key3 !== "sheet" && key3 !== "dnp" && key3 !== "parameters" && key3 !== "canonical_fields" && key3 !== "field_sources") {
        const err23 = { instancePath: instancePath + "/" + key3.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
    }
  } else {
    const err24 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err24];
    } else {
      vErrors.push(err24);
    }
    errors++;
  }
  validate24.errors = vErrors;
  return errors === 0;
}
validate24.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate23(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate23.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.schema === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "schema" }, message: "must have required property 'schema'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.source === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "source" }, message: "must have required property 'source'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.variant === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "variant" }, message: "must have required property 'variant'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.component_count === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "component_count" }, message: "must have required property 'component_count'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.dnp_count === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "dnp_count" }, message: "must have required property 'dnp_count'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.components === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "components" }, message: "must have required property 'components'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.schema !== void 0) {
      let data0 = data.schema;
      if (typeof data0 !== "string") {
        const err6 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      if ("altium_cruncher.bom.raw.a0" !== data0) {
        const err7 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.bom.raw.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.source !== void 0) {
      let data1 = data.source;
      if (data1 && typeof data1 == "object" && !Array.isArray(data1)) {
        if (data1.path === void 0) {
          const err8 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/ImportedBomNormalized_Source/required", keyword: "required", params: { missingProperty: "path" }, message: "must have required property 'path'" };
          if (vErrors === null) {
            vErrors = [err8];
          } else {
            vErrors.push(err8);
          }
          errors++;
        }
        if (data1.name === void 0) {
          const err9 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/ImportedBomNormalized_Source/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
          if (vErrors === null) {
            vErrors = [err9];
          } else {
            vErrors.push(err9);
          }
          errors++;
        }
        if (data1.stem === void 0) {
          const err10 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/ImportedBomNormalized_Source/required", keyword: "required", params: { missingProperty: "stem" }, message: "must have required property 'stem'" };
          if (vErrors === null) {
            vErrors = [err10];
          } else {
            vErrors.push(err10);
          }
          errors++;
        }
        if (data1.path !== void 0) {
          if (typeof data1.path !== "string") {
            const err11 = { instancePath: instancePath + "/source/path", schemaPath: "#/$defs/ImportedBomNormalized_Source/properties/path/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err11];
            } else {
              vErrors.push(err11);
            }
            errors++;
          }
        }
        if (data1.name !== void 0) {
          if (typeof data1.name !== "string") {
            const err12 = { instancePath: instancePath + "/source/name", schemaPath: "#/$defs/ImportedBomNormalized_Source/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err12];
            } else {
              vErrors.push(err12);
            }
            errors++;
          }
        }
        if (data1.stem !== void 0) {
          if (typeof data1.stem !== "string") {
            const err13 = { instancePath: instancePath + "/source/stem", schemaPath: "#/$defs/ImportedBomNormalized_Source/properties/stem/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err13];
            } else {
              vErrors.push(err13);
            }
            errors++;
          }
        }
        for (const key0 in data1) {
          if (key0 !== "path" && key0 !== "name" && key0 !== "stem") {
            const err14 = { instancePath: instancePath + "/source/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/ImportedBomNormalized_Source/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err14];
            } else {
              vErrors.push(err14);
            }
            errors++;
          }
        }
      } else {
        const err15 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/ImportedBomNormalized_Source/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
    }
    if (data.variant !== void 0) {
      let data6 = data.variant;
      const _errs16 = errors;
      let valid4 = false;
      const _errs17 = errors;
      if (typeof data6 !== "string") {
        const err16 = { instancePath: instancePath + "/variant", schemaPath: "#/properties/variant/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid0 = _errs17 === errors;
      valid4 = valid4 || _valid0;
      const _errs19 = errors;
      if (data6 !== null) {
        const err17 = { instancePath: instancePath + "/variant", schemaPath: "#/properties/variant/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      var _valid0 = _errs19 === errors;
      valid4 = valid4 || _valid0;
      if (!valid4) {
        const err18 = { instancePath: instancePath + "/variant", schemaPath: "#/properties/variant/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      } else {
        errors = _errs16;
        if (vErrors !== null) {
          if (_errs16) {
            vErrors.length = _errs16;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.component_count !== void 0) {
      let data7 = data.component_count;
      if (!(typeof data7 == "number" && (!(data7 % 1) && !isNaN(data7)))) {
        const err19 = { instancePath: instancePath + "/component_count", schemaPath: "#/$defs/ImportedBomNormalized_Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
      if (typeof data7 == "number") {
        if (data7 < 0 || isNaN(data7)) {
          const err20 = { instancePath: instancePath + "/component_count", schemaPath: "#/$defs/ImportedBomNormalized_Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err20];
          } else {
            vErrors.push(err20);
          }
          errors++;
        }
      }
    }
    if (data.dnp_count !== void 0) {
      let data8 = data.dnp_count;
      if (!(typeof data8 == "number" && (!(data8 % 1) && !isNaN(data8)))) {
        const err21 = { instancePath: instancePath + "/dnp_count", schemaPath: "#/$defs/ImportedBomNormalized_Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      if (typeof data8 == "number") {
        if (data8 < 0 || isNaN(data8)) {
          const err22 = { instancePath: instancePath + "/dnp_count", schemaPath: "#/$defs/ImportedBomNormalized_Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err22];
          } else {
            vErrors.push(err22);
          }
          errors++;
        }
      }
    }
    if (data.components !== void 0) {
      let data9 = data.components;
      if (Array.isArray(data9)) {
        const len0 = data9.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!validate24(data9[i0], { instancePath: instancePath + "/components/" + i0, parentData: data9, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate24.errors : vErrors.concat(validate24.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err23 = { instancePath: instancePath + "/components", schemaPath: "#/properties/components/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "schema" && key1 !== "source" && key1 !== "variant" && key1 !== "component_count" && key1 !== "dnp_count" && key1 !== "components") {
        const err24 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
    }
  } else {
    const err25 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err25];
    } else {
      vErrors.push(err25);
    }
    errors++;
  }
  validate23.errors = vErrors;
  return errors === 0;
}
validate23.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate20(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  ;
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate20.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.schema === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "schema" }, message: "must have required property 'schema'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.source === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "source" }, message: "must have required property 'source'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.variant === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "variant" }, message: "must have required property 'variant'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.component_count === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "component_count" }, message: "must have required property 'component_count'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.dnp_count === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "dnp_count" }, message: "must have required property 'dnp_count'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.columns === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "columns" }, message: "must have required property 'columns'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.parameter_columns === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "parameter_columns" }, message: "must have required property 'parameter_columns'" };
      if (vErrors === null) {
        vErrors = [err6];
      } else {
        vErrors.push(err6);
      }
      errors++;
    }
    if (data.components === void 0) {
      const err7 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "components" }, message: "must have required property 'components'" };
      if (vErrors === null) {
        vErrors = [err7];
      } else {
        vErrors.push(err7);
      }
      errors++;
    }
    if (data.raw_components === void 0) {
      const err8 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "raw_components" }, message: "must have required property 'raw_components'" };
      if (vErrors === null) {
        vErrors = [err8];
      } else {
        vErrors.push(err8);
      }
      errors++;
    }
    if (data.normalized === void 0) {
      const err9 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "normalized" }, message: "must have required property 'normalized'" };
      if (vErrors === null) {
        vErrors = [err9];
      } else {
        vErrors.push(err9);
      }
      errors++;
    }
    if (data.schema !== void 0) {
      let data0 = data.schema;
      if (typeof data0 !== "string") {
        const err10 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      if ("altium_cruncher.bom.a0" !== data0) {
        const err11 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.bom.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
    }
    if (data.source !== void 0) {
      let data1 = data.source;
      if (data1 && typeof data1 == "object" && !Array.isArray(data1)) {
        if (data1.path === void 0) {
          const err12 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/Source/required", keyword: "required", params: { missingProperty: "path" }, message: "must have required property 'path'" };
          if (vErrors === null) {
            vErrors = [err12];
          } else {
            vErrors.push(err12);
          }
          errors++;
        }
        if (data1.name === void 0) {
          const err13 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/Source/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
          if (vErrors === null) {
            vErrors = [err13];
          } else {
            vErrors.push(err13);
          }
          errors++;
        }
        if (data1.stem === void 0) {
          const err14 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/Source/required", keyword: "required", params: { missingProperty: "stem" }, message: "must have required property 'stem'" };
          if (vErrors === null) {
            vErrors = [err14];
          } else {
            vErrors.push(err14);
          }
          errors++;
        }
        if (data1.path !== void 0) {
          if (typeof data1.path !== "string") {
            const err15 = { instancePath: instancePath + "/source/path", schemaPath: "#/$defs/Source/properties/path/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err15];
            } else {
              vErrors.push(err15);
            }
            errors++;
          }
        }
        if (data1.name !== void 0) {
          if (typeof data1.name !== "string") {
            const err16 = { instancePath: instancePath + "/source/name", schemaPath: "#/$defs/Source/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err16];
            } else {
              vErrors.push(err16);
            }
            errors++;
          }
        }
        if (data1.stem !== void 0) {
          if (typeof data1.stem !== "string") {
            const err17 = { instancePath: instancePath + "/source/stem", schemaPath: "#/$defs/Source/properties/stem/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err17];
            } else {
              vErrors.push(err17);
            }
            errors++;
          }
        }
        for (const key0 in data1) {
          if (key0 !== "path" && key0 !== "name" && key0 !== "stem") {
            const err18 = { instancePath: instancePath + "/source/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/Source/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err18];
            } else {
              vErrors.push(err18);
            }
            errors++;
          }
        }
      } else {
        const err19 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/Source/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
    }
    if (data.variant !== void 0) {
      let data6 = data.variant;
      const _errs17 = errors;
      let valid4 = false;
      const _errs18 = errors;
      if (typeof data6 !== "string") {
        const err20 = { instancePath: instancePath + "/variant", schemaPath: "#/properties/variant/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      var _valid0 = _errs18 === errors;
      valid4 = valid4 || _valid0;
      const _errs20 = errors;
      if (data6 !== null) {
        const err21 = { instancePath: instancePath + "/variant", schemaPath: "#/properties/variant/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      var _valid0 = _errs20 === errors;
      valid4 = valid4 || _valid0;
      if (!valid4) {
        const err22 = { instancePath: instancePath + "/variant", schemaPath: "#/properties/variant/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      } else {
        errors = _errs17;
        if (vErrors !== null) {
          if (_errs17) {
            vErrors.length = _errs17;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.component_count !== void 0) {
      let data7 = data.component_count;
      if (!(typeof data7 == "number" && (!(data7 % 1) && !isNaN(data7)))) {
        const err23 = { instancePath: instancePath + "/component_count", schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      if (typeof data7 == "number") {
        if (data7 < 0 || isNaN(data7)) {
          const err24 = { instancePath: instancePath + "/component_count", schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err24];
          } else {
            vErrors.push(err24);
          }
          errors++;
        }
      }
    }
    if (data.dnp_count !== void 0) {
      let data8 = data.dnp_count;
      if (!(typeof data8 == "number" && (!(data8 % 1) && !isNaN(data8)))) {
        const err25 = { instancePath: instancePath + "/dnp_count", schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
      if (typeof data8 == "number") {
        if (data8 < 0 || isNaN(data8)) {
          const err26 = { instancePath: instancePath + "/dnp_count", schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err26];
          } else {
            vErrors.push(err26);
          }
          errors++;
        }
      }
    }
    if (data.columns !== void 0) {
      let data9 = data.columns;
      if (Array.isArray(data9)) {
        const len0 = data9.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (typeof data9[i0] !== "string") {
            const err27 = { instancePath: instancePath + "/columns/" + i0, schemaPath: "#/properties/columns/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err27];
            } else {
              vErrors.push(err27);
            }
            errors++;
          }
        }
      } else {
        const err28 = { instancePath: instancePath + "/columns", schemaPath: "#/properties/columns/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
    }
    if (data.parameter_columns !== void 0) {
      let data11 = data.parameter_columns;
      if (Array.isArray(data11)) {
        const len1 = data11.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (typeof data11[i1] !== "string") {
            const err29 = { instancePath: instancePath + "/parameter_columns/" + i1, schemaPath: "#/properties/parameter_columns/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err29];
            } else {
              vErrors.push(err29);
            }
            errors++;
          }
        }
      } else {
        const err30 = { instancePath: instancePath + "/parameter_columns", schemaPath: "#/properties/parameter_columns/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
        }
        errors++;
      }
    }
    if (data.components !== void 0) {
      let data13 = data.components;
      if (Array.isArray(data13)) {
        const len2 = data13.length;
        for (let i2 = 0; i2 < len2; i2++) {
          let data14 = data13[i2];
          if (data14 && typeof data14 == "object" && !Array.isArray(data14)) {
            for (const key1 in data14) {
              if (typeof data14[key1] !== "string") {
                const err31 = { instancePath: instancePath + "/components/" + i2 + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/RecordString/unevaluatedProperties/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err31];
                } else {
                  vErrors.push(err31);
                }
                errors++;
              }
            }
          } else {
            const err32 = { instancePath: instancePath + "/components/" + i2, schemaPath: "#/$defs/RecordString/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err32];
            } else {
              vErrors.push(err32);
            }
            errors++;
          }
        }
      } else {
        const err33 = { instancePath: instancePath + "/components", schemaPath: "#/properties/components/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
    }
    if (data.raw_components !== void 0) {
      let data16 = data.raw_components;
      if (Array.isArray(data16)) {
        const len3 = data16.length;
        for (let i3 = 0; i3 < len3; i3++) {
          if (!validate21(data16[i3], { instancePath: instancePath + "/raw_components/" + i3, parentData: data16, parentDataProperty: i3, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err34 = { instancePath: instancePath + "/raw_components", schemaPath: "#/properties/raw_components/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
        }
        errors++;
      }
    }
    if (data.normalized !== void 0) {
      if (!validate23(data.normalized, { instancePath: instancePath + "/normalized", parentData: data, parentDataProperty: "normalized", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate23.errors : vErrors.concat(validate23.errors);
        errors = vErrors.length;
      }
    }
    for (const key2 in data) {
      if (key2 !== "schema" && key2 !== "source" && key2 !== "variant" && key2 !== "component_count" && key2 !== "dnp_count" && key2 !== "columns" && key2 !== "parameter_columns" && key2 !== "components" && key2 !== "raw_components" && key2 !== "normalized") {
        const err35 = { instancePath: instancePath + "/" + key2.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err35];
        } else {
          vErrors.push(err35);
        }
        errors++;
      }
    }
  } else {
    const err36 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err36];
    } else {
      vErrors.push(err36);
    }
    errors++;
  }
  validate20.errors = vErrors;
  return errors === 0;
}
validate20.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
export {
  validate_default as default,
  validate
};
