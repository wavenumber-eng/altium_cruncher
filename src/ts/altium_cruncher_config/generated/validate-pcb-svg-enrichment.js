// Generated from src/tsp/altium_cruncher/outputs/pcb-svg-enrichment.tsp. Do not edit.
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
    if (data.bounds_mode === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "bounds_mode" }, message: "must have required property 'bounds_mode'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.bounds_mils === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "bounds_mils" }, message: "must have required property 'bounds_mils'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.margin_mm === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "margin_mm" }, message: "must have required property 'margin_mm'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.altium_origin_mils === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "altium_origin_mils" }, message: "must have required property 'altium_origin_mils'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.svg_units === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "svg_units" }, message: "must have required property 'svg_units'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.geometry_transform === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "geometry_transform" }, message: "must have required property 'geometry_transform'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.metadata_coordinate_policy === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "metadata_coordinate_policy" }, message: "must have required property 'metadata_coordinate_policy'" };
      if (vErrors === null) {
        vErrors = [err6];
      } else {
        vErrors.push(err6);
      }
      errors++;
    }
    if (data.bounds_mode !== void 0) {
      let data0 = data.bounds_mode;
      const _errs2 = errors;
      let valid1 = false;
      const _errs3 = errors;
      if (typeof data0 !== "string") {
        const err7 = { instancePath: instancePath + "/bounds_mode", schemaPath: "#/properties/bounds_mode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      if ("all_geometry" !== data0) {
        const err8 = { instancePath: instancePath + "/bounds_mode", schemaPath: "#/properties/bounds_mode/anyOf/0/const", keyword: "const", params: { allowedValue: "all_geometry" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid0 = _errs3 === errors;
      valid1 = valid1 || _valid0;
      const _errs5 = errors;
      if (typeof data0 !== "string") {
        const err9 = { instancePath: instancePath + "/bounds_mode", schemaPath: "#/properties/bounds_mode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      if ("board_outline" !== data0) {
        const err10 = { instancePath: instancePath + "/bounds_mode", schemaPath: "#/properties/bounds_mode/anyOf/1/const", keyword: "const", params: { allowedValue: "board_outline" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid0 = _errs5 === errors;
      valid1 = valid1 || _valid0;
      if (!valid1) {
        const err11 = { instancePath: instancePath + "/bounds_mode", schemaPath: "#/properties/bounds_mode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
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
    if (data.bounds_mils !== void 0) {
      let data1 = data.bounds_mils;
      if (Array.isArray(data1)) {
        if (data1.length > 4) {
          const err12 = { instancePath: instancePath + "/bounds_mils", schemaPath: "#/$defs/Bounds/maxItems", keyword: "maxItems", params: { limit: 4 }, message: "must NOT have more than 4 items" };
          if (vErrors === null) {
            vErrors = [err12];
          } else {
            vErrors.push(err12);
          }
          errors++;
        }
        if (data1.length < 4) {
          const err13 = { instancePath: instancePath + "/bounds_mils", schemaPath: "#/$defs/Bounds/minItems", keyword: "minItems", params: { limit: 4 }, message: "must NOT have fewer than 4 items" };
          if (vErrors === null) {
            vErrors = [err13];
          } else {
            vErrors.push(err13);
          }
          errors++;
        }
        const len0 = data1.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!(typeof data1[i0] == "number")) {
            const err14 = { instancePath: instancePath + "/bounds_mils/" + i0, schemaPath: "#/$defs/Bounds/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err14];
            } else {
              vErrors.push(err14);
            }
            errors++;
          }
        }
      } else {
        const err15 = { instancePath: instancePath + "/bounds_mils", schemaPath: "#/$defs/Bounds/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
    }
    if (data.margin_mm !== void 0) {
      if (!(typeof data.margin_mm == "number")) {
        const err16 = { instancePath: instancePath + "/margin_mm", schemaPath: "#/properties/margin_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
    }
    if (data.altium_origin_mils !== void 0) {
      let data4 = data.altium_origin_mils;
      if (Array.isArray(data4)) {
        if (data4.length > 2) {
          const err17 = { instancePath: instancePath + "/altium_origin_mils", schemaPath: "#/$defs/Pair/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err17];
          } else {
            vErrors.push(err17);
          }
          errors++;
        }
        if (data4.length < 2) {
          const err18 = { instancePath: instancePath + "/altium_origin_mils", schemaPath: "#/$defs/Pair/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err18];
          } else {
            vErrors.push(err18);
          }
          errors++;
        }
        const len1 = data4.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (!(typeof data4[i1] == "number")) {
            const err19 = { instancePath: instancePath + "/altium_origin_mils/" + i1, schemaPath: "#/$defs/Pair/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err19];
            } else {
              vErrors.push(err19);
            }
            errors++;
          }
        }
      } else {
        const err20 = { instancePath: instancePath + "/altium_origin_mils", schemaPath: "#/$defs/Pair/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
    }
    if (data.svg_units !== void 0) {
      let data6 = data.svg_units;
      if (typeof data6 !== "string") {
        const err21 = { instancePath: instancePath + "/svg_units", schemaPath: "#/properties/svg_units/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      if ("mm" !== data6) {
        const err22 = { instancePath: instancePath + "/svg_units", schemaPath: "#/properties/svg_units/const", keyword: "const", params: { allowedValue: "mm" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
    }
    if (data.geometry_transform !== void 0) {
      let data7 = data.geometry_transform;
      if (data7 && typeof data7 == "object" && !Array.isArray(data7)) {
        if (data7.x_svg_mm === void 0) {
          const err23 = { instancePath: instancePath + "/geometry_transform", schemaPath: "#/properties/geometry_transform/required", keyword: "required", params: { missingProperty: "x_svg_mm" }, message: "must have required property 'x_svg_mm'" };
          if (vErrors === null) {
            vErrors = [err23];
          } else {
            vErrors.push(err23);
          }
          errors++;
        }
        if (data7.y_svg_mm === void 0) {
          const err24 = { instancePath: instancePath + "/geometry_transform", schemaPath: "#/properties/geometry_transform/required", keyword: "required", params: { missingProperty: "y_svg_mm" }, message: "must have required property 'y_svg_mm'" };
          if (vErrors === null) {
            vErrors = [err24];
          } else {
            vErrors.push(err24);
          }
          errors++;
        }
        if (data7.x_svg_mm !== void 0) {
          if (typeof data7.x_svg_mm !== "string") {
            const err25 = { instancePath: instancePath + "/geometry_transform/x_svg_mm", schemaPath: "#/properties/geometry_transform/properties/x_svg_mm/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err25];
            } else {
              vErrors.push(err25);
            }
            errors++;
          }
        }
        if (data7.y_svg_mm !== void 0) {
          if (typeof data7.y_svg_mm !== "string") {
            const err26 = { instancePath: instancePath + "/geometry_transform/y_svg_mm", schemaPath: "#/properties/geometry_transform/properties/y_svg_mm/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err26];
            } else {
              vErrors.push(err26);
            }
            errors++;
          }
        }
        for (const key0 in data7) {
          if (key0 !== "x_svg_mm" && key0 !== "y_svg_mm") {
            const err27 = { instancePath: instancePath + "/geometry_transform/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/properties/geometry_transform/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err27];
            } else {
              vErrors.push(err27);
            }
            errors++;
          }
        }
      } else {
        const err28 = { instancePath: instancePath + "/geometry_transform", schemaPath: "#/properties/geometry_transform/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
    }
    if (data.metadata_coordinate_policy !== void 0) {
      if (typeof data.metadata_coordinate_policy !== "string") {
        const err29 = { instancePath: instancePath + "/metadata_coordinate_policy", schemaPath: "#/properties/metadata_coordinate_policy/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      }
    }
    if (data.view_box_mm !== void 0) {
      let data12 = data.view_box_mm;
      if (Array.isArray(data12)) {
        if (data12.length > 4) {
          const err30 = { instancePath: instancePath + "/view_box_mm", schemaPath: "#/$defs/Bounds/maxItems", keyword: "maxItems", params: { limit: 4 }, message: "must NOT have more than 4 items" };
          if (vErrors === null) {
            vErrors = [err30];
          } else {
            vErrors.push(err30);
          }
          errors++;
        }
        if (data12.length < 4) {
          const err31 = { instancePath: instancePath + "/view_box_mm", schemaPath: "#/$defs/Bounds/minItems", keyword: "minItems", params: { limit: 4 }, message: "must NOT have fewer than 4 items" };
          if (vErrors === null) {
            vErrors = [err31];
          } else {
            vErrors.push(err31);
          }
          errors++;
        }
        const len2 = data12.length;
        for (let i2 = 0; i2 < len2; i2++) {
          if (!(typeof data12[i2] == "number")) {
            const err32 = { instancePath: instancePath + "/view_box_mm/" + i2, schemaPath: "#/$defs/Bounds/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err32];
            } else {
              vErrors.push(err32);
            }
            errors++;
          }
        }
      } else {
        const err33 = { instancePath: instancePath + "/view_box_mm", schemaPath: "#/$defs/Bounds/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
    }
    if (data.scene_mirror_x !== void 0) {
      if (typeof data.scene_mirror_x !== "boolean") {
        const err34 = { instancePath: instancePath + "/scene_mirror_x", schemaPath: "#/properties/scene_mirror_x/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
        }
        errors++;
      }
    }
    if (data.scene_mirror_width_mm !== void 0) {
      if (!(typeof data.scene_mirror_width_mm == "number")) {
        const err35 = { instancePath: instancePath + "/scene_mirror_width_mm", schemaPath: "#/properties/scene_mirror_width_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err35];
        } else {
          vErrors.push(err35);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "bounds_mode" && key1 !== "bounds_mils" && key1 !== "margin_mm" && key1 !== "altium_origin_mils" && key1 !== "svg_units" && key1 !== "geometry_transform" && key1 !== "metadata_coordinate_policy" && key1 !== "view_box_mm" && key1 !== "scene_mirror_x" && key1 !== "scene_mirror_width_mm") {
        const err36 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err36];
        } else {
          vErrors.push(err36);
        }
        errors++;
      }
    }
  } else {
    const err37 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err37];
    } else {
      vErrors.push(err37);
    }
    errors++;
  }
  validate21.errors = vErrors;
  return errors === 0;
}
validate21.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate26(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate26.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
  } else {
    const err0 = { instancePath, schemaPath: "#/$defs/ImportedPcbSvgComponentLayers_RecordUnknown/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err0];
    } else {
      vErrors.push(err0);
    }
    errors++;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.index === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "index" }, message: "must have required property 'index'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.kind === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "kind" }, message: "must have required property 'kind'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.lower_z_mm === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "lower_z_mm" }, message: "must have required property 'lower_z_mm'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.upper_z_mm === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "upper_z_mm" }, message: "must have required property 'upper_z_mm'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.color === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "color" }, message: "must have required property 'color'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.opacity === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "opacity" }, message: "must have required property 'opacity'" };
      if (vErrors === null) {
        vErrors = [err6];
      } else {
        vErrors.push(err6);
      }
      errors++;
    }
    if (data.index !== void 0) {
      let data0 = data.index;
      if (!(typeof data0 == "number" && (!(data0 % 1) && !isNaN(data0)))) {
        const err7 = { instancePath: instancePath + "/index", schemaPath: "#/properties/index/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.kind !== void 0) {
      let data1 = data.kind;
      const _errs8 = errors;
      let valid3 = false;
      const _errs9 = errors;
      if (typeof data1 !== "string") {
        const err8 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      if ("step" !== data1) {
        const err9 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/anyOf/0/const", keyword: "const", params: { allowedValue: "step" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (typeof data1 !== "string") {
        const err10 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      if ("extruded" !== data1) {
        const err11 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/anyOf/1/const", keyword: "const", params: { allowedValue: "extruded" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid0 = _errs11 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err12 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      } else {
        errors = _errs8;
        if (vErrors !== null) {
          if (_errs8) {
            vErrors.length = _errs8;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.lower_z_mm !== void 0) {
      if (!(typeof data.lower_z_mm == "number")) {
        const err13 = { instancePath: instancePath + "/lower_z_mm", schemaPath: "#/properties/lower_z_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.upper_z_mm !== void 0) {
      if (!(typeof data.upper_z_mm == "number")) {
        const err14 = { instancePath: instancePath + "/upper_z_mm", schemaPath: "#/properties/upper_z_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
    }
    if (data.color !== void 0) {
      let data4 = data.color;
      const _errs18 = errors;
      let valid4 = false;
      const _errs19 = errors;
      if (Array.isArray(data4)) {
        const len0 = data4.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!(typeof data4[i0] == "number")) {
            const err15 = { instancePath: instancePath + "/color/" + i0, schemaPath: "#/properties/color/anyOf/0/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err15];
            } else {
              vErrors.push(err15);
            }
            errors++;
          }
        }
      } else {
        const err16 = { instancePath: instancePath + "/color", schemaPath: "#/properties/color/anyOf/0/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid1 = _errs19 === errors;
      valid4 = valid4 || _valid1;
      const _errs23 = errors;
      if (data4 !== null) {
        const err17 = { instancePath: instancePath + "/color", schemaPath: "#/properties/color/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      var _valid1 = _errs23 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err18 = { instancePath: instancePath + "/color", schemaPath: "#/properties/color/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      } else {
        errors = _errs18;
        if (vErrors !== null) {
          if (_errs18) {
            vErrors.length = _errs18;
          } else {
            vErrors = null;
          }
        }
      }
      if (Array.isArray(data4)) {
        if (data4.length > 3) {
          const err19 = { instancePath: instancePath + "/color", schemaPath: "#/properties/color/maxItems", keyword: "maxItems", params: { limit: 3 }, message: "must NOT have more than 3 items" };
          if (vErrors === null) {
            vErrors = [err19];
          } else {
            vErrors.push(err19);
          }
          errors++;
        }
        if (data4.length < 3) {
          const err20 = { instancePath: instancePath + "/color", schemaPath: "#/properties/color/minItems", keyword: "minItems", params: { limit: 3 }, message: "must NOT have fewer than 3 items" };
          if (vErrors === null) {
            vErrors = [err20];
          } else {
            vErrors.push(err20);
          }
          errors++;
        }
      }
    }
    if (data.opacity !== void 0) {
      let data6 = data.opacity;
      if (typeof data6 == "number") {
        if (data6 > 1 || isNaN(data6)) {
          const err21 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/maximum", keyword: "maximum", params: { comparison: "<=", limit: 1 }, message: "must be <= 1" };
          if (vErrors === null) {
            vErrors = [err21];
          } else {
            vErrors.push(err21);
          }
          errors++;
        }
        if (data6 < 0 || isNaN(data6)) {
          const err22 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err22];
          } else {
            vErrors.push(err22);
          }
          errors++;
        }
      } else {
        const err23 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/type", keyword: "type", params: { type: "number" }, message: "must be number" };
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
  validate26.errors = vErrors;
  return errors === 0;
}
validate26.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate25(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate25.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
  } else {
    const err0 = { instancePath, schemaPath: "#/$defs/ImportedPcbSvgComponentLayers_RecordUnknown/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err0];
    } else {
      vErrors.push(err0);
    }
    errors++;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.group_id === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "group_id" }, message: "must have required property 'group_id'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.component_index === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "component_index" }, message: "must have required property 'component_index'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.designator === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "designator" }, message: "must have required property 'designator'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.group_id !== void 0) {
      if (typeof data.group_id !== "string") {
        const err4 = { instancePath: instancePath + "/group_id", schemaPath: "#/properties/group_id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.component_index !== void 0) {
      let data1 = data.component_index;
      const _errs8 = errors;
      let valid3 = false;
      const _errs9 = errors;
      if (!(typeof data1 == "number" && (!(data1 % 1) && !isNaN(data1)))) {
        const err5 = { instancePath: instancePath + "/component_index", schemaPath: "#/properties/component_index/anyOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (data1 !== null) {
        const err6 = { instancePath: instancePath + "/component_index", schemaPath: "#/properties/component_index/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs11 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err7 = { instancePath: instancePath + "/component_index", schemaPath: "#/properties/component_index/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      } else {
        errors = _errs8;
        if (vErrors !== null) {
          if (_errs8) {
            vErrors.length = _errs8;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.designator !== void 0) {
      if (typeof data.designator !== "string") {
        const err8 = { instancePath: instancePath + "/designator", schemaPath: "#/properties/designator/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
    if (data.side !== void 0) {
      let data3 = data.side;
      const _errs16 = errors;
      let valid4 = false;
      const _errs17 = errors;
      if (typeof data3 !== "string") {
        const err9 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      if ("top" !== data3) {
        const err10 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/const", keyword: "const", params: { allowedValue: "top" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid1 = _errs17 === errors;
      valid4 = valid4 || _valid1;
      const _errs19 = errors;
      if (typeof data3 !== "string") {
        const err11 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      if ("bottom" !== data3) {
        const err12 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/1/const", keyword: "const", params: { allowedValue: "bottom" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid1 = _errs19 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err13 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
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
    if (data.symbol_id !== void 0) {
      if (typeof data.symbol_id !== "string") {
        const err14 = { instancePath: instancePath + "/symbol_id", schemaPath: "#/properties/symbol_id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
    }
    if (data.anchor_svg_mm !== void 0) {
      let data5 = data.anchor_svg_mm;
      if (Array.isArray(data5)) {
        if (data5.length > 2) {
          const err15 = { instancePath: instancePath + "/anchor_svg_mm", schemaPath: "#/properties/anchor_svg_mm/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err15];
          } else {
            vErrors.push(err15);
          }
          errors++;
        }
        if (data5.length < 2) {
          const err16 = { instancePath: instancePath + "/anchor_svg_mm", schemaPath: "#/properties/anchor_svg_mm/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err16];
          } else {
            vErrors.push(err16);
          }
          errors++;
        }
        const len0 = data5.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!(typeof data5[i0] == "number")) {
            const err17 = { instancePath: instancePath + "/anchor_svg_mm/" + i0, schemaPath: "#/properties/anchor_svg_mm/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err17];
            } else {
              vErrors.push(err17);
            }
            errors++;
          }
        }
      } else {
        const err18 = { instancePath: instancePath + "/anchor_svg_mm", schemaPath: "#/properties/anchor_svg_mm/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
    }
    if (data.anchor_board_mm !== void 0) {
      let data7 = data.anchor_board_mm;
      if (Array.isArray(data7)) {
        if (data7.length > 2) {
          const err19 = { instancePath: instancePath + "/anchor_board_mm", schemaPath: "#/properties/anchor_board_mm/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err19];
          } else {
            vErrors.push(err19);
          }
          errors++;
        }
        if (data7.length < 2) {
          const err20 = { instancePath: instancePath + "/anchor_board_mm", schemaPath: "#/properties/anchor_board_mm/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err20];
          } else {
            vErrors.push(err20);
          }
          errors++;
        }
        const len1 = data7.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (!(typeof data7[i1] == "number")) {
            const err21 = { instancePath: instancePath + "/anchor_board_mm/" + i1, schemaPath: "#/properties/anchor_board_mm/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err21];
            } else {
              vErrors.push(err21);
            }
            errors++;
          }
        }
      } else {
        const err22 = { instancePath: instancePath + "/anchor_board_mm", schemaPath: "#/properties/anchor_board_mm/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
    }
    if (data.bounds_local_xyz_mm !== void 0) {
      let data9 = data.bounds_local_xyz_mm;
      if (Array.isArray(data9)) {
        if (data9.length > 6) {
          const err23 = { instancePath: instancePath + "/bounds_local_xyz_mm", schemaPath: "#/properties/bounds_local_xyz_mm/maxItems", keyword: "maxItems", params: { limit: 6 }, message: "must NOT have more than 6 items" };
          if (vErrors === null) {
            vErrors = [err23];
          } else {
            vErrors.push(err23);
          }
          errors++;
        }
        if (data9.length < 6) {
          const err24 = { instancePath: instancePath + "/bounds_local_xyz_mm", schemaPath: "#/properties/bounds_local_xyz_mm/minItems", keyword: "minItems", params: { limit: 6 }, message: "must NOT have fewer than 6 items" };
          if (vErrors === null) {
            vErrors = [err24];
          } else {
            vErrors.push(err24);
          }
          errors++;
        }
        const len2 = data9.length;
        for (let i2 = 0; i2 < len2; i2++) {
          if (!(typeof data9[i2] == "number")) {
            const err25 = { instancePath: instancePath + "/bounds_local_xyz_mm/" + i2, schemaPath: "#/properties/bounds_local_xyz_mm/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err25];
            } else {
              vErrors.push(err25);
            }
            errors++;
          }
        }
      } else {
        const err26 = { instancePath: instancePath + "/bounds_local_xyz_mm", schemaPath: "#/properties/bounds_local_xyz_mm/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
    }
    if (data.bodies !== void 0) {
      let data11 = data.bodies;
      if (Array.isArray(data11)) {
        const len3 = data11.length;
        for (let i3 = 0; i3 < len3; i3++) {
          if (!validate26(data11[i3], { instancePath: instancePath + "/bodies/" + i3, parentData: data11, parentDataProperty: i3, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate26.errors : vErrors.concat(validate26.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err27 = { instancePath: instancePath + "/bodies", schemaPath: "#/properties/bodies/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
    }
    if (data.paint_order !== void 0) {
      let data13 = data.paint_order;
      if (!(typeof data13 == "number" && (!(data13 % 1) && !isNaN(data13)))) {
        const err28 = { instancePath: instancePath + "/paint_order", schemaPath: "#/properties/paint_order/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
      if (typeof data13 == "number") {
        if (data13 < 0 || isNaN(data13)) {
          const err29 = { instancePath: instancePath + "/paint_order", schemaPath: "#/properties/paint_order/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err29];
          } else {
            vErrors.push(err29);
          }
          errors++;
        }
      }
    }
    if (data.geometry_source !== void 0) {
      let data14 = data.geometry_source;
      const _errs41 = errors;
      let valid13 = false;
      const _errs42 = errors;
      if (typeof data14 !== "string") {
        const err30 = { instancePath: instancePath + "/geometry_source", schemaPath: "#/properties/geometry_source/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
        }
        errors++;
      }
      if ("model" !== data14) {
        const err31 = { instancePath: instancePath + "/geometry_source", schemaPath: "#/properties/geometry_source/anyOf/0/const", keyword: "const", params: { allowedValue: "model" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      }
      var _valid2 = _errs42 === errors;
      valid13 = valid13 || _valid2;
      const _errs44 = errors;
      if (typeof data14 !== "string") {
        const err32 = { instancePath: instancePath + "/geometry_source", schemaPath: "#/properties/geometry_source/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
        }
        errors++;
      }
      if ("pads" !== data14) {
        const err33 = { instancePath: instancePath + "/geometry_source", schemaPath: "#/properties/geometry_source/anyOf/1/const", keyword: "const", params: { allowedValue: "pads" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
      var _valid2 = _errs44 === errors;
      valid13 = valid13 || _valid2;
      if (!valid13) {
        const err34 = { instancePath: instancePath + "/geometry_source", schemaPath: "#/properties/geometry_source/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
        }
        errors++;
      } else {
        errors = _errs41;
        if (vErrors !== null) {
          if (_errs41) {
            vErrors.length = _errs41;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.center_view_mm !== void 0) {
      let data15 = data.center_view_mm;
      if (Array.isArray(data15)) {
        if (data15.length > 2) {
          const err35 = { instancePath: instancePath + "/center_view_mm", schemaPath: "#/properties/center_view_mm/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err35];
          } else {
            vErrors.push(err35);
          }
          errors++;
        }
        if (data15.length < 2) {
          const err36 = { instancePath: instancePath + "/center_view_mm", schemaPath: "#/properties/center_view_mm/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err36];
          } else {
            vErrors.push(err36);
          }
          errors++;
        }
        const len4 = data15.length;
        for (let i4 = 0; i4 < len4; i4++) {
          if (!(typeof data15[i4] == "number")) {
            const err37 = { instancePath: instancePath + "/center_view_mm/" + i4, schemaPath: "#/properties/center_view_mm/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err37];
            } else {
              vErrors.push(err37);
            }
            errors++;
          }
        }
      } else {
        const err38 = { instancePath: instancePath + "/center_view_mm", schemaPath: "#/properties/center_view_mm/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err38];
        } else {
          vErrors.push(err38);
        }
        errors++;
      }
    }
    if (data.font_size_mm !== void 0) {
      let data17 = data.font_size_mm;
      if (typeof data17 == "number") {
        if (data17 <= 0 || isNaN(data17)) {
          const err39 = { instancePath: instancePath + "/font_size_mm", schemaPath: "#/properties/font_size_mm/exclusiveMinimum", keyword: "exclusiveMinimum", params: { comparison: ">", limit: 0 }, message: "must be > 0" };
          if (vErrors === null) {
            vErrors = [err39];
          } else {
            vErrors.push(err39);
          }
          errors++;
        }
      } else {
        const err40 = { instancePath: instancePath + "/font_size_mm", schemaPath: "#/properties/font_size_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err40];
        } else {
          vErrors.push(err40);
        }
        errors++;
      }
    }
    if (data.rotation_degrees !== void 0) {
      if (!(typeof data.rotation_degrees == "number")) {
        const err41 = { instancePath: instancePath + "/rotation_degrees", schemaPath: "#/properties/rotation_degrees/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err41];
        } else {
          vErrors.push(err41);
        }
        errors++;
      }
    }
  } else {
    const err42 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err42];
    } else {
      vErrors.push(err42);
    }
    errors++;
  }
  validate25.errors = vErrors;
  return errors === 0;
}
validate25.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
  } else {
    const err0 = { instancePath, schemaPath: "#/$defs/ImportedPcbSvgComponentLayers_RecordUnknown/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err0];
    } else {
      vErrors.push(err0);
    }
    errors++;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.token === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "token" }, message: "must have required property 'token'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.group_id === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "group_id" }, message: "must have required property 'group_id'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.side === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "side" }, message: "must have required property 'side'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.instances === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "instances" }, message: "must have required property 'instances'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.token !== void 0) {
      let data0 = data.token;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err5 = { instancePath: instancePath + "/token", schemaPath: "#/properties/token/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      if ("ILLUSTRATION_TOP" !== data0) {
        const err6 = { instancePath: instancePath + "/token", schemaPath: "#/properties/token/anyOf/0/const", keyword: "const", params: { allowedValue: "ILLUSTRATION_TOP" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid3 = valid3 || _valid0;
      const _errs9 = errors;
      if (typeof data0 !== "string") {
        const err7 = { instancePath: instancePath + "/token", schemaPath: "#/properties/token/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      if ("ILLUSTRATION_BOTTOM" !== data0) {
        const err8 = { instancePath: instancePath + "/token", schemaPath: "#/properties/token/anyOf/1/const", keyword: "const", params: { allowedValue: "ILLUSTRATION_BOTTOM" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (typeof data0 !== "string") {
        const err9 = { instancePath: instancePath + "/token", schemaPath: "#/properties/token/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      if ("ASSEMBLY_DESIGNATORS_TOP" !== data0) {
        const err10 = { instancePath: instancePath + "/token", schemaPath: "#/properties/token/anyOf/2/const", keyword: "const", params: { allowedValue: "ASSEMBLY_DESIGNATORS_TOP" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid0 = _errs11 === errors;
      valid3 = valid3 || _valid0;
      const _errs13 = errors;
      if (typeof data0 !== "string") {
        const err11 = { instancePath: instancePath + "/token", schemaPath: "#/properties/token/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      if ("ASSEMBLY_DESIGNATORS_BOTTOM" !== data0) {
        const err12 = { instancePath: instancePath + "/token", schemaPath: "#/properties/token/anyOf/3/const", keyword: "const", params: { allowedValue: "ASSEMBLY_DESIGNATORS_BOTTOM" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid0 = _errs13 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err13 = { instancePath: instancePath + "/token", schemaPath: "#/properties/token/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      } else {
        errors = _errs6;
        if (vErrors !== null) {
          if (_errs6) {
            vErrors.length = _errs6;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.group_id !== void 0) {
      if (typeof data.group_id !== "string") {
        const err14 = { instancePath: instancePath + "/group_id", schemaPath: "#/properties/group_id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
    }
    if (data.side !== void 0) {
      let data2 = data.side;
      const _errs18 = errors;
      let valid4 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err15 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      if ("top" !== data2) {
        const err16 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/const", keyword: "const", params: { allowedValue: "top" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid1 = _errs19 === errors;
      valid4 = valid4 || _valid1;
      const _errs21 = errors;
      if (typeof data2 !== "string") {
        const err17 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      if ("bottom" !== data2) {
        const err18 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/1/const", keyword: "const", params: { allowedValue: "bottom" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
      var _valid1 = _errs21 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err19 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      } else {
        errors = _errs18;
        if (vErrors !== null) {
          if (_errs18) {
            vErrors.length = _errs18;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.instances !== void 0) {
      let data3 = data.instances;
      if (Array.isArray(data3)) {
        const len0 = data3.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!validate25(data3[i0], { instancePath: instancePath + "/instances/" + i0, parentData: data3, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate25.errors : vErrors.concat(validate25.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err20 = { instancePath: instancePath + "/instances", schemaPath: "#/properties/instances/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
    }
    if (data.unique_symbols !== void 0) {
      let data5 = data.unique_symbols;
      if (!(typeof data5 == "number" && (!(data5 % 1) && !isNaN(data5)))) {
        const err21 = { instancePath: instancePath + "/unique_symbols", schemaPath: "#/properties/unique_symbols/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      if (typeof data5 == "number") {
        if (data5 < 0 || isNaN(data5)) {
          const err22 = { instancePath: instancePath + "/unique_symbols", schemaPath: "#/properties/unique_symbols/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err22];
          } else {
            vErrors.push(err22);
          }
          errors++;
        }
      }
    }
  } else {
    const err23 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err23];
    } else {
      vErrors.push(err23);
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
  } else {
    const err0 = { instancePath, schemaPath: "#/$defs/ImportedPcbSvgComponentLayers_RecordUnknown/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err0];
    } else {
      vErrors.push(err0);
    }
    errors++;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.schema === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "schema" }, message: "must have required property 'schema'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.coordinate_policy === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "coordinate_policy" }, message: "must have required property 'coordinate_policy'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.layers === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "layers" }, message: "must have required property 'layers'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.schema !== void 0) {
      let data0 = data.schema;
      if (typeof data0 !== "string") {
        const err4 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      if ("pcb.svg.component-layers.a0" !== data0) {
        const err5 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "pcb.svg.component-layers.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.coordinate_policy !== void 0) {
      if (typeof data.coordinate_policy !== "string") {
        const err6 = { instancePath: instancePath + "/coordinate_policy", schemaPath: "#/properties/coordinate_policy/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.layers !== void 0) {
      let data2 = data.layers;
      if (Array.isArray(data2)) {
        const len0 = data2.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!validate24(data2[i0], { instancePath: instancePath + "/layers/" + i0, parentData: data2, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate24.errors : vErrors.concat(validate24.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err7 = { instancePath: instancePath + "/layers", schemaPath: "#/properties/layers/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
  } else {
    const err8 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err8];
    } else {
      vErrors.push(err8);
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
    if (data.canvas === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "canvas" }, message: "must have required property 'canvas'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.canvas !== void 0) {
      if (!validate21(data.canvas, { instancePath: instancePath + "/canvas", parentData: data, parentDataProperty: "canvas", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
        errors = vErrors.length;
      }
    }
    if (data.virtual_component_layers !== void 0) {
      if (!validate23(data.virtual_component_layers, { instancePath: instancePath + "/virtual_component_layers", parentData: data, parentDataProperty: "virtual_component_layers", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate23.errors : vErrors.concat(validate23.errors);
        errors = vErrors.length;
      }
    }
  } else {
    const err2 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err2];
    } else {
      vErrors.push(err2);
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
