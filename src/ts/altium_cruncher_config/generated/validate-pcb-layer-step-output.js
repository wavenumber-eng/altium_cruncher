// Generated from src/tsp/altium_cruncher/outputs/pcb-layer-step.tsp. Do not edit.
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
    if (data.mode === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "mode" }, message: "must have required property 'mode'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.origin_mils === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "origin_mils" }, message: "must have required property 'origin_mils'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.origin_mm === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "origin_mm" }, message: "must have required property 'origin_mm'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.geometry === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "geometry" }, message: "must have required property 'geometry'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.mode !== void 0) {
      let data0 = data.mode;
      if (typeof data0 !== "string") {
        const err4 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      if ("board_origin" !== data0) {
        const err5 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/const", keyword: "const", params: { allowedValue: "board_origin" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.origin_mils !== void 0) {
      let data1 = data.origin_mils;
      if (Array.isArray(data1)) {
        if (data1.length > 2) {
          const err6 = { instancePath: instancePath + "/origin_mils", schemaPath: "#/$defs/Point/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err6];
          } else {
            vErrors.push(err6);
          }
          errors++;
        }
        if (data1.length < 2) {
          const err7 = { instancePath: instancePath + "/origin_mils", schemaPath: "#/$defs/Point/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err7];
          } else {
            vErrors.push(err7);
          }
          errors++;
        }
        const len0 = data1.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!(typeof data1[i0] == "number")) {
            const err8 = { instancePath: instancePath + "/origin_mils/" + i0, schemaPath: "#/$defs/Point/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err8];
            } else {
              vErrors.push(err8);
            }
            errors++;
          }
        }
      } else {
        const err9 = { instancePath: instancePath + "/origin_mils", schemaPath: "#/$defs/Point/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    if (data.origin_mm !== void 0) {
      let data3 = data.origin_mm;
      if (Array.isArray(data3)) {
        if (data3.length > 2) {
          const err10 = { instancePath: instancePath + "/origin_mm", schemaPath: "#/$defs/Point/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err10];
          } else {
            vErrors.push(err10);
          }
          errors++;
        }
        if (data3.length < 2) {
          const err11 = { instancePath: instancePath + "/origin_mm", schemaPath: "#/$defs/Point/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err11];
          } else {
            vErrors.push(err11);
          }
          errors++;
        }
        const len1 = data3.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (!(typeof data3[i1] == "number")) {
            const err12 = { instancePath: instancePath + "/origin_mm/" + i1, schemaPath: "#/$defs/Point/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err12];
            } else {
              vErrors.push(err12);
            }
            errors++;
          }
        }
      } else {
        const err13 = { instancePath: instancePath + "/origin_mm", schemaPath: "#/$defs/Point/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.geometry !== void 0) {
      if (typeof data.geometry !== "string") {
        const err14 = { instancePath: instancePath + "/geometry", schemaPath: "#/properties/geometry/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
    }
    for (const key0 in data) {
      if (key0 !== "mode" && key0 !== "origin_mils" && key0 !== "origin_mm" && key0 !== "geometry") {
        const err15 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
    }
  } else {
    const err16 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err16];
    } else {
      vErrors.push(err16);
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
    if (data.tracks === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "tracks" }, message: "must have required property 'tracks'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.arcs === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "arcs" }, message: "must have required property 'arcs'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.fills === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "fills" }, message: "must have required property 'fills'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.polygons === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "polygons" }, message: "must have required property 'polygons'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.regions === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "regions" }, message: "must have required property 'regions'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.vias === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "vias" }, message: "must have required property 'vias'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.component_pads === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "component_pads" }, message: "must have required property 'component_pads'" };
      if (vErrors === null) {
        vErrors = [err6];
      } else {
        vErrors.push(err6);
      }
      errors++;
    }
    if (data.free_pads === void 0) {
      const err7 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "free_pads" }, message: "must have required property 'free_pads'" };
      if (vErrors === null) {
        vErrors = [err7];
      } else {
        vErrors.push(err7);
      }
      errors++;
    }
    if (data.tracks !== void 0) {
      let data0 = data.tracks;
      if (data0 && typeof data0 == "object" && !Array.isArray(data0)) {
        if (data0.color === void 0) {
          const err8 = { instancePath: instancePath + "/tracks", schemaPath: "#/$defs/FeatureStyle/required", keyword: "required", params: { missingProperty: "color" }, message: "must have required property 'color'" };
          if (vErrors === null) {
            vErrors = [err8];
          } else {
            vErrors.push(err8);
          }
          errors++;
        }
        if (data0.step_body_name === void 0) {
          const err9 = { instancePath: instancePath + "/tracks", schemaPath: "#/$defs/FeatureStyle/required", keyword: "required", params: { missingProperty: "step_body_name" }, message: "must have required property 'step_body_name'" };
          if (vErrors === null) {
            vErrors = [err9];
          } else {
            vErrors.push(err9);
          }
          errors++;
        }
        if (data0.color !== void 0) {
          let data1 = data0.color;
          const _errs5 = errors;
          let valid3 = false;
          const _errs6 = errors;
          if (typeof data1 !== "string") {
            const err10 = { instancePath: instancePath + "/tracks/color", schemaPath: "#/$defs/FeatureStyle/properties/color/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err10];
            } else {
              vErrors.push(err10);
            }
            errors++;
          }
          var _valid0 = _errs6 === errors;
          valid3 = valid3 || _valid0;
          const _errs8 = errors;
          if (data1 !== null) {
            const err11 = { instancePath: instancePath + "/tracks/color", schemaPath: "#/$defs/FeatureStyle/properties/color/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err11];
            } else {
              vErrors.push(err11);
            }
            errors++;
          }
          var _valid0 = _errs8 === errors;
          valid3 = valid3 || _valid0;
          if (!valid3) {
            const err12 = { instancePath: instancePath + "/tracks/color", schemaPath: "#/$defs/FeatureStyle/properties/color/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err12];
            } else {
              vErrors.push(err12);
            }
            errors++;
          } else {
            errors = _errs5;
            if (vErrors !== null) {
              if (_errs5) {
                vErrors.length = _errs5;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data0.step_body_name !== void 0) {
          let data2 = data0.step_body_name;
          const _errs11 = errors;
          let valid4 = false;
          const _errs12 = errors;
          if (typeof data2 !== "string") {
            const err13 = { instancePath: instancePath + "/tracks/step_body_name", schemaPath: "#/$defs/FeatureStyle/properties/step_body_name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err13];
            } else {
              vErrors.push(err13);
            }
            errors++;
          }
          var _valid1 = _errs12 === errors;
          valid4 = valid4 || _valid1;
          const _errs14 = errors;
          if (data2 !== null) {
            const err14 = { instancePath: instancePath + "/tracks/step_body_name", schemaPath: "#/$defs/FeatureStyle/properties/step_body_name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err14];
            } else {
              vErrors.push(err14);
            }
            errors++;
          }
          var _valid1 = _errs14 === errors;
          valid4 = valid4 || _valid1;
          if (!valid4) {
            const err15 = { instancePath: instancePath + "/tracks/step_body_name", schemaPath: "#/$defs/FeatureStyle/properties/step_body_name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err15];
            } else {
              vErrors.push(err15);
            }
            errors++;
          } else {
            errors = _errs11;
            if (vErrors !== null) {
              if (_errs11) {
                vErrors.length = _errs11;
              } else {
                vErrors = null;
              }
            }
          }
        }
        for (const key0 in data0) {
          if (key0 !== "color" && key0 !== "step_body_name") {
            const err16 = { instancePath: instancePath + "/tracks/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/FeatureStyle/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err16];
            } else {
              vErrors.push(err16);
            }
            errors++;
          }
        }
      } else {
        const err17 = { instancePath: instancePath + "/tracks", schemaPath: "#/$defs/FeatureStyle/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
    }
    if (data.arcs !== void 0) {
      let data4 = data.arcs;
      if (data4 && typeof data4 == "object" && !Array.isArray(data4)) {
        if (data4.color === void 0) {
          const err18 = { instancePath: instancePath + "/arcs", schemaPath: "#/$defs/FeatureStyle/required", keyword: "required", params: { missingProperty: "color" }, message: "must have required property 'color'" };
          if (vErrors === null) {
            vErrors = [err18];
          } else {
            vErrors.push(err18);
          }
          errors++;
        }
        if (data4.step_body_name === void 0) {
          const err19 = { instancePath: instancePath + "/arcs", schemaPath: "#/$defs/FeatureStyle/required", keyword: "required", params: { missingProperty: "step_body_name" }, message: "must have required property 'step_body_name'" };
          if (vErrors === null) {
            vErrors = [err19];
          } else {
            vErrors.push(err19);
          }
          errors++;
        }
        if (data4.color !== void 0) {
          let data5 = data4.color;
          const _errs23 = errors;
          let valid8 = false;
          const _errs24 = errors;
          if (typeof data5 !== "string") {
            const err20 = { instancePath: instancePath + "/arcs/color", schemaPath: "#/$defs/FeatureStyle/properties/color/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err20];
            } else {
              vErrors.push(err20);
            }
            errors++;
          }
          var _valid2 = _errs24 === errors;
          valid8 = valid8 || _valid2;
          const _errs26 = errors;
          if (data5 !== null) {
            const err21 = { instancePath: instancePath + "/arcs/color", schemaPath: "#/$defs/FeatureStyle/properties/color/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err21];
            } else {
              vErrors.push(err21);
            }
            errors++;
          }
          var _valid2 = _errs26 === errors;
          valid8 = valid8 || _valid2;
          if (!valid8) {
            const err22 = { instancePath: instancePath + "/arcs/color", schemaPath: "#/$defs/FeatureStyle/properties/color/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err22];
            } else {
              vErrors.push(err22);
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
        if (data4.step_body_name !== void 0) {
          let data6 = data4.step_body_name;
          const _errs29 = errors;
          let valid9 = false;
          const _errs30 = errors;
          if (typeof data6 !== "string") {
            const err23 = { instancePath: instancePath + "/arcs/step_body_name", schemaPath: "#/$defs/FeatureStyle/properties/step_body_name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err23];
            } else {
              vErrors.push(err23);
            }
            errors++;
          }
          var _valid3 = _errs30 === errors;
          valid9 = valid9 || _valid3;
          const _errs32 = errors;
          if (data6 !== null) {
            const err24 = { instancePath: instancePath + "/arcs/step_body_name", schemaPath: "#/$defs/FeatureStyle/properties/step_body_name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err24];
            } else {
              vErrors.push(err24);
            }
            errors++;
          }
          var _valid3 = _errs32 === errors;
          valid9 = valid9 || _valid3;
          if (!valid9) {
            const err25 = { instancePath: instancePath + "/arcs/step_body_name", schemaPath: "#/$defs/FeatureStyle/properties/step_body_name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err25];
            } else {
              vErrors.push(err25);
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
        for (const key1 in data4) {
          if (key1 !== "color" && key1 !== "step_body_name") {
            const err26 = { instancePath: instancePath + "/arcs/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/FeatureStyle/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err26];
            } else {
              vErrors.push(err26);
            }
            errors++;
          }
        }
      } else {
        const err27 = { instancePath: instancePath + "/arcs", schemaPath: "#/$defs/FeatureStyle/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
    }
    if (data.fills !== void 0) {
      let data8 = data.fills;
      if (data8 && typeof data8 == "object" && !Array.isArray(data8)) {
        if (data8.color === void 0) {
          const err28 = { instancePath: instancePath + "/fills", schemaPath: "#/$defs/FeatureStyle/required", keyword: "required", params: { missingProperty: "color" }, message: "must have required property 'color'" };
          if (vErrors === null) {
            vErrors = [err28];
          } else {
            vErrors.push(err28);
          }
          errors++;
        }
        if (data8.step_body_name === void 0) {
          const err29 = { instancePath: instancePath + "/fills", schemaPath: "#/$defs/FeatureStyle/required", keyword: "required", params: { missingProperty: "step_body_name" }, message: "must have required property 'step_body_name'" };
          if (vErrors === null) {
            vErrors = [err29];
          } else {
            vErrors.push(err29);
          }
          errors++;
        }
        if (data8.color !== void 0) {
          let data9 = data8.color;
          const _errs41 = errors;
          let valid13 = false;
          const _errs42 = errors;
          if (typeof data9 !== "string") {
            const err30 = { instancePath: instancePath + "/fills/color", schemaPath: "#/$defs/FeatureStyle/properties/color/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err30];
            } else {
              vErrors.push(err30);
            }
            errors++;
          }
          var _valid4 = _errs42 === errors;
          valid13 = valid13 || _valid4;
          const _errs44 = errors;
          if (data9 !== null) {
            const err31 = { instancePath: instancePath + "/fills/color", schemaPath: "#/$defs/FeatureStyle/properties/color/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err31];
            } else {
              vErrors.push(err31);
            }
            errors++;
          }
          var _valid4 = _errs44 === errors;
          valid13 = valid13 || _valid4;
          if (!valid13) {
            const err32 = { instancePath: instancePath + "/fills/color", schemaPath: "#/$defs/FeatureStyle/properties/color/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err32];
            } else {
              vErrors.push(err32);
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
        if (data8.step_body_name !== void 0) {
          let data10 = data8.step_body_name;
          const _errs47 = errors;
          let valid14 = false;
          const _errs48 = errors;
          if (typeof data10 !== "string") {
            const err33 = { instancePath: instancePath + "/fills/step_body_name", schemaPath: "#/$defs/FeatureStyle/properties/step_body_name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err33];
            } else {
              vErrors.push(err33);
            }
            errors++;
          }
          var _valid5 = _errs48 === errors;
          valid14 = valid14 || _valid5;
          const _errs50 = errors;
          if (data10 !== null) {
            const err34 = { instancePath: instancePath + "/fills/step_body_name", schemaPath: "#/$defs/FeatureStyle/properties/step_body_name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err34];
            } else {
              vErrors.push(err34);
            }
            errors++;
          }
          var _valid5 = _errs50 === errors;
          valid14 = valid14 || _valid5;
          if (!valid14) {
            const err35 = { instancePath: instancePath + "/fills/step_body_name", schemaPath: "#/$defs/FeatureStyle/properties/step_body_name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err35];
            } else {
              vErrors.push(err35);
            }
            errors++;
          } else {
            errors = _errs47;
            if (vErrors !== null) {
              if (_errs47) {
                vErrors.length = _errs47;
              } else {
                vErrors = null;
              }
            }
          }
        }
        for (const key2 in data8) {
          if (key2 !== "color" && key2 !== "step_body_name") {
            const err36 = { instancePath: instancePath + "/fills/" + key2.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/FeatureStyle/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err36];
            } else {
              vErrors.push(err36);
            }
            errors++;
          }
        }
      } else {
        const err37 = { instancePath: instancePath + "/fills", schemaPath: "#/$defs/FeatureStyle/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err37];
        } else {
          vErrors.push(err37);
        }
        errors++;
      }
    }
    if (data.polygons !== void 0) {
      let data12 = data.polygons;
      if (data12 && typeof data12 == "object" && !Array.isArray(data12)) {
        if (data12.color === void 0) {
          const err38 = { instancePath: instancePath + "/polygons", schemaPath: "#/$defs/FeatureStyle/required", keyword: "required", params: { missingProperty: "color" }, message: "must have required property 'color'" };
          if (vErrors === null) {
            vErrors = [err38];
          } else {
            vErrors.push(err38);
          }
          errors++;
        }
        if (data12.step_body_name === void 0) {
          const err39 = { instancePath: instancePath + "/polygons", schemaPath: "#/$defs/FeatureStyle/required", keyword: "required", params: { missingProperty: "step_body_name" }, message: "must have required property 'step_body_name'" };
          if (vErrors === null) {
            vErrors = [err39];
          } else {
            vErrors.push(err39);
          }
          errors++;
        }
        if (data12.color !== void 0) {
          let data13 = data12.color;
          const _errs59 = errors;
          let valid18 = false;
          const _errs60 = errors;
          if (typeof data13 !== "string") {
            const err40 = { instancePath: instancePath + "/polygons/color", schemaPath: "#/$defs/FeatureStyle/properties/color/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err40];
            } else {
              vErrors.push(err40);
            }
            errors++;
          }
          var _valid6 = _errs60 === errors;
          valid18 = valid18 || _valid6;
          const _errs62 = errors;
          if (data13 !== null) {
            const err41 = { instancePath: instancePath + "/polygons/color", schemaPath: "#/$defs/FeatureStyle/properties/color/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err41];
            } else {
              vErrors.push(err41);
            }
            errors++;
          }
          var _valid6 = _errs62 === errors;
          valid18 = valid18 || _valid6;
          if (!valid18) {
            const err42 = { instancePath: instancePath + "/polygons/color", schemaPath: "#/$defs/FeatureStyle/properties/color/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err42];
            } else {
              vErrors.push(err42);
            }
            errors++;
          } else {
            errors = _errs59;
            if (vErrors !== null) {
              if (_errs59) {
                vErrors.length = _errs59;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data12.step_body_name !== void 0) {
          let data14 = data12.step_body_name;
          const _errs65 = errors;
          let valid19 = false;
          const _errs66 = errors;
          if (typeof data14 !== "string") {
            const err43 = { instancePath: instancePath + "/polygons/step_body_name", schemaPath: "#/$defs/FeatureStyle/properties/step_body_name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err43];
            } else {
              vErrors.push(err43);
            }
            errors++;
          }
          var _valid7 = _errs66 === errors;
          valid19 = valid19 || _valid7;
          const _errs68 = errors;
          if (data14 !== null) {
            const err44 = { instancePath: instancePath + "/polygons/step_body_name", schemaPath: "#/$defs/FeatureStyle/properties/step_body_name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err44];
            } else {
              vErrors.push(err44);
            }
            errors++;
          }
          var _valid7 = _errs68 === errors;
          valid19 = valid19 || _valid7;
          if (!valid19) {
            const err45 = { instancePath: instancePath + "/polygons/step_body_name", schemaPath: "#/$defs/FeatureStyle/properties/step_body_name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err45];
            } else {
              vErrors.push(err45);
            }
            errors++;
          } else {
            errors = _errs65;
            if (vErrors !== null) {
              if (_errs65) {
                vErrors.length = _errs65;
              } else {
                vErrors = null;
              }
            }
          }
        }
        for (const key3 in data12) {
          if (key3 !== "color" && key3 !== "step_body_name") {
            const err46 = { instancePath: instancePath + "/polygons/" + key3.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/FeatureStyle/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err46];
            } else {
              vErrors.push(err46);
            }
            errors++;
          }
        }
      } else {
        const err47 = { instancePath: instancePath + "/polygons", schemaPath: "#/$defs/FeatureStyle/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err47];
        } else {
          vErrors.push(err47);
        }
        errors++;
      }
    }
    if (data.regions !== void 0) {
      let data16 = data.regions;
      if (data16 && typeof data16 == "object" && !Array.isArray(data16)) {
        if (data16.color === void 0) {
          const err48 = { instancePath: instancePath + "/regions", schemaPath: "#/$defs/FeatureStyle/required", keyword: "required", params: { missingProperty: "color" }, message: "must have required property 'color'" };
          if (vErrors === null) {
            vErrors = [err48];
          } else {
            vErrors.push(err48);
          }
          errors++;
        }
        if (data16.step_body_name === void 0) {
          const err49 = { instancePath: instancePath + "/regions", schemaPath: "#/$defs/FeatureStyle/required", keyword: "required", params: { missingProperty: "step_body_name" }, message: "must have required property 'step_body_name'" };
          if (vErrors === null) {
            vErrors = [err49];
          } else {
            vErrors.push(err49);
          }
          errors++;
        }
        if (data16.color !== void 0) {
          let data17 = data16.color;
          const _errs77 = errors;
          let valid23 = false;
          const _errs78 = errors;
          if (typeof data17 !== "string") {
            const err50 = { instancePath: instancePath + "/regions/color", schemaPath: "#/$defs/FeatureStyle/properties/color/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err50];
            } else {
              vErrors.push(err50);
            }
            errors++;
          }
          var _valid8 = _errs78 === errors;
          valid23 = valid23 || _valid8;
          const _errs80 = errors;
          if (data17 !== null) {
            const err51 = { instancePath: instancePath + "/regions/color", schemaPath: "#/$defs/FeatureStyle/properties/color/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err51];
            } else {
              vErrors.push(err51);
            }
            errors++;
          }
          var _valid8 = _errs80 === errors;
          valid23 = valid23 || _valid8;
          if (!valid23) {
            const err52 = { instancePath: instancePath + "/regions/color", schemaPath: "#/$defs/FeatureStyle/properties/color/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err52];
            } else {
              vErrors.push(err52);
            }
            errors++;
          } else {
            errors = _errs77;
            if (vErrors !== null) {
              if (_errs77) {
                vErrors.length = _errs77;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data16.step_body_name !== void 0) {
          let data18 = data16.step_body_name;
          const _errs83 = errors;
          let valid24 = false;
          const _errs84 = errors;
          if (typeof data18 !== "string") {
            const err53 = { instancePath: instancePath + "/regions/step_body_name", schemaPath: "#/$defs/FeatureStyle/properties/step_body_name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err53];
            } else {
              vErrors.push(err53);
            }
            errors++;
          }
          var _valid9 = _errs84 === errors;
          valid24 = valid24 || _valid9;
          const _errs86 = errors;
          if (data18 !== null) {
            const err54 = { instancePath: instancePath + "/regions/step_body_name", schemaPath: "#/$defs/FeatureStyle/properties/step_body_name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err54];
            } else {
              vErrors.push(err54);
            }
            errors++;
          }
          var _valid9 = _errs86 === errors;
          valid24 = valid24 || _valid9;
          if (!valid24) {
            const err55 = { instancePath: instancePath + "/regions/step_body_name", schemaPath: "#/$defs/FeatureStyle/properties/step_body_name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err55];
            } else {
              vErrors.push(err55);
            }
            errors++;
          } else {
            errors = _errs83;
            if (vErrors !== null) {
              if (_errs83) {
                vErrors.length = _errs83;
              } else {
                vErrors = null;
              }
            }
          }
        }
        for (const key4 in data16) {
          if (key4 !== "color" && key4 !== "step_body_name") {
            const err56 = { instancePath: instancePath + "/regions/" + key4.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/FeatureStyle/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err56];
            } else {
              vErrors.push(err56);
            }
            errors++;
          }
        }
      } else {
        const err57 = { instancePath: instancePath + "/regions", schemaPath: "#/$defs/FeatureStyle/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err57];
        } else {
          vErrors.push(err57);
        }
        errors++;
      }
    }
    if (data.vias !== void 0) {
      let data20 = data.vias;
      if (data20 && typeof data20 == "object" && !Array.isArray(data20)) {
        if (data20.color === void 0) {
          const err58 = { instancePath: instancePath + "/vias", schemaPath: "#/$defs/FeatureStyle/required", keyword: "required", params: { missingProperty: "color" }, message: "must have required property 'color'" };
          if (vErrors === null) {
            vErrors = [err58];
          } else {
            vErrors.push(err58);
          }
          errors++;
        }
        if (data20.step_body_name === void 0) {
          const err59 = { instancePath: instancePath + "/vias", schemaPath: "#/$defs/FeatureStyle/required", keyword: "required", params: { missingProperty: "step_body_name" }, message: "must have required property 'step_body_name'" };
          if (vErrors === null) {
            vErrors = [err59];
          } else {
            vErrors.push(err59);
          }
          errors++;
        }
        if (data20.color !== void 0) {
          let data21 = data20.color;
          const _errs95 = errors;
          let valid28 = false;
          const _errs96 = errors;
          if (typeof data21 !== "string") {
            const err60 = { instancePath: instancePath + "/vias/color", schemaPath: "#/$defs/FeatureStyle/properties/color/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err60];
            } else {
              vErrors.push(err60);
            }
            errors++;
          }
          var _valid10 = _errs96 === errors;
          valid28 = valid28 || _valid10;
          const _errs98 = errors;
          if (data21 !== null) {
            const err61 = { instancePath: instancePath + "/vias/color", schemaPath: "#/$defs/FeatureStyle/properties/color/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err61];
            } else {
              vErrors.push(err61);
            }
            errors++;
          }
          var _valid10 = _errs98 === errors;
          valid28 = valid28 || _valid10;
          if (!valid28) {
            const err62 = { instancePath: instancePath + "/vias/color", schemaPath: "#/$defs/FeatureStyle/properties/color/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err62];
            } else {
              vErrors.push(err62);
            }
            errors++;
          } else {
            errors = _errs95;
            if (vErrors !== null) {
              if (_errs95) {
                vErrors.length = _errs95;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data20.step_body_name !== void 0) {
          let data22 = data20.step_body_name;
          const _errs101 = errors;
          let valid29 = false;
          const _errs102 = errors;
          if (typeof data22 !== "string") {
            const err63 = { instancePath: instancePath + "/vias/step_body_name", schemaPath: "#/$defs/FeatureStyle/properties/step_body_name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err63];
            } else {
              vErrors.push(err63);
            }
            errors++;
          }
          var _valid11 = _errs102 === errors;
          valid29 = valid29 || _valid11;
          const _errs104 = errors;
          if (data22 !== null) {
            const err64 = { instancePath: instancePath + "/vias/step_body_name", schemaPath: "#/$defs/FeatureStyle/properties/step_body_name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err64];
            } else {
              vErrors.push(err64);
            }
            errors++;
          }
          var _valid11 = _errs104 === errors;
          valid29 = valid29 || _valid11;
          if (!valid29) {
            const err65 = { instancePath: instancePath + "/vias/step_body_name", schemaPath: "#/$defs/FeatureStyle/properties/step_body_name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err65];
            } else {
              vErrors.push(err65);
            }
            errors++;
          } else {
            errors = _errs101;
            if (vErrors !== null) {
              if (_errs101) {
                vErrors.length = _errs101;
              } else {
                vErrors = null;
              }
            }
          }
        }
        for (const key5 in data20) {
          if (key5 !== "color" && key5 !== "step_body_name") {
            const err66 = { instancePath: instancePath + "/vias/" + key5.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/FeatureStyle/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err66];
            } else {
              vErrors.push(err66);
            }
            errors++;
          }
        }
      } else {
        const err67 = { instancePath: instancePath + "/vias", schemaPath: "#/$defs/FeatureStyle/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err67];
        } else {
          vErrors.push(err67);
        }
        errors++;
      }
    }
    if (data.component_pads !== void 0) {
      let data24 = data.component_pads;
      if (data24 && typeof data24 == "object" && !Array.isArray(data24)) {
        if (data24.color === void 0) {
          const err68 = { instancePath: instancePath + "/component_pads", schemaPath: "#/$defs/FeatureStyle/required", keyword: "required", params: { missingProperty: "color" }, message: "must have required property 'color'" };
          if (vErrors === null) {
            vErrors = [err68];
          } else {
            vErrors.push(err68);
          }
          errors++;
        }
        if (data24.step_body_name === void 0) {
          const err69 = { instancePath: instancePath + "/component_pads", schemaPath: "#/$defs/FeatureStyle/required", keyword: "required", params: { missingProperty: "step_body_name" }, message: "must have required property 'step_body_name'" };
          if (vErrors === null) {
            vErrors = [err69];
          } else {
            vErrors.push(err69);
          }
          errors++;
        }
        if (data24.color !== void 0) {
          let data25 = data24.color;
          const _errs113 = errors;
          let valid33 = false;
          const _errs114 = errors;
          if (typeof data25 !== "string") {
            const err70 = { instancePath: instancePath + "/component_pads/color", schemaPath: "#/$defs/FeatureStyle/properties/color/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err70];
            } else {
              vErrors.push(err70);
            }
            errors++;
          }
          var _valid12 = _errs114 === errors;
          valid33 = valid33 || _valid12;
          const _errs116 = errors;
          if (data25 !== null) {
            const err71 = { instancePath: instancePath + "/component_pads/color", schemaPath: "#/$defs/FeatureStyle/properties/color/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err71];
            } else {
              vErrors.push(err71);
            }
            errors++;
          }
          var _valid12 = _errs116 === errors;
          valid33 = valid33 || _valid12;
          if (!valid33) {
            const err72 = { instancePath: instancePath + "/component_pads/color", schemaPath: "#/$defs/FeatureStyle/properties/color/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err72];
            } else {
              vErrors.push(err72);
            }
            errors++;
          } else {
            errors = _errs113;
            if (vErrors !== null) {
              if (_errs113) {
                vErrors.length = _errs113;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data24.step_body_name !== void 0) {
          let data26 = data24.step_body_name;
          const _errs119 = errors;
          let valid34 = false;
          const _errs120 = errors;
          if (typeof data26 !== "string") {
            const err73 = { instancePath: instancePath + "/component_pads/step_body_name", schemaPath: "#/$defs/FeatureStyle/properties/step_body_name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err73];
            } else {
              vErrors.push(err73);
            }
            errors++;
          }
          var _valid13 = _errs120 === errors;
          valid34 = valid34 || _valid13;
          const _errs122 = errors;
          if (data26 !== null) {
            const err74 = { instancePath: instancePath + "/component_pads/step_body_name", schemaPath: "#/$defs/FeatureStyle/properties/step_body_name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err74];
            } else {
              vErrors.push(err74);
            }
            errors++;
          }
          var _valid13 = _errs122 === errors;
          valid34 = valid34 || _valid13;
          if (!valid34) {
            const err75 = { instancePath: instancePath + "/component_pads/step_body_name", schemaPath: "#/$defs/FeatureStyle/properties/step_body_name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err75];
            } else {
              vErrors.push(err75);
            }
            errors++;
          } else {
            errors = _errs119;
            if (vErrors !== null) {
              if (_errs119) {
                vErrors.length = _errs119;
              } else {
                vErrors = null;
              }
            }
          }
        }
        for (const key6 in data24) {
          if (key6 !== "color" && key6 !== "step_body_name") {
            const err76 = { instancePath: instancePath + "/component_pads/" + key6.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/FeatureStyle/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err76];
            } else {
              vErrors.push(err76);
            }
            errors++;
          }
        }
      } else {
        const err77 = { instancePath: instancePath + "/component_pads", schemaPath: "#/$defs/FeatureStyle/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err77];
        } else {
          vErrors.push(err77);
        }
        errors++;
      }
    }
    if (data.free_pads !== void 0) {
      let data28 = data.free_pads;
      if (data28 && typeof data28 == "object" && !Array.isArray(data28)) {
        if (data28.color === void 0) {
          const err78 = { instancePath: instancePath + "/free_pads", schemaPath: "#/$defs/FeatureStyle/required", keyword: "required", params: { missingProperty: "color" }, message: "must have required property 'color'" };
          if (vErrors === null) {
            vErrors = [err78];
          } else {
            vErrors.push(err78);
          }
          errors++;
        }
        if (data28.step_body_name === void 0) {
          const err79 = { instancePath: instancePath + "/free_pads", schemaPath: "#/$defs/FeatureStyle/required", keyword: "required", params: { missingProperty: "step_body_name" }, message: "must have required property 'step_body_name'" };
          if (vErrors === null) {
            vErrors = [err79];
          } else {
            vErrors.push(err79);
          }
          errors++;
        }
        if (data28.color !== void 0) {
          let data29 = data28.color;
          const _errs131 = errors;
          let valid38 = false;
          const _errs132 = errors;
          if (typeof data29 !== "string") {
            const err80 = { instancePath: instancePath + "/free_pads/color", schemaPath: "#/$defs/FeatureStyle/properties/color/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err80];
            } else {
              vErrors.push(err80);
            }
            errors++;
          }
          var _valid14 = _errs132 === errors;
          valid38 = valid38 || _valid14;
          const _errs134 = errors;
          if (data29 !== null) {
            const err81 = { instancePath: instancePath + "/free_pads/color", schemaPath: "#/$defs/FeatureStyle/properties/color/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err81];
            } else {
              vErrors.push(err81);
            }
            errors++;
          }
          var _valid14 = _errs134 === errors;
          valid38 = valid38 || _valid14;
          if (!valid38) {
            const err82 = { instancePath: instancePath + "/free_pads/color", schemaPath: "#/$defs/FeatureStyle/properties/color/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err82];
            } else {
              vErrors.push(err82);
            }
            errors++;
          } else {
            errors = _errs131;
            if (vErrors !== null) {
              if (_errs131) {
                vErrors.length = _errs131;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data28.step_body_name !== void 0) {
          let data30 = data28.step_body_name;
          const _errs137 = errors;
          let valid39 = false;
          const _errs138 = errors;
          if (typeof data30 !== "string") {
            const err83 = { instancePath: instancePath + "/free_pads/step_body_name", schemaPath: "#/$defs/FeatureStyle/properties/step_body_name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err83];
            } else {
              vErrors.push(err83);
            }
            errors++;
          }
          var _valid15 = _errs138 === errors;
          valid39 = valid39 || _valid15;
          const _errs140 = errors;
          if (data30 !== null) {
            const err84 = { instancePath: instancePath + "/free_pads/step_body_name", schemaPath: "#/$defs/FeatureStyle/properties/step_body_name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err84];
            } else {
              vErrors.push(err84);
            }
            errors++;
          }
          var _valid15 = _errs140 === errors;
          valid39 = valid39 || _valid15;
          if (!valid39) {
            const err85 = { instancePath: instancePath + "/free_pads/step_body_name", schemaPath: "#/$defs/FeatureStyle/properties/step_body_name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err85];
            } else {
              vErrors.push(err85);
            }
            errors++;
          } else {
            errors = _errs137;
            if (vErrors !== null) {
              if (_errs137) {
                vErrors.length = _errs137;
              } else {
                vErrors = null;
              }
            }
          }
        }
        for (const key7 in data28) {
          if (key7 !== "color" && key7 !== "step_body_name") {
            const err86 = { instancePath: instancePath + "/free_pads/" + key7.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/FeatureStyle/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err86];
            } else {
              vErrors.push(err86);
            }
            errors++;
          }
        }
      } else {
        const err87 = { instancePath: instancePath + "/free_pads", schemaPath: "#/$defs/FeatureStyle/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err87];
        } else {
          vErrors.push(err87);
        }
        errors++;
      }
    }
    for (const key8 in data) {
      if (key8 !== "tracks" && key8 !== "arcs" && key8 !== "fills" && key8 !== "polygons" && key8 !== "regions" && key8 !== "vias" && key8 !== "component_pads" && key8 !== "free_pads") {
        const err88 = { instancePath: instancePath + "/" + key8.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err88];
        } else {
          vErrors.push(err88);
        }
        errors++;
      }
    }
  } else {
    const err89 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err89];
    } else {
      vErrors.push(err89);
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
    if (data.thickness_mm === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "thickness_mm" }, message: "must have required property 'thickness_mm'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.z_mm === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "z_mm" }, message: "must have required property 'z_mm'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.copper_color === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "copper_color" }, message: "must have required property 'copper_color'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.outline_width_mm === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "outline_width_mm" }, message: "must have required property 'outline_width_mm'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.outline_color === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "outline_color" }, message: "must have required property 'outline_color'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.board_cutout_color === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "board_cutout_color" }, message: "must have required property 'board_cutout_color'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.include_copper === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "include_copper" }, message: "must have required property 'include_copper'" };
      if (vErrors === null) {
        vErrors = [err6];
      } else {
        vErrors.push(err6);
      }
      errors++;
    }
    if (data.include_board_outline === void 0) {
      const err7 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "include_board_outline" }, message: "must have required property 'include_board_outline'" };
      if (vErrors === null) {
        vErrors = [err7];
      } else {
        vErrors.push(err7);
      }
      errors++;
    }
    if (data.include_board_cutouts === void 0) {
      const err8 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "include_board_cutouts" }, message: "must have required property 'include_board_cutouts'" };
      if (vErrors === null) {
        vErrors = [err8];
      } else {
        vErrors.push(err8);
      }
      errors++;
    }
    if (data.include_poured_polygons === void 0) {
      const err9 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "include_poured_polygons" }, message: "must have required property 'include_poured_polygons'" };
      if (vErrors === null) {
        vErrors = [err9];
      } else {
        vErrors.push(err9);
      }
      errors++;
    }
    if (data.cut_holes === void 0) {
      const err10 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "cut_holes" }, message: "must have required property 'cut_holes'" };
      if (vErrors === null) {
        vErrors = [err10];
      } else {
        vErrors.push(err10);
      }
      errors++;
    }
    if (data.drill_hole_mode === void 0) {
      const err11 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "drill_hole_mode" }, message: "must have required property 'drill_hole_mode'" };
      if (vErrors === null) {
        vErrors = [err11];
      } else {
        vErrors.push(err11);
      }
      errors++;
    }
    if (data.effective_drill_hole_mode === void 0) {
      const err12 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "effective_drill_hole_mode" }, message: "must have required property 'effective_drill_hole_mode'" };
      if (vErrors === null) {
        vErrors = [err12];
      } else {
        vErrors.push(err12);
      }
      errors++;
    }
    if (data.max_boolean_drill_cuts === void 0) {
      const err13 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "max_boolean_drill_cuts" }, message: "must have required property 'max_boolean_drill_cuts'" };
      if (vErrors === null) {
        vErrors = [err13];
      } else {
        vErrors.push(err13);
      }
      errors++;
    }
    if (data.drill_hole_color === void 0) {
      const err14 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "drill_hole_color" }, message: "must have required property 'drill_hole_color'" };
      if (vErrors === null) {
        vErrors = [err14];
      } else {
        vErrors.push(err14);
      }
      errors++;
    }
    if (data.drill_plated_hole_color === void 0) {
      const err15 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "drill_plated_hole_color" }, message: "must have required property 'drill_plated_hole_color'" };
      if (vErrors === null) {
        vErrors = [err15];
      } else {
        vErrors.push(err15);
      }
      errors++;
    }
    if (data.drill_non_plated_hole_color === void 0) {
      const err16 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "drill_non_plated_hole_color" }, message: "must have required property 'drill_non_plated_hole_color'" };
      if (vErrors === null) {
        vErrors = [err16];
      } else {
        vErrors.push(err16);
      }
      errors++;
    }
    if (data.drill_overlay_thickness_mm === void 0) {
      const err17 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "drill_overlay_thickness_mm" }, message: "must have required property 'drill_overlay_thickness_mm'" };
      if (vErrors === null) {
        vErrors = [err17];
      } else {
        vErrors.push(err17);
      }
      errors++;
    }
    if (data.drill_minimum_diameter_mm === void 0) {
      const err18 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "drill_minimum_diameter_mm" }, message: "must have required property 'drill_minimum_diameter_mm'" };
      if (vErrors === null) {
        vErrors = [err18];
      } else {
        vErrors.push(err18);
      }
      errors++;
    }
    if (data.drill_hole_shape === void 0) {
      const err19 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "drill_hole_shape" }, message: "must have required property 'drill_hole_shape'" };
      if (vErrors === null) {
        vErrors = [err19];
      } else {
        vErrors.push(err19);
      }
      errors++;
    }
    if (data.drill_ring_width_mm === void 0) {
      const err20 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "drill_ring_width_mm" }, message: "must have required property 'drill_ring_width_mm'" };
      if (vErrors === null) {
        vErrors = [err20];
      } else {
        vErrors.push(err20);
      }
      errors++;
    }
    if (data.drill_plated_ring_shape === void 0) {
      const err21 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "drill_plated_ring_shape" }, message: "must have required property 'drill_plated_ring_shape'" };
      if (vErrors === null) {
        vErrors = [err21];
      } else {
        vErrors.push(err21);
      }
      errors++;
    }
    if (data.drill_selected_component_mode === void 0) {
      const err22 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "drill_selected_component_mode" }, message: "must have required property 'drill_selected_component_mode'" };
      if (vErrors === null) {
        vErrors = [err22];
      } else {
        vErrors.push(err22);
      }
      errors++;
    }
    if (data.drill_other_component_mode === void 0) {
      const err23 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "drill_other_component_mode" }, message: "must have required property 'drill_other_component_mode'" };
      if (vErrors === null) {
        vErrors = [err23];
      } else {
        vErrors.push(err23);
      }
      errors++;
    }
    if (data.drill_free_pad_mode === void 0) {
      const err24 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "drill_free_pad_mode" }, message: "must have required property 'drill_free_pad_mode'" };
      if (vErrors === null) {
        vErrors = [err24];
      } else {
        vErrors.push(err24);
      }
      errors++;
    }
    if (data.drill_via_mode === void 0) {
      const err25 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "drill_via_mode" }, message: "must have required property 'drill_via_mode'" };
      if (vErrors === null) {
        vErrors = [err25];
      } else {
        vErrors.push(err25);
      }
      errors++;
    }
    if (data.fuse_copper === void 0) {
      const err26 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "fuse_copper" }, message: "must have required property 'fuse_copper'" };
      if (vErrors === null) {
        vErrors = [err26];
      } else {
        vErrors.push(err26);
      }
      errors++;
    }
    if (data.fuse_board_outline === void 0) {
      const err27 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "fuse_board_outline" }, message: "must have required property 'fuse_board_outline'" };
      if (vErrors === null) {
        vErrors = [err27];
      } else {
        vErrors.push(err27);
      }
      errors++;
    }
    if (data.arc_segments === void 0) {
      const err28 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "arc_segments" }, message: "must have required property 'arc_segments'" };
      if (vErrors === null) {
        vErrors = [err28];
      } else {
        vErrors.push(err28);
      }
      errors++;
    }
    if (data.features === void 0) {
      const err29 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "features" }, message: "must have required property 'features'" };
      if (vErrors === null) {
        vErrors = [err29];
      } else {
        vErrors.push(err29);
      }
      errors++;
    }
    if (data.pad_color_rules === void 0) {
      const err30 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "pad_color_rules" }, message: "must have required property 'pad_color_rules'" };
      if (vErrors === null) {
        vErrors = [err30];
      } else {
        vErrors.push(err30);
      }
      errors++;
    }
    if (data.feature_color_rules === void 0) {
      const err31 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "feature_color_rules" }, message: "must have required property 'feature_color_rules'" };
      if (vErrors === null) {
        vErrors = [err31];
      } else {
        vErrors.push(err31);
      }
      errors++;
    }
    if (data.thickness_bias_mm === void 0) {
      const err32 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "thickness_bias_mm" }, message: "must have required property 'thickness_bias_mm'" };
      if (vErrors === null) {
        vErrors = [err32];
      } else {
        vErrors.push(err32);
      }
      errors++;
    }
    if (data.highlight_count === void 0) {
      const err33 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "highlight_count" }, message: "must have required property 'highlight_count'" };
      if (vErrors === null) {
        vErrors = [err33];
      } else {
        vErrors.push(err33);
      }
      errors++;
    }
    if (data.thickness_mm !== void 0) {
      if (!(typeof data.thickness_mm == "number")) {
        const err34 = { instancePath: instancePath + "/thickness_mm", schemaPath: "#/properties/thickness_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
        }
        errors++;
      }
    }
    if (data.z_mm !== void 0) {
      if (!(typeof data.z_mm == "number")) {
        const err35 = { instancePath: instancePath + "/z_mm", schemaPath: "#/properties/z_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err35];
        } else {
          vErrors.push(err35);
        }
        errors++;
      }
    }
    if (data.copper_color !== void 0) {
      if (typeof data.copper_color !== "string") {
        const err36 = { instancePath: instancePath + "/copper_color", schemaPath: "#/properties/copper_color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err36];
        } else {
          vErrors.push(err36);
        }
        errors++;
      }
    }
    if (data.outline_width_mm !== void 0) {
      if (!(typeof data.outline_width_mm == "number")) {
        const err37 = { instancePath: instancePath + "/outline_width_mm", schemaPath: "#/properties/outline_width_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err37];
        } else {
          vErrors.push(err37);
        }
        errors++;
      }
    }
    if (data.outline_color !== void 0) {
      if (typeof data.outline_color !== "string") {
        const err38 = { instancePath: instancePath + "/outline_color", schemaPath: "#/properties/outline_color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err38];
        } else {
          vErrors.push(err38);
        }
        errors++;
      }
    }
    if (data.board_cutout_color !== void 0) {
      if (typeof data.board_cutout_color !== "string") {
        const err39 = { instancePath: instancePath + "/board_cutout_color", schemaPath: "#/properties/board_cutout_color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err39];
        } else {
          vErrors.push(err39);
        }
        errors++;
      }
    }
    if (data.include_copper !== void 0) {
      if (typeof data.include_copper !== "boolean") {
        const err40 = { instancePath: instancePath + "/include_copper", schemaPath: "#/properties/include_copper/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err40];
        } else {
          vErrors.push(err40);
        }
        errors++;
      }
    }
    if (data.include_board_outline !== void 0) {
      if (typeof data.include_board_outline !== "boolean") {
        const err41 = { instancePath: instancePath + "/include_board_outline", schemaPath: "#/properties/include_board_outline/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err41];
        } else {
          vErrors.push(err41);
        }
        errors++;
      }
    }
    if (data.include_board_cutouts !== void 0) {
      if (typeof data.include_board_cutouts !== "boolean") {
        const err42 = { instancePath: instancePath + "/include_board_cutouts", schemaPath: "#/properties/include_board_cutouts/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err42];
        } else {
          vErrors.push(err42);
        }
        errors++;
      }
    }
    if (data.include_poured_polygons !== void 0) {
      if (typeof data.include_poured_polygons !== "boolean") {
        const err43 = { instancePath: instancePath + "/include_poured_polygons", schemaPath: "#/properties/include_poured_polygons/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err43];
        } else {
          vErrors.push(err43);
        }
        errors++;
      }
    }
    if (data.cut_holes !== void 0) {
      if (typeof data.cut_holes !== "boolean") {
        const err44 = { instancePath: instancePath + "/cut_holes", schemaPath: "#/properties/cut_holes/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err44];
        } else {
          vErrors.push(err44);
        }
        errors++;
      }
    }
    if (data.drill_hole_mode !== void 0) {
      if (typeof data.drill_hole_mode !== "string") {
        const err45 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/properties/drill_hole_mode/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err45];
        } else {
          vErrors.push(err45);
        }
        errors++;
      }
    }
    if (data.effective_drill_hole_mode !== void 0) {
      if (typeof data.effective_drill_hole_mode !== "string") {
        const err46 = { instancePath: instancePath + "/effective_drill_hole_mode", schemaPath: "#/properties/effective_drill_hole_mode/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err46];
        } else {
          vErrors.push(err46);
        }
        errors++;
      }
    }
    if (data.max_boolean_drill_cuts !== void 0) {
      let data13 = data.max_boolean_drill_cuts;
      if (!(typeof data13 == "number" && (!(data13 % 1) && !isNaN(data13)))) {
        const err47 = { instancePath: instancePath + "/max_boolean_drill_cuts", schemaPath: "#/properties/max_boolean_drill_cuts/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err47];
        } else {
          vErrors.push(err47);
        }
        errors++;
      }
    }
    if (data.drill_hole_color !== void 0) {
      if (typeof data.drill_hole_color !== "string") {
        const err48 = { instancePath: instancePath + "/drill_hole_color", schemaPath: "#/properties/drill_hole_color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err48];
        } else {
          vErrors.push(err48);
        }
        errors++;
      }
    }
    if (data.drill_plated_hole_color !== void 0) {
      if (typeof data.drill_plated_hole_color !== "string") {
        const err49 = { instancePath: instancePath + "/drill_plated_hole_color", schemaPath: "#/properties/drill_plated_hole_color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err49];
        } else {
          vErrors.push(err49);
        }
        errors++;
      }
    }
    if (data.drill_non_plated_hole_color !== void 0) {
      if (typeof data.drill_non_plated_hole_color !== "string") {
        const err50 = { instancePath: instancePath + "/drill_non_plated_hole_color", schemaPath: "#/properties/drill_non_plated_hole_color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err50];
        } else {
          vErrors.push(err50);
        }
        errors++;
      }
    }
    if (data.drill_overlay_thickness_mm !== void 0) {
      if (!(typeof data.drill_overlay_thickness_mm == "number")) {
        const err51 = { instancePath: instancePath + "/drill_overlay_thickness_mm", schemaPath: "#/properties/drill_overlay_thickness_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err51];
        } else {
          vErrors.push(err51);
        }
        errors++;
      }
    }
    if (data.drill_minimum_diameter_mm !== void 0) {
      if (!(typeof data.drill_minimum_diameter_mm == "number")) {
        const err52 = { instancePath: instancePath + "/drill_minimum_diameter_mm", schemaPath: "#/properties/drill_minimum_diameter_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err52];
        } else {
          vErrors.push(err52);
        }
        errors++;
      }
    }
    if (data.drill_hole_shape !== void 0) {
      if (typeof data.drill_hole_shape !== "string") {
        const err53 = { instancePath: instancePath + "/drill_hole_shape", schemaPath: "#/properties/drill_hole_shape/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err53];
        } else {
          vErrors.push(err53);
        }
        errors++;
      }
    }
    if (data.drill_ring_width_mm !== void 0) {
      if (!(typeof data.drill_ring_width_mm == "number")) {
        const err54 = { instancePath: instancePath + "/drill_ring_width_mm", schemaPath: "#/properties/drill_ring_width_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err54];
        } else {
          vErrors.push(err54);
        }
        errors++;
      }
    }
    if (data.drill_plated_ring_shape !== void 0) {
      if (typeof data.drill_plated_ring_shape !== "string") {
        const err55 = { instancePath: instancePath + "/drill_plated_ring_shape", schemaPath: "#/properties/drill_plated_ring_shape/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err55];
        } else {
          vErrors.push(err55);
        }
        errors++;
      }
    }
    if (data.drill_selected_component_mode !== void 0) {
      if (typeof data.drill_selected_component_mode !== "string") {
        const err56 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/properties/drill_selected_component_mode/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err56];
        } else {
          vErrors.push(err56);
        }
        errors++;
      }
    }
    if (data.drill_other_component_mode !== void 0) {
      if (typeof data.drill_other_component_mode !== "string") {
        const err57 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/properties/drill_other_component_mode/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err57];
        } else {
          vErrors.push(err57);
        }
        errors++;
      }
    }
    if (data.drill_free_pad_mode !== void 0) {
      if (typeof data.drill_free_pad_mode !== "string") {
        const err58 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/properties/drill_free_pad_mode/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err58];
        } else {
          vErrors.push(err58);
        }
        errors++;
      }
    }
    if (data.drill_via_mode !== void 0) {
      if (typeof data.drill_via_mode !== "string") {
        const err59 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/properties/drill_via_mode/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err59];
        } else {
          vErrors.push(err59);
        }
        errors++;
      }
    }
    if (data.fuse_copper !== void 0) {
      if (typeof data.fuse_copper !== "boolean") {
        const err60 = { instancePath: instancePath + "/fuse_copper", schemaPath: "#/properties/fuse_copper/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err60];
        } else {
          vErrors.push(err60);
        }
        errors++;
      }
    }
    if (data.fuse_board_outline !== void 0) {
      if (typeof data.fuse_board_outline !== "boolean") {
        const err61 = { instancePath: instancePath + "/fuse_board_outline", schemaPath: "#/properties/fuse_board_outline/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err61];
        } else {
          vErrors.push(err61);
        }
        errors++;
      }
    }
    if (data.arc_segments !== void 0) {
      let data28 = data.arc_segments;
      if (!(typeof data28 == "number" && (!(data28 % 1) && !isNaN(data28)))) {
        const err62 = { instancePath: instancePath + "/arc_segments", schemaPath: "#/properties/arc_segments/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err62];
        } else {
          vErrors.push(err62);
        }
        errors++;
      }
    }
    if (data.features !== void 0) {
      let data29 = data.features;
      if (data29 && typeof data29 == "object" && !Array.isArray(data29)) {
        if (data29.tracks === void 0) {
          const err63 = { instancePath: instancePath + "/features", schemaPath: "#/$defs/FeatureSwitches/required", keyword: "required", params: { missingProperty: "tracks" }, message: "must have required property 'tracks'" };
          if (vErrors === null) {
            vErrors = [err63];
          } else {
            vErrors.push(err63);
          }
          errors++;
        }
        if (data29.arcs === void 0) {
          const err64 = { instancePath: instancePath + "/features", schemaPath: "#/$defs/FeatureSwitches/required", keyword: "required", params: { missingProperty: "arcs" }, message: "must have required property 'arcs'" };
          if (vErrors === null) {
            vErrors = [err64];
          } else {
            vErrors.push(err64);
          }
          errors++;
        }
        if (data29.fills === void 0) {
          const err65 = { instancePath: instancePath + "/features", schemaPath: "#/$defs/FeatureSwitches/required", keyword: "required", params: { missingProperty: "fills" }, message: "must have required property 'fills'" };
          if (vErrors === null) {
            vErrors = [err65];
          } else {
            vErrors.push(err65);
          }
          errors++;
        }
        if (data29.polygons === void 0) {
          const err66 = { instancePath: instancePath + "/features", schemaPath: "#/$defs/FeatureSwitches/required", keyword: "required", params: { missingProperty: "polygons" }, message: "must have required property 'polygons'" };
          if (vErrors === null) {
            vErrors = [err66];
          } else {
            vErrors.push(err66);
          }
          errors++;
        }
        if (data29.regions === void 0) {
          const err67 = { instancePath: instancePath + "/features", schemaPath: "#/$defs/FeatureSwitches/required", keyword: "required", params: { missingProperty: "regions" }, message: "must have required property 'regions'" };
          if (vErrors === null) {
            vErrors = [err67];
          } else {
            vErrors.push(err67);
          }
          errors++;
        }
        if (data29.vias === void 0) {
          const err68 = { instancePath: instancePath + "/features", schemaPath: "#/$defs/FeatureSwitches/required", keyword: "required", params: { missingProperty: "vias" }, message: "must have required property 'vias'" };
          if (vErrors === null) {
            vErrors = [err68];
          } else {
            vErrors.push(err68);
          }
          errors++;
        }
        if (data29.component_pads === void 0) {
          const err69 = { instancePath: instancePath + "/features", schemaPath: "#/$defs/FeatureSwitches/required", keyword: "required", params: { missingProperty: "component_pads" }, message: "must have required property 'component_pads'" };
          if (vErrors === null) {
            vErrors = [err69];
          } else {
            vErrors.push(err69);
          }
          errors++;
        }
        if (data29.free_pads === void 0) {
          const err70 = { instancePath: instancePath + "/features", schemaPath: "#/$defs/FeatureSwitches/required", keyword: "required", params: { missingProperty: "free_pads" }, message: "must have required property 'free_pads'" };
          if (vErrors === null) {
            vErrors = [err70];
          } else {
            vErrors.push(err70);
          }
          errors++;
        }
        if (data29.include_designators === void 0) {
          const err71 = { instancePath: instancePath + "/features", schemaPath: "#/$defs/FeatureSwitches/required", keyword: "required", params: { missingProperty: "include_designators" }, message: "must have required property 'include_designators'" };
          if (vErrors === null) {
            vErrors = [err71];
          } else {
            vErrors.push(err71);
          }
          errors++;
        }
        if (data29.tracks !== void 0) {
          if (typeof data29.tracks !== "boolean") {
            const err72 = { instancePath: instancePath + "/features/tracks", schemaPath: "#/$defs/FeatureSwitches/properties/tracks/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err72];
            } else {
              vErrors.push(err72);
            }
            errors++;
          }
        }
        if (data29.arcs !== void 0) {
          if (typeof data29.arcs !== "boolean") {
            const err73 = { instancePath: instancePath + "/features/arcs", schemaPath: "#/$defs/FeatureSwitches/properties/arcs/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err73];
            } else {
              vErrors.push(err73);
            }
            errors++;
          }
        }
        if (data29.fills !== void 0) {
          if (typeof data29.fills !== "boolean") {
            const err74 = { instancePath: instancePath + "/features/fills", schemaPath: "#/$defs/FeatureSwitches/properties/fills/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err74];
            } else {
              vErrors.push(err74);
            }
            errors++;
          }
        }
        if (data29.polygons !== void 0) {
          if (typeof data29.polygons !== "boolean") {
            const err75 = { instancePath: instancePath + "/features/polygons", schemaPath: "#/$defs/FeatureSwitches/properties/polygons/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err75];
            } else {
              vErrors.push(err75);
            }
            errors++;
          }
        }
        if (data29.regions !== void 0) {
          if (typeof data29.regions !== "boolean") {
            const err76 = { instancePath: instancePath + "/features/regions", schemaPath: "#/$defs/FeatureSwitches/properties/regions/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err76];
            } else {
              vErrors.push(err76);
            }
            errors++;
          }
        }
        if (data29.vias !== void 0) {
          if (typeof data29.vias !== "boolean") {
            const err77 = { instancePath: instancePath + "/features/vias", schemaPath: "#/$defs/FeatureSwitches/properties/vias/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err77];
            } else {
              vErrors.push(err77);
            }
            errors++;
          }
        }
        if (data29.component_pads !== void 0) {
          if (typeof data29.component_pads !== "boolean") {
            const err78 = { instancePath: instancePath + "/features/component_pads", schemaPath: "#/$defs/FeatureSwitches/properties/component_pads/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err78];
            } else {
              vErrors.push(err78);
            }
            errors++;
          }
        }
        if (data29.free_pads !== void 0) {
          if (typeof data29.free_pads !== "boolean") {
            const err79 = { instancePath: instancePath + "/features/free_pads", schemaPath: "#/$defs/FeatureSwitches/properties/free_pads/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err79];
            } else {
              vErrors.push(err79);
            }
            errors++;
          }
        }
        if (data29.include_designators !== void 0) {
          let data38 = data29.include_designators;
          if (Array.isArray(data38)) {
            const len0 = data38.length;
            for (let i0 = 0; i0 < len0; i0++) {
              if (typeof data38[i0] !== "string") {
                const err80 = { instancePath: instancePath + "/features/include_designators/" + i0, schemaPath: "#/$defs/FeatureSwitches/properties/include_designators/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err80];
                } else {
                  vErrors.push(err80);
                }
                errors++;
              }
            }
          } else {
            const err81 = { instancePath: instancePath + "/features/include_designators", schemaPath: "#/$defs/FeatureSwitches/properties/include_designators/type", keyword: "type", params: { type: "array" }, message: "must be array" };
            if (vErrors === null) {
              vErrors = [err81];
            } else {
              vErrors.push(err81);
            }
            errors++;
          }
        }
        for (const key0 in data29) {
          if (key0 !== "tracks" && key0 !== "arcs" && key0 !== "fills" && key0 !== "polygons" && key0 !== "regions" && key0 !== "vias" && key0 !== "component_pads" && key0 !== "free_pads" && key0 !== "include_designators") {
            const err82 = { instancePath: instancePath + "/features/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/FeatureSwitches/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err82];
            } else {
              vErrors.push(err82);
            }
            errors++;
          }
        }
      } else {
        const err83 = { instancePath: instancePath + "/features", schemaPath: "#/$defs/FeatureSwitches/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err83];
        } else {
          vErrors.push(err83);
        }
        errors++;
      }
    }
    if (data.pad_color_rules !== void 0) {
      let data41 = data.pad_color_rules;
      if (Array.isArray(data41)) {
        const len1 = data41.length;
        for (let i1 = 0; i1 < len1; i1++) {
          let data42 = data41[i1];
          if (data42 && typeof data42 == "object" && !Array.isArray(data42)) {
            if (data42.designators === void 0) {
              const err84 = { instancePath: instancePath + "/pad_color_rules/" + i1, schemaPath: "#/$defs/PadColorRule/required", keyword: "required", params: { missingProperty: "designators" }, message: "must have required property 'designators'" };
              if (vErrors === null) {
                vErrors = [err84];
              } else {
                vErrors.push(err84);
              }
              errors++;
            }
            if (data42.color === void 0) {
              const err85 = { instancePath: instancePath + "/pad_color_rules/" + i1, schemaPath: "#/$defs/PadColorRule/required", keyword: "required", params: { missingProperty: "color" }, message: "must have required property 'color'" };
              if (vErrors === null) {
                vErrors = [err85];
              } else {
                vErrors.push(err85);
              }
              errors++;
            }
            if (data42.step_body_name === void 0) {
              const err86 = { instancePath: instancePath + "/pad_color_rules/" + i1, schemaPath: "#/$defs/PadColorRule/required", keyword: "required", params: { missingProperty: "step_body_name" }, message: "must have required property 'step_body_name'" };
              if (vErrors === null) {
                vErrors = [err86];
              } else {
                vErrors.push(err86);
              }
              errors++;
            }
            if (data42.designators !== void 0) {
              let data43 = data42.designators;
              if (Array.isArray(data43)) {
                const len2 = data43.length;
                for (let i2 = 0; i2 < len2; i2++) {
                  if (typeof data43[i2] !== "string") {
                    const err87 = { instancePath: instancePath + "/pad_color_rules/" + i1 + "/designators/" + i2, schemaPath: "#/$defs/PadColorRule/properties/designators/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                    if (vErrors === null) {
                      vErrors = [err87];
                    } else {
                      vErrors.push(err87);
                    }
                    errors++;
                  }
                }
              } else {
                const err88 = { instancePath: instancePath + "/pad_color_rules/" + i1 + "/designators", schemaPath: "#/$defs/PadColorRule/properties/designators/type", keyword: "type", params: { type: "array" }, message: "must be array" };
                if (vErrors === null) {
                  vErrors = [err88];
                } else {
                  vErrors.push(err88);
                }
                errors++;
              }
            }
            if (data42.color !== void 0) {
              if (typeof data42.color !== "string") {
                const err89 = { instancePath: instancePath + "/pad_color_rules/" + i1 + "/color", schemaPath: "#/$defs/PadColorRule/properties/color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err89];
                } else {
                  vErrors.push(err89);
                }
                errors++;
              }
            }
            if (data42.step_body_name !== void 0) {
              let data46 = data42.step_body_name;
              const _errs97 = errors;
              let valid12 = false;
              const _errs98 = errors;
              if (typeof data46 !== "string") {
                const err90 = { instancePath: instancePath + "/pad_color_rules/" + i1 + "/step_body_name", schemaPath: "#/$defs/PadColorRule/properties/step_body_name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err90];
                } else {
                  vErrors.push(err90);
                }
                errors++;
              }
              var _valid0 = _errs98 === errors;
              valid12 = valid12 || _valid0;
              const _errs100 = errors;
              if (data46 !== null) {
                const err91 = { instancePath: instancePath + "/pad_color_rules/" + i1 + "/step_body_name", schemaPath: "#/$defs/PadColorRule/properties/step_body_name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
                if (vErrors === null) {
                  vErrors = [err91];
                } else {
                  vErrors.push(err91);
                }
                errors++;
              }
              var _valid0 = _errs100 === errors;
              valid12 = valid12 || _valid0;
              if (!valid12) {
                const err92 = { instancePath: instancePath + "/pad_color_rules/" + i1 + "/step_body_name", schemaPath: "#/$defs/PadColorRule/properties/step_body_name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err92];
                } else {
                  vErrors.push(err92);
                }
                errors++;
              } else {
                errors = _errs97;
                if (vErrors !== null) {
                  if (_errs97) {
                    vErrors.length = _errs97;
                  } else {
                    vErrors = null;
                  }
                }
              }
            }
            for (const key1 in data42) {
              if (key1 !== "designators" && key1 !== "color" && key1 !== "step_body_name") {
                const err93 = { instancePath: instancePath + "/pad_color_rules/" + i1 + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/PadColorRule/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err93];
                } else {
                  vErrors.push(err93);
                }
                errors++;
              }
            }
          } else {
            const err94 = { instancePath: instancePath + "/pad_color_rules/" + i1, schemaPath: "#/$defs/PadColorRule/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err94];
            } else {
              vErrors.push(err94);
            }
            errors++;
          }
        }
      } else {
        const err95 = { instancePath: instancePath + "/pad_color_rules", schemaPath: "#/properties/pad_color_rules/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err95];
        } else {
          vErrors.push(err95);
        }
        errors++;
      }
    }
    if (data.feature_color_rules !== void 0) {
      if (!validate24(data.feature_color_rules, { instancePath: instancePath + "/feature_color_rules", parentData: data, parentDataProperty: "feature_color_rules", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate24.errors : vErrors.concat(validate24.errors);
        errors = vErrors.length;
      }
    }
    if (data.thickness_bias_mm !== void 0) {
      let data49 = data.thickness_bias_mm;
      if (data49 && typeof data49 == "object" && !Array.isArray(data49)) {
        if (data49.tracks === void 0) {
          const err96 = { instancePath: instancePath + "/thickness_bias_mm", schemaPath: "#/$defs/ThicknessBias/required", keyword: "required", params: { missingProperty: "tracks" }, message: "must have required property 'tracks'" };
          if (vErrors === null) {
            vErrors = [err96];
          } else {
            vErrors.push(err96);
          }
          errors++;
        }
        if (data49.arcs === void 0) {
          const err97 = { instancePath: instancePath + "/thickness_bias_mm", schemaPath: "#/$defs/ThicknessBias/required", keyword: "required", params: { missingProperty: "arcs" }, message: "must have required property 'arcs'" };
          if (vErrors === null) {
            vErrors = [err97];
          } else {
            vErrors.push(err97);
          }
          errors++;
        }
        if (data49.fills === void 0) {
          const err98 = { instancePath: instancePath + "/thickness_bias_mm", schemaPath: "#/$defs/ThicknessBias/required", keyword: "required", params: { missingProperty: "fills" }, message: "must have required property 'fills'" };
          if (vErrors === null) {
            vErrors = [err98];
          } else {
            vErrors.push(err98);
          }
          errors++;
        }
        if (data49.polygons === void 0) {
          const err99 = { instancePath: instancePath + "/thickness_bias_mm", schemaPath: "#/$defs/ThicknessBias/required", keyword: "required", params: { missingProperty: "polygons" }, message: "must have required property 'polygons'" };
          if (vErrors === null) {
            vErrors = [err99];
          } else {
            vErrors.push(err99);
          }
          errors++;
        }
        if (data49.regions === void 0) {
          const err100 = { instancePath: instancePath + "/thickness_bias_mm", schemaPath: "#/$defs/ThicknessBias/required", keyword: "required", params: { missingProperty: "regions" }, message: "must have required property 'regions'" };
          if (vErrors === null) {
            vErrors = [err100];
          } else {
            vErrors.push(err100);
          }
          errors++;
        }
        if (data49.vias === void 0) {
          const err101 = { instancePath: instancePath + "/thickness_bias_mm", schemaPath: "#/$defs/ThicknessBias/required", keyword: "required", params: { missingProperty: "vias" }, message: "must have required property 'vias'" };
          if (vErrors === null) {
            vErrors = [err101];
          } else {
            vErrors.push(err101);
          }
          errors++;
        }
        if (data49.component_pads === void 0) {
          const err102 = { instancePath: instancePath + "/thickness_bias_mm", schemaPath: "#/$defs/ThicknessBias/required", keyword: "required", params: { missingProperty: "component_pads" }, message: "must have required property 'component_pads'" };
          if (vErrors === null) {
            vErrors = [err102];
          } else {
            vErrors.push(err102);
          }
          errors++;
        }
        if (data49.free_pads === void 0) {
          const err103 = { instancePath: instancePath + "/thickness_bias_mm", schemaPath: "#/$defs/ThicknessBias/required", keyword: "required", params: { missingProperty: "free_pads" }, message: "must have required property 'free_pads'" };
          if (vErrors === null) {
            vErrors = [err103];
          } else {
            vErrors.push(err103);
          }
          errors++;
        }
        if (data49.tracks !== void 0) {
          if (!(typeof data49.tracks == "number")) {
            const err104 = { instancePath: instancePath + "/thickness_bias_mm/tracks", schemaPath: "#/$defs/ThicknessBias/properties/tracks/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err104];
            } else {
              vErrors.push(err104);
            }
            errors++;
          }
        }
        if (data49.arcs !== void 0) {
          if (!(typeof data49.arcs == "number")) {
            const err105 = { instancePath: instancePath + "/thickness_bias_mm/arcs", schemaPath: "#/$defs/ThicknessBias/properties/arcs/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err105];
            } else {
              vErrors.push(err105);
            }
            errors++;
          }
        }
        if (data49.fills !== void 0) {
          if (!(typeof data49.fills == "number")) {
            const err106 = { instancePath: instancePath + "/thickness_bias_mm/fills", schemaPath: "#/$defs/ThicknessBias/properties/fills/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err106];
            } else {
              vErrors.push(err106);
            }
            errors++;
          }
        }
        if (data49.polygons !== void 0) {
          if (!(typeof data49.polygons == "number")) {
            const err107 = { instancePath: instancePath + "/thickness_bias_mm/polygons", schemaPath: "#/$defs/ThicknessBias/properties/polygons/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err107];
            } else {
              vErrors.push(err107);
            }
            errors++;
          }
        }
        if (data49.regions !== void 0) {
          if (!(typeof data49.regions == "number")) {
            const err108 = { instancePath: instancePath + "/thickness_bias_mm/regions", schemaPath: "#/$defs/ThicknessBias/properties/regions/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err108];
            } else {
              vErrors.push(err108);
            }
            errors++;
          }
        }
        if (data49.vias !== void 0) {
          if (!(typeof data49.vias == "number")) {
            const err109 = { instancePath: instancePath + "/thickness_bias_mm/vias", schemaPath: "#/$defs/ThicknessBias/properties/vias/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err109];
            } else {
              vErrors.push(err109);
            }
            errors++;
          }
        }
        if (data49.component_pads !== void 0) {
          if (!(typeof data49.component_pads == "number")) {
            const err110 = { instancePath: instancePath + "/thickness_bias_mm/component_pads", schemaPath: "#/$defs/ThicknessBias/properties/component_pads/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err110];
            } else {
              vErrors.push(err110);
            }
            errors++;
          }
        }
        if (data49.free_pads !== void 0) {
          if (!(typeof data49.free_pads == "number")) {
            const err111 = { instancePath: instancePath + "/thickness_bias_mm/free_pads", schemaPath: "#/$defs/ThicknessBias/properties/free_pads/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err111];
            } else {
              vErrors.push(err111);
            }
            errors++;
          }
        }
        for (const key2 in data49) {
          if (key2 !== "tracks" && key2 !== "arcs" && key2 !== "fills" && key2 !== "polygons" && key2 !== "regions" && key2 !== "vias" && key2 !== "component_pads" && key2 !== "free_pads") {
            const err112 = { instancePath: instancePath + "/thickness_bias_mm/" + key2.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/ThicknessBias/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err112];
            } else {
              vErrors.push(err112);
            }
            errors++;
          }
        }
      } else {
        const err113 = { instancePath: instancePath + "/thickness_bias_mm", schemaPath: "#/$defs/ThicknessBias/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err113];
        } else {
          vErrors.push(err113);
        }
        errors++;
      }
    }
    if (data.highlight_count !== void 0) {
      let data59 = data.highlight_count;
      if (!(typeof data59 == "number" && (!(data59 % 1) && !isNaN(data59)))) {
        const err114 = { instancePath: instancePath + "/highlight_count", schemaPath: "#/properties/highlight_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err114];
        } else {
          vErrors.push(err114);
        }
        errors++;
      }
    }
    for (const key3 in data) {
      if (key3 !== "thickness_mm" && key3 !== "z_mm" && key3 !== "copper_color" && key3 !== "outline_width_mm" && key3 !== "outline_color" && key3 !== "board_cutout_color" && key3 !== "include_copper" && key3 !== "include_board_outline" && key3 !== "include_board_cutouts" && key3 !== "include_poured_polygons" && key3 !== "cut_holes" && key3 !== "drill_hole_mode" && key3 !== "effective_drill_hole_mode" && key3 !== "max_boolean_drill_cuts" && key3 !== "drill_hole_color" && key3 !== "drill_plated_hole_color" && key3 !== "drill_non_plated_hole_color" && key3 !== "drill_overlay_thickness_mm" && key3 !== "drill_minimum_diameter_mm" && key3 !== "drill_hole_shape" && key3 !== "drill_ring_width_mm" && key3 !== "drill_plated_ring_shape" && key3 !== "drill_selected_component_mode" && key3 !== "drill_other_component_mode" && key3 !== "drill_free_pad_mode" && key3 !== "drill_via_mode" && key3 !== "fuse_copper" && key3 !== "fuse_board_outline" && key3 !== "arc_segments" && key3 !== "features" && key3 !== "pad_color_rules" && key3 !== "feature_color_rules" && key3 !== "thickness_bias_mm" && key3 !== "highlight_count") {
        const err115 = { instancePath: instancePath + "/" + key3.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err115];
        } else {
          vErrors.push(err115);
        }
        errors++;
      }
    }
  } else {
    const err116 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err116];
    } else {
      vErrors.push(err116);
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
    if (data.backend === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "backend" }, message: "must have required property 'backend'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.board === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "board" }, message: "must have required property 'board'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.source_input === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "source_input" }, message: "must have required property 'source_input'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.step_file === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "step_file" }, message: "must have required property 'step_file'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.coordinate_origin === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "coordinate_origin" }, message: "must have required property 'coordinate_origin'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.layer === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "layer" }, message: "must have required property 'layer'" };
      if (vErrors === null) {
        vErrors = [err6];
      } else {
        vErrors.push(err6);
      }
      errors++;
    }
    if (data.options === void 0) {
      const err7 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "options" }, message: "must have required property 'options'" };
      if (vErrors === null) {
        vErrors = [err7];
      } else {
        vErrors.push(err7);
      }
      errors++;
    }
    if (data.counts === void 0) {
      const err8 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "counts" }, message: "must have required property 'counts'" };
      if (vErrors === null) {
        vErrors = [err8];
      } else {
        vErrors.push(err8);
      }
      errors++;
    }
    if (data.bytes === void 0) {
      const err9 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "bytes" }, message: "must have required property 'bytes'" };
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
      if ("altium_cruncher.pcb_layer_step.a0" !== data0) {
        const err11 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.pcb_layer_step.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
    }
    if (data.backend !== void 0) {
      let data1 = data.backend;
      if (typeof data1 !== "string") {
        const err12 = { instancePath: instancePath + "/backend", schemaPath: "#/properties/backend/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("geometer.planar_step" !== data1) {
        const err13 = { instancePath: instancePath + "/backend", schemaPath: "#/properties/backend/const", keyword: "const", params: { allowedValue: "geometer.planar_step" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.board !== void 0) {
      if (typeof data.board !== "string") {
        const err14 = { instancePath: instancePath + "/board", schemaPath: "#/properties/board/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
    }
    if (data.source_input !== void 0) {
      let data3 = data.source_input;
      const _errs9 = errors;
      let valid1 = false;
      const _errs10 = errors;
      if (typeof data3 !== "string") {
        const err15 = { instancePath: instancePath + "/source_input", schemaPath: "#/properties/source_input/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      valid1 = valid1 || _valid0;
      const _errs12 = errors;
      if (data3 !== null) {
        const err16 = { instancePath: instancePath + "/source_input", schemaPath: "#/properties/source_input/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid0 = _errs12 === errors;
      valid1 = valid1 || _valid0;
      if (!valid1) {
        const err17 = { instancePath: instancePath + "/source_input", schemaPath: "#/properties/source_input/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      } else {
        errors = _errs9;
        if (vErrors !== null) {
          if (_errs9) {
            vErrors.length = _errs9;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.step_file !== void 0) {
      if (typeof data.step_file !== "string") {
        const err18 = { instancePath: instancePath + "/step_file", schemaPath: "#/properties/step_file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
    }
    if (data.coordinate_origin !== void 0) {
      if (!validate21(data.coordinate_origin, { instancePath: instancePath + "/coordinate_origin", parentData: data, parentDataProperty: "coordinate_origin", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
        errors = vErrors.length;
      }
    }
    if (data.layer !== void 0) {
      let data6 = data.layer;
      if (data6 && typeof data6 == "object" && !Array.isArray(data6)) {
        if (data6.id === void 0) {
          const err19 = { instancePath: instancePath + "/layer", schemaPath: "#/$defs/Layer/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
          if (vErrors === null) {
            vErrors = [err19];
          } else {
            vErrors.push(err19);
          }
          errors++;
        }
        if (data6.json_name === void 0) {
          const err20 = { instancePath: instancePath + "/layer", schemaPath: "#/$defs/Layer/required", keyword: "required", params: { missingProperty: "json_name" }, message: "must have required property 'json_name'" };
          if (vErrors === null) {
            vErrors = [err20];
          } else {
            vErrors.push(err20);
          }
          errors++;
        }
        if (data6.display_name === void 0) {
          const err21 = { instancePath: instancePath + "/layer", schemaPath: "#/$defs/Layer/required", keyword: "required", params: { missingProperty: "display_name" }, message: "must have required property 'display_name'" };
          if (vErrors === null) {
            vErrors = [err21];
          } else {
            vErrors.push(err21);
          }
          errors++;
        }
        if (data6.id !== void 0) {
          let data7 = data6.id;
          if (!(typeof data7 == "number" && (!(data7 % 1) && !isNaN(data7)))) {
            const err22 = { instancePath: instancePath + "/layer/id", schemaPath: "#/$defs/Layer/properties/id/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
            if (vErrors === null) {
              vErrors = [err22];
            } else {
              vErrors.push(err22);
            }
            errors++;
          }
        }
        if (data6.json_name !== void 0) {
          if (typeof data6.json_name !== "string") {
            const err23 = { instancePath: instancePath + "/layer/json_name", schemaPath: "#/$defs/Layer/properties/json_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err23];
            } else {
              vErrors.push(err23);
            }
            errors++;
          }
        }
        if (data6.display_name !== void 0) {
          if (typeof data6.display_name !== "string") {
            const err24 = { instancePath: instancePath + "/layer/display_name", schemaPath: "#/$defs/Layer/properties/display_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err24];
            } else {
              vErrors.push(err24);
            }
            errors++;
          }
        }
        for (const key0 in data6) {
          if (key0 !== "id" && key0 !== "json_name" && key0 !== "display_name") {
            const err25 = { instancePath: instancePath + "/layer/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/Layer/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err25];
            } else {
              vErrors.push(err25);
            }
            errors++;
          }
        }
      } else {
        const err26 = { instancePath: instancePath + "/layer", schemaPath: "#/$defs/Layer/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
    }
    if (data.options !== void 0) {
      if (!validate23(data.options, { instancePath: instancePath + "/options", parentData: data, parentDataProperty: "options", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate23.errors : vErrors.concat(validate23.errors);
        errors = vErrors.length;
      }
    }
    if (data.counts !== void 0) {
      let data12 = data.counts;
      if (data12 && typeof data12 == "object" && !Array.isArray(data12)) {
        for (const key1 in data12) {
          let data13 = data12[key1];
          if (!(typeof data13 == "number" && (!(data13 % 1) && !isNaN(data13)))) {
            const err27 = { instancePath: instancePath + "/counts/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/RecordInteger/unevaluatedProperties/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
            if (vErrors === null) {
              vErrors = [err27];
            } else {
              vErrors.push(err27);
            }
            errors++;
          }
        }
      } else {
        const err28 = { instancePath: instancePath + "/counts", schemaPath: "#/$defs/RecordInteger/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
    }
    if (data.bytes !== void 0) {
      let data14 = data.bytes;
      if (!(typeof data14 == "number" && (!(data14 % 1) && !isNaN(data14)))) {
        const err29 = { instancePath: instancePath + "/bytes", schemaPath: "#/properties/bytes/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      }
    }
    for (const key2 in data) {
      if (key2 !== "schema" && key2 !== "backend" && key2 !== "board" && key2 !== "source_input" && key2 !== "step_file" && key2 !== "coordinate_origin" && key2 !== "layer" && key2 !== "options" && key2 !== "counts" && key2 !== "bytes") {
        const err30 = { instancePath: instancePath + "/" + key2.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
        }
        errors++;
      }
    }
  } else {
    const err31 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err31];
    } else {
      vErrors.push(err31);
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
