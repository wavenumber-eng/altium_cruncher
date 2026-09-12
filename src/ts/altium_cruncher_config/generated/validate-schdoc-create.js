// Generated from src/tsp/altium_cruncher/config/creation.tsp. Do not edit.
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
var func1 = require_ucs2length().default;
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
    if (data.width === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "width" }, message: "must have required property 'width'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.height === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "height" }, message: "must have required property 'height'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.width !== void 0) {
      let data0 = data.width;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (!(typeof data0 == "number")) {
        const err3 = { instancePath: instancePath + "/width", schemaPath: "#/properties/width/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid3 = valid3 || _valid0;
      const _errs9 = errors;
      if (typeof data0 !== "boolean") {
        const err4 = { instancePath: instancePath + "/width", schemaPath: "#/properties/width/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err5 = { instancePath: instancePath + "/width", schemaPath: "#/properties/width/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.height !== void 0) {
      let data1 = data.height;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (!(typeof data1 == "number")) {
        const err6 = { instancePath: instancePath + "/height", schemaPath: "#/properties/height/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid1 = _errs13 === errors;
      valid4 = valid4 || _valid1;
      const _errs15 = errors;
      if (typeof data1 !== "boolean") {
        const err7 = { instancePath: instancePath + "/height", schemaPath: "#/properties/height/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err8 = { instancePath: instancePath + "/height", schemaPath: "#/properties/height/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
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
    if (data.schema === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "schema" }, message: "must have required property 'schema'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.file === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.schema !== void 0) {
      let data0 = data.schema;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      if ("altium_cruncher.schdoc.create.config.a0" !== data0) {
        const err4 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.schdoc.create.config.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.file !== void 0) {
      let data1 = data.file;
      if (typeof data1 === "string") {
        if (func1(data1) < 1) {
          const err5 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/NonemptyString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err5];
          } else {
            vErrors.push(err5);
          }
          errors++;
        }
      } else {
        const err6 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/NonemptyString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.sheet_style !== void 0) {
      let data2 = data.sheet_style;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data2 !== "string") {
        const err7 = { instancePath: instancePath + "/sheet_style", schemaPath: "#/properties/sheet_style/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid0 = _errs13 === errors;
      valid4 = valid4 || _valid0;
      const _errs15 = errors;
      if (!(typeof data2 == "number" && (!(data2 % 1) && !isNaN(data2)))) {
        const err8 = { instancePath: instancePath + "/sheet_style", schemaPath: "#/properties/sheet_style/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid0 = _errs15 === errors;
      valid4 = valid4 || _valid0;
      const _errs17 = errors;
      if (typeof data2 !== "boolean") {
        const err9 = { instancePath: instancePath + "/sheet_style", schemaPath: "#/properties/sheet_style/anyOf/2/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid0 = _errs17 === errors;
      valid4 = valid4 || _valid0;
      const _errs19 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/sheet_style", schemaPath: "#/properties/sheet_style/anyOf/3/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid0 = _errs19 === errors;
      valid4 = valid4 || _valid0;
      if (!valid4) {
        const err11 = { instancePath: instancePath + "/sheet_style", schemaPath: "#/properties/sheet_style/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
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
    if (data.template !== void 0) {
      let data3 = data.template;
      const _errs22 = errors;
      let valid5 = false;
      const _errs23 = errors;
      if (typeof data3 === "string") {
        if (func1(data3) < 1) {
          const err12 = { instancePath: instancePath + "/template", schemaPath: "#/$defs/NonemptyString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err12];
          } else {
            vErrors.push(err12);
          }
          errors++;
        }
      } else {
        const err13 = { instancePath: instancePath + "/template", schemaPath: "#/$defs/NonemptyString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid1 = _errs23 === errors;
      valid5 = valid5 || _valid1;
      const _errs26 = errors;
      if (data3 !== null) {
        const err14 = { instancePath: instancePath + "/template", schemaPath: "#/properties/template/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid1 = _errs26 === errors;
      valid5 = valid5 || _valid1;
      if (!valid5) {
        const err15 = { instancePath: instancePath + "/template", schemaPath: "#/properties/template/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.apply_template_visual_sheet_settings !== void 0) {
      let data4 = data.apply_template_visual_sheet_settings;
      const _errs29 = errors;
      let valid7 = false;
      const _errs30 = errors;
      if (typeof data4 !== "boolean") {
        const err16 = { instancePath: instancePath + "/apply_template_visual_sheet_settings", schemaPath: "#/properties/apply_template_visual_sheet_settings/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid2 = _errs30 === errors;
      valid7 = valid7 || _valid2;
      const _errs32 = errors;
      if (typeof data4 !== "string") {
        const err17 = { instancePath: instancePath + "/apply_template_visual_sheet_settings", schemaPath: "#/properties/apply_template_visual_sheet_settings/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      var _valid2 = _errs32 === errors;
      valid7 = valid7 || _valid2;
      const _errs34 = errors;
      if (!(typeof data4 == "number")) {
        const err18 = { instancePath: instancePath + "/apply_template_visual_sheet_settings", schemaPath: "#/properties/apply_template_visual_sheet_settings/anyOf/2/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
      var _valid2 = _errs34 === errors;
      valid7 = valid7 || _valid2;
      const _errs36 = errors;
      if (data4 !== null) {
        const err19 = { instancePath: instancePath + "/apply_template_visual_sheet_settings", schemaPath: "#/properties/apply_template_visual_sheet_settings/anyOf/3/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
      var _valid2 = _errs36 === errors;
      valid7 = valid7 || _valid2;
      const _errs38 = errors;
      if (!Array.isArray(data4)) {
        const err20 = { instancePath: instancePath + "/apply_template_visual_sheet_settings", schemaPath: "#/properties/apply_template_visual_sheet_settings/anyOf/4/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      var _valid2 = _errs38 === errors;
      valid7 = valid7 || _valid2;
      const _errs40 = errors;
      if (data4 && typeof data4 == "object" && !Array.isArray(data4)) {
      } else {
        const err21 = { instancePath: instancePath + "/apply_template_visual_sheet_settings", schemaPath: "#/$defs/RecordUnknown/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      var _valid2 = _errs40 === errors;
      valid7 = valid7 || _valid2;
      if (!valid7) {
        const err22 = { instancePath: instancePath + "/apply_template_visual_sheet_settings", schemaPath: "#/properties/apply_template_visual_sheet_settings/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
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
    if (data.custom_sheet_mils !== void 0) {
      let data5 = data.custom_sheet_mils;
      const _errs45 = errors;
      let valid9 = false;
      const _errs46 = errors;
      if (!validate21(data5, { instancePath: instancePath + "/custom_sheet_mils", parentData: data, parentDataProperty: "custom_sheet_mils", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
        errors = vErrors.length;
      }
      var _valid3 = _errs46 === errors;
      valid9 = valid9 || _valid3;
      const _errs47 = errors;
      if (data5 !== null) {
        const err23 = { instancePath: instancePath + "/custom_sheet_mils", schemaPath: "#/properties/custom_sheet_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      var _valid3 = _errs47 === errors;
      valid9 = valid9 || _valid3;
      if (!valid9) {
        const err24 = { instancePath: instancePath + "/custom_sheet_mils", schemaPath: "#/properties/custom_sheet_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
  } else {
    const err25 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err25];
    } else {
      vErrors.push(err25);
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
