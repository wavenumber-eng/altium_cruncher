// Generated from src/tsp/altium_cruncher/outputs/easyeda.tsp. Do not edit.
// validate.js
var validate = validate20;
var validate_default = validate20;
function validate22(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate22.evaluated;
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
  validate22.errors = vErrors;
  return errors === 0;
}
validate22.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.name !== void 0) {
      if (typeof data.name !== "string") {
        const err0 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err0];
        } else {
          vErrors.push(err0);
        }
        errors++;
      }
    }
    if (data.error !== void 0) {
      if (typeof data.error !== "string") {
        const err1 = { instancePath: instancePath + "/error", schemaPath: "#/properties/error/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
    }
    if (data.location_mils !== void 0) {
      let data2 = data.location_mils;
      if (Array.isArray(data2)) {
        const len0 = data2.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!(typeof data2[i0] == "number")) {
            const err2 = { instancePath: instancePath + "/location_mils/" + i0, schemaPath: "#/properties/location_mils/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err2];
            } else {
              vErrors.push(err2);
            }
            errors++;
          }
        }
      } else {
        const err3 = { instancePath: instancePath + "/location_mils", schemaPath: "#/properties/location_mils/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.raw_location_mils !== void 0) {
      let data4 = data.raw_location_mils;
      if (Array.isArray(data4)) {
        const len1 = data4.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (!(typeof data4[i1] == "number")) {
            const err4 = { instancePath: instancePath + "/raw_location_mils/" + i1, schemaPath: "#/properties/raw_location_mils/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err4];
            } else {
              vErrors.push(err4);
            }
            errors++;
          }
        }
      } else {
        const err5 = { instancePath: instancePath + "/raw_location_mils", schemaPath: "#/properties/raw_location_mils/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.centered_fallback !== void 0) {
      if (typeof data.centered_fallback !== "boolean") {
        const err6 = { instancePath: instancePath + "/centered_fallback", schemaPath: "#/properties/centered_fallback/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.rotation_degrees !== void 0) {
      let data7 = data.rotation_degrees;
      if (Array.isArray(data7)) {
        const len2 = data7.length;
        for (let i2 = 0; i2 < len2; i2++) {
          if (!(typeof data7[i2] == "number")) {
            const err7 = { instancePath: instancePath + "/rotation_degrees/" + i2, schemaPath: "#/properties/rotation_degrees/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err7];
            } else {
              vErrors.push(err7);
            }
            errors++;
          }
        }
      } else {
        const err8 = { instancePath: instancePath + "/rotation_degrees", schemaPath: "#/properties/rotation_degrees/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
    if (data.standoff_mils !== void 0) {
      if (!(typeof data.standoff_mils == "number")) {
        const err9 = { instancePath: instancePath + "/standoff_mils", schemaPath: "#/properties/standoff_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    if (data.identifier !== void 0) {
      if (typeof data.identifier !== "string") {
        const err10 = { instancePath: instancePath + "/identifier", schemaPath: "#/properties/identifier/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
    }
    if (data.placement_check !== void 0) {
      if (!validate22(data.placement_check, { instancePath: instancePath + "/placement_check", parentData: data, parentDataProperty: "placement_check", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate22.errors : vErrors.concat(validate22.errors);
        errors = vErrors.length;
      }
    }
    for (const key0 in data) {
      if (key0 !== "name" && key0 !== "error" && key0 !== "location_mils" && key0 !== "raw_location_mils" && key0 !== "centered_fallback" && key0 !== "rotation_degrees" && key0 !== "standoff_mils" && key0 !== "identifier" && key0 !== "placement_check") {
        const err11 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
    }
  } else {
    const err12 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err12];
    } else {
      vErrors.push(err12);
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
    if (data.lcsc_id === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "lcsc_id" }, message: "must have required property 'lcsc_id'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.footprint_name === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "footprint_name" }, message: "must have required property 'footprint_name'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.source_pad_count === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "source_pad_count" }, message: "must have required property 'source_pad_count'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.generated_pad_count === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "generated_pad_count" }, message: "must have required property 'generated_pad_count'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.generated_hole_pad_count === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "generated_hole_pad_count" }, message: "must have required property 'generated_hole_pad_count'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.custom_pad_count === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "custom_pad_count" }, message: "must have required property 'custom_pad_count'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.slotted_pad_count === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "slotted_pad_count" }, message: "must have required property 'slotted_pad_count'" };
      if (vErrors === null) {
        vErrors = [err6];
      } else {
        vErrors.push(err6);
      }
      errors++;
    }
    if (data.track_count === void 0) {
      const err7 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "track_count" }, message: "must have required property 'track_count'" };
      if (vErrors === null) {
        vErrors = [err7];
      } else {
        vErrors.push(err7);
      }
      errors++;
    }
    if (data.track_segment_count === void 0) {
      const err8 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "track_segment_count" }, message: "must have required property 'track_segment_count'" };
      if (vErrors === null) {
        vErrors = [err8];
      } else {
        vErrors.push(err8);
      }
      errors++;
    }
    if (data.circle_count === void 0) {
      const err9 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "circle_count" }, message: "must have required property 'circle_count'" };
      if (vErrors === null) {
        vErrors = [err9];
      } else {
        vErrors.push(err9);
      }
      errors++;
    }
    if (data.arc_count === void 0) {
      const err10 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "arc_count" }, message: "must have required property 'arc_count'" };
      if (vErrors === null) {
        vErrors = [err10];
      } else {
        vErrors.push(err10);
      }
      errors++;
    }
    if (data.rectangle_count === void 0) {
      const err11 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "rectangle_count" }, message: "must have required property 'rectangle_count'" };
      if (vErrors === null) {
        vErrors = [err11];
      } else {
        vErrors.push(err11);
      }
      errors++;
    }
    if (data.region_count === void 0) {
      const err12 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "region_count" }, message: "must have required property 'region_count'" };
      if (vErrors === null) {
        vErrors = [err12];
      } else {
        vErrors.push(err12);
      }
      errors++;
    }
    if (data.text_count === void 0) {
      const err13 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "text_count" }, message: "must have required property 'text_count'" };
      if (vErrors === null) {
        vErrors = [err13];
      } else {
        vErrors.push(err13);
      }
      errors++;
    }
    if (data.unsupported_count === void 0) {
      const err14 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "unsupported_count" }, message: "must have required property 'unsupported_count'" };
      if (vErrors === null) {
        vErrors = [err14];
      } else {
        vErrors.push(err14);
      }
      errors++;
    }
    if (data.unsupported_graphics === void 0) {
      const err15 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "unsupported_graphics" }, message: "must have required property 'unsupported_graphics'" };
      if (vErrors === null) {
        vErrors = [err15];
      } else {
        vErrors.push(err15);
      }
      errors++;
    }
    if (data.warnings === void 0) {
      const err16 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "warnings" }, message: "must have required property 'warnings'" };
      if (vErrors === null) {
        vErrors = [err16];
      } else {
        vErrors.push(err16);
      }
      errors++;
    }
    if (data.layers === void 0) {
      const err17 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "layers" }, message: "must have required property 'layers'" };
      if (vErrors === null) {
        vErrors = [err17];
      } else {
        vErrors.push(err17);
      }
      errors++;
    }
    if (data.policy === void 0) {
      const err18 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "policy" }, message: "must have required property 'policy'" };
      if (vErrors === null) {
        vErrors = [err18];
      } else {
        vErrors.push(err18);
      }
      errors++;
    }
    if (data.transform === void 0) {
      const err19 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "transform" }, message: "must have required property 'transform'" };
      if (vErrors === null) {
        vErrors = [err19];
      } else {
        vErrors.push(err19);
      }
      errors++;
    }
    if (data.model_3d_attached === void 0) {
      const err20 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "model_3d_attached" }, message: "must have required property 'model_3d_attached'" };
      if (vErrors === null) {
        vErrors = [err20];
      } else {
        vErrors.push(err20);
      }
      errors++;
    }
    if (data.model_3d_centered_fallback === void 0) {
      const err21 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "model_3d_centered_fallback" }, message: "must have required property 'model_3d_centered_fallback'" };
      if (vErrors === null) {
        vErrors = [err21];
      } else {
        vErrors.push(err21);
      }
      errors++;
    }
    if (data.model_3d_placement_verdict === void 0) {
      const err22 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "model_3d_placement_verdict" }, message: "must have required property 'model_3d_placement_verdict'" };
      if (vErrors === null) {
        vErrors = [err22];
      } else {
        vErrors.push(err22);
      }
      errors++;
    }
    if (data.model_3d === void 0) {
      const err23 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "model_3d" }, message: "must have required property 'model_3d'" };
      if (vErrors === null) {
        vErrors = [err23];
      } else {
        vErrors.push(err23);
      }
      errors++;
    }
    if (data.lcsc_id !== void 0) {
      if (typeof data.lcsc_id !== "string") {
        const err24 = { instancePath: instancePath + "/lcsc_id", schemaPath: "#/properties/lcsc_id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
    }
    if (data.footprint_name !== void 0) {
      if (typeof data.footprint_name !== "string") {
        const err25 = { instancePath: instancePath + "/footprint_name", schemaPath: "#/properties/footprint_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
    }
    if (data.source_pad_count !== void 0) {
      let data2 = data.source_pad_count;
      if (!(typeof data2 == "number" && (!(data2 % 1) && !isNaN(data2)))) {
        const err26 = { instancePath: instancePath + "/source_pad_count", schemaPath: "#/properties/source_pad_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
    }
    if (data.generated_pad_count !== void 0) {
      let data3 = data.generated_pad_count;
      if (!(typeof data3 == "number" && (!(data3 % 1) && !isNaN(data3)))) {
        const err27 = { instancePath: instancePath + "/generated_pad_count", schemaPath: "#/properties/generated_pad_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
    }
    if (data.generated_hole_pad_count !== void 0) {
      let data4 = data.generated_hole_pad_count;
      if (!(typeof data4 == "number" && (!(data4 % 1) && !isNaN(data4)))) {
        const err28 = { instancePath: instancePath + "/generated_hole_pad_count", schemaPath: "#/properties/generated_hole_pad_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
    }
    if (data.custom_pad_count !== void 0) {
      let data5 = data.custom_pad_count;
      if (!(typeof data5 == "number" && (!(data5 % 1) && !isNaN(data5)))) {
        const err29 = { instancePath: instancePath + "/custom_pad_count", schemaPath: "#/properties/custom_pad_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      }
    }
    if (data.slotted_pad_count !== void 0) {
      let data6 = data.slotted_pad_count;
      if (!(typeof data6 == "number" && (!(data6 % 1) && !isNaN(data6)))) {
        const err30 = { instancePath: instancePath + "/slotted_pad_count", schemaPath: "#/properties/slotted_pad_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
        }
        errors++;
      }
    }
    if (data.track_count !== void 0) {
      let data7 = data.track_count;
      if (!(typeof data7 == "number" && (!(data7 % 1) && !isNaN(data7)))) {
        const err31 = { instancePath: instancePath + "/track_count", schemaPath: "#/properties/track_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      }
    }
    if (data.track_segment_count !== void 0) {
      let data8 = data.track_segment_count;
      if (!(typeof data8 == "number" && (!(data8 % 1) && !isNaN(data8)))) {
        const err32 = { instancePath: instancePath + "/track_segment_count", schemaPath: "#/properties/track_segment_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
        }
        errors++;
      }
    }
    if (data.circle_count !== void 0) {
      let data9 = data.circle_count;
      if (!(typeof data9 == "number" && (!(data9 % 1) && !isNaN(data9)))) {
        const err33 = { instancePath: instancePath + "/circle_count", schemaPath: "#/properties/circle_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
    }
    if (data.arc_count !== void 0) {
      let data10 = data.arc_count;
      if (!(typeof data10 == "number" && (!(data10 % 1) && !isNaN(data10)))) {
        const err34 = { instancePath: instancePath + "/arc_count", schemaPath: "#/properties/arc_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
        }
        errors++;
      }
    }
    if (data.rectangle_count !== void 0) {
      let data11 = data.rectangle_count;
      if (!(typeof data11 == "number" && (!(data11 % 1) && !isNaN(data11)))) {
        const err35 = { instancePath: instancePath + "/rectangle_count", schemaPath: "#/properties/rectangle_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err35];
        } else {
          vErrors.push(err35);
        }
        errors++;
      }
    }
    if (data.region_count !== void 0) {
      let data12 = data.region_count;
      if (!(typeof data12 == "number" && (!(data12 % 1) && !isNaN(data12)))) {
        const err36 = { instancePath: instancePath + "/region_count", schemaPath: "#/properties/region_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err36];
        } else {
          vErrors.push(err36);
        }
        errors++;
      }
    }
    if (data.text_count !== void 0) {
      let data13 = data.text_count;
      if (!(typeof data13 == "number" && (!(data13 % 1) && !isNaN(data13)))) {
        const err37 = { instancePath: instancePath + "/text_count", schemaPath: "#/properties/text_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err37];
        } else {
          vErrors.push(err37);
        }
        errors++;
      }
    }
    if (data.unsupported_count !== void 0) {
      let data14 = data.unsupported_count;
      if (!(typeof data14 == "number" && (!(data14 % 1) && !isNaN(data14)))) {
        const err38 = { instancePath: instancePath + "/unsupported_count", schemaPath: "#/properties/unsupported_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err38];
        } else {
          vErrors.push(err38);
        }
        errors++;
      }
    }
    if (data.unsupported_graphics !== void 0) {
      let data15 = data.unsupported_graphics;
      if (Array.isArray(data15)) {
        const len0 = data15.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (typeof data15[i0] !== "string") {
            const err39 = { instancePath: instancePath + "/unsupported_graphics/" + i0, schemaPath: "#/properties/unsupported_graphics/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err39];
            } else {
              vErrors.push(err39);
            }
            errors++;
          }
        }
      } else {
        const err40 = { instancePath: instancePath + "/unsupported_graphics", schemaPath: "#/properties/unsupported_graphics/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err40];
        } else {
          vErrors.push(err40);
        }
        errors++;
      }
    }
    if (data.warnings !== void 0) {
      let data17 = data.warnings;
      if (Array.isArray(data17)) {
        const len1 = data17.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (typeof data17[i1] !== "string") {
            const err41 = { instancePath: instancePath + "/warnings/" + i1, schemaPath: "#/properties/warnings/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err41];
            } else {
              vErrors.push(err41);
            }
            errors++;
          }
        }
      } else {
        const err42 = { instancePath: instancePath + "/warnings", schemaPath: "#/properties/warnings/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err42];
        } else {
          vErrors.push(err42);
        }
        errors++;
      }
    }
    if (data.layers !== void 0) {
      let data19 = data.layers;
      if (data19 && typeof data19 == "object" && !Array.isArray(data19)) {
        for (const key0 in data19) {
          let data20 = data19[key0];
          if (!(typeof data20 == "number" && (!(data20 % 1) && !isNaN(data20)))) {
            const err43 = { instancePath: instancePath + "/layers/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/RecordInteger/unevaluatedProperties/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
            if (vErrors === null) {
              vErrors = [err43];
            } else {
              vErrors.push(err43);
            }
            errors++;
          }
        }
      } else {
        const err44 = { instancePath: instancePath + "/layers", schemaPath: "#/$defs/RecordInteger/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err44];
        } else {
          vErrors.push(err44);
        }
        errors++;
      }
    }
    if (data.policy !== void 0) {
      let data21 = data.policy;
      if (data21 && typeof data21 == "object" && !Array.isArray(data21)) {
        if (data21.mils_per_easyeda_unit !== void 0) {
          if (!(typeof data21.mils_per_easyeda_unit == "number")) {
            const err45 = { instancePath: instancePath + "/policy/mils_per_easyeda_unit", schemaPath: "#/$defs/FootprintPolicy/properties/mils_per_easyeda_unit/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err45];
            } else {
              vErrors.push(err45);
            }
            errors++;
          }
        }
        if (data21.invert_y !== void 0) {
          if (typeof data21.invert_y !== "boolean") {
            const err46 = { instancePath: instancePath + "/policy/invert_y", schemaPath: "#/$defs/FootprintPolicy/properties/invert_y/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err46];
            } else {
              vErrors.push(err46);
            }
            errors++;
          }
        }
        if (data21.include_source_graphics !== void 0) {
          if (typeof data21.include_source_graphics !== "boolean") {
            const err47 = { instancePath: instancePath + "/policy/include_source_graphics", schemaPath: "#/$defs/FootprintPolicy/properties/include_source_graphics/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err47];
            } else {
              vErrors.push(err47);
            }
            errors++;
          }
        }
        if (data21.include_source_text !== void 0) {
          if (typeof data21.include_source_text !== "boolean") {
            const err48 = { instancePath: instancePath + "/policy/include_source_text", schemaPath: "#/$defs/FootprintPolicy/properties/include_source_text/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err48];
            } else {
              vErrors.push(err48);
            }
            errors++;
          }
        }
        if (data21.include_non_pad_holes !== void 0) {
          if (typeof data21.include_non_pad_holes !== "boolean") {
            const err49 = { instancePath: instancePath + "/policy/include_non_pad_holes", schemaPath: "#/$defs/FootprintPolicy/properties/include_non_pad_holes/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err49];
            } else {
              vErrors.push(err49);
            }
            errors++;
          }
        }
        if (data21.default_graphic_width_mils !== void 0) {
          if (!(typeof data21.default_graphic_width_mils == "number")) {
            const err50 = { instancePath: instancePath + "/policy/default_graphic_width_mils", schemaPath: "#/$defs/FootprintPolicy/properties/default_graphic_width_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err50];
            } else {
              vErrors.push(err50);
            }
            errors++;
          }
        }
        if (data21.curve_approximation_segments !== void 0) {
          let data28 = data21.curve_approximation_segments;
          if (!(typeof data28 == "number" && (!(data28 % 1) && !isNaN(data28)))) {
            const err51 = { instancePath: instancePath + "/policy/curve_approximation_segments", schemaPath: "#/$defs/FootprintPolicy/properties/curve_approximation_segments/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
            if (vErrors === null) {
              vErrors = [err51];
            } else {
              vErrors.push(err51);
            }
            errors++;
          }
        }
        if (data21.arc_approximation_max_degrees !== void 0) {
          if (!(typeof data21.arc_approximation_max_degrees == "number")) {
            const err52 = { instancePath: instancePath + "/policy/arc_approximation_max_degrees", schemaPath: "#/$defs/FootprintPolicy/properties/arc_approximation_max_degrees/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err52];
            } else {
              vErrors.push(err52);
            }
            errors++;
          }
        }
        for (const key1 in data21) {
          if (key1 !== "mils_per_easyeda_unit" && key1 !== "invert_y" && key1 !== "include_source_graphics" && key1 !== "include_source_text" && key1 !== "include_non_pad_holes" && key1 !== "default_graphic_width_mils" && key1 !== "curve_approximation_segments" && key1 !== "arc_approximation_max_degrees") {
            const err53 = { instancePath: instancePath + "/policy/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/FootprintPolicy/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err53];
            } else {
              vErrors.push(err53);
            }
            errors++;
          }
        }
      } else {
        const err54 = { instancePath: instancePath + "/policy", schemaPath: "#/$defs/FootprintPolicy/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err54];
        } else {
          vErrors.push(err54);
        }
        errors++;
      }
    }
    if (data.transform !== void 0) {
      let data31 = data.transform;
      if (data31 && typeof data31 == "object" && !Array.isArray(data31)) {
        if (data31.anchor_x !== void 0) {
          if (!(typeof data31.anchor_x == "number")) {
            const err55 = { instancePath: instancePath + "/transform/anchor_x", schemaPath: "#/$defs/FootprintTransform/properties/anchor_x/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err55];
            } else {
              vErrors.push(err55);
            }
            errors++;
          }
        }
        if (data31.anchor_y !== void 0) {
          if (!(typeof data31.anchor_y == "number")) {
            const err56 = { instancePath: instancePath + "/transform/anchor_y", schemaPath: "#/$defs/FootprintTransform/properties/anchor_y/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err56];
            } else {
              vErrors.push(err56);
            }
            errors++;
          }
        }
        if (data31.mils_per_easyeda_unit !== void 0) {
          if (!(typeof data31.mils_per_easyeda_unit == "number")) {
            const err57 = { instancePath: instancePath + "/transform/mils_per_easyeda_unit", schemaPath: "#/$defs/FootprintTransform/properties/mils_per_easyeda_unit/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err57];
            } else {
              vErrors.push(err57);
            }
            errors++;
          }
        }
        if (data31.invert_y !== void 0) {
          if (typeof data31.invert_y !== "boolean") {
            const err58 = { instancePath: instancePath + "/transform/invert_y", schemaPath: "#/$defs/FootprintTransform/properties/invert_y/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err58];
            } else {
              vErrors.push(err58);
            }
            errors++;
          }
        }
        for (const key2 in data31) {
          if (key2 !== "anchor_x" && key2 !== "anchor_y" && key2 !== "mils_per_easyeda_unit" && key2 !== "invert_y") {
            const err59 = { instancePath: instancePath + "/transform/" + key2.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/FootprintTransform/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err59];
            } else {
              vErrors.push(err59);
            }
            errors++;
          }
        }
      } else {
        const err60 = { instancePath: instancePath + "/transform", schemaPath: "#/$defs/FootprintTransform/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err60];
        } else {
          vErrors.push(err60);
        }
        errors++;
      }
    }
    if (data.model_3d_attached !== void 0) {
      if (typeof data.model_3d_attached !== "boolean") {
        const err61 = { instancePath: instancePath + "/model_3d_attached", schemaPath: "#/properties/model_3d_attached/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err61];
        } else {
          vErrors.push(err61);
        }
        errors++;
      }
    }
    if (data.model_3d_centered_fallback !== void 0) {
      if (typeof data.model_3d_centered_fallback !== "boolean") {
        const err62 = { instancePath: instancePath + "/model_3d_centered_fallback", schemaPath: "#/properties/model_3d_centered_fallback/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err62];
        } else {
          vErrors.push(err62);
        }
        errors++;
      }
    }
    if (data.model_3d_placement_verdict !== void 0) {
      if (typeof data.model_3d_placement_verdict !== "string") {
        const err63 = { instancePath: instancePath + "/model_3d_placement_verdict", schemaPath: "#/properties/model_3d_placement_verdict/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err63];
        } else {
          vErrors.push(err63);
        }
        errors++;
      }
    }
    if (data.model_3d !== void 0) {
      if (!validate21(data.model_3d, { instancePath: instancePath + "/model_3d", parentData: data, parentDataProperty: "model_3d", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
        errors = vErrors.length;
      }
    }
    for (const key3 in data) {
      if (key3 !== "lcsc_id" && key3 !== "footprint_name" && key3 !== "source_pad_count" && key3 !== "generated_pad_count" && key3 !== "generated_hole_pad_count" && key3 !== "custom_pad_count" && key3 !== "slotted_pad_count" && key3 !== "track_count" && key3 !== "track_segment_count" && key3 !== "circle_count" && key3 !== "arc_count" && key3 !== "rectangle_count" && key3 !== "region_count" && key3 !== "text_count" && key3 !== "unsupported_count" && key3 !== "unsupported_graphics" && key3 !== "warnings" && key3 !== "layers" && key3 !== "policy" && key3 !== "transform" && key3 !== "model_3d_attached" && key3 !== "model_3d_centered_fallback" && key3 !== "model_3d_placement_verdict" && key3 !== "model_3d") {
        const err64 = { instancePath: instancePath + "/" + key3.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err64];
        } else {
          vErrors.push(err64);
        }
        errors++;
      }
    }
  } else {
    const err65 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err65];
    } else {
      vErrors.push(err65);
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
