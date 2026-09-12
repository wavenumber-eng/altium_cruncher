// Generated from src/tsp/altium_cruncher/config/mate-config.tsp. Do not edit.
var __getOwnPropNames = Object.getOwnPropertyNames;
var __commonJS = (cb, mod) => function __require() {
  try {
    return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
  } catch (e) {
    throw mod = 0, e;
  }
};

// node_modules/ajv/dist/runtime/ucs2length.js
var require_ucs2length = __commonJS({
  "node_modules/ajv/dist/runtime/ucs2length.js"(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    function ucs2length(str) {
      const len = str.length;
      let length = 0;
      let pos = 0;
      let value;
      while (pos < len) {
        length++;
        value = str.charCodeAt(pos++);
        if (value >= 55296 && value <= 56319 && pos < len) {
          value = str.charCodeAt(pos);
          if ((value & 64512) === 56320)
            pos++;
        }
      }
      return length;
    }
    exports.default = ucs2length;
    ucs2length.code = 'require("ajv/dist/runtime/ucs2length").default';
  }
});

// validate.js
var validate = validate20;
var validate_default = validate20;
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
    const err0 = { instancePath, schemaPath: "#/$defs/RecordUnknown/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err0];
    } else {
      vErrors.push(err0);
    }
    errors++;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.left !== void 0) {
      let data0 = data.left;
      if (typeof data0 == "number") {
        if (data0 < 0 || isNaN(data0)) {
          const err1 = { instancePath: instancePath + "/left", schemaPath: "#/properties/left/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err1];
          } else {
            vErrors.push(err1);
          }
          errors++;
        }
      } else {
        const err2 = { instancePath: instancePath + "/left", schemaPath: "#/properties/left/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
    if (data.bottom !== void 0) {
      let data1 = data.bottom;
      if (typeof data1 == "number") {
        if (data1 < 0 || isNaN(data1)) {
          const err3 = { instancePath: instancePath + "/bottom", schemaPath: "#/properties/bottom/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/bottom", schemaPath: "#/properties/bottom/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.right !== void 0) {
      let data2 = data.right;
      if (typeof data2 == "number") {
        if (data2 < 0 || isNaN(data2)) {
          const err5 = { instancePath: instancePath + "/right", schemaPath: "#/properties/right/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err5];
          } else {
            vErrors.push(err5);
          }
          errors++;
        }
      } else {
        const err6 = { instancePath: instancePath + "/right", schemaPath: "#/properties/right/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.top !== void 0) {
      let data3 = data.top;
      if (typeof data3 == "number") {
        if (data3 < 0 || isNaN(data3)) {
          const err7 = { instancePath: instancePath + "/top", schemaPath: "#/properties/top/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err7];
          } else {
            vErrors.push(err7);
          }
          errors++;
        }
      } else {
        const err8 = { instancePath: instancePath + "/top", schemaPath: "#/properties/top/type", keyword: "type", params: { type: "number" }, message: "must be number" };
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
    const err0 = { instancePath, schemaPath: "#/$defs/RecordUnknown/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err0];
    } else {
      vErrors.push(err0);
    }
    errors++;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.mode !== void 0) {
      let data0 = data.mode;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err1 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      if ("source_bounds" !== data0) {
        const err2 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf/0/const", keyword: "const", params: { allowedValue: "source_bounds" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid3 = valid3 || _valid0;
      const _errs9 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      if ("match_source_bounds" !== data0) {
        const err4 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf/1/const", keyword: "const", params: { allowedValue: "match_source_bounds" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (typeof data0 !== "string") {
        const err5 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      if ("match_bounds" !== data0) {
        const err6 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf/2/const", keyword: "const", params: { allowedValue: "match_bounds" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs11 === errors;
      valid3 = valid3 || _valid0;
      const _errs13 = errors;
      if (typeof data0 !== "string") {
        const err7 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      if ("source_bounds_with_margin" !== data0) {
        const err8 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf/3/const", keyword: "const", params: { allowedValue: "source_bounds_with_margin" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid0 = _errs13 === errors;
      valid3 = valid3 || _valid0;
      const _errs15 = errors;
      if (typeof data0 !== "string") {
        const err9 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf/4/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      if ("source_bounds_plus_margin" !== data0) {
        const err10 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf/4/const", keyword: "const", params: { allowedValue: "source_bounds_plus_margin" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid0 = _errs15 === errors;
      valid3 = valid3 || _valid0;
      const _errs17 = errors;
      if (typeof data0 !== "string") {
        const err11 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf/5/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      if ("padded_rectangle" !== data0) {
        const err12 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf/5/const", keyword: "const", params: { allowedValue: "padded_rectangle" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid0 = _errs17 === errors;
      valid3 = valid3 || _valid0;
      const _errs19 = errors;
      if (typeof data0 !== "string") {
        const err13 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf/6/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      if ("padded_source_bounds" !== data0) {
        const err14 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf/6/const", keyword: "const", params: { allowedValue: "padded_source_bounds" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid0 = _errs19 === errors;
      valid3 = valid3 || _valid0;
      const _errs21 = errors;
      if (data0 !== null) {
        const err15 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf/7/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid0 = _errs21 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err16 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
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
    if (data.margin_mils !== void 0) {
      let data1 = data.margin_mils;
      const _errs24 = errors;
      let valid4 = false;
      const _errs25 = errors;
      if (typeof data1 == "number") {
        if (data1 < 0 || isNaN(data1)) {
          const err17 = { instancePath: instancePath + "/margin_mils", schemaPath: "#/$defs/Nonnegative/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err17];
          } else {
            vErrors.push(err17);
          }
          errors++;
        }
      } else {
        const err18 = { instancePath: instancePath + "/margin_mils", schemaPath: "#/$defs/Nonnegative/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
      var _valid1 = _errs25 === errors;
      valid4 = valid4 || _valid1;
      const _errs28 = errors;
      if (!validate24(data1, { instancePath: instancePath + "/margin_mils", parentData: data, parentDataProperty: "margin_mils", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate24.errors : vErrors.concat(validate24.errors);
        errors = vErrors.length;
      }
      var _valid1 = _errs28 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err19 = { instancePath: instancePath + "/margin_mils", schemaPath: "#/properties/margin_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      } else {
        errors = _errs24;
        if (vErrors !== null) {
          if (_errs24) {
            vErrors.length = _errs24;
          } else {
            vErrors = null;
          }
        }
      }
    }
  } else {
    const err20 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err20];
    } else {
      vErrors.push(err20);
    }
    errors++;
  }
  validate23.errors = vErrors;
  return errors === 0;
}
validate23.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.backend !== void 0) {
      let data0 = data.backend;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err1 = { instancePath: instancePath + "/backend", schemaPath: "#/properties/backend/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      if ("altium" !== data0) {
        const err2 = { instancePath: instancePath + "/backend", schemaPath: "#/properties/backend/anyOf/0/const", keyword: "const", params: { allowedValue: "altium" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid3 = valid3 || _valid0;
      const _errs9 = errors;
      if (data0 !== null) {
        const err3 = { instancePath: instancePath + "/backend", schemaPath: "#/properties/backend/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err4 = { instancePath: instancePath + "/backend", schemaPath: "#/properties/backend/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
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
    if (data.output_dir !== void 0) {
      let data1 = data.output_dir;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err5 = { instancePath: instancePath + "/output_dir", schemaPath: "#/properties/output_dir/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid1 = _errs13 === errors;
      valid4 = valid4 || _valid1;
      const _errs15 = errors;
      if (data1 !== null) {
        const err6 = { instancePath: instancePath + "/output_dir", schemaPath: "#/properties/output_dir/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err7 = { instancePath: instancePath + "/output_dir", schemaPath: "#/properties/output_dir/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.project_name !== void 0) {
      let data2 = data.project_name;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err8 = { instancePath: instancePath + "/project_name", schemaPath: "#/properties/project_name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err9 = { instancePath: instancePath + "/project_name", schemaPath: "#/properties/project_name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err10 = { instancePath: instancePath + "/project_name", schemaPath: "#/properties/project_name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.schematic_filename !== void 0) {
      let data3 = data.schematic_filename;
      const _errs24 = errors;
      let valid6 = false;
      const _errs25 = errors;
      if (typeof data3 !== "string") {
        const err11 = { instancePath: instancePath + "/schematic_filename", schemaPath: "#/properties/schematic_filename/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid3 = _errs25 === errors;
      valid6 = valid6 || _valid3;
      const _errs27 = errors;
      if (data3 !== null) {
        const err12 = { instancePath: instancePath + "/schematic_filename", schemaPath: "#/properties/schematic_filename/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid3 = _errs27 === errors;
      valid6 = valid6 || _valid3;
      if (!valid6) {
        const err13 = { instancePath: instancePath + "/schematic_filename", schemaPath: "#/properties/schematic_filename/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      } else {
        errors = _errs24;
        if (vErrors !== null) {
          if (_errs24) {
            vErrors.length = _errs24;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.schematic_sheet_style !== void 0) {
      let data4 = data.schematic_sheet_style;
      const _errs30 = errors;
      let valid7 = false;
      const _errs31 = errors;
      if (typeof data4 !== "string") {
        const err14 = { instancePath: instancePath + "/schematic_sheet_style", schemaPath: "#/properties/schematic_sheet_style/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid4 = _errs31 === errors;
      valid7 = valid7 || _valid4;
      const _errs33 = errors;
      if (data4 !== null) {
        const err15 = { instancePath: instancePath + "/schematic_sheet_style", schemaPath: "#/properties/schematic_sheet_style/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid4 = _errs33 === errors;
      valid7 = valid7 || _valid4;
      if (!valid7) {
        const err16 = { instancePath: instancePath + "/schematic_sheet_style", schemaPath: "#/properties/schematic_sheet_style/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      } else {
        errors = _errs30;
        if (vErrors !== null) {
          if (_errs30) {
            vErrors.length = _errs30;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.board_filename !== void 0) {
      let data5 = data.board_filename;
      const _errs36 = errors;
      let valid8 = false;
      const _errs37 = errors;
      if (typeof data5 !== "string") {
        const err17 = { instancePath: instancePath + "/board_filename", schemaPath: "#/properties/board_filename/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      var _valid5 = _errs37 === errors;
      valid8 = valid8 || _valid5;
      const _errs39 = errors;
      if (data5 !== null) {
        const err18 = { instancePath: instancePath + "/board_filename", schemaPath: "#/properties/board_filename/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
      var _valid5 = _errs39 === errors;
      valid8 = valid8 || _valid5;
      if (!valid8) {
        const err19 = { instancePath: instancePath + "/board_filename", schemaPath: "#/properties/board_filename/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      } else {
        errors = _errs36;
        if (vErrors !== null) {
          if (_errs36) {
            vErrors.length = _errs36;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.project_filename !== void 0) {
      let data6 = data.project_filename;
      const _errs42 = errors;
      let valid9 = false;
      const _errs43 = errors;
      if (typeof data6 !== "string") {
        const err20 = { instancePath: instancePath + "/project_filename", schemaPath: "#/properties/project_filename/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      var _valid6 = _errs43 === errors;
      valid9 = valid9 || _valid6;
      const _errs45 = errors;
      if (data6 !== null) {
        const err21 = { instancePath: instancePath + "/project_filename", schemaPath: "#/properties/project_filename/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      var _valid6 = _errs45 === errors;
      valid9 = valid9 || _valid6;
      if (!valid9) {
        const err22 = { instancePath: instancePath + "/project_filename", schemaPath: "#/properties/project_filename/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      } else {
        errors = _errs42;
        if (vErrors !== null) {
          if (_errs42) {
            vErrors.length = _errs42;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.origin !== void 0) {
      let data7 = data.origin;
      const _errs48 = errors;
      let valid10 = false;
      const _errs49 = errors;
      if (typeof data7 !== "string") {
        const err23 = { instancePath: instancePath + "/origin", schemaPath: "#/properties/origin/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      var _valid7 = _errs49 === errors;
      valid10 = valid10 || _valid7;
      const _errs51 = errors;
      if (data7 !== null) {
        const err24 = { instancePath: instancePath + "/origin", schemaPath: "#/properties/origin/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      var _valid7 = _errs51 === errors;
      valid10 = valid10 || _valid7;
      if (!valid10) {
        const err25 = { instancePath: instancePath + "/origin", schemaPath: "#/properties/origin/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      } else {
        errors = _errs48;
        if (vErrors !== null) {
          if (_errs48) {
            vErrors.length = _errs48;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.overwrite !== void 0) {
      let data8 = data.overwrite;
      const _errs54 = errors;
      let valid11 = false;
      const _errs55 = errors;
      if (typeof data8 !== "boolean") {
        const err26 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
      var _valid8 = _errs55 === errors;
      valid11 = valid11 || _valid8;
      const _errs57 = errors;
      if (data8 !== null) {
        const err27 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
      var _valid8 = _errs57 === errors;
      valid11 = valid11 || _valid8;
      if (!valid11) {
        const err28 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      } else {
        errors = _errs54;
        if (vErrors !== null) {
          if (_errs54) {
            vErrors.length = _errs54;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.layer_stack_template !== void 0) {
      let data9 = data.layer_stack_template;
      const _errs60 = errors;
      let valid12 = false;
      const _errs61 = errors;
      if (typeof data9 !== "string") {
        const err29 = { instancePath: instancePath + "/layer_stack_template", schemaPath: "#/properties/layer_stack_template/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      }
      var _valid9 = _errs61 === errors;
      valid12 = valid12 || _valid9;
      const _errs63 = errors;
      if (data9 !== null) {
        const err30 = { instancePath: instancePath + "/layer_stack_template", schemaPath: "#/properties/layer_stack_template/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
        }
        errors++;
      }
      var _valid9 = _errs63 === errors;
      valid12 = valid12 || _valid9;
      if (!valid12) {
        const err31 = { instancePath: instancePath + "/layer_stack_template", schemaPath: "#/properties/layer_stack_template/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      } else {
        errors = _errs60;
        if (vErrors !== null) {
          if (_errs60) {
            vErrors.length = _errs60;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.board_outline !== void 0) {
      let data10 = data.board_outline;
      const _errs66 = errors;
      let valid13 = false;
      const _errs67 = errors;
      if (!validate23(data10, { instancePath: instancePath + "/board_outline", parentData: data, parentDataProperty: "board_outline", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate23.errors : vErrors.concat(validate23.errors);
        errors = vErrors.length;
      }
      var _valid10 = _errs67 === errors;
      valid13 = valid13 || _valid10;
      const _errs68 = errors;
      if (data10 !== null) {
        const err32 = { instancePath: instancePath + "/board_outline", schemaPath: "#/properties/board_outline/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
        }
        errors++;
      }
      var _valid10 = _errs68 === errors;
      valid13 = valid13 || _valid10;
      if (!valid13) {
        const err33 = { instancePath: instancePath + "/board_outline", schemaPath: "#/properties/board_outline/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      } else {
        errors = _errs66;
        if (vErrors !== null) {
          if (_errs66) {
            vErrors.length = _errs66;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.board_outline_mils !== void 0) {
      let data11 = data.board_outline_mils;
      const _errs71 = errors;
      let valid14 = false;
      const _errs72 = errors;
      if (data11 && typeof data11 == "object" && !Array.isArray(data11)) {
        if (data11.left === void 0) {
          const err34 = { instancePath: instancePath + "/board_outline_mils", schemaPath: "#/$defs/Bounds/required", keyword: "required", params: { missingProperty: "left" }, message: "must have required property 'left'" };
          if (vErrors === null) {
            vErrors = [err34];
          } else {
            vErrors.push(err34);
          }
          errors++;
        }
        if (data11.bottom === void 0) {
          const err35 = { instancePath: instancePath + "/board_outline_mils", schemaPath: "#/$defs/Bounds/required", keyword: "required", params: { missingProperty: "bottom" }, message: "must have required property 'bottom'" };
          if (vErrors === null) {
            vErrors = [err35];
          } else {
            vErrors.push(err35);
          }
          errors++;
        }
        if (data11.right === void 0) {
          const err36 = { instancePath: instancePath + "/board_outline_mils", schemaPath: "#/$defs/Bounds/required", keyword: "required", params: { missingProperty: "right" }, message: "must have required property 'right'" };
          if (vErrors === null) {
            vErrors = [err36];
          } else {
            vErrors.push(err36);
          }
          errors++;
        }
        if (data11.top === void 0) {
          const err37 = { instancePath: instancePath + "/board_outline_mils", schemaPath: "#/$defs/Bounds/required", keyword: "required", params: { missingProperty: "top" }, message: "must have required property 'top'" };
          if (vErrors === null) {
            vErrors = [err37];
          } else {
            vErrors.push(err37);
          }
          errors++;
        }
        if (data11.left !== void 0) {
          if (!(typeof data11.left == "number")) {
            const err38 = { instancePath: instancePath + "/board_outline_mils/left", schemaPath: "#/$defs/Bounds/properties/left/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err38];
            } else {
              vErrors.push(err38);
            }
            errors++;
          }
        }
        if (data11.bottom !== void 0) {
          if (!(typeof data11.bottom == "number")) {
            const err39 = { instancePath: instancePath + "/board_outline_mils/bottom", schemaPath: "#/$defs/Bounds/properties/bottom/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err39];
            } else {
              vErrors.push(err39);
            }
            errors++;
          }
        }
        if (data11.right !== void 0) {
          if (!(typeof data11.right == "number")) {
            const err40 = { instancePath: instancePath + "/board_outline_mils/right", schemaPath: "#/$defs/Bounds/properties/right/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err40];
            } else {
              vErrors.push(err40);
            }
            errors++;
          }
        }
        if (data11.top !== void 0) {
          if (!(typeof data11.top == "number")) {
            const err41 = { instancePath: instancePath + "/board_outline_mils/top", schemaPath: "#/$defs/Bounds/properties/top/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err41];
            } else {
              vErrors.push(err41);
            }
            errors++;
          }
        }
        for (const key1 in data11) {
          if (key1 !== "left" && key1 !== "bottom" && key1 !== "right" && key1 !== "top") {
            const err42 = { instancePath: instancePath + "/board_outline_mils/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/Bounds/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err42];
            } else {
              vErrors.push(err42);
            }
            errors++;
          }
        }
      } else {
        const err43 = { instancePath: instancePath + "/board_outline_mils", schemaPath: "#/$defs/Bounds/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err43];
        } else {
          vErrors.push(err43);
        }
        errors++;
      }
      var _valid11 = _errs72 === errors;
      valid14 = valid14 || _valid11;
      const _errs86 = errors;
      if (data11 !== null) {
        const err44 = { instancePath: instancePath + "/board_outline_mils", schemaPath: "#/properties/board_outline_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err44];
        } else {
          vErrors.push(err44);
        }
        errors++;
      }
      var _valid11 = _errs86 === errors;
      valid14 = valid14 || _valid11;
      if (!valid14) {
        const err45 = { instancePath: instancePath + "/board_outline_mils", schemaPath: "#/properties/board_outline_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err45];
        } else {
          vErrors.push(err45);
        }
        errors++;
      } else {
        errors = _errs71;
        if (vErrors !== null) {
          if (_errs71) {
            vErrors.length = _errs71;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.board_origin_mils !== void 0) {
      let data17 = data.board_origin_mils;
      const _errs89 = errors;
      let valid18 = false;
      const _errs90 = errors;
      if (data17 && typeof data17 == "object" && !Array.isArray(data17)) {
        if (data17.x === void 0) {
          const err46 = { instancePath: instancePath + "/board_origin_mils", schemaPath: "#/$defs/Point/required", keyword: "required", params: { missingProperty: "x" }, message: "must have required property 'x'" };
          if (vErrors === null) {
            vErrors = [err46];
          } else {
            vErrors.push(err46);
          }
          errors++;
        }
        if (data17.y === void 0) {
          const err47 = { instancePath: instancePath + "/board_origin_mils", schemaPath: "#/$defs/Point/required", keyword: "required", params: { missingProperty: "y" }, message: "must have required property 'y'" };
          if (vErrors === null) {
            vErrors = [err47];
          } else {
            vErrors.push(err47);
          }
          errors++;
        }
        if (data17.x !== void 0) {
          if (!(typeof data17.x == "number")) {
            const err48 = { instancePath: instancePath + "/board_origin_mils/x", schemaPath: "#/$defs/Point/properties/x/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err48];
            } else {
              vErrors.push(err48);
            }
            errors++;
          }
        }
        if (data17.y !== void 0) {
          if (!(typeof data17.y == "number")) {
            const err49 = { instancePath: instancePath + "/board_origin_mils/y", schemaPath: "#/$defs/Point/properties/y/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err49];
            } else {
              vErrors.push(err49);
            }
            errors++;
          }
        }
        for (const key2 in data17) {
          if (key2 !== "x" && key2 !== "y") {
            const err50 = { instancePath: instancePath + "/board_origin_mils/" + key2.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/Point/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err50];
            } else {
              vErrors.push(err50);
            }
            errors++;
          }
        }
      } else {
        const err51 = { instancePath: instancePath + "/board_origin_mils", schemaPath: "#/$defs/Point/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err51];
        } else {
          vErrors.push(err51);
        }
        errors++;
      }
      var _valid12 = _errs90 === errors;
      valid18 = valid18 || _valid12;
      const _errs100 = errors;
      if (data17 !== null) {
        const err52 = { instancePath: instancePath + "/board_origin_mils", schemaPath: "#/properties/board_origin_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err52];
        } else {
          vErrors.push(err52);
        }
        errors++;
      }
      var _valid12 = _errs100 === errors;
      valid18 = valid18 || _valid12;
      if (!valid18) {
        const err53 = { instancePath: instancePath + "/board_origin_mils", schemaPath: "#/properties/board_origin_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err53];
        } else {
          vErrors.push(err53);
        }
        errors++;
      } else {
        errors = _errs89;
        if (vErrors !== null) {
          if (_errs89) {
            vErrors.length = _errs89;
          } else {
            vErrors = null;
          }
        }
      }
    }
  } else {
    const err54 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err54];
    } else {
      vErrors.push(err54);
    }
    errors++;
  }
  validate22.errors = vErrors;
  return errors === 0;
}
validate22.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate28(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate28.evaluated;
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
    if (data.roots !== void 0) {
      let data0 = data.roots;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err1 = { instancePath: instancePath + "/roots", schemaPath: "#/properties/roots/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid3 = valid3 || _valid0;
      const _errs9 = errors;
      if (Array.isArray(data0)) {
        const len0 = data0.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (typeof data0[i0] !== "string") {
            const err2 = { instancePath: instancePath + "/roots/" + i0, schemaPath: "#/$defs/StringArray/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err2];
            } else {
              vErrors.push(err2);
            }
            errors++;
          }
        }
      } else {
        const err3 = { instancePath: instancePath + "/roots", schemaPath: "#/$defs/StringArray/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs14 = errors;
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/roots", schemaPath: "#/properties/roots/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid0 = _errs14 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err5 = { instancePath: instancePath + "/roots", schemaPath: "#/properties/roots/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
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
    if (data.recursive !== void 0) {
      let data2 = data.recursive;
      const _errs17 = errors;
      let valid7 = false;
      const _errs18 = errors;
      if (typeof data2 !== "boolean") {
        const err6 = { instancePath: instancePath + "/recursive", schemaPath: "#/properties/recursive/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid1 = _errs18 === errors;
      valid7 = valid7 || _valid1;
      const _errs20 = errors;
      if (data2 !== null) {
        const err7 = { instancePath: instancePath + "/recursive", schemaPath: "#/properties/recursive/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid1 = _errs20 === errors;
      valid7 = valid7 || _valid1;
      if (!valid7) {
        const err8 = { instancePath: instancePath + "/recursive", schemaPath: "#/properties/recursive/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
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
  } else {
    const err9 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err9];
    } else {
      vErrors.push(err9);
    }
    errors++;
  }
  validate28.errors = vErrors;
  return errors === 0;
}
validate28.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate30(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate30.evaluated;
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
    if (data.manifest !== void 0) {
      let data0 = data.manifest;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err1 = { instancePath: instancePath + "/manifest", schemaPath: "#/properties/manifest/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid3 = valid3 || _valid0;
      const _errs9 = errors;
      if (data0 !== null) {
        const err2 = { instancePath: instancePath + "/manifest", schemaPath: "#/properties/manifest/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err3 = { instancePath: instancePath + "/manifest", schemaPath: "#/properties/manifest/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
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
    if (data.cache_dir !== void 0) {
      let data1 = data.cache_dir;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err4 = { instancePath: instancePath + "/cache_dir", schemaPath: "#/properties/cache_dir/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid1 = _errs13 === errors;
      valid4 = valid4 || _valid1;
      const _errs15 = errors;
      if (data1 !== null) {
        const err5 = { instancePath: instancePath + "/cache_dir", schemaPath: "#/properties/cache_dir/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err6 = { instancePath: instancePath + "/cache_dir", schemaPath: "#/properties/cache_dir/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
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
  } else {
    const err7 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err7];
    } else {
      vErrors.push(err7);
    }
    errors++;
  }
  validate30.errors = vErrors;
  return errors === 0;
}
validate30.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate33(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate33.evaluated;
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
    if (data.height_mils !== void 0) {
      let data0 = data.height_mils;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (!(typeof data0 == "number")) {
        const err1 = { instancePath: instancePath + "/height_mils", schemaPath: "#/properties/height_mils/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid3 = valid3 || _valid0;
      const _errs9 = errors;
      if (data0 !== null) {
        const err2 = { instancePath: instancePath + "/height_mils", schemaPath: "#/properties/height_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err3 = { instancePath: instancePath + "/height_mils", schemaPath: "#/properties/height_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
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
    if (data.layer !== void 0) {
      let data1 = data.layer;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err4 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid1 = _errs13 === errors;
      valid4 = valid4 || _valid1;
      const _errs15 = errors;
      if (!(typeof data1 == "number" && (!(data1 % 1) && !isNaN(data1)))) {
        const err5 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      valid4 = valid4 || _valid1;
      const _errs17 = errors;
      if (data1 !== null) {
        const err6 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid1 = _errs17 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err7 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.font_kind !== void 0) {
      let data2 = data.font_kind;
      const _errs20 = errors;
      let valid5 = false;
      const _errs21 = errors;
      if (typeof data2 !== "string") {
        const err8 = { instancePath: instancePath + "/font_kind", schemaPath: "#/properties/font_kind/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      const _errs23 = errors;
      if (data2 !== null) {
        const err9 = { instancePath: instancePath + "/font_kind", schemaPath: "#/properties/font_kind/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs23 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err10 = { instancePath: instancePath + "/font_kind", schemaPath: "#/properties/font_kind/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      } else {
        errors = _errs20;
        if (vErrors !== null) {
          if (_errs20) {
            vErrors.length = _errs20;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.font_name !== void 0) {
      let data3 = data.font_name;
      const _errs26 = errors;
      let valid6 = false;
      const _errs27 = errors;
      if (typeof data3 !== "string") {
        const err11 = { instancePath: instancePath + "/font_name", schemaPath: "#/properties/font_name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid3 = _errs27 === errors;
      valid6 = valid6 || _valid3;
      const _errs29 = errors;
      if (data3 !== null) {
        const err12 = { instancePath: instancePath + "/font_name", schemaPath: "#/properties/font_name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid3 = _errs29 === errors;
      valid6 = valid6 || _valid3;
      if (!valid6) {
        const err13 = { instancePath: instancePath + "/font_name", schemaPath: "#/properties/font_name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      } else {
        errors = _errs26;
        if (vErrors !== null) {
          if (_errs26) {
            vErrors.length = _errs26;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.bold !== void 0) {
      let data4 = data.bold;
      const _errs32 = errors;
      let valid7 = false;
      const _errs33 = errors;
      if (typeof data4 !== "boolean") {
        const err14 = { instancePath: instancePath + "/bold", schemaPath: "#/properties/bold/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid4 = _errs33 === errors;
      valid7 = valid7 || _valid4;
      const _errs35 = errors;
      if (data4 !== null) {
        const err15 = { instancePath: instancePath + "/bold", schemaPath: "#/properties/bold/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid4 = _errs35 === errors;
      valid7 = valid7 || _valid4;
      if (!valid7) {
        const err16 = { instancePath: instancePath + "/bold", schemaPath: "#/properties/bold/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      } else {
        errors = _errs32;
        if (vErrors !== null) {
          if (_errs32) {
            vErrors.length = _errs32;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.italic !== void 0) {
      let data5 = data.italic;
      const _errs38 = errors;
      let valid8 = false;
      const _errs39 = errors;
      if (typeof data5 !== "boolean") {
        const err17 = { instancePath: instancePath + "/italic", schemaPath: "#/properties/italic/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      var _valid5 = _errs39 === errors;
      valid8 = valid8 || _valid5;
      const _errs41 = errors;
      if (data5 !== null) {
        const err18 = { instancePath: instancePath + "/italic", schemaPath: "#/properties/italic/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
      var _valid5 = _errs41 === errors;
      valid8 = valid8 || _valid5;
      if (!valid8) {
        const err19 = { instancePath: instancePath + "/italic", schemaPath: "#/properties/italic/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      } else {
        errors = _errs38;
        if (vErrors !== null) {
          if (_errs38) {
            vErrors.length = _errs38;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.stroke_width_mils !== void 0) {
      let data6 = data.stroke_width_mils;
      const _errs44 = errors;
      let valid9 = false;
      const _errs45 = errors;
      if (!(typeof data6 == "number")) {
        const err20 = { instancePath: instancePath + "/stroke_width_mils", schemaPath: "#/properties/stroke_width_mils/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      var _valid6 = _errs45 === errors;
      valid9 = valid9 || _valid6;
      const _errs47 = errors;
      if (data6 !== null) {
        const err21 = { instancePath: instancePath + "/stroke_width_mils", schemaPath: "#/properties/stroke_width_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      var _valid6 = _errs47 === errors;
      valid9 = valid9 || _valid6;
      if (!valid9) {
        const err22 = { instancePath: instancePath + "/stroke_width_mils", schemaPath: "#/properties/stroke_width_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      } else {
        errors = _errs44;
        if (vErrors !== null) {
          if (_errs44) {
            vErrors.length = _errs44;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.text_justification !== void 0) {
      let data7 = data.text_justification;
      const _errs50 = errors;
      let valid10 = false;
      const _errs51 = errors;
      if (typeof data7 !== "string") {
        const err23 = { instancePath: instancePath + "/text_justification", schemaPath: "#/properties/text_justification/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      var _valid7 = _errs51 === errors;
      valid10 = valid10 || _valid7;
      const _errs53 = errors;
      if (!(typeof data7 == "number" && (!(data7 % 1) && !isNaN(data7)))) {
        const err24 = { instancePath: instancePath + "/text_justification", schemaPath: "#/properties/text_justification/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      var _valid7 = _errs53 === errors;
      valid10 = valid10 || _valid7;
      const _errs55 = errors;
      if (data7 !== null) {
        const err25 = { instancePath: instancePath + "/text_justification", schemaPath: "#/properties/text_justification/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
      var _valid7 = _errs55 === errors;
      valid10 = valid10 || _valid7;
      if (!valid10) {
        const err26 = { instancePath: instancePath + "/text_justification", schemaPath: "#/properties/text_justification/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      } else {
        errors = _errs50;
        if (vErrors !== null) {
          if (_errs50) {
            vErrors.length = _errs50;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.is_inverted !== void 0) {
      let data8 = data.is_inverted;
      const _errs58 = errors;
      let valid11 = false;
      const _errs59 = errors;
      if (typeof data8 !== "boolean") {
        const err27 = { instancePath: instancePath + "/is_inverted", schemaPath: "#/properties/is_inverted/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
      var _valid8 = _errs59 === errors;
      valid11 = valid11 || _valid8;
      const _errs61 = errors;
      if (data8 !== null) {
        const err28 = { instancePath: instancePath + "/is_inverted", schemaPath: "#/properties/is_inverted/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
      var _valid8 = _errs61 === errors;
      valid11 = valid11 || _valid8;
      if (!valid11) {
        const err29 = { instancePath: instancePath + "/is_inverted", schemaPath: "#/properties/is_inverted/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      } else {
        errors = _errs58;
        if (vErrors !== null) {
          if (_errs58) {
            vErrors.length = _errs58;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.inverted_margin_mils !== void 0) {
      let data9 = data.inverted_margin_mils;
      const _errs64 = errors;
      let valid12 = false;
      const _errs65 = errors;
      if (!(typeof data9 == "number")) {
        const err30 = { instancePath: instancePath + "/inverted_margin_mils", schemaPath: "#/properties/inverted_margin_mils/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
        }
        errors++;
      }
      var _valid9 = _errs65 === errors;
      valid12 = valid12 || _valid9;
      const _errs67 = errors;
      if (data9 !== null) {
        const err31 = { instancePath: instancePath + "/inverted_margin_mils", schemaPath: "#/properties/inverted_margin_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      }
      var _valid9 = _errs67 === errors;
      valid12 = valid12 || _valid9;
      if (!valid12) {
        const err32 = { instancePath: instancePath + "/inverted_margin_mils", schemaPath: "#/properties/inverted_margin_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
        }
        errors++;
      } else {
        errors = _errs64;
        if (vErrors !== null) {
          if (_errs64) {
            vErrors.length = _errs64;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.use_inverted_rectangle !== void 0) {
      let data10 = data.use_inverted_rectangle;
      const _errs70 = errors;
      let valid13 = false;
      const _errs71 = errors;
      if (typeof data10 !== "boolean") {
        const err33 = { instancePath: instancePath + "/use_inverted_rectangle", schemaPath: "#/properties/use_inverted_rectangle/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
      var _valid10 = _errs71 === errors;
      valid13 = valid13 || _valid10;
      const _errs73 = errors;
      if (data10 !== null) {
        const err34 = { instancePath: instancePath + "/use_inverted_rectangle", schemaPath: "#/properties/use_inverted_rectangle/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
        }
        errors++;
      }
      var _valid10 = _errs73 === errors;
      valid13 = valid13 || _valid10;
      if (!valid13) {
        const err35 = { instancePath: instancePath + "/use_inverted_rectangle", schemaPath: "#/properties/use_inverted_rectangle/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err35];
        } else {
          vErrors.push(err35);
        }
        errors++;
      } else {
        errors = _errs70;
        if (vErrors !== null) {
          if (_errs70) {
            vErrors.length = _errs70;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.is_frame !== void 0) {
      let data11 = data.is_frame;
      const _errs76 = errors;
      let valid14 = false;
      const _errs77 = errors;
      if (typeof data11 !== "boolean") {
        const err36 = { instancePath: instancePath + "/is_frame", schemaPath: "#/properties/is_frame/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err36];
        } else {
          vErrors.push(err36);
        }
        errors++;
      }
      var _valid11 = _errs77 === errors;
      valid14 = valid14 || _valid11;
      const _errs79 = errors;
      if (data11 !== null) {
        const err37 = { instancePath: instancePath + "/is_frame", schemaPath: "#/properties/is_frame/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err37];
        } else {
          vErrors.push(err37);
        }
        errors++;
      }
      var _valid11 = _errs79 === errors;
      valid14 = valid14 || _valid11;
      if (!valid14) {
        const err38 = { instancePath: instancePath + "/is_frame", schemaPath: "#/properties/is_frame/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err38];
        } else {
          vErrors.push(err38);
        }
        errors++;
      } else {
        errors = _errs76;
        if (vErrors !== null) {
          if (_errs76) {
            vErrors.length = _errs76;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.header_height_mils !== void 0) {
      let data12 = data.header_height_mils;
      const _errs82 = errors;
      let valid15 = false;
      const _errs83 = errors;
      if (!(typeof data12 == "number")) {
        const err39 = { instancePath: instancePath + "/header_height_mils", schemaPath: "#/properties/header_height_mils/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err39];
        } else {
          vErrors.push(err39);
        }
        errors++;
      }
      var _valid12 = _errs83 === errors;
      valid15 = valid15 || _valid12;
      const _errs85 = errors;
      if (data12 !== null) {
        const err40 = { instancePath: instancePath + "/header_height_mils", schemaPath: "#/properties/header_height_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err40];
        } else {
          vErrors.push(err40);
        }
        errors++;
      }
      var _valid12 = _errs85 === errors;
      valid15 = valid15 || _valid12;
      if (!valid15) {
        const err41 = { instancePath: instancePath + "/header_height_mils", schemaPath: "#/properties/header_height_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err41];
        } else {
          vErrors.push(err41);
        }
        errors++;
      } else {
        errors = _errs82;
        if (vErrors !== null) {
          if (_errs82) {
            vErrors.length = _errs82;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.header_stroke_width_mils !== void 0) {
      let data13 = data.header_stroke_width_mils;
      const _errs88 = errors;
      let valid16 = false;
      const _errs89 = errors;
      if (!(typeof data13 == "number")) {
        const err42 = { instancePath: instancePath + "/header_stroke_width_mils", schemaPath: "#/properties/header_stroke_width_mils/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err42];
        } else {
          vErrors.push(err42);
        }
        errors++;
      }
      var _valid13 = _errs89 === errors;
      valid16 = valid16 || _valid13;
      const _errs91 = errors;
      if (data13 !== null) {
        const err43 = { instancePath: instancePath + "/header_stroke_width_mils", schemaPath: "#/properties/header_stroke_width_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err43];
        } else {
          vErrors.push(err43);
        }
        errors++;
      }
      var _valid13 = _errs91 === errors;
      valid16 = valid16 || _valid13;
      if (!valid16) {
        const err44 = { instancePath: instancePath + "/header_stroke_width_mils", schemaPath: "#/properties/header_stroke_width_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err44];
        } else {
          vErrors.push(err44);
        }
        errors++;
      } else {
        errors = _errs88;
        if (vErrors !== null) {
          if (_errs88) {
            vErrors.length = _errs88;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.rotation_degrees !== void 0) {
      let data14 = data.rotation_degrees;
      const _errs94 = errors;
      let valid17 = false;
      const _errs95 = errors;
      if (!(typeof data14 == "number")) {
        const err45 = { instancePath: instancePath + "/rotation_degrees", schemaPath: "#/properties/rotation_degrees/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err45];
        } else {
          vErrors.push(err45);
        }
        errors++;
      }
      var _valid14 = _errs95 === errors;
      valid17 = valid17 || _valid14;
      const _errs97 = errors;
      if (data14 !== null) {
        const err46 = { instancePath: instancePath + "/rotation_degrees", schemaPath: "#/properties/rotation_degrees/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err46];
        } else {
          vErrors.push(err46);
        }
        errors++;
      }
      var _valid14 = _errs97 === errors;
      valid17 = valid17 || _valid14;
      if (!valid17) {
        const err47 = { instancePath: instancePath + "/rotation_degrees", schemaPath: "#/properties/rotation_degrees/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err47];
        } else {
          vErrors.push(err47);
        }
        errors++;
      } else {
        errors = _errs94;
        if (vErrors !== null) {
          if (_errs94) {
            vErrors.length = _errs94;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.stroke_font_type !== void 0) {
      let data15 = data.stroke_font_type;
      const _errs100 = errors;
      let valid18 = false;
      const _errs101 = errors;
      if (typeof data15 !== "string") {
        const err48 = { instancePath: instancePath + "/stroke_font_type", schemaPath: "#/properties/stroke_font_type/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err48];
        } else {
          vErrors.push(err48);
        }
        errors++;
      }
      var _valid15 = _errs101 === errors;
      valid18 = valid18 || _valid15;
      const _errs103 = errors;
      if (!(typeof data15 == "number" && (!(data15 % 1) && !isNaN(data15)))) {
        const err49 = { instancePath: instancePath + "/stroke_font_type", schemaPath: "#/properties/stroke_font_type/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err49];
        } else {
          vErrors.push(err49);
        }
        errors++;
      }
      var _valid15 = _errs103 === errors;
      valid18 = valid18 || _valid15;
      const _errs105 = errors;
      if (data15 !== null) {
        const err50 = { instancePath: instancePath + "/stroke_font_type", schemaPath: "#/properties/stroke_font_type/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err50];
        } else {
          vErrors.push(err50);
        }
        errors++;
      }
      var _valid15 = _errs105 === errors;
      valid18 = valid18 || _valid15;
      if (!valid18) {
        const err51 = { instancePath: instancePath + "/stroke_font_type", schemaPath: "#/properties/stroke_font_type/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err51];
        } else {
          vErrors.push(err51);
        }
        errors++;
      } else {
        errors = _errs100;
        if (vErrors !== null) {
          if (_errs100) {
            vErrors.length = _errs100;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.is_comment !== void 0) {
      let data16 = data.is_comment;
      const _errs108 = errors;
      let valid19 = false;
      const _errs109 = errors;
      if (typeof data16 !== "boolean") {
        const err52 = { instancePath: instancePath + "/is_comment", schemaPath: "#/properties/is_comment/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err52];
        } else {
          vErrors.push(err52);
        }
        errors++;
      }
      var _valid16 = _errs109 === errors;
      valid19 = valid19 || _valid16;
      const _errs111 = errors;
      if (data16 !== null) {
        const err53 = { instancePath: instancePath + "/is_comment", schemaPath: "#/properties/is_comment/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err53];
        } else {
          vErrors.push(err53);
        }
        errors++;
      }
      var _valid16 = _errs111 === errors;
      valid19 = valid19 || _valid16;
      if (!valid19) {
        const err54 = { instancePath: instancePath + "/is_comment", schemaPath: "#/properties/is_comment/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err54];
        } else {
          vErrors.push(err54);
        }
        errors++;
      } else {
        errors = _errs108;
        if (vErrors !== null) {
          if (_errs108) {
            vErrors.length = _errs108;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.is_designator !== void 0) {
      let data17 = data.is_designator;
      const _errs114 = errors;
      let valid20 = false;
      const _errs115 = errors;
      if (typeof data17 !== "boolean") {
        const err55 = { instancePath: instancePath + "/is_designator", schemaPath: "#/properties/is_designator/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err55];
        } else {
          vErrors.push(err55);
        }
        errors++;
      }
      var _valid17 = _errs115 === errors;
      valid20 = valid20 || _valid17;
      const _errs117 = errors;
      if (data17 !== null) {
        const err56 = { instancePath: instancePath + "/is_designator", schemaPath: "#/properties/is_designator/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err56];
        } else {
          vErrors.push(err56);
        }
        errors++;
      }
      var _valid17 = _errs117 === errors;
      valid20 = valid20 || _valid17;
      if (!valid20) {
        const err57 = { instancePath: instancePath + "/is_designator", schemaPath: "#/properties/is_designator/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err57];
        } else {
          vErrors.push(err57);
        }
        errors++;
      } else {
        errors = _errs114;
        if (vErrors !== null) {
          if (_errs114) {
            vErrors.length = _errs114;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.is_mirrored !== void 0) {
      let data18 = data.is_mirrored;
      const _errs120 = errors;
      let valid21 = false;
      const _errs121 = errors;
      if (typeof data18 !== "boolean") {
        const err58 = { instancePath: instancePath + "/is_mirrored", schemaPath: "#/properties/is_mirrored/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err58];
        } else {
          vErrors.push(err58);
        }
        errors++;
      }
      var _valid18 = _errs121 === errors;
      valid21 = valid21 || _valid18;
      const _errs123 = errors;
      if (data18 !== null) {
        const err59 = { instancePath: instancePath + "/is_mirrored", schemaPath: "#/properties/is_mirrored/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err59];
        } else {
          vErrors.push(err59);
        }
        errors++;
      }
      var _valid18 = _errs123 === errors;
      valid21 = valid21 || _valid18;
      if (!valid21) {
        const err60 = { instancePath: instancePath + "/is_mirrored", schemaPath: "#/properties/is_mirrored/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err60];
        } else {
          vErrors.push(err60);
        }
        errors++;
      } else {
        errors = _errs120;
        if (vErrors !== null) {
          if (_errs120) {
            vErrors.length = _errs120;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.barcode_kind !== void 0) {
      let data19 = data.barcode_kind;
      const _errs126 = errors;
      let valid22 = false;
      const _errs127 = errors;
      if (typeof data19 !== "string") {
        const err61 = { instancePath: instancePath + "/barcode_kind", schemaPath: "#/properties/barcode_kind/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err61];
        } else {
          vErrors.push(err61);
        }
        errors++;
      }
      var _valid19 = _errs127 === errors;
      valid22 = valid22 || _valid19;
      const _errs129 = errors;
      if (!(typeof data19 == "number" && (!(data19 % 1) && !isNaN(data19)))) {
        const err62 = { instancePath: instancePath + "/barcode_kind", schemaPath: "#/properties/barcode_kind/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err62];
        } else {
          vErrors.push(err62);
        }
        errors++;
      }
      var _valid19 = _errs129 === errors;
      valid22 = valid22 || _valid19;
      const _errs131 = errors;
      if (data19 !== null) {
        const err63 = { instancePath: instancePath + "/barcode_kind", schemaPath: "#/properties/barcode_kind/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err63];
        } else {
          vErrors.push(err63);
        }
        errors++;
      }
      var _valid19 = _errs131 === errors;
      valid22 = valid22 || _valid19;
      if (!valid22) {
        const err64 = { instancePath: instancePath + "/barcode_kind", schemaPath: "#/properties/barcode_kind/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err64];
        } else {
          vErrors.push(err64);
        }
        errors++;
      } else {
        errors = _errs126;
        if (vErrors !== null) {
          if (_errs126) {
            vErrors.length = _errs126;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.barcode_render_mode !== void 0) {
      let data20 = data.barcode_render_mode;
      const _errs134 = errors;
      let valid23 = false;
      const _errs135 = errors;
      if (typeof data20 !== "string") {
        const err65 = { instancePath: instancePath + "/barcode_render_mode", schemaPath: "#/properties/barcode_render_mode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err65];
        } else {
          vErrors.push(err65);
        }
        errors++;
      }
      var _valid20 = _errs135 === errors;
      valid23 = valid23 || _valid20;
      const _errs137 = errors;
      if (!(typeof data20 == "number" && (!(data20 % 1) && !isNaN(data20)))) {
        const err66 = { instancePath: instancePath + "/barcode_render_mode", schemaPath: "#/properties/barcode_render_mode/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err66];
        } else {
          vErrors.push(err66);
        }
        errors++;
      }
      var _valid20 = _errs137 === errors;
      valid23 = valid23 || _valid20;
      const _errs139 = errors;
      if (data20 !== null) {
        const err67 = { instancePath: instancePath + "/barcode_render_mode", schemaPath: "#/properties/barcode_render_mode/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err67];
        } else {
          vErrors.push(err67);
        }
        errors++;
      }
      var _valid20 = _errs139 === errors;
      valid23 = valid23 || _valid20;
      if (!valid23) {
        const err68 = { instancePath: instancePath + "/barcode_render_mode", schemaPath: "#/properties/barcode_render_mode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err68];
        } else {
          vErrors.push(err68);
        }
        errors++;
      } else {
        errors = _errs134;
        if (vErrors !== null) {
          if (_errs134) {
            vErrors.length = _errs134;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.barcode_full_size_mils !== void 0) {
      let data21 = data.barcode_full_size_mils;
      const _errs142 = errors;
      let valid24 = false;
      const _errs143 = errors;
      if (Array.isArray(data21)) {
        if (data21.length > 2) {
          const err69 = { instancePath: instancePath + "/barcode_full_size_mils", schemaPath: "#/$defs/Pair/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err69];
          } else {
            vErrors.push(err69);
          }
          errors++;
        }
        if (data21.length < 2) {
          const err70 = { instancePath: instancePath + "/barcode_full_size_mils", schemaPath: "#/$defs/Pair/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err70];
          } else {
            vErrors.push(err70);
          }
          errors++;
        }
        const len0 = data21.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!(typeof data21[i0] == "number")) {
            const err71 = { instancePath: instancePath + "/barcode_full_size_mils/" + i0, schemaPath: "#/$defs/Pair/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err71];
            } else {
              vErrors.push(err71);
            }
            errors++;
          }
        }
      } else {
        const err72 = { instancePath: instancePath + "/barcode_full_size_mils", schemaPath: "#/$defs/Pair/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err72];
        } else {
          vErrors.push(err72);
        }
        errors++;
      }
      var _valid21 = _errs143 === errors;
      valid24 = valid24 || _valid21;
      const _errs148 = errors;
      if (data21 !== null) {
        const err73 = { instancePath: instancePath + "/barcode_full_size_mils", schemaPath: "#/properties/barcode_full_size_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err73];
        } else {
          vErrors.push(err73);
        }
        errors++;
      }
      var _valid21 = _errs148 === errors;
      valid24 = valid24 || _valid21;
      if (!valid24) {
        const err74 = { instancePath: instancePath + "/barcode_full_size_mils", schemaPath: "#/properties/barcode_full_size_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err74];
        } else {
          vErrors.push(err74);
        }
        errors++;
      } else {
        errors = _errs142;
        if (vErrors !== null) {
          if (_errs142) {
            vErrors.length = _errs142;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.barcode_margin_mils !== void 0) {
      let data23 = data.barcode_margin_mils;
      const _errs151 = errors;
      let valid28 = false;
      const _errs152 = errors;
      if (Array.isArray(data23)) {
        if (data23.length > 2) {
          const err75 = { instancePath: instancePath + "/barcode_margin_mils", schemaPath: "#/$defs/Pair/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err75];
          } else {
            vErrors.push(err75);
          }
          errors++;
        }
        if (data23.length < 2) {
          const err76 = { instancePath: instancePath + "/barcode_margin_mils", schemaPath: "#/$defs/Pair/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err76];
          } else {
            vErrors.push(err76);
          }
          errors++;
        }
        const len1 = data23.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (!(typeof data23[i1] == "number")) {
            const err77 = { instancePath: instancePath + "/barcode_margin_mils/" + i1, schemaPath: "#/$defs/Pair/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err77];
            } else {
              vErrors.push(err77);
            }
            errors++;
          }
        }
      } else {
        const err78 = { instancePath: instancePath + "/barcode_margin_mils", schemaPath: "#/$defs/Pair/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err78];
        } else {
          vErrors.push(err78);
        }
        errors++;
      }
      var _valid22 = _errs152 === errors;
      valid28 = valid28 || _valid22;
      const _errs157 = errors;
      if (data23 !== null) {
        const err79 = { instancePath: instancePath + "/barcode_margin_mils", schemaPath: "#/properties/barcode_margin_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err79];
        } else {
          vErrors.push(err79);
        }
        errors++;
      }
      var _valid22 = _errs157 === errors;
      valid28 = valid28 || _valid22;
      if (!valid28) {
        const err80 = { instancePath: instancePath + "/barcode_margin_mils", schemaPath: "#/properties/barcode_margin_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err80];
        } else {
          vErrors.push(err80);
        }
        errors++;
      } else {
        errors = _errs151;
        if (vErrors !== null) {
          if (_errs151) {
            vErrors.length = _errs151;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.barcode_min_width_mils !== void 0) {
      let data25 = data.barcode_min_width_mils;
      const _errs160 = errors;
      let valid32 = false;
      const _errs161 = errors;
      if (!(typeof data25 == "number")) {
        const err81 = { instancePath: instancePath + "/barcode_min_width_mils", schemaPath: "#/properties/barcode_min_width_mils/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err81];
        } else {
          vErrors.push(err81);
        }
        errors++;
      }
      var _valid23 = _errs161 === errors;
      valid32 = valid32 || _valid23;
      const _errs163 = errors;
      if (data25 !== null) {
        const err82 = { instancePath: instancePath + "/barcode_min_width_mils", schemaPath: "#/properties/barcode_min_width_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err82];
        } else {
          vErrors.push(err82);
        }
        errors++;
      }
      var _valid23 = _errs163 === errors;
      valid32 = valid32 || _valid23;
      if (!valid32) {
        const err83 = { instancePath: instancePath + "/barcode_min_width_mils", schemaPath: "#/properties/barcode_min_width_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err83];
        } else {
          vErrors.push(err83);
        }
        errors++;
      } else {
        errors = _errs160;
        if (vErrors !== null) {
          if (_errs160) {
            vErrors.length = _errs160;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.barcode_show_text !== void 0) {
      let data26 = data.barcode_show_text;
      const _errs166 = errors;
      let valid33 = false;
      const _errs167 = errors;
      if (typeof data26 !== "boolean") {
        const err84 = { instancePath: instancePath + "/barcode_show_text", schemaPath: "#/properties/barcode_show_text/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err84];
        } else {
          vErrors.push(err84);
        }
        errors++;
      }
      var _valid24 = _errs167 === errors;
      valid33 = valid33 || _valid24;
      const _errs169 = errors;
      if (data26 !== null) {
        const err85 = { instancePath: instancePath + "/barcode_show_text", schemaPath: "#/properties/barcode_show_text/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err85];
        } else {
          vErrors.push(err85);
        }
        errors++;
      }
      var _valid24 = _errs169 === errors;
      valid33 = valid33 || _valid24;
      if (!valid33) {
        const err86 = { instancePath: instancePath + "/barcode_show_text", schemaPath: "#/properties/barcode_show_text/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err86];
        } else {
          vErrors.push(err86);
        }
        errors++;
      } else {
        errors = _errs166;
        if (vErrors !== null) {
          if (_errs166) {
            vErrors.length = _errs166;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.barcode_inverted !== void 0) {
      let data27 = data.barcode_inverted;
      const _errs172 = errors;
      let valid34 = false;
      const _errs173 = errors;
      if (typeof data27 !== "boolean") {
        const err87 = { instancePath: instancePath + "/barcode_inverted", schemaPath: "#/properties/barcode_inverted/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err87];
        } else {
          vErrors.push(err87);
        }
        errors++;
      }
      var _valid25 = _errs173 === errors;
      valid34 = valid34 || _valid25;
      const _errs175 = errors;
      if (data27 !== null) {
        const err88 = { instancePath: instancePath + "/barcode_inverted", schemaPath: "#/properties/barcode_inverted/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err88];
        } else {
          vErrors.push(err88);
        }
        errors++;
      }
      var _valid25 = _errs175 === errors;
      valid34 = valid34 || _valid25;
      if (!valid34) {
        const err89 = { instancePath: instancePath + "/barcode_inverted", schemaPath: "#/properties/barcode_inverted/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err89];
        } else {
          vErrors.push(err89);
        }
        errors++;
      } else {
        errors = _errs172;
        if (vErrors !== null) {
          if (_errs172) {
            vErrors.length = _errs172;
          } else {
            vErrors = null;
          }
        }
      }
    }
  } else {
    const err90 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err90];
    } else {
      vErrors.push(err90);
    }
    errors++;
  }
  validate33.errors = vErrors;
  return errors === 0;
}
validate33.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate32(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate32.evaluated;
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
    if (data.enabled !== void 0) {
      let data0 = data.enabled;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "boolean") {
        const err1 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid3 = valid3 || _valid0;
      const _errs9 = errors;
      if (data0 !== null) {
        const err2 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err3 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
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
    if (data.placement !== void 0) {
      let data1 = data.placement;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err4 = { instancePath: instancePath + "/placement", schemaPath: "#/properties/placement/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      if ("above_component" !== data1) {
        const err5 = { instancePath: instancePath + "/placement", schemaPath: "#/properties/placement/anyOf/0/const", keyword: "const", params: { allowedValue: "above_component" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid1 = _errs13 === errors;
      valid4 = valid4 || _valid1;
      const _errs15 = errors;
      if (data1 !== null) {
        const err6 = { instancePath: instancePath + "/placement", schemaPath: "#/properties/placement/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err7 = { instancePath: instancePath + "/placement", schemaPath: "#/properties/placement/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.offset_mils !== void 0) {
      let data2 = data.offset_mils;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (Array.isArray(data2)) {
        if (data2.length > 2) {
          const err8 = { instancePath: instancePath + "/offset_mils", schemaPath: "#/$defs/Pair/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err8];
          } else {
            vErrors.push(err8);
          }
          errors++;
        }
        if (data2.length < 2) {
          const err9 = { instancePath: instancePath + "/offset_mils", schemaPath: "#/$defs/Pair/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err9];
          } else {
            vErrors.push(err9);
          }
          errors++;
        }
        const len0 = data2.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!(typeof data2[i0] == "number")) {
            const err10 = { instancePath: instancePath + "/offset_mils/" + i0, schemaPath: "#/$defs/Pair/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err10];
            } else {
              vErrors.push(err10);
            }
            errors++;
          }
        }
      } else {
        const err11 = { instancePath: instancePath + "/offset_mils", schemaPath: "#/$defs/Pair/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs24 = errors;
      if (data2 !== null) {
        const err12 = { instancePath: instancePath + "/offset_mils", schemaPath: "#/properties/offset_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid2 = _errs24 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err13 = { instancePath: instancePath + "/offset_mils", schemaPath: "#/properties/offset_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
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
    if (data.width_factor !== void 0) {
      let data4 = data.width_factor;
      const _errs27 = errors;
      let valid9 = false;
      const _errs28 = errors;
      if (!(typeof data4 == "number")) {
        const err14 = { instancePath: instancePath + "/width_factor", schemaPath: "#/properties/width_factor/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid3 = _errs28 === errors;
      valid9 = valid9 || _valid3;
      const _errs30 = errors;
      if (data4 !== null) {
        const err15 = { instancePath: instancePath + "/width_factor", schemaPath: "#/properties/width_factor/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid3 = _errs30 === errors;
      valid9 = valid9 || _valid3;
      if (!valid9) {
        const err16 = { instancePath: instancePath + "/width_factor", schemaPath: "#/properties/width_factor/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      } else {
        errors = _errs27;
        if (vErrors !== null) {
          if (_errs27) {
            vErrors.length = _errs27;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.style !== void 0) {
      if (!validate33(data.style, { instancePath: instancePath + "/style", parentData: data, parentDataProperty: "style", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate33.errors : vErrors.concat(validate33.errors);
        errors = vErrors.length;
      }
    }
  } else {
    const err17 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err17];
    } else {
      vErrors.push(err17);
    }
    errors++;
  }
  validate32.errors = vErrors;
  return errors === 0;
}
validate32.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
var func1 = require_ucs2length().default;
function validate38(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate38.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.color !== void 0) {
      let data0 = data.color;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err0 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err0];
          } else {
            vErrors.push(err0);
          }
          errors++;
        }
      } else {
        const err1 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
    }
    if (data.cutout_color !== void 0) {
      let data1 = data.cutout_color;
      if (typeof data1 === "string") {
        if (func1(data1) < 1) {
          const err2 = { instancePath: instancePath + "/cutout_color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err2];
          } else {
            vErrors.push(err2);
          }
          errors++;
        }
      } else {
        const err3 = { instancePath: instancePath + "/cutout_color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.cutouts_color !== void 0) {
      let data2 = data.cutouts_color;
      if (typeof data2 === "string") {
        if (func1(data2) < 1) {
          const err4 = { instancePath: instancePath + "/cutouts_color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err4];
          } else {
            vErrors.push(err4);
          }
          errors++;
        }
      } else {
        const err5 = { instancePath: instancePath + "/cutouts_color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.cutouts !== void 0) {
      if (typeof data.cutouts !== "boolean") {
        const err6 = { instancePath: instancePath + "/cutouts", schemaPath: "#/properties/cutouts/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.width_mm !== void 0) {
      let data4 = data.width_mm;
      if (typeof data4 == "number") {
        if (data4 < 0 || isNaN(data4)) {
          const err7 = { instancePath: instancePath + "/width_mm", schemaPath: "#/properties/width_mm/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err7];
          } else {
            vErrors.push(err7);
          }
          errors++;
        }
      } else {
        const err8 = { instancePath: instancePath + "/width_mm", schemaPath: "#/properties/width_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
    if (data.fuse !== void 0) {
      if (typeof data.fuse !== "boolean") {
        const err9 = { instancePath: instancePath + "/fuse", schemaPath: "#/properties/fuse/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    for (const key0 in data) {
      if (key0 !== "color" && key0 !== "cutout_color" && key0 !== "cutouts_color" && key0 !== "cutouts" && key0 !== "width_mm" && key0 !== "fuse") {
        const err10 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
    }
  } else {
    const err11 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err11];
    } else {
      vErrors.push(err11);
    }
    errors++;
  }
  validate38.errors = vErrors;
  return errors === 0;
}
validate38.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate41(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate41.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.color !== void 0) {
      let data0 = data.color;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err0 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err0];
          } else {
            vErrors.push(err0);
          }
          errors++;
        }
      } else {
        const err1 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
    }
    for (const key0 in data) {
      if (key0 !== "color") {
        const err2 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
  } else {
    const err3 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err3];
    } else {
      vErrors.push(err3);
    }
    errors++;
  }
  validate41.errors = vErrors;
  return errors === 0;
}
validate41.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate44(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate44.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.enabled !== void 0) {
      if (typeof data.enabled !== "boolean") {
        const err0 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err0];
        } else {
          vErrors.push(err0);
        }
        errors++;
      }
    }
    if (data.color !== void 0) {
      let data1 = data.color;
      if (typeof data1 === "string") {
        if (func1(data1) < 1) {
          const err1 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err1];
          } else {
            vErrors.push(err1);
          }
          errors++;
        }
      } else {
        const err2 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
    if (data.step_body_name !== void 0) {
      let data2 = data.step_body_name;
      if (typeof data2 === "string") {
        if (func1(data2) < 1) {
          const err3 = { instancePath: instancePath + "/step_body_name", schemaPath: "#/properties/step_body_name/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/step_body_name", schemaPath: "#/properties/step_body_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.thickness_bias_mm !== void 0) {
      let data3 = data.thickness_bias_mm;
      if (typeof data3 == "number") {
        if (data3 < 0 || isNaN(data3)) {
          const err5 = { instancePath: instancePath + "/thickness_bias_mm", schemaPath: "#/properties/thickness_bias_mm/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err5];
          } else {
            vErrors.push(err5);
          }
          errors++;
        }
      } else {
        const err6 = { instancePath: instancePath + "/thickness_bias_mm", schemaPath: "#/properties/thickness_bias_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    for (const key0 in data) {
      if (key0 !== "enabled" && key0 !== "color" && key0 !== "step_body_name" && key0 !== "thickness_bias_mm") {
        const err7 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
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
  validate44.errors = vErrors;
  return errors === 0;
}
validate44.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate43(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate43.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  const _errs0 = errors;
  let valid0 = false;
  let passing0 = null;
  const _errs1 = errors;
  if (typeof data !== "boolean") {
    const err0 = { instancePath, schemaPath: "#/oneOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
    if (vErrors === null) {
      vErrors = [err0];
    } else {
      vErrors.push(err0);
    }
    errors++;
  }
  var _valid0 = _errs1 === errors;
  if (_valid0) {
    valid0 = true;
    passing0 = 0;
  }
  const _errs3 = errors;
  if (!validate44(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate44.errors : vErrors.concat(validate44.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs3 === errors;
  if (_valid0 && valid0) {
    valid0 = false;
    passing0 = [passing0, 1];
  } else {
    if (_valid0) {
      valid0 = true;
      passing0 = 1;
      var props0 = true;
    }
  }
  if (!valid0) {
    const err1 = { instancePath, schemaPath: "#/oneOf", keyword: "oneOf", params: { passingSchemas: passing0 }, message: "must match exactly one schema in oneOf" };
    if (vErrors === null) {
      vErrors = [err1];
    } else {
      vErrors.push(err1);
    }
    errors++;
  } else {
    errors = _errs0;
    if (vErrors !== null) {
      if (_errs0) {
        vErrors.length = _errs0;
      } else {
        vErrors = null;
      }
    }
  }
  validate43.errors = vErrors;
  evaluated0.props = props0;
  return errors === 0;
}
validate43.evaluated = { "dynamicProps": true, "dynamicItems": false };
function validate58(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate58.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.designators === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "designators" }, message: "must have required property 'designators'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.color === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "color" }, message: "must have required property 'color'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.designators !== void 0) {
      let data0 = data.designators;
      const _errs3 = errors;
      let valid2 = false;
      let passing0 = null;
      const _errs4 = errors;
      if (typeof data0 !== "string") {
        const err2 = { instancePath: instancePath + "/designators", schemaPath: "#/$defs/StringList/oneOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs4 === errors;
      if (_valid0) {
        valid2 = true;
        passing0 = 0;
      }
      const _errs6 = errors;
      if (Array.isArray(data0)) {
        const len0 = data0.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (typeof data0[i0] !== "string") {
            const err3 = { instancePath: instancePath + "/designators/" + i0, schemaPath: "#/$defs/StringList/oneOf/1/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err3];
            } else {
              vErrors.push(err3);
            }
            errors++;
          }
        }
      } else {
        const err4 = { instancePath: instancePath + "/designators", schemaPath: "#/$defs/StringList/oneOf/1/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid0 = _errs6 === errors;
      if (_valid0 && valid2) {
        valid2 = false;
        passing0 = [passing0, 1];
      } else {
        if (_valid0) {
          valid2 = true;
          passing0 = 1;
        }
      }
      if (!valid2) {
        const err5 = { instancePath: instancePath + "/designators", schemaPath: "#/$defs/StringList/oneOf", keyword: "oneOf", params: { passingSchemas: passing0 }, message: "must match exactly one schema in oneOf" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      } else {
        errors = _errs3;
        if (vErrors !== null) {
          if (_errs3) {
            vErrors.length = _errs3;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.color !== void 0) {
      let data2 = data.color;
      if (typeof data2 === "string") {
        if (func1(data2) < 1) {
          const err6 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err6];
          } else {
            vErrors.push(err6);
          }
          errors++;
        }
      } else {
        const err7 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.step_body_name !== void 0) {
      let data3 = data.step_body_name;
      if (typeof data3 === "string") {
        if (func1(data3) < 1) {
          const err8 = { instancePath: instancePath + "/step_body_name", schemaPath: "#/properties/step_body_name/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err8];
          } else {
            vErrors.push(err8);
          }
          errors++;
        }
      } else {
        const err9 = { instancePath: instancePath + "/step_body_name", schemaPath: "#/properties/step_body_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    for (const key0 in data) {
      if (key0 !== "designators" && key0 !== "color" && key0 !== "step_body_name") {
        const err10 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
    }
  } else {
    const err11 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err11];
    } else {
      vErrors.push(err11);
    }
    errors++;
  }
  validate58.errors = vErrors;
  return errors === 0;
}
validate58.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate57(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate57.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (Array.isArray(data)) {
    const len0 = data.length;
    for (let i0 = 0; i0 < len0; i0++) {
      if (!validate58(data[i0], { instancePath: instancePath + "/" + i0, parentData: data, parentDataProperty: i0, rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate58.errors : vErrors.concat(validate58.errors);
        errors = vErrors.length;
      }
    }
  } else {
    const err0 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "array" }, message: "must be array" };
    if (vErrors === null) {
      vErrors = [err0];
    } else {
      vErrors.push(err0);
    }
    errors++;
  }
  validate57.errors = vErrors;
  return errors === 0;
}
validate57.evaluated = { "items": true, "dynamicProps": false, "dynamicItems": false };
function validate56(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate56.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.enabled !== void 0) {
      if (typeof data.enabled !== "boolean") {
        const err0 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err0];
        } else {
          vErrors.push(err0);
        }
        errors++;
      }
    }
    if (data.mode !== void 0) {
      let data1 = data.mode;
      const _errs4 = errors;
      let valid1 = false;
      const _errs5 = errors;
      if (typeof data1 !== "string") {
        const err1 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      if ("none" !== data1) {
        const err2 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf/0/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs5 === errors;
      valid1 = valid1 || _valid0;
      const _errs7 = errors;
      if (typeof data1 !== "string") {
        const err3 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      if ("all" !== data1) {
        const err4 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf/1/const", keyword: "const", params: { allowedValue: "all" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid1 = valid1 || _valid0;
      const _errs9 = errors;
      if (typeof data1 !== "string") {
        const err5 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      if ("matching_designators" !== data1) {
        const err6 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf/2/const", keyword: "const", params: { allowedValue: "matching_designators" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid1 = valid1 || _valid0;
      if (!valid1) {
        const err7 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
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
    if (data.include_designators !== void 0) {
      let data2 = data.include_designators;
      const _errs13 = errors;
      let valid3 = false;
      let passing0 = null;
      const _errs14 = errors;
      if (typeof data2 !== "string") {
        const err8 = { instancePath: instancePath + "/include_designators", schemaPath: "#/$defs/StringList/oneOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid1 = _errs14 === errors;
      if (_valid1) {
        valid3 = true;
        passing0 = 0;
      }
      const _errs16 = errors;
      if (Array.isArray(data2)) {
        const len0 = data2.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (typeof data2[i0] !== "string") {
            const err9 = { instancePath: instancePath + "/include_designators/" + i0, schemaPath: "#/$defs/StringList/oneOf/1/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err9];
            } else {
              vErrors.push(err9);
            }
            errors++;
          }
        }
      } else {
        const err10 = { instancePath: instancePath + "/include_designators", schemaPath: "#/$defs/StringList/oneOf/1/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid1 = _errs16 === errors;
      if (_valid1 && valid3) {
        valid3 = false;
        passing0 = [passing0, 1];
      } else {
        if (_valid1) {
          valid3 = true;
          passing0 = 1;
        }
      }
      if (!valid3) {
        const err11 = { instancePath: instancePath + "/include_designators", schemaPath: "#/$defs/StringList/oneOf", keyword: "oneOf", params: { passingSchemas: passing0 }, message: "must match exactly one schema in oneOf" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      } else {
        errors = _errs13;
        if (vErrors !== null) {
          if (_errs13) {
            vErrors.length = _errs13;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.color !== void 0) {
      let data4 = data.color;
      if (typeof data4 === "string") {
        if (func1(data4) < 1) {
          const err12 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err12];
          } else {
            vErrors.push(err12);
          }
          errors++;
        }
      } else {
        const err13 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.step_body_name !== void 0) {
      let data5 = data.step_body_name;
      if (typeof data5 === "string") {
        if (func1(data5) < 1) {
          const err14 = { instancePath: instancePath + "/step_body_name", schemaPath: "#/properties/step_body_name/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err14];
          } else {
            vErrors.push(err14);
          }
          errors++;
        }
      } else {
        const err15 = { instancePath: instancePath + "/step_body_name", schemaPath: "#/properties/step_body_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
    }
    if (data.thickness_bias_mm !== void 0) {
      let data6 = data.thickness_bias_mm;
      if (typeof data6 == "number") {
        if (data6 < 0 || isNaN(data6)) {
          const err16 = { instancePath: instancePath + "/thickness_bias_mm", schemaPath: "#/properties/thickness_bias_mm/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err16];
          } else {
            vErrors.push(err16);
          }
          errors++;
        }
      } else {
        const err17 = { instancePath: instancePath + "/thickness_bias_mm", schemaPath: "#/properties/thickness_bias_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
    }
    if (data.highlight_rules !== void 0) {
      if (!validate57(data.highlight_rules, { instancePath: instancePath + "/highlight_rules", parentData: data, parentDataProperty: "highlight_rules", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate57.errors : vErrors.concat(validate57.errors);
        errors = vErrors.length;
      }
    }
    for (const key0 in data) {
      if (key0 !== "enabled" && key0 !== "mode" && key0 !== "include_designators" && key0 !== "color" && key0 !== "step_body_name" && key0 !== "thickness_bias_mm" && key0 !== "highlight_rules") {
        const err18 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
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
  validate56.errors = vErrors;
  return errors === 0;
}
validate56.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate55(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate55.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  const _errs0 = errors;
  let valid0 = false;
  let passing0 = null;
  const _errs1 = errors;
  if (typeof data !== "boolean") {
    const err0 = { instancePath, schemaPath: "#/oneOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
    if (vErrors === null) {
      vErrors = [err0];
    } else {
      vErrors.push(err0);
    }
    errors++;
  }
  var _valid0 = _errs1 === errors;
  if (_valid0) {
    valid0 = true;
    passing0 = 0;
  }
  const _errs3 = errors;
  if (!validate56(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate56.errors : vErrors.concat(validate56.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs3 === errors;
  if (_valid0 && valid0) {
    valid0 = false;
    passing0 = [passing0, 1];
  } else {
    if (_valid0) {
      valid0 = true;
      passing0 = 1;
      var props0 = true;
    }
  }
  if (!valid0) {
    const err1 = { instancePath, schemaPath: "#/oneOf", keyword: "oneOf", params: { passingSchemas: passing0 }, message: "must match exactly one schema in oneOf" };
    if (vErrors === null) {
      vErrors = [err1];
    } else {
      vErrors.push(err1);
    }
    errors++;
  } else {
    errors = _errs0;
    if (vErrors !== null) {
      if (_errs0) {
        vErrors.length = _errs0;
      } else {
        vErrors = null;
      }
    }
  }
  validate55.errors = vErrors;
  evaluated0.props = props0;
  return errors === 0;
}
validate55.evaluated = { "dynamicProps": true, "dynamicItems": false };
function validate40(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate40.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.defaults !== void 0) {
      if (!validate41(data.defaults, { instancePath: instancePath + "/defaults", parentData: data, parentDataProperty: "defaults", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate41.errors : vErrors.concat(validate41.errors);
        errors = vErrors.length;
      }
    }
    if (data.tracks !== void 0) {
      if (!validate43(data.tracks, { instancePath: instancePath + "/tracks", parentData: data, parentDataProperty: "tracks", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate43.errors : vErrors.concat(validate43.errors);
        errors = vErrors.length;
      }
    }
    if (data.traces !== void 0) {
      if (!validate43(data.traces, { instancePath: instancePath + "/traces", parentData: data, parentDataProperty: "traces", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate43.errors : vErrors.concat(validate43.errors);
        errors = vErrors.length;
      }
    }
    if (data.arcs !== void 0) {
      if (!validate43(data.arcs, { instancePath: instancePath + "/arcs", parentData: data, parentDataProperty: "arcs", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate43.errors : vErrors.concat(validate43.errors);
        errors = vErrors.length;
      }
    }
    if (data.fills !== void 0) {
      if (!validate43(data.fills, { instancePath: instancePath + "/fills", parentData: data, parentDataProperty: "fills", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate43.errors : vErrors.concat(validate43.errors);
        errors = vErrors.length;
      }
    }
    if (data.polygons !== void 0) {
      if (!validate43(data.polygons, { instancePath: instancePath + "/polygons", parentData: data, parentDataProperty: "polygons", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate43.errors : vErrors.concat(validate43.errors);
        errors = vErrors.length;
      }
    }
    if (data.poured_polygons !== void 0) {
      if (!validate43(data.poured_polygons, { instancePath: instancePath + "/poured_polygons", parentData: data, parentDataProperty: "poured_polygons", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate43.errors : vErrors.concat(validate43.errors);
        errors = vErrors.length;
      }
    }
    if (data.regions !== void 0) {
      if (!validate43(data.regions, { instancePath: instancePath + "/regions", parentData: data, parentDataProperty: "regions", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate43.errors : vErrors.concat(validate43.errors);
        errors = vErrors.length;
      }
    }
    if (data.shapebased_regions !== void 0) {
      if (!validate43(data.shapebased_regions, { instancePath: instancePath + "/shapebased_regions", parentData: data, parentDataProperty: "shapebased_regions", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate43.errors : vErrors.concat(validate43.errors);
        errors = vErrors.length;
      }
    }
    if (data.vias !== void 0) {
      if (!validate43(data.vias, { instancePath: instancePath + "/vias", parentData: data, parentDataProperty: "vias", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate43.errors : vErrors.concat(validate43.errors);
        errors = vErrors.length;
      }
    }
    if (data.component_pads !== void 0) {
      if (!validate55(data.component_pads, { instancePath: instancePath + "/component_pads", parentData: data, parentDataProperty: "component_pads", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate55.errors : vErrors.concat(validate55.errors);
        errors = vErrors.length;
      }
    }
    if (data.free_pads !== void 0) {
      if (!validate43(data.free_pads, { instancePath: instancePath + "/free_pads", parentData: data, parentDataProperty: "free_pads", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate43.errors : vErrors.concat(validate43.errors);
        errors = vErrors.length;
      }
    }
    for (const key0 in data) {
      if (key0 !== "defaults" && key0 !== "tracks" && key0 !== "traces" && key0 !== "arcs" && key0 !== "fills" && key0 !== "polygons" && key0 !== "poured_polygons" && key0 !== "regions" && key0 !== "shapebased_regions" && key0 !== "vias" && key0 !== "component_pads" && key0 !== "free_pads") {
        const err0 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err0];
        } else {
          vErrors.push(err0);
        }
        errors++;
      }
    }
  } else {
    const err1 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err1];
    } else {
      vErrors.push(err1);
    }
    errors++;
  }
  validate40.errors = vErrors;
  return errors === 0;
}
validate40.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate65(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate65.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.mode !== void 0) {
      let data0 = data.mode;
      const _errs3 = errors;
      let valid2 = false;
      const _errs4 = errors;
      if (typeof data0 !== "string") {
        const err0 = { instancePath: instancePath + "/mode", schemaPath: "#/$defs/DrillMode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err0];
        } else {
          vErrors.push(err0);
        }
        errors++;
      }
      if ("auto" !== data0) {
        const err1 = { instancePath: instancePath + "/mode", schemaPath: "#/$defs/DrillMode/anyOf/0/const", keyword: "const", params: { allowedValue: "auto" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      var _valid0 = _errs4 === errors;
      valid2 = valid2 || _valid0;
      const _errs6 = errors;
      if (typeof data0 !== "string") {
        const err2 = { instancePath: instancePath + "/mode", schemaPath: "#/$defs/DrillMode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      if ("cut" !== data0) {
        const err3 = { instancePath: instancePath + "/mode", schemaPath: "#/$defs/DrillMode/anyOf/1/const", keyword: "const", params: { allowedValue: "cut" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      var _valid0 = _errs6 === errors;
      valid2 = valid2 || _valid0;
      const _errs8 = errors;
      if (typeof data0 !== "string") {
        const err4 = { instancePath: instancePath + "/mode", schemaPath: "#/$defs/DrillMode/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      if ("overlay" !== data0) {
        const err5 = { instancePath: instancePath + "/mode", schemaPath: "#/$defs/DrillMode/anyOf/2/const", keyword: "const", params: { allowedValue: "overlay" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid0 = _errs8 === errors;
      valid2 = valid2 || _valid0;
      const _errs10 = errors;
      if (typeof data0 !== "string") {
        const err6 = { instancePath: instancePath + "/mode", schemaPath: "#/$defs/DrillMode/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      if ("none" !== data0) {
        const err7 = { instancePath: instancePath + "/mode", schemaPath: "#/$defs/DrillMode/anyOf/3/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      valid2 = valid2 || _valid0;
      if (!valid2) {
        const err8 = { instancePath: instancePath + "/mode", schemaPath: "#/$defs/DrillMode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      } else {
        errors = _errs3;
        if (vErrors !== null) {
          if (_errs3) {
            vErrors.length = _errs3;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.minimum_diameter_mm !== void 0) {
      let data1 = data.minimum_diameter_mm;
      if (typeof data1 == "number") {
        if (data1 < 0 || isNaN(data1)) {
          const err9 = { instancePath: instancePath + "/minimum_diameter_mm", schemaPath: "#/properties/minimum_diameter_mm/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err9];
          } else {
            vErrors.push(err9);
          }
          errors++;
        }
      } else {
        const err10 = { instancePath: instancePath + "/minimum_diameter_mm", schemaPath: "#/properties/minimum_diameter_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
    }
    if (data.shape !== void 0) {
      let data2 = data.shape;
      const _errs16 = errors;
      let valid4 = false;
      const _errs17 = errors;
      if (typeof data2 !== "string") {
        const err11 = { instancePath: instancePath + "/shape", schemaPath: "#/$defs/DrillShape/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      if ("solid" !== data2) {
        const err12 = { instancePath: instancePath + "/shape", schemaPath: "#/$defs/DrillShape/anyOf/0/const", keyword: "const", params: { allowedValue: "solid" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid1 = _errs17 === errors;
      valid4 = valid4 || _valid1;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err13 = { instancePath: instancePath + "/shape", schemaPath: "#/$defs/DrillShape/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      if ("ring" !== data2) {
        const err14 = { instancePath: instancePath + "/shape", schemaPath: "#/$defs/DrillShape/anyOf/1/const", keyword: "const", params: { allowedValue: "ring" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid1 = _errs19 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err15 = { instancePath: instancePath + "/shape", schemaPath: "#/$defs/DrillShape/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
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
    if (data.color !== void 0) {
      let data3 = data.color;
      if (typeof data3 === "string") {
        if (func1(data3) < 1) {
          const err16 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err16];
          } else {
            vErrors.push(err16);
          }
          errors++;
        }
      } else {
        const err17 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
    }
    if (data.plated_color !== void 0) {
      let data4 = data.plated_color;
      if (typeof data4 === "string") {
        if (func1(data4) < 1) {
          const err18 = { instancePath: instancePath + "/plated_color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err18];
          } else {
            vErrors.push(err18);
          }
          errors++;
        }
      } else {
        const err19 = { instancePath: instancePath + "/plated_color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
    }
    if (data.non_plated_color !== void 0) {
      let data5 = data.non_plated_color;
      if (typeof data5 === "string") {
        if (func1(data5) < 1) {
          const err20 = { instancePath: instancePath + "/non_plated_color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err20];
          } else {
            vErrors.push(err20);
          }
          errors++;
        }
      } else {
        const err21 = { instancePath: instancePath + "/non_plated_color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
    }
    if (data.ring_width_mm !== void 0) {
      let data6 = data.ring_width_mm;
      if (typeof data6 == "number") {
        if (data6 < 0 || isNaN(data6)) {
          const err22 = { instancePath: instancePath + "/ring_width_mm", schemaPath: "#/properties/ring_width_mm/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err22];
          } else {
            vErrors.push(err22);
          }
          errors++;
        }
      } else {
        const err23 = { instancePath: instancePath + "/ring_width_mm", schemaPath: "#/properties/ring_width_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
    }
    if (data.plated_ring_shape !== void 0) {
      let data7 = data.plated_ring_shape;
      const _errs34 = errors;
      let valid9 = false;
      const _errs35 = errors;
      if (typeof data7 !== "string") {
        const err24 = { instancePath: instancePath + "/plated_ring_shape", schemaPath: "#/$defs/PlatedRingShape/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      if ("annulus" !== data7) {
        const err25 = { instancePath: instancePath + "/plated_ring_shape", schemaPath: "#/$defs/PlatedRingShape/anyOf/0/const", keyword: "const", params: { allowedValue: "annulus" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
      var _valid2 = _errs35 === errors;
      valid9 = valid9 || _valid2;
      if (!valid9) {
        const err26 = { instancePath: instancePath + "/plated_ring_shape", schemaPath: "#/$defs/PlatedRingShape/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
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
    if (data.selected_component_mode !== void 0) {
      let data8 = data.selected_component_mode;
      const _errs39 = errors;
      let valid11 = false;
      const _errs40 = errors;
      if (typeof data8 !== "string") {
        const err27 = { instancePath: instancePath + "/selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
      if ("inherit" !== data8) {
        const err28 = { instancePath: instancePath + "/selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/const", keyword: "const", params: { allowedValue: "inherit" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
      var _valid3 = _errs40 === errors;
      valid11 = valid11 || _valid3;
      const _errs42 = errors;
      if (typeof data8 !== "string") {
        const err29 = { instancePath: instancePath + "/selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      }
      if ("cut" !== data8) {
        const err30 = { instancePath: instancePath + "/selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/const", keyword: "const", params: { allowedValue: "cut" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
        }
        errors++;
      }
      var _valid3 = _errs42 === errors;
      valid11 = valid11 || _valid3;
      const _errs44 = errors;
      if (typeof data8 !== "string") {
        const err31 = { instancePath: instancePath + "/selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      }
      if ("overlay" !== data8) {
        const err32 = { instancePath: instancePath + "/selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/const", keyword: "const", params: { allowedValue: "overlay" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
        }
        errors++;
      }
      var _valid3 = _errs44 === errors;
      valid11 = valid11 || _valid3;
      const _errs46 = errors;
      if (typeof data8 !== "string") {
        const err33 = { instancePath: instancePath + "/selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
      if ("none" !== data8) {
        const err34 = { instancePath: instancePath + "/selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
        }
        errors++;
      }
      var _valid3 = _errs46 === errors;
      valid11 = valid11 || _valid3;
      if (!valid11) {
        const err35 = { instancePath: instancePath + "/selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err35];
        } else {
          vErrors.push(err35);
        }
        errors++;
      } else {
        errors = _errs39;
        if (vErrors !== null) {
          if (_errs39) {
            vErrors.length = _errs39;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.other_component_mode !== void 0) {
      let data9 = data.other_component_mode;
      const _errs50 = errors;
      let valid13 = false;
      const _errs51 = errors;
      if (typeof data9 !== "string") {
        const err36 = { instancePath: instancePath + "/other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err36];
        } else {
          vErrors.push(err36);
        }
        errors++;
      }
      if ("inherit" !== data9) {
        const err37 = { instancePath: instancePath + "/other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/const", keyword: "const", params: { allowedValue: "inherit" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err37];
        } else {
          vErrors.push(err37);
        }
        errors++;
      }
      var _valid4 = _errs51 === errors;
      valid13 = valid13 || _valid4;
      const _errs53 = errors;
      if (typeof data9 !== "string") {
        const err38 = { instancePath: instancePath + "/other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err38];
        } else {
          vErrors.push(err38);
        }
        errors++;
      }
      if ("cut" !== data9) {
        const err39 = { instancePath: instancePath + "/other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/const", keyword: "const", params: { allowedValue: "cut" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err39];
        } else {
          vErrors.push(err39);
        }
        errors++;
      }
      var _valid4 = _errs53 === errors;
      valid13 = valid13 || _valid4;
      const _errs55 = errors;
      if (typeof data9 !== "string") {
        const err40 = { instancePath: instancePath + "/other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err40];
        } else {
          vErrors.push(err40);
        }
        errors++;
      }
      if ("overlay" !== data9) {
        const err41 = { instancePath: instancePath + "/other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/const", keyword: "const", params: { allowedValue: "overlay" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err41];
        } else {
          vErrors.push(err41);
        }
        errors++;
      }
      var _valid4 = _errs55 === errors;
      valid13 = valid13 || _valid4;
      const _errs57 = errors;
      if (typeof data9 !== "string") {
        const err42 = { instancePath: instancePath + "/other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err42];
        } else {
          vErrors.push(err42);
        }
        errors++;
      }
      if ("none" !== data9) {
        const err43 = { instancePath: instancePath + "/other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err43];
        } else {
          vErrors.push(err43);
        }
        errors++;
      }
      var _valid4 = _errs57 === errors;
      valid13 = valid13 || _valid4;
      if (!valid13) {
        const err44 = { instancePath: instancePath + "/other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err44];
        } else {
          vErrors.push(err44);
        }
        errors++;
      } else {
        errors = _errs50;
        if (vErrors !== null) {
          if (_errs50) {
            vErrors.length = _errs50;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.free_pad_mode !== void 0) {
      let data10 = data.free_pad_mode;
      const _errs61 = errors;
      let valid15 = false;
      const _errs62 = errors;
      if (typeof data10 !== "string") {
        const err45 = { instancePath: instancePath + "/free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err45];
        } else {
          vErrors.push(err45);
        }
        errors++;
      }
      if ("inherit" !== data10) {
        const err46 = { instancePath: instancePath + "/free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/const", keyword: "const", params: { allowedValue: "inherit" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err46];
        } else {
          vErrors.push(err46);
        }
        errors++;
      }
      var _valid5 = _errs62 === errors;
      valid15 = valid15 || _valid5;
      const _errs64 = errors;
      if (typeof data10 !== "string") {
        const err47 = { instancePath: instancePath + "/free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err47];
        } else {
          vErrors.push(err47);
        }
        errors++;
      }
      if ("cut" !== data10) {
        const err48 = { instancePath: instancePath + "/free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/const", keyword: "const", params: { allowedValue: "cut" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err48];
        } else {
          vErrors.push(err48);
        }
        errors++;
      }
      var _valid5 = _errs64 === errors;
      valid15 = valid15 || _valid5;
      const _errs66 = errors;
      if (typeof data10 !== "string") {
        const err49 = { instancePath: instancePath + "/free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err49];
        } else {
          vErrors.push(err49);
        }
        errors++;
      }
      if ("overlay" !== data10) {
        const err50 = { instancePath: instancePath + "/free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/const", keyword: "const", params: { allowedValue: "overlay" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err50];
        } else {
          vErrors.push(err50);
        }
        errors++;
      }
      var _valid5 = _errs66 === errors;
      valid15 = valid15 || _valid5;
      const _errs68 = errors;
      if (typeof data10 !== "string") {
        const err51 = { instancePath: instancePath + "/free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err51];
        } else {
          vErrors.push(err51);
        }
        errors++;
      }
      if ("none" !== data10) {
        const err52 = { instancePath: instancePath + "/free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err52];
        } else {
          vErrors.push(err52);
        }
        errors++;
      }
      var _valid5 = _errs68 === errors;
      valid15 = valid15 || _valid5;
      if (!valid15) {
        const err53 = { instancePath: instancePath + "/free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err53];
        } else {
          vErrors.push(err53);
        }
        errors++;
      } else {
        errors = _errs61;
        if (vErrors !== null) {
          if (_errs61) {
            vErrors.length = _errs61;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.via_mode !== void 0) {
      let data11 = data.via_mode;
      const _errs72 = errors;
      let valid17 = false;
      const _errs73 = errors;
      if (typeof data11 !== "string") {
        const err54 = { instancePath: instancePath + "/via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err54];
        } else {
          vErrors.push(err54);
        }
        errors++;
      }
      if ("inherit" !== data11) {
        const err55 = { instancePath: instancePath + "/via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/const", keyword: "const", params: { allowedValue: "inherit" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err55];
        } else {
          vErrors.push(err55);
        }
        errors++;
      }
      var _valid6 = _errs73 === errors;
      valid17 = valid17 || _valid6;
      const _errs75 = errors;
      if (typeof data11 !== "string") {
        const err56 = { instancePath: instancePath + "/via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err56];
        } else {
          vErrors.push(err56);
        }
        errors++;
      }
      if ("cut" !== data11) {
        const err57 = { instancePath: instancePath + "/via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/const", keyword: "const", params: { allowedValue: "cut" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err57];
        } else {
          vErrors.push(err57);
        }
        errors++;
      }
      var _valid6 = _errs75 === errors;
      valid17 = valid17 || _valid6;
      const _errs77 = errors;
      if (typeof data11 !== "string") {
        const err58 = { instancePath: instancePath + "/via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err58];
        } else {
          vErrors.push(err58);
        }
        errors++;
      }
      if ("overlay" !== data11) {
        const err59 = { instancePath: instancePath + "/via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/const", keyword: "const", params: { allowedValue: "overlay" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err59];
        } else {
          vErrors.push(err59);
        }
        errors++;
      }
      var _valid6 = _errs77 === errors;
      valid17 = valid17 || _valid6;
      const _errs79 = errors;
      if (typeof data11 !== "string") {
        const err60 = { instancePath: instancePath + "/via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err60];
        } else {
          vErrors.push(err60);
        }
        errors++;
      }
      if ("none" !== data11) {
        const err61 = { instancePath: instancePath + "/via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err61];
        } else {
          vErrors.push(err61);
        }
        errors++;
      }
      var _valid6 = _errs79 === errors;
      valid17 = valid17 || _valid6;
      if (!valid17) {
        const err62 = { instancePath: instancePath + "/via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err62];
        } else {
          vErrors.push(err62);
        }
        errors++;
      } else {
        errors = _errs72;
        if (vErrors !== null) {
          if (_errs72) {
            vErrors.length = _errs72;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.overlay_thickness_mm !== void 0) {
      let data12 = data.overlay_thickness_mm;
      if (typeof data12 == "number") {
        if (data12 < 0 || isNaN(data12)) {
          const err63 = { instancePath: instancePath + "/overlay_thickness_mm", schemaPath: "#/properties/overlay_thickness_mm/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err63];
          } else {
            vErrors.push(err63);
          }
          errors++;
        }
      } else {
        const err64 = { instancePath: instancePath + "/overlay_thickness_mm", schemaPath: "#/properties/overlay_thickness_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err64];
        } else {
          vErrors.push(err64);
        }
        errors++;
      }
    }
    for (const key0 in data) {
      if (key0 !== "mode" && key0 !== "minimum_diameter_mm" && key0 !== "shape" && key0 !== "color" && key0 !== "plated_color" && key0 !== "non_plated_color" && key0 !== "ring_width_mm" && key0 !== "plated_ring_shape" && key0 !== "selected_component_mode" && key0 !== "other_component_mode" && key0 !== "free_pad_mode" && key0 !== "via_mode" && key0 !== "overlay_thickness_mm") {
        const err65 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err65];
        } else {
          vErrors.push(err65);
        }
        errors++;
      }
    }
  } else {
    const err66 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err66];
    } else {
      vErrors.push(err66);
    }
    errors++;
  }
  validate65.errors = vErrors;
  return errors === 0;
}
validate65.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate67(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate67.evaluated;
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
    if (data.enabled !== void 0) {
      let data0 = data.enabled;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "boolean") {
        const err1 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid3 = valid3 || _valid0;
      const _errs9 = errors;
      if (data0 !== null) {
        const err2 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err3 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
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
    if (data.name !== void 0) {
      let data1 = data.name;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err4 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid1 = _errs13 === errors;
      valid4 = valid4 || _valid1;
      const _errs15 = errors;
      if (data1 !== null) {
        const err5 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err6 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
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
    if (data.layer !== void 0) {
      let data2 = data.layer;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err7 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err8 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err9 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
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
    if (data.side !== void 0) {
      let data3 = data.side;
      const _errs24 = errors;
      let valid6 = false;
      const _errs25 = errors;
      if (typeof data3 !== "string") {
        const err10 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid3 = _errs25 === errors;
      valid6 = valid6 || _valid3;
      const _errs27 = errors;
      if (data3 !== null) {
        const err11 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid3 = _errs27 === errors;
      valid6 = valid6 || _valid3;
      if (!valid6) {
        const err12 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      } else {
        errors = _errs24;
        if (vErrors !== null) {
          if (_errs24) {
            vErrors.length = _errs24;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.location_mils !== void 0) {
      let data4 = data.location_mils;
      const _errs30 = errors;
      let valid7 = false;
      const _errs31 = errors;
      if (Array.isArray(data4)) {
        if (data4.length > 2) {
          const err13 = { instancePath: instancePath + "/location_mils", schemaPath: "#/$defs/Pair/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err13];
          } else {
            vErrors.push(err13);
          }
          errors++;
        }
        if (data4.length < 2) {
          const err14 = { instancePath: instancePath + "/location_mils", schemaPath: "#/$defs/Pair/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err14];
          } else {
            vErrors.push(err14);
          }
          errors++;
        }
        const len0 = data4.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!(typeof data4[i0] == "number")) {
            const err15 = { instancePath: instancePath + "/location_mils/" + i0, schemaPath: "#/$defs/Pair/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err15];
            } else {
              vErrors.push(err15);
            }
            errors++;
          }
        }
      } else {
        const err16 = { instancePath: instancePath + "/location_mils", schemaPath: "#/$defs/Pair/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid4 = _errs31 === errors;
      valid7 = valid7 || _valid4;
      const _errs36 = errors;
      if (data4 !== null) {
        const err17 = { instancePath: instancePath + "/location_mils", schemaPath: "#/properties/location_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      var _valid4 = _errs36 === errors;
      valid7 = valid7 || _valid4;
      if (!valid7) {
        const err18 = { instancePath: instancePath + "/location_mils", schemaPath: "#/properties/location_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      } else {
        errors = _errs30;
        if (vErrors !== null) {
          if (_errs30) {
            vErrors.length = _errs30;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.z_mm !== void 0) {
      let data6 = data.z_mm;
      const _errs39 = errors;
      let valid11 = false;
      const _errs40 = errors;
      if (!(typeof data6 == "number")) {
        const err19 = { instancePath: instancePath + "/z_mm", schemaPath: "#/properties/z_mm/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
      var _valid5 = _errs40 === errors;
      valid11 = valid11 || _valid5;
      const _errs42 = errors;
      if (data6 !== null) {
        const err20 = { instancePath: instancePath + "/z_mm", schemaPath: "#/properties/z_mm/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      var _valid5 = _errs42 === errors;
      valid11 = valid11 || _valid5;
      if (!valid11) {
        const err21 = { instancePath: instancePath + "/z_mm", schemaPath: "#/properties/z_mm/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      } else {
        errors = _errs39;
        if (vErrors !== null) {
          if (_errs39) {
            vErrors.length = _errs39;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.rotation_z_degrees !== void 0) {
      let data7 = data.rotation_z_degrees;
      const _errs45 = errors;
      let valid12 = false;
      const _errs46 = errors;
      if (!(typeof data7 == "number")) {
        const err22 = { instancePath: instancePath + "/rotation_z_degrees", schemaPath: "#/properties/rotation_z_degrees/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
      var _valid6 = _errs46 === errors;
      valid12 = valid12 || _valid6;
      const _errs48 = errors;
      if (data7 !== null) {
        const err23 = { instancePath: instancePath + "/rotation_z_degrees", schemaPath: "#/properties/rotation_z_degrees/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      var _valid6 = _errs48 === errors;
      valid12 = valid12 || _valid6;
      if (!valid12) {
        const err24 = { instancePath: instancePath + "/rotation_z_degrees", schemaPath: "#/properties/rotation_z_degrees/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      } else {
        errors = _errs45;
        if (vErrors !== null) {
          if (_errs45) {
            vErrors.length = _errs45;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.opacity !== void 0) {
      let data8 = data.opacity;
      const _errs51 = errors;
      let valid13 = false;
      const _errs52 = errors;
      if (!(typeof data8 == "number")) {
        const err25 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
      var _valid7 = _errs52 === errors;
      valid13 = valid13 || _valid7;
      const _errs54 = errors;
      if (data8 !== null) {
        const err26 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
      var _valid7 = _errs54 === errors;
      valid13 = valid13 || _valid7;
      if (!valid13) {
        const err27 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      } else {
        errors = _errs51;
        if (vErrors !== null) {
          if (_errs51) {
            vErrors.length = _errs51;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.bounds_mils !== void 0) {
      let data9 = data.bounds_mils;
      const _errs57 = errors;
      let valid14 = false;
      const _errs58 = errors;
      if (data9 && typeof data9 == "object" && !Array.isArray(data9)) {
        if (data9.left === void 0) {
          const err28 = { instancePath: instancePath + "/bounds_mils", schemaPath: "#/$defs/Bounds/required", keyword: "required", params: { missingProperty: "left" }, message: "must have required property 'left'" };
          if (vErrors === null) {
            vErrors = [err28];
          } else {
            vErrors.push(err28);
          }
          errors++;
        }
        if (data9.bottom === void 0) {
          const err29 = { instancePath: instancePath + "/bounds_mils", schemaPath: "#/$defs/Bounds/required", keyword: "required", params: { missingProperty: "bottom" }, message: "must have required property 'bottom'" };
          if (vErrors === null) {
            vErrors = [err29];
          } else {
            vErrors.push(err29);
          }
          errors++;
        }
        if (data9.right === void 0) {
          const err30 = { instancePath: instancePath + "/bounds_mils", schemaPath: "#/$defs/Bounds/required", keyword: "required", params: { missingProperty: "right" }, message: "must have required property 'right'" };
          if (vErrors === null) {
            vErrors = [err30];
          } else {
            vErrors.push(err30);
          }
          errors++;
        }
        if (data9.top === void 0) {
          const err31 = { instancePath: instancePath + "/bounds_mils", schemaPath: "#/$defs/Bounds/required", keyword: "required", params: { missingProperty: "top" }, message: "must have required property 'top'" };
          if (vErrors === null) {
            vErrors = [err31];
          } else {
            vErrors.push(err31);
          }
          errors++;
        }
        if (data9.left !== void 0) {
          if (!(typeof data9.left == "number")) {
            const err32 = { instancePath: instancePath + "/bounds_mils/left", schemaPath: "#/$defs/Bounds/properties/left/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err32];
            } else {
              vErrors.push(err32);
            }
            errors++;
          }
        }
        if (data9.bottom !== void 0) {
          if (!(typeof data9.bottom == "number")) {
            const err33 = { instancePath: instancePath + "/bounds_mils/bottom", schemaPath: "#/$defs/Bounds/properties/bottom/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err33];
            } else {
              vErrors.push(err33);
            }
            errors++;
          }
        }
        if (data9.right !== void 0) {
          if (!(typeof data9.right == "number")) {
            const err34 = { instancePath: instancePath + "/bounds_mils/right", schemaPath: "#/$defs/Bounds/properties/right/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err34];
            } else {
              vErrors.push(err34);
            }
            errors++;
          }
        }
        if (data9.top !== void 0) {
          if (!(typeof data9.top == "number")) {
            const err35 = { instancePath: instancePath + "/bounds_mils/top", schemaPath: "#/$defs/Bounds/properties/top/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err35];
            } else {
              vErrors.push(err35);
            }
            errors++;
          }
        }
        for (const key1 in data9) {
          if (key1 !== "left" && key1 !== "bottom" && key1 !== "right" && key1 !== "top") {
            const err36 = { instancePath: instancePath + "/bounds_mils/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/Bounds/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err36];
            } else {
              vErrors.push(err36);
            }
            errors++;
          }
        }
      } else {
        const err37 = { instancePath: instancePath + "/bounds_mils", schemaPath: "#/$defs/Bounds/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err37];
        } else {
          vErrors.push(err37);
        }
        errors++;
      }
      var _valid8 = _errs58 === errors;
      valid14 = valid14 || _valid8;
      const _errs72 = errors;
      if (Array.isArray(data9)) {
        if (data9.length > 4) {
          const err38 = { instancePath: instancePath + "/bounds_mils", schemaPath: "#/$defs/BoundsArray/maxItems", keyword: "maxItems", params: { limit: 4 }, message: "must NOT have more than 4 items" };
          if (vErrors === null) {
            vErrors = [err38];
          } else {
            vErrors.push(err38);
          }
          errors++;
        }
        if (data9.length < 4) {
          const err39 = { instancePath: instancePath + "/bounds_mils", schemaPath: "#/$defs/BoundsArray/minItems", keyword: "minItems", params: { limit: 4 }, message: "must NOT have fewer than 4 items" };
          if (vErrors === null) {
            vErrors = [err39];
          } else {
            vErrors.push(err39);
          }
          errors++;
        }
        const len1 = data9.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (!(typeof data9[i1] == "number")) {
            const err40 = { instancePath: instancePath + "/bounds_mils/" + i1, schemaPath: "#/$defs/BoundsArray/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err40];
            } else {
              vErrors.push(err40);
            }
            errors++;
          }
        }
      } else {
        const err41 = { instancePath: instancePath + "/bounds_mils", schemaPath: "#/$defs/BoundsArray/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err41];
        } else {
          vErrors.push(err41);
        }
        errors++;
      }
      var _valid8 = _errs72 === errors;
      valid14 = valid14 || _valid8;
      const _errs77 = errors;
      if (data9 !== null) {
        const err42 = { instancePath: instancePath + "/bounds_mils", schemaPath: "#/properties/bounds_mils/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err42];
        } else {
          vErrors.push(err42);
        }
        errors++;
      }
      var _valid8 = _errs77 === errors;
      valid14 = valid14 || _valid8;
      if (!valid14) {
        const err43 = { instancePath: instancePath + "/bounds_mils", schemaPath: "#/properties/bounds_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err43];
        } else {
          vErrors.push(err43);
        }
        errors++;
      } else {
        errors = _errs57;
        if (vErrors !== null) {
          if (_errs57) {
            vErrors.length = _errs57;
          } else {
            vErrors = null;
          }
        }
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
  validate67.errors = vErrors;
  return errors === 0;
}
validate67.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate69(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate69.evaluated;
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
    if (data.projection === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "projection" }, message: "must have required property 'projection'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.projection !== void 0) {
      if (typeof data.projection !== "string") {
        const err2 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
    if (data.name !== void 0) {
      let data1 = data.name;
      const _errs8 = errors;
      let valid3 = false;
      const _errs9 = errors;
      if (typeof data1 !== "string") {
        const err3 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (data1 !== null) {
        const err4 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid0 = _errs11 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err5 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
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
    if (data.color !== void 0) {
      let data2 = data.color;
      const _errs14 = errors;
      let valid4 = false;
      const _errs15 = errors;
      if (typeof data2 !== "string") {
        const err6 = { instancePath: instancePath + "/color", schemaPath: "#/properties/color/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      valid4 = valid4 || _valid1;
      const _errs17 = errors;
      if (data2 !== null) {
        const err7 = { instancePath: instancePath + "/color", schemaPath: "#/properties/color/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid1 = _errs17 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err8 = { instancePath: instancePath + "/color", schemaPath: "#/properties/color/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      } else {
        errors = _errs14;
        if (vErrors !== null) {
          if (_errs14) {
            vErrors.length = _errs14;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.z_offset_mm !== void 0) {
      let data3 = data.z_offset_mm;
      const _errs20 = errors;
      let valid5 = false;
      const _errs21 = errors;
      if (!(typeof data3 == "number")) {
        const err9 = { instancePath: instancePath + "/z_offset_mm", schemaPath: "#/properties/z_offset_mm/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      const _errs23 = errors;
      if (data3 !== null) {
        const err10 = { instancePath: instancePath + "/z_offset_mm", schemaPath: "#/properties/z_offset_mm/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs23 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/z_offset_mm", schemaPath: "#/properties/z_offset_mm/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      } else {
        errors = _errs20;
        if (vErrors !== null) {
          if (_errs20) {
            vErrors.length = _errs20;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.thickness_mm !== void 0) {
      let data4 = data.thickness_mm;
      const _errs26 = errors;
      let valid6 = false;
      const _errs27 = errors;
      if (!(typeof data4 == "number")) {
        const err12 = { instancePath: instancePath + "/thickness_mm", schemaPath: "#/properties/thickness_mm/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid3 = _errs27 === errors;
      valid6 = valid6 || _valid3;
      const _errs29 = errors;
      if (data4 !== null) {
        const err13 = { instancePath: instancePath + "/thickness_mm", schemaPath: "#/properties/thickness_mm/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid3 = _errs29 === errors;
      valid6 = valid6 || _valid3;
      if (!valid6) {
        const err14 = { instancePath: instancePath + "/thickness_mm", schemaPath: "#/properties/thickness_mm/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      } else {
        errors = _errs26;
        if (vErrors !== null) {
          if (_errs26) {
            vErrors.length = _errs26;
          } else {
            vErrors = null;
          }
        }
      }
    }
  } else {
    const err15 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err15];
    } else {
      vErrors.push(err15);
    }
    errors++;
  }
  validate69.errors = vErrors;
  return errors === 0;
}
validate69.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate37(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate37.evaluated;
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
    if (data.thickness_mm !== void 0) {
      let data0 = data.thickness_mm;
      if (typeof data0 == "number") {
        if (data0 <= 0 || isNaN(data0)) {
          const err1 = { instancePath: instancePath + "/thickness_mm", schemaPath: "#/properties/thickness_mm/exclusiveMinimum", keyword: "exclusiveMinimum", params: { comparison: ">", limit: 0 }, message: "must be > 0" };
          if (vErrors === null) {
            vErrors = [err1];
          } else {
            vErrors.push(err1);
          }
          errors++;
        }
      } else {
        const err2 = { instancePath: instancePath + "/thickness_mm", schemaPath: "#/properties/thickness_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
    if (data.z_mm !== void 0) {
      if (!(typeof data.z_mm == "number")) {
        const err3 = { instancePath: instancePath + "/z_mm", schemaPath: "#/properties/z_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.copper_color !== void 0) {
      let data2 = data.copper_color;
      if (typeof data2 === "string") {
        if (func1(data2) < 1) {
          const err4 = { instancePath: instancePath + "/copper_color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err4];
          } else {
            vErrors.push(err4);
          }
          errors++;
        }
      } else {
        const err5 = { instancePath: instancePath + "/copper_color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.outline_width_mm !== void 0) {
      let data3 = data.outline_width_mm;
      if (typeof data3 == "number") {
        if (data3 < 0 || isNaN(data3)) {
          const err6 = { instancePath: instancePath + "/outline_width_mm", schemaPath: "#/properties/outline_width_mm/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err6];
          } else {
            vErrors.push(err6);
          }
          errors++;
        }
      } else {
        const err7 = { instancePath: instancePath + "/outline_width_mm", schemaPath: "#/properties/outline_width_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.outline_color !== void 0) {
      let data4 = data.outline_color;
      if (typeof data4 === "string") {
        if (func1(data4) < 1) {
          const err8 = { instancePath: instancePath + "/outline_color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err8];
          } else {
            vErrors.push(err8);
          }
          errors++;
        }
      } else {
        const err9 = { instancePath: instancePath + "/outline_color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    if (data.board_cutout_color !== void 0) {
      let data5 = data.board_cutout_color;
      if (typeof data5 === "string") {
        if (func1(data5) < 1) {
          const err10 = { instancePath: instancePath + "/board_cutout_color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err10];
          } else {
            vErrors.push(err10);
          }
          errors++;
        }
      } else {
        const err11 = { instancePath: instancePath + "/board_cutout_color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
    }
    if (data.include_board_cutouts !== void 0) {
      if (typeof data.include_board_cutouts !== "boolean") {
        const err12 = { instancePath: instancePath + "/include_board_cutouts", schemaPath: "#/properties/include_board_cutouts/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
    }
    if (data.include_copper !== void 0) {
      if (typeof data.include_copper !== "boolean") {
        const err13 = { instancePath: instancePath + "/include_copper", schemaPath: "#/properties/include_copper/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.include_board_outline !== void 0) {
      if (typeof data.include_board_outline !== "boolean") {
        const err14 = { instancePath: instancePath + "/include_board_outline", schemaPath: "#/properties/include_board_outline/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
    }
    if (data.include_poured_polygons !== void 0) {
      if (typeof data.include_poured_polygons !== "boolean") {
        const err15 = { instancePath: instancePath + "/include_poured_polygons", schemaPath: "#/properties/include_poured_polygons/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
    }
    if (data.cut_holes !== void 0) {
      if (typeof data.cut_holes !== "boolean") {
        const err16 = { instancePath: instancePath + "/cut_holes", schemaPath: "#/properties/cut_holes/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
    }
    if (data.drill_hole_mode !== void 0) {
      let data11 = data.drill_hole_mode;
      const _errs32 = errors;
      let valid7 = false;
      const _errs33 = errors;
      if (typeof data11 !== "string") {
        const err17 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      if ("auto" !== data11) {
        const err18 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf/0/const", keyword: "const", params: { allowedValue: "auto" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
      var _valid0 = _errs33 === errors;
      valid7 = valid7 || _valid0;
      const _errs35 = errors;
      if (typeof data11 !== "string") {
        const err19 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
      if ("cut" !== data11) {
        const err20 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf/1/const", keyword: "const", params: { allowedValue: "cut" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      var _valid0 = _errs35 === errors;
      valid7 = valid7 || _valid0;
      const _errs37 = errors;
      if (typeof data11 !== "string") {
        const err21 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      if ("overlay" !== data11) {
        const err22 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf/2/const", keyword: "const", params: { allowedValue: "overlay" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
      var _valid0 = _errs37 === errors;
      valid7 = valid7 || _valid0;
      const _errs39 = errors;
      if (typeof data11 !== "string") {
        const err23 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      if ("none" !== data11) {
        const err24 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf/3/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      var _valid0 = _errs39 === errors;
      valid7 = valid7 || _valid0;
      if (!valid7) {
        const err25 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      } else {
        errors = _errs32;
        if (vErrors !== null) {
          if (_errs32) {
            vErrors.length = _errs32;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.max_boolean_drill_cuts !== void 0) {
      let data12 = data.max_boolean_drill_cuts;
      if (!(typeof data12 == "number" && (!(data12 % 1) && !isNaN(data12)))) {
        const err26 = { instancePath: instancePath + "/max_boolean_drill_cuts", schemaPath: "#/properties/max_boolean_drill_cuts/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
      if (typeof data12 == "number") {
        if (data12 < 0 || isNaN(data12)) {
          const err27 = { instancePath: instancePath + "/max_boolean_drill_cuts", schemaPath: "#/properties/max_boolean_drill_cuts/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err27];
          } else {
            vErrors.push(err27);
          }
          errors++;
        }
      }
    }
    if (data.drill_hole_color !== void 0) {
      let data13 = data.drill_hole_color;
      if (typeof data13 === "string") {
        if (func1(data13) < 1) {
          const err28 = { instancePath: instancePath + "/drill_hole_color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err28];
          } else {
            vErrors.push(err28);
          }
          errors++;
        }
      } else {
        const err29 = { instancePath: instancePath + "/drill_hole_color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      }
    }
    if (data.drill_plated_hole_color !== void 0) {
      let data14 = data.drill_plated_hole_color;
      if (typeof data14 === "string") {
        if (func1(data14) < 1) {
          const err30 = { instancePath: instancePath + "/drill_plated_hole_color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err30];
          } else {
            vErrors.push(err30);
          }
          errors++;
        }
      } else {
        const err31 = { instancePath: instancePath + "/drill_plated_hole_color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      }
    }
    if (data.drill_non_plated_hole_color !== void 0) {
      let data15 = data.drill_non_plated_hole_color;
      if (typeof data15 === "string") {
        if (func1(data15) < 1) {
          const err32 = { instancePath: instancePath + "/drill_non_plated_hole_color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err32];
          } else {
            vErrors.push(err32);
          }
          errors++;
        }
      } else {
        const err33 = { instancePath: instancePath + "/drill_non_plated_hole_color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
    }
    if (data.drill_overlay_thickness_mm !== void 0) {
      let data16 = data.drill_overlay_thickness_mm;
      if (typeof data16 == "number") {
        if (data16 < 0 || isNaN(data16)) {
          const err34 = { instancePath: instancePath + "/drill_overlay_thickness_mm", schemaPath: "#/properties/drill_overlay_thickness_mm/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err34];
          } else {
            vErrors.push(err34);
          }
          errors++;
        }
      } else {
        const err35 = { instancePath: instancePath + "/drill_overlay_thickness_mm", schemaPath: "#/properties/drill_overlay_thickness_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err35];
        } else {
          vErrors.push(err35);
        }
        errors++;
      }
    }
    if (data.drill_minimum_diameter_mm !== void 0) {
      let data17 = data.drill_minimum_diameter_mm;
      if (typeof data17 == "number") {
        if (data17 < 0 || isNaN(data17)) {
          const err36 = { instancePath: instancePath + "/drill_minimum_diameter_mm", schemaPath: "#/properties/drill_minimum_diameter_mm/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err36];
          } else {
            vErrors.push(err36);
          }
          errors++;
        }
      } else {
        const err37 = { instancePath: instancePath + "/drill_minimum_diameter_mm", schemaPath: "#/properties/drill_minimum_diameter_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err37];
        } else {
          vErrors.push(err37);
        }
        errors++;
      }
    }
    if (data.drill_hole_shape !== void 0) {
      let data18 = data.drill_hole_shape;
      const _errs58 = errors;
      let valid12 = false;
      const _errs59 = errors;
      if (typeof data18 !== "string") {
        const err38 = { instancePath: instancePath + "/drill_hole_shape", schemaPath: "#/$defs/DrillShape/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err38];
        } else {
          vErrors.push(err38);
        }
        errors++;
      }
      if ("solid" !== data18) {
        const err39 = { instancePath: instancePath + "/drill_hole_shape", schemaPath: "#/$defs/DrillShape/anyOf/0/const", keyword: "const", params: { allowedValue: "solid" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err39];
        } else {
          vErrors.push(err39);
        }
        errors++;
      }
      var _valid1 = _errs59 === errors;
      valid12 = valid12 || _valid1;
      const _errs61 = errors;
      if (typeof data18 !== "string") {
        const err40 = { instancePath: instancePath + "/drill_hole_shape", schemaPath: "#/$defs/DrillShape/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err40];
        } else {
          vErrors.push(err40);
        }
        errors++;
      }
      if ("ring" !== data18) {
        const err41 = { instancePath: instancePath + "/drill_hole_shape", schemaPath: "#/$defs/DrillShape/anyOf/1/const", keyword: "const", params: { allowedValue: "ring" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err41];
        } else {
          vErrors.push(err41);
        }
        errors++;
      }
      var _valid1 = _errs61 === errors;
      valid12 = valid12 || _valid1;
      if (!valid12) {
        const err42 = { instancePath: instancePath + "/drill_hole_shape", schemaPath: "#/$defs/DrillShape/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err42];
        } else {
          vErrors.push(err42);
        }
        errors++;
      } else {
        errors = _errs58;
        if (vErrors !== null) {
          if (_errs58) {
            vErrors.length = _errs58;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.drill_ring_width_mm !== void 0) {
      let data19 = data.drill_ring_width_mm;
      if (typeof data19 == "number") {
        if (data19 < 0 || isNaN(data19)) {
          const err43 = { instancePath: instancePath + "/drill_ring_width_mm", schemaPath: "#/properties/drill_ring_width_mm/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err43];
          } else {
            vErrors.push(err43);
          }
          errors++;
        }
      } else {
        const err44 = { instancePath: instancePath + "/drill_ring_width_mm", schemaPath: "#/properties/drill_ring_width_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err44];
        } else {
          vErrors.push(err44);
        }
        errors++;
      }
    }
    if (data.drill_plated_ring_shape !== void 0) {
      let data20 = data.drill_plated_ring_shape;
      const _errs67 = errors;
      let valid14 = false;
      const _errs68 = errors;
      if (typeof data20 !== "string") {
        const err45 = { instancePath: instancePath + "/drill_plated_ring_shape", schemaPath: "#/$defs/PlatedRingShape/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err45];
        } else {
          vErrors.push(err45);
        }
        errors++;
      }
      if ("annulus" !== data20) {
        const err46 = { instancePath: instancePath + "/drill_plated_ring_shape", schemaPath: "#/$defs/PlatedRingShape/anyOf/0/const", keyword: "const", params: { allowedValue: "annulus" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err46];
        } else {
          vErrors.push(err46);
        }
        errors++;
      }
      var _valid2 = _errs68 === errors;
      valid14 = valid14 || _valid2;
      if (!valid14) {
        const err47 = { instancePath: instancePath + "/drill_plated_ring_shape", schemaPath: "#/$defs/PlatedRingShape/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err47];
        } else {
          vErrors.push(err47);
        }
        errors++;
      } else {
        errors = _errs67;
        if (vErrors !== null) {
          if (_errs67) {
            vErrors.length = _errs67;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.drill_selected_component_mode !== void 0) {
      let data21 = data.drill_selected_component_mode;
      const _errs72 = errors;
      let valid16 = false;
      const _errs73 = errors;
      if (typeof data21 !== "string") {
        const err48 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err48];
        } else {
          vErrors.push(err48);
        }
        errors++;
      }
      if ("inherit" !== data21) {
        const err49 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/const", keyword: "const", params: { allowedValue: "inherit" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err49];
        } else {
          vErrors.push(err49);
        }
        errors++;
      }
      var _valid3 = _errs73 === errors;
      valid16 = valid16 || _valid3;
      const _errs75 = errors;
      if (typeof data21 !== "string") {
        const err50 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err50];
        } else {
          vErrors.push(err50);
        }
        errors++;
      }
      if ("cut" !== data21) {
        const err51 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/const", keyword: "const", params: { allowedValue: "cut" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err51];
        } else {
          vErrors.push(err51);
        }
        errors++;
      }
      var _valid3 = _errs75 === errors;
      valid16 = valid16 || _valid3;
      const _errs77 = errors;
      if (typeof data21 !== "string") {
        const err52 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err52];
        } else {
          vErrors.push(err52);
        }
        errors++;
      }
      if ("overlay" !== data21) {
        const err53 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/const", keyword: "const", params: { allowedValue: "overlay" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err53];
        } else {
          vErrors.push(err53);
        }
        errors++;
      }
      var _valid3 = _errs77 === errors;
      valid16 = valid16 || _valid3;
      const _errs79 = errors;
      if (typeof data21 !== "string") {
        const err54 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err54];
        } else {
          vErrors.push(err54);
        }
        errors++;
      }
      if ("none" !== data21) {
        const err55 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err55];
        } else {
          vErrors.push(err55);
        }
        errors++;
      }
      var _valid3 = _errs79 === errors;
      valid16 = valid16 || _valid3;
      if (!valid16) {
        const err56 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err56];
        } else {
          vErrors.push(err56);
        }
        errors++;
      } else {
        errors = _errs72;
        if (vErrors !== null) {
          if (_errs72) {
            vErrors.length = _errs72;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.drill_other_component_mode !== void 0) {
      let data22 = data.drill_other_component_mode;
      const _errs83 = errors;
      let valid18 = false;
      const _errs84 = errors;
      if (typeof data22 !== "string") {
        const err57 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err57];
        } else {
          vErrors.push(err57);
        }
        errors++;
      }
      if ("inherit" !== data22) {
        const err58 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/const", keyword: "const", params: { allowedValue: "inherit" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err58];
        } else {
          vErrors.push(err58);
        }
        errors++;
      }
      var _valid4 = _errs84 === errors;
      valid18 = valid18 || _valid4;
      const _errs86 = errors;
      if (typeof data22 !== "string") {
        const err59 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err59];
        } else {
          vErrors.push(err59);
        }
        errors++;
      }
      if ("cut" !== data22) {
        const err60 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/const", keyword: "const", params: { allowedValue: "cut" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err60];
        } else {
          vErrors.push(err60);
        }
        errors++;
      }
      var _valid4 = _errs86 === errors;
      valid18 = valid18 || _valid4;
      const _errs88 = errors;
      if (typeof data22 !== "string") {
        const err61 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err61];
        } else {
          vErrors.push(err61);
        }
        errors++;
      }
      if ("overlay" !== data22) {
        const err62 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/const", keyword: "const", params: { allowedValue: "overlay" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err62];
        } else {
          vErrors.push(err62);
        }
        errors++;
      }
      var _valid4 = _errs88 === errors;
      valid18 = valid18 || _valid4;
      const _errs90 = errors;
      if (typeof data22 !== "string") {
        const err63 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err63];
        } else {
          vErrors.push(err63);
        }
        errors++;
      }
      if ("none" !== data22) {
        const err64 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err64];
        } else {
          vErrors.push(err64);
        }
        errors++;
      }
      var _valid4 = _errs90 === errors;
      valid18 = valid18 || _valid4;
      if (!valid18) {
        const err65 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err65];
        } else {
          vErrors.push(err65);
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
    if (data.drill_free_pad_mode !== void 0) {
      let data23 = data.drill_free_pad_mode;
      const _errs94 = errors;
      let valid20 = false;
      const _errs95 = errors;
      if (typeof data23 !== "string") {
        const err66 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err66];
        } else {
          vErrors.push(err66);
        }
        errors++;
      }
      if ("inherit" !== data23) {
        const err67 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/const", keyword: "const", params: { allowedValue: "inherit" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err67];
        } else {
          vErrors.push(err67);
        }
        errors++;
      }
      var _valid5 = _errs95 === errors;
      valid20 = valid20 || _valid5;
      const _errs97 = errors;
      if (typeof data23 !== "string") {
        const err68 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err68];
        } else {
          vErrors.push(err68);
        }
        errors++;
      }
      if ("cut" !== data23) {
        const err69 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/const", keyword: "const", params: { allowedValue: "cut" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err69];
        } else {
          vErrors.push(err69);
        }
        errors++;
      }
      var _valid5 = _errs97 === errors;
      valid20 = valid20 || _valid5;
      const _errs99 = errors;
      if (typeof data23 !== "string") {
        const err70 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err70];
        } else {
          vErrors.push(err70);
        }
        errors++;
      }
      if ("overlay" !== data23) {
        const err71 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/const", keyword: "const", params: { allowedValue: "overlay" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err71];
        } else {
          vErrors.push(err71);
        }
        errors++;
      }
      var _valid5 = _errs99 === errors;
      valid20 = valid20 || _valid5;
      const _errs101 = errors;
      if (typeof data23 !== "string") {
        const err72 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err72];
        } else {
          vErrors.push(err72);
        }
        errors++;
      }
      if ("none" !== data23) {
        const err73 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err73];
        } else {
          vErrors.push(err73);
        }
        errors++;
      }
      var _valid5 = _errs101 === errors;
      valid20 = valid20 || _valid5;
      if (!valid20) {
        const err74 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err74];
        } else {
          vErrors.push(err74);
        }
        errors++;
      } else {
        errors = _errs94;
        if (vErrors !== null) {
          if (_errs94) {
            vErrors.length = _errs94;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.drill_via_mode !== void 0) {
      let data24 = data.drill_via_mode;
      const _errs105 = errors;
      let valid22 = false;
      const _errs106 = errors;
      if (typeof data24 !== "string") {
        const err75 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err75];
        } else {
          vErrors.push(err75);
        }
        errors++;
      }
      if ("inherit" !== data24) {
        const err76 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/const", keyword: "const", params: { allowedValue: "inherit" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err76];
        } else {
          vErrors.push(err76);
        }
        errors++;
      }
      var _valid6 = _errs106 === errors;
      valid22 = valid22 || _valid6;
      const _errs108 = errors;
      if (typeof data24 !== "string") {
        const err77 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err77];
        } else {
          vErrors.push(err77);
        }
        errors++;
      }
      if ("cut" !== data24) {
        const err78 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/const", keyword: "const", params: { allowedValue: "cut" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err78];
        } else {
          vErrors.push(err78);
        }
        errors++;
      }
      var _valid6 = _errs108 === errors;
      valid22 = valid22 || _valid6;
      const _errs110 = errors;
      if (typeof data24 !== "string") {
        const err79 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err79];
        } else {
          vErrors.push(err79);
        }
        errors++;
      }
      if ("overlay" !== data24) {
        const err80 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/const", keyword: "const", params: { allowedValue: "overlay" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err80];
        } else {
          vErrors.push(err80);
        }
        errors++;
      }
      var _valid6 = _errs110 === errors;
      valid22 = valid22 || _valid6;
      const _errs112 = errors;
      if (typeof data24 !== "string") {
        const err81 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err81];
        } else {
          vErrors.push(err81);
        }
        errors++;
      }
      if ("none" !== data24) {
        const err82 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err82];
        } else {
          vErrors.push(err82);
        }
        errors++;
      }
      var _valid6 = _errs112 === errors;
      valid22 = valid22 || _valid6;
      if (!valid22) {
        const err83 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err83];
        } else {
          vErrors.push(err83);
        }
        errors++;
      } else {
        errors = _errs105;
        if (vErrors !== null) {
          if (_errs105) {
            vErrors.length = _errs105;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.fuse_copper !== void 0) {
      if (typeof data.fuse_copper !== "boolean") {
        const err84 = { instancePath: instancePath + "/fuse_copper", schemaPath: "#/properties/fuse_copper/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err84];
        } else {
          vErrors.push(err84);
        }
        errors++;
      }
    }
    if (data.fuse_board_outline !== void 0) {
      if (typeof data.fuse_board_outline !== "boolean") {
        const err85 = { instancePath: instancePath + "/fuse_board_outline", schemaPath: "#/properties/fuse_board_outline/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err85];
        } else {
          vErrors.push(err85);
        }
        errors++;
      }
    }
    if (data.arc_segments !== void 0) {
      let data27 = data.arc_segments;
      if (!(typeof data27 == "number" && (!(data27 % 1) && !isNaN(data27)))) {
        const err86 = { instancePath: instancePath + "/arc_segments", schemaPath: "#/properties/arc_segments/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err86];
        } else {
          vErrors.push(err86);
        }
        errors++;
      }
      if (typeof data27 == "number") {
        if (data27 < 1 || isNaN(data27)) {
          const err87 = { instancePath: instancePath + "/arc_segments", schemaPath: "#/properties/arc_segments/minimum", keyword: "minimum", params: { comparison: ">=", limit: 1 }, message: "must be >= 1" };
          if (vErrors === null) {
            vErrors = [err87];
          } else {
            vErrors.push(err87);
          }
          errors++;
        }
      }
    }
    if (data.include_tracks !== void 0) {
      if (typeof data.include_tracks !== "boolean") {
        const err88 = { instancePath: instancePath + "/include_tracks", schemaPath: "#/properties/include_tracks/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err88];
        } else {
          vErrors.push(err88);
        }
        errors++;
      }
    }
    if (data.include_arcs !== void 0) {
      if (typeof data.include_arcs !== "boolean") {
        const err89 = { instancePath: instancePath + "/include_arcs", schemaPath: "#/properties/include_arcs/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err89];
        } else {
          vErrors.push(err89);
        }
        errors++;
      }
    }
    if (data.include_fills !== void 0) {
      if (typeof data.include_fills !== "boolean") {
        const err90 = { instancePath: instancePath + "/include_fills", schemaPath: "#/properties/include_fills/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err90];
        } else {
          vErrors.push(err90);
        }
        errors++;
      }
    }
    if (data.include_regions !== void 0) {
      if (typeof data.include_regions !== "boolean") {
        const err91 = { instancePath: instancePath + "/include_regions", schemaPath: "#/properties/include_regions/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err91];
        } else {
          vErrors.push(err91);
        }
        errors++;
      }
    }
    if (data.include_vias !== void 0) {
      if (typeof data.include_vias !== "boolean") {
        const err92 = { instancePath: instancePath + "/include_vias", schemaPath: "#/properties/include_vias/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err92];
        } else {
          vErrors.push(err92);
        }
        errors++;
      }
    }
    if (data.include_component_pads !== void 0) {
      if (typeof data.include_component_pads !== "boolean") {
        const err93 = { instancePath: instancePath + "/include_component_pads", schemaPath: "#/properties/include_component_pads/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err93];
        } else {
          vErrors.push(err93);
        }
        errors++;
      }
    }
    if (data.include_free_pads !== void 0) {
      if (typeof data.include_free_pads !== "boolean") {
        const err94 = { instancePath: instancePath + "/include_free_pads", schemaPath: "#/properties/include_free_pads/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err94];
        } else {
          vErrors.push(err94);
        }
        errors++;
      }
    }
    if (data.include_designators !== void 0) {
      let data35 = data.include_designators;
      const _errs136 = errors;
      let valid24 = false;
      let passing0 = null;
      const _errs137 = errors;
      if (typeof data35 !== "string") {
        const err95 = { instancePath: instancePath + "/include_designators", schemaPath: "#/$defs/StringList/oneOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err95];
        } else {
          vErrors.push(err95);
        }
        errors++;
      }
      var _valid7 = _errs137 === errors;
      if (_valid7) {
        valid24 = true;
        passing0 = 0;
      }
      const _errs139 = errors;
      if (Array.isArray(data35)) {
        const len0 = data35.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (typeof data35[i0] !== "string") {
            const err96 = { instancePath: instancePath + "/include_designators/" + i0, schemaPath: "#/$defs/StringList/oneOf/1/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err96];
            } else {
              vErrors.push(err96);
            }
            errors++;
          }
        }
      } else {
        const err97 = { instancePath: instancePath + "/include_designators", schemaPath: "#/$defs/StringList/oneOf/1/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err97];
        } else {
          vErrors.push(err97);
        }
        errors++;
      }
      var _valid7 = _errs139 === errors;
      if (_valid7 && valid24) {
        valid24 = false;
        passing0 = [passing0, 1];
      } else {
        if (_valid7) {
          valid24 = true;
          passing0 = 1;
        }
      }
      if (!valid24) {
        const err98 = { instancePath: instancePath + "/include_designators", schemaPath: "#/$defs/StringList/oneOf", keyword: "oneOf", params: { passingSchemas: passing0 }, message: "must match exactly one schema in oneOf" };
        if (vErrors === null) {
          vErrors = [err98];
        } else {
          vErrors.push(err98);
        }
        errors++;
      } else {
        errors = _errs136;
        if (vErrors !== null) {
          if (_errs136) {
            vErrors.length = _errs136;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.board_outline !== void 0) {
      if (!validate38(data.board_outline, { instancePath: instancePath + "/board_outline", parentData: data, parentDataProperty: "board_outline", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate38.errors : vErrors.concat(validate38.errors);
        errors = vErrors.length;
      }
    }
    if (data.features !== void 0) {
      if (!validate40(data.features, { instancePath: instancePath + "/features", parentData: data, parentDataProperty: "features", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate40.errors : vErrors.concat(validate40.errors);
        errors = vErrors.length;
      }
    }
    if (data.drills !== void 0) {
      if (!validate65(data.drills, { instancePath: instancePath + "/drills", parentData: data, parentDataProperty: "drills", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate65.errors : vErrors.concat(validate65.errors);
        errors = vErrors.length;
      }
    }
    if (data.enabled !== void 0) {
      let data40 = data.enabled;
      const _errs147 = errors;
      let valid27 = false;
      const _errs148 = errors;
      if (typeof data40 !== "boolean") {
        const err99 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err99];
        } else {
          vErrors.push(err99);
        }
        errors++;
      }
      var _valid8 = _errs148 === errors;
      valid27 = valid27 || _valid8;
      const _errs150 = errors;
      if (data40 !== null) {
        const err100 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err100];
        } else {
          vErrors.push(err100);
        }
        errors++;
      }
      var _valid8 = _errs150 === errors;
      valid27 = valid27 || _valid8;
      if (!valid27) {
        const err101 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err101];
        } else {
          vErrors.push(err101);
        }
        errors++;
      } else {
        errors = _errs147;
        if (vErrors !== null) {
          if (_errs147) {
            vErrors.length = _errs147;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.source_layer !== void 0) {
      let data41 = data.source_layer;
      const _errs153 = errors;
      let valid28 = false;
      const _errs154 = errors;
      if (typeof data41 !== "string") {
        const err102 = { instancePath: instancePath + "/source_layer", schemaPath: "#/properties/source_layer/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err102];
        } else {
          vErrors.push(err102);
        }
        errors++;
      }
      var _valid9 = _errs154 === errors;
      valid28 = valid28 || _valid9;
      const _errs156 = errors;
      if (data41 !== null) {
        const err103 = { instancePath: instancePath + "/source_layer", schemaPath: "#/properties/source_layer/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err103];
        } else {
          vErrors.push(err103);
        }
        errors++;
      }
      var _valid9 = _errs156 === errors;
      valid28 = valid28 || _valid9;
      if (!valid28) {
        const err104 = { instancePath: instancePath + "/source_layer", schemaPath: "#/properties/source_layer/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err104];
        } else {
          vErrors.push(err104);
        }
        errors++;
      } else {
        errors = _errs153;
        if (vErrors !== null) {
          if (_errs153) {
            vErrors.length = _errs153;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.insert_in_output !== void 0) {
      let data42 = data.insert_in_output;
      const _errs159 = errors;
      let valid29 = false;
      const _errs160 = errors;
      if (typeof data42 !== "boolean") {
        const err105 = { instancePath: instancePath + "/insert_in_output", schemaPath: "#/properties/insert_in_output/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err105];
        } else {
          vErrors.push(err105);
        }
        errors++;
      }
      var _valid10 = _errs160 === errors;
      valid29 = valid29 || _valid10;
      const _errs162 = errors;
      if (!validate67(data42, { instancePath: instancePath + "/insert_in_output", parentData: data, parentDataProperty: "insert_in_output", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate67.errors : vErrors.concat(validate67.errors);
        errors = vErrors.length;
      }
      var _valid10 = _errs162 === errors;
      valid29 = valid29 || _valid10;
      const _errs163 = errors;
      if (data42 !== null) {
        const err106 = { instancePath: instancePath + "/insert_in_output", schemaPath: "#/properties/insert_in_output/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err106];
        } else {
          vErrors.push(err106);
        }
        errors++;
      }
      var _valid10 = _errs163 === errors;
      valid29 = valid29 || _valid10;
      if (!valid29) {
        const err107 = { instancePath: instancePath + "/insert_in_output", schemaPath: "#/properties/insert_in_output/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err107];
        } else {
          vErrors.push(err107);
        }
        errors++;
      } else {
        errors = _errs159;
        if (vErrors !== null) {
          if (_errs159) {
            vErrors.length = _errs159;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.highlights !== void 0) {
      let data43 = data.highlights;
      const _errs166 = errors;
      let valid30 = false;
      const _errs167 = errors;
      if (Array.isArray(data43)) {
        const len1 = data43.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (!validate69(data43[i1], { instancePath: instancePath + "/highlights/" + i1, parentData: data43, parentDataProperty: i1, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate69.errors : vErrors.concat(validate69.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err108 = { instancePath: instancePath + "/highlights", schemaPath: "#/properties/highlights/anyOf/0/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err108];
        } else {
          vErrors.push(err108);
        }
        errors++;
      }
      var _valid11 = _errs167 === errors;
      valid30 = valid30 || _valid11;
      const _errs170 = errors;
      if (data43 !== null) {
        const err109 = { instancePath: instancePath + "/highlights", schemaPath: "#/properties/highlights/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err109];
        } else {
          vErrors.push(err109);
        }
        errors++;
      }
      var _valid11 = _errs170 === errors;
      valid30 = valid30 || _valid11;
      if (!valid30) {
        const err110 = { instancePath: instancePath + "/highlights", schemaPath: "#/properties/highlights/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err110];
        } else {
          vErrors.push(err110);
        }
        errors++;
      } else {
        errors = _errs166;
        if (vErrors !== null) {
          if (_errs166) {
            vErrors.length = _errs166;
          } else {
            vErrors = null;
          }
        }
      }
    }
  } else {
    const err111 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err111];
    } else {
      vErrors.push(err111);
    }
    errors++;
  }
  validate37.errors = vErrors;
  return errors === 0;
}
validate37.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate36(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate36.evaluated;
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
    if (data.pcb_layer_step !== void 0) {
      let data0 = data.pcb_layer_step;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (!validate37(data0, { instancePath: instancePath + "/pcb_layer_step", parentData: data, parentDataProperty: "pcb_layer_step", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate37.errors : vErrors.concat(validate37.errors);
        errors = vErrors.length;
      }
      var _valid0 = _errs7 === errors;
      valid3 = valid3 || _valid0;
      const _errs8 = errors;
      if (data0 !== null) {
        const err1 = { instancePath: instancePath + "/pcb_layer_step", schemaPath: "#/properties/pcb_layer_step/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      var _valid0 = _errs8 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err2 = { instancePath: instancePath + "/pcb_layer_step", schemaPath: "#/properties/pcb_layer_step/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
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
  } else {
    const err3 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err3];
    } else {
      vErrors.push(err3);
    }
    errors++;
  }
  validate36.errors = vErrors;
  return errors === 0;
}
validate36.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate73(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate73.evaluated;
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
    if (data.source_side !== void 0) {
      let data0 = data.source_side;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err1 = { instancePath: instancePath + "/source_side", schemaPath: "#/properties/source_side/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      if ("infer_single_side" !== data0) {
        const err2 = { instancePath: instancePath + "/source_side", schemaPath: "#/properties/source_side/anyOf/0/const", keyword: "const", params: { allowedValue: "infer_single_side" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid3 = valid3 || _valid0;
      const _errs9 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/source_side", schemaPath: "#/properties/source_side/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      if ("any" !== data0) {
        const err4 = { instancePath: instancePath + "/source_side", schemaPath: "#/properties/source_side/anyOf/1/const", keyword: "const", params: { allowedValue: "any" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (typeof data0 !== "string") {
        const err5 = { instancePath: instancePath + "/source_side", schemaPath: "#/properties/source_side/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      if ("none" !== data0) {
        const err6 = { instancePath: instancePath + "/source_side", schemaPath: "#/properties/source_side/anyOf/2/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs11 === errors;
      valid3 = valid3 || _valid0;
      const _errs13 = errors;
      if (typeof data0 !== "string") {
        const err7 = { instancePath: instancePath + "/source_side", schemaPath: "#/properties/source_side/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      if ("top" !== data0) {
        const err8 = { instancePath: instancePath + "/source_side", schemaPath: "#/properties/source_side/anyOf/3/const", keyword: "const", params: { allowedValue: "top" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid0 = _errs13 === errors;
      valid3 = valid3 || _valid0;
      const _errs15 = errors;
      if (typeof data0 !== "string") {
        const err9 = { instancePath: instancePath + "/source_side", schemaPath: "#/properties/source_side/anyOf/4/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      if ("bottom" !== data0) {
        const err10 = { instancePath: instancePath + "/source_side", schemaPath: "#/properties/source_side/anyOf/4/const", keyword: "const", params: { allowedValue: "bottom" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid0 = _errs15 === errors;
      valid3 = valid3 || _valid0;
      const _errs17 = errors;
      if (data0 !== null) {
        const err11 = { instancePath: instancePath + "/source_side", schemaPath: "#/properties/source_side/anyOf/5/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid0 = _errs17 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err12 = { instancePath: instancePath + "/source_side", schemaPath: "#/properties/source_side/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
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
    if (data.allow_side_agnostic_through_hole !== void 0) {
      let data1 = data.allow_side_agnostic_through_hole;
      const _errs20 = errors;
      let valid4 = false;
      const _errs21 = errors;
      if (typeof data1 !== "boolean") {
        const err13 = { instancePath: instancePath + "/allow_side_agnostic_through_hole", schemaPath: "#/properties/allow_side_agnostic_through_hole/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid1 = _errs21 === errors;
      valid4 = valid4 || _valid1;
      const _errs23 = errors;
      if (data1 !== null) {
        const err14 = { instancePath: instancePath + "/allow_side_agnostic_through_hole", schemaPath: "#/properties/allow_side_agnostic_through_hole/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid1 = _errs23 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err15 = { instancePath: instancePath + "/allow_side_agnostic_through_hole", schemaPath: "#/properties/allow_side_agnostic_through_hole/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      } else {
        errors = _errs20;
        if (vErrors !== null) {
          if (_errs20) {
            vErrors.length = _errs20;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.side_agnostic_kinds !== void 0) {
      let data2 = data.side_agnostic_kinds;
      const _errs26 = errors;
      let valid5 = false;
      const _errs27 = errors;
      if (Array.isArray(data2)) {
        const len0 = data2.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (typeof data2[i0] !== "string") {
            const err16 = { instancePath: instancePath + "/side_agnostic_kinds/" + i0, schemaPath: "#/$defs/StringArray/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err16];
            } else {
              vErrors.push(err16);
            }
            errors++;
          }
        }
      } else {
        const err17 = { instancePath: instancePath + "/side_agnostic_kinds", schemaPath: "#/$defs/StringArray/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      var _valid2 = _errs27 === errors;
      valid5 = valid5 || _valid2;
      const _errs32 = errors;
      if (data2 !== null) {
        const err18 = { instancePath: instancePath + "/side_agnostic_kinds", schemaPath: "#/properties/side_agnostic_kinds/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
      var _valid2 = _errs32 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err19 = { instancePath: instancePath + "/side_agnostic_kinds", schemaPath: "#/properties/side_agnostic_kinds/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      } else {
        errors = _errs26;
        if (vErrors !== null) {
          if (_errs26) {
            vErrors.length = _errs26;
          } else {
            vErrors = null;
          }
        }
      }
    }
  } else {
    const err20 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err20];
    } else {
      vErrors.push(err20);
    }
    errors++;
  }
  validate73.errors = vErrors;
  return errors === 0;
}
validate73.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate77(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate77.evaluated;
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
    if (data.min !== void 0) {
      let data0 = data.min;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (!(typeof data0 == "number")) {
        const err1 = { instancePath: instancePath + "/min", schemaPath: "#/properties/min/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid3 = valid3 || _valid0;
      const _errs9 = errors;
      if (data0 !== null) {
        const err2 = { instancePath: instancePath + "/min", schemaPath: "#/properties/min/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err3 = { instancePath: instancePath + "/min", schemaPath: "#/properties/min/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
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
    if (data.max !== void 0) {
      let data1 = data.max;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (!(typeof data1 == "number")) {
        const err4 = { instancePath: instancePath + "/max", schemaPath: "#/properties/max/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid1 = _errs13 === errors;
      valid4 = valid4 || _valid1;
      const _errs15 = errors;
      if (data1 !== null) {
        const err5 = { instancePath: instancePath + "/max", schemaPath: "#/properties/max/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err6 = { instancePath: instancePath + "/max", schemaPath: "#/properties/max/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
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
  } else {
    const err7 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err7];
    } else {
      vErrors.push(err7);
    }
    errors++;
  }
  validate77.errors = vErrors;
  return errors === 0;
}
validate77.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate76(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate76.evaluated;
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
    if (data.object !== void 0) {
      let data0 = data.object;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err1 = { instancePath: instancePath + "/object", schemaPath: "#/properties/object/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid3 = valid3 || _valid0;
      const _errs9 = errors;
      if (data0 !== null) {
        const err2 = { instancePath: instancePath + "/object", schemaPath: "#/properties/object/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err3 = { instancePath: instancePath + "/object", schemaPath: "#/properties/object/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
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
    if (data.type !== void 0) {
      let data1 = data.type;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err4 = { instancePath: instancePath + "/type", schemaPath: "#/properties/type/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid1 = _errs13 === errors;
      valid4 = valid4 || _valid1;
      const _errs15 = errors;
      if (data1 !== null) {
        const err5 = { instancePath: instancePath + "/type", schemaPath: "#/properties/type/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err6 = { instancePath: instancePath + "/type", schemaPath: "#/properties/type/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
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
    if (data.kind !== void 0) {
      let data2 = data.kind;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err7 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (Array.isArray(data2)) {
        const len0 = data2.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (typeof data2[i0] !== "string") {
            const err8 = { instancePath: instancePath + "/kind/" + i0, schemaPath: "#/$defs/StringArray/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err8];
            } else {
              vErrors.push(err8);
            }
            errors++;
          }
        }
      } else {
        const err9 = { instancePath: instancePath + "/kind", schemaPath: "#/$defs/StringArray/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      const _errs26 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs26 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
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
    if (data.kinds !== void 0) {
      let data4 = data.kinds;
      const _errs29 = errors;
      let valid9 = false;
      const _errs30 = errors;
      if (typeof data4 !== "string") {
        const err12 = { instancePath: instancePath + "/kinds", schemaPath: "#/properties/kinds/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid3 = _errs30 === errors;
      valid9 = valid9 || _valid3;
      const _errs32 = errors;
      if (Array.isArray(data4)) {
        const len1 = data4.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (typeof data4[i1] !== "string") {
            const err13 = { instancePath: instancePath + "/kinds/" + i1, schemaPath: "#/$defs/StringArray/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err13];
            } else {
              vErrors.push(err13);
            }
            errors++;
          }
        }
      } else {
        const err14 = { instancePath: instancePath + "/kinds", schemaPath: "#/$defs/StringArray/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid3 = _errs32 === errors;
      valid9 = valid9 || _valid3;
      const _errs37 = errors;
      if (data4 !== null) {
        const err15 = { instancePath: instancePath + "/kinds", schemaPath: "#/properties/kinds/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid3 = _errs37 === errors;
      valid9 = valid9 || _valid3;
      if (!valid9) {
        const err16 = { instancePath: instancePath + "/kinds", schemaPath: "#/properties/kinds/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
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
    if (data.designators !== void 0) {
      let data6 = data.designators;
      const _errs40 = errors;
      let valid13 = false;
      const _errs41 = errors;
      if (typeof data6 !== "string") {
        const err17 = { instancePath: instancePath + "/designators", schemaPath: "#/properties/designators/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      var _valid4 = _errs41 === errors;
      valid13 = valid13 || _valid4;
      const _errs43 = errors;
      if (Array.isArray(data6)) {
        const len2 = data6.length;
        for (let i2 = 0; i2 < len2; i2++) {
          if (typeof data6[i2] !== "string") {
            const err18 = { instancePath: instancePath + "/designators/" + i2, schemaPath: "#/$defs/StringArray/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err18];
            } else {
              vErrors.push(err18);
            }
            errors++;
          }
        }
      } else {
        const err19 = { instancePath: instancePath + "/designators", schemaPath: "#/$defs/StringArray/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
      var _valid4 = _errs43 === errors;
      valid13 = valid13 || _valid4;
      const _errs48 = errors;
      if (data6 !== null) {
        const err20 = { instancePath: instancePath + "/designators", schemaPath: "#/properties/designators/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      var _valid4 = _errs48 === errors;
      valid13 = valid13 || _valid4;
      if (!valid13) {
        const err21 = { instancePath: instancePath + "/designators", schemaPath: "#/properties/designators/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      } else {
        errors = _errs40;
        if (vErrors !== null) {
          if (_errs40) {
            vErrors.length = _errs40;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.hole_size_mils !== void 0) {
      let data8 = data.hole_size_mils;
      const _errs51 = errors;
      let valid17 = false;
      const _errs52 = errors;
      if (!validate77(data8, { instancePath: instancePath + "/hole_size_mils", parentData: data, parentDataProperty: "hole_size_mils", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate77.errors : vErrors.concat(validate77.errors);
        errors = vErrors.length;
      }
      var _valid5 = _errs52 === errors;
      valid17 = valid17 || _valid5;
      const _errs53 = errors;
      if (data8 !== null) {
        const err22 = { instancePath: instancePath + "/hole_size_mils", schemaPath: "#/properties/hole_size_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
      var _valid5 = _errs53 === errors;
      valid17 = valid17 || _valid5;
      if (!valid17) {
        const err23 = { instancePath: instancePath + "/hole_size_mils", schemaPath: "#/properties/hole_size_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      } else {
        errors = _errs51;
        if (vErrors !== null) {
          if (_errs51) {
            vErrors.length = _errs51;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.plated !== void 0) {
      let data9 = data.plated;
      const _errs56 = errors;
      let valid18 = false;
      const _errs57 = errors;
      if (typeof data9 !== "boolean") {
        const err24 = { instancePath: instancePath + "/plated", schemaPath: "#/properties/plated/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      var _valid6 = _errs57 === errors;
      valid18 = valid18 || _valid6;
      const _errs59 = errors;
      if (data9 !== null) {
        const err25 = { instancePath: instancePath + "/plated", schemaPath: "#/properties/plated/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
      var _valid6 = _errs59 === errors;
      valid18 = valid18 || _valid6;
      if (!valid18) {
        const err26 = { instancePath: instancePath + "/plated", schemaPath: "#/properties/plated/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      } else {
        errors = _errs56;
        if (vErrors !== null) {
          if (_errs56) {
            vErrors.length = _errs56;
          } else {
            vErrors = null;
          }
        }
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
  validate76.errors = vErrors;
  return errors === 0;
}
validate76.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate83(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate83.evaluated;
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
    if (data.kind === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "kind" }, message: "must have required property 'kind'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.part !== void 0) {
      let data0 = data.part;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err2 = { instancePath: instancePath + "/part", schemaPath: "#/properties/part/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid3 = valid3 || _valid0;
      const _errs9 = errors;
      if (data0 !== null) {
        const err3 = { instancePath: instancePath + "/part", schemaPath: "#/properties/part/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err4 = { instancePath: instancePath + "/part", schemaPath: "#/properties/part/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
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
    if (data.role !== void 0) {
      let data1 = data.role;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err5 = { instancePath: instancePath + "/role", schemaPath: "#/properties/role/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid1 = _errs13 === errors;
      valid4 = valid4 || _valid1;
      const _errs15 = errors;
      if (data1 !== null) {
        const err6 = { instancePath: instancePath + "/role", schemaPath: "#/properties/role/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err7 = { instancePath: instancePath + "/role", schemaPath: "#/properties/role/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.description !== void 0) {
      let data2 = data.description;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err8 = { instancePath: instancePath + "/description", schemaPath: "#/properties/description/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err9 = { instancePath: instancePath + "/description", schemaPath: "#/properties/description/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err10 = { instancePath: instancePath + "/description", schemaPath: "#/properties/description/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.symbol_name !== void 0) {
      let data3 = data.symbol_name;
      const _errs24 = errors;
      let valid6 = false;
      const _errs25 = errors;
      if (typeof data3 !== "string") {
        const err11 = { instancePath: instancePath + "/symbol_name", schemaPath: "#/properties/symbol_name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid3 = _errs25 === errors;
      valid6 = valid6 || _valid3;
      const _errs27 = errors;
      if (data3 !== null) {
        const err12 = { instancePath: instancePath + "/symbol_name", schemaPath: "#/properties/symbol_name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid3 = _errs27 === errors;
      valid6 = valid6 || _valid3;
      if (!valid6) {
        const err13 = { instancePath: instancePath + "/symbol_name", schemaPath: "#/properties/symbol_name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      } else {
        errors = _errs24;
        if (vErrors !== null) {
          if (_errs24) {
            vErrors.length = _errs24;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.footprint_name !== void 0) {
      let data4 = data.footprint_name;
      const _errs30 = errors;
      let valid7 = false;
      const _errs31 = errors;
      if (typeof data4 !== "string") {
        const err14 = { instancePath: instancePath + "/footprint_name", schemaPath: "#/properties/footprint_name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid4 = _errs31 === errors;
      valid7 = valid7 || _valid4;
      const _errs33 = errors;
      if (data4 !== null) {
        const err15 = { instancePath: instancePath + "/footprint_name", schemaPath: "#/properties/footprint_name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid4 = _errs33 === errors;
      valid7 = valid7 || _valid4;
      if (!valid7) {
        const err16 = { instancePath: instancePath + "/footprint_name", schemaPath: "#/properties/footprint_name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      } else {
        errors = _errs30;
        if (vErrors !== null) {
          if (_errs30) {
            vErrors.length = _errs30;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.designator_prefix !== void 0) {
      let data5 = data.designator_prefix;
      const _errs36 = errors;
      let valid8 = false;
      const _errs37 = errors;
      if (typeof data5 !== "string") {
        const err17 = { instancePath: instancePath + "/designator_prefix", schemaPath: "#/properties/designator_prefix/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      var _valid5 = _errs37 === errors;
      valid8 = valid8 || _valid5;
      const _errs39 = errors;
      if (data5 !== null) {
        const err18 = { instancePath: instancePath + "/designator_prefix", schemaPath: "#/properties/designator_prefix/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
      var _valid5 = _errs39 === errors;
      valid8 = valid8 || _valid5;
      if (!valid8) {
        const err19 = { instancePath: instancePath + "/designator_prefix", schemaPath: "#/properties/designator_prefix/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      } else {
        errors = _errs36;
        if (vErrors !== null) {
          if (_errs36) {
            vErrors.length = _errs36;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.signal_pad_designator !== void 0) {
      let data6 = data.signal_pad_designator;
      const _errs42 = errors;
      let valid9 = false;
      const _errs43 = errors;
      if (typeof data6 !== "string") {
        const err20 = { instancePath: instancePath + "/signal_pad_designator", schemaPath: "#/properties/signal_pad_designator/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      var _valid6 = _errs43 === errors;
      valid9 = valid9 || _valid6;
      const _errs45 = errors;
      if (data6 !== null) {
        const err21 = { instancePath: instancePath + "/signal_pad_designator", schemaPath: "#/properties/signal_pad_designator/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      var _valid6 = _errs45 === errors;
      valid9 = valid9 || _valid6;
      if (!valid9) {
        const err22 = { instancePath: instancePath + "/signal_pad_designator", schemaPath: "#/properties/signal_pad_designator/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      } else {
        errors = _errs42;
        if (vErrors !== null) {
          if (_errs42) {
            vErrors.length = _errs42;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.kind !== void 0) {
      let data7 = data.kind;
      if (typeof data7 !== "string") {
        const err23 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      if ("mate_component" !== data7) {
        const err24 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/const", keyword: "const", params: { allowedValue: "mate_component" }, message: "must be equal to constant" };
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
  validate83.errors = vErrors;
  return errors === 0;
}
validate83.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate86(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate86.evaluated;
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
    if (data.mode !== void 0) {
      let data0 = data.mode;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err1 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid3 = valid3 || _valid0;
      const _errs9 = errors;
      if (data0 !== null) {
        const err2 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err3 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
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
    if (data.outline_count !== void 0) {
      let data1 = data.outline_count;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (!(typeof data1 == "number" && (!(data1 % 1) && !isNaN(data1)))) {
        const err4 = { instancePath: instancePath + "/outline_count", schemaPath: "#/properties/outline_count/anyOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid1 = _errs13 === errors;
      valid4 = valid4 || _valid1;
      const _errs15 = errors;
      if (data1 !== null) {
        const err5 = { instancePath: instancePath + "/outline_count", schemaPath: "#/properties/outline_count/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err6 = { instancePath: instancePath + "/outline_count", schemaPath: "#/properties/outline_count/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
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
      if (typeof data1 == "number") {
        if (data1 < 1 || isNaN(data1)) {
          const err7 = { instancePath: instancePath + "/outline_count", schemaPath: "#/properties/outline_count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 1 }, message: "must be >= 1" };
          if (vErrors === null) {
            vErrors = [err7];
          } else {
            vErrors.push(err7);
          }
          errors++;
        }
      }
    }
    if (data.clearance_mils !== void 0) {
      if (!(typeof data.clearance_mils == "number")) {
        const err8 = { instancePath: instancePath + "/clearance_mils", schemaPath: "#/properties/clearance_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
    if (data.outline_spacing_mils !== void 0) {
      if (!(typeof data.outline_spacing_mils == "number")) {
        const err9 = { instancePath: instancePath + "/outline_spacing_mils", schemaPath: "#/properties/outline_spacing_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    if (data.stroke_width_mils !== void 0) {
      if (!(typeof data.stroke_width_mils == "number")) {
        const err10 = { instancePath: instancePath + "/stroke_width_mils", schemaPath: "#/properties/stroke_width_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
    }
  } else {
    const err11 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err11];
    } else {
      vErrors.push(err11);
    }
    errors++;
  }
  validate86.errors = vErrors;
  return errors === 0;
}
validate86.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate85(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate85.evaluated;
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
    if (data.kind === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "kind" }, message: "must have required property 'kind'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.kind !== void 0) {
      let data0 = data.kind;
      if (typeof data0 !== "string") {
        const err2 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      if ("reference_graphics" !== data0) {
        const err3 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/const", keyword: "const", params: { allowedValue: "reference_graphics" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.shape !== void 0) {
      let data1 = data.shape;
      const _errs8 = errors;
      let valid3 = false;
      const _errs9 = errors;
      if (typeof data1 !== "string") {
        const err4 = { instancePath: instancePath + "/shape", schemaPath: "#/properties/shape/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      if ("source_pad_outline" !== data1) {
        const err5 = { instancePath: instancePath + "/shape", schemaPath: "#/properties/shape/anyOf/0/const", keyword: "const", params: { allowedValue: "source_pad_outline" }, message: "must be equal to constant" };
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
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/shape", schemaPath: "#/properties/shape/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      if ("destination_pad_outline" !== data1) {
        const err7 = { instancePath: instancePath + "/shape", schemaPath: "#/properties/shape/anyOf/1/const", keyword: "const", params: { allowedValue: "destination_pad_outline" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid0 = _errs11 === errors;
      valid3 = valid3 || _valid0;
      const _errs13 = errors;
      if (data1 !== null) {
        const err8 = { instancePath: instancePath + "/shape", schemaPath: "#/properties/shape/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid0 = _errs13 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err9 = { instancePath: instancePath + "/shape", schemaPath: "#/properties/shape/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
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
    if (data.layer !== void 0) {
      let data2 = data.layer;
      const _errs16 = errors;
      let valid4 = false;
      const _errs17 = errors;
      if (typeof data2 !== "string") {
        const err10 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data2 !== null) {
        const err11 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid1 = _errs19 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err12 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
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
    if (data.enabled !== void 0) {
      let data3 = data.enabled;
      const _errs22 = errors;
      let valid5 = false;
      const _errs23 = errors;
      if (typeof data3 !== "boolean") {
        const err13 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid2 = _errs23 === errors;
      valid5 = valid5 || _valid2;
      const _errs25 = errors;
      if (data3 !== null) {
        const err14 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid2 = _errs25 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err15 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      } else {
        errors = _errs22;
        if (vErrors !== null) {
          if (_errs22) {
            vErrors.length = _errs22;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.style !== void 0) {
      if (!validate86(data.style, { instancePath: instancePath + "/style", parentData: data, parentDataProperty: "style", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate86.errors : vErrors.concat(validate86.errors);
        errors = vErrors.length;
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
  validate85.errors = vErrors;
  return errors === 0;
}
validate85.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate91(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate91.evaluated;
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
    if (data.side !== void 0) {
      let data0 = data.side;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err1 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      if ("left" !== data0) {
        const err2 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/const", keyword: "const", params: { allowedValue: "left" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid3 = valid3 || _valid0;
      const _errs9 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      if ("right" !== data0) {
        const err4 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/1/const", keyword: "const", params: { allowedValue: "right" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (typeof data0 !== "string") {
        const err5 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      if ("board_left" !== data0) {
        const err6 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/2/const", keyword: "const", params: { allowedValue: "board_left" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs11 === errors;
      valid3 = valid3 || _valid0;
      const _errs13 = errors;
      if (typeof data0 !== "string") {
        const err7 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      if ("board_right" !== data0) {
        const err8 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/3/const", keyword: "const", params: { allowedValue: "board_right" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid0 = _errs13 === errors;
      valid3 = valid3 || _valid0;
      const _errs15 = errors;
      if (data0 !== null) {
        const err9 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/4/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid0 = _errs15 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err10 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
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
    if (data.offset_mils !== void 0) {
      let data1 = data.offset_mils;
      const _errs18 = errors;
      let valid4 = false;
      const _errs19 = errors;
      if (Array.isArray(data1)) {
        if (data1.length > 2) {
          const err11 = { instancePath: instancePath + "/offset_mils", schemaPath: "#/$defs/Pair/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err11];
          } else {
            vErrors.push(err11);
          }
          errors++;
        }
        if (data1.length < 2) {
          const err12 = { instancePath: instancePath + "/offset_mils", schemaPath: "#/$defs/Pair/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err12];
          } else {
            vErrors.push(err12);
          }
          errors++;
        }
        const len0 = data1.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!(typeof data1[i0] == "number")) {
            const err13 = { instancePath: instancePath + "/offset_mils/" + i0, schemaPath: "#/$defs/Pair/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err13];
            } else {
              vErrors.push(err13);
            }
            errors++;
          }
        }
      } else {
        const err14 = { instancePath: instancePath + "/offset_mils", schemaPath: "#/$defs/Pair/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid1 = _errs19 === errors;
      valid4 = valid4 || _valid1;
      const _errs24 = errors;
      if (data1 !== null) {
        const err15 = { instancePath: instancePath + "/offset_mils", schemaPath: "#/properties/offset_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid1 = _errs24 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err16 = { instancePath: instancePath + "/offset_mils", schemaPath: "#/properties/offset_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
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
    if (data.box_size_mils !== void 0) {
      let data3 = data.box_size_mils;
      const _errs27 = errors;
      let valid8 = false;
      const _errs28 = errors;
      if (Array.isArray(data3)) {
        if (data3.length > 2) {
          const err17 = { instancePath: instancePath + "/box_size_mils", schemaPath: "#/$defs/Pair/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err17];
          } else {
            vErrors.push(err17);
          }
          errors++;
        }
        if (data3.length < 2) {
          const err18 = { instancePath: instancePath + "/box_size_mils", schemaPath: "#/$defs/Pair/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err18];
          } else {
            vErrors.push(err18);
          }
          errors++;
        }
        const len1 = data3.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (!(typeof data3[i1] == "number")) {
            const err19 = { instancePath: instancePath + "/box_size_mils/" + i1, schemaPath: "#/$defs/Pair/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err19];
            } else {
              vErrors.push(err19);
            }
            errors++;
          }
        }
      } else {
        const err20 = { instancePath: instancePath + "/box_size_mils", schemaPath: "#/$defs/Pair/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      var _valid2 = _errs28 === errors;
      valid8 = valid8 || _valid2;
      const _errs33 = errors;
      if (data3 !== null) {
        const err21 = { instancePath: instancePath + "/box_size_mils", schemaPath: "#/properties/box_size_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      var _valid2 = _errs33 === errors;
      valid8 = valid8 || _valid2;
      if (!valid8) {
        const err22 = { instancePath: instancePath + "/box_size_mils", schemaPath: "#/properties/box_size_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      } else {
        errors = _errs27;
        if (vErrors !== null) {
          if (_errs27) {
            vErrors.length = _errs27;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.center_box_on_target !== void 0) {
      let data5 = data.center_box_on_target;
      const _errs36 = errors;
      let valid12 = false;
      const _errs37 = errors;
      if (typeof data5 !== "boolean") {
        const err23 = { instancePath: instancePath + "/center_box_on_target", schemaPath: "#/properties/center_box_on_target/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      var _valid3 = _errs37 === errors;
      valid12 = valid12 || _valid3;
      const _errs39 = errors;
      if (data5 !== null) {
        const err24 = { instancePath: instancePath + "/center_box_on_target", schemaPath: "#/properties/center_box_on_target/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      var _valid3 = _errs39 === errors;
      valid12 = valid12 || _valid3;
      if (!valid12) {
        const err25 = { instancePath: instancePath + "/center_box_on_target", schemaPath: "#/properties/center_box_on_target/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      } else {
        errors = _errs36;
        if (vErrors !== null) {
          if (_errs36) {
            vErrors.length = _errs36;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.row_spacing_mils !== void 0) {
      let data6 = data.row_spacing_mils;
      const _errs42 = errors;
      let valid13 = false;
      const _errs43 = errors;
      if (!(typeof data6 == "number")) {
        const err26 = { instancePath: instancePath + "/row_spacing_mils", schemaPath: "#/properties/row_spacing_mils/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
      var _valid4 = _errs43 === errors;
      valid13 = valid13 || _valid4;
      const _errs45 = errors;
      if (data6 !== null) {
        const err27 = { instancePath: instancePath + "/row_spacing_mils", schemaPath: "#/properties/row_spacing_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
      var _valid4 = _errs45 === errors;
      valid13 = valid13 || _valid4;
      if (!valid13) {
        const err28 = { instancePath: instancePath + "/row_spacing_mils", schemaPath: "#/properties/row_spacing_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      } else {
        errors = _errs42;
        if (vErrors !== null) {
          if (_errs42) {
            vErrors.length = _errs42;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.column_spacing_mils !== void 0) {
      let data7 = data.column_spacing_mils;
      const _errs48 = errors;
      let valid14 = false;
      const _errs49 = errors;
      if (!(typeof data7 == "number")) {
        const err29 = { instancePath: instancePath + "/column_spacing_mils", schemaPath: "#/properties/column_spacing_mils/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      }
      var _valid5 = _errs49 === errors;
      valid14 = valid14 || _valid5;
      const _errs51 = errors;
      if (data7 !== null) {
        const err30 = { instancePath: instancePath + "/column_spacing_mils", schemaPath: "#/properties/column_spacing_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
        }
        errors++;
      }
      var _valid5 = _errs51 === errors;
      valid14 = valid14 || _valid5;
      if (!valid14) {
        const err31 = { instancePath: instancePath + "/column_spacing_mils", schemaPath: "#/properties/column_spacing_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      } else {
        errors = _errs48;
        if (vErrors !== null) {
          if (_errs48) {
            vErrors.length = _errs48;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.auto_width_padding_mils !== void 0) {
      let data8 = data.auto_width_padding_mils;
      const _errs54 = errors;
      let valid15 = false;
      const _errs55 = errors;
      if (!(typeof data8 == "number")) {
        const err32 = { instancePath: instancePath + "/auto_width_padding_mils", schemaPath: "#/properties/auto_width_padding_mils/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
        }
        errors++;
      }
      var _valid6 = _errs55 === errors;
      valid15 = valid15 || _valid6;
      const _errs57 = errors;
      if (data8 !== null) {
        const err33 = { instancePath: instancePath + "/auto_width_padding_mils", schemaPath: "#/properties/auto_width_padding_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
      var _valid6 = _errs57 === errors;
      valid15 = valid15 || _valid6;
      if (!valid15) {
        const err34 = { instancePath: instancePath + "/auto_width_padding_mils", schemaPath: "#/properties/auto_width_padding_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
        }
        errors++;
      } else {
        errors = _errs54;
        if (vErrors !== null) {
          if (_errs54) {
            vErrors.length = _errs54;
          } else {
            vErrors = null;
          }
        }
      }
    }
  } else {
    const err35 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err35];
    } else {
      vErrors.push(err35);
    }
    errors++;
  }
  validate91.errors = vErrors;
  return errors === 0;
}
validate91.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate89(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate89.evaluated;
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
    if (data.kind === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "kind" }, message: "must have required property 'kind'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.kind !== void 0) {
      let data0 = data.kind;
      if (typeof data0 !== "string") {
        const err2 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      if ("label" !== data0) {
        const err3 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/const", keyword: "const", params: { allowedValue: "label" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.enabled !== void 0) {
      let data1 = data.enabled;
      const _errs8 = errors;
      let valid3 = false;
      const _errs9 = errors;
      if (typeof data1 !== "boolean") {
        const err4 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (data1 !== null) {
        const err5 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid0 = _errs11 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err6 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
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
    if (data.style !== void 0) {
      let data2 = data.style;
      const _errs14 = errors;
      let valid4 = false;
      const _errs15 = errors;
      if (!validate33(data2, { instancePath: instancePath + "/style", parentData: data, parentDataProperty: "style", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate33.errors : vErrors.concat(validate33.errors);
        errors = vErrors.length;
      }
      var _valid1 = _errs15 === errors;
      valid4 = valid4 || _valid1;
      const _errs16 = errors;
      if (data2 !== null) {
        const err7 = { instancePath: instancePath + "/style", schemaPath: "#/properties/style/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid1 = _errs16 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err8 = { instancePath: instancePath + "/style", schemaPath: "#/properties/style/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      } else {
        errors = _errs14;
        if (vErrors !== null) {
          if (_errs14) {
            vErrors.length = _errs14;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.text !== void 0) {
      let data3 = data.text;
      const _errs19 = errors;
      let valid5 = false;
      const _errs20 = errors;
      if (typeof data3 !== "string") {
        const err9 = { instancePath: instancePath + "/text", schemaPath: "#/properties/text/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs20 === errors;
      valid5 = valid5 || _valid2;
      const _errs22 = errors;
      if (data3 !== null) {
        const err10 = { instancePath: instancePath + "/text", schemaPath: "#/properties/text/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs22 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/text", schemaPath: "#/properties/text/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      } else {
        errors = _errs19;
        if (vErrors !== null) {
          if (_errs19) {
            vErrors.length = _errs19;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.value !== void 0) {
      let data4 = data.value;
      const _errs25 = errors;
      let valid6 = false;
      const _errs26 = errors;
      if (typeof data4 !== "string") {
        const err12 = { instancePath: instancePath + "/value", schemaPath: "#/properties/value/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid3 = _errs26 === errors;
      valid6 = valid6 || _valid3;
      const _errs28 = errors;
      if (data4 !== null) {
        const err13 = { instancePath: instancePath + "/value", schemaPath: "#/properties/value/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid3 = _errs28 === errors;
      valid6 = valid6 || _valid3;
      if (!valid6) {
        const err14 = { instancePath: instancePath + "/value", schemaPath: "#/properties/value/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      } else {
        errors = _errs25;
        if (vErrors !== null) {
          if (_errs25) {
            vErrors.length = _errs25;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.placement !== void 0) {
      let data5 = data.placement;
      const _errs31 = errors;
      let valid7 = false;
      const _errs32 = errors;
      if (!validate91(data5, { instancePath: instancePath + "/placement", parentData: data, parentDataProperty: "placement", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate91.errors : vErrors.concat(validate91.errors);
        errors = vErrors.length;
      }
      var _valid4 = _errs32 === errors;
      valid7 = valid7 || _valid4;
      const _errs33 = errors;
      if (data5 !== null) {
        const err15 = { instancePath: instancePath + "/placement", schemaPath: "#/properties/placement/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid4 = _errs33 === errors;
      valid7 = valid7 || _valid4;
      if (!valid7) {
        const err16 = { instancePath: instancePath + "/placement", schemaPath: "#/properties/placement/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      } else {
        errors = _errs31;
        if (vErrors !== null) {
          if (_errs31) {
            vErrors.length = _errs31;
          } else {
            vErrors = null;
          }
        }
      }
    }
  } else {
    const err17 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err17];
    } else {
      vErrors.push(err17);
    }
    errors++;
  }
  validate89.errors = vErrors;
  return errors === 0;
}
validate89.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate82(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate82.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  const _errs0 = errors;
  let valid0 = false;
  const _errs1 = errors;
  if (!validate83(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate83.errors : vErrors.concat(validate83.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs1 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    var props0 = true;
  }
  const _errs2 = errors;
  if (!validate85(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate85.errors : vErrors.concat(validate85.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs2 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs3 = errors;
  if (!validate89(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate89.errors : vErrors.concat(validate89.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs3 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  if (!valid0) {
    const err0 = { instancePath, schemaPath: "#/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
    if (vErrors === null) {
      vErrors = [err0];
    } else {
      vErrors.push(err0);
    }
    errors++;
  } else {
    errors = _errs0;
    if (vErrors !== null) {
      if (_errs0) {
        vErrors.length = _errs0;
      } else {
        vErrors = null;
      }
    }
  }
  validate82.errors = vErrors;
  evaluated0.props = props0;
  return errors === 0;
}
validate82.evaluated = { "dynamicProps": true, "dynamicItems": false };
function validate75(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate75.evaluated;
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
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err1 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid3 = valid3 || _valid0;
      const _errs9 = errors;
      if (data0 !== null) {
        const err2 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
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
    if (data.source !== void 0) {
      let data1 = data.source;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (!validate76(data1, { instancePath: instancePath + "/source", parentData: data, parentDataProperty: "source", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate76.errors : vErrors.concat(validate76.errors);
        errors = vErrors.length;
      }
      var _valid1 = _errs13 === errors;
      valid4 = valid4 || _valid1;
      const _errs14 = errors;
      if (data1 !== null) {
        const err4 = { instancePath: instancePath + "/source", schemaPath: "#/properties/source/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid1 = _errs14 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err5 = { instancePath: instancePath + "/source", schemaPath: "#/properties/source/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
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
    if (data.select !== void 0) {
      let data2 = data.select;
      if (data2 && typeof data2 == "object" && !Array.isArray(data2)) {
        if (data2.components !== void 0) {
          if (!validate76(data2.components, { instancePath: instancePath + "/select/components", parentData: data2, parentDataProperty: "components", rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate76.errors : vErrors.concat(validate76.errors);
            errors = vErrors.length;
          }
        }
        if (data2.free_pads !== void 0) {
          if (!validate76(data2.free_pads, { instancePath: instancePath + "/select/free_pads", parentData: data2, parentDataProperty: "free_pads", rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate76.errors : vErrors.concat(validate76.errors);
            errors = vErrors.length;
          }
        }
        for (const key1 in data2) {
          if (key1 !== "components" && key1 !== "free_pads") {
            const err6 = { instancePath: instancePath + "/select/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/properties/select/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err6];
            } else {
              vErrors.push(err6);
            }
            errors++;
          }
        }
      } else {
        const err7 = { instancePath: instancePath + "/select", schemaPath: "#/properties/select/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.actions !== void 0) {
      let data6 = data.actions;
      if (Array.isArray(data6)) {
        const len0 = data6.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!validate82(data6[i0], { instancePath: instancePath + "/actions/" + i0, parentData: data6, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate82.errors : vErrors.concat(validate82.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err8 = { instancePath: instancePath + "/actions", schemaPath: "#/properties/actions/type", keyword: "type", params: { type: "array" }, message: "must be array" };
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
  validate75.errors = vErrors;
  return errors === 0;
}
validate75.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate97(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate97.evaluated;
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
    if (data.enabled !== void 0) {
      let data0 = data.enabled;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "boolean") {
        const err1 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid3 = valid3 || _valid0;
      const _errs9 = errors;
      if (data0 !== null) {
        const err2 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err3 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
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
    if (data.layer !== void 0) {
      let data1 = data.layer;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err4 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid1 = _errs13 === errors;
      valid4 = valid4 || _valid1;
      const _errs15 = errors;
      if (data1 !== null) {
        const err5 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err6 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
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
    if (data.stroke_width_mils !== void 0) {
      if (!(typeof data.stroke_width_mils == "number")) {
        const err7 = { instancePath: instancePath + "/stroke_width_mils", schemaPath: "#/properties/stroke_width_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
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
  validate97.errors = vErrors;
  return errors === 0;
}
validate97.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate96(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate96.evaluated;
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
    if (data.outline !== void 0) {
      let data0 = data.outline;
      if (data0 && typeof data0 == "object" && !Array.isArray(data0)) {
        if (data0.graphics !== void 0) {
          if (!validate97(data0.graphics, { instancePath: instancePath + "/outline/graphics", parentData: data0, parentDataProperty: "graphics", rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate97.errors : vErrors.concat(validate97.errors);
            errors = vErrors.length;
          }
        }
        for (const key1 in data0) {
          if (key1 !== "graphics") {
            const err1 = { instancePath: instancePath + "/outline/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/properties/outline/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err1];
            } else {
              vErrors.push(err1);
            }
            errors++;
          }
        }
      } else {
        const err2 = { instancePath: instancePath + "/outline", schemaPath: "#/properties/outline/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
    if (data.cutouts !== void 0) {
      let data3 = data.cutouts;
      if (data3 && typeof data3 == "object" && !Array.isArray(data3)) {
        if (data3.graphics !== void 0) {
          if (!validate97(data3.graphics, { instancePath: instancePath + "/cutouts/graphics", parentData: data3, parentDataProperty: "graphics", rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate97.errors : vErrors.concat(validate97.errors);
            errors = vErrors.length;
          }
        }
        if (data3.scope !== void 0) {
          let data5 = data3.scope;
          const _errs15 = errors;
          let valid6 = false;
          const _errs16 = errors;
          if (typeof data5 !== "string") {
            const err3 = { instancePath: instancePath + "/cutouts/scope", schemaPath: "#/properties/cutouts/properties/scope/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err3];
            } else {
              vErrors.push(err3);
            }
            errors++;
          }
          if ("all" !== data5) {
            const err4 = { instancePath: instancePath + "/cutouts/scope", schemaPath: "#/properties/cutouts/properties/scope/anyOf/0/const", keyword: "const", params: { allowedValue: "all" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err4];
            } else {
              vErrors.push(err4);
            }
            errors++;
          }
          var _valid0 = _errs16 === errors;
          valid6 = valid6 || _valid0;
          const _errs18 = errors;
          if (typeof data5 !== "string") {
            const err5 = { instancePath: instancePath + "/cutouts/scope", schemaPath: "#/properties/cutouts/properties/scope/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err5];
            } else {
              vErrors.push(err5);
            }
            errors++;
          }
          if ("interior" !== data5) {
            const err6 = { instancePath: instancePath + "/cutouts/scope", schemaPath: "#/properties/cutouts/properties/scope/anyOf/1/const", keyword: "const", params: { allowedValue: "interior" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err6];
            } else {
              vErrors.push(err6);
            }
            errors++;
          }
          var _valid0 = _errs18 === errors;
          valid6 = valid6 || _valid0;
          const _errs20 = errors;
          if (data5 !== null) {
            const err7 = { instancePath: instancePath + "/cutouts/scope", schemaPath: "#/properties/cutouts/properties/scope/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err7];
            } else {
              vErrors.push(err7);
            }
            errors++;
          }
          var _valid0 = _errs20 === errors;
          valid6 = valid6 || _valid0;
          if (!valid6) {
            const err8 = { instancePath: instancePath + "/cutouts/scope", schemaPath: "#/properties/cutouts/properties/scope/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err8];
            } else {
              vErrors.push(err8);
            }
            errors++;
          } else {
            errors = _errs15;
            if (vErrors !== null) {
              if (_errs15) {
                vErrors.length = _errs15;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data3.actual_cutouts !== void 0) {
          let data6 = data3.actual_cutouts;
          const _errs23 = errors;
          let valid7 = false;
          const _errs24 = errors;
          if (typeof data6 !== "boolean") {
            const err9 = { instancePath: instancePath + "/cutouts/actual_cutouts", schemaPath: "#/properties/cutouts/properties/actual_cutouts/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err9];
            } else {
              vErrors.push(err9);
            }
            errors++;
          }
          var _valid1 = _errs24 === errors;
          valid7 = valid7 || _valid1;
          const _errs26 = errors;
          if (data6 !== null) {
            const err10 = { instancePath: instancePath + "/cutouts/actual_cutouts", schemaPath: "#/properties/cutouts/properties/actual_cutouts/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err10];
            } else {
              vErrors.push(err10);
            }
            errors++;
          }
          var _valid1 = _errs26 === errors;
          valid7 = valid7 || _valid1;
          if (!valid7) {
            const err11 = { instancePath: instancePath + "/cutouts/actual_cutouts", schemaPath: "#/properties/cutouts/properties/actual_cutouts/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err11];
            } else {
              vErrors.push(err11);
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
        if (data3.layer !== void 0) {
          let data7 = data3.layer;
          const _errs29 = errors;
          let valid8 = false;
          const _errs30 = errors;
          if (typeof data7 !== "string") {
            const err12 = { instancePath: instancePath + "/cutouts/layer", schemaPath: "#/properties/cutouts/properties/layer/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err12];
            } else {
              vErrors.push(err12);
            }
            errors++;
          }
          var _valid2 = _errs30 === errors;
          valid8 = valid8 || _valid2;
          const _errs32 = errors;
          if (data7 !== null) {
            const err13 = { instancePath: instancePath + "/cutouts/layer", schemaPath: "#/properties/cutouts/properties/layer/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err13];
            } else {
              vErrors.push(err13);
            }
            errors++;
          }
          var _valid2 = _errs32 === errors;
          valid8 = valid8 || _valid2;
          if (!valid8) {
            const err14 = { instancePath: instancePath + "/cutouts/layer", schemaPath: "#/properties/cutouts/properties/layer/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err14];
            } else {
              vErrors.push(err14);
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
        for (const key2 in data3) {
          if (key2 !== "graphics" && key2 !== "scope" && key2 !== "actual_cutouts" && key2 !== "layer") {
            const err15 = { instancePath: instancePath + "/cutouts/" + key2.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/properties/cutouts/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err15];
            } else {
              vErrors.push(err15);
            }
            errors++;
          }
        }
      } else {
        const err16 = { instancePath: instancePath + "/cutouts", schemaPath: "#/properties/cutouts/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
    }
  } else {
    const err17 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err17];
    } else {
      vErrors.push(err17);
    }
    errors++;
  }
  validate96.errors = vErrors;
  return errors === 0;
}
validate96.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.schema === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "schema" }, message: "must have required property 'schema'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.output !== void 0) {
      if (!validate22(data.output, { instancePath: instancePath + "/output", parentData: data, parentDataProperty: "output", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate22.errors : vErrors.concat(validate22.errors);
        errors = vErrors.length;
      }
    }
    if (data.libraries !== void 0) {
      let data1 = data.libraries;
      const _errs7 = errors;
      let valid3 = false;
      const _errs8 = errors;
      if (!validate28(data1, { instancePath: instancePath + "/libraries", parentData: data, parentDataProperty: "libraries", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate28.errors : vErrors.concat(validate28.errors);
        errors = vErrors.length;
      }
      var _valid0 = _errs8 === errors;
      valid3 = valid3 || _valid0;
      const _errs9 = errors;
      if (data1 !== null) {
        const err2 = { instancePath: instancePath + "/libraries", schemaPath: "#/properties/libraries/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err3 = { instancePath: instancePath + "/libraries", schemaPath: "#/properties/libraries/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
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
    if (data.known_parts !== void 0) {
      let data2 = data.known_parts;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (!validate30(data2, { instancePath: instancePath + "/known_parts", parentData: data, parentDataProperty: "known_parts", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate30.errors : vErrors.concat(validate30.errors);
        errors = vErrors.length;
      }
      var _valid1 = _errs13 === errors;
      valid4 = valid4 || _valid1;
      const _errs14 = errors;
      if (data2 !== null) {
        const err4 = { instancePath: instancePath + "/known_parts", schemaPath: "#/properties/known_parts/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid1 = _errs14 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err5 = { instancePath: instancePath + "/known_parts", schemaPath: "#/properties/known_parts/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
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
    if (data.pcb_designators !== void 0) {
      let data3 = data.pcb_designators;
      const _errs17 = errors;
      let valid5 = false;
      const _errs18 = errors;
      if (!validate32(data3, { instancePath: instancePath + "/pcb_designators", parentData: data, parentDataProperty: "pcb_designators", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate32.errors : vErrors.concat(validate32.errors);
        errors = vErrors.length;
      }
      var _valid2 = _errs18 === errors;
      valid5 = valid5 || _valid2;
      const _errs19 = errors;
      if (data3 !== null) {
        const err6 = { instancePath: instancePath + "/pcb_designators", schemaPath: "#/properties/pcb_designators/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err7 = { instancePath: instancePath + "/pcb_designators", schemaPath: "#/properties/pcb_designators/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
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
    if (data.artifacts !== void 0) {
      if (!validate36(data.artifacts, { instancePath: instancePath + "/artifacts", parentData: data, parentDataProperty: "artifacts", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate36.errors : vErrors.concat(validate36.errors);
        errors = vErrors.length;
      }
    }
    if (data.schema !== void 0) {
      let data5 = data.schema;
      if (typeof data5 !== "string") {
        const err8 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      if ("altium_cruncher.mate.config.a0" !== data5) {
        const err9 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.mate.config.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    if (data.source !== void 0) {
      let data6 = data.source;
      if (data6 && typeof data6 == "object" && !Array.isArray(data6)) {
        if (data6.board !== void 0) {
          let data7 = data6.board;
          const _errs27 = errors;
          let valid7 = false;
          const _errs28 = errors;
          if (typeof data7 !== "string") {
            const err10 = { instancePath: instancePath + "/source/board", schemaPath: "#/properties/source/properties/board/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err10];
            } else {
              vErrors.push(err10);
            }
            errors++;
          }
          var _valid3 = _errs28 === errors;
          valid7 = valid7 || _valid3;
          const _errs30 = errors;
          if (data7 !== null) {
            const err11 = { instancePath: instancePath + "/source/board", schemaPath: "#/properties/source/properties/board/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err11];
            } else {
              vErrors.push(err11);
            }
            errors++;
          }
          var _valid3 = _errs30 === errors;
          valid7 = valid7 || _valid3;
          if (!valid7) {
            const err12 = { instancePath: instancePath + "/source/board", schemaPath: "#/properties/source/properties/board/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err12];
            } else {
              vErrors.push(err12);
            }
            errors++;
          } else {
            errors = _errs27;
            if (vErrors !== null) {
              if (_errs27) {
                vErrors.length = _errs27;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data6.pcbdoc !== void 0) {
          let data8 = data6.pcbdoc;
          const _errs33 = errors;
          let valid8 = false;
          const _errs34 = errors;
          if (typeof data8 !== "string") {
            const err13 = { instancePath: instancePath + "/source/pcbdoc", schemaPath: "#/properties/source/properties/pcbdoc/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err13];
            } else {
              vErrors.push(err13);
            }
            errors++;
          }
          var _valid4 = _errs34 === errors;
          valid8 = valid8 || _valid4;
          const _errs36 = errors;
          if (data8 !== null) {
            const err14 = { instancePath: instancePath + "/source/pcbdoc", schemaPath: "#/properties/source/properties/pcbdoc/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err14];
            } else {
              vErrors.push(err14);
            }
            errors++;
          }
          var _valid4 = _errs36 === errors;
          valid8 = valid8 || _valid4;
          if (!valid8) {
            const err15 = { instancePath: instancePath + "/source/pcbdoc", schemaPath: "#/properties/source/properties/pcbdoc/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err15];
            } else {
              vErrors.push(err15);
            }
            errors++;
          } else {
            errors = _errs33;
            if (vErrors !== null) {
              if (_errs33) {
                vErrors.length = _errs33;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data6.project_context !== void 0) {
          let data9 = data6.project_context;
          const _errs39 = errors;
          let valid9 = false;
          const _errs40 = errors;
          if (typeof data9 !== "string") {
            const err16 = { instancePath: instancePath + "/source/project_context", schemaPath: "#/properties/source/properties/project_context/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err16];
            } else {
              vErrors.push(err16);
            }
            errors++;
          }
          if ("auto" !== data9) {
            const err17 = { instancePath: instancePath + "/source/project_context", schemaPath: "#/properties/source/properties/project_context/anyOf/0/const", keyword: "const", params: { allowedValue: "auto" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err17];
            } else {
              vErrors.push(err17);
            }
            errors++;
          }
          var _valid5 = _errs40 === errors;
          valid9 = valid9 || _valid5;
          const _errs42 = errors;
          if (typeof data9 !== "string") {
            const err18 = { instancePath: instancePath + "/source/project_context", schemaPath: "#/properties/source/properties/project_context/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err18];
            } else {
              vErrors.push(err18);
            }
            errors++;
          }
          if ("none" !== data9) {
            const err19 = { instancePath: instancePath + "/source/project_context", schemaPath: "#/properties/source/properties/project_context/anyOf/1/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err19];
            } else {
              vErrors.push(err19);
            }
            errors++;
          }
          var _valid5 = _errs42 === errors;
          valid9 = valid9 || _valid5;
          const _errs44 = errors;
          if (typeof data9 !== "string") {
            const err20 = { instancePath: instancePath + "/source/project_context", schemaPath: "#/properties/source/properties/project_context/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err20];
            } else {
              vErrors.push(err20);
            }
            errors++;
          }
          if ("schematic" !== data9) {
            const err21 = { instancePath: instancePath + "/source/project_context", schemaPath: "#/properties/source/properties/project_context/anyOf/2/const", keyword: "const", params: { allowedValue: "schematic" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err21];
            } else {
              vErrors.push(err21);
            }
            errors++;
          }
          var _valid5 = _errs44 === errors;
          valid9 = valid9 || _valid5;
          const _errs46 = errors;
          if (data9 !== null) {
            const err22 = { instancePath: instancePath + "/source/project_context", schemaPath: "#/properties/source/properties/project_context/anyOf/3/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err22];
            } else {
              vErrors.push(err22);
            }
            errors++;
          }
          var _valid5 = _errs46 === errors;
          valid9 = valid9 || _valid5;
          if (!valid9) {
            const err23 = { instancePath: instancePath + "/source/project_context", schemaPath: "#/properties/source/properties/project_context/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err23];
            } else {
              vErrors.push(err23);
            }
            errors++;
          } else {
            errors = _errs39;
            if (vErrors !== null) {
              if (_errs39) {
                vErrors.length = _errs39;
              } else {
                vErrors = null;
              }
            }
          }
        }
        for (const key1 in data6) {
          if (key1 !== "board" && key1 !== "pcbdoc" && key1 !== "project_context") {
            const err24 = { instancePath: instancePath + "/source/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/properties/source/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err24];
            } else {
              vErrors.push(err24);
            }
            errors++;
          }
        }
      } else {
        const err25 = { instancePath: instancePath + "/source", schemaPath: "#/properties/source/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
    }
    if (data.validation !== void 0) {
      if (!validate73(data.validation, { instancePath: instancePath + "/validation", parentData: data, parentDataProperty: "validation", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate73.errors : vErrors.concat(validate73.errors);
        errors = vErrors.length;
      }
    }
    if (data.projections !== void 0) {
      let data12 = data.projections;
      if (Array.isArray(data12)) {
        const len0 = data12.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!validate75(data12[i0], { instancePath: instancePath + "/projections/" + i0, parentData: data12, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate75.errors : vErrors.concat(validate75.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err26 = { instancePath: instancePath + "/projections", schemaPath: "#/properties/projections/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
    }
    if (data.board_projection !== void 0) {
      if (!validate96(data.board_projection, { instancePath: instancePath + "/board_projection", parentData: data, parentDataProperty: "board_projection", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate96.errors : vErrors.concat(validate96.errors);
        errors = vErrors.length;
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
  validate21.errors = vErrors;
  return errors === 0;
}
validate21.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate108(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate108.evaluated;
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
    if (data.side !== void 0) {
      let data0 = data.side;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err1 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      if ("left" !== data0) {
        const err2 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/const", keyword: "const", params: { allowedValue: "left" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid3 = valid3 || _valid0;
      const _errs9 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      if ("right" !== data0) {
        const err4 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/1/const", keyword: "const", params: { allowedValue: "right" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (typeof data0 !== "string") {
        const err5 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      if ("board_left" !== data0) {
        const err6 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/2/const", keyword: "const", params: { allowedValue: "board_left" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs11 === errors;
      valid3 = valid3 || _valid0;
      const _errs13 = errors;
      if (typeof data0 !== "string") {
        const err7 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      if ("board_right" !== data0) {
        const err8 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/3/const", keyword: "const", params: { allowedValue: "board_right" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid0 = _errs13 === errors;
      valid3 = valid3 || _valid0;
      const _errs15 = errors;
      if (data0 !== null) {
        const err9 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/4/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid0 = _errs15 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err10 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
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
    if (data.offset_mils !== void 0) {
      let data1 = data.offset_mils;
      const _errs18 = errors;
      let valid4 = false;
      const _errs19 = errors;
      if (Array.isArray(data1)) {
        if (data1.length > 2) {
          const err11 = { instancePath: instancePath + "/offset_mils", schemaPath: "#/$defs/Pair/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err11];
          } else {
            vErrors.push(err11);
          }
          errors++;
        }
        if (data1.length < 2) {
          const err12 = { instancePath: instancePath + "/offset_mils", schemaPath: "#/$defs/Pair/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err12];
          } else {
            vErrors.push(err12);
          }
          errors++;
        }
        const len0 = data1.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!(typeof data1[i0] == "number")) {
            const err13 = { instancePath: instancePath + "/offset_mils/" + i0, schemaPath: "#/$defs/Pair/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err13];
            } else {
              vErrors.push(err13);
            }
            errors++;
          }
        }
      } else {
        const err14 = { instancePath: instancePath + "/offset_mils", schemaPath: "#/$defs/Pair/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid1 = _errs19 === errors;
      valid4 = valid4 || _valid1;
      const _errs24 = errors;
      if (data1 !== null) {
        const err15 = { instancePath: instancePath + "/offset_mils", schemaPath: "#/properties/offset_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid1 = _errs24 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err16 = { instancePath: instancePath + "/offset_mils", schemaPath: "#/properties/offset_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
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
    if (data.box_size_mils !== void 0) {
      let data3 = data.box_size_mils;
      const _errs27 = errors;
      let valid8 = false;
      const _errs28 = errors;
      if (Array.isArray(data3)) {
        if (data3.length > 2) {
          const err17 = { instancePath: instancePath + "/box_size_mils", schemaPath: "#/$defs/Pair/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err17];
          } else {
            vErrors.push(err17);
          }
          errors++;
        }
        if (data3.length < 2) {
          const err18 = { instancePath: instancePath + "/box_size_mils", schemaPath: "#/$defs/Pair/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err18];
          } else {
            vErrors.push(err18);
          }
          errors++;
        }
        const len1 = data3.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (!(typeof data3[i1] == "number")) {
            const err19 = { instancePath: instancePath + "/box_size_mils/" + i1, schemaPath: "#/$defs/Pair/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err19];
            } else {
              vErrors.push(err19);
            }
            errors++;
          }
        }
      } else {
        const err20 = { instancePath: instancePath + "/box_size_mils", schemaPath: "#/$defs/Pair/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      var _valid2 = _errs28 === errors;
      valid8 = valid8 || _valid2;
      const _errs33 = errors;
      if (data3 !== null) {
        const err21 = { instancePath: instancePath + "/box_size_mils", schemaPath: "#/properties/box_size_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      var _valid2 = _errs33 === errors;
      valid8 = valid8 || _valid2;
      if (!valid8) {
        const err22 = { instancePath: instancePath + "/box_size_mils", schemaPath: "#/properties/box_size_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      } else {
        errors = _errs27;
        if (vErrors !== null) {
          if (_errs27) {
            vErrors.length = _errs27;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.center_box_on_target !== void 0) {
      let data5 = data.center_box_on_target;
      const _errs36 = errors;
      let valid12 = false;
      const _errs37 = errors;
      if (typeof data5 !== "boolean") {
        const err23 = { instancePath: instancePath + "/center_box_on_target", schemaPath: "#/properties/center_box_on_target/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      var _valid3 = _errs37 === errors;
      valid12 = valid12 || _valid3;
      const _errs39 = errors;
      if (data5 !== null) {
        const err24 = { instancePath: instancePath + "/center_box_on_target", schemaPath: "#/properties/center_box_on_target/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      var _valid3 = _errs39 === errors;
      valid12 = valid12 || _valid3;
      if (!valid12) {
        const err25 = { instancePath: instancePath + "/center_box_on_target", schemaPath: "#/properties/center_box_on_target/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      } else {
        errors = _errs36;
        if (vErrors !== null) {
          if (_errs36) {
            vErrors.length = _errs36;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.row_spacing_mils !== void 0) {
      let data6 = data.row_spacing_mils;
      const _errs42 = errors;
      let valid13 = false;
      const _errs43 = errors;
      if (!(typeof data6 == "number")) {
        const err26 = { instancePath: instancePath + "/row_spacing_mils", schemaPath: "#/properties/row_spacing_mils/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
      var _valid4 = _errs43 === errors;
      valid13 = valid13 || _valid4;
      const _errs45 = errors;
      if (data6 !== null) {
        const err27 = { instancePath: instancePath + "/row_spacing_mils", schemaPath: "#/properties/row_spacing_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
      var _valid4 = _errs45 === errors;
      valid13 = valid13 || _valid4;
      if (!valid13) {
        const err28 = { instancePath: instancePath + "/row_spacing_mils", schemaPath: "#/properties/row_spacing_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      } else {
        errors = _errs42;
        if (vErrors !== null) {
          if (_errs42) {
            vErrors.length = _errs42;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.column_spacing_mils !== void 0) {
      let data7 = data.column_spacing_mils;
      const _errs48 = errors;
      let valid14 = false;
      const _errs49 = errors;
      if (!(typeof data7 == "number")) {
        const err29 = { instancePath: instancePath + "/column_spacing_mils", schemaPath: "#/properties/column_spacing_mils/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      }
      var _valid5 = _errs49 === errors;
      valid14 = valid14 || _valid5;
      const _errs51 = errors;
      if (data7 !== null) {
        const err30 = { instancePath: instancePath + "/column_spacing_mils", schemaPath: "#/properties/column_spacing_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
        }
        errors++;
      }
      var _valid5 = _errs51 === errors;
      valid14 = valid14 || _valid5;
      if (!valid14) {
        const err31 = { instancePath: instancePath + "/column_spacing_mils", schemaPath: "#/properties/column_spacing_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      } else {
        errors = _errs48;
        if (vErrors !== null) {
          if (_errs48) {
            vErrors.length = _errs48;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.auto_width_padding_mils !== void 0) {
      let data8 = data.auto_width_padding_mils;
      const _errs54 = errors;
      let valid15 = false;
      const _errs55 = errors;
      if (!(typeof data8 == "number")) {
        const err32 = { instancePath: instancePath + "/auto_width_padding_mils", schemaPath: "#/properties/auto_width_padding_mils/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
        }
        errors++;
      }
      var _valid6 = _errs55 === errors;
      valid15 = valid15 || _valid6;
      const _errs57 = errors;
      if (data8 !== null) {
        const err33 = { instancePath: instancePath + "/auto_width_padding_mils", schemaPath: "#/properties/auto_width_padding_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
      var _valid6 = _errs57 === errors;
      valid15 = valid15 || _valid6;
      if (!valid15) {
        const err34 = { instancePath: instancePath + "/auto_width_padding_mils", schemaPath: "#/properties/auto_width_padding_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
        }
        errors++;
      } else {
        errors = _errs54;
        if (vErrors !== null) {
          if (_errs54) {
            vErrors.length = _errs54;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.enabled !== void 0) {
      let data9 = data.enabled;
      const _errs60 = errors;
      let valid16 = false;
      const _errs61 = errors;
      if (typeof data9 !== "boolean") {
        const err35 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err35];
        } else {
          vErrors.push(err35);
        }
        errors++;
      }
      var _valid7 = _errs61 === errors;
      valid16 = valid16 || _valid7;
      const _errs63 = errors;
      if (data9 !== null) {
        const err36 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err36];
        } else {
          vErrors.push(err36);
        }
        errors++;
      }
      var _valid7 = _errs63 === errors;
      valid16 = valid16 || _valid7;
      if (!valid16) {
        const err37 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err37];
        } else {
          vErrors.push(err37);
        }
        errors++;
      } else {
        errors = _errs60;
        if (vErrors !== null) {
          if (_errs60) {
            vErrors.length = _errs60;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.style !== void 0) {
      if (!validate33(data.style, { instancePath: instancePath + "/style", parentData: data, parentDataProperty: "style", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate33.errors : vErrors.concat(validate33.errors);
        errors = vErrors.length;
      }
    }
  } else {
    const err38 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err38];
    } else {
      vErrors.push(err38);
    }
    errors++;
  }
  validate108.errors = vErrors;
  return errors === 0;
}
validate108.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate113(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate113.evaluated;
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
    if (data.kind !== void 0) {
      let data0 = data.kind;
      if (typeof data0 !== "string") {
        const err1 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      if ("mate_component" !== data0) {
        const err2 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/const", keyword: "const", params: { allowedValue: "mate_component" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
    if (data.part !== void 0) {
      let data1 = data.part;
      const _errs8 = errors;
      let valid3 = false;
      const _errs9 = errors;
      if (typeof data1 !== "string") {
        const err3 = { instancePath: instancePath + "/part", schemaPath: "#/properties/part/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (data1 !== null) {
        const err4 = { instancePath: instancePath + "/part", schemaPath: "#/properties/part/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid0 = _errs11 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err5 = { instancePath: instancePath + "/part", schemaPath: "#/properties/part/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
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
    if (data.role !== void 0) {
      let data2 = data.role;
      const _errs14 = errors;
      let valid4 = false;
      const _errs15 = errors;
      if (typeof data2 !== "string") {
        const err6 = { instancePath: instancePath + "/role", schemaPath: "#/properties/role/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      valid4 = valid4 || _valid1;
      const _errs17 = errors;
      if (data2 !== null) {
        const err7 = { instancePath: instancePath + "/role", schemaPath: "#/properties/role/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid1 = _errs17 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err8 = { instancePath: instancePath + "/role", schemaPath: "#/properties/role/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      } else {
        errors = _errs14;
        if (vErrors !== null) {
          if (_errs14) {
            vErrors.length = _errs14;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.description !== void 0) {
      let data3 = data.description;
      const _errs20 = errors;
      let valid5 = false;
      const _errs21 = errors;
      if (typeof data3 !== "string") {
        const err9 = { instancePath: instancePath + "/description", schemaPath: "#/properties/description/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      const _errs23 = errors;
      if (data3 !== null) {
        const err10 = { instancePath: instancePath + "/description", schemaPath: "#/properties/description/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs23 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/description", schemaPath: "#/properties/description/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      } else {
        errors = _errs20;
        if (vErrors !== null) {
          if (_errs20) {
            vErrors.length = _errs20;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.symbol_name !== void 0) {
      let data4 = data.symbol_name;
      const _errs26 = errors;
      let valid6 = false;
      const _errs27 = errors;
      if (typeof data4 !== "string") {
        const err12 = { instancePath: instancePath + "/symbol_name", schemaPath: "#/properties/symbol_name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid3 = _errs27 === errors;
      valid6 = valid6 || _valid3;
      const _errs29 = errors;
      if (data4 !== null) {
        const err13 = { instancePath: instancePath + "/symbol_name", schemaPath: "#/properties/symbol_name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid3 = _errs29 === errors;
      valid6 = valid6 || _valid3;
      if (!valid6) {
        const err14 = { instancePath: instancePath + "/symbol_name", schemaPath: "#/properties/symbol_name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      } else {
        errors = _errs26;
        if (vErrors !== null) {
          if (_errs26) {
            vErrors.length = _errs26;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.footprint_name !== void 0) {
      let data5 = data.footprint_name;
      const _errs32 = errors;
      let valid7 = false;
      const _errs33 = errors;
      if (typeof data5 !== "string") {
        const err15 = { instancePath: instancePath + "/footprint_name", schemaPath: "#/properties/footprint_name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid4 = _errs33 === errors;
      valid7 = valid7 || _valid4;
      const _errs35 = errors;
      if (data5 !== null) {
        const err16 = { instancePath: instancePath + "/footprint_name", schemaPath: "#/properties/footprint_name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid4 = _errs35 === errors;
      valid7 = valid7 || _valid4;
      if (!valid7) {
        const err17 = { instancePath: instancePath + "/footprint_name", schemaPath: "#/properties/footprint_name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      } else {
        errors = _errs32;
        if (vErrors !== null) {
          if (_errs32) {
            vErrors.length = _errs32;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.designator_prefix !== void 0) {
      let data6 = data.designator_prefix;
      const _errs38 = errors;
      let valid8 = false;
      const _errs39 = errors;
      if (typeof data6 !== "string") {
        const err18 = { instancePath: instancePath + "/designator_prefix", schemaPath: "#/properties/designator_prefix/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
      var _valid5 = _errs39 === errors;
      valid8 = valid8 || _valid5;
      const _errs41 = errors;
      if (data6 !== null) {
        const err19 = { instancePath: instancePath + "/designator_prefix", schemaPath: "#/properties/designator_prefix/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
      var _valid5 = _errs41 === errors;
      valid8 = valid8 || _valid5;
      if (!valid8) {
        const err20 = { instancePath: instancePath + "/designator_prefix", schemaPath: "#/properties/designator_prefix/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      } else {
        errors = _errs38;
        if (vErrors !== null) {
          if (_errs38) {
            vErrors.length = _errs38;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.signal_pad_designator !== void 0) {
      let data7 = data.signal_pad_designator;
      const _errs44 = errors;
      let valid9 = false;
      const _errs45 = errors;
      if (typeof data7 !== "string") {
        const err21 = { instancePath: instancePath + "/signal_pad_designator", schemaPath: "#/properties/signal_pad_designator/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      var _valid6 = _errs45 === errors;
      valid9 = valid9 || _valid6;
      const _errs47 = errors;
      if (data7 !== null) {
        const err22 = { instancePath: instancePath + "/signal_pad_designator", schemaPath: "#/properties/signal_pad_designator/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
      var _valid6 = _errs47 === errors;
      valid9 = valid9 || _valid6;
      if (!valid9) {
        const err23 = { instancePath: instancePath + "/signal_pad_designator", schemaPath: "#/properties/signal_pad_designator/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      } else {
        errors = _errs44;
        if (vErrors !== null) {
          if (_errs44) {
            vErrors.length = _errs44;
          } else {
            vErrors = null;
          }
        }
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
  validate113.errors = vErrors;
  return errors === 0;
}
validate113.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate116(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate116.evaluated;
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
    if (data.enabled !== void 0) {
      let data0 = data.enabled;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "boolean") {
        const err1 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid3 = valid3 || _valid0;
      const _errs9 = errors;
      if (data0 !== null) {
        const err2 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err3 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
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
    if (data.layer !== void 0) {
      let data1 = data.layer;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err4 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid1 = _errs13 === errors;
      valid4 = valid4 || _valid1;
      const _errs15 = errors;
      if (data1 !== null) {
        const err5 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err6 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
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
    if (data.shape !== void 0) {
      let data2 = data.shape;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err7 = { instancePath: instancePath + "/shape", schemaPath: "#/properties/shape/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      if ("source_pad_outline" !== data2) {
        const err8 = { instancePath: instancePath + "/shape", schemaPath: "#/properties/shape/anyOf/0/const", keyword: "const", params: { allowedValue: "source_pad_outline" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/shape", schemaPath: "#/properties/shape/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      if ("destination_pad_outline" !== data2) {
        const err10 = { instancePath: instancePath + "/shape", schemaPath: "#/properties/shape/anyOf/1/const", keyword: "const", params: { allowedValue: "destination_pad_outline" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      const _errs23 = errors;
      if (data2 !== null) {
        const err11 = { instancePath: instancePath + "/shape", schemaPath: "#/properties/shape/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid2 = _errs23 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err12 = { instancePath: instancePath + "/shape", schemaPath: "#/properties/shape/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
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
    if (data.style !== void 0) {
      if (!validate86(data.style, { instancePath: instancePath + "/style", parentData: data, parentDataProperty: "style", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate86.errors : vErrors.concat(validate86.errors);
        errors = vErrors.length;
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
  validate116.errors = vErrors;
  return errors === 0;
}
validate116.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate119(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate119.evaluated;
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
    if (data.text !== void 0) {
      let data0 = data.text;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err1 = { instancePath: instancePath + "/text", schemaPath: "#/properties/text/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid3 = valid3 || _valid0;
      const _errs9 = errors;
      if (data0 !== null) {
        const err2 = { instancePath: instancePath + "/text", schemaPath: "#/properties/text/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err3 = { instancePath: instancePath + "/text", schemaPath: "#/properties/text/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
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
    if (data.style !== void 0) {
      let data1 = data.style;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err4 = { instancePath: instancePath + "/style", schemaPath: "#/properties/style/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid1 = _errs13 === errors;
      valid4 = valid4 || _valid1;
      const _errs15 = errors;
      if (data1 !== null) {
        const err5 = { instancePath: instancePath + "/style", schemaPath: "#/properties/style/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err6 = { instancePath: instancePath + "/style", schemaPath: "#/properties/style/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
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
    if (data.show_net_name !== void 0) {
      if (typeof data.show_net_name !== "boolean") {
        const err7 = { instancePath: instancePath + "/show_net_name", schemaPath: "#/properties/show_net_name/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
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
  validate119.errors = vErrors;
  return errors === 0;
}
validate119.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate121(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate121.evaluated;
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
    if (data.x_mils !== void 0) {
      if (!(typeof data.x_mils == "number")) {
        const err1 = { instancePath: instancePath + "/x_mils", schemaPath: "#/properties/x_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
    }
    if (data.y_mils !== void 0) {
      if (!(typeof data.y_mils == "number")) {
        const err2 = { instancePath: instancePath + "/y_mils", schemaPath: "#/properties/y_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
    if (data.width_mils !== void 0) {
      if (!(typeof data.width_mils == "number")) {
        const err3 = { instancePath: instancePath + "/width_mils", schemaPath: "#/properties/width_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.height_mils !== void 0) {
      if (!(typeof data.height_mils == "number")) {
        const err4 = { instancePath: instancePath + "/height_mils", schemaPath: "#/properties/height_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.shape !== void 0) {
      let data4 = data.shape;
      if (!(typeof data4 == "number" && (!(data4 % 1) && !isNaN(data4)))) {
        const err5 = { instancePath: instancePath + "/shape", schemaPath: "#/properties/shape/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.layer !== void 0) {
      let data5 = data.layer;
      if (!(typeof data5 == "number" && (!(data5 % 1) && !isNaN(data5)))) {
        const err6 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.rotation_degrees !== void 0) {
      if (!(typeof data.rotation_degrees == "number")) {
        const err7 = { instancePath: instancePath + "/rotation_degrees", schemaPath: "#/properties/rotation_degrees/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.corner_radius_mils !== void 0) {
      if (!(typeof data.corner_radius_mils == "number")) {
        const err8 = { instancePath: instancePath + "/corner_radius_mils", schemaPath: "#/properties/corner_radius_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
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
  validate121.errors = vErrors;
  return errors === 0;
}
validate121.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate112(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate112.evaluated;
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
    if (data.mate_projection_id !== void 0) {
      let data0 = data.mate_projection_id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err1 = { instancePath: instancePath + "/mate_projection_id", schemaPath: "#/properties/mate_projection_id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid3 = valid3 || _valid0;
      const _errs9 = errors;
      if (data0 !== null) {
        const err2 = { instancePath: instancePath + "/mate_projection_id", schemaPath: "#/properties/mate_projection_id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err3 = { instancePath: instancePath + "/mate_projection_id", schemaPath: "#/properties/mate_projection_id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
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
    if (data.mate_part_role !== void 0) {
      let data1 = data.mate_part_role;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err4 = { instancePath: instancePath + "/mate_part_role", schemaPath: "#/properties/mate_part_role/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid1 = _errs13 === errors;
      valid4 = valid4 || _valid1;
      const _errs15 = errors;
      if (data1 !== null) {
        const err5 = { instancePath: instancePath + "/mate_part_role", schemaPath: "#/properties/mate_part_role/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err6 = { instancePath: instancePath + "/mate_part_role", schemaPath: "#/properties/mate_part_role/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
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
    if (data.mate_component !== void 0) {
      let data2 = data.mate_component;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (!validate113(data2, { instancePath: instancePath + "/mate_component", parentData: data, parentDataProperty: "mate_component", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate113.errors : vErrors.concat(validate113.errors);
        errors = vErrors.length;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs20 = errors;
      if (data2 !== null) {
        const err7 = { instancePath: instancePath + "/mate_component", schemaPath: "#/properties/mate_component/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid2 = _errs20 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err8 = { instancePath: instancePath + "/mate_component", schemaPath: "#/properties/mate_component/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
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
    if (data.mate_pcb_label !== void 0) {
      let data3 = data.mate_pcb_label;
      const _errs23 = errors;
      let valid6 = false;
      const _errs24 = errors;
      if (!validate108(data3, { instancePath: instancePath + "/mate_pcb_label", parentData: data, parentDataProperty: "mate_pcb_label", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate108.errors : vErrors.concat(validate108.errors);
        errors = vErrors.length;
      }
      var _valid3 = _errs24 === errors;
      valid6 = valid6 || _valid3;
      const _errs25 = errors;
      if (data3 !== null) {
        const err9 = { instancePath: instancePath + "/mate_pcb_label", schemaPath: "#/properties/mate_pcb_label/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid3 = _errs25 === errors;
      valid6 = valid6 || _valid3;
      if (!valid6) {
        const err10 = { instancePath: instancePath + "/mate_pcb_label", schemaPath: "#/properties/mate_pcb_label/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
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
    if (data.mate_reference_graphics !== void 0) {
      let data4 = data.mate_reference_graphics;
      const _errs28 = errors;
      let valid7 = false;
      const _errs29 = errors;
      if (!validate116(data4, { instancePath: instancePath + "/mate_reference_graphics", parentData: data, parentDataProperty: "mate_reference_graphics", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate116.errors : vErrors.concat(validate116.errors);
        errors = vErrors.length;
      }
      var _valid4 = _errs29 === errors;
      valid7 = valid7 || _valid4;
      const _errs30 = errors;
      if (data4 !== null) {
        const err11 = { instancePath: instancePath + "/mate_reference_graphics", schemaPath: "#/properties/mate_reference_graphics/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid4 = _errs30 === errors;
      valid7 = valid7 || _valid4;
      if (!valid7) {
        const err12 = { instancePath: instancePath + "/mate_reference_graphics", schemaPath: "#/properties/mate_reference_graphics/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      } else {
        errors = _errs28;
        if (vErrors !== null) {
          if (_errs28) {
            vErrors.length = _errs28;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.source_power_port !== void 0) {
      let data5 = data.source_power_port;
      const _errs33 = errors;
      let valid8 = false;
      const _errs34 = errors;
      if (!validate119(data5, { instancePath: instancePath + "/source_power_port", parentData: data, parentDataProperty: "source_power_port", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate119.errors : vErrors.concat(validate119.errors);
        errors = vErrors.length;
      }
      var _valid5 = _errs34 === errors;
      valid8 = valid8 || _valid5;
      const _errs35 = errors;
      if (data5 !== null) {
        const err13 = { instancePath: instancePath + "/source_power_port", schemaPath: "#/properties/source_power_port/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid5 = _errs35 === errors;
      valid8 = valid8 || _valid5;
      if (!valid8) {
        const err14 = { instancePath: instancePath + "/source_power_port", schemaPath: "#/properties/source_power_port/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      } else {
        errors = _errs33;
        if (vErrors !== null) {
          if (_errs33) {
            vErrors.length = _errs33;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.source_pad_geometries !== void 0) {
      let data6 = data.source_pad_geometries;
      const _errs38 = errors;
      let valid9 = false;
      const _errs39 = errors;
      if (Array.isArray(data6)) {
        const len0 = data6.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!validate121(data6[i0], { instancePath: instancePath + "/source_pad_geometries/" + i0, parentData: data6, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate121.errors : vErrors.concat(validate121.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err15 = { instancePath: instancePath + "/source_pad_geometries", schemaPath: "#/properties/source_pad_geometries/anyOf/0/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid6 = _errs39 === errors;
      valid9 = valid9 || _valid6;
      const _errs42 = errors;
      if (data6 !== null) {
        const err16 = { instancePath: instancePath + "/source_pad_geometries", schemaPath: "#/properties/source_pad_geometries/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid6 = _errs42 === errors;
      valid9 = valid9 || _valid6;
      if (!valid9) {
        const err17 = { instancePath: instancePath + "/source_pad_geometries", schemaPath: "#/properties/source_pad_geometries/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      } else {
        errors = _errs38;
        if (vErrors !== null) {
          if (_errs38) {
            vErrors.length = _errs38;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.designator !== void 0) {
      if (typeof data.designator !== "string") {
        const err18 = { instancePath: instancePath + "/designator", schemaPath: "#/properties/designator/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
    }
    if (data.kind !== void 0) {
      if (typeof data.kind !== "string") {
        const err19 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
    }
    if (data.layer !== void 0) {
      if (typeof data.layer !== "string") {
        const err20 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
    }
    if (data.footprint !== void 0) {
      if (typeof data.footprint !== "string") {
        const err21 = { instancePath: instancePath + "/footprint", schemaPath: "#/properties/footprint/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
    }
    if (data.x_mils !== void 0) {
      if (!(typeof data.x_mils == "number")) {
        const err22 = { instancePath: instancePath + "/x_mils", schemaPath: "#/properties/x_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
    }
    if (data.y_mils !== void 0) {
      if (!(typeof data.y_mils == "number")) {
        const err23 = { instancePath: instancePath + "/y_mils", schemaPath: "#/properties/y_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
    }
    if (data.net_name !== void 0) {
      let data14 = data.net_name;
      const _errs57 = errors;
      let valid12 = false;
      const _errs58 = errors;
      if (typeof data14 !== "string") {
        const err24 = { instancePath: instancePath + "/net_name", schemaPath: "#/properties/net_name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      var _valid7 = _errs58 === errors;
      valid12 = valid12 || _valid7;
      const _errs60 = errors;
      if (data14 !== null) {
        const err25 = { instancePath: instancePath + "/net_name", schemaPath: "#/properties/net_name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
      var _valid7 = _errs60 === errors;
      valid12 = valid12 || _valid7;
      if (!valid12) {
        const err26 = { instancePath: instancePath + "/net_name", schemaPath: "#/properties/net_name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      } else {
        errors = _errs57;
        if (vErrors !== null) {
          if (_errs57) {
            vErrors.length = _errs57;
          } else {
            vErrors = null;
          }
        }
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
  validate112.errors = vErrors;
  return errors === 0;
}
validate112.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate124(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate124.evaluated;
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
    if (data.mate_projection_id !== void 0) {
      let data0 = data.mate_projection_id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err1 = { instancePath: instancePath + "/mate_projection_id", schemaPath: "#/properties/mate_projection_id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid3 = valid3 || _valid0;
      const _errs9 = errors;
      if (data0 !== null) {
        const err2 = { instancePath: instancePath + "/mate_projection_id", schemaPath: "#/properties/mate_projection_id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err3 = { instancePath: instancePath + "/mate_projection_id", schemaPath: "#/properties/mate_projection_id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
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
    if (data.mate_part_role !== void 0) {
      let data1 = data.mate_part_role;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err4 = { instancePath: instancePath + "/mate_part_role", schemaPath: "#/properties/mate_part_role/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid1 = _errs13 === errors;
      valid4 = valid4 || _valid1;
      const _errs15 = errors;
      if (data1 !== null) {
        const err5 = { instancePath: instancePath + "/mate_part_role", schemaPath: "#/properties/mate_part_role/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err6 = { instancePath: instancePath + "/mate_part_role", schemaPath: "#/properties/mate_part_role/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
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
    if (data.mate_component !== void 0) {
      let data2 = data.mate_component;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (!validate113(data2, { instancePath: instancePath + "/mate_component", parentData: data, parentDataProperty: "mate_component", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate113.errors : vErrors.concat(validate113.errors);
        errors = vErrors.length;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs20 = errors;
      if (data2 !== null) {
        const err7 = { instancePath: instancePath + "/mate_component", schemaPath: "#/properties/mate_component/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid2 = _errs20 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err8 = { instancePath: instancePath + "/mate_component", schemaPath: "#/properties/mate_component/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
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
    if (data.mate_pcb_label !== void 0) {
      let data3 = data.mate_pcb_label;
      const _errs23 = errors;
      let valid6 = false;
      const _errs24 = errors;
      if (!validate108(data3, { instancePath: instancePath + "/mate_pcb_label", parentData: data, parentDataProperty: "mate_pcb_label", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate108.errors : vErrors.concat(validate108.errors);
        errors = vErrors.length;
      }
      var _valid3 = _errs24 === errors;
      valid6 = valid6 || _valid3;
      const _errs25 = errors;
      if (data3 !== null) {
        const err9 = { instancePath: instancePath + "/mate_pcb_label", schemaPath: "#/properties/mate_pcb_label/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid3 = _errs25 === errors;
      valid6 = valid6 || _valid3;
      if (!valid6) {
        const err10 = { instancePath: instancePath + "/mate_pcb_label", schemaPath: "#/properties/mate_pcb_label/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
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
    if (data.mate_reference_graphics !== void 0) {
      let data4 = data.mate_reference_graphics;
      const _errs28 = errors;
      let valid7 = false;
      const _errs29 = errors;
      if (!validate116(data4, { instancePath: instancePath + "/mate_reference_graphics", parentData: data, parentDataProperty: "mate_reference_graphics", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate116.errors : vErrors.concat(validate116.errors);
        errors = vErrors.length;
      }
      var _valid4 = _errs29 === errors;
      valid7 = valid7 || _valid4;
      const _errs30 = errors;
      if (data4 !== null) {
        const err11 = { instancePath: instancePath + "/mate_reference_graphics", schemaPath: "#/properties/mate_reference_graphics/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid4 = _errs30 === errors;
      valid7 = valid7 || _valid4;
      if (!valid7) {
        const err12 = { instancePath: instancePath + "/mate_reference_graphics", schemaPath: "#/properties/mate_reference_graphics/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      } else {
        errors = _errs28;
        if (vErrors !== null) {
          if (_errs28) {
            vErrors.length = _errs28;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.source_power_port !== void 0) {
      let data5 = data.source_power_port;
      const _errs33 = errors;
      let valid8 = false;
      const _errs34 = errors;
      if (!validate119(data5, { instancePath: instancePath + "/source_power_port", parentData: data, parentDataProperty: "source_power_port", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate119.errors : vErrors.concat(validate119.errors);
        errors = vErrors.length;
      }
      var _valid5 = _errs34 === errors;
      valid8 = valid8 || _valid5;
      const _errs35 = errors;
      if (data5 !== null) {
        const err13 = { instancePath: instancePath + "/source_power_port", schemaPath: "#/properties/source_power_port/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid5 = _errs35 === errors;
      valid8 = valid8 || _valid5;
      if (!valid8) {
        const err14 = { instancePath: instancePath + "/source_power_port", schemaPath: "#/properties/source_power_port/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      } else {
        errors = _errs33;
        if (vErrors !== null) {
          if (_errs33) {
            vErrors.length = _errs33;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.source_pad_geometries !== void 0) {
      let data6 = data.source_pad_geometries;
      const _errs38 = errors;
      let valid9 = false;
      const _errs39 = errors;
      if (Array.isArray(data6)) {
        const len0 = data6.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!validate121(data6[i0], { instancePath: instancePath + "/source_pad_geometries/" + i0, parentData: data6, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate121.errors : vErrors.concat(validate121.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err15 = { instancePath: instancePath + "/source_pad_geometries", schemaPath: "#/properties/source_pad_geometries/anyOf/0/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid6 = _errs39 === errors;
      valid9 = valid9 || _valid6;
      const _errs42 = errors;
      if (data6 !== null) {
        const err16 = { instancePath: instancePath + "/source_pad_geometries", schemaPath: "#/properties/source_pad_geometries/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid6 = _errs42 === errors;
      valid9 = valid9 || _valid6;
      if (!valid9) {
        const err17 = { instancePath: instancePath + "/source_pad_geometries", schemaPath: "#/properties/source_pad_geometries/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      } else {
        errors = _errs38;
        if (vErrors !== null) {
          if (_errs38) {
            vErrors.length = _errs38;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.designator !== void 0) {
      if (typeof data.designator !== "string") {
        const err18 = { instancePath: instancePath + "/designator", schemaPath: "#/properties/designator/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
    }
    if (data.kind !== void 0) {
      if (typeof data.kind !== "string") {
        const err19 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
    }
    if (data.x_mils !== void 0) {
      if (!(typeof data.x_mils == "number")) {
        const err20 = { instancePath: instancePath + "/x_mils", schemaPath: "#/properties/x_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
    }
    if (data.y_mils !== void 0) {
      if (!(typeof data.y_mils == "number")) {
        const err21 = { instancePath: instancePath + "/y_mils", schemaPath: "#/properties/y_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
    }
    if (data.net_name !== void 0) {
      let data12 = data.net_name;
      const _errs53 = errors;
      let valid12 = false;
      const _errs54 = errors;
      if (typeof data12 !== "string") {
        const err22 = { instancePath: instancePath + "/net_name", schemaPath: "#/properties/net_name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
      var _valid7 = _errs54 === errors;
      valid12 = valid12 || _valid7;
      const _errs56 = errors;
      if (data12 !== null) {
        const err23 = { instancePath: instancePath + "/net_name", schemaPath: "#/properties/net_name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      var _valid7 = _errs56 === errors;
      valid12 = valid12 || _valid7;
      if (!valid12) {
        const err24 = { instancePath: instancePath + "/net_name", schemaPath: "#/properties/net_name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      } else {
        errors = _errs53;
        if (vErrors !== null) {
          if (_errs53) {
            vErrors.length = _errs53;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.width_mils !== void 0) {
      if (!(typeof data.width_mils == "number")) {
        const err25 = { instancePath: instancePath + "/width_mils", schemaPath: "#/properties/width_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
    }
    if (data.height_mils !== void 0) {
      if (!(typeof data.height_mils == "number")) {
        const err26 = { instancePath: instancePath + "/height_mils", schemaPath: "#/properties/height_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
    }
    if (data.hole_size_mils !== void 0) {
      if (!(typeof data.hole_size_mils == "number")) {
        const err27 = { instancePath: instancePath + "/hole_size_mils", schemaPath: "#/properties/hole_size_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
    }
    if (data.shape !== void 0) {
      let data16 = data.shape;
      if (!(typeof data16 == "number" && (!(data16 % 1) && !isNaN(data16)))) {
        const err28 = { instancePath: instancePath + "/shape", schemaPath: "#/properties/shape/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
    }
    if (data.layer !== void 0) {
      let data17 = data.layer;
      if (!(typeof data17 == "number" && (!(data17 % 1) && !isNaN(data17)))) {
        const err29 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      }
    }
    if (data.rotation_degrees !== void 0) {
      if (!(typeof data.rotation_degrees == "number")) {
        const err30 = { instancePath: instancePath + "/rotation_degrees", schemaPath: "#/properties/rotation_degrees/type", keyword: "type", params: { type: "number" }, message: "must be number" };
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
  validate124.errors = vErrors;
  return errors === 0;
}
validate124.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate132(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate132.evaluated;
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
    if (data.x_mils === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "x_mils" }, message: "must have required property 'x_mils'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.y_mils === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "y_mils" }, message: "must have required property 'y_mils'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.x_mils !== void 0) {
      if (!(typeof data.x_mils == "number")) {
        const err3 = { instancePath: instancePath + "/x_mils", schemaPath: "#/properties/x_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.y_mils !== void 0) {
      if (!(typeof data.y_mils == "number")) {
        const err4 = { instancePath: instancePath + "/y_mils", schemaPath: "#/properties/y_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.segment !== void 0) {
      let data2 = data.segment;
      const _errs10 = errors;
      let valid3 = false;
      const _errs11 = errors;
      if (typeof data2 !== "string") {
        const err5 = { instancePath: instancePath + "/segment", schemaPath: "#/properties/segment/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      if ("line" !== data2) {
        const err6 = { instancePath: instancePath + "/segment", schemaPath: "#/properties/segment/anyOf/0/const", keyword: "const", params: { allowedValue: "line" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs11 === errors;
      valid3 = valid3 || _valid0;
      const _errs13 = errors;
      if (typeof data2 !== "string") {
        const err7 = { instancePath: instancePath + "/segment", schemaPath: "#/properties/segment/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      if ("arc" !== data2) {
        const err8 = { instancePath: instancePath + "/segment", schemaPath: "#/properties/segment/anyOf/1/const", keyword: "const", params: { allowedValue: "arc" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid0 = _errs13 === errors;
      valid3 = valid3 || _valid0;
      const _errs15 = errors;
      if (data2 !== null) {
        const err9 = { instancePath: instancePath + "/segment", schemaPath: "#/properties/segment/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid0 = _errs15 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err10 = { instancePath: instancePath + "/segment", schemaPath: "#/properties/segment/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      } else {
        errors = _errs10;
        if (vErrors !== null) {
          if (_errs10) {
            vErrors.length = _errs10;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.center_mils !== void 0) {
      let data3 = data.center_mils;
      if (Array.isArray(data3)) {
        if (data3.length > 2) {
          const err11 = { instancePath: instancePath + "/center_mils", schemaPath: "#/$defs/Pair/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err11];
          } else {
            vErrors.push(err11);
          }
          errors++;
        }
        if (data3.length < 2) {
          const err12 = { instancePath: instancePath + "/center_mils", schemaPath: "#/$defs/Pair/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err12];
          } else {
            vErrors.push(err12);
          }
          errors++;
        }
        const len0 = data3.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!(typeof data3[i0] == "number")) {
            const err13 = { instancePath: instancePath + "/center_mils/" + i0, schemaPath: "#/$defs/Pair/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err13];
            } else {
              vErrors.push(err13);
            }
            errors++;
          }
        }
      } else {
        const err14 = { instancePath: instancePath + "/center_mils", schemaPath: "#/$defs/Pair/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
    }
    if (data.radius_mils !== void 0) {
      if (!(typeof data.radius_mils == "number")) {
        const err15 = { instancePath: instancePath + "/radius_mils", schemaPath: "#/properties/radius_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
    }
    if (data.start_angle_degrees !== void 0) {
      if (!(typeof data.start_angle_degrees == "number")) {
        const err16 = { instancePath: instancePath + "/start_angle_degrees", schemaPath: "#/properties/start_angle_degrees/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
    }
    if (data.end_angle_degrees !== void 0) {
      if (!(typeof data.end_angle_degrees == "number")) {
        const err17 = { instancePath: instancePath + "/end_angle_degrees", schemaPath: "#/properties/end_angle_degrees/type", keyword: "type", params: { type: "number" }, message: "must be number" };
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
  validate132.errors = vErrors;
  return errors === 0;
}
validate132.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
var wrapper0 = { validate: validate131 };
function validate131(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate131.evaluated;
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
    if (data.vertices === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "vertices" }, message: "must have required property 'vertices'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.vertices !== void 0) {
      let data0 = data.vertices;
      if (Array.isArray(data0)) {
        const len0 = data0.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!validate132(data0[i0], { instancePath: instancePath + "/vertices/" + i0, parentData: data0, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate132.errors : vErrors.concat(validate132.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err2 = { instancePath: instancePath + "/vertices", schemaPath: "#/properties/vertices/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
    if (data.closed !== void 0) {
      if (typeof data.closed !== "boolean") {
        const err3 = { instancePath: instancePath + "/closed", schemaPath: "#/properties/closed/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.cutouts !== void 0) {
      let data3 = data.cutouts;
      const _errs11 = errors;
      let valid5 = false;
      const _errs12 = errors;
      if (Array.isArray(data3)) {
        const len1 = data3.length;
        for (let i1 = 0; i1 < len1; i1++) {
          let data4 = data3[i1];
          const _errs15 = errors;
          let valid8 = false;
          const _errs16 = errors;
          if (!wrapper0.validate(data4, { instancePath: instancePath + "/cutouts/" + i1, parentData: data3, parentDataProperty: i1, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? wrapper0.validate.errors : vErrors.concat(wrapper0.validate.errors);
            errors = vErrors.length;
          } else {
            var items0 = wrapper0.validate.evaluated.items;
          }
          var _valid1 = _errs16 === errors;
          valid8 = valid8 || _valid1;
          const _errs17 = errors;
          if (Array.isArray(data4)) {
            const len2 = data4.length;
            for (let i2 = 0; i2 < len2; i2++) {
              if (!validate132(data4[i2], { instancePath: instancePath + "/cutouts/" + i1 + "/" + i2, parentData: data4, parentDataProperty: i2, rootData, dynamicAnchors })) {
                vErrors = vErrors === null ? validate132.errors : vErrors.concat(validate132.errors);
                errors = vErrors.length;
              }
            }
          } else {
            const err4 = { instancePath: instancePath + "/cutouts/" + i1, schemaPath: "#/properties/cutouts/anyOf/0/items/anyOf/1/type", keyword: "type", params: { type: "array" }, message: "must be array" };
            if (vErrors === null) {
              vErrors = [err4];
            } else {
              vErrors.push(err4);
            }
            errors++;
          }
          var _valid1 = _errs17 === errors;
          valid8 = valid8 || _valid1;
          if (_valid1) {
            if (items0 !== true) {
              items0 = true;
            }
          }
          if (!valid8) {
            const err5 = { instancePath: instancePath + "/cutouts/" + i1, schemaPath: "#/properties/cutouts/anyOf/0/items/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err5];
            } else {
              vErrors.push(err5);
            }
            errors++;
          } else {
            errors = _errs15;
            if (vErrors !== null) {
              if (_errs15) {
                vErrors.length = _errs15;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err6 = { instancePath: instancePath + "/cutouts", schemaPath: "#/properties/cutouts/anyOf/0/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs12 === errors;
      valid5 = valid5 || _valid0;
      const _errs20 = errors;
      if (data3 !== null) {
        const err7 = { instancePath: instancePath + "/cutouts", schemaPath: "#/properties/cutouts/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid0 = _errs20 === errors;
      valid5 = valid5 || _valid0;
      if (!valid5) {
        const err8 = { instancePath: instancePath + "/cutouts", schemaPath: "#/properties/cutouts/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
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
  } else {
    const err9 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err9];
    } else {
      vErrors.push(err9);
    }
    errors++;
  }
  validate131.errors = vErrors;
  return errors === 0;
}
validate131.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate111(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate111.evaluated;
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
    if (data.board_key !== void 0) {
      if (typeof data.board_key !== "string") {
        const err1 = { instancePath: instancePath + "/board_key", schemaPath: "#/properties/board_key/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
    }
    if (data.pcb_path !== void 0) {
      if (typeof data.pcb_path !== "string") {
        const err2 = { instancePath: instancePath + "/pcb_path", schemaPath: "#/properties/pcb_path/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
    if (data.components !== void 0) {
      let data2 = data.components;
      if (Array.isArray(data2)) {
        const len0 = data2.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!validate112(data2[i0], { instancePath: instancePath + "/components/" + i0, parentData: data2, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate112.errors : vErrors.concat(validate112.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err3 = { instancePath: instancePath + "/components", schemaPath: "#/properties/components/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.free_pads !== void 0) {
      let data4 = data.free_pads;
      if (Array.isArray(data4)) {
        const len1 = data4.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (!validate124(data4[i1], { instancePath: instancePath + "/free_pads/" + i1, parentData: data4, parentDataProperty: i1, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate124.errors : vErrors.concat(validate124.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err4 = { instancePath: instancePath + "/free_pads", schemaPath: "#/properties/free_pads/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.board_outline_mils !== void 0) {
      let data6 = data.board_outline_mils;
      const _errs16 = errors;
      let valid7 = false;
      const _errs17 = errors;
      if (data6 && typeof data6 == "object" && !Array.isArray(data6)) {
        if (data6.left === void 0) {
          const err5 = { instancePath: instancePath + "/board_outline_mils", schemaPath: "#/$defs/Bounds/required", keyword: "required", params: { missingProperty: "left" }, message: "must have required property 'left'" };
          if (vErrors === null) {
            vErrors = [err5];
          } else {
            vErrors.push(err5);
          }
          errors++;
        }
        if (data6.bottom === void 0) {
          const err6 = { instancePath: instancePath + "/board_outline_mils", schemaPath: "#/$defs/Bounds/required", keyword: "required", params: { missingProperty: "bottom" }, message: "must have required property 'bottom'" };
          if (vErrors === null) {
            vErrors = [err6];
          } else {
            vErrors.push(err6);
          }
          errors++;
        }
        if (data6.right === void 0) {
          const err7 = { instancePath: instancePath + "/board_outline_mils", schemaPath: "#/$defs/Bounds/required", keyword: "required", params: { missingProperty: "right" }, message: "must have required property 'right'" };
          if (vErrors === null) {
            vErrors = [err7];
          } else {
            vErrors.push(err7);
          }
          errors++;
        }
        if (data6.top === void 0) {
          const err8 = { instancePath: instancePath + "/board_outline_mils", schemaPath: "#/$defs/Bounds/required", keyword: "required", params: { missingProperty: "top" }, message: "must have required property 'top'" };
          if (vErrors === null) {
            vErrors = [err8];
          } else {
            vErrors.push(err8);
          }
          errors++;
        }
        if (data6.left !== void 0) {
          if (!(typeof data6.left == "number")) {
            const err9 = { instancePath: instancePath + "/board_outline_mils/left", schemaPath: "#/$defs/Bounds/properties/left/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err9];
            } else {
              vErrors.push(err9);
            }
            errors++;
          }
        }
        if (data6.bottom !== void 0) {
          if (!(typeof data6.bottom == "number")) {
            const err10 = { instancePath: instancePath + "/board_outline_mils/bottom", schemaPath: "#/$defs/Bounds/properties/bottom/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err10];
            } else {
              vErrors.push(err10);
            }
            errors++;
          }
        }
        if (data6.right !== void 0) {
          if (!(typeof data6.right == "number")) {
            const err11 = { instancePath: instancePath + "/board_outline_mils/right", schemaPath: "#/$defs/Bounds/properties/right/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err11];
            } else {
              vErrors.push(err11);
            }
            errors++;
          }
        }
        if (data6.top !== void 0) {
          if (!(typeof data6.top == "number")) {
            const err12 = { instancePath: instancePath + "/board_outline_mils/top", schemaPath: "#/$defs/Bounds/properties/top/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err12];
            } else {
              vErrors.push(err12);
            }
            errors++;
          }
        }
        for (const key1 in data6) {
          if (key1 !== "left" && key1 !== "bottom" && key1 !== "right" && key1 !== "top") {
            const err13 = { instancePath: instancePath + "/board_outline_mils/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/Bounds/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err13];
            } else {
              vErrors.push(err13);
            }
            errors++;
          }
        }
      } else {
        const err14 = { instancePath: instancePath + "/board_outline_mils", schemaPath: "#/$defs/Bounds/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid0 = _errs17 === errors;
      valid7 = valid7 || _valid0;
      const _errs31 = errors;
      if (data6 !== null) {
        const err15 = { instancePath: instancePath + "/board_outline_mils", schemaPath: "#/properties/board_outline_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid0 = _errs31 === errors;
      valid7 = valid7 || _valid0;
      if (!valid7) {
        const err16 = { instancePath: instancePath + "/board_outline_mils", schemaPath: "#/properties/board_outline_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
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
    if (data.board_outline !== void 0) {
      let data12 = data.board_outline;
      const _errs34 = errors;
      let valid11 = false;
      const _errs35 = errors;
      if (!validate131(data12, { instancePath: instancePath + "/board_outline", parentData: data, parentDataProperty: "board_outline", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate131.errors : vErrors.concat(validate131.errors);
        errors = vErrors.length;
      }
      var _valid1 = _errs35 === errors;
      valid11 = valid11 || _valid1;
      const _errs36 = errors;
      if (data12 !== null) {
        const err17 = { instancePath: instancePath + "/board_outline", schemaPath: "#/properties/board_outline/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      var _valid1 = _errs36 === errors;
      valid11 = valid11 || _valid1;
      if (!valid11) {
        const err18 = { instancePath: instancePath + "/board_outline", schemaPath: "#/properties/board_outline/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
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
  } else {
    const err19 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err19];
    } else {
      vErrors.push(err19);
    }
    errors++;
  }
  validate111.errors = vErrors;
  return errors === 0;
}
validate111.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate102(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate102.evaluated;
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
    if (data.output !== void 0) {
      if (!validate22(data.output, { instancePath: instancePath + "/output", parentData: data, parentDataProperty: "output", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate22.errors : vErrors.concat(validate22.errors);
        errors = vErrors.length;
      }
    }
    if (data.libraries !== void 0) {
      let data1 = data.libraries;
      const _errs7 = errors;
      let valid3 = false;
      const _errs8 = errors;
      if (!validate28(data1, { instancePath: instancePath + "/libraries", parentData: data, parentDataProperty: "libraries", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate28.errors : vErrors.concat(validate28.errors);
        errors = vErrors.length;
      }
      var _valid0 = _errs8 === errors;
      valid3 = valid3 || _valid0;
      const _errs9 = errors;
      if (data1 !== null) {
        const err1 = { instancePath: instancePath + "/libraries", schemaPath: "#/properties/libraries/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err2 = { instancePath: instancePath + "/libraries", schemaPath: "#/properties/libraries/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
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
    if (data.known_parts !== void 0) {
      let data2 = data.known_parts;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (!validate30(data2, { instancePath: instancePath + "/known_parts", parentData: data, parentDataProperty: "known_parts", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate30.errors : vErrors.concat(validate30.errors);
        errors = vErrors.length;
      }
      var _valid1 = _errs13 === errors;
      valid4 = valid4 || _valid1;
      const _errs14 = errors;
      if (data2 !== null) {
        const err3 = { instancePath: instancePath + "/known_parts", schemaPath: "#/properties/known_parts/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      var _valid1 = _errs14 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err4 = { instancePath: instancePath + "/known_parts", schemaPath: "#/properties/known_parts/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
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
    if (data.pcb_designators !== void 0) {
      let data3 = data.pcb_designators;
      const _errs17 = errors;
      let valid5 = false;
      const _errs18 = errors;
      if (!validate32(data3, { instancePath: instancePath + "/pcb_designators", parentData: data, parentDataProperty: "pcb_designators", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate32.errors : vErrors.concat(validate32.errors);
        errors = vErrors.length;
      }
      var _valid2 = _errs18 === errors;
      valid5 = valid5 || _valid2;
      const _errs19 = errors;
      if (data3 !== null) {
        const err5 = { instancePath: instancePath + "/pcb_designators", schemaPath: "#/properties/pcb_designators/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err6 = { instancePath: instancePath + "/pcb_designators", schemaPath: "#/properties/pcb_designators/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
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
    if (data.artifacts !== void 0) {
      if (!validate36(data.artifacts, { instancePath: instancePath + "/artifacts", parentData: data, parentDataProperty: "artifacts", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate36.errors : vErrors.concat(validate36.errors);
        errors = vErrors.length;
      }
    }
    if (data.schema !== void 0) {
      let data5 = data.schema;
      const _errs23 = errors;
      let valid6 = false;
      const _errs24 = errors;
      if (typeof data5 !== "string") {
        const err7 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      if ("altium_cruncher.mate.legacy.a0" !== data5) {
        const err8 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf/0/const", keyword: "const", params: { allowedValue: "altium_cruncher.mate.legacy.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid3 = _errs24 === errors;
      valid6 = valid6 || _valid3;
      const _errs26 = errors;
      if (data5 !== null) {
        const err9 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid3 = _errs26 === errors;
      valid6 = valid6 || _valid3;
      if (!valid6) {
        const err10 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
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
    if (data.source !== void 0) {
      let data6 = data.source;
      if (data6 && typeof data6 == "object" && !Array.isArray(data6)) {
        if (data6.dut !== void 0) {
          let data7 = data6.dut;
          const _errs31 = errors;
          let valid8 = false;
          const _errs32 = errors;
          if (typeof data7 !== "string") {
            const err11 = { instancePath: instancePath + "/source/dut", schemaPath: "#/properties/source/properties/dut/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err11];
            } else {
              vErrors.push(err11);
            }
            errors++;
          }
          var _valid4 = _errs32 === errors;
          valid8 = valid8 || _valid4;
          const _errs34 = errors;
          if (data7 !== null) {
            const err12 = { instancePath: instancePath + "/source/dut", schemaPath: "#/properties/source/properties/dut/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err12];
            } else {
              vErrors.push(err12);
            }
            errors++;
          }
          var _valid4 = _errs34 === errors;
          valid8 = valid8 || _valid4;
          if (!valid8) {
            const err13 = { instancePath: instancePath + "/source/dut", schemaPath: "#/properties/source/properties/dut/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err13];
            } else {
              vErrors.push(err13);
            }
            errors++;
          } else {
            errors = _errs31;
            if (vErrors !== null) {
              if (_errs31) {
                vErrors.length = _errs31;
              } else {
                vErrors = null;
              }
            }
          }
        }
        for (const key1 in data6) {
          if (key1 !== "dut") {
            const err14 = { instancePath: instancePath + "/source/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/properties/source/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err14];
            } else {
              vErrors.push(err14);
            }
            errors++;
          }
        }
      } else {
        const err15 = { instancePath: instancePath + "/source", schemaPath: "#/properties/source/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
    }
    if (data.marker !== void 0) {
      let data9 = data.marker;
      if (data9 && typeof data9 == "object" && !Array.isArray(data9)) {
        if (data9.enabled !== void 0) {
          let data10 = data9.enabled;
          const _errs42 = errors;
          let valid11 = false;
          const _errs43 = errors;
          if (typeof data10 !== "boolean") {
            const err16 = { instancePath: instancePath + "/marker/enabled", schemaPath: "#/properties/marker/properties/enabled/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err16];
            } else {
              vErrors.push(err16);
            }
            errors++;
          }
          var _valid5 = _errs43 === errors;
          valid11 = valid11 || _valid5;
          const _errs45 = errors;
          if (data10 !== null) {
            const err17 = { instancePath: instancePath + "/marker/enabled", schemaPath: "#/properties/marker/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err17];
            } else {
              vErrors.push(err17);
            }
            errors++;
          }
          var _valid5 = _errs45 === errors;
          valid11 = valid11 || _valid5;
          if (!valid11) {
            const err18 = { instancePath: instancePath + "/marker/enabled", schemaPath: "#/properties/marker/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err18];
            } else {
              vErrors.push(err18);
            }
            errors++;
          } else {
            errors = _errs42;
            if (vErrors !== null) {
              if (_errs42) {
                vErrors.length = _errs42;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data9.text !== void 0) {
          let data11 = data9.text;
          const _errs48 = errors;
          let valid12 = false;
          const _errs49 = errors;
          if (typeof data11 !== "string") {
            const err19 = { instancePath: instancePath + "/marker/text", schemaPath: "#/properties/marker/properties/text/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err19];
            } else {
              vErrors.push(err19);
            }
            errors++;
          }
          var _valid6 = _errs49 === errors;
          valid12 = valid12 || _valid6;
          const _errs51 = errors;
          if (data11 !== null) {
            const err20 = { instancePath: instancePath + "/marker/text", schemaPath: "#/properties/marker/properties/text/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err20];
            } else {
              vErrors.push(err20);
            }
            errors++;
          }
          var _valid6 = _errs51 === errors;
          valid12 = valid12 || _valid6;
          if (!valid12) {
            const err21 = { instancePath: instancePath + "/marker/text", schemaPath: "#/properties/marker/properties/text/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err21];
            } else {
              vErrors.push(err21);
            }
            errors++;
          } else {
            errors = _errs48;
            if (vErrors !== null) {
              if (_errs48) {
                vErrors.length = _errs48;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data9.position_mils !== void 0) {
          let data12 = data9.position_mils;
          const _errs54 = errors;
          let valid13 = false;
          const _errs55 = errors;
          if (Array.isArray(data12)) {
            if (data12.length > 2) {
              const err22 = { instancePath: instancePath + "/marker/position_mils", schemaPath: "#/$defs/Pair/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
              if (vErrors === null) {
                vErrors = [err22];
              } else {
                vErrors.push(err22);
              }
              errors++;
            }
            if (data12.length < 2) {
              const err23 = { instancePath: instancePath + "/marker/position_mils", schemaPath: "#/$defs/Pair/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
              if (vErrors === null) {
                vErrors = [err23];
              } else {
                vErrors.push(err23);
              }
              errors++;
            }
            const len0 = data12.length;
            for (let i0 = 0; i0 < len0; i0++) {
              if (!(typeof data12[i0] == "number")) {
                const err24 = { instancePath: instancePath + "/marker/position_mils/" + i0, schemaPath: "#/$defs/Pair/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
                if (vErrors === null) {
                  vErrors = [err24];
                } else {
                  vErrors.push(err24);
                }
                errors++;
              }
            }
          } else {
            const err25 = { instancePath: instancePath + "/marker/position_mils", schemaPath: "#/$defs/Pair/type", keyword: "type", params: { type: "array" }, message: "must be array" };
            if (vErrors === null) {
              vErrors = [err25];
            } else {
              vErrors.push(err25);
            }
            errors++;
          }
          var _valid7 = _errs55 === errors;
          valid13 = valid13 || _valid7;
          const _errs60 = errors;
          if (data12 !== null) {
            const err26 = { instancePath: instancePath + "/marker/position_mils", schemaPath: "#/properties/marker/properties/position_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err26];
            } else {
              vErrors.push(err26);
            }
            errors++;
          }
          var _valid7 = _errs60 === errors;
          valid13 = valid13 || _valid7;
          if (!valid13) {
            const err27 = { instancePath: instancePath + "/marker/position_mils", schemaPath: "#/properties/marker/properties/position_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err27];
            } else {
              vErrors.push(err27);
            }
            errors++;
          } else {
            errors = _errs54;
            if (vErrors !== null) {
              if (_errs54) {
                vErrors.length = _errs54;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data9.height_mils !== void 0) {
          let data14 = data9.height_mils;
          const _errs63 = errors;
          let valid17 = false;
          const _errs64 = errors;
          if (!(typeof data14 == "number")) {
            const err28 = { instancePath: instancePath + "/marker/height_mils", schemaPath: "#/properties/marker/properties/height_mils/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err28];
            } else {
              vErrors.push(err28);
            }
            errors++;
          }
          var _valid8 = _errs64 === errors;
          valid17 = valid17 || _valid8;
          const _errs66 = errors;
          if (data14 !== null) {
            const err29 = { instancePath: instancePath + "/marker/height_mils", schemaPath: "#/properties/marker/properties/height_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err29];
            } else {
              vErrors.push(err29);
            }
            errors++;
          }
          var _valid8 = _errs66 === errors;
          valid17 = valid17 || _valid8;
          if (!valid17) {
            const err30 = { instancePath: instancePath + "/marker/height_mils", schemaPath: "#/properties/marker/properties/height_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err30];
            } else {
              vErrors.push(err30);
            }
            errors++;
          } else {
            errors = _errs63;
            if (vErrors !== null) {
              if (_errs63) {
                vErrors.length = _errs63;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data9.layer !== void 0) {
          let data15 = data9.layer;
          const _errs69 = errors;
          let valid18 = false;
          const _errs70 = errors;
          if (typeof data15 !== "string") {
            const err31 = { instancePath: instancePath + "/marker/layer", schemaPath: "#/properties/marker/properties/layer/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err31];
            } else {
              vErrors.push(err31);
            }
            errors++;
          }
          var _valid9 = _errs70 === errors;
          valid18 = valid18 || _valid9;
          const _errs72 = errors;
          if (data15 !== null) {
            const err32 = { instancePath: instancePath + "/marker/layer", schemaPath: "#/properties/marker/properties/layer/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err32];
            } else {
              vErrors.push(err32);
            }
            errors++;
          }
          var _valid9 = _errs72 === errors;
          valid18 = valid18 || _valid9;
          if (!valid18) {
            const err33 = { instancePath: instancePath + "/marker/layer", schemaPath: "#/properties/marker/properties/layer/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err33];
            } else {
              vErrors.push(err33);
            }
            errors++;
          } else {
            errors = _errs69;
            if (vErrors !== null) {
              if (_errs69) {
                vErrors.length = _errs69;
              } else {
                vErrors = null;
              }
            }
          }
        }
        for (const key2 in data9) {
          if (key2 !== "enabled" && key2 !== "text" && key2 !== "position_mils" && key2 !== "height_mils" && key2 !== "layer") {
            const err34 = { instancePath: instancePath + "/marker/" + key2.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/properties/marker/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err34];
            } else {
              vErrors.push(err34);
            }
            errors++;
          }
        }
      } else {
        const err35 = { instancePath: instancePath + "/marker", schemaPath: "#/properties/marker/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err35];
        } else {
          vErrors.push(err35);
        }
        errors++;
      }
    }
    if (data.placement !== void 0) {
      let data17 = data.placement;
      if (data17 && typeof data17 == "object" && !Array.isArray(data17)) {
        if (data17.source_mount_side !== void 0) {
          let data18 = data17.source_mount_side;
          const _errs80 = errors;
          let valid21 = false;
          const _errs81 = errors;
          if (typeof data18 !== "string") {
            const err36 = { instancePath: instancePath + "/placement/source_mount_side", schemaPath: "#/properties/placement/properties/source_mount_side/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err36];
            } else {
              vErrors.push(err36);
            }
            errors++;
          }
          var _valid10 = _errs81 === errors;
          valid21 = valid21 || _valid10;
          const _errs83 = errors;
          if (data18 !== null) {
            const err37 = { instancePath: instancePath + "/placement/source_mount_side", schemaPath: "#/properties/placement/properties/source_mount_side/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err37];
            } else {
              vErrors.push(err37);
            }
            errors++;
          }
          var _valid10 = _errs83 === errors;
          valid21 = valid21 || _valid10;
          if (!valid21) {
            const err38 = { instancePath: instancePath + "/placement/source_mount_side", schemaPath: "#/properties/placement/properties/source_mount_side/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err38];
            } else {
              vErrors.push(err38);
            }
            errors++;
          } else {
            errors = _errs80;
            if (vErrors !== null) {
              if (_errs80) {
                vErrors.length = _errs80;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data17.offset_mils !== void 0) {
          let data19 = data17.offset_mils;
          const _errs86 = errors;
          let valid22 = false;
          const _errs87 = errors;
          if (Array.isArray(data19)) {
            if (data19.length > 2) {
              const err39 = { instancePath: instancePath + "/placement/offset_mils", schemaPath: "#/$defs/Pair/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
              if (vErrors === null) {
                vErrors = [err39];
              } else {
                vErrors.push(err39);
              }
              errors++;
            }
            if (data19.length < 2) {
              const err40 = { instancePath: instancePath + "/placement/offset_mils", schemaPath: "#/$defs/Pair/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
              if (vErrors === null) {
                vErrors = [err40];
              } else {
                vErrors.push(err40);
              }
              errors++;
            }
            const len1 = data19.length;
            for (let i1 = 0; i1 < len1; i1++) {
              if (!(typeof data19[i1] == "number")) {
                const err41 = { instancePath: instancePath + "/placement/offset_mils/" + i1, schemaPath: "#/$defs/Pair/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
                if (vErrors === null) {
                  vErrors = [err41];
                } else {
                  vErrors.push(err41);
                }
                errors++;
              }
            }
          } else {
            const err42 = { instancePath: instancePath + "/placement/offset_mils", schemaPath: "#/$defs/Pair/type", keyword: "type", params: { type: "array" }, message: "must be array" };
            if (vErrors === null) {
              vErrors = [err42];
            } else {
              vErrors.push(err42);
            }
            errors++;
          }
          var _valid11 = _errs87 === errors;
          valid22 = valid22 || _valid11;
          const _errs92 = errors;
          if (data19 !== null) {
            const err43 = { instancePath: instancePath + "/placement/offset_mils", schemaPath: "#/properties/placement/properties/offset_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err43];
            } else {
              vErrors.push(err43);
            }
            errors++;
          }
          var _valid11 = _errs92 === errors;
          valid22 = valid22 || _valid11;
          if (!valid22) {
            const err44 = { instancePath: instancePath + "/placement/offset_mils", schemaPath: "#/properties/placement/properties/offset_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err44];
            } else {
              vErrors.push(err44);
            }
            errors++;
          } else {
            errors = _errs86;
            if (vErrors !== null) {
              if (_errs86) {
                vErrors.length = _errs86;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data17.mirror_x !== void 0) {
          let data21 = data17.mirror_x;
          const _errs95 = errors;
          let valid26 = false;
          const _errs96 = errors;
          if (typeof data21 !== "boolean") {
            const err45 = { instancePath: instancePath + "/placement/mirror_x", schemaPath: "#/properties/placement/properties/mirror_x/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err45];
            } else {
              vErrors.push(err45);
            }
            errors++;
          }
          var _valid12 = _errs96 === errors;
          valid26 = valid26 || _valid12;
          const _errs98 = errors;
          if (data21 !== null) {
            const err46 = { instancePath: instancePath + "/placement/mirror_x", schemaPath: "#/properties/placement/properties/mirror_x/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err46];
            } else {
              vErrors.push(err46);
            }
            errors++;
          }
          var _valid12 = _errs98 === errors;
          valid26 = valid26 || _valid12;
          if (!valid26) {
            const err47 = { instancePath: instancePath + "/placement/mirror_x", schemaPath: "#/properties/placement/properties/mirror_x/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err47];
            } else {
              vErrors.push(err47);
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
        if (data17.mirror_y !== void 0) {
          let data22 = data17.mirror_y;
          const _errs101 = errors;
          let valid27 = false;
          const _errs102 = errors;
          if (typeof data22 !== "boolean") {
            const err48 = { instancePath: instancePath + "/placement/mirror_y", schemaPath: "#/properties/placement/properties/mirror_y/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err48];
            } else {
              vErrors.push(err48);
            }
            errors++;
          }
          var _valid13 = _errs102 === errors;
          valid27 = valid27 || _valid13;
          const _errs104 = errors;
          if (data22 !== null) {
            const err49 = { instancePath: instancePath + "/placement/mirror_y", schemaPath: "#/properties/placement/properties/mirror_y/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err49];
            } else {
              vErrors.push(err49);
            }
            errors++;
          }
          var _valid13 = _errs104 === errors;
          valid27 = valid27 || _valid13;
          if (!valid27) {
            const err50 = { instancePath: instancePath + "/placement/mirror_y", schemaPath: "#/properties/placement/properties/mirror_y/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err50];
            } else {
              vErrors.push(err50);
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
        if (data17.mirror_origin_mils !== void 0) {
          let data23 = data17.mirror_origin_mils;
          const _errs107 = errors;
          let valid28 = false;
          const _errs108 = errors;
          if (Array.isArray(data23)) {
            if (data23.length > 2) {
              const err51 = { instancePath: instancePath + "/placement/mirror_origin_mils", schemaPath: "#/$defs/Pair/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
              if (vErrors === null) {
                vErrors = [err51];
              } else {
                vErrors.push(err51);
              }
              errors++;
            }
            if (data23.length < 2) {
              const err52 = { instancePath: instancePath + "/placement/mirror_origin_mils", schemaPath: "#/$defs/Pair/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
              if (vErrors === null) {
                vErrors = [err52];
              } else {
                vErrors.push(err52);
              }
              errors++;
            }
            const len2 = data23.length;
            for (let i2 = 0; i2 < len2; i2++) {
              if (!(typeof data23[i2] == "number")) {
                const err53 = { instancePath: instancePath + "/placement/mirror_origin_mils/" + i2, schemaPath: "#/$defs/Pair/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
                if (vErrors === null) {
                  vErrors = [err53];
                } else {
                  vErrors.push(err53);
                }
                errors++;
              }
            }
          } else {
            const err54 = { instancePath: instancePath + "/placement/mirror_origin_mils", schemaPath: "#/$defs/Pair/type", keyword: "type", params: { type: "array" }, message: "must be array" };
            if (vErrors === null) {
              vErrors = [err54];
            } else {
              vErrors.push(err54);
            }
            errors++;
          }
          var _valid14 = _errs108 === errors;
          valid28 = valid28 || _valid14;
          const _errs113 = errors;
          if (data23 !== null) {
            const err55 = { instancePath: instancePath + "/placement/mirror_origin_mils", schemaPath: "#/properties/placement/properties/mirror_origin_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err55];
            } else {
              vErrors.push(err55);
            }
            errors++;
          }
          var _valid14 = _errs113 === errors;
          valid28 = valid28 || _valid14;
          if (!valid28) {
            const err56 = { instancePath: instancePath + "/placement/mirror_origin_mils", schemaPath: "#/properties/placement/properties/mirror_origin_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err56];
            } else {
              vErrors.push(err56);
            }
            errors++;
          } else {
            errors = _errs107;
            if (vErrors !== null) {
              if (_errs107) {
                vErrors.length = _errs107;
              } else {
                vErrors = null;
              }
            }
          }
        }
        for (const key3 in data17) {
          if (key3 !== "source_mount_side" && key3 !== "offset_mils" && key3 !== "mirror_x" && key3 !== "mirror_y" && key3 !== "mirror_origin_mils") {
            const err57 = { instancePath: instancePath + "/placement/" + key3.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/properties/placement/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err57];
            } else {
              vErrors.push(err57);
            }
            errors++;
          }
        }
      } else {
        const err58 = { instancePath: instancePath + "/placement", schemaPath: "#/properties/placement/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err58];
        } else {
          vErrors.push(err58);
        }
        errors++;
      }
    }
    if (data.pcb_labels !== void 0) {
      let data26 = data.pcb_labels;
      const _errs119 = errors;
      let valid33 = false;
      const _errs120 = errors;
      if (!validate108(data26, { instancePath: instancePath + "/pcb_labels", parentData: data, parentDataProperty: "pcb_labels", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate108.errors : vErrors.concat(validate108.errors);
        errors = vErrors.length;
      }
      var _valid15 = _errs120 === errors;
      valid33 = valid33 || _valid15;
      const _errs121 = errors;
      if (data26 !== null) {
        const err59 = { instancePath: instancePath + "/pcb_labels", schemaPath: "#/properties/pcb_labels/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err59];
        } else {
          vErrors.push(err59);
        }
        errors++;
      }
      var _valid15 = _errs121 === errors;
      valid33 = valid33 || _valid15;
      if (!valid33) {
        const err60 = { instancePath: instancePath + "/pcb_labels", schemaPath: "#/properties/pcb_labels/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err60];
        } else {
          vErrors.push(err60);
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
    if (data.selection !== void 0) {
      let data27 = data.selection;
      if (data27 && typeof data27 == "object" && !Array.isArray(data27)) {
        if (data27.boards !== void 0) {
          let data28 = data27.boards;
          if (Array.isArray(data28)) {
            const len3 = data28.length;
            for (let i3 = 0; i3 < len3; i3++) {
              if (!validate111(data28[i3], { instancePath: instancePath + "/selection/boards/" + i3, parentData: data28, parentDataProperty: i3, rootData, dynamicAnchors })) {
                vErrors = vErrors === null ? validate111.errors : vErrors.concat(validate111.errors);
                errors = vErrors.length;
              }
            }
          } else {
            const err61 = { instancePath: instancePath + "/selection/boards", schemaPath: "#/properties/selection/properties/boards/type", keyword: "type", params: { type: "array" }, message: "must be array" };
            if (vErrors === null) {
              vErrors = [err61];
            } else {
              vErrors.push(err61);
            }
            errors++;
          }
        }
        for (const key4 in data27) {
          if (key4 !== "boards") {
            const err62 = { instancePath: instancePath + "/selection/" + key4.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/properties/selection/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err62];
            } else {
              vErrors.push(err62);
            }
            errors++;
          }
        }
      } else {
        const err63 = { instancePath: instancePath + "/selection", schemaPath: "#/properties/selection/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err63];
        } else {
          vErrors.push(err63);
        }
        errors++;
      }
    }
    if (data.board_projection !== void 0) {
      let data31 = data.board_projection;
      const _errs132 = errors;
      let valid38 = false;
      const _errs133 = errors;
      if (!validate96(data31, { instancePath: instancePath + "/board_projection", parentData: data, parentDataProperty: "board_projection", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate96.errors : vErrors.concat(validate96.errors);
        errors = vErrors.length;
      }
      var _valid16 = _errs133 === errors;
      valid38 = valid38 || _valid16;
      const _errs134 = errors;
      if (data31 !== null) {
        const err64 = { instancePath: instancePath + "/board_projection", schemaPath: "#/properties/board_projection/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err64];
        } else {
          vErrors.push(err64);
        }
        errors++;
      }
      var _valid16 = _errs134 === errors;
      valid38 = valid38 || _valid16;
      if (!valid38) {
        const err65 = { instancePath: instancePath + "/board_projection", schemaPath: "#/properties/board_projection/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err65];
        } else {
          vErrors.push(err65);
        }
        errors++;
      } else {
        errors = _errs132;
        if (vErrors !== null) {
          if (_errs132) {
            vErrors.length = _errs132;
          } else {
            vErrors = null;
          }
        }
      }
    }
  } else {
    const err66 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err66];
    } else {
      vErrors.push(err66);
    }
    errors++;
  }
  validate102.errors = vErrors;
  return errors === 0;
}
validate102.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
  const _errs1 = errors;
  let valid0 = false;
  const _errs2 = errors;
  if (!validate21(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs2 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    var props0 = true;
  }
  const _errs3 = errors;
  if (!validate102(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate102.errors : vErrors.concat(validate102.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs3 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  if (!valid0) {
    const err0 = { instancePath, schemaPath: "#/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
    if (vErrors === null) {
      vErrors = [err0];
    } else {
      vErrors.push(err0);
    }
    errors++;
  } else {
    errors = _errs1;
    if (vErrors !== null) {
      if (_errs1) {
        vErrors.length = _errs1;
      } else {
        vErrors = null;
      }
    }
  }
  validate20.errors = vErrors;
  evaluated0.props = props0;
  return errors === 0;
}
validate20.evaluated = { "dynamicProps": true, "dynamicItems": false };
export {
  validate_default as default,
  validate
};
