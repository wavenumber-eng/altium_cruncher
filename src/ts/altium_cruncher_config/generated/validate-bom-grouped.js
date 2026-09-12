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
    if (data.item === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "item" }, message: "must have required property 'item'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.quantity === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "quantity" }, message: "must have required property 'quantity'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.designators === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "designators" }, message: "must have required property 'designators'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.dnp === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "dnp" }, message: "must have required property 'dnp'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.fields === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "fields" }, message: "must have required property 'fields'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.item !== void 0) {
      let data0 = data.item;
      if (!(typeof data0 == "number" && (!(data0 % 1) && !isNaN(data0)))) {
        const err5 = { instancePath: instancePath + "/item", schemaPath: "#/properties/item/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.quantity !== void 0) {
      let data1 = data.quantity;
      if (!(typeof data1 == "number" && (!(data1 % 1) && !isNaN(data1)))) {
        const err6 = { instancePath: instancePath + "/quantity", schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      if (typeof data1 == "number") {
        if (data1 < 0 || isNaN(data1)) {
          const err7 = { instancePath: instancePath + "/quantity", schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err7];
          } else {
            vErrors.push(err7);
          }
          errors++;
        }
      }
    }
    if (data.designators !== void 0) {
      let data2 = data.designators;
      if (Array.isArray(data2)) {
        const len0 = data2.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (typeof data2[i0] !== "string") {
            const err8 = { instancePath: instancePath + "/designators/" + i0, schemaPath: "#/properties/designators/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err8];
            } else {
              vErrors.push(err8);
            }
            errors++;
          }
        }
      } else {
        const err9 = { instancePath: instancePath + "/designators", schemaPath: "#/properties/designators/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    if (data.dnp !== void 0) {
      if (typeof data.dnp !== "boolean") {
        const err10 = { instancePath: instancePath + "/dnp", schemaPath: "#/properties/dnp/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
    }
    if (data.fields !== void 0) {
      let data5 = data.fields;
      if (data5 && typeof data5 == "object" && !Array.isArray(data5)) {
        for (const key0 in data5) {
          if (typeof data5[key0] !== "string") {
            const err11 = { instancePath: instancePath + "/fields/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/RecordString/unevaluatedProperties/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err11];
            } else {
              vErrors.push(err11);
            }
            errors++;
          }
        }
      } else {
        const err12 = { instancePath: instancePath + "/fields", schemaPath: "#/$defs/RecordString/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "item" && key1 !== "quantity" && key1 !== "designators" && key1 !== "dnp" && key1 !== "fields") {
        const err13 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
  } else {
    const err14 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err14];
    } else {
      vErrors.push(err14);
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
    if (data.line_count === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "line_count" }, message: "must have required property 'line_count'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.component_count === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "component_count" }, message: "must have required property 'component_count'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.dnp_line_count === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "dnp_line_count" }, message: "must have required property 'dnp_line_count'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.lines === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "lines" }, message: "must have required property 'lines'" };
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
      if ("altium_cruncher.bom.grouped.a0" !== data0) {
        const err8 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.bom.grouped.a0" }, message: "must be equal to constant" };
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
    if (data.line_count !== void 0) {
      let data7 = data.line_count;
      if (!(typeof data7 == "number" && (!(data7 % 1) && !isNaN(data7)))) {
        const err20 = { instancePath: instancePath + "/line_count", schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      if (typeof data7 == "number") {
        if (data7 < 0 || isNaN(data7)) {
          const err21 = { instancePath: instancePath + "/line_count", schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err21];
          } else {
            vErrors.push(err21);
          }
          errors++;
        }
      }
    }
    if (data.component_count !== void 0) {
      let data8 = data.component_count;
      if (!(typeof data8 == "number" && (!(data8 % 1) && !isNaN(data8)))) {
        const err22 = { instancePath: instancePath + "/component_count", schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
      if (typeof data8 == "number") {
        if (data8 < 0 || isNaN(data8)) {
          const err23 = { instancePath: instancePath + "/component_count", schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err23];
          } else {
            vErrors.push(err23);
          }
          errors++;
        }
      }
    }
    if (data.dnp_line_count !== void 0) {
      let data9 = data.dnp_line_count;
      if (!(typeof data9 == "number" && (!(data9 % 1) && !isNaN(data9)))) {
        const err24 = { instancePath: instancePath + "/dnp_line_count", schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      if (typeof data9 == "number") {
        if (data9 < 0 || isNaN(data9)) {
          const err25 = { instancePath: instancePath + "/dnp_line_count", schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err25];
          } else {
            vErrors.push(err25);
          }
          errors++;
        }
      }
    }
    if (data.lines !== void 0) {
      let data10 = data.lines;
      if (Array.isArray(data10)) {
        const len0 = data10.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!validate21(data10[i0], { instancePath: instancePath + "/lines/" + i0, parentData: data10, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err26 = { instancePath: instancePath + "/lines", schemaPath: "#/properties/lines/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "schema" && key1 !== "source" && key1 !== "variant" && key1 !== "line_count" && key1 !== "component_count" && key1 !== "dnp_line_count" && key1 !== "lines") {
        const err27 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
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
  validate20.errors = vErrors;
  return errors === 0;
}
validate20.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
export {
  validate_default as default,
  validate
};
