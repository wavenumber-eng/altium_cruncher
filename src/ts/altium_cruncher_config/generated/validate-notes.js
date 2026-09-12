// Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit.
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
    if (data.text === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "text" }, message: "must have required property 'text'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.position_mils === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "position_mils" }, message: "must have required property 'position_mils'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.text !== void 0) {
      if (typeof data.text !== "string") {
        const err2 = { instancePath: instancePath + "/text", schemaPath: "#/properties/text/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
    if (data.position_mils !== void 0) {
      let data1 = data.position_mils;
      const _errs4 = errors;
      let valid1 = false;
      const _errs5 = errors;
      if (data1 && typeof data1 == "object" && !Array.isArray(data1)) {
        if (data1.x === void 0) {
          const err3 = { instancePath: instancePath + "/position_mils", schemaPath: "#/$defs/Point/required", keyword: "required", params: { missingProperty: "x" }, message: "must have required property 'x'" };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
        if (data1.y === void 0) {
          const err4 = { instancePath: instancePath + "/position_mils", schemaPath: "#/$defs/Point/required", keyword: "required", params: { missingProperty: "y" }, message: "must have required property 'y'" };
          if (vErrors === null) {
            vErrors = [err4];
          } else {
            vErrors.push(err4);
          }
          errors++;
        }
        if (data1.x !== void 0) {
          if (!(typeof data1.x == "number")) {
            const err5 = { instancePath: instancePath + "/position_mils/x", schemaPath: "#/$defs/Point/properties/x/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err5];
            } else {
              vErrors.push(err5);
            }
            errors++;
          }
        }
        if (data1.y !== void 0) {
          if (!(typeof data1.y == "number")) {
            const err6 = { instancePath: instancePath + "/position_mils/y", schemaPath: "#/$defs/Point/properties/y/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err6];
            } else {
              vErrors.push(err6);
            }
            errors++;
          }
        }
        for (const key0 in data1) {
          if (key0 !== "x" && key0 !== "y") {
            const err7 = { instancePath: instancePath + "/position_mils/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/Point/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err7];
            } else {
              vErrors.push(err7);
            }
            errors++;
          }
        }
      } else {
        const err8 = { instancePath: instancePath + "/position_mils", schemaPath: "#/$defs/Point/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid0 = _errs5 === errors;
      valid1 = valid1 || _valid0;
      const _errs15 = errors;
      if (data1 !== null) {
        const err9 = { instancePath: instancePath + "/position_mils", schemaPath: "#/properties/position_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid0 = _errs15 === errors;
      valid1 = valid1 || _valid0;
      if (!valid1) {
        const err10 = { instancePath: instancePath + "/position_mils", schemaPath: "#/properties/position_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      } else {
        errors = _errs4;
        if (vErrors !== null) {
          if (_errs4) {
            vErrors.length = _errs4;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.unique_id !== void 0) {
      if (typeof data.unique_id !== "string") {
        const err11 = { instancePath: instancePath + "/unique_id", schemaPath: "#/properties/unique_id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
    }
    if (data.bounds_mils !== void 0) {
      let data6 = data.bounds_mils;
      if (data6 && typeof data6 == "object" && !Array.isArray(data6)) {
        if (data6.x_min === void 0) {
          const err12 = { instancePath: instancePath + "/bounds_mils", schemaPath: "#/$defs/Bounds/required", keyword: "required", params: { missingProperty: "x_min" }, message: "must have required property 'x_min'" };
          if (vErrors === null) {
            vErrors = [err12];
          } else {
            vErrors.push(err12);
          }
          errors++;
        }
        if (data6.y_min === void 0) {
          const err13 = { instancePath: instancePath + "/bounds_mils", schemaPath: "#/$defs/Bounds/required", keyword: "required", params: { missingProperty: "y_min" }, message: "must have required property 'y_min'" };
          if (vErrors === null) {
            vErrors = [err13];
          } else {
            vErrors.push(err13);
          }
          errors++;
        }
        if (data6.x_max === void 0) {
          const err14 = { instancePath: instancePath + "/bounds_mils", schemaPath: "#/$defs/Bounds/required", keyword: "required", params: { missingProperty: "x_max" }, message: "must have required property 'x_max'" };
          if (vErrors === null) {
            vErrors = [err14];
          } else {
            vErrors.push(err14);
          }
          errors++;
        }
        if (data6.y_max === void 0) {
          const err15 = { instancePath: instancePath + "/bounds_mils", schemaPath: "#/$defs/Bounds/required", keyword: "required", params: { missingProperty: "y_max" }, message: "must have required property 'y_max'" };
          if (vErrors === null) {
            vErrors = [err15];
          } else {
            vErrors.push(err15);
          }
          errors++;
        }
        if (data6.x_min !== void 0) {
          if (!(typeof data6.x_min == "number")) {
            const err16 = { instancePath: instancePath + "/bounds_mils/x_min", schemaPath: "#/$defs/Bounds/properties/x_min/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err16];
            } else {
              vErrors.push(err16);
            }
            errors++;
          }
        }
        if (data6.y_min !== void 0) {
          if (!(typeof data6.y_min == "number")) {
            const err17 = { instancePath: instancePath + "/bounds_mils/y_min", schemaPath: "#/$defs/Bounds/properties/y_min/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err17];
            } else {
              vErrors.push(err17);
            }
            errors++;
          }
        }
        if (data6.x_max !== void 0) {
          if (!(typeof data6.x_max == "number")) {
            const err18 = { instancePath: instancePath + "/bounds_mils/x_max", schemaPath: "#/$defs/Bounds/properties/x_max/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err18];
            } else {
              vErrors.push(err18);
            }
            errors++;
          }
        }
        if (data6.y_max !== void 0) {
          if (!(typeof data6.y_max == "number")) {
            const err19 = { instancePath: instancePath + "/bounds_mils/y_max", schemaPath: "#/$defs/Bounds/properties/y_max/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err19];
            } else {
              vErrors.push(err19);
            }
            errors++;
          }
        }
        for (const key1 in data6) {
          if (key1 !== "x_min" && key1 !== "y_min" && key1 !== "x_max" && key1 !== "y_max") {
            const err20 = { instancePath: instancePath + "/bounds_mils/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/Bounds/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err20];
            } else {
              vErrors.push(err20);
            }
            errors++;
          }
        }
      } else {
        const err21 = { instancePath: instancePath + "/bounds_mils", schemaPath: "#/$defs/Bounds/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
    }
    if (data.author !== void 0) {
      let data12 = data.author;
      const _errs34 = errors;
      let valid8 = false;
      const _errs35 = errors;
      if (typeof data12 !== "string") {
        const err22 = { instancePath: instancePath + "/author", schemaPath: "#/properties/author/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
      var _valid1 = _errs35 === errors;
      valid8 = valid8 || _valid1;
      const _errs37 = errors;
      if (!(typeof data12 == "number")) {
        const err23 = { instancePath: instancePath + "/author", schemaPath: "#/properties/author/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      var _valid1 = _errs37 === errors;
      valid8 = valid8 || _valid1;
      const _errs39 = errors;
      if (typeof data12 !== "boolean") {
        const err24 = { instancePath: instancePath + "/author", schemaPath: "#/properties/author/anyOf/2/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      var _valid1 = _errs39 === errors;
      valid8 = valid8 || _valid1;
      if (!valid8) {
        const err25 = { instancePath: instancePath + "/author", schemaPath: "#/properties/author/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      } else {
        errors = _errs34;
        if (vErrors !== null) {
          if (_errs34) {
            vErrors.length = _errs34;
          } else {
            vErrors = null;
          }
        }
      }
    }
    for (const key2 in data) {
      if (key2 !== "text" && key2 !== "position_mils" && key2 !== "unique_id" && key2 !== "bounds_mils" && key2 !== "author") {
        const err26 = { instancePath: instancePath + "/" + key2.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
    }
  } else {
    const err27 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err27];
    } else {
      vErrors.push(err27);
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
    if (data.file === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.file !== void 0) {
      if (typeof data.file !== "string") {
        const err1 = { instancePath: instancePath + "/file", schemaPath: "#/properties/file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
    }
    if (data.notes !== void 0) {
      let data1 = data.notes;
      if (Array.isArray(data1)) {
        const len0 = data1.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!validate22(data1[i0], { instancePath: instancePath + "/notes/" + i0, parentData: data1, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate22.errors : vErrors.concat(validate22.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err2 = { instancePath: instancePath + "/notes", schemaPath: "#/properties/notes/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
    if (data.text_frames !== void 0) {
      let data3 = data.text_frames;
      if (Array.isArray(data3)) {
        const len1 = data3.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (!validate22(data3[i1], { instancePath: instancePath + "/text_frames/" + i1, parentData: data3, parentDataProperty: i1, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate22.errors : vErrors.concat(validate22.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err3 = { instancePath: instancePath + "/text_frames", schemaPath: "#/properties/text_frames/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.free_text !== void 0) {
      let data5 = data.free_text;
      if (Array.isArray(data5)) {
        const len2 = data5.length;
        for (let i2 = 0; i2 < len2; i2++) {
          if (!validate22(data5[i2], { instancePath: instancePath + "/free_text/" + i2, parentData: data5, parentDataProperty: i2, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate22.errors : vErrors.concat(validate22.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err4 = { instancePath: instancePath + "/free_text", schemaPath: "#/properties/free_text/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    for (const key0 in data) {
      if (key0 !== "file" && key0 !== "notes" && key0 !== "text_frames" && key0 !== "free_text") {
        const err5 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
  } else {
    const err6 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err6];
    } else {
      vErrors.push(err6);
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
    if (data.input === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "input" }, message: "must have required property 'input'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.source_kind === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "source_kind" }, message: "must have required property 'source_kind'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.path_base === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "path_base" }, message: "must have required property 'path_base'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.schdoc_count === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "schdoc_count" }, message: "must have required property 'schdoc_count'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.filters === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "filters" }, message: "must have required property 'filters'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.schdocs === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "schdocs" }, message: "must have required property 'schdocs'" };
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
      if ("altium_cruncher.notes.a0" !== data0) {
        const err8 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.notes.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
    if (data.input !== void 0) {
      if (typeof data.input !== "string") {
        const err9 = { instancePath: instancePath + "/input", schemaPath: "#/properties/input/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    if (data.source_kind !== void 0) {
      let data2 = data.source_kind;
      const _errs7 = errors;
      let valid1 = false;
      const _errs8 = errors;
      if (typeof data2 !== "string") {
        const err10 = { instancePath: instancePath + "/source_kind", schemaPath: "#/properties/source_kind/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      if ("schdoc" !== data2) {
        const err11 = { instancePath: instancePath + "/source_kind", schemaPath: "#/properties/source_kind/anyOf/0/const", keyword: "const", params: { allowedValue: "schdoc" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid0 = _errs8 === errors;
      valid1 = valid1 || _valid0;
      const _errs10 = errors;
      if (typeof data2 !== "string") {
        const err12 = { instancePath: instancePath + "/source_kind", schemaPath: "#/properties/source_kind/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("prjpcb" !== data2) {
        const err13 = { instancePath: instancePath + "/source_kind", schemaPath: "#/properties/source_kind/anyOf/1/const", keyword: "const", params: { allowedValue: "prjpcb" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      valid1 = valid1 || _valid0;
      if (!valid1) {
        const err14 = { instancePath: instancePath + "/source_kind", schemaPath: "#/properties/source_kind/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      } else {
        errors = _errs7;
        if (vErrors !== null) {
          if (_errs7) {
            vErrors.length = _errs7;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.path_base !== void 0) {
      let data3 = data.path_base;
      if (typeof data3 !== "string") {
        const err15 = { instancePath: instancePath + "/path_base", schemaPath: "#/properties/path_base/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      if ("input_directory" !== data3) {
        const err16 = { instancePath: instancePath + "/path_base", schemaPath: "#/properties/path_base/const", keyword: "const", params: { allowedValue: "input_directory" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
    }
    if (data.schdoc_count !== void 0) {
      let data4 = data.schdoc_count;
      if (!(typeof data4 == "number" && (!(data4 % 1) && !isNaN(data4)))) {
        const err17 = { instancePath: instancePath + "/schdoc_count", schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      if (typeof data4 == "number") {
        if (data4 < 0 || isNaN(data4)) {
          const err18 = { instancePath: instancePath + "/schdoc_count", schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err18];
          } else {
            vErrors.push(err18);
          }
          errors++;
        }
      }
    }
    if (data.filters !== void 0) {
      let data5 = data.filters;
      if (data5 && typeof data5 == "object" && !Array.isArray(data5)) {
        if (data5.include_sheet_template_text === void 0) {
          const err19 = { instancePath: instancePath + "/filters", schemaPath: "#/$defs/NoteFilters/required", keyword: "required", params: { missingProperty: "include_sheet_template_text" }, message: "must have required property 'include_sheet_template_text'" };
          if (vErrors === null) {
            vErrors = [err19];
          } else {
            vErrors.push(err19);
          }
          errors++;
        }
        if (data5.default_suppression === void 0) {
          const err20 = { instancePath: instancePath + "/filters", schemaPath: "#/$defs/NoteFilters/required", keyword: "required", params: { missingProperty: "default_suppression" }, message: "must have required property 'default_suppression'" };
          if (vErrors === null) {
            vErrors = [err20];
          } else {
            vErrors.push(err20);
          }
          errors++;
        }
        if (data5.include_sheet_template_text !== void 0) {
          if (typeof data5.include_sheet_template_text !== "boolean") {
            const err21 = { instancePath: instancePath + "/filters/include_sheet_template_text", schemaPath: "#/$defs/NoteFilters/properties/include_sheet_template_text/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err21];
            } else {
              vErrors.push(err21);
            }
            errors++;
          }
        }
        if (data5.default_suppression !== void 0) {
          if (typeof data5.default_suppression !== "string") {
            const err22 = { instancePath: instancePath + "/filters/default_suppression", schemaPath: "#/$defs/NoteFilters/properties/default_suppression/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err22];
            } else {
              vErrors.push(err22);
            }
            errors++;
          }
        }
        for (const key0 in data5) {
          if (key0 !== "include_sheet_template_text" && key0 !== "default_suppression") {
            const err23 = { instancePath: instancePath + "/filters/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/NoteFilters/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err23];
            } else {
              vErrors.push(err23);
            }
            errors++;
          }
        }
      } else {
        const err24 = { instancePath: instancePath + "/filters", schemaPath: "#/$defs/NoteFilters/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
    }
    if (data.schdocs !== void 0) {
      let data9 = data.schdocs;
      if (Array.isArray(data9)) {
        const len0 = data9.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!validate21(data9[i0], { instancePath: instancePath + "/schdocs/" + i0, parentData: data9, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err25 = { instancePath: instancePath + "/schdocs", schemaPath: "#/properties/schdocs/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "schema" && key1 !== "input" && key1 !== "source_kind" && key1 !== "path_base" && key1 !== "schdoc_count" && key1 !== "filters" && key1 !== "schdocs") {
        const err26 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
    }
  } else {
    const err27 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err27];
    } else {
      vErrors.push(err27);
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
