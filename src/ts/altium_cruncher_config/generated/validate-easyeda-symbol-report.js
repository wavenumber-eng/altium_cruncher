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
    if (data.hotspot_grid_mils !== void 0) {
      if (!(typeof data.hotspot_grid_mils == "number")) {
        const err0 = { instancePath: instancePath + "/hotspot_grid_mils", schemaPath: "#/properties/hotspot_grid_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err0];
        } else {
          vErrors.push(err0);
        }
        errors++;
      }
    }
    if (data.align_hotspots_to_grid !== void 0) {
      if (typeof data.align_hotspots_to_grid !== "boolean") {
        const err1 = { instancePath: instancePath + "/align_hotspots_to_grid", schemaPath: "#/properties/align_hotspots_to_grid/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
    }
    if (data.anchor_adjusted_to_grid !== void 0) {
      if (typeof data.anchor_adjusted_to_grid !== "boolean") {
        const err2 = { instancePath: instancePath + "/anchor_adjusted_to_grid", schemaPath: "#/properties/anchor_adjusted_to_grid/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
    if (data.source_grid_units !== void 0) {
      if (!(typeof data.source_grid_units == "number")) {
        const err3 = { instancePath: instancePath + "/source_grid_units", schemaPath: "#/properties/source_grid_units/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.source_common_offset_possible !== void 0) {
      if (typeof data.source_common_offset_possible !== "boolean") {
        const err4 = { instancePath: instancePath + "/source_common_offset_possible", schemaPath: "#/properties/source_common_offset_possible/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.source_x_remainder !== void 0) {
      let data5 = data.source_x_remainder;
      const _errs12 = errors;
      let valid1 = false;
      const _errs13 = errors;
      if (!(typeof data5 == "number")) {
        const err5 = { instancePath: instancePath + "/source_x_remainder", schemaPath: "#/properties/source_x_remainder/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid0 = _errs13 === errors;
      valid1 = valid1 || _valid0;
      const _errs15 = errors;
      if (data5 !== null) {
        const err6 = { instancePath: instancePath + "/source_x_remainder", schemaPath: "#/properties/source_x_remainder/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs15 === errors;
      valid1 = valid1 || _valid0;
      if (!valid1) {
        const err7 = { instancePath: instancePath + "/source_x_remainder", schemaPath: "#/properties/source_x_remainder/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      } else {
        errors = _errs12;
        if (vErrors !== null) {
          if (_errs12) {
            vErrors.length = _errs12;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.source_y_remainder !== void 0) {
      let data6 = data.source_y_remainder;
      const _errs18 = errors;
      let valid2 = false;
      const _errs19 = errors;
      if (!(typeof data6 == "number")) {
        const err8 = { instancePath: instancePath + "/source_y_remainder", schemaPath: "#/properties/source_y_remainder/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid1 = _errs19 === errors;
      valid2 = valid2 || _valid1;
      const _errs21 = errors;
      if (data6 !== null) {
        const err9 = { instancePath: instancePath + "/source_y_remainder", schemaPath: "#/properties/source_y_remainder/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid1 = _errs21 === errors;
      valid2 = valid2 || _valid1;
      if (!valid2) {
        const err10 = { instancePath: instancePath + "/source_y_remainder", schemaPath: "#/properties/source_y_remainder/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
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
    if (data.hotspot_count !== void 0) {
      let data7 = data.hotspot_count;
      if (!(typeof data7 == "number" && (!(data7 % 1) && !isNaN(data7)))) {
        const err11 = { instancePath: instancePath + "/hotspot_count", schemaPath: "#/properties/hotspot_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
    }
    if (data.off_grid_hotspot_count !== void 0) {
      let data8 = data.off_grid_hotspot_count;
      if (!(typeof data8 == "number" && (!(data8 % 1) && !isNaN(data8)))) {
        const err12 = { instancePath: instancePath + "/off_grid_hotspot_count", schemaPath: "#/properties/off_grid_hotspot_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
    }
    if (data.max_hotspot_error_mils !== void 0) {
      if (!(typeof data.max_hotspot_error_mils == "number")) {
        const err13 = { instancePath: instancePath + "/max_hotspot_error_mils", schemaPath: "#/properties/max_hotspot_error_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.off_grid_hotspots_sample !== void 0) {
      let data10 = data.off_grid_hotspots_sample;
      if (Array.isArray(data10)) {
        const len0 = data10.length;
        for (let i0 = 0; i0 < len0; i0++) {
          let data11 = data10[i0];
          if (data11 && typeof data11 == "object" && !Array.isArray(data11)) {
            if (data11.pin === void 0) {
              const err14 = { instancePath: instancePath + "/off_grid_hotspots_sample/" + i0, schemaPath: "#/$defs/OffGridHotspot/required", keyword: "required", params: { missingProperty: "pin" }, message: "must have required property 'pin'" };
              if (vErrors === null) {
                vErrors = [err14];
              } else {
                vErrors.push(err14);
              }
              errors++;
            }
            if (data11.name === void 0) {
              const err15 = { instancePath: instancePath + "/off_grid_hotspots_sample/" + i0, schemaPath: "#/$defs/OffGridHotspot/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
              if (vErrors === null) {
                vErrors = [err15];
              } else {
                vErrors.push(err15);
              }
              errors++;
            }
            if (data11.x_mils === void 0) {
              const err16 = { instancePath: instancePath + "/off_grid_hotspots_sample/" + i0, schemaPath: "#/$defs/OffGridHotspot/required", keyword: "required", params: { missingProperty: "x_mils" }, message: "must have required property 'x_mils'" };
              if (vErrors === null) {
                vErrors = [err16];
              } else {
                vErrors.push(err16);
              }
              errors++;
            }
            if (data11.y_mils === void 0) {
              const err17 = { instancePath: instancePath + "/off_grid_hotspots_sample/" + i0, schemaPath: "#/$defs/OffGridHotspot/required", keyword: "required", params: { missingProperty: "y_mils" }, message: "must have required property 'y_mils'" };
              if (vErrors === null) {
                vErrors = [err17];
              } else {
                vErrors.push(err17);
              }
              errors++;
            }
            if (data11.x_error_mils === void 0) {
              const err18 = { instancePath: instancePath + "/off_grid_hotspots_sample/" + i0, schemaPath: "#/$defs/OffGridHotspot/required", keyword: "required", params: { missingProperty: "x_error_mils" }, message: "must have required property 'x_error_mils'" };
              if (vErrors === null) {
                vErrors = [err18];
              } else {
                vErrors.push(err18);
              }
              errors++;
            }
            if (data11.y_error_mils === void 0) {
              const err19 = { instancePath: instancePath + "/off_grid_hotspots_sample/" + i0, schemaPath: "#/$defs/OffGridHotspot/required", keyword: "required", params: { missingProperty: "y_error_mils" }, message: "must have required property 'y_error_mils'" };
              if (vErrors === null) {
                vErrors = [err19];
              } else {
                vErrors.push(err19);
              }
              errors++;
            }
            if (data11.pin !== void 0) {
              if (typeof data11.pin !== "string") {
                const err20 = { instancePath: instancePath + "/off_grid_hotspots_sample/" + i0 + "/pin", schemaPath: "#/$defs/OffGridHotspot/properties/pin/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err20];
                } else {
                  vErrors.push(err20);
                }
                errors++;
              }
            }
            if (data11.name !== void 0) {
              if (typeof data11.name !== "string") {
                const err21 = { instancePath: instancePath + "/off_grid_hotspots_sample/" + i0 + "/name", schemaPath: "#/$defs/OffGridHotspot/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err21];
                } else {
                  vErrors.push(err21);
                }
                errors++;
              }
            }
            if (data11.x_mils !== void 0) {
              if (!(typeof data11.x_mils == "number")) {
                const err22 = { instancePath: instancePath + "/off_grid_hotspots_sample/" + i0 + "/x_mils", schemaPath: "#/$defs/OffGridHotspot/properties/x_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
                if (vErrors === null) {
                  vErrors = [err22];
                } else {
                  vErrors.push(err22);
                }
                errors++;
              }
            }
            if (data11.y_mils !== void 0) {
              if (!(typeof data11.y_mils == "number")) {
                const err23 = { instancePath: instancePath + "/off_grid_hotspots_sample/" + i0 + "/y_mils", schemaPath: "#/$defs/OffGridHotspot/properties/y_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
                if (vErrors === null) {
                  vErrors = [err23];
                } else {
                  vErrors.push(err23);
                }
                errors++;
              }
            }
            if (data11.x_error_mils !== void 0) {
              if (!(typeof data11.x_error_mils == "number")) {
                const err24 = { instancePath: instancePath + "/off_grid_hotspots_sample/" + i0 + "/x_error_mils", schemaPath: "#/$defs/OffGridHotspot/properties/x_error_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
                if (vErrors === null) {
                  vErrors = [err24];
                } else {
                  vErrors.push(err24);
                }
                errors++;
              }
            }
            if (data11.y_error_mils !== void 0) {
              if (!(typeof data11.y_error_mils == "number")) {
                const err25 = { instancePath: instancePath + "/off_grid_hotspots_sample/" + i0 + "/y_error_mils", schemaPath: "#/$defs/OffGridHotspot/properties/y_error_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
                if (vErrors === null) {
                  vErrors = [err25];
                } else {
                  vErrors.push(err25);
                }
                errors++;
              }
            }
            for (const key0 in data11) {
              if (key0 !== "pin" && key0 !== "name" && key0 !== "x_mils" && key0 !== "y_mils" && key0 !== "x_error_mils" && key0 !== "y_error_mils") {
                const err26 = { instancePath: instancePath + "/off_grid_hotspots_sample/" + i0 + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/OffGridHotspot/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err26];
                } else {
                  vErrors.push(err26);
                }
                errors++;
              }
            }
          } else {
            const err27 = { instancePath: instancePath + "/off_grid_hotspots_sample/" + i0, schemaPath: "#/$defs/OffGridHotspot/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err27];
            } else {
              vErrors.push(err27);
            }
            errors++;
          }
        }
      } else {
        const err28 = { instancePath: instancePath + "/off_grid_hotspots_sample", schemaPath: "#/properties/off_grid_hotspots_sample/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "hotspot_grid_mils" && key1 !== "align_hotspots_to_grid" && key1 !== "anchor_adjusted_to_grid" && key1 !== "source_grid_units" && key1 !== "source_common_offset_possible" && key1 !== "source_x_remainder" && key1 !== "source_y_remainder" && key1 !== "hotspot_count" && key1 !== "off_grid_hotspot_count" && key1 !== "max_hotspot_error_mils" && key1 !== "off_grid_hotspots_sample") {
        const err29 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      }
    }
  } else {
    const err30 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err30];
    } else {
      vErrors.push(err30);
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
    if (data.symbol_name === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "symbol_name" }, message: "must have required property 'symbol_name'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.designator === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "designator" }, message: "must have required property 'designator'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.pin_count === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "pin_count" }, message: "must have required property 'pin_count'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.rectangle_count === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "rectangle_count" }, message: "must have required property 'rectangle_count'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.circle_count === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "circle_count" }, message: "must have required property 'circle_count'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.ellipse_count === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "ellipse_count" }, message: "must have required property 'ellipse_count'" };
      if (vErrors === null) {
        vErrors = [err6];
      } else {
        vErrors.push(err6);
      }
      errors++;
    }
    if (data.polyline_count === void 0) {
      const err7 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "polyline_count" }, message: "must have required property 'polyline_count'" };
      if (vErrors === null) {
        vErrors = [err7];
      } else {
        vErrors.push(err7);
      }
      errors++;
    }
    if (data.polygon_count === void 0) {
      const err8 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "polygon_count" }, message: "must have required property 'polygon_count'" };
      if (vErrors === null) {
        vErrors = [err8];
      } else {
        vErrors.push(err8);
      }
      errors++;
    }
    if (data.unsupported_count === void 0) {
      const err9 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "unsupported_count" }, message: "must have required property 'unsupported_count'" };
      if (vErrors === null) {
        vErrors = [err9];
      } else {
        vErrors.push(err9);
      }
      errors++;
    }
    if (data.unsupported_graphics === void 0) {
      const err10 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "unsupported_graphics" }, message: "must have required property 'unsupported_graphics'" };
      if (vErrors === null) {
        vErrors = [err10];
      } else {
        vErrors.push(err10);
      }
      errors++;
    }
    if (data.warnings === void 0) {
      const err11 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "warnings" }, message: "must have required property 'warnings'" };
      if (vErrors === null) {
        vErrors = [err11];
      } else {
        vErrors.push(err11);
      }
      errors++;
    }
    if (data.policy === void 0) {
      const err12 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "policy" }, message: "must have required property 'policy'" };
      if (vErrors === null) {
        vErrors = [err12];
      } else {
        vErrors.push(err12);
      }
      errors++;
    }
    if (data.grid === void 0) {
      const err13 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "grid" }, message: "must have required property 'grid'" };
      if (vErrors === null) {
        vErrors = [err13];
      } else {
        vErrors.push(err13);
      }
      errors++;
    }
    if (data.lcsc_id !== void 0) {
      if (typeof data.lcsc_id !== "string") {
        const err14 = { instancePath: instancePath + "/lcsc_id", schemaPath: "#/properties/lcsc_id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
    }
    if (data.symbol_name !== void 0) {
      if (typeof data.symbol_name !== "string") {
        const err15 = { instancePath: instancePath + "/symbol_name", schemaPath: "#/properties/symbol_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
    }
    if (data.designator !== void 0) {
      if (typeof data.designator !== "string") {
        const err16 = { instancePath: instancePath + "/designator", schemaPath: "#/properties/designator/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
    }
    if (data.pin_count !== void 0) {
      let data3 = data.pin_count;
      if (!(typeof data3 == "number" && (!(data3 % 1) && !isNaN(data3)))) {
        const err17 = { instancePath: instancePath + "/pin_count", schemaPath: "#/properties/pin_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
    }
    if (data.rectangle_count !== void 0) {
      let data4 = data.rectangle_count;
      if (!(typeof data4 == "number" && (!(data4 % 1) && !isNaN(data4)))) {
        const err18 = { instancePath: instancePath + "/rectangle_count", schemaPath: "#/properties/rectangle_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
    }
    if (data.circle_count !== void 0) {
      let data5 = data.circle_count;
      if (!(typeof data5 == "number" && (!(data5 % 1) && !isNaN(data5)))) {
        const err19 = { instancePath: instancePath + "/circle_count", schemaPath: "#/properties/circle_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
    }
    if (data.ellipse_count !== void 0) {
      let data6 = data.ellipse_count;
      if (!(typeof data6 == "number" && (!(data6 % 1) && !isNaN(data6)))) {
        const err20 = { instancePath: instancePath + "/ellipse_count", schemaPath: "#/properties/ellipse_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
    }
    if (data.polyline_count !== void 0) {
      let data7 = data.polyline_count;
      if (!(typeof data7 == "number" && (!(data7 % 1) && !isNaN(data7)))) {
        const err21 = { instancePath: instancePath + "/polyline_count", schemaPath: "#/properties/polyline_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
    }
    if (data.polygon_count !== void 0) {
      let data8 = data.polygon_count;
      if (!(typeof data8 == "number" && (!(data8 % 1) && !isNaN(data8)))) {
        const err22 = { instancePath: instancePath + "/polygon_count", schemaPath: "#/properties/polygon_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
    }
    if (data.unsupported_count !== void 0) {
      let data9 = data.unsupported_count;
      if (!(typeof data9 == "number" && (!(data9 % 1) && !isNaN(data9)))) {
        const err23 = { instancePath: instancePath + "/unsupported_count", schemaPath: "#/properties/unsupported_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
    }
    if (data.unsupported_graphics !== void 0) {
      let data10 = data.unsupported_graphics;
      if (Array.isArray(data10)) {
        const len0 = data10.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (typeof data10[i0] !== "string") {
            const err24 = { instancePath: instancePath + "/unsupported_graphics/" + i0, schemaPath: "#/properties/unsupported_graphics/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err24];
            } else {
              vErrors.push(err24);
            }
            errors++;
          }
        }
      } else {
        const err25 = { instancePath: instancePath + "/unsupported_graphics", schemaPath: "#/properties/unsupported_graphics/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
    }
    if (data.warnings !== void 0) {
      let data12 = data.warnings;
      if (Array.isArray(data12)) {
        const len1 = data12.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (typeof data12[i1] !== "string") {
            const err26 = { instancePath: instancePath + "/warnings/" + i1, schemaPath: "#/properties/warnings/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err26];
            } else {
              vErrors.push(err26);
            }
            errors++;
          }
        }
      } else {
        const err27 = { instancePath: instancePath + "/warnings", schemaPath: "#/properties/warnings/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
    }
    if (data.policy !== void 0) {
      let data14 = data.policy;
      if (data14 && typeof data14 == "object" && !Array.isArray(data14)) {
        if (data14.mils_per_easyeda_unit !== void 0) {
          if (!(typeof data14.mils_per_easyeda_unit == "number")) {
            const err28 = { instancePath: instancePath + "/policy/mils_per_easyeda_unit", schemaPath: "#/$defs/SymbolPolicy/properties/mils_per_easyeda_unit/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err28];
            } else {
              vErrors.push(err28);
            }
            errors++;
          }
        }
        if (data14.invert_y !== void 0) {
          if (typeof data14.invert_y !== "boolean") {
            const err29 = { instancePath: instancePath + "/policy/invert_y", schemaPath: "#/$defs/SymbolPolicy/properties/invert_y/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err29];
            } else {
              vErrors.push(err29);
            }
            errors++;
          }
        }
        if (data14.default_pin_length_mils !== void 0) {
          if (!(typeof data14.default_pin_length_mils == "number")) {
            const err30 = { instancePath: instancePath + "/policy/default_pin_length_mils", schemaPath: "#/$defs/SymbolPolicy/properties/default_pin_length_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err30];
            } else {
              vErrors.push(err30);
            }
            errors++;
          }
        }
        if (data14.hotspot_grid_mils !== void 0) {
          if (!(typeof data14.hotspot_grid_mils == "number")) {
            const err31 = { instancePath: instancePath + "/policy/hotspot_grid_mils", schemaPath: "#/$defs/SymbolPolicy/properties/hotspot_grid_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err31];
            } else {
              vErrors.push(err31);
            }
            errors++;
          }
        }
        if (data14.align_hotspots_to_grid !== void 0) {
          if (typeof data14.align_hotspots_to_grid !== "boolean") {
            const err32 = { instancePath: instancePath + "/policy/align_hotspots_to_grid", schemaPath: "#/$defs/SymbolPolicy/properties/align_hotspots_to_grid/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err32];
            } else {
              vErrors.push(err32);
            }
            errors++;
          }
        }
        if (data14.body_color !== void 0) {
          let data20 = data14.body_color;
          if (!(typeof data20 == "number" && (!(data20 % 1) && !isNaN(data20)))) {
            const err33 = { instancePath: instancePath + "/policy/body_color", schemaPath: "#/$defs/SymbolPolicy/properties/body_color/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
            if (vErrors === null) {
              vErrors = [err33];
            } else {
              vErrors.push(err33);
            }
            errors++;
          }
        }
        if (data14.body_fill_color !== void 0) {
          let data21 = data14.body_fill_color;
          if (!(typeof data21 == "number" && (!(data21 % 1) && !isNaN(data21)))) {
            const err34 = { instancePath: instancePath + "/policy/body_fill_color", schemaPath: "#/$defs/SymbolPolicy/properties/body_fill_color/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
            if (vErrors === null) {
              vErrors = [err34];
            } else {
              vErrors.push(err34);
            }
            errors++;
          }
        }
        if (data14.use_source_pin_electrical !== void 0) {
          if (typeof data14.use_source_pin_electrical !== "boolean") {
            const err35 = { instancePath: instancePath + "/policy/use_source_pin_electrical", schemaPath: "#/$defs/SymbolPolicy/properties/use_source_pin_electrical/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err35];
            } else {
              vErrors.push(err35);
            }
            errors++;
          }
        }
        if (data14.use_source_pin_ieee_symbols !== void 0) {
          if (typeof data14.use_source_pin_ieee_symbols !== "boolean") {
            const err36 = { instancePath: instancePath + "/policy/use_source_pin_ieee_symbols", schemaPath: "#/$defs/SymbolPolicy/properties/use_source_pin_ieee_symbols/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err36];
            } else {
              vErrors.push(err36);
            }
            errors++;
          }
        }
        if (data14.pin_name_visibility !== void 0) {
          if (typeof data14.pin_name_visibility !== "string") {
            const err37 = { instancePath: instancePath + "/policy/pin_name_visibility", schemaPath: "#/$defs/SymbolPolicy/properties/pin_name_visibility/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err37];
            } else {
              vErrors.push(err37);
            }
            errors++;
          }
        }
        if (data14.pin_designator_visibility !== void 0) {
          if (typeof data14.pin_designator_visibility !== "string") {
            const err38 = { instancePath: instancePath + "/policy/pin_designator_visibility", schemaPath: "#/$defs/SymbolPolicy/properties/pin_designator_visibility/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err38];
            } else {
              vErrors.push(err38);
            }
            errors++;
          }
        }
        if (data14.pin_text_orientation !== void 0) {
          if (typeof data14.pin_text_orientation !== "string") {
            const err39 = { instancePath: instancePath + "/policy/pin_text_orientation", schemaPath: "#/$defs/SymbolPolicy/properties/pin_text_orientation/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err39];
            } else {
              vErrors.push(err39);
            }
            errors++;
          }
        }
        if (data14.rotate_vertical_pin_text !== void 0) {
          if (typeof data14.rotate_vertical_pin_text !== "boolean") {
            const err40 = { instancePath: instancePath + "/policy/rotate_vertical_pin_text", schemaPath: "#/$defs/SymbolPolicy/properties/rotate_vertical_pin_text/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err40];
            } else {
              vErrors.push(err40);
            }
            errors++;
          }
        }
        for (const key0 in data14) {
          if (key0 !== "mils_per_easyeda_unit" && key0 !== "invert_y" && key0 !== "default_pin_length_mils" && key0 !== "hotspot_grid_mils" && key0 !== "align_hotspots_to_grid" && key0 !== "body_color" && key0 !== "body_fill_color" && key0 !== "use_source_pin_electrical" && key0 !== "use_source_pin_ieee_symbols" && key0 !== "pin_name_visibility" && key0 !== "pin_designator_visibility" && key0 !== "pin_text_orientation" && key0 !== "rotate_vertical_pin_text") {
            const err41 = { instancePath: instancePath + "/policy/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/SymbolPolicy/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err41];
            } else {
              vErrors.push(err41);
            }
            errors++;
          }
        }
      } else {
        const err42 = { instancePath: instancePath + "/policy", schemaPath: "#/$defs/SymbolPolicy/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err42];
        } else {
          vErrors.push(err42);
        }
        errors++;
      }
    }
    if (data.grid !== void 0) {
      if (!validate21(data.grid, { instancePath: instancePath + "/grid", parentData: data, parentDataProperty: "grid", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
        errors = vErrors.length;
      }
    }
    for (const key1 in data) {
      if (key1 !== "lcsc_id" && key1 !== "symbol_name" && key1 !== "designator" && key1 !== "pin_count" && key1 !== "rectangle_count" && key1 !== "circle_count" && key1 !== "ellipse_count" && key1 !== "polyline_count" && key1 !== "polygon_count" && key1 !== "unsupported_count" && key1 !== "unsupported_graphics" && key1 !== "warnings" && key1 !== "policy" && key1 !== "grid") {
        const err43 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err43];
        } else {
          vErrors.push(err43);
        }
        errors++;
      }
    }
  } else {
    const err44 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err44];
    } else {
      vErrors.push(err44);
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
