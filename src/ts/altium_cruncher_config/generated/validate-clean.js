// Generated from src/tsp/altium_cruncher/config/clean-config.tsp. Do not edit.
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
    if (data.font_name !== void 0) {
      let data0 = data.font_name;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err0 = { instancePath: instancePath + "/font_name", schemaPath: "#/properties/font_name/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err0];
          } else {
            vErrors.push(err0);
          }
          errors++;
        }
      } else {
        const err1 = { instancePath: instancePath + "/font_name", schemaPath: "#/properties/font_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
    }
    if (data.font !== void 0) {
      let data1 = data.font;
      if (typeof data1 === "string") {
        if (func1(data1) < 1) {
          const err2 = { instancePath: instancePath + "/font", schemaPath: "#/properties/font/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err2];
          } else {
            vErrors.push(err2);
          }
          errors++;
        }
      } else {
        const err3 = { instancePath: instancePath + "/font", schemaPath: "#/properties/font/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.size_pt !== void 0) {
      let data2 = data.size_pt;
      if (!(typeof data2 == "number" && (!(data2 % 1) && !isNaN(data2)))) {
        const err4 = { instancePath: instancePath + "/size_pt", schemaPath: "#/properties/size_pt/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      if (typeof data2 == "number") {
        if (data2 < 1 || isNaN(data2)) {
          const err5 = { instancePath: instancePath + "/size_pt", schemaPath: "#/properties/size_pt/minimum", keyword: "minimum", params: { comparison: ">=", limit: 1 }, message: "must be >= 1" };
          if (vErrors === null) {
            vErrors = [err5];
          } else {
            vErrors.push(err5);
          }
          errors++;
        }
      }
    }
    if (data.size !== void 0) {
      let data3 = data.size;
      if (!(typeof data3 == "number" && (!(data3 % 1) && !isNaN(data3)))) {
        const err6 = { instancePath: instancePath + "/size", schemaPath: "#/properties/size/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      if (typeof data3 == "number") {
        if (data3 < 1 || isNaN(data3)) {
          const err7 = { instancePath: instancePath + "/size", schemaPath: "#/properties/size/minimum", keyword: "minimum", params: { comparison: ">=", limit: 1 }, message: "must be >= 1" };
          if (vErrors === null) {
            vErrors = [err7];
          } else {
            vErrors.push(err7);
          }
          errors++;
        }
      }
    }
    if (data.bold !== void 0) {
      if (typeof data.bold !== "boolean") {
        const err8 = { instancePath: instancePath + "/bold", schemaPath: "#/properties/bold/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
    if (data.italic !== void 0) {
      if (typeof data.italic !== "boolean") {
        const err9 = { instancePath: instancePath + "/italic", schemaPath: "#/properties/italic/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    if (data.color_win32 !== void 0) {
      let data6 = data.color_win32;
      const _errs15 = errors;
      let valid2 = false;
      let passing0 = null;
      const _errs16 = errors;
      if (!(typeof data6 == "number" && (!(data6 % 1) && !isNaN(data6)))) {
        const err10 = { instancePath: instancePath + "/color_win32", schemaPath: "#/$defs/ColorValue/oneOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid0 = _errs16 === errors;
      if (_valid0) {
        valid2 = true;
        passing0 = 0;
      }
      const _errs18 = errors;
      if (typeof data6 !== "string") {
        const err11 = { instancePath: instancePath + "/color_win32", schemaPath: "#/$defs/ColorValue/oneOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid0 = _errs18 === errors;
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
        const err12 = { instancePath: instancePath + "/color_win32", schemaPath: "#/$defs/ColorValue/oneOf", keyword: "oneOf", params: { passingSchemas: passing0 }, message: "must match exactly one schema in oneOf" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
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
    if (data.color !== void 0) {
      let data7 = data.color;
      const _errs22 = errors;
      let valid4 = false;
      let passing1 = null;
      const _errs23 = errors;
      if (!(typeof data7 == "number" && (!(data7 % 1) && !isNaN(data7)))) {
        const err13 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/ColorValue/oneOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid1 = _errs23 === errors;
      if (_valid1) {
        valid4 = true;
        passing1 = 0;
      }
      const _errs25 = errors;
      if (typeof data7 !== "string") {
        const err14 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/ColorValue/oneOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid1 = _errs25 === errors;
      if (_valid1 && valid4) {
        valid4 = false;
        passing1 = [passing1, 1];
      } else {
        if (_valid1) {
          valid4 = true;
          passing1 = 1;
        }
      }
      if (!valid4) {
        const err15 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/ColorValue/oneOf", keyword: "oneOf", params: { passingSchemas: passing1 }, message: "must match exactly one schema in oneOf" };
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
    for (const key0 in data) {
      if (key0 !== "font_name" && key0 !== "font" && key0 !== "size_pt" && key0 !== "size" && key0 !== "bold" && key0 !== "italic" && key0 !== "color_win32" && key0 !== "color") {
        const err16 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
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
    if (data.name_font !== void 0) {
      if (!validate23(data.name_font, { instancePath: instancePath + "/name_font", parentData: data, parentDataProperty: "name_font", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate23.errors : vErrors.concat(validate23.errors);
        errors = vErrors.length;
      }
    }
    if (data.name !== void 0) {
      if (!validate23(data.name, { instancePath: instancePath + "/name", parentData: data, parentDataProperty: "name", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate23.errors : vErrors.concat(validate23.errors);
        errors = vErrors.length;
      }
    }
    if (data.designator_font !== void 0) {
      if (!validate23(data.designator_font, { instancePath: instancePath + "/designator_font", parentData: data, parentDataProperty: "designator_font", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate23.errors : vErrors.concat(validate23.errors);
        errors = vErrors.length;
      }
    }
    if (data.designator !== void 0) {
      if (!validate23(data.designator, { instancePath: instancePath + "/designator", parentData: data, parentDataProperty: "designator", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate23.errors : vErrors.concat(validate23.errors);
        errors = vErrors.length;
      }
    }
    for (const key0 in data) {
      if (key0 !== "enabled" && key0 !== "name_font" && key0 !== "name" && key0 !== "designator_font" && key0 !== "designator") {
        const err1 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
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
  validate22.errors = vErrors;
  return errors === 0;
}
validate22.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate29(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate29.evaluated;
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
    if (data.min_width_mils !== void 0) {
      let data1 = data.min_width_mils;
      if (typeof data1 == "number") {
        if (data1 < 0 || isNaN(data1)) {
          const err1 = { instancePath: instancePath + "/min_width_mils", schemaPath: "#/properties/min_width_mils/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err1];
          } else {
            vErrors.push(err1);
          }
          errors++;
        }
      } else {
        const err2 = { instancePath: instancePath + "/min_width_mils", schemaPath: "#/properties/min_width_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
    if (data.min_height_mils !== void 0) {
      let data2 = data.min_height_mils;
      if (typeof data2 == "number") {
        if (data2 < 0 || isNaN(data2)) {
          const err3 = { instancePath: instancePath + "/min_height_mils", schemaPath: "#/properties/min_height_mils/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/min_height_mils", schemaPath: "#/properties/min_height_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.outline_color_win32 !== void 0) {
      let data3 = data.outline_color_win32;
      const _errs9 = errors;
      let valid2 = false;
      let passing0 = null;
      const _errs10 = errors;
      if (!(typeof data3 == "number" && (!(data3 % 1) && !isNaN(data3)))) {
        const err5 = { instancePath: instancePath + "/outline_color_win32", schemaPath: "#/$defs/ColorValue/oneOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      if (_valid0) {
        valid2 = true;
        passing0 = 0;
      }
      const _errs12 = errors;
      if (typeof data3 !== "string") {
        const err6 = { instancePath: instancePath + "/outline_color_win32", schemaPath: "#/$defs/ColorValue/oneOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs12 === errors;
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
        const err7 = { instancePath: instancePath + "/outline_color_win32", schemaPath: "#/$defs/ColorValue/oneOf", keyword: "oneOf", params: { passingSchemas: passing0 }, message: "must match exactly one schema in oneOf" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
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
    if (data.outline_color !== void 0) {
      let data4 = data.outline_color;
      const _errs16 = errors;
      let valid4 = false;
      let passing1 = null;
      const _errs17 = errors;
      if (!(typeof data4 == "number" && (!(data4 % 1) && !isNaN(data4)))) {
        const err8 = { instancePath: instancePath + "/outline_color", schemaPath: "#/$defs/ColorValue/oneOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid1 = _errs17 === errors;
      if (_valid1) {
        valid4 = true;
        passing1 = 0;
      }
      const _errs19 = errors;
      if (typeof data4 !== "string") {
        const err9 = { instancePath: instancePath + "/outline_color", schemaPath: "#/$defs/ColorValue/oneOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid1 = _errs19 === errors;
      if (_valid1 && valid4) {
        valid4 = false;
        passing1 = [passing1, 1];
      } else {
        if (_valid1) {
          valid4 = true;
          passing1 = 1;
        }
      }
      if (!valid4) {
        const err10 = { instancePath: instancePath + "/outline_color", schemaPath: "#/$defs/ColorValue/oneOf", keyword: "oneOf", params: { passingSchemas: passing1 }, message: "must match exactly one schema in oneOf" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
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
      let data5 = data.color;
      const _errs23 = errors;
      let valid6 = false;
      let passing2 = null;
      const _errs24 = errors;
      if (!(typeof data5 == "number" && (!(data5 % 1) && !isNaN(data5)))) {
        const err11 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/ColorValue/oneOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid2 = _errs24 === errors;
      if (_valid2) {
        valid6 = true;
        passing2 = 0;
      }
      const _errs26 = errors;
      if (typeof data5 !== "string") {
        const err12 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/ColorValue/oneOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid2 = _errs26 === errors;
      if (_valid2 && valid6) {
        valid6 = false;
        passing2 = [passing2, 1];
      } else {
        if (_valid2) {
          valid6 = true;
          passing2 = 1;
        }
      }
      if (!valid6) {
        const err13 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/ColorValue/oneOf", keyword: "oneOf", params: { passingSchemas: passing2 }, message: "must match exactly one schema in oneOf" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
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
    if (data.line_width !== void 0) {
      let data6 = data.line_width;
      const _errs30 = errors;
      let valid8 = false;
      let passing3 = null;
      const _errs31 = errors;
      const _errs32 = errors;
      let valid9 = false;
      const _errs33 = errors;
      if (typeof data6 !== "string") {
        const err14 = { instancePath: instancePath + "/line_width", schemaPath: "#/$defs/LineWidth/oneOf/0/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      if ("smallest" !== data6) {
        const err15 = { instancePath: instancePath + "/line_width", schemaPath: "#/$defs/LineWidth/oneOf/0/anyOf/0/const", keyword: "const", params: { allowedValue: "smallest" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid4 = _errs33 === errors;
      valid9 = valid9 || _valid4;
      const _errs35 = errors;
      if (typeof data6 !== "string") {
        const err16 = { instancePath: instancePath + "/line_width", schemaPath: "#/$defs/LineWidth/oneOf/0/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      if ("zero" !== data6) {
        const err17 = { instancePath: instancePath + "/line_width", schemaPath: "#/$defs/LineWidth/oneOf/0/anyOf/1/const", keyword: "const", params: { allowedValue: "zero" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      var _valid4 = _errs35 === errors;
      valid9 = valid9 || _valid4;
      const _errs37 = errors;
      if (typeof data6 !== "string") {
        const err18 = { instancePath: instancePath + "/line_width", schemaPath: "#/$defs/LineWidth/oneOf/0/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
      if ("small" !== data6) {
        const err19 = { instancePath: instancePath + "/line_width", schemaPath: "#/$defs/LineWidth/oneOf/0/anyOf/2/const", keyword: "const", params: { allowedValue: "small" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
      var _valid4 = _errs37 === errors;
      valid9 = valid9 || _valid4;
      const _errs39 = errors;
      if (typeof data6 !== "string") {
        const err20 = { instancePath: instancePath + "/line_width", schemaPath: "#/$defs/LineWidth/oneOf/0/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      if ("medium" !== data6) {
        const err21 = { instancePath: instancePath + "/line_width", schemaPath: "#/$defs/LineWidth/oneOf/0/anyOf/3/const", keyword: "const", params: { allowedValue: "medium" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      var _valid4 = _errs39 === errors;
      valid9 = valid9 || _valid4;
      const _errs41 = errors;
      if (typeof data6 !== "string") {
        const err22 = { instancePath: instancePath + "/line_width", schemaPath: "#/$defs/LineWidth/oneOf/0/anyOf/4/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
      if ("large" !== data6) {
        const err23 = { instancePath: instancePath + "/line_width", schemaPath: "#/$defs/LineWidth/oneOf/0/anyOf/4/const", keyword: "const", params: { allowedValue: "large" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      var _valid4 = _errs41 === errors;
      valid9 = valid9 || _valid4;
      if (!valid9) {
        const err24 = { instancePath: instancePath + "/line_width", schemaPath: "#/$defs/LineWidth/oneOf/0/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
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
      var _valid3 = _errs31 === errors;
      if (_valid3) {
        valid8 = true;
        passing3 = 0;
      }
      const _errs43 = errors;
      if (!(typeof data6 == "number" && (!(data6 % 1) && !isNaN(data6)))) {
        const err25 = { instancePath: instancePath + "/line_width", schemaPath: "#/$defs/LineWidth/oneOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
      var _valid3 = _errs43 === errors;
      if (_valid3 && valid8) {
        valid8 = false;
        passing3 = [passing3, 1];
      } else {
        if (_valid3) {
          valid8 = true;
          passing3 = 1;
        }
      }
      if (!valid8) {
        const err26 = { instancePath: instancePath + "/line_width", schemaPath: "#/$defs/LineWidth/oneOf", keyword: "oneOf", params: { passingSchemas: passing3 }, message: "must match exactly one schema in oneOf" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
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
    if (data.fill_color_win32 !== void 0) {
      let data7 = data.fill_color_win32;
      const _errs47 = errors;
      let valid11 = false;
      let passing4 = null;
      const _errs48 = errors;
      if (!(typeof data7 == "number" && (!(data7 % 1) && !isNaN(data7)))) {
        const err27 = { instancePath: instancePath + "/fill_color_win32", schemaPath: "#/$defs/ColorValue/oneOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
      var _valid5 = _errs48 === errors;
      if (_valid5) {
        valid11 = true;
        passing4 = 0;
      }
      const _errs50 = errors;
      if (typeof data7 !== "string") {
        const err28 = { instancePath: instancePath + "/fill_color_win32", schemaPath: "#/$defs/ColorValue/oneOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
      var _valid5 = _errs50 === errors;
      if (_valid5 && valid11) {
        valid11 = false;
        passing4 = [passing4, 1];
      } else {
        if (_valid5) {
          valid11 = true;
          passing4 = 1;
        }
      }
      if (!valid11) {
        const err29 = { instancePath: instancePath + "/fill_color_win32", schemaPath: "#/$defs/ColorValue/oneOf", keyword: "oneOf", params: { passingSchemas: passing4 }, message: "must match exactly one schema in oneOf" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
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
    if (data.fill_color !== void 0) {
      let data8 = data.fill_color;
      const _errs54 = errors;
      let valid13 = false;
      let passing5 = null;
      const _errs55 = errors;
      if (!(typeof data8 == "number" && (!(data8 % 1) && !isNaN(data8)))) {
        const err30 = { instancePath: instancePath + "/fill_color", schemaPath: "#/$defs/ColorValue/oneOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
        }
        errors++;
      }
      var _valid6 = _errs55 === errors;
      if (_valid6) {
        valid13 = true;
        passing5 = 0;
      }
      const _errs57 = errors;
      if (typeof data8 !== "string") {
        const err31 = { instancePath: instancePath + "/fill_color", schemaPath: "#/$defs/ColorValue/oneOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      }
      var _valid6 = _errs57 === errors;
      if (_valid6 && valid13) {
        valid13 = false;
        passing5 = [passing5, 1];
      } else {
        if (_valid6) {
          valid13 = true;
          passing5 = 1;
        }
      }
      if (!valid13) {
        const err32 = { instancePath: instancePath + "/fill_color", schemaPath: "#/$defs/ColorValue/oneOf", keyword: "oneOf", params: { passingSchemas: passing5 }, message: "must match exactly one schema in oneOf" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
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
    if (data.area_color !== void 0) {
      let data9 = data.area_color;
      const _errs61 = errors;
      let valid15 = false;
      let passing6 = null;
      const _errs62 = errors;
      if (!(typeof data9 == "number" && (!(data9 % 1) && !isNaN(data9)))) {
        const err33 = { instancePath: instancePath + "/area_color", schemaPath: "#/$defs/ColorValue/oneOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
      var _valid7 = _errs62 === errors;
      if (_valid7) {
        valid15 = true;
        passing6 = 0;
      }
      const _errs64 = errors;
      if (typeof data9 !== "string") {
        const err34 = { instancePath: instancePath + "/area_color", schemaPath: "#/$defs/ColorValue/oneOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
        }
        errors++;
      }
      var _valid7 = _errs64 === errors;
      if (_valid7 && valid15) {
        valid15 = false;
        passing6 = [passing6, 1];
      } else {
        if (_valid7) {
          valid15 = true;
          passing6 = 1;
        }
      }
      if (!valid15) {
        const err35 = { instancePath: instancePath + "/area_color", schemaPath: "#/$defs/ColorValue/oneOf", keyword: "oneOf", params: { passingSchemas: passing6 }, message: "must match exactly one schema in oneOf" };
        if (vErrors === null) {
          vErrors = [err35];
        } else {
          vErrors.push(err35);
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
    if (data.is_solid !== void 0) {
      if (typeof data.is_solid !== "boolean") {
        const err36 = { instancePath: instancePath + "/is_solid", schemaPath: "#/properties/is_solid/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err36];
        } else {
          vErrors.push(err36);
        }
        errors++;
      }
    }
    if (data.transparent !== void 0) {
      if (typeof data.transparent !== "boolean") {
        const err37 = { instancePath: instancePath + "/transparent", schemaPath: "#/properties/transparent/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err37];
        } else {
          vErrors.push(err37);
        }
        errors++;
      }
    }
    for (const key0 in data) {
      if (key0 !== "enabled" && key0 !== "min_width_mils" && key0 !== "min_height_mils" && key0 !== "outline_color_win32" && key0 !== "outline_color" && key0 !== "color" && key0 !== "line_width" && key0 !== "fill_color_win32" && key0 !== "fill_color" && key0 !== "area_color" && key0 !== "is_solid" && key0 !== "transparent") {
        const err38 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err38];
        } else {
          vErrors.push(err38);
        }
        errors++;
      }
    }
  } else {
    const err39 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err39];
    } else {
      vErrors.push(err39);
    }
    errors++;
  }
  validate29.errors = vErrors;
  return errors === 0;
}
validate29.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate31(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate31.evaluated;
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
    if (data.color_win32 !== void 0) {
      let data1 = data.color_win32;
      const _errs5 = errors;
      let valid2 = false;
      let passing0 = null;
      const _errs6 = errors;
      if (!(typeof data1 == "number" && (!(data1 % 1) && !isNaN(data1)))) {
        const err1 = { instancePath: instancePath + "/color_win32", schemaPath: "#/$defs/ColorValue/oneOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      var _valid0 = _errs6 === errors;
      if (_valid0) {
        valid2 = true;
        passing0 = 0;
      }
      const _errs8 = errors;
      if (typeof data1 !== "string") {
        const err2 = { instancePath: instancePath + "/color_win32", schemaPath: "#/$defs/ColorValue/oneOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs8 === errors;
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
        const err3 = { instancePath: instancePath + "/color_win32", schemaPath: "#/$defs/ColorValue/oneOf", keyword: "oneOf", params: { passingSchemas: passing0 }, message: "must match exactly one schema in oneOf" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
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
    if (data.color !== void 0) {
      let data2 = data.color;
      const _errs12 = errors;
      let valid4 = false;
      let passing1 = null;
      const _errs13 = errors;
      if (!(typeof data2 == "number" && (!(data2 % 1) && !isNaN(data2)))) {
        const err4 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/ColorValue/oneOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid1 = _errs13 === errors;
      if (_valid1) {
        valid4 = true;
        passing1 = 0;
      }
      const _errs15 = errors;
      if (typeof data2 !== "string") {
        const err5 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/ColorValue/oneOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      if (_valid1 && valid4) {
        valid4 = false;
        passing1 = [passing1, 1];
      } else {
        if (_valid1) {
          valid4 = true;
          passing1 = 1;
        }
      }
      if (!valid4) {
        const err6 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/ColorValue/oneOf", keyword: "oneOf", params: { passingSchemas: passing1 }, message: "must match exactly one schema in oneOf" };
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
    if (data.font_name !== void 0) {
      let data3 = data.font_name;
      if (typeof data3 === "string") {
        if (func1(data3) < 1) {
          const err7 = { instancePath: instancePath + "/font_name", schemaPath: "#/properties/font_name/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err7];
          } else {
            vErrors.push(err7);
          }
          errors++;
        }
      } else {
        const err8 = { instancePath: instancePath + "/font_name", schemaPath: "#/properties/font_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
    if (data.size_pt !== void 0) {
      let data4 = data.size_pt;
      if (!(typeof data4 == "number" && (!(data4 % 1) && !isNaN(data4)))) {
        const err9 = { instancePath: instancePath + "/size_pt", schemaPath: "#/properties/size_pt/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      if (typeof data4 == "number") {
        if (data4 < 1 || isNaN(data4)) {
          const err10 = { instancePath: instancePath + "/size_pt", schemaPath: "#/properties/size_pt/minimum", keyword: "minimum", params: { comparison: ">=", limit: 1 }, message: "must be >= 1" };
          if (vErrors === null) {
            vErrors = [err10];
          } else {
            vErrors.push(err10);
          }
          errors++;
        }
      }
    }
    if (data.bold !== void 0) {
      if (typeof data.bold !== "boolean") {
        const err11 = { instancePath: instancePath + "/bold", schemaPath: "#/properties/bold/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
    }
    if (data.italic !== void 0) {
      if (typeof data.italic !== "boolean") {
        const err12 = { instancePath: instancePath + "/italic", schemaPath: "#/properties/italic/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
    }
    if (data.font !== void 0) {
      if (!validate23(data.font, { instancePath: instancePath + "/font", parentData: data, parentDataProperty: "font", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate23.errors : vErrors.concat(validate23.errors);
        errors = vErrors.length;
      }
    }
    for (const key0 in data) {
      if (key0 !== "enabled" && key0 !== "color_win32" && key0 !== "color" && key0 !== "font_name" && key0 !== "size_pt" && key0 !== "bold" && key0 !== "italic" && key0 !== "font") {
        const err13 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
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
  validate31.errors = vErrors;
  return errors === 0;
}
validate31.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate35(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate35.evaluated;
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
    if (data.font !== void 0) {
      if (!validate23(data.font, { instancePath: instancePath + "/font", parentData: data, parentDataProperty: "font", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate23.errors : vErrors.concat(validate23.errors);
        errors = vErrors.length;
      }
    }
    for (const key0 in data) {
      if (key0 !== "enabled" && key0 !== "font") {
        const err1 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
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
  validate35.errors = vErrors;
  return errors === 0;
}
validate35.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate39(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate39.evaluated;
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
    if (data.font_name !== void 0) {
      let data1 = data.font_name;
      if (typeof data1 === "string") {
        if (func1(data1) < 1) {
          const err1 = { instancePath: instancePath + "/font_name", schemaPath: "#/properties/font_name/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err1];
          } else {
            vErrors.push(err1);
          }
          errors++;
        }
      } else {
        const err2 = { instancePath: instancePath + "/font_name", schemaPath: "#/properties/font_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
    if (data.font !== void 0) {
      let data2 = data.font;
      if (typeof data2 === "string") {
        if (func1(data2) < 1) {
          const err3 = { instancePath: instancePath + "/font", schemaPath: "#/properties/font/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/font", schemaPath: "#/properties/font/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.color_win32 !== void 0) {
      let data3 = data.color_win32;
      const _errs9 = errors;
      let valid2 = false;
      let passing0 = null;
      const _errs10 = errors;
      if (!(typeof data3 == "number" && (!(data3 % 1) && !isNaN(data3)))) {
        const err5 = { instancePath: instancePath + "/color_win32", schemaPath: "#/$defs/ColorValue/oneOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      if (_valid0) {
        valid2 = true;
        passing0 = 0;
      }
      const _errs12 = errors;
      if (typeof data3 !== "string") {
        const err6 = { instancePath: instancePath + "/color_win32", schemaPath: "#/$defs/ColorValue/oneOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs12 === errors;
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
        const err7 = { instancePath: instancePath + "/color_win32", schemaPath: "#/$defs/ColorValue/oneOf", keyword: "oneOf", params: { passingSchemas: passing0 }, message: "must match exactly one schema in oneOf" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
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
    if (data.color !== void 0) {
      let data4 = data.color;
      const _errs16 = errors;
      let valid4 = false;
      let passing1 = null;
      const _errs17 = errors;
      if (!(typeof data4 == "number" && (!(data4 % 1) && !isNaN(data4)))) {
        const err8 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/ColorValue/oneOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid1 = _errs17 === errors;
      if (_valid1) {
        valid4 = true;
        passing1 = 0;
      }
      const _errs19 = errors;
      if (typeof data4 !== "string") {
        const err9 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/ColorValue/oneOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid1 = _errs19 === errors;
      if (_valid1 && valid4) {
        valid4 = false;
        passing1 = [passing1, 1];
      } else {
        if (_valid1) {
          valid4 = true;
          passing1 = 1;
        }
      }
      if (!valid4) {
        const err10 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/ColorValue/oneOf", keyword: "oneOf", params: { passingSchemas: passing1 }, message: "must match exactly one schema in oneOf" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
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
    for (const key0 in data) {
      if (key0 !== "enabled" && key0 !== "font_name" && key0 !== "font" && key0 !== "color_win32" && key0 !== "color") {
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
  validate39.errors = vErrors;
  return errors === 0;
}
validate39.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.color_win32 !== void 0) {
      let data1 = data.color_win32;
      const _errs5 = errors;
      let valid2 = false;
      let passing0 = null;
      const _errs6 = errors;
      if (!(typeof data1 == "number" && (!(data1 % 1) && !isNaN(data1)))) {
        const err1 = { instancePath: instancePath + "/color_win32", schemaPath: "#/$defs/ColorValue/oneOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      var _valid0 = _errs6 === errors;
      if (_valid0) {
        valid2 = true;
        passing0 = 0;
      }
      const _errs8 = errors;
      if (typeof data1 !== "string") {
        const err2 = { instancePath: instancePath + "/color_win32", schemaPath: "#/$defs/ColorValue/oneOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs8 === errors;
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
        const err3 = { instancePath: instancePath + "/color_win32", schemaPath: "#/$defs/ColorValue/oneOf", keyword: "oneOf", params: { passingSchemas: passing0 }, message: "must match exactly one schema in oneOf" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
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
    if (data.color !== void 0) {
      let data2 = data.color;
      const _errs12 = errors;
      let valid4 = false;
      let passing1 = null;
      const _errs13 = errors;
      if (!(typeof data2 == "number" && (!(data2 % 1) && !isNaN(data2)))) {
        const err4 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/ColorValue/oneOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid1 = _errs13 === errors;
      if (_valid1) {
        valid4 = true;
        passing1 = 0;
      }
      const _errs15 = errors;
      if (typeof data2 !== "string") {
        const err5 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/ColorValue/oneOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      if (_valid1 && valid4) {
        valid4 = false;
        passing1 = [passing1, 1];
      } else {
        if (_valid1) {
          valid4 = true;
          passing1 = 1;
        }
      }
      if (!valid4) {
        const err6 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/ColorValue/oneOf", keyword: "oneOf", params: { passingSchemas: passing1 }, message: "must match exactly one schema in oneOf" };
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
    for (const key0 in data) {
      if (key0 !== "enabled" && key0 !== "color_win32" && key0 !== "color") {
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
  validate41.errors = vErrors;
  return errors === 0;
}
validate41.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.color_win32 !== void 0) {
      let data1 = data.color_win32;
      const _errs5 = errors;
      let valid2 = false;
      let passing0 = null;
      const _errs6 = errors;
      if (!(typeof data1 == "number" && (!(data1 % 1) && !isNaN(data1)))) {
        const err1 = { instancePath: instancePath + "/color_win32", schemaPath: "#/$defs/ColorValue/oneOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      var _valid0 = _errs6 === errors;
      if (_valid0) {
        valid2 = true;
        passing0 = 0;
      }
      const _errs8 = errors;
      if (typeof data1 !== "string") {
        const err2 = { instancePath: instancePath + "/color_win32", schemaPath: "#/$defs/ColorValue/oneOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs8 === errors;
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
        const err3 = { instancePath: instancePath + "/color_win32", schemaPath: "#/$defs/ColorValue/oneOf", keyword: "oneOf", params: { passingSchemas: passing0 }, message: "must match exactly one schema in oneOf" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
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
    if (data.color !== void 0) {
      let data2 = data.color;
      const _errs12 = errors;
      let valid4 = false;
      let passing1 = null;
      const _errs13 = errors;
      if (!(typeof data2 == "number" && (!(data2 % 1) && !isNaN(data2)))) {
        const err4 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/ColorValue/oneOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid1 = _errs13 === errors;
      if (_valid1) {
        valid4 = true;
        passing1 = 0;
      }
      const _errs15 = errors;
      if (typeof data2 !== "string") {
        const err5 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/ColorValue/oneOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      if (_valid1 && valid4) {
        valid4 = false;
        passing1 = [passing1, 1];
      } else {
        if (_valid1) {
          valid4 = true;
          passing1 = 1;
        }
      }
      if (!valid4) {
        const err6 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/ColorValue/oneOf", keyword: "oneOf", params: { passingSchemas: passing1 }, message: "must match exactly one schema in oneOf" };
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
    if (data.symbol !== void 0) {
      let data3 = data.symbol;
      const _errs19 = errors;
      let valid6 = false;
      let passing2 = null;
      const _errs20 = errors;
      if (!(typeof data3 == "number" && (!(data3 % 1) && !isNaN(data3)))) {
        const err7 = { instancePath: instancePath + "/symbol", schemaPath: "#/$defs/NoErcRuleSymbol/oneOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid2 = _errs20 === errors;
      if (_valid2) {
        valid6 = true;
        passing2 = 0;
      }
      const _errs22 = errors;
      if (typeof data3 !== "string") {
        const err8 = { instancePath: instancePath + "/symbol", schemaPath: "#/$defs/NoErcRuleSymbol/oneOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid2 = _errs22 === errors;
      if (_valid2 && valid6) {
        valid6 = false;
        passing2 = [passing2, 1];
      } else {
        if (_valid2) {
          valid6 = true;
          passing2 = 1;
        }
      }
      if (!valid6) {
        const err9 = { instancePath: instancePath + "/symbol", schemaPath: "#/$defs/NoErcRuleSymbol/oneOf", keyword: "oneOf", params: { passingSchemas: passing2 }, message: "must match exactly one schema in oneOf" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
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
    if (data.style !== void 0) {
      let data4 = data.style;
      const _errs26 = errors;
      let valid8 = false;
      let passing3 = null;
      const _errs27 = errors;
      if (!(typeof data4 == "number" && (!(data4 % 1) && !isNaN(data4)))) {
        const err10 = { instancePath: instancePath + "/style", schemaPath: "#/$defs/NoErcRuleStyle/oneOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid3 = _errs27 === errors;
      if (_valid3) {
        valid8 = true;
        passing3 = 0;
      }
      const _errs29 = errors;
      if (typeof data4 !== "string") {
        const err11 = { instancePath: instancePath + "/style", schemaPath: "#/$defs/NoErcRuleStyle/oneOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid3 = _errs29 === errors;
      if (_valid3 && valid8) {
        valid8 = false;
        passing3 = [passing3, 1];
      } else {
        if (_valid3) {
          valid8 = true;
          passing3 = 1;
        }
      }
      if (!valid8) {
        const err12 = { instancePath: instancePath + "/style", schemaPath: "#/$defs/NoErcRuleStyle/oneOf", keyword: "oneOf", params: { passingSchemas: passing3 }, message: "must match exactly one schema in oneOf" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
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
    for (const key0 in data) {
      if (key0 !== "enabled" && key0 !== "color_win32" && key0 !== "color" && key0 !== "symbol" && key0 !== "style") {
        const err13 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
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
  validate43.errors = vErrors;
  return errors === 0;
}
validate43.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate45(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate45.evaluated;
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
    if (data.line_color_win32 !== void 0) {
      let data1 = data.line_color_win32;
      const _errs5 = errors;
      let valid2 = false;
      let passing0 = null;
      const _errs6 = errors;
      if (!(typeof data1 == "number" && (!(data1 % 1) && !isNaN(data1)))) {
        const err1 = { instancePath: instancePath + "/line_color_win32", schemaPath: "#/$defs/ColorValue/oneOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      var _valid0 = _errs6 === errors;
      if (_valid0) {
        valid2 = true;
        passing0 = 0;
      }
      const _errs8 = errors;
      if (typeof data1 !== "string") {
        const err2 = { instancePath: instancePath + "/line_color_win32", schemaPath: "#/$defs/ColorValue/oneOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs8 === errors;
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
        const err3 = { instancePath: instancePath + "/line_color_win32", schemaPath: "#/$defs/ColorValue/oneOf", keyword: "oneOf", params: { passingSchemas: passing0 }, message: "must match exactly one schema in oneOf" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
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
    if (data.line_color !== void 0) {
      let data2 = data.line_color;
      const _errs12 = errors;
      let valid4 = false;
      let passing1 = null;
      const _errs13 = errors;
      if (!(typeof data2 == "number" && (!(data2 % 1) && !isNaN(data2)))) {
        const err4 = { instancePath: instancePath + "/line_color", schemaPath: "#/$defs/ColorValue/oneOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid1 = _errs13 === errors;
      if (_valid1) {
        valid4 = true;
        passing1 = 0;
      }
      const _errs15 = errors;
      if (typeof data2 !== "string") {
        const err5 = { instancePath: instancePath + "/line_color", schemaPath: "#/$defs/ColorValue/oneOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      if (_valid1 && valid4) {
        valid4 = false;
        passing1 = [passing1, 1];
      } else {
        if (_valid1) {
          valid4 = true;
          passing1 = 1;
        }
      }
      if (!valid4) {
        const err6 = { instancePath: instancePath + "/line_color", schemaPath: "#/$defs/ColorValue/oneOf", keyword: "oneOf", params: { passingSchemas: passing1 }, message: "must match exactly one schema in oneOf" };
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
    if (data.color !== void 0) {
      let data3 = data.color;
      const _errs19 = errors;
      let valid6 = false;
      let passing2 = null;
      const _errs20 = errors;
      if (!(typeof data3 == "number" && (!(data3 % 1) && !isNaN(data3)))) {
        const err7 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/ColorValue/oneOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid2 = _errs20 === errors;
      if (_valid2) {
        valid6 = true;
        passing2 = 0;
      }
      const _errs22 = errors;
      if (typeof data3 !== "string") {
        const err8 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/ColorValue/oneOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid2 = _errs22 === errors;
      if (_valid2 && valid6) {
        valid6 = false;
        passing2 = [passing2, 1];
      } else {
        if (_valid2) {
          valid6 = true;
          passing2 = 1;
        }
      }
      if (!valid6) {
        const err9 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/ColorValue/oneOf", keyword: "oneOf", params: { passingSchemas: passing2 }, message: "must match exactly one schema in oneOf" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
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
    if (data.area_color_win32 !== void 0) {
      let data4 = data.area_color_win32;
      const _errs26 = errors;
      let valid8 = false;
      let passing3 = null;
      const _errs27 = errors;
      if (!(typeof data4 == "number" && (!(data4 % 1) && !isNaN(data4)))) {
        const err10 = { instancePath: instancePath + "/area_color_win32", schemaPath: "#/$defs/ColorValue/oneOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid3 = _errs27 === errors;
      if (_valid3) {
        valid8 = true;
        passing3 = 0;
      }
      const _errs29 = errors;
      if (typeof data4 !== "string") {
        const err11 = { instancePath: instancePath + "/area_color_win32", schemaPath: "#/$defs/ColorValue/oneOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid3 = _errs29 === errors;
      if (_valid3 && valid8) {
        valid8 = false;
        passing3 = [passing3, 1];
      } else {
        if (_valid3) {
          valid8 = true;
          passing3 = 1;
        }
      }
      if (!valid8) {
        const err12 = { instancePath: instancePath + "/area_color_win32", schemaPath: "#/$defs/ColorValue/oneOf", keyword: "oneOf", params: { passingSchemas: passing3 }, message: "must match exactly one schema in oneOf" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
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
    if (data.area_color !== void 0) {
      let data5 = data.area_color;
      const _errs33 = errors;
      let valid10 = false;
      let passing4 = null;
      const _errs34 = errors;
      if (!(typeof data5 == "number" && (!(data5 % 1) && !isNaN(data5)))) {
        const err13 = { instancePath: instancePath + "/area_color", schemaPath: "#/$defs/ColorValue/oneOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid4 = _errs34 === errors;
      if (_valid4) {
        valid10 = true;
        passing4 = 0;
      }
      const _errs36 = errors;
      if (typeof data5 !== "string") {
        const err14 = { instancePath: instancePath + "/area_color", schemaPath: "#/$defs/ColorValue/oneOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid4 = _errs36 === errors;
      if (_valid4 && valid10) {
        valid10 = false;
        passing4 = [passing4, 1];
      } else {
        if (_valid4) {
          valid10 = true;
          passing4 = 1;
        }
      }
      if (!valid10) {
        const err15 = { instancePath: instancePath + "/area_color", schemaPath: "#/$defs/ColorValue/oneOf", keyword: "oneOf", params: { passingSchemas: passing4 }, message: "must match exactly one schema in oneOf" };
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
    if (data.document_font !== void 0) {
      if (!validate23(data.document_font, { instancePath: instancePath + "/document_font", parentData: data, parentDataProperty: "document_font", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate23.errors : vErrors.concat(validate23.errors);
        errors = vErrors.length;
      }
    }
    if (data.font !== void 0) {
      if (!validate23(data.font, { instancePath: instancePath + "/font", parentData: data, parentDataProperty: "font", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate23.errors : vErrors.concat(validate23.errors);
        errors = vErrors.length;
      }
    }
    for (const key0 in data) {
      if (key0 !== "enabled" && key0 !== "line_color_win32" && key0 !== "line_color" && key0 !== "color" && key0 !== "area_color_win32" && key0 !== "area_color" && key0 !== "document_font" && key0 !== "font") {
        const err16 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
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
  validate45.errors = vErrors;
  return errors === 0;
}
validate45.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.schema !== void 0) {
      let data0 = data.schema;
      const _errs2 = errors;
      let valid1 = false;
      const _errs3 = errors;
      if (typeof data0 !== "string") {
        const err0 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err0];
        } else {
          vErrors.push(err0);
        }
        errors++;
      }
      if ("altium_cruncher.clean.config.a0" !== data0) {
        const err1 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf/0/const", keyword: "const", params: { allowedValue: "altium_cruncher.clean.config.a0" }, message: "must be equal to constant" };
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
      if (data0 !== null) {
        const err2 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs5 === errors;
      valid1 = valid1 || _valid0;
      if (!valid1) {
        const err3 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
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
    if (data.normalize_pin_fonts !== void 0) {
      if (!validate22(data.normalize_pin_fonts, { instancePath: instancePath + "/normalize_pin_fonts", parentData: data, parentDataProperty: "normalize_pin_fonts", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate22.errors : vErrors.concat(validate22.errors);
        errors = vErrors.length;
      }
    }
    if (data.normalize_symbol_body_rectangles !== void 0) {
      if (!validate29(data.normalize_symbol_body_rectangles, { instancePath: instancePath + "/normalize_symbol_body_rectangles", parentData: data, parentDataProperty: "normalize_symbol_body_rectangles", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate29.errors : vErrors.concat(validate29.errors);
        errors = vErrors.length;
      }
    }
    if (data.normalize_power_symbols !== void 0) {
      if (!validate31(data.normalize_power_symbols, { instancePath: instancePath + "/normalize_power_symbols", parentData: data, parentDataProperty: "normalize_power_symbols", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate31.errors : vErrors.concat(validate31.errors);
        errors = vErrors.length;
      }
    }
    if (data.normalize_net_labels !== void 0) {
      if (!validate31(data.normalize_net_labels, { instancePath: instancePath + "/normalize_net_labels", parentData: data, parentDataProperty: "normalize_net_labels", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate31.errors : vErrors.concat(validate31.errors);
        errors = vErrors.length;
      }
    }
    if (data.normalize_component_designators !== void 0) {
      if (!validate35(data.normalize_component_designators, { instancePath: instancePath + "/normalize_component_designators", parentData: data, parentDataProperty: "normalize_component_designators", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate35.errors : vErrors.concat(validate35.errors);
        errors = vErrors.length;
      }
    }
    if (data.normalize_component_parameters !== void 0) {
      if (!validate35(data.normalize_component_parameters, { instancePath: instancePath + "/normalize_component_parameters", parentData: data, parentDataProperty: "normalize_component_parameters", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate35.errors : vErrors.concat(validate35.errors);
        errors = vErrors.length;
      }
    }
    if (data.normalize_component_free_text !== void 0) {
      if (!validate39(data.normalize_component_free_text, { instancePath: instancePath + "/normalize_component_free_text", parentData: data, parentDataProperty: "normalize_component_free_text", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate39.errors : vErrors.concat(validate39.errors);
        errors = vErrors.length;
      }
    }
    if (data.normalize_wires !== void 0) {
      if (!validate41(data.normalize_wires, { instancePath: instancePath + "/normalize_wires", parentData: data, parentDataProperty: "normalize_wires", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate41.errors : vErrors.concat(validate41.errors);
        errors = vErrors.length;
      }
    }
    if (data.normalize_no_erc !== void 0) {
      if (!validate43(data.normalize_no_erc, { instancePath: instancePath + "/normalize_no_erc", parentData: data, parentDataProperty: "normalize_no_erc", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate43.errors : vErrors.concat(validate43.errors);
        errors = vErrors.length;
      }
    }
    if (data.normalize_sheet_style !== void 0) {
      if (!validate45(data.normalize_sheet_style, { instancePath: instancePath + "/normalize_sheet_style", parentData: data, parentDataProperty: "normalize_sheet_style", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate45.errors : vErrors.concat(validate45.errors);
        errors = vErrors.length;
      }
    }
    if (data.normalize_symbol_internal_graphics_monochrome !== void 0) {
      let data11 = data.normalize_symbol_internal_graphics_monochrome;
      if (data11 && typeof data11 == "object" && !Array.isArray(data11)) {
        if (data11.enabled !== void 0) {
          if (typeof data11.enabled !== "boolean") {
            const err4 = { instancePath: instancePath + "/normalize_symbol_internal_graphics_monochrome/enabled", schemaPath: "#/$defs/InternalGraphics/properties/enabled/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err4];
            } else {
              vErrors.push(err4);
            }
            errors++;
          }
        }
        if (data11.saturation !== void 0) {
          let data13 = data11.saturation;
          if (typeof data13 == "number") {
            if (data13 > 1 || isNaN(data13)) {
              const err5 = { instancePath: instancePath + "/normalize_symbol_internal_graphics_monochrome/saturation", schemaPath: "#/$defs/InternalGraphics/properties/saturation/maximum", keyword: "maximum", params: { comparison: "<=", limit: 1 }, message: "must be <= 1" };
              if (vErrors === null) {
                vErrors = [err5];
              } else {
                vErrors.push(err5);
              }
              errors++;
            }
            if (data13 < 0 || isNaN(data13)) {
              const err6 = { instancePath: instancePath + "/normalize_symbol_internal_graphics_monochrome/saturation", schemaPath: "#/$defs/InternalGraphics/properties/saturation/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
              if (vErrors === null) {
                vErrors = [err6];
              } else {
                vErrors.push(err6);
              }
              errors++;
            }
          } else {
            const err7 = { instancePath: instancePath + "/normalize_symbol_internal_graphics_monochrome/saturation", schemaPath: "#/$defs/InternalGraphics/properties/saturation/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err7];
            } else {
              vErrors.push(err7);
            }
            errors++;
          }
        }
        for (const key0 in data11) {
          if (key0 !== "enabled" && key0 !== "saturation") {
            const err8 = { instancePath: instancePath + "/normalize_symbol_internal_graphics_monochrome/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/InternalGraphics/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err8];
            } else {
              vErrors.push(err8);
            }
            errors++;
          }
        }
      } else {
        const err9 = { instancePath: instancePath + "/normalize_symbol_internal_graphics_monochrome", schemaPath: "#/$defs/InternalGraphics/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "schema" && key1 !== "normalize_pin_fonts" && key1 !== "normalize_symbol_body_rectangles" && key1 !== "normalize_power_symbols" && key1 !== "normalize_net_labels" && key1 !== "normalize_component_designators" && key1 !== "normalize_component_parameters" && key1 !== "normalize_component_free_text" && key1 !== "normalize_wires" && key1 !== "normalize_no_erc" && key1 !== "normalize_sheet_style" && key1 !== "normalize_symbol_internal_graphics_monochrome") {
        const err10 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
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
  validate21.errors = vErrors;
  return errors === 0;
}
validate21.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate51(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate51.evaluated;
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
    if (data.primitive_types !== void 0) {
      let data1 = data.primitive_types;
      if (Array.isArray(data1)) {
        const len0 = data1.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (typeof data1[i0] !== "string") {
            const err1 = { instancePath: instancePath + "/primitive_types/" + i0, schemaPath: "#/$defs/StringList/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err1];
            } else {
              vErrors.push(err1);
            }
            errors++;
          }
        }
      } else {
        const err2 = { instancePath: instancePath + "/primitive_types", schemaPath: "#/$defs/StringList/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
    if (data.layers !== void 0) {
      let data3 = data.layers;
      if (Array.isArray(data3)) {
        const len1 = data3.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (typeof data3[i1] !== "string") {
            const err3 = { instancePath: instancePath + "/layers/" + i1, schemaPath: "#/$defs/StringList/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err3];
            } else {
              vErrors.push(err3);
            }
            errors++;
          }
        }
      } else {
        const err4 = { instancePath: instancePath + "/layers", schemaPath: "#/$defs/StringList/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.preserve_regions !== void 0) {
      if (typeof data.preserve_regions !== "boolean") {
        const err5 = { instancePath: instancePath + "/preserve_regions", schemaPath: "#/properties/preserve_regions/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.preserve_component_bodies !== void 0) {
      if (typeof data.preserve_component_bodies !== "boolean") {
        const err6 = { instancePath: instancePath + "/preserve_component_bodies", schemaPath: "#/properties/preserve_component_bodies/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    for (const key0 in data) {
      if (key0 !== "enabled" && key0 !== "primitive_types" && key0 !== "layers" && key0 !== "preserve_regions" && key0 !== "preserve_component_bodies") {
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
  validate51.errors = vErrors;
  return errors === 0;
}
validate51.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate53(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate53.evaluated;
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
    if (data.layers !== void 0) {
      let data1 = data.layers;
      if (Array.isArray(data1)) {
        const len0 = data1.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (typeof data1[i0] !== "string") {
            const err1 = { instancePath: instancePath + "/layers/" + i0, schemaPath: "#/$defs/StringList/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err1];
            } else {
              vErrors.push(err1);
            }
            errors++;
          }
        }
      } else {
        const err2 = { instancePath: instancePath + "/layers", schemaPath: "#/$defs/StringList/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
    if (data.match !== void 0) {
      let data3 = data.match;
      const _errs9 = errors;
      let valid4 = false;
      const _errs10 = errors;
      if (typeof data3 !== "string") {
        const err3 = { instancePath: instancePath + "/match", schemaPath: "#/properties/match/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      if ("all" !== data3) {
        const err4 = { instancePath: instancePath + "/match", schemaPath: "#/properties/match/anyOf/0/const", keyword: "const", params: { allowedValue: "all" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      valid4 = valid4 || _valid0;
      const _errs12 = errors;
      if (typeof data3 !== "string") {
        const err5 = { instancePath: instancePath + "/match", schemaPath: "#/properties/match/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      if ("regex" !== data3) {
        const err6 = { instancePath: instancePath + "/match", schemaPath: "#/properties/match/anyOf/1/const", keyword: "const", params: { allowedValue: "regex" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs12 === errors;
      valid4 = valid4 || _valid0;
      const _errs14 = errors;
      if (typeof data3 !== "string") {
        const err7 = { instancePath: instancePath + "/match", schemaPath: "#/properties/match/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      if ("contains" !== data3) {
        const err8 = { instancePath: instancePath + "/match", schemaPath: "#/properties/match/anyOf/2/const", keyword: "const", params: { allowedValue: "contains" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid0 = _errs14 === errors;
      valid4 = valid4 || _valid0;
      const _errs16 = errors;
      if (typeof data3 !== "string") {
        const err9 = { instancePath: instancePath + "/match", schemaPath: "#/properties/match/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      if ("exact" !== data3) {
        const err10 = { instancePath: instancePath + "/match", schemaPath: "#/properties/match/anyOf/3/const", keyword: "const", params: { allowedValue: "exact" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid0 = _errs16 === errors;
      valid4 = valid4 || _valid0;
      if (!valid4) {
        const err11 = { instancePath: instancePath + "/match", schemaPath: "#/properties/match/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
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
    if (data.patterns !== void 0) {
      let data4 = data.patterns;
      if (Array.isArray(data4)) {
        const len1 = data4.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (typeof data4[i1] !== "string") {
            const err12 = { instancePath: instancePath + "/patterns/" + i1, schemaPath: "#/$defs/StringList/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err12];
            } else {
              vErrors.push(err12);
            }
            errors++;
          }
        }
      } else {
        const err13 = { instancePath: instancePath + "/patterns", schemaPath: "#/$defs/StringList/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    for (const key0 in data) {
      if (key0 !== "enabled" && key0 !== "layers" && key0 !== "match" && key0 !== "patterns") {
        const err14 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
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
  validate53.errors = vErrors;
  return errors === 0;
}
validate53.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.layers !== void 0) {
      let data1 = data.layers;
      if (Array.isArray(data1)) {
        const len0 = data1.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (typeof data1[i0] !== "string") {
            const err1 = { instancePath: instancePath + "/layers/" + i0, schemaPath: "#/$defs/StringList/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err1];
            } else {
              vErrors.push(err1);
            }
            errors++;
          }
        }
      } else {
        const err2 = { instancePath: instancePath + "/layers", schemaPath: "#/$defs/StringList/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
    if (data.preserve_component_linked !== void 0) {
      if (typeof data.preserve_component_linked !== "boolean") {
        const err3 = { instancePath: instancePath + "/preserve_component_linked", schemaPath: "#/properties/preserve_component_linked/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.preserve_model_associated !== void 0) {
      if (typeof data.preserve_model_associated !== "boolean") {
        const err4 = { instancePath: instancePath + "/preserve_model_associated", schemaPath: "#/properties/preserve_model_associated/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.preserve_keepouts !== void 0) {
      if (typeof data.preserve_keepouts !== "boolean") {
        const err5 = { instancePath: instancePath + "/preserve_keepouts", schemaPath: "#/properties/preserve_keepouts/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.preserve_board_cutouts !== void 0) {
      if (typeof data.preserve_board_cutouts !== "boolean") {
        const err6 = { instancePath: instancePath + "/preserve_board_cutouts", schemaPath: "#/properties/preserve_board_cutouts/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.preserve_custom_pad_regions !== void 0) {
      if (typeof data.preserve_custom_pad_regions !== "boolean") {
        const err7 = { instancePath: instancePath + "/preserve_custom_pad_regions", schemaPath: "#/properties/preserve_custom_pad_regions/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    for (const key0 in data) {
      if (key0 !== "enabled" && key0 !== "layers" && key0 !== "preserve_component_linked" && key0 !== "preserve_model_associated" && key0 !== "preserve_keepouts" && key0 !== "preserve_board_cutouts" && key0 !== "preserve_custom_pad_regions") {
        const err8 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
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
  validate55.errors = vErrors;
  return errors === 0;
}
validate55.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate50(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate50.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.schema !== void 0) {
      let data0 = data.schema;
      const _errs2 = errors;
      let valid1 = false;
      const _errs3 = errors;
      if (typeof data0 !== "string") {
        const err0 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err0];
        } else {
          vErrors.push(err0);
        }
        errors++;
      }
      if ("altium_cruncher.pcblib.clean.config.a0" !== data0) {
        const err1 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf/0/const", keyword: "const", params: { allowedValue: "altium_cruncher.pcblib.clean.config.a0" }, message: "must be equal to constant" };
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
      if (data0 !== null) {
        const err2 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs5 === errors;
      valid1 = valid1 || _valid0;
      if (!valid1) {
        const err3 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
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
    if (data.profile !== void 0) {
      let data1 = data.profile;
      const _errs8 = errors;
      let valid2 = false;
      const _errs9 = errors;
      if (typeof data1 !== "string") {
        const err4 = { instancePath: instancePath + "/profile", schemaPath: "#/properties/profile/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      if ("default" !== data1) {
        const err5 = { instancePath: instancePath + "/profile", schemaPath: "#/properties/profile/anyOf/0/const", keyword: "const", params: { allowedValue: "default" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid1 = _errs9 === errors;
      valid2 = valid2 || _valid1;
      const _errs11 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/profile", schemaPath: "#/properties/profile/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      if ("raw" !== data1) {
        const err7 = { instancePath: instancePath + "/profile", schemaPath: "#/properties/profile/anyOf/1/const", keyword: "const", params: { allowedValue: "raw" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid1 = _errs11 === errors;
      valid2 = valid2 || _valid1;
      if (!valid2) {
        const err8 = { instancePath: instancePath + "/profile", schemaPath: "#/properties/profile/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
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
    if (data.remove_mechanical_primitives !== void 0) {
      if (!validate51(data.remove_mechanical_primitives, { instancePath: instancePath + "/remove_mechanical_primitives", parentData: data, parentDataProperty: "remove_mechanical_primitives", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate51.errors : vErrors.concat(validate51.errors);
        errors = vErrors.length;
      }
    }
    if (data.remove_text_strings !== void 0) {
      if (!validate53(data.remove_text_strings, { instancePath: instancePath + "/remove_text_strings", parentData: data, parentDataProperty: "remove_text_strings", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate53.errors : vErrors.concat(validate53.errors);
        errors = vErrors.length;
      }
    }
    if (data.remove_regions !== void 0) {
      if (!validate55(data.remove_regions, { instancePath: instancePath + "/remove_regions", parentData: data, parentDataProperty: "remove_regions", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate55.errors : vErrors.concat(validate55.errors);
        errors = vErrors.length;
      }
    }
    for (const key0 in data) {
      if (key0 !== "schema" && key0 !== "profile" && key0 !== "remove_mechanical_primitives" && key0 !== "remove_text_strings" && key0 !== "remove_regions") {
        const err9 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
  } else {
    const err10 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err10];
    } else {
      vErrors.push(err10);
    }
    errors++;
  }
  validate50.errors = vErrors;
  return errors === 0;
}
validate50.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
  if (!validate50(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate50.errors : vErrors.concat(validate50.errors);
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
