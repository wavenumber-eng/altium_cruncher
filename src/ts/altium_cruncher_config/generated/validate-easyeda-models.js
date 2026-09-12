// Generated from src/tsp/altium_cruncher/outputs/easyeda.tsp. Do not edit.
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
    if (data.uuid === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "uuid" }, message: "must have required property 'uuid'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.title === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "title" }, message: "must have required property 'title'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.origin === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "origin" }, message: "must have required property 'origin'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.z === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "z" }, message: "must have required property 'z'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.rotation === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "rotation" }, message: "must have required property 'rotation'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.files === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "files" }, message: "must have required property 'files'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.errors === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "errors" }, message: "must have required property 'errors'" };
      if (vErrors === null) {
        vErrors = [err6];
      } else {
        vErrors.push(err6);
      }
      errors++;
    }
    if (data.placement_status === void 0) {
      const err7 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "placement_status" }, message: "must have required property 'placement_status'" };
      if (vErrors === null) {
        vErrors = [err7];
      } else {
        vErrors.push(err7);
      }
      errors++;
    }
    if (data.uuid !== void 0) {
      if (typeof data.uuid !== "string") {
        const err8 = { instancePath: instancePath + "/uuid", schemaPath: "#/properties/uuid/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
    if (data.title !== void 0) {
      if (typeof data.title !== "string") {
        const err9 = { instancePath: instancePath + "/title", schemaPath: "#/properties/title/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    if (data.origin !== void 0) {
      if (typeof data.origin !== "string") {
        const err10 = { instancePath: instancePath + "/origin", schemaPath: "#/properties/origin/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
    }
    if (data.z !== void 0) {
      if (typeof data.z !== "string") {
        const err11 = { instancePath: instancePath + "/z", schemaPath: "#/properties/z/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
    }
    if (data.rotation !== void 0) {
      if (typeof data.rotation !== "string") {
        const err12 = { instancePath: instancePath + "/rotation", schemaPath: "#/properties/rotation/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
    }
    if (data.files !== void 0) {
      let data5 = data.files;
      if (data5 && typeof data5 == "object" && !Array.isArray(data5)) {
        for (const key0 in data5) {
          if (typeof data5[key0] !== "string") {
            const err13 = { instancePath: instancePath + "/files/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/RecordString/unevaluatedProperties/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err13];
            } else {
              vErrors.push(err13);
            }
            errors++;
          }
        }
      } else {
        const err14 = { instancePath: instancePath + "/files", schemaPath: "#/$defs/RecordString/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
    }
    if (data.errors !== void 0) {
      let data7 = data.errors;
      if (data7 && typeof data7 == "object" && !Array.isArray(data7)) {
        for (const key1 in data7) {
          if (typeof data7[key1] !== "string") {
            const err15 = { instancePath: instancePath + "/errors/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/RecordString/unevaluatedProperties/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err15];
            } else {
              vErrors.push(err15);
            }
            errors++;
          }
        }
      } else {
        const err16 = { instancePath: instancePath + "/errors", schemaPath: "#/$defs/RecordString/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
    }
    if (data.placement_status !== void 0) {
      if (typeof data.placement_status !== "string") {
        const err17 = { instancePath: instancePath + "/placement_status", schemaPath: "#/properties/placement_status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
    }
    for (const key2 in data) {
      if (key2 !== "uuid" && key2 !== "title" && key2 !== "origin" && key2 !== "z" && key2 !== "rotation" && key2 !== "files" && key2 !== "errors" && key2 !== "placement_status") {
        const err18 = { instancePath: instancePath + "/" + key2.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
    }
  } else {
    const err19 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err19];
    } else {
      vErrors.push(err19);
    }
    errors++;
  }
  validate21.errors = vErrors;
  return errors === 0;
}
validate21.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.verdict !== void 0) {
      let data0 = data.verdict;
      const _errs2 = errors;
      let valid1 = false;
      const _errs3 = errors;
      if (typeof data0 !== "string") {
        const err0 = { instancePath: instancePath + "/verdict", schemaPath: "#/properties/verdict/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err0];
        } else {
          vErrors.push(err0);
        }
        errors++;
      }
      if ("ok" !== data0) {
        const err1 = { instancePath: instancePath + "/verdict", schemaPath: "#/properties/verdict/anyOf/0/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      var _valid0 = _errs3 === errors;
      valid1 = valid1 || _valid0;
      const _errs5 = errors;
      if (typeof data0 !== "string") {
        const err2 = { instancePath: instancePath + "/verdict", schemaPath: "#/properties/verdict/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      if ("needs_checking" !== data0) {
        const err3 = { instancePath: instancePath + "/verdict", schemaPath: "#/properties/verdict/anyOf/1/const", keyword: "const", params: { allowedValue: "needs_checking" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      var _valid0 = _errs5 === errors;
      valid1 = valid1 || _valid0;
      if (!valid1) {
        const err4 = { instancePath: instancePath + "/verdict", schemaPath: "#/properties/verdict/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      } else {
        errors = _errs2;
        if (vErrors !== null) {
          if (_errs2) {
            vErrors.length = _errs2;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.checked !== void 0) {
      if (typeof data.checked !== "boolean") {
        const err5 = { instancePath: instancePath + "/checked", schemaPath: "#/properties/checked/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.reason !== void 0) {
      if (typeof data.reason !== "string") {
        const err6 = { instancePath: instancePath + "/reason", schemaPath: "#/properties/reason/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.center_distance_mils !== void 0) {
      if (!(typeof data.center_distance_mils == "number")) {
        const err7 = { instancePath: instancePath + "/center_distance_mils", schemaPath: "#/properties/center_distance_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.distance_ratio !== void 0) {
      if (!(typeof data.distance_ratio == "number")) {
        const err8 = { instancePath: instancePath + "/distance_ratio", schemaPath: "#/properties/distance_ratio/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
    if (data.model_bounds_mils !== void 0) {
      let data5 = data.model_bounds_mils;
      if (Array.isArray(data5)) {
        if (data5.length > 4) {
          const err9 = { instancePath: instancePath + "/model_bounds_mils", schemaPath: "#/$defs/BoundsArray/maxItems", keyword: "maxItems", params: { limit: 4 }, message: "must NOT have more than 4 items" };
          if (vErrors === null) {
            vErrors = [err9];
          } else {
            vErrors.push(err9);
          }
          errors++;
        }
        if (data5.length < 4) {
          const err10 = { instancePath: instancePath + "/model_bounds_mils", schemaPath: "#/$defs/BoundsArray/minItems", keyword: "minItems", params: { limit: 4 }, message: "must NOT have fewer than 4 items" };
          if (vErrors === null) {
            vErrors = [err10];
          } else {
            vErrors.push(err10);
          }
          errors++;
        }
        const len0 = data5.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!(typeof data5[i0] == "number")) {
            const err11 = { instancePath: instancePath + "/model_bounds_mils/" + i0, schemaPath: "#/$defs/BoundsArray/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err11];
            } else {
              vErrors.push(err11);
            }
            errors++;
          }
        }
      } else {
        const err12 = { instancePath: instancePath + "/model_bounds_mils", schemaPath: "#/$defs/BoundsArray/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
    }
    if (data.pad_bounds_mils !== void 0) {
      let data7 = data.pad_bounds_mils;
      if (Array.isArray(data7)) {
        if (data7.length > 4) {
          const err13 = { instancePath: instancePath + "/pad_bounds_mils", schemaPath: "#/$defs/BoundsArray/maxItems", keyword: "maxItems", params: { limit: 4 }, message: "must NOT have more than 4 items" };
          if (vErrors === null) {
            vErrors = [err13];
          } else {
            vErrors.push(err13);
          }
          errors++;
        }
        if (data7.length < 4) {
          const err14 = { instancePath: instancePath + "/pad_bounds_mils", schemaPath: "#/$defs/BoundsArray/minItems", keyword: "minItems", params: { limit: 4 }, message: "must NOT have fewer than 4 items" };
          if (vErrors === null) {
            vErrors = [err14];
          } else {
            vErrors.push(err14);
          }
          errors++;
        }
        const len1 = data7.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (!(typeof data7[i1] == "number")) {
            const err15 = { instancePath: instancePath + "/pad_bounds_mils/" + i1, schemaPath: "#/$defs/BoundsArray/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err15];
            } else {
              vErrors.push(err15);
            }
            errors++;
          }
        }
      } else {
        const err16 = { instancePath: instancePath + "/pad_bounds_mils", schemaPath: "#/$defs/BoundsArray/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
    }
    for (const key0 in data) {
      if (key0 !== "verdict" && key0 !== "checked" && key0 !== "reason" && key0 !== "center_distance_mils" && key0 !== "distance_ratio" && key0 !== "model_bounds_mils" && key0 !== "pad_bounds_mils") {
        const err17 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
    }
  } else {
    const err18 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err18];
    } else {
      vErrors.push(err18);
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
    if (data.lcsc_id === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "lcsc_id" }, message: "must have required property 'lcsc_id'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.placement_implemented === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "placement_implemented" }, message: "must have required property 'placement_implemented'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.placement_note === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "placement_note" }, message: "must have required property 'placement_note'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.models === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "models" }, message: "must have required property 'models'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.schema !== void 0) {
      let data0 = data.schema;
      if (typeof data0 !== "string") {
        const err5 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      if ("altium_cruncher.easyeda.3d_models.a0" !== data0) {
        const err6 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.easyeda.3d_models.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.lcsc_id !== void 0) {
      if (typeof data.lcsc_id !== "string") {
        const err7 = { instancePath: instancePath + "/lcsc_id", schemaPath: "#/properties/lcsc_id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.placement_implemented !== void 0) {
      if (typeof data.placement_implemented !== "boolean") {
        const err8 = { instancePath: instancePath + "/placement_implemented", schemaPath: "#/properties/placement_implemented/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
    if (data.placement_note !== void 0) {
      if (typeof data.placement_note !== "string") {
        const err9 = { instancePath: instancePath + "/placement_note", schemaPath: "#/properties/placement_note/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    if (data.models !== void 0) {
      let data4 = data.models;
      if (Array.isArray(data4)) {
        const len0 = data4.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!validate21(data4[i0], { instancePath: instancePath + "/models/" + i0, parentData: data4, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err10 = { instancePath: instancePath + "/models", schemaPath: "#/properties/models/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
    }
    if (data.placement_verdict !== void 0) {
      if (typeof data.placement_verdict !== "string") {
        const err11 = { instancePath: instancePath + "/placement_verdict", schemaPath: "#/properties/placement_verdict/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
    }
    if (data.placement_check !== void 0) {
      if (!validate23(data.placement_check, { instancePath: instancePath + "/placement_check", parentData: data, parentDataProperty: "placement_check", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate23.errors : vErrors.concat(validate23.errors);
        errors = vErrors.length;
      }
    }
    for (const key0 in data) {
      if (key0 !== "schema" && key0 !== "lcsc_id" && key0 !== "placement_implemented" && key0 !== "placement_note" && key0 !== "models" && key0 !== "placement_verdict" && key0 !== "placement_check") {
        const err12 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
    }
  } else {
    const err13 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err13];
    } else {
      vErrors.push(err13);
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
