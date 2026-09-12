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
    if (data.designator === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "designator" }, message: "must have required property 'designator'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.comment === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "comment" }, message: "must have required property 'comment'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.layer === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "layer" }, message: "must have required property 'layer'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.footprint === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "footprint" }, message: "must have required property 'footprint'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.center_x === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "center_x" }, message: "must have required property 'center_x'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.center_y === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "center_y" }, message: "must have required property 'center_y'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.rotation === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "rotation" }, message: "must have required property 'rotation'" };
      if (vErrors === null) {
        vErrors = [err6];
      } else {
        vErrors.push(err6);
      }
      errors++;
    }
    if (data.units === void 0) {
      const err7 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "units" }, message: "must have required property 'units'" };
      if (vErrors === null) {
        vErrors = [err7];
      } else {
        vErrors.push(err7);
      }
      errors++;
    }
    if (data.description === void 0) {
      const err8 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "description" }, message: "must have required property 'description'" };
      if (vErrors === null) {
        vErrors = [err8];
      } else {
        vErrors.push(err8);
      }
      errors++;
    }
    if (data.parameters === void 0) {
      const err9 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "parameters" }, message: "must have required property 'parameters'" };
      if (vErrors === null) {
        vErrors = [err9];
      } else {
        vErrors.push(err9);
      }
      errors++;
    }
    if (data.canonical_fields === void 0) {
      const err10 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "canonical_fields" }, message: "must have required property 'canonical_fields'" };
      if (vErrors === null) {
        vErrors = [err10];
      } else {
        vErrors.push(err10);
      }
      errors++;
    }
    if (data.field_sources === void 0) {
      const err11 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "field_sources" }, message: "must have required property 'field_sources'" };
      if (vErrors === null) {
        vErrors = [err11];
      } else {
        vErrors.push(err11);
      }
      errors++;
    }
    if (data.designator !== void 0) {
      if (typeof data.designator !== "string") {
        const err12 = { instancePath: instancePath + "/designator", schemaPath: "#/properties/designator/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
    }
    if (data.comment !== void 0) {
      if (typeof data.comment !== "string") {
        const err13 = { instancePath: instancePath + "/comment", schemaPath: "#/properties/comment/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.layer !== void 0) {
      if (typeof data.layer !== "string") {
        const err14 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
    }
    if (data.footprint !== void 0) {
      if (typeof data.footprint !== "string") {
        const err15 = { instancePath: instancePath + "/footprint", schemaPath: "#/properties/footprint/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
    }
    if (data.center_x !== void 0) {
      if (!(typeof data.center_x == "number")) {
        const err16 = { instancePath: instancePath + "/center_x", schemaPath: "#/properties/center_x/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
    }
    if (data.center_y !== void 0) {
      if (!(typeof data.center_y == "number")) {
        const err17 = { instancePath: instancePath + "/center_y", schemaPath: "#/properties/center_y/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
    }
    if (data.rotation !== void 0) {
      if (!(typeof data.rotation == "number")) {
        const err18 = { instancePath: instancePath + "/rotation", schemaPath: "#/properties/rotation/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
    }
    if (data.units !== void 0) {
      if (typeof data.units !== "string") {
        const err19 = { instancePath: instancePath + "/units", schemaPath: "#/properties/units/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
    }
    if (data.description !== void 0) {
      if (typeof data.description !== "string") {
        const err20 = { instancePath: instancePath + "/description", schemaPath: "#/properties/description/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
    }
    if (data.parameters !== void 0) {
      let data9 = data.parameters;
      if (data9 && typeof data9 == "object" && !Array.isArray(data9)) {
        for (const key0 in data9) {
          if (typeof data9[key0] !== "string") {
            const err21 = { instancePath: instancePath + "/parameters/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/RecordString/unevaluatedProperties/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err21];
            } else {
              vErrors.push(err21);
            }
            errors++;
          }
        }
      } else {
        const err22 = { instancePath: instancePath + "/parameters", schemaPath: "#/$defs/RecordString/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
    }
    if (data.canonical_fields !== void 0) {
      let data11 = data.canonical_fields;
      if (data11 && typeof data11 == "object" && !Array.isArray(data11)) {
        for (const key1 in data11) {
          if (typeof data11[key1] !== "string") {
            const err23 = { instancePath: instancePath + "/canonical_fields/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/RecordString/unevaluatedProperties/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err23];
            } else {
              vErrors.push(err23);
            }
            errors++;
          }
        }
      } else {
        const err24 = { instancePath: instancePath + "/canonical_fields", schemaPath: "#/$defs/RecordString/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
    }
    if (data.field_sources !== void 0) {
      let data13 = data.field_sources;
      if (data13 && typeof data13 == "object" && !Array.isArray(data13)) {
        for (const key2 in data13) {
          if (typeof data13[key2] !== "string") {
            const err25 = { instancePath: instancePath + "/field_sources/" + key2.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/RecordString/unevaluatedProperties/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err25];
            } else {
              vErrors.push(err25);
            }
            errors++;
          }
        }
      } else {
        const err26 = { instancePath: instancePath + "/field_sources", schemaPath: "#/$defs/RecordString/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
    }
    for (const key3 in data) {
      if (key3 !== "designator" && key3 !== "comment" && key3 !== "layer" && key3 !== "footprint" && key3 !== "center_x" && key3 !== "center_y" && key3 !== "rotation" && key3 !== "units" && key3 !== "description" && key3 !== "parameters" && key3 !== "canonical_fields" && key3 !== "field_sources") {
        const err27 = { instancePath: instancePath + "/" + key3.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
    }
  } else {
    const err28 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err28];
    } else {
      vErrors.push(err28);
    }
    errors++;
  }
  validate21.errors = vErrors;
  return errors === 0;
}
validate21.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.units === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "units" }, message: "must have required property 'units'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.position_mode === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "position_mode" }, message: "must have required property 'position_mode'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.placement_count === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "placement_count" }, message: "must have required property 'placement_count'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.placements === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "placements" }, message: "must have required property 'placements'" };
      if (vErrors === null) {
        vErrors = [err6];
      } else {
        vErrors.push(err6);
      }
      errors++;
    }
    if (data.schema !== void 0) {
      let data0 = data.schema;
      if (typeof data0 !== "string") {
        const err7 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      if ("altium_cruncher.pnp.a0" !== data0) {
        const err8 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.pnp.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
    if (data.source !== void 0) {
      let data1 = data.source;
      if (data1 && typeof data1 == "object" && !Array.isArray(data1)) {
        if (data1.path === void 0) {
          const err9 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/Source/required", keyword: "required", params: { missingProperty: "path" }, message: "must have required property 'path'" };
          if (vErrors === null) {
            vErrors = [err9];
          } else {
            vErrors.push(err9);
          }
          errors++;
        }
        if (data1.name === void 0) {
          const err10 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/Source/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
          if (vErrors === null) {
            vErrors = [err10];
          } else {
            vErrors.push(err10);
          }
          errors++;
        }
        if (data1.stem === void 0) {
          const err11 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/Source/required", keyword: "required", params: { missingProperty: "stem" }, message: "must have required property 'stem'" };
          if (vErrors === null) {
            vErrors = [err11];
          } else {
            vErrors.push(err11);
          }
          errors++;
        }
        if (data1.path !== void 0) {
          if (typeof data1.path !== "string") {
            const err12 = { instancePath: instancePath + "/source/path", schemaPath: "#/$defs/Source/properties/path/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err12];
            } else {
              vErrors.push(err12);
            }
            errors++;
          }
        }
        if (data1.name !== void 0) {
          if (typeof data1.name !== "string") {
            const err13 = { instancePath: instancePath + "/source/name", schemaPath: "#/$defs/Source/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err13];
            } else {
              vErrors.push(err13);
            }
            errors++;
          }
        }
        if (data1.stem !== void 0) {
          if (typeof data1.stem !== "string") {
            const err14 = { instancePath: instancePath + "/source/stem", schemaPath: "#/$defs/Source/properties/stem/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err14];
            } else {
              vErrors.push(err14);
            }
            errors++;
          }
        }
        for (const key0 in data1) {
          if (key0 !== "path" && key0 !== "name" && key0 !== "stem") {
            const err15 = { instancePath: instancePath + "/source/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/Source/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err15];
            } else {
              vErrors.push(err15);
            }
            errors++;
          }
        }
      } else {
        const err16 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/Source/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
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
        const err17 = { instancePath: instancePath + "/variant", schemaPath: "#/properties/variant/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      var _valid0 = _errs18 === errors;
      valid4 = valid4 || _valid0;
      const _errs20 = errors;
      if (data6 !== null) {
        const err18 = { instancePath: instancePath + "/variant", schemaPath: "#/properties/variant/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
      var _valid0 = _errs20 === errors;
      valid4 = valid4 || _valid0;
      if (!valid4) {
        const err19 = { instancePath: instancePath + "/variant", schemaPath: "#/properties/variant/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
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
    if (data.units !== void 0) {
      let data7 = data.units;
      const _errs23 = errors;
      let valid5 = false;
      const _errs24 = errors;
      if (typeof data7 !== "string") {
        const err20 = { instancePath: instancePath + "/units", schemaPath: "#/properties/units/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      if ("mm" !== data7) {
        const err21 = { instancePath: instancePath + "/units", schemaPath: "#/properties/units/anyOf/0/const", keyword: "const", params: { allowedValue: "mm" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      var _valid1 = _errs24 === errors;
      valid5 = valid5 || _valid1;
      const _errs26 = errors;
      if (typeof data7 !== "string") {
        const err22 = { instancePath: instancePath + "/units", schemaPath: "#/properties/units/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
      if ("mils" !== data7) {
        const err23 = { instancePath: instancePath + "/units", schemaPath: "#/properties/units/anyOf/1/const", keyword: "const", params: { allowedValue: "mils" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      var _valid1 = _errs26 === errors;
      valid5 = valid5 || _valid1;
      if (!valid5) {
        const err24 = { instancePath: instancePath + "/units", schemaPath: "#/properties/units/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      } else {
        errors = _errs23;
        if (vErrors !== null) {
          if (_errs23) {
            vErrors.length = _errs23;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.position_mode !== void 0) {
      let data8 = data.position_mode;
      const _errs29 = errors;
      let valid6 = false;
      const _errs30 = errors;
      if (typeof data8 !== "string") {
        const err25 = { instancePath: instancePath + "/position_mode", schemaPath: "#/properties/position_mode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
      if ("altium-pick-place" !== data8) {
        const err26 = { instancePath: instancePath + "/position_mode", schemaPath: "#/properties/position_mode/anyOf/0/const", keyword: "const", params: { allowedValue: "altium-pick-place" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
      var _valid2 = _errs30 === errors;
      valid6 = valid6 || _valid2;
      const _errs32 = errors;
      if (typeof data8 !== "string") {
        const err27 = { instancePath: instancePath + "/position_mode", schemaPath: "#/properties/position_mode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
      if ("component-origin" !== data8) {
        const err28 = { instancePath: instancePath + "/position_mode", schemaPath: "#/properties/position_mode/anyOf/1/const", keyword: "const", params: { allowedValue: "component-origin" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
      var _valid2 = _errs32 === errors;
      valid6 = valid6 || _valid2;
      if (!valid6) {
        const err29 = { instancePath: instancePath + "/position_mode", schemaPath: "#/properties/position_mode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      } else {
        errors = _errs29;
        if (vErrors !== null) {
          if (_errs29) {
            vErrors.length = _errs29;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.placement_count !== void 0) {
      let data9 = data.placement_count;
      if (!(typeof data9 == "number" && (!(data9 % 1) && !isNaN(data9)))) {
        const err30 = { instancePath: instancePath + "/placement_count", schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
        }
        errors++;
      }
      if (typeof data9 == "number") {
        if (data9 < 0 || isNaN(data9)) {
          const err31 = { instancePath: instancePath + "/placement_count", schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err31];
          } else {
            vErrors.push(err31);
          }
          errors++;
        }
      }
    }
    if (data.placements !== void 0) {
      let data10 = data.placements;
      if (Array.isArray(data10)) {
        const len0 = data10.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!validate21(data10[i0], { instancePath: instancePath + "/placements/" + i0, parentData: data10, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err32 = { instancePath: instancePath + "/placements", schemaPath: "#/properties/placements/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "schema" && key1 !== "source" && key1 !== "variant" && key1 !== "units" && key1 !== "position_mode" && key1 !== "placement_count" && key1 !== "placements") {
        const err33 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
    }
  } else {
    const err34 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err34];
    } else {
      vErrors.push(err34);
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
