// Generated from src/tsp/altium_cruncher/config/pcb-svg.tsp. Do not edit.
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
var pattern4 = new RegExp("^\\s*(?:[bB][oO][aA][rR][dD]_[oO][uU][tT][lL][iI][nN][eE]|[aA][lL][lL]_[gG][eE][oO][mM][eE][tT][rR][yY]|[bB][oO][aA][rR][dD]|[oO][uU][tT][lL][iI][nN][eE]|[bB][oO][aA][rR][dD]_[pP][rR][oO][fF][iI][lL][eE]|[lL][eE][gG][aA][cC][yY]|[aA][lL][lL]|[rR][eE][nN][dD][eE][rR][eE][dD]_[vV][iI][eE][wW]|[rR][eE][nN][dD][eE][rR][eE][dD]_[gG][eE][oO][mM][eE][tT][rR][yY])\\s*$", "u");
var pattern5 = new RegExp("^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$", "u");
var pattern6 = new RegExp("^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$", "u");
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
    for (const key0 in data) {
      let data0 = data[key0];
      if (data0 && typeof data0 == "object" && !Array.isArray(data0)) {
      } else {
        const err0 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/StyleObject/type", keyword: "type", params: { type: "object" }, message: "must be object" };
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
  validate23.errors = vErrors;
  return errors === 0;
}
validate23.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
      if (!(typeof data0 == "number")) {
        const err2 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (typeof data0 === "string") {
        if (!pattern6.test(data0)) {
          const err3 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err5 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.line_width_mm !== void 0) {
      let data1 = data.line_width_mm;
      const _errs14 = errors;
      let valid4 = false;
      const _errs15 = errors;
      if (typeof data1 == "number") {
        if (data1 <= 0 || isNaN(data1)) {
          const err6 = { instancePath: instancePath + "/line_width_mm", schemaPath: "#/properties/line_width_mm/anyOf/0/exclusiveMinimum", keyword: "exclusiveMinimum", params: { comparison: ">", limit: 0 }, message: "must be > 0" };
          if (vErrors === null) {
            vErrors = [err6];
          } else {
            vErrors.push(err6);
          }
          errors++;
        }
      } else {
        const err7 = { instancePath: instancePath + "/line_width_mm", schemaPath: "#/properties/line_width_mm/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      valid4 = valid4 || _valid1;
      const _errs17 = errors;
      if (typeof data1 !== "boolean") {
        const err8 = { instancePath: instancePath + "/line_width_mm", schemaPath: "#/properties/line_width_mm/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid1 = _errs17 === errors;
      valid4 = valid4 || _valid1;
      const _errs19 = errors;
      if (typeof data1 === "string") {
        if (!pattern5.test(data1)) {
          const err9 = { instancePath: instancePath + "/line_width_mm", schemaPath: "#/properties/line_width_mm/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err9];
          } else {
            vErrors.push(err9);
          }
          errors++;
        }
      } else {
        const err10 = { instancePath: instancePath + "/line_width_mm", schemaPath: "#/properties/line_width_mm/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid1 = _errs19 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err11 = { instancePath: instancePath + "/line_width_mm", schemaPath: "#/properties/line_width_mm/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
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
      if (typeof data1 === "string" || typeof data1 === "boolean") {
        if (!Number.isFinite(Number(data1))) {
          const err12 = { instancePath: instancePath + "/line_width_mm", schemaPath: "#/properties/line_width_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err12];
          } else {
            vErrors.push(err12);
          }
          errors++;
        }
        if (Number(data1) <= 0) {
          const err13 = { instancePath: instancePath + "/line_width_mm", schemaPath: "#/properties/line_width_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err13];
          } else {
            vErrors.push(err13);
          }
          errors++;
        }
      }
    }
    if (data.opacity !== void 0) {
      let data2 = data.opacity;
      const _errs22 = errors;
      let valid5 = false;
      const _errs23 = errors;
      if (typeof data2 == "number") {
        if (data2 > 1 || isNaN(data2)) {
          const err14 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/0/maximum", keyword: "maximum", params: { comparison: "<=", limit: 1 }, message: "must be <= 1" };
          if (vErrors === null) {
            vErrors = [err14];
          } else {
            vErrors.push(err14);
          }
          errors++;
        }
        if (data2 < 0 || isNaN(data2)) {
          const err15 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/0/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err15];
          } else {
            vErrors.push(err15);
          }
          errors++;
        }
      } else {
        const err16 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid2 = _errs23 === errors;
      valid5 = valid5 || _valid2;
      const _errs25 = errors;
      if (typeof data2 !== "boolean") {
        const err17 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      var _valid2 = _errs25 === errors;
      valid5 = valid5 || _valid2;
      const _errs27 = errors;
      if (typeof data2 === "string") {
        if (!pattern5.test(data2)) {
          const err18 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err18];
          } else {
            vErrors.push(err18);
          }
          errors++;
        }
      } else {
        const err19 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
      var _valid2 = _errs27 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err20 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
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
      if (typeof data2 === "string" || typeof data2 === "boolean") {
        if (!Number.isFinite(Number(data2))) {
          const err21 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err21];
          } else {
            vErrors.push(err21);
          }
          errors++;
        }
        if (Number(data2) < 0) {
          const err22 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err22];
          } else {
            vErrors.push(err22);
          }
          errors++;
        }
        if (Number(data2) > 1) {
          const err23 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err23];
          } else {
            vErrors.push(err23);
          }
          errors++;
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
  validate25.errors = vErrors;
  return errors === 0;
}
validate25.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate27(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate27.evaluated;
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
      if (!(typeof data0 == "number")) {
        const err2 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (typeof data0 === "string") {
        if (!pattern6.test(data0)) {
          const err3 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err5 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.color !== void 0) {
      if (typeof data.color !== "string") {
        const err6 = { instancePath: instancePath + "/color", schemaPath: "#/properties/color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.stroke_color !== void 0) {
      if (typeof data.stroke_color !== "string") {
        const err7 = { instancePath: instancePath + "/stroke_color", schemaPath: "#/properties/stroke_color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.stroke_width_mm !== void 0) {
      let data3 = data.stroke_width_mm;
      const _errs18 = errors;
      let valid4 = false;
      const _errs19 = errors;
      if (typeof data3 == "number") {
        if (data3 < 0 || isNaN(data3)) {
          const err8 = { instancePath: instancePath + "/stroke_width_mm", schemaPath: "#/properties/stroke_width_mm/anyOf/0/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err8];
          } else {
            vErrors.push(err8);
          }
          errors++;
        }
      } else {
        const err9 = { instancePath: instancePath + "/stroke_width_mm", schemaPath: "#/properties/stroke_width_mm/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid1 = _errs19 === errors;
      valid4 = valid4 || _valid1;
      const _errs21 = errors;
      if (typeof data3 !== "boolean") {
        const err10 = { instancePath: instancePath + "/stroke_width_mm", schemaPath: "#/properties/stroke_width_mm/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid1 = _errs21 === errors;
      valid4 = valid4 || _valid1;
      const _errs23 = errors;
      if (typeof data3 === "string") {
        if (!pattern5.test(data3)) {
          const err11 = { instancePath: instancePath + "/stroke_width_mm", schemaPath: "#/properties/stroke_width_mm/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err11];
          } else {
            vErrors.push(err11);
          }
          errors++;
        }
      } else {
        const err12 = { instancePath: instancePath + "/stroke_width_mm", schemaPath: "#/properties/stroke_width_mm/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid1 = _errs23 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err13 = { instancePath: instancePath + "/stroke_width_mm", schemaPath: "#/properties/stroke_width_mm/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
      if (typeof data3 === "string" || typeof data3 === "boolean") {
        if (!Number.isFinite(Number(data3))) {
          const err14 = { instancePath: instancePath + "/stroke_width_mm", schemaPath: "#/properties/stroke_width_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err14];
          } else {
            vErrors.push(err14);
          }
          errors++;
        }
        if (Number(data3) < 0) {
          const err15 = { instancePath: instancePath + "/stroke_width_mm", schemaPath: "#/properties/stroke_width_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err15];
          } else {
            vErrors.push(err15);
          }
          errors++;
        }
      }
    }
    if (data.fill_ratio !== void 0) {
      let data4 = data.fill_ratio;
      const _errs26 = errors;
      let valid5 = false;
      const _errs27 = errors;
      if (typeof data4 == "number") {
        if (data4 > 1 || isNaN(data4)) {
          const err16 = { instancePath: instancePath + "/fill_ratio", schemaPath: "#/properties/fill_ratio/anyOf/0/maximum", keyword: "maximum", params: { comparison: "<=", limit: 1 }, message: "must be <= 1" };
          if (vErrors === null) {
            vErrors = [err16];
          } else {
            vErrors.push(err16);
          }
          errors++;
        }
        if (data4 <= 0 || isNaN(data4)) {
          const err17 = { instancePath: instancePath + "/fill_ratio", schemaPath: "#/properties/fill_ratio/anyOf/0/exclusiveMinimum", keyword: "exclusiveMinimum", params: { comparison: ">", limit: 0 }, message: "must be > 0" };
          if (vErrors === null) {
            vErrors = [err17];
          } else {
            vErrors.push(err17);
          }
          errors++;
        }
      } else {
        const err18 = { instancePath: instancePath + "/fill_ratio", schemaPath: "#/properties/fill_ratio/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
      var _valid2 = _errs27 === errors;
      valid5 = valid5 || _valid2;
      const _errs29 = errors;
      if (typeof data4 !== "boolean") {
        const err19 = { instancePath: instancePath + "/fill_ratio", schemaPath: "#/properties/fill_ratio/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
      var _valid2 = _errs29 === errors;
      valid5 = valid5 || _valid2;
      const _errs31 = errors;
      if (typeof data4 === "string") {
        if (!pattern5.test(data4)) {
          const err20 = { instancePath: instancePath + "/fill_ratio", schemaPath: "#/properties/fill_ratio/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err20];
          } else {
            vErrors.push(err20);
          }
          errors++;
        }
      } else {
        const err21 = { instancePath: instancePath + "/fill_ratio", schemaPath: "#/properties/fill_ratio/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      var _valid2 = _errs31 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err22 = { instancePath: instancePath + "/fill_ratio", schemaPath: "#/properties/fill_ratio/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
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
      if (typeof data4 === "string" || typeof data4 === "boolean") {
        if (!Number.isFinite(Number(data4))) {
          const err23 = { instancePath: instancePath + "/fill_ratio", schemaPath: "#/properties/fill_ratio/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err23];
          } else {
            vErrors.push(err23);
          }
          errors++;
        }
        if (Number(data4) > 1) {
          const err24 = { instancePath: instancePath + "/fill_ratio", schemaPath: "#/properties/fill_ratio/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err24];
          } else {
            vErrors.push(err24);
          }
          errors++;
        }
        if (Number(data4) <= 0) {
          const err25 = { instancePath: instancePath + "/fill_ratio", schemaPath: "#/properties/fill_ratio/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err25];
          } else {
            vErrors.push(err25);
          }
          errors++;
        }
      }
    }
    if (data.max_font_size_mm !== void 0) {
      let data5 = data.max_font_size_mm;
      const _errs34 = errors;
      let valid6 = false;
      const _errs35 = errors;
      if (typeof data5 == "number") {
        if (data5 <= 0 || isNaN(data5)) {
          const err26 = { instancePath: instancePath + "/max_font_size_mm", schemaPath: "#/properties/max_font_size_mm/anyOf/0/exclusiveMinimum", keyword: "exclusiveMinimum", params: { comparison: ">", limit: 0 }, message: "must be > 0" };
          if (vErrors === null) {
            vErrors = [err26];
          } else {
            vErrors.push(err26);
          }
          errors++;
        }
      } else {
        const err27 = { instancePath: instancePath + "/max_font_size_mm", schemaPath: "#/properties/max_font_size_mm/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
      var _valid3 = _errs35 === errors;
      valid6 = valid6 || _valid3;
      const _errs37 = errors;
      if (typeof data5 !== "boolean") {
        const err28 = { instancePath: instancePath + "/max_font_size_mm", schemaPath: "#/properties/max_font_size_mm/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
      var _valid3 = _errs37 === errors;
      valid6 = valid6 || _valid3;
      const _errs39 = errors;
      if (typeof data5 === "string") {
        if (!pattern5.test(data5)) {
          const err29 = { instancePath: instancePath + "/max_font_size_mm", schemaPath: "#/properties/max_font_size_mm/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err29];
          } else {
            vErrors.push(err29);
          }
          errors++;
        }
      } else {
        const err30 = { instancePath: instancePath + "/max_font_size_mm", schemaPath: "#/properties/max_font_size_mm/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
        }
        errors++;
      }
      var _valid3 = _errs39 === errors;
      valid6 = valid6 || _valid3;
      if (!valid6) {
        const err31 = { instancePath: instancePath + "/max_font_size_mm", schemaPath: "#/properties/max_font_size_mm/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
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
      if (typeof data5 === "string" || typeof data5 === "boolean") {
        if (!Number.isFinite(Number(data5))) {
          const err32 = { instancePath: instancePath + "/max_font_size_mm", schemaPath: "#/properties/max_font_size_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err32];
          } else {
            vErrors.push(err32);
          }
          errors++;
        }
        if (Number(data5) <= 0) {
          const err33 = { instancePath: instancePath + "/max_font_size_mm", schemaPath: "#/properties/max_font_size_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err33];
          } else {
            vErrors.push(err33);
          }
          errors++;
        }
      }
    }
    if (data.opacity !== void 0) {
      let data6 = data.opacity;
      const _errs42 = errors;
      let valid7 = false;
      const _errs43 = errors;
      if (typeof data6 == "number") {
        if (data6 > 1 || isNaN(data6)) {
          const err34 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/0/maximum", keyword: "maximum", params: { comparison: "<=", limit: 1 }, message: "must be <= 1" };
          if (vErrors === null) {
            vErrors = [err34];
          } else {
            vErrors.push(err34);
          }
          errors++;
        }
        if (data6 < 0 || isNaN(data6)) {
          const err35 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/0/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err35];
          } else {
            vErrors.push(err35);
          }
          errors++;
        }
      } else {
        const err36 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err36];
        } else {
          vErrors.push(err36);
        }
        errors++;
      }
      var _valid4 = _errs43 === errors;
      valid7 = valid7 || _valid4;
      const _errs45 = errors;
      if (typeof data6 !== "boolean") {
        const err37 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err37];
        } else {
          vErrors.push(err37);
        }
        errors++;
      }
      var _valid4 = _errs45 === errors;
      valid7 = valid7 || _valid4;
      const _errs47 = errors;
      if (typeof data6 === "string") {
        if (!pattern5.test(data6)) {
          const err38 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err38];
          } else {
            vErrors.push(err38);
          }
          errors++;
        }
      } else {
        const err39 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err39];
        } else {
          vErrors.push(err39);
        }
        errors++;
      }
      var _valid4 = _errs47 === errors;
      valid7 = valid7 || _valid4;
      if (!valid7) {
        const err40 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err40];
        } else {
          vErrors.push(err40);
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
      if (typeof data6 === "string" || typeof data6 === "boolean") {
        if (!Number.isFinite(Number(data6))) {
          const err41 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err41];
          } else {
            vErrors.push(err41);
          }
          errors++;
        }
        if (Number(data6) < 0) {
          const err42 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err42];
          } else {
            vErrors.push(err42);
          }
          errors++;
        }
        if (Number(data6) > 1) {
          const err43 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err43];
          } else {
            vErrors.push(err43);
          }
          errors++;
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
  validate27.errors = vErrors;
  return errors === 0;
}
validate27.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
      if (!(typeof data0 == "number")) {
        const err2 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (typeof data0 === "string") {
        if (!pattern6.test(data0)) {
          const err3 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err5 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.color !== void 0) {
      if (typeof data.color !== "string") {
        const err6 = { instancePath: instancePath + "/color", schemaPath: "#/properties/color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
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
      if (!(typeof data0 == "number")) {
        const err2 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (typeof data0 === "string") {
        if (!pattern6.test(data0)) {
          const err3 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err5 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.color !== void 0) {
      if (typeof data.color !== "string") {
        const err6 = { instancePath: instancePath + "/color", schemaPath: "#/properties/color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.opacity !== void 0) {
      let data2 = data.opacity;
      const _errs16 = errors;
      let valid4 = false;
      const _errs17 = errors;
      if (typeof data2 == "number") {
        if (data2 > 1 || isNaN(data2)) {
          const err7 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/0/maximum", keyword: "maximum", params: { comparison: "<=", limit: 1 }, message: "must be <= 1" };
          if (vErrors === null) {
            vErrors = [err7];
          } else {
            vErrors.push(err7);
          }
          errors++;
        }
        if (data2 < 0 || isNaN(data2)) {
          const err8 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/0/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err8];
          } else {
            vErrors.push(err8);
          }
          errors++;
        }
      } else {
        const err9 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid1 = _errs17 === errors;
      valid4 = valid4 || _valid1;
      const _errs19 = errors;
      if (typeof data2 !== "boolean") {
        const err10 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid1 = _errs19 === errors;
      valid4 = valid4 || _valid1;
      const _errs21 = errors;
      if (typeof data2 === "string") {
        if (!pattern5.test(data2)) {
          const err11 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err11];
          } else {
            vErrors.push(err11);
          }
          errors++;
        }
      } else {
        const err12 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid1 = _errs21 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err13 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
      if (typeof data2 === "string" || typeof data2 === "boolean") {
        if (!Number.isFinite(Number(data2))) {
          const err14 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err14];
          } else {
            vErrors.push(err14);
          }
          errors++;
        }
        if (Number(data2) < 0) {
          const err15 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err15];
          } else {
            vErrors.push(err15);
          }
          errors++;
        }
        if (Number(data2) > 1) {
          const err16 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err16];
          } else {
            vErrors.push(err16);
          }
          errors++;
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
  validate31.errors = vErrors;
  return errors === 0;
}
validate31.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate34(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate34.evaluated;
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
    if (data.include_hidden !== void 0) {
      let data0 = data.include_hidden;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "boolean") {
        const err1 = { instancePath: instancePath + "/include_hidden", schemaPath: "#/properties/include_hidden/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
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
      if (!(typeof data0 == "number")) {
        const err2 = { instancePath: instancePath + "/include_hidden", schemaPath: "#/properties/include_hidden/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (typeof data0 === "string") {
        if (!pattern6.test(data0)) {
          const err3 = { instancePath: instancePath + "/include_hidden", schemaPath: "#/properties/include_hidden/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/include_hidden", schemaPath: "#/properties/include_hidden/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err5 = { instancePath: instancePath + "/include_hidden", schemaPath: "#/properties/include_hidden/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.include_boundaries !== void 0) {
      let data1 = data.include_boundaries;
      const _errs14 = errors;
      let valid4 = false;
      const _errs15 = errors;
      if (typeof data1 !== "boolean") {
        const err6 = { instancePath: instancePath + "/include_boundaries", schemaPath: "#/properties/include_boundaries/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
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
      if (!(typeof data1 == "number")) {
        const err7 = { instancePath: instancePath + "/include_boundaries", schemaPath: "#/properties/include_boundaries/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid1 = _errs17 === errors;
      valid4 = valid4 || _valid1;
      const _errs19 = errors;
      if (typeof data1 === "string") {
        if (!pattern6.test(data1)) {
          const err8 = { instancePath: instancePath + "/include_boundaries", schemaPath: "#/properties/include_boundaries/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err8];
          } else {
            vErrors.push(err8);
          }
          errors++;
        }
      } else {
        const err9 = { instancePath: instancePath + "/include_boundaries", schemaPath: "#/properties/include_boundaries/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid1 = _errs19 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err10 = { instancePath: instancePath + "/include_boundaries", schemaPath: "#/properties/include_boundaries/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
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
    if (data.include_creases !== void 0) {
      let data2 = data.include_creases;
      const _errs22 = errors;
      let valid5 = false;
      const _errs23 = errors;
      if (typeof data2 !== "boolean") {
        const err11 = { instancePath: instancePath + "/include_creases", schemaPath: "#/properties/include_creases/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid2 = _errs23 === errors;
      valid5 = valid5 || _valid2;
      const _errs25 = errors;
      if (!(typeof data2 == "number")) {
        const err12 = { instancePath: instancePath + "/include_creases", schemaPath: "#/properties/include_creases/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid2 = _errs25 === errors;
      valid5 = valid5 || _valid2;
      const _errs27 = errors;
      if (typeof data2 === "string") {
        if (!pattern6.test(data2)) {
          const err13 = { instancePath: instancePath + "/include_creases", schemaPath: "#/properties/include_creases/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err13];
          } else {
            vErrors.push(err13);
          }
          errors++;
        }
      } else {
        const err14 = { instancePath: instancePath + "/include_creases", schemaPath: "#/properties/include_creases/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid2 = _errs27 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err15 = { instancePath: instancePath + "/include_creases", schemaPath: "#/properties/include_creases/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.include_silhouettes !== void 0) {
      let data3 = data.include_silhouettes;
      const _errs30 = errors;
      let valid6 = false;
      const _errs31 = errors;
      if (typeof data3 !== "boolean") {
        const err16 = { instancePath: instancePath + "/include_silhouettes", schemaPath: "#/properties/include_silhouettes/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid3 = _errs31 === errors;
      valid6 = valid6 || _valid3;
      const _errs33 = errors;
      if (!(typeof data3 == "number")) {
        const err17 = { instancePath: instancePath + "/include_silhouettes", schemaPath: "#/properties/include_silhouettes/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      var _valid3 = _errs33 === errors;
      valid6 = valid6 || _valid3;
      const _errs35 = errors;
      if (typeof data3 === "string") {
        if (!pattern6.test(data3)) {
          const err18 = { instancePath: instancePath + "/include_silhouettes", schemaPath: "#/properties/include_silhouettes/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err18];
          } else {
            vErrors.push(err18);
          }
          errors++;
        }
      } else {
        const err19 = { instancePath: instancePath + "/include_silhouettes", schemaPath: "#/properties/include_silhouettes/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
      var _valid3 = _errs35 === errors;
      valid6 = valid6 || _valid3;
      if (!valid6) {
        const err20 = { instancePath: instancePath + "/include_silhouettes", schemaPath: "#/properties/include_silhouettes/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
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
    if (data.suppress_coplanar_seams !== void 0) {
      let data4 = data.suppress_coplanar_seams;
      const _errs38 = errors;
      let valid7 = false;
      const _errs39 = errors;
      if (typeof data4 !== "boolean") {
        const err21 = { instancePath: instancePath + "/suppress_coplanar_seams", schemaPath: "#/properties/suppress_coplanar_seams/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      var _valid4 = _errs39 === errors;
      valid7 = valid7 || _valid4;
      const _errs41 = errors;
      if (!(typeof data4 == "number")) {
        const err22 = { instancePath: instancePath + "/suppress_coplanar_seams", schemaPath: "#/properties/suppress_coplanar_seams/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
      var _valid4 = _errs41 === errors;
      valid7 = valid7 || _valid4;
      const _errs43 = errors;
      if (typeof data4 === "string") {
        if (!pattern6.test(data4)) {
          const err23 = { instancePath: instancePath + "/suppress_coplanar_seams", schemaPath: "#/properties/suppress_coplanar_seams/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err23];
          } else {
            vErrors.push(err23);
          }
          errors++;
        }
      } else {
        const err24 = { instancePath: instancePath + "/suppress_coplanar_seams", schemaPath: "#/properties/suppress_coplanar_seams/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      var _valid4 = _errs43 === errors;
      valid7 = valid7 || _valid4;
      if (!valid7) {
        const err25 = { instancePath: instancePath + "/suppress_coplanar_seams", schemaPath: "#/properties/suppress_coplanar_seams/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
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
  } else {
    const err26 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err26];
    } else {
      vErrors.push(err26);
    }
    errors++;
  }
  validate34.errors = vErrors;
  return errors === 0;
}
validate34.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.projection_algorithm !== void 0) {
      let data0 = data.projection_algorithm;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err1 = { instancePath: instancePath + "/projection_algorithm", schemaPath: "#/properties/projection_algorithm/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      if ("fast" !== data0) {
        const err2 = { instancePath: instancePath + "/projection_algorithm", schemaPath: "#/properties/projection_algorithm/anyOf/0/const", keyword: "const", params: { allowedValue: "fast" }, message: "must be equal to constant" };
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
        const err3 = { instancePath: instancePath + "/projection_algorithm", schemaPath: "#/properties/projection_algorithm/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      if ("poly" !== data0) {
        const err4 = { instancePath: instancePath + "/projection_algorithm", schemaPath: "#/properties/projection_algorithm/anyOf/1/const", keyword: "const", params: { allowedValue: "poly" }, message: "must be equal to constant" };
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
        const err5 = { instancePath: instancePath + "/projection_algorithm", schemaPath: "#/properties/projection_algorithm/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      if ("exact" !== data0) {
        const err6 = { instancePath: instancePath + "/projection_algorithm", schemaPath: "#/properties/projection_algorithm/anyOf/2/const", keyword: "const", params: { allowedValue: "exact" }, message: "must be equal to constant" };
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
        const err7 = { instancePath: instancePath + "/projection_algorithm", schemaPath: "#/properties/projection_algorithm/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
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
    if (data.outline_algorithm !== void 0) {
      let data1 = data.outline_algorithm;
      const _errs14 = errors;
      let valid4 = false;
      const _errs15 = errors;
      if (typeof data1 !== "string") {
        const err8 = { instancePath: instancePath + "/outline_algorithm", schemaPath: "#/properties/outline_algorithm/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      if ("fast-mesh-shadow" !== data1) {
        const err9 = { instancePath: instancePath + "/outline_algorithm", schemaPath: "#/properties/outline_algorithm/anyOf/0/const", keyword: "const", params: { allowedValue: "fast-mesh-shadow" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      valid4 = valid4 || _valid1;
      const _errs17 = errors;
      if (typeof data1 !== "string") {
        const err10 = { instancePath: instancePath + "/outline_algorithm", schemaPath: "#/properties/outline_algorithm/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      if ("mesh-shadow" !== data1) {
        const err11 = { instancePath: instancePath + "/outline_algorithm", schemaPath: "#/properties/outline_algorithm/anyOf/1/const", keyword: "const", params: { allowedValue: "mesh-shadow" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid1 = _errs17 === errors;
      valid4 = valid4 || _valid1;
      const _errs19 = errors;
      if (typeof data1 !== "string") {
        const err12 = { instancePath: instancePath + "/outline_algorithm", schemaPath: "#/properties/outline_algorithm/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("hlr-close" !== data1) {
        const err13 = { instancePath: instancePath + "/outline_algorithm", schemaPath: "#/properties/outline_algorithm/anyOf/2/const", keyword: "const", params: { allowedValue: "hlr-close" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid1 = _errs19 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err14 = { instancePath: instancePath + "/outline_algorithm", schemaPath: "#/properties/outline_algorithm/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
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
    if (data.fast !== void 0) {
      if (!validate34(data.fast, { instancePath: instancePath + "/fast", parentData: data, parentDataProperty: "fast", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate34.errors : vErrors.concat(validate34.errors);
        errors = vErrors.length;
      }
    }
    if (data.enabled !== void 0) {
      let data3 = data.enabled;
      const _errs23 = errors;
      let valid5 = false;
      const _errs24 = errors;
      if (typeof data3 !== "boolean") {
        const err15 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid2 = _errs24 === errors;
      valid5 = valid5 || _valid2;
      const _errs26 = errors;
      if (!(typeof data3 == "number")) {
        const err16 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid2 = _errs26 === errors;
      valid5 = valid5 || _valid2;
      const _errs28 = errors;
      if (typeof data3 === "string") {
        if (!pattern6.test(data3)) {
          const err17 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err17];
          } else {
            vErrors.push(err17);
          }
          errors++;
        }
      } else {
        const err18 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
      var _valid2 = _errs28 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err19 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
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
    if (data.color !== void 0) {
      if (typeof data.color !== "string") {
        const err20 = { instancePath: instancePath + "/color", schemaPath: "#/properties/color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
    }
    if (data.line_width_mm !== void 0) {
      let data5 = data.line_width_mm;
      const _errs33 = errors;
      let valid6 = false;
      const _errs34 = errors;
      if (!(typeof data5 == "number")) {
        const err21 = { instancePath: instancePath + "/line_width_mm", schemaPath: "#/properties/line_width_mm/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      var _valid3 = _errs34 === errors;
      valid6 = valid6 || _valid3;
      const _errs36 = errors;
      if (typeof data5 !== "boolean") {
        const err22 = { instancePath: instancePath + "/line_width_mm", schemaPath: "#/properties/line_width_mm/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
      var _valid3 = _errs36 === errors;
      valid6 = valid6 || _valid3;
      const _errs38 = errors;
      if (typeof data5 === "string") {
        if (!pattern5.test(data5)) {
          const err23 = { instancePath: instancePath + "/line_width_mm", schemaPath: "#/properties/line_width_mm/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err23];
          } else {
            vErrors.push(err23);
          }
          errors++;
        }
      } else {
        const err24 = { instancePath: instancePath + "/line_width_mm", schemaPath: "#/properties/line_width_mm/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      var _valid3 = _errs38 === errors;
      valid6 = valid6 || _valid3;
      if (!valid6) {
        const err25 = { instancePath: instancePath + "/line_width_mm", schemaPath: "#/properties/line_width_mm/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
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
      if (typeof data5 === "string" || typeof data5 === "boolean") {
        if (!Number.isFinite(Number(data5))) {
          const err26 = { instancePath: instancePath + "/line_width_mm", schemaPath: "#/properties/line_width_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err26];
          } else {
            vErrors.push(err26);
          }
          errors++;
        }
      }
    }
    if (data.curve_mode !== void 0) {
      if (typeof data.curve_mode !== "string") {
        const err27 = { instancePath: instancePath + "/curve_mode", schemaPath: "#/properties/curve_mode/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
    }
    if (data.samples_per_curve !== void 0) {
      let data7 = data.samples_per_curve;
      const _errs43 = errors;
      let valid7 = false;
      const _errs44 = errors;
      if (!(typeof data7 == "number")) {
        const err28 = { instancePath: instancePath + "/samples_per_curve", schemaPath: "#/properties/samples_per_curve/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
      var _valid4 = _errs44 === errors;
      valid7 = valid7 || _valid4;
      const _errs46 = errors;
      if (typeof data7 !== "boolean") {
        const err29 = { instancePath: instancePath + "/samples_per_curve", schemaPath: "#/properties/samples_per_curve/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      }
      var _valid4 = _errs46 === errors;
      valid7 = valid7 || _valid4;
      const _errs48 = errors;
      if (typeof data7 === "string") {
        if (!pattern5.test(data7)) {
          const err30 = { instancePath: instancePath + "/samples_per_curve", schemaPath: "#/properties/samples_per_curve/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err30];
          } else {
            vErrors.push(err30);
          }
          errors++;
        }
      } else {
        const err31 = { instancePath: instancePath + "/samples_per_curve", schemaPath: "#/properties/samples_per_curve/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      }
      var _valid4 = _errs48 === errors;
      valid7 = valid7 || _valid4;
      if (!valid7) {
        const err32 = { instancePath: instancePath + "/samples_per_curve", schemaPath: "#/properties/samples_per_curve/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
        }
        errors++;
      } else {
        errors = _errs43;
        if (vErrors !== null) {
          if (_errs43) {
            vErrors.length = _errs43;
          } else {
            vErrors = null;
          }
        }
      }
      if (typeof data7 === "string" || typeof data7 === "boolean") {
        if (!Number.isFinite(Number(data7))) {
          const err33 = { instancePath: instancePath + "/samples_per_curve", schemaPath: "#/properties/samples_per_curve/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err33];
          } else {
            vErrors.push(err33);
          }
          errors++;
        }
      }
    }
    if (data.round_digits !== void 0) {
      let data8 = data.round_digits;
      const _errs51 = errors;
      let valid8 = false;
      const _errs52 = errors;
      if (!(typeof data8 == "number")) {
        const err34 = { instancePath: instancePath + "/round_digits", schemaPath: "#/properties/round_digits/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
        }
        errors++;
      }
      var _valid5 = _errs52 === errors;
      valid8 = valid8 || _valid5;
      const _errs54 = errors;
      if (typeof data8 !== "boolean") {
        const err35 = { instancePath: instancePath + "/round_digits", schemaPath: "#/properties/round_digits/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err35];
        } else {
          vErrors.push(err35);
        }
        errors++;
      }
      var _valid5 = _errs54 === errors;
      valid8 = valid8 || _valid5;
      const _errs56 = errors;
      if (typeof data8 === "string") {
        if (!pattern5.test(data8)) {
          const err36 = { instancePath: instancePath + "/round_digits", schemaPath: "#/properties/round_digits/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err36];
          } else {
            vErrors.push(err36);
          }
          errors++;
        }
      } else {
        const err37 = { instancePath: instancePath + "/round_digits", schemaPath: "#/properties/round_digits/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err37];
        } else {
          vErrors.push(err37);
        }
        errors++;
      }
      var _valid5 = _errs56 === errors;
      valid8 = valid8 || _valid5;
      if (!valid8) {
        const err38 = { instancePath: instancePath + "/round_digits", schemaPath: "#/properties/round_digits/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err38];
        } else {
          vErrors.push(err38);
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
      if (typeof data8 === "string" || typeof data8 === "boolean") {
        if (!Number.isFinite(Number(data8))) {
          const err39 = { instancePath: instancePath + "/round_digits", schemaPath: "#/properties/round_digits/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err39];
          } else {
            vErrors.push(err39);
          }
          errors++;
        }
      }
    }
    if (data.include_visible !== void 0) {
      let data9 = data.include_visible;
      const _errs59 = errors;
      let valid9 = false;
      const _errs60 = errors;
      if (typeof data9 !== "boolean") {
        const err40 = { instancePath: instancePath + "/include_visible", schemaPath: "#/properties/include_visible/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err40];
        } else {
          vErrors.push(err40);
        }
        errors++;
      }
      var _valid6 = _errs60 === errors;
      valid9 = valid9 || _valid6;
      const _errs62 = errors;
      if (!(typeof data9 == "number")) {
        const err41 = { instancePath: instancePath + "/include_visible", schemaPath: "#/properties/include_visible/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err41];
        } else {
          vErrors.push(err41);
        }
        errors++;
      }
      var _valid6 = _errs62 === errors;
      valid9 = valid9 || _valid6;
      const _errs64 = errors;
      if (typeof data9 === "string") {
        if (!pattern6.test(data9)) {
          const err42 = { instancePath: instancePath + "/include_visible", schemaPath: "#/properties/include_visible/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err42];
          } else {
            vErrors.push(err42);
          }
          errors++;
        }
      } else {
        const err43 = { instancePath: instancePath + "/include_visible", schemaPath: "#/properties/include_visible/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err43];
        } else {
          vErrors.push(err43);
        }
        errors++;
      }
      var _valid6 = _errs64 === errors;
      valid9 = valid9 || _valid6;
      if (!valid9) {
        const err44 = { instancePath: instancePath + "/include_visible", schemaPath: "#/properties/include_visible/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err44];
        } else {
          vErrors.push(err44);
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
    if (data.include_outline !== void 0) {
      let data10 = data.include_outline;
      const _errs67 = errors;
      let valid10 = false;
      const _errs68 = errors;
      if (typeof data10 !== "boolean") {
        const err45 = { instancePath: instancePath + "/include_outline", schemaPath: "#/properties/include_outline/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err45];
        } else {
          vErrors.push(err45);
        }
        errors++;
      }
      var _valid7 = _errs68 === errors;
      valid10 = valid10 || _valid7;
      const _errs70 = errors;
      if (!(typeof data10 == "number")) {
        const err46 = { instancePath: instancePath + "/include_outline", schemaPath: "#/properties/include_outline/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err46];
        } else {
          vErrors.push(err46);
        }
        errors++;
      }
      var _valid7 = _errs70 === errors;
      valid10 = valid10 || _valid7;
      const _errs72 = errors;
      if (typeof data10 === "string") {
        if (!pattern6.test(data10)) {
          const err47 = { instancePath: instancePath + "/include_outline", schemaPath: "#/properties/include_outline/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err47];
          } else {
            vErrors.push(err47);
          }
          errors++;
        }
      } else {
        const err48 = { instancePath: instancePath + "/include_outline", schemaPath: "#/properties/include_outline/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err48];
        } else {
          vErrors.push(err48);
        }
        errors++;
      }
      var _valid7 = _errs72 === errors;
      valid10 = valid10 || _valid7;
      if (!valid10) {
        const err49 = { instancePath: instancePath + "/include_outline", schemaPath: "#/properties/include_outline/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err49];
        } else {
          vErrors.push(err49);
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
    if (data.union_polygons !== void 0) {
      let data11 = data.union_polygons;
      const _errs75 = errors;
      let valid11 = false;
      const _errs76 = errors;
      if (typeof data11 !== "boolean") {
        const err50 = { instancePath: instancePath + "/union_polygons", schemaPath: "#/properties/union_polygons/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err50];
        } else {
          vErrors.push(err50);
        }
        errors++;
      }
      var _valid8 = _errs76 === errors;
      valid11 = valid11 || _valid8;
      const _errs78 = errors;
      if (!(typeof data11 == "number")) {
        const err51 = { instancePath: instancePath + "/union_polygons", schemaPath: "#/properties/union_polygons/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err51];
        } else {
          vErrors.push(err51);
        }
        errors++;
      }
      var _valid8 = _errs78 === errors;
      valid11 = valid11 || _valid8;
      const _errs80 = errors;
      if (typeof data11 === "string") {
        if (!pattern6.test(data11)) {
          const err52 = { instancePath: instancePath + "/union_polygons", schemaPath: "#/properties/union_polygons/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err52];
          } else {
            vErrors.push(err52);
          }
          errors++;
        }
      } else {
        const err53 = { instancePath: instancePath + "/union_polygons", schemaPath: "#/properties/union_polygons/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err53];
        } else {
          vErrors.push(err53);
        }
        errors++;
      }
      var _valid8 = _errs80 === errors;
      valid11 = valid11 || _valid8;
      if (!valid11) {
        const err54 = { instancePath: instancePath + "/union_polygons", schemaPath: "#/properties/union_polygons/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err54];
        } else {
          vErrors.push(err54);
        }
        errors++;
      } else {
        errors = _errs75;
        if (vErrors !== null) {
          if (_errs75) {
            vErrors.length = _errs75;
          } else {
            vErrors = null;
          }
        }
      }
    }
  } else {
    const err55 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err55];
    } else {
      vErrors.push(err55);
    }
    errors++;
  }
  validate33.errors = vErrors;
  return errors === 0;
}
validate33.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
      if (!(typeof data0 == "number")) {
        const err2 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (typeof data0 === "string") {
        if (!pattern6.test(data0)) {
          const err3 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err5 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.color !== void 0) {
      if (typeof data.color !== "string") {
        const err6 = { instancePath: instancePath + "/color", schemaPath: "#/properties/color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.line_width_mm !== void 0) {
      let data2 = data.line_width_mm;
      const _errs16 = errors;
      let valid4 = false;
      const _errs17 = errors;
      if (typeof data2 == "number") {
        if (data2 <= 0 || isNaN(data2)) {
          const err7 = { instancePath: instancePath + "/line_width_mm", schemaPath: "#/properties/line_width_mm/anyOf/0/exclusiveMinimum", keyword: "exclusiveMinimum", params: { comparison: ">", limit: 0 }, message: "must be > 0" };
          if (vErrors === null) {
            vErrors = [err7];
          } else {
            vErrors.push(err7);
          }
          errors++;
        }
      } else {
        const err8 = { instancePath: instancePath + "/line_width_mm", schemaPath: "#/properties/line_width_mm/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid1 = _errs17 === errors;
      valid4 = valid4 || _valid1;
      const _errs19 = errors;
      if (typeof data2 !== "boolean") {
        const err9 = { instancePath: instancePath + "/line_width_mm", schemaPath: "#/properties/line_width_mm/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid1 = _errs19 === errors;
      valid4 = valid4 || _valid1;
      const _errs21 = errors;
      if (typeof data2 === "string") {
        if (!pattern5.test(data2)) {
          const err10 = { instancePath: instancePath + "/line_width_mm", schemaPath: "#/properties/line_width_mm/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err10];
          } else {
            vErrors.push(err10);
          }
          errors++;
        }
      } else {
        const err11 = { instancePath: instancePath + "/line_width_mm", schemaPath: "#/properties/line_width_mm/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid1 = _errs21 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err12 = { instancePath: instancePath + "/line_width_mm", schemaPath: "#/properties/line_width_mm/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
      if (typeof data2 === "string" || typeof data2 === "boolean") {
        if (!Number.isFinite(Number(data2))) {
          const err13 = { instancePath: instancePath + "/line_width_mm", schemaPath: "#/properties/line_width_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err13];
          } else {
            vErrors.push(err13);
          }
          errors++;
        }
        if (Number(data2) <= 0) {
          const err14 = { instancePath: instancePath + "/line_width_mm", schemaPath: "#/properties/line_width_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err14];
          } else {
            vErrors.push(err14);
          }
          errors++;
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
  validate37.errors = vErrors;
  return errors === 0;
}
validate37.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
var pattern49 = new RegExp("^(?:[sS][oO][lL][iI][dD]|[dD][aA][sS][hH][eE][dD])$", "u");
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
      if (!(typeof data0 == "number")) {
        const err2 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (typeof data0 === "string") {
        if (!pattern6.test(data0)) {
          const err3 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err5 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.scope !== void 0) {
      let data1 = data.scope;
      const _errs14 = errors;
      let valid4 = false;
      const _errs15 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/scope", schemaPath: "#/properties/scope/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      if ("all" !== data1) {
        const err7 = { instancePath: instancePath + "/scope", schemaPath: "#/properties/scope/anyOf/0/const", keyword: "const", params: { allowedValue: "all" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      valid4 = valid4 || _valid1;
      const _errs17 = errors;
      if (typeof data1 !== "string") {
        const err8 = { instancePath: instancePath + "/scope", schemaPath: "#/properties/scope/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      if ("interior" !== data1) {
        const err9 = { instancePath: instancePath + "/scope", schemaPath: "#/properties/scope/anyOf/1/const", keyword: "const", params: { allowedValue: "interior" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid1 = _errs17 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err10 = { instancePath: instancePath + "/scope", schemaPath: "#/properties/scope/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
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
    if (data.outline_opacity !== void 0) {
      let data2 = data.outline_opacity;
      const _errs20 = errors;
      let valid5 = false;
      const _errs21 = errors;
      if (typeof data2 == "number") {
        if (data2 > 1 || isNaN(data2)) {
          const err11 = { instancePath: instancePath + "/outline_opacity", schemaPath: "#/properties/outline_opacity/anyOf/0/maximum", keyword: "maximum", params: { comparison: "<=", limit: 1 }, message: "must be <= 1" };
          if (vErrors === null) {
            vErrors = [err11];
          } else {
            vErrors.push(err11);
          }
          errors++;
        }
        if (data2 < 0 || isNaN(data2)) {
          const err12 = { instancePath: instancePath + "/outline_opacity", schemaPath: "#/properties/outline_opacity/anyOf/0/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err12];
          } else {
            vErrors.push(err12);
          }
          errors++;
        }
      } else {
        const err13 = { instancePath: instancePath + "/outline_opacity", schemaPath: "#/properties/outline_opacity/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      const _errs23 = errors;
      if (typeof data2 !== "boolean") {
        const err14 = { instancePath: instancePath + "/outline_opacity", schemaPath: "#/properties/outline_opacity/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid2 = _errs23 === errors;
      valid5 = valid5 || _valid2;
      const _errs25 = errors;
      if (typeof data2 === "string") {
        if (!pattern5.test(data2)) {
          const err15 = { instancePath: instancePath + "/outline_opacity", schemaPath: "#/properties/outline_opacity/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err15];
          } else {
            vErrors.push(err15);
          }
          errors++;
        }
      } else {
        const err16 = { instancePath: instancePath + "/outline_opacity", schemaPath: "#/properties/outline_opacity/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid2 = _errs25 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err17 = { instancePath: instancePath + "/outline_opacity", schemaPath: "#/properties/outline_opacity/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
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
      if (typeof data2 === "string" || typeof data2 === "boolean") {
        if (!Number.isFinite(Number(data2))) {
          const err18 = { instancePath: instancePath + "/outline_opacity", schemaPath: "#/properties/outline_opacity/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err18];
          } else {
            vErrors.push(err18);
          }
          errors++;
        }
        if (Number(data2) < 0) {
          const err19 = { instancePath: instancePath + "/outline_opacity", schemaPath: "#/properties/outline_opacity/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err19];
          } else {
            vErrors.push(err19);
          }
          errors++;
        }
        if (Number(data2) > 1) {
          const err20 = { instancePath: instancePath + "/outline_opacity", schemaPath: "#/properties/outline_opacity/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err20];
          } else {
            vErrors.push(err20);
          }
          errors++;
        }
      }
    }
    if (data.hatch_color !== void 0) {
      if (typeof data.hatch_color !== "string") {
        const err21 = { instancePath: instancePath + "/hatch_color", schemaPath: "#/properties/hatch_color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
    }
    if (data.hatch_opacity !== void 0) {
      let data4 = data.hatch_opacity;
      const _errs30 = errors;
      let valid6 = false;
      const _errs31 = errors;
      if (typeof data4 == "number") {
        if (data4 > 1 || isNaN(data4)) {
          const err22 = { instancePath: instancePath + "/hatch_opacity", schemaPath: "#/properties/hatch_opacity/anyOf/0/maximum", keyword: "maximum", params: { comparison: "<=", limit: 1 }, message: "must be <= 1" };
          if (vErrors === null) {
            vErrors = [err22];
          } else {
            vErrors.push(err22);
          }
          errors++;
        }
        if (data4 < 0 || isNaN(data4)) {
          const err23 = { instancePath: instancePath + "/hatch_opacity", schemaPath: "#/properties/hatch_opacity/anyOf/0/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err23];
          } else {
            vErrors.push(err23);
          }
          errors++;
        }
      } else {
        const err24 = { instancePath: instancePath + "/hatch_opacity", schemaPath: "#/properties/hatch_opacity/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      var _valid3 = _errs31 === errors;
      valid6 = valid6 || _valid3;
      const _errs33 = errors;
      if (typeof data4 !== "boolean") {
        const err25 = { instancePath: instancePath + "/hatch_opacity", schemaPath: "#/properties/hatch_opacity/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
      var _valid3 = _errs33 === errors;
      valid6 = valid6 || _valid3;
      const _errs35 = errors;
      if (typeof data4 === "string") {
        if (!pattern5.test(data4)) {
          const err26 = { instancePath: instancePath + "/hatch_opacity", schemaPath: "#/properties/hatch_opacity/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err26];
          } else {
            vErrors.push(err26);
          }
          errors++;
        }
      } else {
        const err27 = { instancePath: instancePath + "/hatch_opacity", schemaPath: "#/properties/hatch_opacity/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
      var _valid3 = _errs35 === errors;
      valid6 = valid6 || _valid3;
      if (!valid6) {
        const err28 = { instancePath: instancePath + "/hatch_opacity", schemaPath: "#/properties/hatch_opacity/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
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
      if (typeof data4 === "string" || typeof data4 === "boolean") {
        if (!Number.isFinite(Number(data4))) {
          const err29 = { instancePath: instancePath + "/hatch_opacity", schemaPath: "#/properties/hatch_opacity/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err29];
          } else {
            vErrors.push(err29);
          }
          errors++;
        }
        if (Number(data4) < 0) {
          const err30 = { instancePath: instancePath + "/hatch_opacity", schemaPath: "#/properties/hatch_opacity/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err30];
          } else {
            vErrors.push(err30);
          }
          errors++;
        }
        if (Number(data4) > 1) {
          const err31 = { instancePath: instancePath + "/hatch_opacity", schemaPath: "#/properties/hatch_opacity/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err31];
          } else {
            vErrors.push(err31);
          }
          errors++;
        }
      }
    }
    if (data.label !== void 0) {
      if (typeof data.label !== "string") {
        const err32 = { instancePath: instancePath + "/label", schemaPath: "#/properties/label/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
        }
        errors++;
      }
    }
    if (data.label_color !== void 0) {
      if (typeof data.label_color !== "string") {
        const err33 = { instancePath: instancePath + "/label_color", schemaPath: "#/properties/label_color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
    }
    if (data.label_opacity !== void 0) {
      let data7 = data.label_opacity;
      const _errs42 = errors;
      let valid7 = false;
      const _errs43 = errors;
      if (typeof data7 == "number") {
        if (data7 > 1 || isNaN(data7)) {
          const err34 = { instancePath: instancePath + "/label_opacity", schemaPath: "#/properties/label_opacity/anyOf/0/maximum", keyword: "maximum", params: { comparison: "<=", limit: 1 }, message: "must be <= 1" };
          if (vErrors === null) {
            vErrors = [err34];
          } else {
            vErrors.push(err34);
          }
          errors++;
        }
        if (data7 < 0 || isNaN(data7)) {
          const err35 = { instancePath: instancePath + "/label_opacity", schemaPath: "#/properties/label_opacity/anyOf/0/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err35];
          } else {
            vErrors.push(err35);
          }
          errors++;
        }
      } else {
        const err36 = { instancePath: instancePath + "/label_opacity", schemaPath: "#/properties/label_opacity/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err36];
        } else {
          vErrors.push(err36);
        }
        errors++;
      }
      var _valid4 = _errs43 === errors;
      valid7 = valid7 || _valid4;
      const _errs45 = errors;
      if (typeof data7 !== "boolean") {
        const err37 = { instancePath: instancePath + "/label_opacity", schemaPath: "#/properties/label_opacity/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err37];
        } else {
          vErrors.push(err37);
        }
        errors++;
      }
      var _valid4 = _errs45 === errors;
      valid7 = valid7 || _valid4;
      const _errs47 = errors;
      if (typeof data7 === "string") {
        if (!pattern5.test(data7)) {
          const err38 = { instancePath: instancePath + "/label_opacity", schemaPath: "#/properties/label_opacity/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err38];
          } else {
            vErrors.push(err38);
          }
          errors++;
        }
      } else {
        const err39 = { instancePath: instancePath + "/label_opacity", schemaPath: "#/properties/label_opacity/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err39];
        } else {
          vErrors.push(err39);
        }
        errors++;
      }
      var _valid4 = _errs47 === errors;
      valid7 = valid7 || _valid4;
      if (!valid7) {
        const err40 = { instancePath: instancePath + "/label_opacity", schemaPath: "#/properties/label_opacity/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err40];
        } else {
          vErrors.push(err40);
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
      if (typeof data7 === "string" || typeof data7 === "boolean") {
        if (!Number.isFinite(Number(data7))) {
          const err41 = { instancePath: instancePath + "/label_opacity", schemaPath: "#/properties/label_opacity/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err41];
          } else {
            vErrors.push(err41);
          }
          errors++;
        }
        if (Number(data7) < 0) {
          const err42 = { instancePath: instancePath + "/label_opacity", schemaPath: "#/properties/label_opacity/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err42];
          } else {
            vErrors.push(err42);
          }
          errors++;
        }
        if (Number(data7) > 1) {
          const err43 = { instancePath: instancePath + "/label_opacity", schemaPath: "#/properties/label_opacity/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err43];
          } else {
            vErrors.push(err43);
          }
          errors++;
        }
      }
    }
    if (data.label_max_font_size_mm !== void 0) {
      let data8 = data.label_max_font_size_mm;
      const _errs50 = errors;
      let valid8 = false;
      const _errs51 = errors;
      if (typeof data8 == "number") {
        if (data8 <= 0 || isNaN(data8)) {
          const err44 = { instancePath: instancePath + "/label_max_font_size_mm", schemaPath: "#/properties/label_max_font_size_mm/anyOf/0/exclusiveMinimum", keyword: "exclusiveMinimum", params: { comparison: ">", limit: 0 }, message: "must be > 0" };
          if (vErrors === null) {
            vErrors = [err44];
          } else {
            vErrors.push(err44);
          }
          errors++;
        }
      } else {
        const err45 = { instancePath: instancePath + "/label_max_font_size_mm", schemaPath: "#/properties/label_max_font_size_mm/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err45];
        } else {
          vErrors.push(err45);
        }
        errors++;
      }
      var _valid5 = _errs51 === errors;
      valid8 = valid8 || _valid5;
      const _errs53 = errors;
      if (typeof data8 !== "boolean") {
        const err46 = { instancePath: instancePath + "/label_max_font_size_mm", schemaPath: "#/properties/label_max_font_size_mm/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err46];
        } else {
          vErrors.push(err46);
        }
        errors++;
      }
      var _valid5 = _errs53 === errors;
      valid8 = valid8 || _valid5;
      const _errs55 = errors;
      if (typeof data8 === "string") {
        if (!pattern5.test(data8)) {
          const err47 = { instancePath: instancePath + "/label_max_font_size_mm", schemaPath: "#/properties/label_max_font_size_mm/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err47];
          } else {
            vErrors.push(err47);
          }
          errors++;
        }
      } else {
        const err48 = { instancePath: instancePath + "/label_max_font_size_mm", schemaPath: "#/properties/label_max_font_size_mm/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err48];
        } else {
          vErrors.push(err48);
        }
        errors++;
      }
      var _valid5 = _errs55 === errors;
      valid8 = valid8 || _valid5;
      if (!valid8) {
        const err49 = { instancePath: instancePath + "/label_max_font_size_mm", schemaPath: "#/properties/label_max_font_size_mm/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err49];
        } else {
          vErrors.push(err49);
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
      if (typeof data8 === "string" || typeof data8 === "boolean") {
        if (!Number.isFinite(Number(data8))) {
          const err50 = { instancePath: instancePath + "/label_max_font_size_mm", schemaPath: "#/properties/label_max_font_size_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err50];
          } else {
            vErrors.push(err50);
          }
          errors++;
        }
        if (Number(data8) <= 0) {
          const err51 = { instancePath: instancePath + "/label_max_font_size_mm", schemaPath: "#/properties/label_max_font_size_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err51];
          } else {
            vErrors.push(err51);
          }
          errors++;
        }
      }
    }
    if (data.label_fill_ratio !== void 0) {
      let data9 = data.label_fill_ratio;
      const _errs58 = errors;
      let valid9 = false;
      const _errs59 = errors;
      if (typeof data9 == "number") {
        if (data9 > 1 || isNaN(data9)) {
          const err52 = { instancePath: instancePath + "/label_fill_ratio", schemaPath: "#/properties/label_fill_ratio/anyOf/0/maximum", keyword: "maximum", params: { comparison: "<=", limit: 1 }, message: "must be <= 1" };
          if (vErrors === null) {
            vErrors = [err52];
          } else {
            vErrors.push(err52);
          }
          errors++;
        }
        if (data9 <= 0 || isNaN(data9)) {
          const err53 = { instancePath: instancePath + "/label_fill_ratio", schemaPath: "#/properties/label_fill_ratio/anyOf/0/exclusiveMinimum", keyword: "exclusiveMinimum", params: { comparison: ">", limit: 0 }, message: "must be > 0" };
          if (vErrors === null) {
            vErrors = [err53];
          } else {
            vErrors.push(err53);
          }
          errors++;
        }
      } else {
        const err54 = { instancePath: instancePath + "/label_fill_ratio", schemaPath: "#/properties/label_fill_ratio/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err54];
        } else {
          vErrors.push(err54);
        }
        errors++;
      }
      var _valid6 = _errs59 === errors;
      valid9 = valid9 || _valid6;
      const _errs61 = errors;
      if (typeof data9 !== "boolean") {
        const err55 = { instancePath: instancePath + "/label_fill_ratio", schemaPath: "#/properties/label_fill_ratio/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err55];
        } else {
          vErrors.push(err55);
        }
        errors++;
      }
      var _valid6 = _errs61 === errors;
      valid9 = valid9 || _valid6;
      const _errs63 = errors;
      if (typeof data9 === "string") {
        if (!pattern5.test(data9)) {
          const err56 = { instancePath: instancePath + "/label_fill_ratio", schemaPath: "#/properties/label_fill_ratio/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err56];
          } else {
            vErrors.push(err56);
          }
          errors++;
        }
      } else {
        const err57 = { instancePath: instancePath + "/label_fill_ratio", schemaPath: "#/properties/label_fill_ratio/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err57];
        } else {
          vErrors.push(err57);
        }
        errors++;
      }
      var _valid6 = _errs63 === errors;
      valid9 = valid9 || _valid6;
      if (!valid9) {
        const err58 = { instancePath: instancePath + "/label_fill_ratio", schemaPath: "#/properties/label_fill_ratio/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err58];
        } else {
          vErrors.push(err58);
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
      if (typeof data9 === "string" || typeof data9 === "boolean") {
        if (!Number.isFinite(Number(data9))) {
          const err59 = { instancePath: instancePath + "/label_fill_ratio", schemaPath: "#/properties/label_fill_ratio/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err59];
          } else {
            vErrors.push(err59);
          }
          errors++;
        }
        if (Number(data9) > 1) {
          const err60 = { instancePath: instancePath + "/label_fill_ratio", schemaPath: "#/properties/label_fill_ratio/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err60];
          } else {
            vErrors.push(err60);
          }
          errors++;
        }
        if (Number(data9) <= 0) {
          const err61 = { instancePath: instancePath + "/label_fill_ratio", schemaPath: "#/properties/label_fill_ratio/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err61];
          } else {
            vErrors.push(err61);
          }
          errors++;
        }
      }
    }
    if (data.label_rotation_min_gain !== void 0) {
      let data10 = data.label_rotation_min_gain;
      const _errs66 = errors;
      let valid10 = false;
      const _errs67 = errors;
      if (typeof data10 == "number") {
        if (data10 < 0 || isNaN(data10)) {
          const err62 = { instancePath: instancePath + "/label_rotation_min_gain", schemaPath: "#/properties/label_rotation_min_gain/anyOf/0/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err62];
          } else {
            vErrors.push(err62);
          }
          errors++;
        }
      } else {
        const err63 = { instancePath: instancePath + "/label_rotation_min_gain", schemaPath: "#/properties/label_rotation_min_gain/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err63];
        } else {
          vErrors.push(err63);
        }
        errors++;
      }
      var _valid7 = _errs67 === errors;
      valid10 = valid10 || _valid7;
      const _errs69 = errors;
      if (typeof data10 !== "boolean") {
        const err64 = { instancePath: instancePath + "/label_rotation_min_gain", schemaPath: "#/properties/label_rotation_min_gain/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err64];
        } else {
          vErrors.push(err64);
        }
        errors++;
      }
      var _valid7 = _errs69 === errors;
      valid10 = valid10 || _valid7;
      const _errs71 = errors;
      if (typeof data10 === "string") {
        if (!pattern5.test(data10)) {
          const err65 = { instancePath: instancePath + "/label_rotation_min_gain", schemaPath: "#/properties/label_rotation_min_gain/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err65];
          } else {
            vErrors.push(err65);
          }
          errors++;
        }
      } else {
        const err66 = { instancePath: instancePath + "/label_rotation_min_gain", schemaPath: "#/properties/label_rotation_min_gain/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err66];
        } else {
          vErrors.push(err66);
        }
        errors++;
      }
      var _valid7 = _errs71 === errors;
      valid10 = valid10 || _valid7;
      if (!valid10) {
        const err67 = { instancePath: instancePath + "/label_rotation_min_gain", schemaPath: "#/properties/label_rotation_min_gain/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err67];
        } else {
          vErrors.push(err67);
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
      if (typeof data10 === "string" || typeof data10 === "boolean") {
        if (!Number.isFinite(Number(data10))) {
          const err68 = { instancePath: instancePath + "/label_rotation_min_gain", schemaPath: "#/properties/label_rotation_min_gain/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err68];
          } else {
            vErrors.push(err68);
          }
          errors++;
        }
        if (Number(data10) < 0) {
          const err69 = { instancePath: instancePath + "/label_rotation_min_gain", schemaPath: "#/properties/label_rotation_min_gain/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err69];
          } else {
            vErrors.push(err69);
          }
          errors++;
        }
      }
    }
    if (data.color !== void 0) {
      if (typeof data.color !== "string") {
        const err70 = { instancePath: instancePath + "/color", schemaPath: "#/properties/color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err70];
        } else {
          vErrors.push(err70);
        }
        errors++;
      }
    }
    if (data.hatch !== void 0) {
      let data12 = data.hatch;
      const _errs76 = errors;
      let valid11 = false;
      const _errs77 = errors;
      if (typeof data12 !== "boolean") {
        const err71 = { instancePath: instancePath + "/hatch", schemaPath: "#/properties/hatch/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err71];
        } else {
          vErrors.push(err71);
        }
        errors++;
      }
      var _valid8 = _errs77 === errors;
      valid11 = valid11 || _valid8;
      const _errs79 = errors;
      if (!(typeof data12 == "number")) {
        const err72 = { instancePath: instancePath + "/hatch", schemaPath: "#/properties/hatch/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err72];
        } else {
          vErrors.push(err72);
        }
        errors++;
      }
      var _valid8 = _errs79 === errors;
      valid11 = valid11 || _valid8;
      const _errs81 = errors;
      if (typeof data12 === "string") {
        if (!pattern6.test(data12)) {
          const err73 = { instancePath: instancePath + "/hatch", schemaPath: "#/properties/hatch/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err73];
          } else {
            vErrors.push(err73);
          }
          errors++;
        }
      } else {
        const err74 = { instancePath: instancePath + "/hatch", schemaPath: "#/properties/hatch/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err74];
        } else {
          vErrors.push(err74);
        }
        errors++;
      }
      var _valid8 = _errs81 === errors;
      valid11 = valid11 || _valid8;
      if (!valid11) {
        const err75 = { instancePath: instancePath + "/hatch", schemaPath: "#/properties/hatch/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err75];
        } else {
          vErrors.push(err75);
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
    if (data.hatch_spacing_mm !== void 0) {
      let data13 = data.hatch_spacing_mm;
      const _errs84 = errors;
      let valid12 = false;
      const _errs85 = errors;
      if (typeof data13 == "number") {
        if (data13 <= 0 || isNaN(data13)) {
          const err76 = { instancePath: instancePath + "/hatch_spacing_mm", schemaPath: "#/properties/hatch_spacing_mm/anyOf/0/exclusiveMinimum", keyword: "exclusiveMinimum", params: { comparison: ">", limit: 0 }, message: "must be > 0" };
          if (vErrors === null) {
            vErrors = [err76];
          } else {
            vErrors.push(err76);
          }
          errors++;
        }
      } else {
        const err77 = { instancePath: instancePath + "/hatch_spacing_mm", schemaPath: "#/properties/hatch_spacing_mm/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err77];
        } else {
          vErrors.push(err77);
        }
        errors++;
      }
      var _valid9 = _errs85 === errors;
      valid12 = valid12 || _valid9;
      const _errs87 = errors;
      if (typeof data13 !== "boolean") {
        const err78 = { instancePath: instancePath + "/hatch_spacing_mm", schemaPath: "#/properties/hatch_spacing_mm/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err78];
        } else {
          vErrors.push(err78);
        }
        errors++;
      }
      var _valid9 = _errs87 === errors;
      valid12 = valid12 || _valid9;
      const _errs89 = errors;
      if (typeof data13 === "string") {
        if (!pattern5.test(data13)) {
          const err79 = { instancePath: instancePath + "/hatch_spacing_mm", schemaPath: "#/properties/hatch_spacing_mm/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err79];
          } else {
            vErrors.push(err79);
          }
          errors++;
        }
      } else {
        const err80 = { instancePath: instancePath + "/hatch_spacing_mm", schemaPath: "#/properties/hatch_spacing_mm/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err80];
        } else {
          vErrors.push(err80);
        }
        errors++;
      }
      var _valid9 = _errs89 === errors;
      valid12 = valid12 || _valid9;
      if (!valid12) {
        const err81 = { instancePath: instancePath + "/hatch_spacing_mm", schemaPath: "#/properties/hatch_spacing_mm/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err81];
        } else {
          vErrors.push(err81);
        }
        errors++;
      } else {
        errors = _errs84;
        if (vErrors !== null) {
          if (_errs84) {
            vErrors.length = _errs84;
          } else {
            vErrors = null;
          }
        }
      }
      if (typeof data13 === "string" || typeof data13 === "boolean") {
        if (!Number.isFinite(Number(data13))) {
          const err82 = { instancePath: instancePath + "/hatch_spacing_mm", schemaPath: "#/properties/hatch_spacing_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err82];
          } else {
            vErrors.push(err82);
          }
          errors++;
        }
        if (Number(data13) <= 0) {
          const err83 = { instancePath: instancePath + "/hatch_spacing_mm", schemaPath: "#/properties/hatch_spacing_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err83];
          } else {
            vErrors.push(err83);
          }
          errors++;
        }
      }
    }
    if (data.hatch_angle_deg !== void 0) {
      let data14 = data.hatch_angle_deg;
      const _errs92 = errors;
      let valid13 = false;
      const _errs93 = errors;
      if (!(typeof data14 == "number")) {
        const err84 = { instancePath: instancePath + "/hatch_angle_deg", schemaPath: "#/properties/hatch_angle_deg/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err84];
        } else {
          vErrors.push(err84);
        }
        errors++;
      }
      var _valid10 = _errs93 === errors;
      valid13 = valid13 || _valid10;
      const _errs95 = errors;
      if (typeof data14 !== "boolean") {
        const err85 = { instancePath: instancePath + "/hatch_angle_deg", schemaPath: "#/properties/hatch_angle_deg/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err85];
        } else {
          vErrors.push(err85);
        }
        errors++;
      }
      var _valid10 = _errs95 === errors;
      valid13 = valid13 || _valid10;
      const _errs97 = errors;
      if (typeof data14 === "string") {
        if (!pattern5.test(data14)) {
          const err86 = { instancePath: instancePath + "/hatch_angle_deg", schemaPath: "#/properties/hatch_angle_deg/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err86];
          } else {
            vErrors.push(err86);
          }
          errors++;
        }
      } else {
        const err87 = { instancePath: instancePath + "/hatch_angle_deg", schemaPath: "#/properties/hatch_angle_deg/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err87];
        } else {
          vErrors.push(err87);
        }
        errors++;
      }
      var _valid10 = _errs97 === errors;
      valid13 = valid13 || _valid10;
      if (!valid13) {
        const err88 = { instancePath: instancePath + "/hatch_angle_deg", schemaPath: "#/properties/hatch_angle_deg/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err88];
        } else {
          vErrors.push(err88);
        }
        errors++;
      } else {
        errors = _errs92;
        if (vErrors !== null) {
          if (_errs92) {
            vErrors.length = _errs92;
          } else {
            vErrors = null;
          }
        }
      }
      if (typeof data14 === "string" || typeof data14 === "boolean") {
        if (!Number.isFinite(Number(data14))) {
          const err89 = { instancePath: instancePath + "/hatch_angle_deg", schemaPath: "#/properties/hatch_angle_deg/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err89];
          } else {
            vErrors.push(err89);
          }
          errors++;
        }
      }
    }
    if (data.hatch_line_width_mm !== void 0) {
      let data15 = data.hatch_line_width_mm;
      const _errs100 = errors;
      let valid14 = false;
      const _errs101 = errors;
      if (typeof data15 == "number") {
        if (data15 <= 0 || isNaN(data15)) {
          const err90 = { instancePath: instancePath + "/hatch_line_width_mm", schemaPath: "#/properties/hatch_line_width_mm/anyOf/0/exclusiveMinimum", keyword: "exclusiveMinimum", params: { comparison: ">", limit: 0 }, message: "must be > 0" };
          if (vErrors === null) {
            vErrors = [err90];
          } else {
            vErrors.push(err90);
          }
          errors++;
        }
      } else {
        const err91 = { instancePath: instancePath + "/hatch_line_width_mm", schemaPath: "#/properties/hatch_line_width_mm/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err91];
        } else {
          vErrors.push(err91);
        }
        errors++;
      }
      var _valid11 = _errs101 === errors;
      valid14 = valid14 || _valid11;
      const _errs103 = errors;
      if (typeof data15 !== "boolean") {
        const err92 = { instancePath: instancePath + "/hatch_line_width_mm", schemaPath: "#/properties/hatch_line_width_mm/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err92];
        } else {
          vErrors.push(err92);
        }
        errors++;
      }
      var _valid11 = _errs103 === errors;
      valid14 = valid14 || _valid11;
      const _errs105 = errors;
      if (typeof data15 === "string") {
        if (!pattern5.test(data15)) {
          const err93 = { instancePath: instancePath + "/hatch_line_width_mm", schemaPath: "#/properties/hatch_line_width_mm/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err93];
          } else {
            vErrors.push(err93);
          }
          errors++;
        }
      } else {
        const err94 = { instancePath: instancePath + "/hatch_line_width_mm", schemaPath: "#/properties/hatch_line_width_mm/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err94];
        } else {
          vErrors.push(err94);
        }
        errors++;
      }
      var _valid11 = _errs105 === errors;
      valid14 = valid14 || _valid11;
      if (!valid14) {
        const err95 = { instancePath: instancePath + "/hatch_line_width_mm", schemaPath: "#/properties/hatch_line_width_mm/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err95];
        } else {
          vErrors.push(err95);
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
      if (typeof data15 === "string" || typeof data15 === "boolean") {
        if (!Number.isFinite(Number(data15))) {
          const err96 = { instancePath: instancePath + "/hatch_line_width_mm", schemaPath: "#/properties/hatch_line_width_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err96];
          } else {
            vErrors.push(err96);
          }
          errors++;
        }
        if (Number(data15) <= 0) {
          const err97 = { instancePath: instancePath + "/hatch_line_width_mm", schemaPath: "#/properties/hatch_line_width_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err97];
          } else {
            vErrors.push(err97);
          }
          errors++;
        }
      }
    }
    if (data.outline_style !== void 0) {
      let data16 = data.outline_style;
      const _errs108 = errors;
      let valid15 = false;
      const _errs109 = errors;
      const _errs110 = errors;
      let valid16 = false;
      const _errs111 = errors;
      if (typeof data16 !== "string") {
        const err98 = { instancePath: instancePath + "/outline_style", schemaPath: "#/properties/outline_style/anyOf/0/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err98];
        } else {
          vErrors.push(err98);
        }
        errors++;
      }
      if ("solid" !== data16) {
        const err99 = { instancePath: instancePath + "/outline_style", schemaPath: "#/properties/outline_style/anyOf/0/anyOf/0/const", keyword: "const", params: { allowedValue: "solid" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err99];
        } else {
          vErrors.push(err99);
        }
        errors++;
      }
      var _valid13 = _errs111 === errors;
      valid16 = valid16 || _valid13;
      const _errs113 = errors;
      if (typeof data16 !== "string") {
        const err100 = { instancePath: instancePath + "/outline_style", schemaPath: "#/properties/outline_style/anyOf/0/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err100];
        } else {
          vErrors.push(err100);
        }
        errors++;
      }
      if ("dashed" !== data16) {
        const err101 = { instancePath: instancePath + "/outline_style", schemaPath: "#/properties/outline_style/anyOf/0/anyOf/1/const", keyword: "const", params: { allowedValue: "dashed" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err101];
        } else {
          vErrors.push(err101);
        }
        errors++;
      }
      var _valid13 = _errs113 === errors;
      valid16 = valid16 || _valid13;
      if (!valid16) {
        const err102 = { instancePath: instancePath + "/outline_style", schemaPath: "#/properties/outline_style/anyOf/0/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err102];
        } else {
          vErrors.push(err102);
        }
        errors++;
      } else {
        errors = _errs110;
        if (vErrors !== null) {
          if (_errs110) {
            vErrors.length = _errs110;
          } else {
            vErrors = null;
          }
        }
      }
      var _valid12 = _errs109 === errors;
      valid15 = valid15 || _valid12;
      const _errs115 = errors;
      if (typeof data16 === "string") {
        if (!pattern49.test(data16)) {
          const err103 = { instancePath: instancePath + "/outline_style", schemaPath: "#/properties/outline_style/anyOf/1/pattern", keyword: "pattern", params: { pattern: "^(?:[sS][oO][lL][iI][dD]|[dD][aA][sS][hH][eE][dD])$" }, message: 'must match pattern "^(?:[sS][oO][lL][iI][dD]|[dD][aA][sS][hH][eE][dD])$"' };
          if (vErrors === null) {
            vErrors = [err103];
          } else {
            vErrors.push(err103);
          }
          errors++;
        }
      } else {
        const err104 = { instancePath: instancePath + "/outline_style", schemaPath: "#/properties/outline_style/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err104];
        } else {
          vErrors.push(err104);
        }
        errors++;
      }
      var _valid12 = _errs115 === errors;
      valid15 = valid15 || _valid12;
      if (!valid15) {
        const err105 = { instancePath: instancePath + "/outline_style", schemaPath: "#/properties/outline_style/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err105];
        } else {
          vErrors.push(err105);
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
    if (data.outline_dash_mm !== void 0) {
      let data17 = data.outline_dash_mm;
      const _errs118 = errors;
      let valid17 = false;
      const _errs119 = errors;
      if (typeof data17 == "number") {
        if (data17 <= 0 || isNaN(data17)) {
          const err106 = { instancePath: instancePath + "/outline_dash_mm", schemaPath: "#/properties/outline_dash_mm/anyOf/0/exclusiveMinimum", keyword: "exclusiveMinimum", params: { comparison: ">", limit: 0 }, message: "must be > 0" };
          if (vErrors === null) {
            vErrors = [err106];
          } else {
            vErrors.push(err106);
          }
          errors++;
        }
      } else {
        const err107 = { instancePath: instancePath + "/outline_dash_mm", schemaPath: "#/properties/outline_dash_mm/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err107];
        } else {
          vErrors.push(err107);
        }
        errors++;
      }
      var _valid14 = _errs119 === errors;
      valid17 = valid17 || _valid14;
      const _errs121 = errors;
      if (typeof data17 !== "boolean") {
        const err108 = { instancePath: instancePath + "/outline_dash_mm", schemaPath: "#/properties/outline_dash_mm/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err108];
        } else {
          vErrors.push(err108);
        }
        errors++;
      }
      var _valid14 = _errs121 === errors;
      valid17 = valid17 || _valid14;
      const _errs123 = errors;
      if (typeof data17 === "string") {
        if (!pattern5.test(data17)) {
          const err109 = { instancePath: instancePath + "/outline_dash_mm", schemaPath: "#/properties/outline_dash_mm/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err109];
          } else {
            vErrors.push(err109);
          }
          errors++;
        }
      } else {
        const err110 = { instancePath: instancePath + "/outline_dash_mm", schemaPath: "#/properties/outline_dash_mm/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err110];
        } else {
          vErrors.push(err110);
        }
        errors++;
      }
      var _valid14 = _errs123 === errors;
      valid17 = valid17 || _valid14;
      if (!valid17) {
        const err111 = { instancePath: instancePath + "/outline_dash_mm", schemaPath: "#/properties/outline_dash_mm/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err111];
        } else {
          vErrors.push(err111);
        }
        errors++;
      } else {
        errors = _errs118;
        if (vErrors !== null) {
          if (_errs118) {
            vErrors.length = _errs118;
          } else {
            vErrors = null;
          }
        }
      }
      if (typeof data17 === "string" || typeof data17 === "boolean") {
        if (!Number.isFinite(Number(data17))) {
          const err112 = { instancePath: instancePath + "/outline_dash_mm", schemaPath: "#/properties/outline_dash_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err112];
          } else {
            vErrors.push(err112);
          }
          errors++;
        }
        if (Number(data17) <= 0) {
          const err113 = { instancePath: instancePath + "/outline_dash_mm", schemaPath: "#/properties/outline_dash_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err113];
          } else {
            vErrors.push(err113);
          }
          errors++;
        }
      }
    }
    if (data.outline_width_mm !== void 0) {
      let data18 = data.outline_width_mm;
      const _errs126 = errors;
      let valid18 = false;
      const _errs127 = errors;
      if (typeof data18 == "number") {
        if (data18 <= 0 || isNaN(data18)) {
          const err114 = { instancePath: instancePath + "/outline_width_mm", schemaPath: "#/properties/outline_width_mm/anyOf/0/exclusiveMinimum", keyword: "exclusiveMinimum", params: { comparison: ">", limit: 0 }, message: "must be > 0" };
          if (vErrors === null) {
            vErrors = [err114];
          } else {
            vErrors.push(err114);
          }
          errors++;
        }
      } else {
        const err115 = { instancePath: instancePath + "/outline_width_mm", schemaPath: "#/properties/outline_width_mm/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err115];
        } else {
          vErrors.push(err115);
        }
        errors++;
      }
      var _valid15 = _errs127 === errors;
      valid18 = valid18 || _valid15;
      const _errs129 = errors;
      if (typeof data18 !== "boolean") {
        const err116 = { instancePath: instancePath + "/outline_width_mm", schemaPath: "#/properties/outline_width_mm/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err116];
        } else {
          vErrors.push(err116);
        }
        errors++;
      }
      var _valid15 = _errs129 === errors;
      valid18 = valid18 || _valid15;
      const _errs131 = errors;
      if (typeof data18 === "string") {
        if (!pattern5.test(data18)) {
          const err117 = { instancePath: instancePath + "/outline_width_mm", schemaPath: "#/properties/outline_width_mm/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err117];
          } else {
            vErrors.push(err117);
          }
          errors++;
        }
      } else {
        const err118 = { instancePath: instancePath + "/outline_width_mm", schemaPath: "#/properties/outline_width_mm/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err118];
        } else {
          vErrors.push(err118);
        }
        errors++;
      }
      var _valid15 = _errs131 === errors;
      valid18 = valid18 || _valid15;
      if (!valid18) {
        const err119 = { instancePath: instancePath + "/outline_width_mm", schemaPath: "#/properties/outline_width_mm/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err119];
        } else {
          vErrors.push(err119);
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
      if (typeof data18 === "string" || typeof data18 === "boolean") {
        if (!Number.isFinite(Number(data18))) {
          const err120 = { instancePath: instancePath + "/outline_width_mm", schemaPath: "#/properties/outline_width_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err120];
          } else {
            vErrors.push(err120);
          }
          errors++;
        }
        if (Number(data18) <= 0) {
          const err121 = { instancePath: instancePath + "/outline_width_mm", schemaPath: "#/properties/outline_width_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err121];
          } else {
            vErrors.push(err121);
          }
          errors++;
        }
      }
    }
  } else {
    const err122 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err122];
    } else {
      vErrors.push(err122);
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
      if (!(typeof data0 == "number")) {
        const err2 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (typeof data0 === "string") {
        if (!pattern6.test(data0)) {
          const err3 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err5 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.plated_color !== void 0) {
      if (typeof data.plated_color !== "string") {
        const err6 = { instancePath: instancePath + "/plated_color", schemaPath: "#/properties/plated_color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.non_plated_color !== void 0) {
      if (typeof data.non_plated_color !== "string") {
        const err7 = { instancePath: instancePath + "/non_plated_color", schemaPath: "#/properties/non_plated_color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.outline !== void 0) {
      let data3 = data.outline;
      const _errs18 = errors;
      let valid4 = false;
      const _errs19 = errors;
      if (typeof data3 !== "boolean") {
        const err8 = { instancePath: instancePath + "/outline", schemaPath: "#/properties/outline/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid1 = _errs19 === errors;
      valid4 = valid4 || _valid1;
      const _errs21 = errors;
      if (!(typeof data3 == "number")) {
        const err9 = { instancePath: instancePath + "/outline", schemaPath: "#/properties/outline/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid1 = _errs21 === errors;
      valid4 = valid4 || _valid1;
      const _errs23 = errors;
      if (typeof data3 === "string") {
        if (!pattern6.test(data3)) {
          const err10 = { instancePath: instancePath + "/outline", schemaPath: "#/properties/outline/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err10];
          } else {
            vErrors.push(err10);
          }
          errors++;
        }
      } else {
        const err11 = { instancePath: instancePath + "/outline", schemaPath: "#/properties/outline/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid1 = _errs23 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err12 = { instancePath: instancePath + "/outline", schemaPath: "#/properties/outline/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.outline_width_mm !== void 0) {
      let data4 = data.outline_width_mm;
      const _errs26 = errors;
      let valid5 = false;
      const _errs27 = errors;
      if (typeof data4 == "number") {
        if (data4 <= 0 || isNaN(data4)) {
          const err13 = { instancePath: instancePath + "/outline_width_mm", schemaPath: "#/properties/outline_width_mm/anyOf/0/exclusiveMinimum", keyword: "exclusiveMinimum", params: { comparison: ">", limit: 0 }, message: "must be > 0" };
          if (vErrors === null) {
            vErrors = [err13];
          } else {
            vErrors.push(err13);
          }
          errors++;
        }
      } else {
        const err14 = { instancePath: instancePath + "/outline_width_mm", schemaPath: "#/properties/outline_width_mm/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid2 = _errs27 === errors;
      valid5 = valid5 || _valid2;
      const _errs29 = errors;
      if (typeof data4 !== "boolean") {
        const err15 = { instancePath: instancePath + "/outline_width_mm", schemaPath: "#/properties/outline_width_mm/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid2 = _errs29 === errors;
      valid5 = valid5 || _valid2;
      const _errs31 = errors;
      if (typeof data4 === "string") {
        if (!pattern5.test(data4)) {
          const err16 = { instancePath: instancePath + "/outline_width_mm", schemaPath: "#/properties/outline_width_mm/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err16];
          } else {
            vErrors.push(err16);
          }
          errors++;
        }
      } else {
        const err17 = { instancePath: instancePath + "/outline_width_mm", schemaPath: "#/properties/outline_width_mm/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      var _valid2 = _errs31 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err18 = { instancePath: instancePath + "/outline_width_mm", schemaPath: "#/properties/outline_width_mm/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
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
      if (typeof data4 === "string" || typeof data4 === "boolean") {
        if (!Number.isFinite(Number(data4))) {
          const err19 = { instancePath: instancePath + "/outline_width_mm", schemaPath: "#/properties/outline_width_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err19];
          } else {
            vErrors.push(err19);
          }
          errors++;
        }
        if (Number(data4) <= 0) {
          const err20 = { instancePath: instancePath + "/outline_width_mm", schemaPath: "#/properties/outline_width_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err20];
          } else {
            vErrors.push(err20);
          }
          errors++;
        }
      }
    }
    if (data.respect_tenting !== void 0) {
      let data5 = data.respect_tenting;
      const _errs34 = errors;
      let valid6 = false;
      const _errs35 = errors;
      if (typeof data5 !== "boolean") {
        const err21 = { instancePath: instancePath + "/respect_tenting", schemaPath: "#/properties/respect_tenting/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      var _valid3 = _errs35 === errors;
      valid6 = valid6 || _valid3;
      const _errs37 = errors;
      if (!(typeof data5 == "number")) {
        const err22 = { instancePath: instancePath + "/respect_tenting", schemaPath: "#/properties/respect_tenting/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
      var _valid3 = _errs37 === errors;
      valid6 = valid6 || _valid3;
      const _errs39 = errors;
      if (typeof data5 === "string") {
        if (!pattern6.test(data5)) {
          const err23 = { instancePath: instancePath + "/respect_tenting", schemaPath: "#/properties/respect_tenting/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err23];
          } else {
            vErrors.push(err23);
          }
          errors++;
        }
      } else {
        const err24 = { instancePath: instancePath + "/respect_tenting", schemaPath: "#/properties/respect_tenting/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      var _valid3 = _errs39 === errors;
      valid6 = valid6 || _valid3;
      if (!valid6) {
        const err25 = { instancePath: instancePath + "/respect_tenting", schemaPath: "#/properties/respect_tenting/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.opacity !== void 0) {
      let data6 = data.opacity;
      const _errs42 = errors;
      let valid7 = false;
      const _errs43 = errors;
      if (typeof data6 == "number") {
        if (data6 > 1 || isNaN(data6)) {
          const err26 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/0/maximum", keyword: "maximum", params: { comparison: "<=", limit: 1 }, message: "must be <= 1" };
          if (vErrors === null) {
            vErrors = [err26];
          } else {
            vErrors.push(err26);
          }
          errors++;
        }
        if (data6 < 0 || isNaN(data6)) {
          const err27 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/0/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err27];
          } else {
            vErrors.push(err27);
          }
          errors++;
        }
      } else {
        const err28 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
      var _valid4 = _errs43 === errors;
      valid7 = valid7 || _valid4;
      const _errs45 = errors;
      if (typeof data6 !== "boolean") {
        const err29 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      }
      var _valid4 = _errs45 === errors;
      valid7 = valid7 || _valid4;
      const _errs47 = errors;
      if (typeof data6 === "string") {
        if (!pattern5.test(data6)) {
          const err30 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err30];
          } else {
            vErrors.push(err30);
          }
          errors++;
        }
      } else {
        const err31 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      }
      var _valid4 = _errs47 === errors;
      valid7 = valid7 || _valid4;
      if (!valid7) {
        const err32 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
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
      if (typeof data6 === "string" || typeof data6 === "boolean") {
        if (!Number.isFinite(Number(data6))) {
          const err33 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err33];
          } else {
            vErrors.push(err33);
          }
          errors++;
        }
        if (Number(data6) < 0) {
          const err34 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err34];
          } else {
            vErrors.push(err34);
          }
          errors++;
        }
        if (Number(data6) > 1) {
          const err35 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err35];
          } else {
            vErrors.push(err35);
          }
          errors++;
        }
      }
    }
  } else {
    const err36 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err36];
    } else {
      vErrors.push(err36);
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
      if (!(typeof data0 == "number")) {
        const err2 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (typeof data0 === "string") {
        if (!pattern6.test(data0)) {
          const err3 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err5 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.color !== void 0) {
      if (typeof data.color !== "string") {
        const err6 = { instancePath: instancePath + "/color", schemaPath: "#/properties/color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
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
  validate44.errors = vErrors;
  return errors === 0;
}
validate44.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate46(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate46.evaluated;
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
      if (!(typeof data0 == "number")) {
        const err2 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (typeof data0 === "string") {
        if (!pattern6.test(data0)) {
          const err3 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err5 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.color !== void 0) {
      if (typeof data.color !== "string") {
        const err6 = { instancePath: instancePath + "/color", schemaPath: "#/properties/color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
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
  validate46.errors = vErrors;
  return errors === 0;
}
validate46.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate48(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate48.evaluated;
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
      if (!(typeof data0 == "number")) {
        const err2 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (typeof data0 === "string") {
        if (!pattern6.test(data0)) {
          const err3 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err5 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.color !== void 0) {
      if (typeof data.color !== "string") {
        const err6 = { instancePath: instancePath + "/color", schemaPath: "#/properties/color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
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
  validate48.errors = vErrors;
  return errors === 0;
}
validate48.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
      if (!(typeof data0 == "number")) {
        const err2 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (typeof data0 === "string") {
        if (!pattern6.test(data0)) {
          const err3 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err5 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.color !== void 0) {
      if (typeof data.color !== "string") {
        const err6 = { instancePath: instancePath + "/color", schemaPath: "#/properties/color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
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
  validate50.errors = vErrors;
  return errors === 0;
}
validate50.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate52(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate52.evaluated;
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
      if (!(typeof data0 == "number")) {
        const err2 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (typeof data0 === "string") {
        if (!pattern6.test(data0)) {
          const err3 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err5 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.color !== void 0) {
      if (typeof data.color !== "string") {
        const err6 = { instancePath: instancePath + "/color", schemaPath: "#/properties/color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
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
  validate52.errors = vErrors;
  return errors === 0;
}
validate52.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate54(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate54.evaluated;
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
      if (!(typeof data0 == "number")) {
        const err2 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (typeof data0 === "string") {
        if (!pattern6.test(data0)) {
          const err3 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err5 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.color !== void 0) {
      if (typeof data.color !== "string") {
        const err6 = { instancePath: instancePath + "/color", schemaPath: "#/properties/color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
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
  validate54.errors = vErrors;
  return errors === 0;
}
validate54.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
      if (!(typeof data0 == "number")) {
        const err2 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (typeof data0 === "string") {
        if (!pattern6.test(data0)) {
          const err3 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err5 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.color !== void 0) {
      if (typeof data.color !== "string") {
        const err6 = { instancePath: instancePath + "/color", schemaPath: "#/properties/color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
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
  validate56.errors = vErrors;
  return errors === 0;
}
validate56.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
      if (!(typeof data0 == "number")) {
        const err2 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (typeof data0 === "string") {
        if (!pattern6.test(data0)) {
          const err3 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err5 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.color !== void 0) {
      if (typeof data.color !== "string") {
        const err6 = { instancePath: instancePath + "/color", schemaPath: "#/properties/color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
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
  validate58.errors = vErrors;
  return errors === 0;
}
validate58.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate60(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate60.evaluated;
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
      if (!(typeof data0 == "number")) {
        const err2 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (typeof data0 === "string") {
        if (!pattern6.test(data0)) {
          const err3 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err5 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.color !== void 0) {
      if (typeof data.color !== "string") {
        const err6 = { instancePath: instancePath + "/color", schemaPath: "#/properties/color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.dot_diameter_mm !== void 0) {
      let data2 = data.dot_diameter_mm;
      const _errs16 = errors;
      let valid4 = false;
      const _errs17 = errors;
      if (!(typeof data2 == "number")) {
        const err7 = { instancePath: instancePath + "/dot_diameter_mm", schemaPath: "#/properties/dot_diameter_mm/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid1 = _errs17 === errors;
      valid4 = valid4 || _valid1;
      const _errs19 = errors;
      if (typeof data2 !== "boolean") {
        const err8 = { instancePath: instancePath + "/dot_diameter_mm", schemaPath: "#/properties/dot_diameter_mm/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid1 = _errs19 === errors;
      valid4 = valid4 || _valid1;
      const _errs21 = errors;
      if (typeof data2 === "string") {
        if (!pattern5.test(data2)) {
          const err9 = { instancePath: instancePath + "/dot_diameter_mm", schemaPath: "#/properties/dot_diameter_mm/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err9];
          } else {
            vErrors.push(err9);
          }
          errors++;
        }
      } else {
        const err10 = { instancePath: instancePath + "/dot_diameter_mm", schemaPath: "#/properties/dot_diameter_mm/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid1 = _errs21 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err11 = { instancePath: instancePath + "/dot_diameter_mm", schemaPath: "#/properties/dot_diameter_mm/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
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
      if (typeof data2 === "string" || typeof data2 === "boolean") {
        if (!Number.isFinite(Number(data2))) {
          const err12 = { instancePath: instancePath + "/dot_diameter_mm", schemaPath: "#/properties/dot_diameter_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err12];
          } else {
            vErrors.push(err12);
          }
          errors++;
        }
      }
    }
    if (data.min_dot_diameter_mm !== void 0) {
      let data3 = data.min_dot_diameter_mm;
      const _errs24 = errors;
      let valid5 = false;
      const _errs25 = errors;
      if (!(typeof data3 == "number")) {
        const err13 = { instancePath: instancePath + "/min_dot_diameter_mm", schemaPath: "#/properties/min_dot_diameter_mm/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid2 = _errs25 === errors;
      valid5 = valid5 || _valid2;
      const _errs27 = errors;
      if (typeof data3 !== "boolean") {
        const err14 = { instancePath: instancePath + "/min_dot_diameter_mm", schemaPath: "#/properties/min_dot_diameter_mm/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid2 = _errs27 === errors;
      valid5 = valid5 || _valid2;
      const _errs29 = errors;
      if (typeof data3 === "string") {
        if (!pattern5.test(data3)) {
          const err15 = { instancePath: instancePath + "/min_dot_diameter_mm", schemaPath: "#/properties/min_dot_diameter_mm/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err15];
          } else {
            vErrors.push(err15);
          }
          errors++;
        }
      } else {
        const err16 = { instancePath: instancePath + "/min_dot_diameter_mm", schemaPath: "#/properties/min_dot_diameter_mm/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid2 = _errs29 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err17 = { instancePath: instancePath + "/min_dot_diameter_mm", schemaPath: "#/properties/min_dot_diameter_mm/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
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
      if (typeof data3 === "string" || typeof data3 === "boolean") {
        if (!Number.isFinite(Number(data3))) {
          const err18 = { instancePath: instancePath + "/min_dot_diameter_mm", schemaPath: "#/properties/min_dot_diameter_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err18];
          } else {
            vErrors.push(err18);
          }
          errors++;
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
  validate60.errors = vErrors;
  return errors === 0;
}
validate60.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate62(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate62.evaluated;
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
      if (!(typeof data0 == "number")) {
        const err2 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      const _errs11 = errors;
      if (typeof data0 === "string") {
        if (!pattern6.test(data0)) {
          const err3 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err5 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.color !== void 0) {
      if (typeof data.color !== "string") {
        const err6 = { instancePath: instancePath + "/color", schemaPath: "#/properties/color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
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
  validate62.errors = vErrors;
  return errors === 0;
}
validate62.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
  if (!validate23(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate23.errors : vErrors.concat(validate23.errors);
    errors = vErrors.length;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.illustration !== void 0) {
      if (!validate25(data.illustration, { instancePath: instancePath + "/illustration", parentData: data, parentDataProperty: "illustration", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate25.errors : vErrors.concat(validate25.errors);
        errors = vErrors.length;
      }
    }
    if (data.assembly_designators !== void 0) {
      if (!validate27(data.assembly_designators, { instancePath: instancePath + "/assembly_designators", parentData: data, parentDataProperty: "assembly_designators", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate27.errors : vErrors.concat(validate27.errors);
        errors = vErrors.length;
      }
    }
    if (data.board_substrate !== void 0) {
      if (!validate29(data.board_substrate, { instancePath: instancePath + "/board_substrate", parentData: data, parentDataProperty: "board_substrate", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate29.errors : vErrors.concat(validate29.errors);
        errors = vErrors.length;
      }
    }
    if (data.soldermask_film !== void 0) {
      if (!validate31(data.soldermask_film, { instancePath: instancePath + "/soldermask_film", parentData: data, parentDataProperty: "soldermask_film", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate31.errors : vErrors.concat(validate31.errors);
        errors = vErrors.length;
      }
    }
    if (data.assembly_hlr !== void 0) {
      if (!validate33(data.assembly_hlr, { instancePath: instancePath + "/assembly_hlr", parentData: data, parentDataProperty: "assembly_hlr", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate33.errors : vErrors.concat(validate33.errors);
        errors = vErrors.length;
      }
    }
    if (data.board_outline !== void 0) {
      if (!validate37(data.board_outline, { instancePath: instancePath + "/board_outline", parentData: data, parentDataProperty: "board_outline", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate37.errors : vErrors.concat(validate37.errors);
        errors = vErrors.length;
      }
    }
    if (data.board_cutouts !== void 0) {
      if (!validate39(data.board_cutouts, { instancePath: instancePath + "/board_cutouts", parentData: data, parentDataProperty: "board_cutouts", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate39.errors : vErrors.concat(validate39.errors);
        errors = vErrors.length;
      }
    }
    if (data.drills !== void 0) {
      if (!validate41(data.drills, { instancePath: instancePath + "/drills", parentData: data, parentDataProperty: "drills", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate41.errors : vErrors.concat(validate41.errors);
        errors = vErrors.length;
      }
    }
    if (data.slots !== void 0) {
      if (!validate41(data.slots, { instancePath: instancePath + "/slots", parentData: data, parentDataProperty: "slots", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate41.errors : vErrors.concat(validate41.errors);
        errors = vErrors.length;
      }
    }
    if (data.copper_traces !== void 0) {
      if (!validate44(data.copper_traces, { instancePath: instancePath + "/copper_traces", parentData: data, parentDataProperty: "copper_traces", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate44.errors : vErrors.concat(validate44.errors);
        errors = vErrors.length;
      }
    }
    if (data.vias !== void 0) {
      if (!validate46(data.vias, { instancePath: instancePath + "/vias", parentData: data, parentDataProperty: "vias", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate46.errors : vErrors.concat(validate46.errors);
        errors = vErrors.length;
      }
    }
    if (data.copper_polygons !== void 0) {
      if (!validate48(data.copper_polygons, { instancePath: instancePath + "/copper_polygons", parentData: data, parentDataProperty: "copper_polygons", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate48.errors : vErrors.concat(validate48.errors);
        errors = vErrors.length;
      }
    }
    if (data.smd_pads !== void 0) {
      if (!validate50(data.smd_pads, { instancePath: instancePath + "/smd_pads", parentData: data, parentDataProperty: "smd_pads", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate50.errors : vErrors.concat(validate50.errors);
        errors = vErrors.length;
      }
    }
    if (data.through_hole_pads !== void 0) {
      if (!validate52(data.through_hole_pads, { instancePath: instancePath + "/through_hole_pads", parentData: data, parentDataProperty: "through_hole_pads", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate52.errors : vErrors.concat(validate52.errors);
        errors = vErrors.length;
      }
    }
    if (data.silkscreen_component_graphics !== void 0) {
      if (!validate54(data.silkscreen_component_graphics, { instancePath: instancePath + "/silkscreen_component_graphics", parentData: data, parentDataProperty: "silkscreen_component_graphics", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate54.errors : vErrors.concat(validate54.errors);
        errors = vErrors.length;
      }
    }
    if (data.silkscreen_designators !== void 0) {
      if (!validate56(data.silkscreen_designators, { instancePath: instancePath + "/silkscreen_designators", parentData: data, parentDataProperty: "silkscreen_designators", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate56.errors : vErrors.concat(validate56.errors);
        errors = vErrors.length;
      }
    }
    if (data.silkscreen_board_graphics !== void 0) {
      if (!validate58(data.silkscreen_board_graphics, { instancePath: instancePath + "/silkscreen_board_graphics", parentData: data, parentDataProperty: "silkscreen_board_graphics", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate58.errors : vErrors.concat(validate58.errors);
        errors = vErrors.length;
      }
    }
    if (data.pin1_marker !== void 0) {
      if (!validate60(data.pin1_marker, { instancePath: instancePath + "/pin1_marker", parentData: data, parentDataProperty: "pin1_marker", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate60.errors : vErrors.concat(validate60.errors);
        errors = vErrors.length;
      }
    }
    if (data.keepout !== void 0) {
      if (!validate62(data.keepout, { instancePath: instancePath + "/keepout", parentData: data, parentDataProperty: "keepout", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate62.errors : vErrors.concat(validate62.errors);
        errors = vErrors.length;
      }
    }
  } else {
    const err0 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err0];
    } else {
      vErrors.push(err0);
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
  const _errs1 = errors;
  const _errs2 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    let missing0;
    if (data.png === void 0 && (missing0 = "png")) {
      const err0 = {};
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
  }
  var valid0 = _errs2 === errors;
  if (valid0) {
    const err1 = { instancePath, schemaPath: "#/not", keyword: "not", params: {}, message: "must NOT be valid" };
    if (vErrors === null) {
      vErrors = [err1];
    } else {
      vErrors.push(err1);
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
  if (data && typeof data == "object" && !Array.isArray(data)) {
  } else {
    const err2 = { instancePath, schemaPath: "#/$defs/RecordUnknown/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err2];
    } else {
      vErrors.push(err2);
    }
    errors++;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.pcbdoc !== void 0) {
      let data0 = data.pcbdoc;
      const _errs8 = errors;
      let valid4 = false;
      const _errs9 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/pcbdoc", schemaPath: "#/properties/pcbdoc/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid4 = valid4 || _valid0;
      const _errs11 = errors;
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/pcbdoc", schemaPath: "#/properties/pcbdoc/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid0 = _errs11 === errors;
      valid4 = valid4 || _valid0;
      if (!valid4) {
        const err5 = { instancePath: instancePath + "/pcbdoc", schemaPath: "#/properties/pcbdoc/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.canvas !== void 0) {
      let data1 = data.canvas;
      const _errs14 = errors;
      let valid5 = false;
      const _errs15 = errors;
      if (data1 && typeof data1 == "object" && !Array.isArray(data1)) {
        if (data1.bounds !== void 0) {
          let data2 = data1.bounds;
          const _errs19 = errors;
          let valid8 = false;
          const _errs20 = errors;
          const _errs21 = errors;
          let valid9 = false;
          const _errs22 = errors;
          if (typeof data2 !== "string") {
            const err6 = { instancePath: instancePath + "/canvas/bounds", schemaPath: "#/$defs/CanvasOptions/properties/bounds/anyOf/0/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err6];
            } else {
              vErrors.push(err6);
            }
            errors++;
          }
          if ("board_outline" !== data2) {
            const err7 = { instancePath: instancePath + "/canvas/bounds", schemaPath: "#/$defs/CanvasOptions/properties/bounds/anyOf/0/anyOf/0/const", keyword: "const", params: { allowedValue: "board_outline" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err7];
            } else {
              vErrors.push(err7);
            }
            errors++;
          }
          var _valid3 = _errs22 === errors;
          valid9 = valid9 || _valid3;
          const _errs24 = errors;
          if (typeof data2 !== "string") {
            const err8 = { instancePath: instancePath + "/canvas/bounds", schemaPath: "#/$defs/CanvasOptions/properties/bounds/anyOf/0/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err8];
            } else {
              vErrors.push(err8);
            }
            errors++;
          }
          if ("all_geometry" !== data2) {
            const err9 = { instancePath: instancePath + "/canvas/bounds", schemaPath: "#/$defs/CanvasOptions/properties/bounds/anyOf/0/anyOf/1/const", keyword: "const", params: { allowedValue: "all_geometry" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err9];
            } else {
              vErrors.push(err9);
            }
            errors++;
          }
          var _valid3 = _errs24 === errors;
          valid9 = valid9 || _valid3;
          const _errs26 = errors;
          if (typeof data2 !== "string") {
            const err10 = { instancePath: instancePath + "/canvas/bounds", schemaPath: "#/$defs/CanvasOptions/properties/bounds/anyOf/0/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err10];
            } else {
              vErrors.push(err10);
            }
            errors++;
          }
          if ("board" !== data2) {
            const err11 = { instancePath: instancePath + "/canvas/bounds", schemaPath: "#/$defs/CanvasOptions/properties/bounds/anyOf/0/anyOf/2/const", keyword: "const", params: { allowedValue: "board" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err11];
            } else {
              vErrors.push(err11);
            }
            errors++;
          }
          var _valid3 = _errs26 === errors;
          valid9 = valid9 || _valid3;
          const _errs28 = errors;
          if (typeof data2 !== "string") {
            const err12 = { instancePath: instancePath + "/canvas/bounds", schemaPath: "#/$defs/CanvasOptions/properties/bounds/anyOf/0/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err12];
            } else {
              vErrors.push(err12);
            }
            errors++;
          }
          if ("outline" !== data2) {
            const err13 = { instancePath: instancePath + "/canvas/bounds", schemaPath: "#/$defs/CanvasOptions/properties/bounds/anyOf/0/anyOf/3/const", keyword: "const", params: { allowedValue: "outline" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err13];
            } else {
              vErrors.push(err13);
            }
            errors++;
          }
          var _valid3 = _errs28 === errors;
          valid9 = valid9 || _valid3;
          const _errs30 = errors;
          if (typeof data2 !== "string") {
            const err14 = { instancePath: instancePath + "/canvas/bounds", schemaPath: "#/$defs/CanvasOptions/properties/bounds/anyOf/0/anyOf/4/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err14];
            } else {
              vErrors.push(err14);
            }
            errors++;
          }
          if ("board_profile" !== data2) {
            const err15 = { instancePath: instancePath + "/canvas/bounds", schemaPath: "#/$defs/CanvasOptions/properties/bounds/anyOf/0/anyOf/4/const", keyword: "const", params: { allowedValue: "board_profile" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err15];
            } else {
              vErrors.push(err15);
            }
            errors++;
          }
          var _valid3 = _errs30 === errors;
          valid9 = valid9 || _valid3;
          const _errs32 = errors;
          if (typeof data2 !== "string") {
            const err16 = { instancePath: instancePath + "/canvas/bounds", schemaPath: "#/$defs/CanvasOptions/properties/bounds/anyOf/0/anyOf/5/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err16];
            } else {
              vErrors.push(err16);
            }
            errors++;
          }
          if ("legacy" !== data2) {
            const err17 = { instancePath: instancePath + "/canvas/bounds", schemaPath: "#/$defs/CanvasOptions/properties/bounds/anyOf/0/anyOf/5/const", keyword: "const", params: { allowedValue: "legacy" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err17];
            } else {
              vErrors.push(err17);
            }
            errors++;
          }
          var _valid3 = _errs32 === errors;
          valid9 = valid9 || _valid3;
          const _errs34 = errors;
          if (typeof data2 !== "string") {
            const err18 = { instancePath: instancePath + "/canvas/bounds", schemaPath: "#/$defs/CanvasOptions/properties/bounds/anyOf/0/anyOf/6/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err18];
            } else {
              vErrors.push(err18);
            }
            errors++;
          }
          if ("all" !== data2) {
            const err19 = { instancePath: instancePath + "/canvas/bounds", schemaPath: "#/$defs/CanvasOptions/properties/bounds/anyOf/0/anyOf/6/const", keyword: "const", params: { allowedValue: "all" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err19];
            } else {
              vErrors.push(err19);
            }
            errors++;
          }
          var _valid3 = _errs34 === errors;
          valid9 = valid9 || _valid3;
          const _errs36 = errors;
          if (typeof data2 !== "string") {
            const err20 = { instancePath: instancePath + "/canvas/bounds", schemaPath: "#/$defs/CanvasOptions/properties/bounds/anyOf/0/anyOf/7/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err20];
            } else {
              vErrors.push(err20);
            }
            errors++;
          }
          if ("rendered_view" !== data2) {
            const err21 = { instancePath: instancePath + "/canvas/bounds", schemaPath: "#/$defs/CanvasOptions/properties/bounds/anyOf/0/anyOf/7/const", keyword: "const", params: { allowedValue: "rendered_view" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err21];
            } else {
              vErrors.push(err21);
            }
            errors++;
          }
          var _valid3 = _errs36 === errors;
          valid9 = valid9 || _valid3;
          const _errs38 = errors;
          if (typeof data2 !== "string") {
            const err22 = { instancePath: instancePath + "/canvas/bounds", schemaPath: "#/$defs/CanvasOptions/properties/bounds/anyOf/0/anyOf/8/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err22];
            } else {
              vErrors.push(err22);
            }
            errors++;
          }
          if ("rendered_geometry" !== data2) {
            const err23 = { instancePath: instancePath + "/canvas/bounds", schemaPath: "#/$defs/CanvasOptions/properties/bounds/anyOf/0/anyOf/8/const", keyword: "const", params: { allowedValue: "rendered_geometry" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err23];
            } else {
              vErrors.push(err23);
            }
            errors++;
          }
          var _valid3 = _errs38 === errors;
          valid9 = valid9 || _valid3;
          if (!valid9) {
            const err24 = { instancePath: instancePath + "/canvas/bounds", schemaPath: "#/$defs/CanvasOptions/properties/bounds/anyOf/0/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err24];
            } else {
              vErrors.push(err24);
            }
            errors++;
          } else {
            errors = _errs21;
            if (vErrors !== null) {
              if (_errs21) {
                vErrors.length = _errs21;
              } else {
                vErrors = null;
              }
            }
          }
          var _valid2 = _errs20 === errors;
          valid8 = valid8 || _valid2;
          const _errs40 = errors;
          if (data2 !== null) {
            const err25 = { instancePath: instancePath + "/canvas/bounds", schemaPath: "#/$defs/CanvasOptions/properties/bounds/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err25];
            } else {
              vErrors.push(err25);
            }
            errors++;
          }
          var _valid2 = _errs40 === errors;
          valid8 = valid8 || _valid2;
          const _errs42 = errors;
          if (typeof data2 === "string") {
            if (!pattern4.test(data2)) {
              const err26 = { instancePath: instancePath + "/canvas/bounds", schemaPath: "#/$defs/CanvasOptions/properties/bounds/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:[bB][oO][aA][rR][dD]_[oO][uU][tT][lL][iI][nN][eE]|[aA][lL][lL]_[gG][eE][oO][mM][eE][tT][rR][yY]|[bB][oO][aA][rR][dD]|[oO][uU][tT][lL][iI][nN][eE]|[bB][oO][aA][rR][dD]_[pP][rR][oO][fF][iI][lL][eE]|[lL][eE][gG][aA][cC][yY]|[aA][lL][lL]|[rR][eE][nN][dD][eE][rR][eE][dD]_[vV][iI][eE][wW]|[rR][eE][nN][dD][eE][rR][eE][dD]_[gG][eE][oO][mM][eE][tT][rR][yY])\\s*$" }, message: 'must match pattern "^\\s*(?:[bB][oO][aA][rR][dD]_[oO][uU][tT][lL][iI][nN][eE]|[aA][lL][lL]_[gG][eE][oO][mM][eE][tT][rR][yY]|[bB][oO][aA][rR][dD]|[oO][uU][tT][lL][iI][nN][eE]|[bB][oO][aA][rR][dD]_[pP][rR][oO][fF][iI][lL][eE]|[lL][eE][gG][aA][cC][yY]|[aA][lL][lL]|[rR][eE][nN][dD][eE][rR][eE][dD]_[vV][iI][eE][wW]|[rR][eE][nN][dD][eE][rR][eE][dD]_[gG][eE][oO][mM][eE][tT][rR][yY])\\s*$"' };
              if (vErrors === null) {
                vErrors = [err26];
              } else {
                vErrors.push(err26);
              }
              errors++;
            }
          } else {
            const err27 = { instancePath: instancePath + "/canvas/bounds", schemaPath: "#/$defs/CanvasOptions/properties/bounds/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err27];
            } else {
              vErrors.push(err27);
            }
            errors++;
          }
          var _valid2 = _errs42 === errors;
          valid8 = valid8 || _valid2;
          if (!valid8) {
            const err28 = { instancePath: instancePath + "/canvas/bounds", schemaPath: "#/$defs/CanvasOptions/properties/bounds/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err28];
            } else {
              vErrors.push(err28);
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
        if (data1.margin_mm !== void 0) {
          let data3 = data1.margin_mm;
          const _errs45 = errors;
          let valid10 = false;
          const _errs46 = errors;
          if (typeof data3 == "number") {
            if (data3 < 0 || isNaN(data3)) {
              const err29 = { instancePath: instancePath + "/canvas/margin_mm", schemaPath: "#/$defs/CanvasOptions/properties/margin_mm/anyOf/0/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
              if (vErrors === null) {
                vErrors = [err29];
              } else {
                vErrors.push(err29);
              }
              errors++;
            }
          } else {
            const err30 = { instancePath: instancePath + "/canvas/margin_mm", schemaPath: "#/$defs/CanvasOptions/properties/margin_mm/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err30];
            } else {
              vErrors.push(err30);
            }
            errors++;
          }
          var _valid4 = _errs46 === errors;
          valid10 = valid10 || _valid4;
          const _errs48 = errors;
          if (data3 !== null) {
            const err31 = { instancePath: instancePath + "/canvas/margin_mm", schemaPath: "#/$defs/CanvasOptions/properties/margin_mm/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err31];
            } else {
              vErrors.push(err31);
            }
            errors++;
          }
          var _valid4 = _errs48 === errors;
          valid10 = valid10 || _valid4;
          const _errs50 = errors;
          if (typeof data3 !== "boolean") {
            const err32 = { instancePath: instancePath + "/canvas/margin_mm", schemaPath: "#/$defs/CanvasOptions/properties/margin_mm/anyOf/2/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err32];
            } else {
              vErrors.push(err32);
            }
            errors++;
          }
          var _valid4 = _errs50 === errors;
          valid10 = valid10 || _valid4;
          const _errs52 = errors;
          if (typeof data3 === "string") {
            if (!pattern5.test(data3)) {
              const err33 = { instancePath: instancePath + "/canvas/margin_mm", schemaPath: "#/$defs/CanvasOptions/properties/margin_mm/anyOf/3/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
              if (vErrors === null) {
                vErrors = [err33];
              } else {
                vErrors.push(err33);
              }
              errors++;
            }
          } else {
            const err34 = { instancePath: instancePath + "/canvas/margin_mm", schemaPath: "#/$defs/CanvasOptions/properties/margin_mm/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err34];
            } else {
              vErrors.push(err34);
            }
            errors++;
          }
          var _valid4 = _errs52 === errors;
          valid10 = valid10 || _valid4;
          if (!valid10) {
            const err35 = { instancePath: instancePath + "/canvas/margin_mm", schemaPath: "#/$defs/CanvasOptions/properties/margin_mm/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err35];
            } else {
              vErrors.push(err35);
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
          if (typeof data3 === "string" || typeof data3 === "boolean") {
            if (!Number.isFinite(Number(data3))) {
              const err36 = { instancePath: instancePath + "/canvas/margin_mm", schemaPath: "#/$defs/CanvasOptions/properties/margin_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
              if (vErrors === null) {
                vErrors = [err36];
              } else {
                vErrors.push(err36);
              }
              errors++;
            }
            if (Number(data3) < 0) {
              const err37 = { instancePath: instancePath + "/canvas/margin_mm", schemaPath: "#/$defs/CanvasOptions/properties/margin_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
              if (vErrors === null) {
                vErrors = [err37];
              } else {
                vErrors.push(err37);
              }
              errors++;
            }
          }
        }
        for (const key1 in data1) {
          if (key1 !== "bounds" && key1 !== "margin_mm") {
            const err38 = { instancePath: instancePath + "/canvas/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/CanvasOptions/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err38];
            } else {
              vErrors.push(err38);
            }
            errors++;
          }
        }
      } else {
        const err39 = { instancePath: instancePath + "/canvas", schemaPath: "#/$defs/CanvasOptions/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err39];
        } else {
          vErrors.push(err39);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      valid5 = valid5 || _valid1;
      const _errs57 = errors;
      if (data1 !== null) {
        const err40 = { instancePath: instancePath + "/canvas", schemaPath: "#/properties/canvas/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err40];
        } else {
          vErrors.push(err40);
        }
        errors++;
      }
      var _valid1 = _errs57 === errors;
      valid5 = valid5 || _valid1;
      if (!valid5) {
        const err41 = { instancePath: instancePath + "/canvas", schemaPath: "#/properties/canvas/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err41];
        } else {
          vErrors.push(err41);
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
    if (data.include_metadata !== void 0) {
      let data5 = data.include_metadata;
      const _errs60 = errors;
      let valid12 = false;
      const _errs61 = errors;
      if (typeof data5 !== "boolean") {
        const err42 = { instancePath: instancePath + "/include_metadata", schemaPath: "#/properties/include_metadata/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err42];
        } else {
          vErrors.push(err42);
        }
        errors++;
      }
      var _valid5 = _errs61 === errors;
      valid12 = valid12 || _valid5;
      const _errs63 = errors;
      if (data5 !== null) {
        const err43 = { instancePath: instancePath + "/include_metadata", schemaPath: "#/properties/include_metadata/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err43];
        } else {
          vErrors.push(err43);
        }
        errors++;
      }
      var _valid5 = _errs63 === errors;
      valid12 = valid12 || _valid5;
      const _errs65 = errors;
      if (!(typeof data5 == "number")) {
        const err44 = { instancePath: instancePath + "/include_metadata", schemaPath: "#/properties/include_metadata/anyOf/2/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err44];
        } else {
          vErrors.push(err44);
        }
        errors++;
      }
      var _valid5 = _errs65 === errors;
      valid12 = valid12 || _valid5;
      const _errs67 = errors;
      if (typeof data5 === "string") {
        if (!pattern6.test(data5)) {
          const err45 = { instancePath: instancePath + "/include_metadata", schemaPath: "#/properties/include_metadata/anyOf/3/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err45];
          } else {
            vErrors.push(err45);
          }
          errors++;
        }
      } else {
        const err46 = { instancePath: instancePath + "/include_metadata", schemaPath: "#/properties/include_metadata/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err46];
        } else {
          vErrors.push(err46);
        }
        errors++;
      }
      var _valid5 = _errs67 === errors;
      valid12 = valid12 || _valid5;
      if (!valid12) {
        const err47 = { instancePath: instancePath + "/include_metadata", schemaPath: "#/properties/include_metadata/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err47];
        } else {
          vErrors.push(err47);
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
    if (data.show_empty_layers !== void 0) {
      let data6 = data.show_empty_layers;
      const _errs70 = errors;
      let valid13 = false;
      const _errs71 = errors;
      if (typeof data6 !== "boolean") {
        const err48 = { instancePath: instancePath + "/show_empty_layers", schemaPath: "#/properties/show_empty_layers/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err48];
        } else {
          vErrors.push(err48);
        }
        errors++;
      }
      var _valid6 = _errs71 === errors;
      valid13 = valid13 || _valid6;
      const _errs73 = errors;
      if (data6 !== null) {
        const err49 = { instancePath: instancePath + "/show_empty_layers", schemaPath: "#/properties/show_empty_layers/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err49];
        } else {
          vErrors.push(err49);
        }
        errors++;
      }
      var _valid6 = _errs73 === errors;
      valid13 = valid13 || _valid6;
      const _errs75 = errors;
      if (!(typeof data6 == "number")) {
        const err50 = { instancePath: instancePath + "/show_empty_layers", schemaPath: "#/properties/show_empty_layers/anyOf/2/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err50];
        } else {
          vErrors.push(err50);
        }
        errors++;
      }
      var _valid6 = _errs75 === errors;
      valid13 = valid13 || _valid6;
      const _errs77 = errors;
      if (typeof data6 === "string") {
        if (!pattern6.test(data6)) {
          const err51 = { instancePath: instancePath + "/show_empty_layers", schemaPath: "#/properties/show_empty_layers/anyOf/3/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err51];
          } else {
            vErrors.push(err51);
          }
          errors++;
        }
      } else {
        const err52 = { instancePath: instancePath + "/show_empty_layers", schemaPath: "#/properties/show_empty_layers/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err52];
        } else {
          vErrors.push(err52);
        }
        errors++;
      }
      var _valid6 = _errs77 === errors;
      valid13 = valid13 || _valid6;
      if (!valid13) {
        const err53 = { instancePath: instancePath + "/show_empty_layers", schemaPath: "#/properties/show_empty_layers/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err53];
        } else {
          vErrors.push(err53);
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
    if (data.clip_to_outline !== void 0) {
      let data7 = data.clip_to_outline;
      const _errs80 = errors;
      let valid14 = false;
      const _errs81 = errors;
      if (typeof data7 !== "boolean") {
        const err54 = { instancePath: instancePath + "/clip_to_outline", schemaPath: "#/properties/clip_to_outline/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err54];
        } else {
          vErrors.push(err54);
        }
        errors++;
      }
      var _valid7 = _errs81 === errors;
      valid14 = valid14 || _valid7;
      const _errs83 = errors;
      if (data7 !== null) {
        const err55 = { instancePath: instancePath + "/clip_to_outline", schemaPath: "#/properties/clip_to_outline/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err55];
        } else {
          vErrors.push(err55);
        }
        errors++;
      }
      var _valid7 = _errs83 === errors;
      valid14 = valid14 || _valid7;
      const _errs85 = errors;
      if (!(typeof data7 == "number")) {
        const err56 = { instancePath: instancePath + "/clip_to_outline", schemaPath: "#/properties/clip_to_outline/anyOf/2/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err56];
        } else {
          vErrors.push(err56);
        }
        errors++;
      }
      var _valid7 = _errs85 === errors;
      valid14 = valid14 || _valid7;
      const _errs87 = errors;
      if (typeof data7 === "string") {
        if (!pattern6.test(data7)) {
          const err57 = { instancePath: instancePath + "/clip_to_outline", schemaPath: "#/properties/clip_to_outline/anyOf/3/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err57];
          } else {
            vErrors.push(err57);
          }
          errors++;
        }
      } else {
        const err58 = { instancePath: instancePath + "/clip_to_outline", schemaPath: "#/properties/clip_to_outline/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err58];
        } else {
          vErrors.push(err58);
        }
        errors++;
      }
      var _valid7 = _errs87 === errors;
      valid14 = valid14 || _valid7;
      if (!valid14) {
        const err59 = { instancePath: instancePath + "/clip_to_outline", schemaPath: "#/properties/clip_to_outline/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err59];
        } else {
          vErrors.push(err59);
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
    if (data.clip_holes_from_copper !== void 0) {
      let data8 = data.clip_holes_from_copper;
      const _errs90 = errors;
      let valid15 = false;
      const _errs91 = errors;
      if (typeof data8 !== "boolean") {
        const err60 = { instancePath: instancePath + "/clip_holes_from_copper", schemaPath: "#/properties/clip_holes_from_copper/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err60];
        } else {
          vErrors.push(err60);
        }
        errors++;
      }
      var _valid8 = _errs91 === errors;
      valid15 = valid15 || _valid8;
      const _errs93 = errors;
      if (data8 !== null) {
        const err61 = { instancePath: instancePath + "/clip_holes_from_copper", schemaPath: "#/properties/clip_holes_from_copper/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err61];
        } else {
          vErrors.push(err61);
        }
        errors++;
      }
      var _valid8 = _errs93 === errors;
      valid15 = valid15 || _valid8;
      const _errs95 = errors;
      if (!(typeof data8 == "number")) {
        const err62 = { instancePath: instancePath + "/clip_holes_from_copper", schemaPath: "#/properties/clip_holes_from_copper/anyOf/2/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err62];
        } else {
          vErrors.push(err62);
        }
        errors++;
      }
      var _valid8 = _errs95 === errors;
      valid15 = valid15 || _valid8;
      const _errs97 = errors;
      if (typeof data8 === "string") {
        if (!pattern6.test(data8)) {
          const err63 = { instancePath: instancePath + "/clip_holes_from_copper", schemaPath: "#/properties/clip_holes_from_copper/anyOf/3/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err63];
          } else {
            vErrors.push(err63);
          }
          errors++;
        }
      } else {
        const err64 = { instancePath: instancePath + "/clip_holes_from_copper", schemaPath: "#/properties/clip_holes_from_copper/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err64];
        } else {
          vErrors.push(err64);
        }
        errors++;
      }
      var _valid8 = _errs97 === errors;
      valid15 = valid15 || _valid8;
      if (!valid15) {
        const err65 = { instancePath: instancePath + "/clip_holes_from_copper", schemaPath: "#/properties/clip_holes_from_copper/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err65];
        } else {
          vErrors.push(err65);
        }
        errors++;
      } else {
        errors = _errs90;
        if (vErrors !== null) {
          if (_errs90) {
            vErrors.length = _errs90;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.mirror_bottom_view !== void 0) {
      let data9 = data.mirror_bottom_view;
      const _errs100 = errors;
      let valid16 = false;
      const _errs101 = errors;
      if (typeof data9 !== "boolean") {
        const err66 = { instancePath: instancePath + "/mirror_bottom_view", schemaPath: "#/properties/mirror_bottom_view/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err66];
        } else {
          vErrors.push(err66);
        }
        errors++;
      }
      var _valid9 = _errs101 === errors;
      valid16 = valid16 || _valid9;
      const _errs103 = errors;
      if (data9 !== null) {
        const err67 = { instancePath: instancePath + "/mirror_bottom_view", schemaPath: "#/properties/mirror_bottom_view/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err67];
        } else {
          vErrors.push(err67);
        }
        errors++;
      }
      var _valid9 = _errs103 === errors;
      valid16 = valid16 || _valid9;
      const _errs105 = errors;
      if (!(typeof data9 == "number")) {
        const err68 = { instancePath: instancePath + "/mirror_bottom_view", schemaPath: "#/properties/mirror_bottom_view/anyOf/2/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err68];
        } else {
          vErrors.push(err68);
        }
        errors++;
      }
      var _valid9 = _errs105 === errors;
      valid16 = valid16 || _valid9;
      const _errs107 = errors;
      if (typeof data9 === "string") {
        if (!pattern6.test(data9)) {
          const err69 = { instancePath: instancePath + "/mirror_bottom_view", schemaPath: "#/properties/mirror_bottom_view/anyOf/3/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err69];
          } else {
            vErrors.push(err69);
          }
          errors++;
        }
      } else {
        const err70 = { instancePath: instancePath + "/mirror_bottom_view", schemaPath: "#/properties/mirror_bottom_view/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err70];
        } else {
          vErrors.push(err70);
        }
        errors++;
      }
      var _valid9 = _errs107 === errors;
      valid16 = valid16 || _valid9;
      if (!valid16) {
        const err71 = { instancePath: instancePath + "/mirror_bottom_view", schemaPath: "#/properties/mirror_bottom_view/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err71];
        } else {
          vErrors.push(err71);
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
    if (data.svg_scale !== void 0) {
      let data10 = data.svg_scale;
      const _errs110 = errors;
      let valid17 = false;
      const _errs111 = errors;
      if (typeof data10 == "number") {
        if (data10 <= 0 || isNaN(data10)) {
          const err72 = { instancePath: instancePath + "/svg_scale", schemaPath: "#/properties/svg_scale/anyOf/0/exclusiveMinimum", keyword: "exclusiveMinimum", params: { comparison: ">", limit: 0 }, message: "must be > 0" };
          if (vErrors === null) {
            vErrors = [err72];
          } else {
            vErrors.push(err72);
          }
          errors++;
        }
      } else {
        const err73 = { instancePath: instancePath + "/svg_scale", schemaPath: "#/properties/svg_scale/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err73];
        } else {
          vErrors.push(err73);
        }
        errors++;
      }
      var _valid10 = _errs111 === errors;
      valid17 = valid17 || _valid10;
      const _errs113 = errors;
      if (data10 !== null) {
        const err74 = { instancePath: instancePath + "/svg_scale", schemaPath: "#/properties/svg_scale/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err74];
        } else {
          vErrors.push(err74);
        }
        errors++;
      }
      var _valid10 = _errs113 === errors;
      valid17 = valid17 || _valid10;
      const _errs115 = errors;
      if (typeof data10 !== "boolean") {
        const err75 = { instancePath: instancePath + "/svg_scale", schemaPath: "#/properties/svg_scale/anyOf/2/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err75];
        } else {
          vErrors.push(err75);
        }
        errors++;
      }
      var _valid10 = _errs115 === errors;
      valid17 = valid17 || _valid10;
      const _errs117 = errors;
      if (typeof data10 === "string") {
        if (!pattern5.test(data10)) {
          const err76 = { instancePath: instancePath + "/svg_scale", schemaPath: "#/properties/svg_scale/anyOf/3/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
          if (vErrors === null) {
            vErrors = [err76];
          } else {
            vErrors.push(err76);
          }
          errors++;
        }
      } else {
        const err77 = { instancePath: instancePath + "/svg_scale", schemaPath: "#/properties/svg_scale/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err77];
        } else {
          vErrors.push(err77);
        }
        errors++;
      }
      var _valid10 = _errs117 === errors;
      valid17 = valid17 || _valid10;
      if (!valid17) {
        const err78 = { instancePath: instancePath + "/svg_scale", schemaPath: "#/properties/svg_scale/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err78];
        } else {
          vErrors.push(err78);
        }
        errors++;
      } else {
        errors = _errs110;
        if (vErrors !== null) {
          if (_errs110) {
            vErrors.length = _errs110;
          } else {
            vErrors = null;
          }
        }
      }
      if (typeof data10 === "string" || typeof data10 === "boolean") {
        if (!Number.isFinite(Number(data10))) {
          const err79 = { instancePath: instancePath + "/svg_scale", schemaPath: "#/properties/svg_scale/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err79];
          } else {
            vErrors.push(err79);
          }
          errors++;
        }
        if (Number(data10) <= 0) {
          const err80 = { instancePath: instancePath + "/svg_scale", schemaPath: "#/properties/svg_scale/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
          if (vErrors === null) {
            vErrors = [err80];
          } else {
            vErrors.push(err80);
          }
          errors++;
        }
      }
    }
    if (data.svg_size_unit !== void 0) {
      let data11 = data.svg_size_unit;
      const _errs120 = errors;
      let valid18 = false;
      const _errs121 = errors;
      if (typeof data11 !== "string") {
        const err81 = { instancePath: instancePath + "/svg_size_unit", schemaPath: "#/properties/svg_size_unit/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err81];
        } else {
          vErrors.push(err81);
        }
        errors++;
      }
      var _valid11 = _errs121 === errors;
      valid18 = valid18 || _valid11;
      const _errs123 = errors;
      if (data11 !== null) {
        const err82 = { instancePath: instancePath + "/svg_size_unit", schemaPath: "#/properties/svg_size_unit/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err82];
        } else {
          vErrors.push(err82);
        }
        errors++;
      }
      var _valid11 = _errs123 === errors;
      valid18 = valid18 || _valid11;
      if (!valid18) {
        const err83 = { instancePath: instancePath + "/svg_size_unit", schemaPath: "#/properties/svg_size_unit/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err83];
        } else {
          vErrors.push(err83);
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
    if (data.clean_output !== void 0) {
      let data12 = data.clean_output;
      const _errs126 = errors;
      let valid19 = false;
      const _errs127 = errors;
      if (typeof data12 !== "boolean") {
        const err84 = { instancePath: instancePath + "/clean_output", schemaPath: "#/properties/clean_output/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err84];
        } else {
          vErrors.push(err84);
        }
        errors++;
      }
      var _valid12 = _errs127 === errors;
      valid19 = valid19 || _valid12;
      const _errs129 = errors;
      if (data12 !== null) {
        const err85 = { instancePath: instancePath + "/clean_output", schemaPath: "#/properties/clean_output/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err85];
        } else {
          vErrors.push(err85);
        }
        errors++;
      }
      var _valid12 = _errs129 === errors;
      valid19 = valid19 || _valid12;
      const _errs131 = errors;
      if (!(typeof data12 == "number")) {
        const err86 = { instancePath: instancePath + "/clean_output", schemaPath: "#/properties/clean_output/anyOf/2/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err86];
        } else {
          vErrors.push(err86);
        }
        errors++;
      }
      var _valid12 = _errs131 === errors;
      valid19 = valid19 || _valid12;
      const _errs133 = errors;
      if (typeof data12 === "string") {
        if (!pattern6.test(data12)) {
          const err87 = { instancePath: instancePath + "/clean_output", schemaPath: "#/properties/clean_output/anyOf/3/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err87];
          } else {
            vErrors.push(err87);
          }
          errors++;
        }
      } else {
        const err88 = { instancePath: instancePath + "/clean_output", schemaPath: "#/properties/clean_output/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err88];
        } else {
          vErrors.push(err88);
        }
        errors++;
      }
      var _valid12 = _errs133 === errors;
      valid19 = valid19 || _valid12;
      if (!valid19) {
        const err89 = { instancePath: instancePath + "/clean_output", schemaPath: "#/properties/clean_output/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err89];
        } else {
          vErrors.push(err89);
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
    if (data.styles !== void 0) {
      let data13 = data.styles;
      const _errs136 = errors;
      let valid20 = false;
      const _errs137 = errors;
      if (!validate22(data13, { instancePath: instancePath + "/styles", parentData: data, parentDataProperty: "styles", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate22.errors : vErrors.concat(validate22.errors);
        errors = vErrors.length;
      }
      var _valid13 = _errs137 === errors;
      valid20 = valid20 || _valid13;
      const _errs138 = errors;
      if (data13 !== null) {
        const err90 = { instancePath: instancePath + "/styles", schemaPath: "#/properties/styles/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err90];
        } else {
          vErrors.push(err90);
        }
        errors++;
      }
      var _valid13 = _errs138 === errors;
      valid20 = valid20 || _valid13;
      if (!valid20) {
        const err91 = { instancePath: instancePath + "/styles", schemaPath: "#/properties/styles/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err91];
        } else {
          vErrors.push(err91);
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
  } else {
    const err92 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err92];
    } else {
      vErrors.push(err92);
    }
    errors++;
  }
  validate21.errors = vErrors;
  return errors === 0;
}
validate21.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
var pattern77 = new RegExp("^\\s*(?:[tT][oO][pP]|[bB][oO][tT][tT][oO][mM]|[tT][oO][pP][lL][aA][yY][eE][rR]|[bB][oO][tT][tT][oO][mM][lL][aA][yY][eE][rR]|[tT][oO][pP]_[lL][aA][yY][eE][rR]|[bB][oO][tT][tT][oO][mM]_[lL][aA][yY][eE][rR]|[tT][oO][pP]-[lL][aA][yY][eE][rR]|[bB][oO][tT][tT][oO][mM]-[lL][aA][yY][eE][rR])\\s*$", "u");
var pattern69 = new RegExp("^\\s*(?:[dD][eE][tT][aA][iI][lL]|[oO][uU][tT][lL][iI][nN][eE]|[sS][iI][mM][pP][lL][eE]|[bB][oO][uU][nN][dD][iI][nN][gG]_[bB][oO][xX]|[nN][oO][nN][eE]|[sS][iI][lL][hH][oO][uU][eE][tT][tT][eE]|[pP][rR][oO][fF][iI][lL][eE]|[bB][oO][uU][nN][dD][iI][nN][gG]-[bB][oO][xX]|[bB][bB][oO][xX]|[bB][oO][xX]|[bB][oO][uU][nN][dD][sS]|[oO][fF][fF]|[dD][iI][sS][aA][bB][lL][eE][dD])\\s*$", "u");
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
    if (data.side !== void 0) {
      let data0 = data.side;
      const _errs2 = errors;
      let valid1 = false;
      const _errs3 = errors;
      const _errs4 = errors;
      let valid2 = false;
      const _errs5 = errors;
      if (typeof data0 !== "string") {
        const err0 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err0];
        } else {
          vErrors.push(err0);
        }
        errors++;
      }
      if ("top" !== data0) {
        const err1 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/anyOf/0/const", keyword: "const", params: { allowedValue: "top" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      var _valid1 = _errs5 === errors;
      valid2 = valid2 || _valid1;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err2 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      if ("bottom" !== data0) {
        const err3 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/anyOf/1/const", keyword: "const", params: { allowedValue: "bottom" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      var _valid1 = _errs7 === errors;
      valid2 = valid2 || _valid1;
      const _errs9 = errors;
      if (typeof data0 !== "string") {
        const err4 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      if ("toplayer" !== data0) {
        const err5 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/anyOf/2/const", keyword: "const", params: { allowedValue: "toplayer" }, message: "must be equal to constant" };
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
      if (typeof data0 !== "string") {
        const err6 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      if ("bottomlayer" !== data0) {
        const err7 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/anyOf/3/const", keyword: "const", params: { allowedValue: "bottomlayer" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid1 = _errs11 === errors;
      valid2 = valid2 || _valid1;
      const _errs13 = errors;
      if (typeof data0 !== "string") {
        const err8 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/anyOf/4/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      if ("top_layer" !== data0) {
        const err9 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/anyOf/4/const", keyword: "const", params: { allowedValue: "top_layer" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid1 = _errs13 === errors;
      valid2 = valid2 || _valid1;
      const _errs15 = errors;
      if (typeof data0 !== "string") {
        const err10 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/anyOf/5/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      if ("bottom_layer" !== data0) {
        const err11 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/anyOf/5/const", keyword: "const", params: { allowedValue: "bottom_layer" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      valid2 = valid2 || _valid1;
      const _errs17 = errors;
      if (typeof data0 !== "string") {
        const err12 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/anyOf/6/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("top-layer" !== data0) {
        const err13 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/anyOf/6/const", keyword: "const", params: { allowedValue: "top-layer" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid1 = _errs17 === errors;
      valid2 = valid2 || _valid1;
      const _errs19 = errors;
      if (typeof data0 !== "string") {
        const err14 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/anyOf/7/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      if ("bottom-layer" !== data0) {
        const err15 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/anyOf/7/const", keyword: "const", params: { allowedValue: "bottom-layer" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid1 = _errs19 === errors;
      valid2 = valid2 || _valid1;
      const _errs21 = errors;
      if (data0 !== null) {
        const err16 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/anyOf/8/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid1 = _errs21 === errors;
      valid2 = valid2 || _valid1;
      if (!valid2) {
        const err17 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
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
      var _valid0 = _errs3 === errors;
      valid1 = valid1 || _valid0;
      const _errs23 = errors;
      if (data0 !== null) {
        const err18 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
      var _valid0 = _errs23 === errors;
      valid1 = valid1 || _valid0;
      const _errs25 = errors;
      if (typeof data0 === "string") {
        if (!pattern77.test(data0)) {
          const err19 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:[tT][oO][pP]|[bB][oO][tT][tT][oO][mM]|[tT][oO][pP][lL][aA][yY][eE][rR]|[bB][oO][tT][tT][oO][mM][lL][aA][yY][eE][rR]|[tT][oO][pP]_[lL][aA][yY][eE][rR]|[bB][oO][tT][tT][oO][mM]_[lL][aA][yY][eE][rR]|[tT][oO][pP]-[lL][aA][yY][eE][rR]|[bB][oO][tT][tT][oO][mM]-[lL][aA][yY][eE][rR])\\s*$" }, message: 'must match pattern "^\\s*(?:[tT][oO][pP]|[bB][oO][tT][tT][oO][mM]|[tT][oO][pP][lL][aA][yY][eE][rR]|[bB][oO][tT][tT][oO][mM][lL][aA][yY][eE][rR]|[tT][oO][pP]_[lL][aA][yY][eE][rR]|[bB][oO][tT][tT][oO][mM]_[lL][aA][yY][eE][rR]|[tT][oO][pP]-[lL][aA][yY][eE][rR]|[bB][oO][tT][tT][oO][mM]-[lL][aA][yY][eE][rR])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err19];
          } else {
            vErrors.push(err19);
          }
          errors++;
        }
      } else {
        const err20 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      var _valid0 = _errs25 === errors;
      valid1 = valid1 || _valid0;
      if (!valid1) {
        const err21 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
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
    if (data.projection !== void 0) {
      let data1 = data.projection;
      const _errs28 = errors;
      let valid3 = false;
      const _errs29 = errors;
      const _errs30 = errors;
      let valid4 = false;
      const _errs31 = errors;
      if (typeof data1 !== "string") {
        const err22 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
      if ("detail" !== data1) {
        const err23 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/0/const", keyword: "const", params: { allowedValue: "detail" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      var _valid3 = _errs31 === errors;
      valid4 = valid4 || _valid3;
      const _errs33 = errors;
      if (typeof data1 !== "string") {
        const err24 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      if ("outline" !== data1) {
        const err25 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/1/const", keyword: "const", params: { allowedValue: "outline" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
      var _valid3 = _errs33 === errors;
      valid4 = valid4 || _valid3;
      const _errs35 = errors;
      if (typeof data1 !== "string") {
        const err26 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
      if ("simple" !== data1) {
        const err27 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/2/const", keyword: "const", params: { allowedValue: "simple" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
      var _valid3 = _errs35 === errors;
      valid4 = valid4 || _valid3;
      const _errs37 = errors;
      if (typeof data1 !== "string") {
        const err28 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
      if ("bounding_box" !== data1) {
        const err29 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/3/const", keyword: "const", params: { allowedValue: "bounding_box" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      }
      var _valid3 = _errs37 === errors;
      valid4 = valid4 || _valid3;
      const _errs39 = errors;
      if (typeof data1 !== "string") {
        const err30 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/4/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
        }
        errors++;
      }
      if ("none" !== data1) {
        const err31 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/4/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      }
      var _valid3 = _errs39 === errors;
      valid4 = valid4 || _valid3;
      const _errs41 = errors;
      if (typeof data1 !== "string") {
        const err32 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/5/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
        }
        errors++;
      }
      if ("silhouette" !== data1) {
        const err33 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/5/const", keyword: "const", params: { allowedValue: "silhouette" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
      var _valid3 = _errs41 === errors;
      valid4 = valid4 || _valid3;
      const _errs43 = errors;
      if (typeof data1 !== "string") {
        const err34 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/6/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
        }
        errors++;
      }
      if ("profile" !== data1) {
        const err35 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/6/const", keyword: "const", params: { allowedValue: "profile" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err35];
        } else {
          vErrors.push(err35);
        }
        errors++;
      }
      var _valid3 = _errs43 === errors;
      valid4 = valid4 || _valid3;
      const _errs45 = errors;
      if (typeof data1 !== "string") {
        const err36 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/7/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err36];
        } else {
          vErrors.push(err36);
        }
        errors++;
      }
      if ("bounding-box" !== data1) {
        const err37 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/7/const", keyword: "const", params: { allowedValue: "bounding-box" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err37];
        } else {
          vErrors.push(err37);
        }
        errors++;
      }
      var _valid3 = _errs45 === errors;
      valid4 = valid4 || _valid3;
      const _errs47 = errors;
      if (typeof data1 !== "string") {
        const err38 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/8/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err38];
        } else {
          vErrors.push(err38);
        }
        errors++;
      }
      if ("bbox" !== data1) {
        const err39 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/8/const", keyword: "const", params: { allowedValue: "bbox" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err39];
        } else {
          vErrors.push(err39);
        }
        errors++;
      }
      var _valid3 = _errs47 === errors;
      valid4 = valid4 || _valid3;
      const _errs49 = errors;
      if (typeof data1 !== "string") {
        const err40 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/9/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err40];
        } else {
          vErrors.push(err40);
        }
        errors++;
      }
      if ("box" !== data1) {
        const err41 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/9/const", keyword: "const", params: { allowedValue: "box" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err41];
        } else {
          vErrors.push(err41);
        }
        errors++;
      }
      var _valid3 = _errs49 === errors;
      valid4 = valid4 || _valid3;
      const _errs51 = errors;
      if (typeof data1 !== "string") {
        const err42 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/10/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err42];
        } else {
          vErrors.push(err42);
        }
        errors++;
      }
      if ("bounds" !== data1) {
        const err43 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/10/const", keyword: "const", params: { allowedValue: "bounds" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err43];
        } else {
          vErrors.push(err43);
        }
        errors++;
      }
      var _valid3 = _errs51 === errors;
      valid4 = valid4 || _valid3;
      const _errs53 = errors;
      if (typeof data1 !== "string") {
        const err44 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/11/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err44];
        } else {
          vErrors.push(err44);
        }
        errors++;
      }
      if ("off" !== data1) {
        const err45 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/11/const", keyword: "const", params: { allowedValue: "off" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err45];
        } else {
          vErrors.push(err45);
        }
        errors++;
      }
      var _valid3 = _errs53 === errors;
      valid4 = valid4 || _valid3;
      const _errs55 = errors;
      if (typeof data1 !== "string") {
        const err46 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/12/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err46];
        } else {
          vErrors.push(err46);
        }
        errors++;
      }
      if ("disabled" !== data1) {
        const err47 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/12/const", keyword: "const", params: { allowedValue: "disabled" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err47];
        } else {
          vErrors.push(err47);
        }
        errors++;
      }
      var _valid3 = _errs55 === errors;
      valid4 = valid4 || _valid3;
      const _errs57 = errors;
      if (data1 !== null) {
        const err48 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf/13/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err48];
        } else {
          vErrors.push(err48);
        }
        errors++;
      }
      var _valid3 = _errs57 === errors;
      valid4 = valid4 || _valid3;
      if (!valid4) {
        const err49 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/0/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err49];
        } else {
          vErrors.push(err49);
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
      var _valid2 = _errs29 === errors;
      valid3 = valid3 || _valid2;
      const _errs59 = errors;
      if (data1 !== null) {
        const err50 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err50];
        } else {
          vErrors.push(err50);
        }
        errors++;
      }
      var _valid2 = _errs59 === errors;
      valid3 = valid3 || _valid2;
      const _errs61 = errors;
      if (typeof data1 === "string") {
        if (!pattern69.test(data1)) {
          const err51 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:[dD][eE][tT][aA][iI][lL]|[oO][uU][tT][lL][iI][nN][eE]|[sS][iI][mM][pP][lL][eE]|[bB][oO][uU][nN][dD][iI][nN][gG]_[bB][oO][xX]|[nN][oO][nN][eE]|[sS][iI][lL][hH][oO][uU][eE][tT][tT][eE]|[pP][rR][oO][fF][iI][lL][eE]|[bB][oO][uU][nN][dD][iI][nN][gG]-[bB][oO][xX]|[bB][bB][oO][xX]|[bB][oO][xX]|[bB][oO][uU][nN][dD][sS]|[oO][fF][fF]|[dD][iI][sS][aA][bB][lL][eE][dD])\\s*$" }, message: 'must match pattern "^\\s*(?:[dD][eE][tT][aA][iI][lL]|[oO][uU][tT][lL][iI][nN][eE]|[sS][iI][mM][pP][lL][eE]|[bB][oO][uU][nN][dD][iI][nN][gG]_[bB][oO][xX]|[nN][oO][nN][eE]|[sS][iI][lL][hH][oO][uU][eE][tT][tT][eE]|[pP][rR][oO][fF][iI][lL][eE]|[bB][oO][uU][nN][dD][iI][nN][gG]-[bB][oO][xX]|[bB][bB][oO][xX]|[bB][oO][xX]|[bB][oO][uU][nN][dD][sS]|[oO][fF][fF]|[dD][iI][sS][aA][bB][lL][eE][dD])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err51];
          } else {
            vErrors.push(err51);
          }
          errors++;
        }
      } else {
        const err52 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err52];
        } else {
          vErrors.push(err52);
        }
        errors++;
      }
      var _valid2 = _errs61 === errors;
      valid3 = valid3 || _valid2;
      if (!valid3) {
        const err53 = { instancePath: instancePath + "/projection", schemaPath: "#/properties/projection/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err53];
        } else {
          vErrors.push(err53);
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
    if (data.assembly_hlr !== void 0) {
      let data2 = data.assembly_hlr;
      const _errs64 = errors;
      let valid5 = false;
      const _errs65 = errors;
      if (!validate33(data2, { instancePath: instancePath + "/assembly_hlr", parentData: data, parentDataProperty: "assembly_hlr", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate33.errors : vErrors.concat(validate33.errors);
        errors = vErrors.length;
      }
      var _valid4 = _errs65 === errors;
      valid5 = valid5 || _valid4;
      const _errs66 = errors;
      if (data2 !== null) {
        const err54 = { instancePath: instancePath + "/assembly_hlr", schemaPath: "#/properties/assembly_hlr/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err54];
        } else {
          vErrors.push(err54);
        }
        errors++;
      }
      var _valid4 = _errs66 === errors;
      valid5 = valid5 || _valid4;
      if (!valid5) {
        const err55 = { instancePath: instancePath + "/assembly_hlr", schemaPath: "#/properties/assembly_hlr/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err55];
        } else {
          vErrors.push(err55);
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
    if (data.pin1_enabled !== void 0) {
      let data3 = data.pin1_enabled;
      const _errs69 = errors;
      let valid6 = false;
      const _errs70 = errors;
      const _errs71 = errors;
      let valid7 = false;
      const _errs72 = errors;
      if (typeof data3 !== "boolean") {
        const err56 = { instancePath: instancePath + "/pin1_enabled", schemaPath: "#/properties/pin1_enabled/anyOf/0/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err56];
        } else {
          vErrors.push(err56);
        }
        errors++;
      }
      var _valid6 = _errs72 === errors;
      valid7 = valid7 || _valid6;
      const _errs74 = errors;
      if (data3 !== null) {
        const err57 = { instancePath: instancePath + "/pin1_enabled", schemaPath: "#/properties/pin1_enabled/anyOf/0/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err57];
        } else {
          vErrors.push(err57);
        }
        errors++;
      }
      var _valid6 = _errs74 === errors;
      valid7 = valid7 || _valid6;
      if (!valid7) {
        const err58 = { instancePath: instancePath + "/pin1_enabled", schemaPath: "#/properties/pin1_enabled/anyOf/0/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err58];
        } else {
          vErrors.push(err58);
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
      var _valid5 = _errs70 === errors;
      valid6 = valid6 || _valid5;
      const _errs76 = errors;
      if (data3 !== null) {
        const err59 = { instancePath: instancePath + "/pin1_enabled", schemaPath: "#/properties/pin1_enabled/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err59];
        } else {
          vErrors.push(err59);
        }
        errors++;
      }
      var _valid5 = _errs76 === errors;
      valid6 = valid6 || _valid5;
      const _errs78 = errors;
      if (!(typeof data3 == "number")) {
        const err60 = { instancePath: instancePath + "/pin1_enabled", schemaPath: "#/properties/pin1_enabled/anyOf/2/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err60];
        } else {
          vErrors.push(err60);
        }
        errors++;
      }
      var _valid5 = _errs78 === errors;
      valid6 = valid6 || _valid5;
      const _errs80 = errors;
      if (typeof data3 === "string") {
        if (!pattern6.test(data3)) {
          const err61 = { instancePath: instancePath + "/pin1_enabled", schemaPath: "#/properties/pin1_enabled/anyOf/3/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err61];
          } else {
            vErrors.push(err61);
          }
          errors++;
        }
      } else {
        const err62 = { instancePath: instancePath + "/pin1_enabled", schemaPath: "#/properties/pin1_enabled/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err62];
        } else {
          vErrors.push(err62);
        }
        errors++;
      }
      var _valid5 = _errs80 === errors;
      valid6 = valid6 || _valid5;
      if (!valid6) {
        const err63 = { instancePath: instancePath + "/pin1_enabled", schemaPath: "#/properties/pin1_enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err63];
        } else {
          vErrors.push(err63);
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
    if (data.pin1_pad !== void 0) {
      let data4 = data.pin1_pad;
      const _errs83 = errors;
      let valid8 = false;
      const _errs84 = errors;
      if (typeof data4 !== "string") {
        const err64 = { instancePath: instancePath + "/pin1_pad", schemaPath: "#/properties/pin1_pad/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err64];
        } else {
          vErrors.push(err64);
        }
        errors++;
      }
      var _valid7 = _errs84 === errors;
      valid8 = valid8 || _valid7;
      const _errs86 = errors;
      if (data4 !== null) {
        const err65 = { instancePath: instancePath + "/pin1_pad", schemaPath: "#/properties/pin1_pad/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err65];
        } else {
          vErrors.push(err65);
        }
        errors++;
      }
      var _valid7 = _errs86 === errors;
      valid8 = valid8 || _valid7;
      if (!valid8) {
        const err66 = { instancePath: instancePath + "/pin1_pad", schemaPath: "#/properties/pin1_pad/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err66];
        } else {
          vErrors.push(err66);
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
    if (data.cathode_pad !== void 0) {
      let data5 = data.cathode_pad;
      const _errs89 = errors;
      let valid9 = false;
      const _errs90 = errors;
      if (typeof data5 !== "string") {
        const err67 = { instancePath: instancePath + "/cathode_pad", schemaPath: "#/properties/cathode_pad/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err67];
        } else {
          vErrors.push(err67);
        }
        errors++;
      }
      var _valid8 = _errs90 === errors;
      valid9 = valid9 || _valid8;
      const _errs92 = errors;
      if (data5 !== null) {
        const err68 = { instancePath: instancePath + "/cathode_pad", schemaPath: "#/properties/cathode_pad/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err68];
        } else {
          vErrors.push(err68);
        }
        errors++;
      }
      var _valid8 = _errs92 === errors;
      valid9 = valid9 || _valid8;
      if (!valid9) {
        const err69 = { instancePath: instancePath + "/cathode_pad", schemaPath: "#/properties/cathode_pad/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err69];
        } else {
          vErrors.push(err69);
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
    if (data.diode !== void 0) {
      let data6 = data.diode;
      const _errs95 = errors;
      let valid10 = false;
      const _errs96 = errors;
      const _errs97 = errors;
      let valid11 = false;
      const _errs98 = errors;
      if (typeof data6 !== "boolean") {
        const err70 = { instancePath: instancePath + "/diode", schemaPath: "#/properties/diode/anyOf/0/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err70];
        } else {
          vErrors.push(err70);
        }
        errors++;
      }
      var _valid10 = _errs98 === errors;
      valid11 = valid11 || _valid10;
      const _errs100 = errors;
      if (data6 !== null) {
        const err71 = { instancePath: instancePath + "/diode", schemaPath: "#/properties/diode/anyOf/0/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err71];
        } else {
          vErrors.push(err71);
        }
        errors++;
      }
      var _valid10 = _errs100 === errors;
      valid11 = valid11 || _valid10;
      if (!valid11) {
        const err72 = { instancePath: instancePath + "/diode", schemaPath: "#/properties/diode/anyOf/0/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err72];
        } else {
          vErrors.push(err72);
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
      var _valid9 = _errs96 === errors;
      valid10 = valid10 || _valid9;
      const _errs102 = errors;
      if (data6 !== null) {
        const err73 = { instancePath: instancePath + "/diode", schemaPath: "#/properties/diode/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err73];
        } else {
          vErrors.push(err73);
        }
        errors++;
      }
      var _valid9 = _errs102 === errors;
      valid10 = valid10 || _valid9;
      const _errs104 = errors;
      if (!(typeof data6 == "number")) {
        const err74 = { instancePath: instancePath + "/diode", schemaPath: "#/properties/diode/anyOf/2/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err74];
        } else {
          vErrors.push(err74);
        }
        errors++;
      }
      var _valid9 = _errs104 === errors;
      valid10 = valid10 || _valid9;
      const _errs106 = errors;
      if (typeof data6 === "string") {
        if (!pattern6.test(data6)) {
          const err75 = { instancePath: instancePath + "/diode", schemaPath: "#/properties/diode/anyOf/3/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err75];
          } else {
            vErrors.push(err75);
          }
          errors++;
        }
      } else {
        const err76 = { instancePath: instancePath + "/diode", schemaPath: "#/properties/diode/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err76];
        } else {
          vErrors.push(err76);
        }
        errors++;
      }
      var _valid9 = _errs106 === errors;
      valid10 = valid10 || _valid9;
      if (!valid10) {
        const err77 = { instancePath: instancePath + "/diode", schemaPath: "#/properties/diode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err77];
        } else {
          vErrors.push(err77);
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
    if (data.diode_line_art !== void 0) {
      let data7 = data.diode_line_art;
      const _errs109 = errors;
      let valid12 = false;
      const _errs110 = errors;
      const _errs111 = errors;
      let valid13 = false;
      const _errs112 = errors;
      if (typeof data7 !== "boolean") {
        const err78 = { instancePath: instancePath + "/diode_line_art", schemaPath: "#/properties/diode_line_art/anyOf/0/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err78];
        } else {
          vErrors.push(err78);
        }
        errors++;
      }
      var _valid12 = _errs112 === errors;
      valid13 = valid13 || _valid12;
      const _errs114 = errors;
      if (data7 !== null) {
        const err79 = { instancePath: instancePath + "/diode_line_art", schemaPath: "#/properties/diode_line_art/anyOf/0/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err79];
        } else {
          vErrors.push(err79);
        }
        errors++;
      }
      var _valid12 = _errs114 === errors;
      valid13 = valid13 || _valid12;
      if (!valid13) {
        const err80 = { instancePath: instancePath + "/diode_line_art", schemaPath: "#/properties/diode_line_art/anyOf/0/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err80];
        } else {
          vErrors.push(err80);
        }
        errors++;
      } else {
        errors = _errs111;
        if (vErrors !== null) {
          if (_errs111) {
            vErrors.length = _errs111;
          } else {
            vErrors = null;
          }
        }
      }
      var _valid11 = _errs110 === errors;
      valid12 = valid12 || _valid11;
      const _errs116 = errors;
      if (data7 !== null) {
        const err81 = { instancePath: instancePath + "/diode_line_art", schemaPath: "#/properties/diode_line_art/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err81];
        } else {
          vErrors.push(err81);
        }
        errors++;
      }
      var _valid11 = _errs116 === errors;
      valid12 = valid12 || _valid11;
      const _errs118 = errors;
      if (!(typeof data7 == "number")) {
        const err82 = { instancePath: instancePath + "/diode_line_art", schemaPath: "#/properties/diode_line_art/anyOf/2/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err82];
        } else {
          vErrors.push(err82);
        }
        errors++;
      }
      var _valid11 = _errs118 === errors;
      valid12 = valid12 || _valid11;
      const _errs120 = errors;
      if (typeof data7 === "string") {
        if (!pattern6.test(data7)) {
          const err83 = { instancePath: instancePath + "/diode_line_art", schemaPath: "#/properties/diode_line_art/anyOf/3/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err83];
          } else {
            vErrors.push(err83);
          }
          errors++;
        }
      } else {
        const err84 = { instancePath: instancePath + "/diode_line_art", schemaPath: "#/properties/diode_line_art/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err84];
        } else {
          vErrors.push(err84);
        }
        errors++;
      }
      var _valid11 = _errs120 === errors;
      valid12 = valid12 || _valid11;
      if (!valid12) {
        const err85 = { instancePath: instancePath + "/diode_line_art", schemaPath: "#/properties/diode_line_art/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err85];
        } else {
          vErrors.push(err85);
        }
        errors++;
      } else {
        errors = _errs109;
        if (vErrors !== null) {
          if (_errs109) {
            vErrors.length = _errs109;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.show_designator !== void 0) {
      let data8 = data.show_designator;
      const _errs123 = errors;
      let valid14 = false;
      const _errs124 = errors;
      const _errs125 = errors;
      let valid15 = false;
      const _errs126 = errors;
      if (typeof data8 !== "boolean") {
        const err86 = { instancePath: instancePath + "/show_designator", schemaPath: "#/properties/show_designator/anyOf/0/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err86];
        } else {
          vErrors.push(err86);
        }
        errors++;
      }
      var _valid14 = _errs126 === errors;
      valid15 = valid15 || _valid14;
      const _errs128 = errors;
      if (data8 !== null) {
        const err87 = { instancePath: instancePath + "/show_designator", schemaPath: "#/properties/show_designator/anyOf/0/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err87];
        } else {
          vErrors.push(err87);
        }
        errors++;
      }
      var _valid14 = _errs128 === errors;
      valid15 = valid15 || _valid14;
      if (!valid15) {
        const err88 = { instancePath: instancePath + "/show_designator", schemaPath: "#/properties/show_designator/anyOf/0/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err88];
        } else {
          vErrors.push(err88);
        }
        errors++;
      } else {
        errors = _errs125;
        if (vErrors !== null) {
          if (_errs125) {
            vErrors.length = _errs125;
          } else {
            vErrors = null;
          }
        }
      }
      var _valid13 = _errs124 === errors;
      valid14 = valid14 || _valid13;
      const _errs130 = errors;
      if (data8 !== null) {
        const err89 = { instancePath: instancePath + "/show_designator", schemaPath: "#/properties/show_designator/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err89];
        } else {
          vErrors.push(err89);
        }
        errors++;
      }
      var _valid13 = _errs130 === errors;
      valid14 = valid14 || _valid13;
      const _errs132 = errors;
      if (!(typeof data8 == "number")) {
        const err90 = { instancePath: instancePath + "/show_designator", schemaPath: "#/properties/show_designator/anyOf/2/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err90];
        } else {
          vErrors.push(err90);
        }
        errors++;
      }
      var _valid13 = _errs132 === errors;
      valid14 = valid14 || _valid13;
      const _errs134 = errors;
      if (typeof data8 === "string") {
        if (!pattern6.test(data8)) {
          const err91 = { instancePath: instancePath + "/show_designator", schemaPath: "#/properties/show_designator/anyOf/3/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err91];
          } else {
            vErrors.push(err91);
          }
          errors++;
        }
      } else {
        const err92 = { instancePath: instancePath + "/show_designator", schemaPath: "#/properties/show_designator/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err92];
        } else {
          vErrors.push(err92);
        }
        errors++;
      }
      var _valid13 = _errs134 === errors;
      valid14 = valid14 || _valid13;
      if (!valid14) {
        const err93 = { instancePath: instancePath + "/show_designator", schemaPath: "#/properties/show_designator/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err93];
        } else {
          vErrors.push(err93);
        }
        errors++;
      } else {
        errors = _errs123;
        if (vErrors !== null) {
          if (_errs123) {
            vErrors.length = _errs123;
          } else {
            vErrors = null;
          }
        }
      }
    }
    for (const key0 in data) {
      if (key0 !== "side" && key0 !== "projection" && key0 !== "assembly_hlr" && key0 !== "pin1_enabled" && key0 !== "pin1_pad" && key0 !== "cathode_pad" && key0 !== "diode" && key0 !== "diode_line_art" && key0 !== "show_designator") {
        const err94 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err94];
        } else {
          vErrors.push(err94);
        }
        errors++;
      }
    }
  } else {
    const err95 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err95];
    } else {
      vErrors.push(err95);
    }
    errors++;
  }
  validate67.errors = vErrors;
  return errors === 0;
}
validate67.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate66(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate66.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    for (const key0 in data) {
      if (!validate67(data[key0], { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), parentData: data, parentDataProperty: key0, rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate67.errors : vErrors.concat(validate67.errors);
        errors = vErrors.length;
      }
    }
  } else {
    const err0 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err0];
    } else {
      vErrors.push(err0);
    }
    errors++;
  }
  validate66.errors = vErrors;
  return errors === 0;
}
validate66.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
var pattern84 = new RegExp("^\\s*(?:[aA][uU][tT][oO]|[aA][uU][tT][oO])\\s*$", "u");
function validate71(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate71.evaluated;
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
      const _errs11 = errors;
      if (!(typeof data0 == "number")) {
        const err3 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      var _valid0 = _errs11 === errors;
      valid3 = valid3 || _valid0;
      const _errs13 = errors;
      if (typeof data0 === "string") {
        if (!pattern6.test(data0)) {
          const err4 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/3/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err4];
          } else {
            vErrors.push(err4);
          }
          errors++;
        }
      } else {
        const err5 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid0 = _errs13 === errors;
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
    if (data.layers !== void 0) {
      let data1 = data.layers;
      const _errs16 = errors;
      let valid4 = false;
      const _errs17 = errors;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data1 !== "string") {
        const err7 = { instancePath: instancePath + "/layers", schemaPath: "#/properties/layers/anyOf/0/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      if ("auto" !== data1) {
        const err8 = { instancePath: instancePath + "/layers", schemaPath: "#/properties/layers/anyOf/0/anyOf/0/const", keyword: "const", params: { allowedValue: "auto" }, message: "must be equal to constant" };
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
      if (typeof data1 !== "string") {
        const err9 = { instancePath: instancePath + "/layers", schemaPath: "#/properties/layers/anyOf/0/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      if ("AUTO" !== data1) {
        const err10 = { instancePath: instancePath + "/layers", schemaPath: "#/properties/layers/anyOf/0/anyOf/1/const", keyword: "const", params: { allowedValue: "AUTO" }, message: "must be equal to constant" };
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
      if (Array.isArray(data1)) {
        const len0 = data1.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (typeof data1[i0] !== "string") {
            const err11 = { instancePath: instancePath + "/layers/" + i0, schemaPath: "#/properties/layers/anyOf/0/anyOf/2/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err11];
            } else {
              vErrors.push(err11);
            }
            errors++;
          }
        }
      } else {
        const err12 = { instancePath: instancePath + "/layers", schemaPath: "#/properties/layers/anyOf/0/anyOf/2/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid2 = _errs23 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err13 = { instancePath: instancePath + "/layers", schemaPath: "#/properties/layers/anyOf/0/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
      var _valid1 = _errs17 === errors;
      valid4 = valid4 || _valid1;
      const _errs27 = errors;
      if (data1 !== null) {
        const err14 = { instancePath: instancePath + "/layers", schemaPath: "#/properties/layers/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid1 = _errs27 === errors;
      valid4 = valid4 || _valid1;
      const _errs29 = errors;
      if (typeof data1 === "string") {
        if (!pattern84.test(data1)) {
          const err15 = { instancePath: instancePath + "/layers", schemaPath: "#/properties/layers/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:[aA][uU][tT][oO]|[aA][uU][tT][oO])\\s*$" }, message: 'must match pattern "^\\s*(?:[aA][uU][tT][oO]|[aA][uU][tT][oO])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err15];
          } else {
            vErrors.push(err15);
          }
          errors++;
        }
      } else {
        const err16 = { instancePath: instancePath + "/layers", schemaPath: "#/properties/layers/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid1 = _errs29 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err17 = { instancePath: instancePath + "/layers", schemaPath: "#/properties/layers/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
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
    if (data.include_special_layers !== void 0) {
      let data3 = data.include_special_layers;
      const _errs32 = errors;
      let valid8 = false;
      const _errs33 = errors;
      if (Array.isArray(data3)) {
        const len1 = data3.length;
        for (let i1 = 0; i1 < len1; i1++) {
          let data4 = data3[i1];
          const _errs36 = errors;
          let valid11 = false;
          const _errs37 = errors;
          if (typeof data4 !== "string") {
            const err18 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err18];
            } else {
              vErrors.push(err18);
            }
            errors++;
          }
          if ("BOARD_SUBSTRATE" !== data4) {
            const err19 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/0/const", keyword: "const", params: { allowedValue: "BOARD_SUBSTRATE" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err19];
            } else {
              vErrors.push(err19);
            }
            errors++;
          }
          var _valid4 = _errs37 === errors;
          valid11 = valid11 || _valid4;
          const _errs39 = errors;
          if (typeof data4 !== "string") {
            const err20 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err20];
            } else {
              vErrors.push(err20);
            }
            errors++;
          }
          if ("BOARD_OUTLINE" !== data4) {
            const err21 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/1/const", keyword: "const", params: { allowedValue: "BOARD_OUTLINE" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err21];
            } else {
              vErrors.push(err21);
            }
            errors++;
          }
          var _valid4 = _errs39 === errors;
          valid11 = valid11 || _valid4;
          const _errs41 = errors;
          if (typeof data4 !== "string") {
            const err22 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err22];
            } else {
              vErrors.push(err22);
            }
            errors++;
          }
          if ("BOARD_CUTOUTS" !== data4) {
            const err23 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/2/const", keyword: "const", params: { allowedValue: "BOARD_CUTOUTS" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err23];
            } else {
              vErrors.push(err23);
            }
            errors++;
          }
          var _valid4 = _errs41 === errors;
          valid11 = valid11 || _valid4;
          const _errs43 = errors;
          if (typeof data4 !== "string") {
            const err24 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err24];
            } else {
              vErrors.push(err24);
            }
            errors++;
          }
          if ("DRILLS" !== data4) {
            const err25 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/3/const", keyword: "const", params: { allowedValue: "DRILLS" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err25];
            } else {
              vErrors.push(err25);
            }
            errors++;
          }
          var _valid4 = _errs43 === errors;
          valid11 = valid11 || _valid4;
          const _errs45 = errors;
          if (typeof data4 !== "string") {
            const err26 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/4/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err26];
            } else {
              vErrors.push(err26);
            }
            errors++;
          }
          if ("SLOTS" !== data4) {
            const err27 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/4/const", keyword: "const", params: { allowedValue: "SLOTS" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err27];
            } else {
              vErrors.push(err27);
            }
            errors++;
          }
          var _valid4 = _errs45 === errors;
          valid11 = valid11 || _valid4;
          const _errs47 = errors;
          if (typeof data4 !== "string") {
            const err28 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/5/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err28];
            } else {
              vErrors.push(err28);
            }
            errors++;
          }
          if ("ASSEMBLY_HLR_TOP" !== data4) {
            const err29 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/5/const", keyword: "const", params: { allowedValue: "ASSEMBLY_HLR_TOP" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err29];
            } else {
              vErrors.push(err29);
            }
            errors++;
          }
          var _valid4 = _errs47 === errors;
          valid11 = valid11 || _valid4;
          const _errs49 = errors;
          if (typeof data4 !== "string") {
            const err30 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/6/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err30];
            } else {
              vErrors.push(err30);
            }
            errors++;
          }
          if ("ASSEMBLY_HLR_BOTTOM" !== data4) {
            const err31 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/6/const", keyword: "const", params: { allowedValue: "ASSEMBLY_HLR_BOTTOM" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err31];
            } else {
              vErrors.push(err31);
            }
            errors++;
          }
          var _valid4 = _errs49 === errors;
          valid11 = valid11 || _valid4;
          const _errs51 = errors;
          if (typeof data4 !== "string") {
            const err32 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/7/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err32];
            } else {
              vErrors.push(err32);
            }
            errors++;
          }
          if ("ASSEMBLY_DESIGNATORS_TOP" !== data4) {
            const err33 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/7/const", keyword: "const", params: { allowedValue: "ASSEMBLY_DESIGNATORS_TOP" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err33];
            } else {
              vErrors.push(err33);
            }
            errors++;
          }
          var _valid4 = _errs51 === errors;
          valid11 = valid11 || _valid4;
          const _errs53 = errors;
          if (typeof data4 !== "string") {
            const err34 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/8/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err34];
            } else {
              vErrors.push(err34);
            }
            errors++;
          }
          if ("ASSEMBLY_DESIGNATORS_BOTTOM" !== data4) {
            const err35 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/8/const", keyword: "const", params: { allowedValue: "ASSEMBLY_DESIGNATORS_BOTTOM" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err35];
            } else {
              vErrors.push(err35);
            }
            errors++;
          }
          var _valid4 = _errs53 === errors;
          valid11 = valid11 || _valid4;
          const _errs55 = errors;
          if (typeof data4 !== "string") {
            const err36 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/9/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err36];
            } else {
              vErrors.push(err36);
            }
            errors++;
          }
          if ("PIN1_TOP" !== data4) {
            const err37 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/9/const", keyword: "const", params: { allowedValue: "PIN1_TOP" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err37];
            } else {
              vErrors.push(err37);
            }
            errors++;
          }
          var _valid4 = _errs55 === errors;
          valid11 = valid11 || _valid4;
          const _errs57 = errors;
          if (typeof data4 !== "string") {
            const err38 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/10/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err38];
            } else {
              vErrors.push(err38);
            }
            errors++;
          }
          if ("PIN1_BOTTOM" !== data4) {
            const err39 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/10/const", keyword: "const", params: { allowedValue: "PIN1_BOTTOM" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err39];
            } else {
              vErrors.push(err39);
            }
            errors++;
          }
          var _valid4 = _errs57 === errors;
          valid11 = valid11 || _valid4;
          const _errs59 = errors;
          if (typeof data4 !== "string") {
            const err40 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/11/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err40];
            } else {
              vErrors.push(err40);
            }
            errors++;
          }
          if ("SOLDERMASK_FILM_TOP" !== data4) {
            const err41 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/11/const", keyword: "const", params: { allowedValue: "SOLDERMASK_FILM_TOP" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err41];
            } else {
              vErrors.push(err41);
            }
            errors++;
          }
          var _valid4 = _errs59 === errors;
          valid11 = valid11 || _valid4;
          const _errs61 = errors;
          if (typeof data4 !== "string") {
            const err42 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/12/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err42];
            } else {
              vErrors.push(err42);
            }
            errors++;
          }
          if ("SOLDERMASK_FILM_BOTTOM" !== data4) {
            const err43 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/12/const", keyword: "const", params: { allowedValue: "SOLDERMASK_FILM_BOTTOM" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err43];
            } else {
              vErrors.push(err43);
            }
            errors++;
          }
          var _valid4 = _errs61 === errors;
          valid11 = valid11 || _valid4;
          const _errs63 = errors;
          if (typeof data4 !== "string") {
            const err44 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/13/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err44];
            } else {
              vErrors.push(err44);
            }
            errors++;
          }
          if ("ILLUSTRATION_TOP" !== data4) {
            const err45 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/13/const", keyword: "const", params: { allowedValue: "ILLUSTRATION_TOP" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err45];
            } else {
              vErrors.push(err45);
            }
            errors++;
          }
          var _valid4 = _errs63 === errors;
          valid11 = valid11 || _valid4;
          const _errs65 = errors;
          if (typeof data4 !== "string") {
            const err46 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/14/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err46];
            } else {
              vErrors.push(err46);
            }
            errors++;
          }
          if ("ILLUSTRATION_BOTTOM" !== data4) {
            const err47 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/14/const", keyword: "const", params: { allowedValue: "ILLUSTRATION_BOTTOM" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err47];
            } else {
              vErrors.push(err47);
            }
            errors++;
          }
          var _valid4 = _errs65 === errors;
          valid11 = valid11 || _valid4;
          const _errs67 = errors;
          if (typeof data4 !== "string") {
            const err48 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf/15/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err48];
            } else {
              vErrors.push(err48);
            }
            errors++;
          }
          var _valid4 = _errs67 === errors;
          valid11 = valid11 || _valid4;
          if (!valid11) {
            const err49 = { instancePath: instancePath + "/include_special_layers/" + i1, schemaPath: "#/properties/include_special_layers/anyOf/0/items/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err49];
            } else {
              vErrors.push(err49);
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
      } else {
        const err50 = { instancePath: instancePath + "/include_special_layers", schemaPath: "#/properties/include_special_layers/anyOf/0/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err50];
        } else {
          vErrors.push(err50);
        }
        errors++;
      }
      var _valid3 = _errs33 === errors;
      valid8 = valid8 || _valid3;
      const _errs69 = errors;
      if (data3 !== null) {
        const err51 = { instancePath: instancePath + "/include_special_layers", schemaPath: "#/properties/include_special_layers/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err51];
        } else {
          vErrors.push(err51);
        }
        errors++;
      }
      var _valid3 = _errs69 === errors;
      valid8 = valid8 || _valid3;
      if (!valid8) {
        const err52 = { instancePath: instancePath + "/include_special_layers", schemaPath: "#/properties/include_special_layers/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err52];
        } else {
          vErrors.push(err52);
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
    if (data.output_dir !== void 0) {
      let data5 = data.output_dir;
      const _errs72 = errors;
      let valid12 = false;
      const _errs73 = errors;
      if (typeof data5 !== "string") {
        const err53 = { instancePath: instancePath + "/output_dir", schemaPath: "#/properties/output_dir/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err53];
        } else {
          vErrors.push(err53);
        }
        errors++;
      }
      var _valid5 = _errs73 === errors;
      valid12 = valid12 || _valid5;
      const _errs75 = errors;
      if (data5 !== null) {
        const err54 = { instancePath: instancePath + "/output_dir", schemaPath: "#/properties/output_dir/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err54];
        } else {
          vErrors.push(err54);
        }
        errors++;
      }
      var _valid5 = _errs75 === errors;
      valid12 = valid12 || _valid5;
      if (!valid12) {
        const err55 = { instancePath: instancePath + "/output_dir", schemaPath: "#/properties/output_dir/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err55];
        } else {
          vErrors.push(err55);
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
  } else {
    const err56 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err56];
    } else {
      vErrors.push(err56);
    }
    errors++;
  }
  validate71.errors = vErrors;
  return errors === 0;
}
validate71.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
var func1 = require_ucs2length().default;
var pattern87 = new RegExp("^(?:[oO][uU][tT][lL][iI][nN][eE]|[sS][iI][mM][pP][lL][eE]|[dD][eE][tT][aA][iI][lL]|[dD][eE][tT][aA][iI][lL][eE][dD]|[bB][oO][uU][nN][dD][iI][nN][gG]_[bB][oO][xX]|[nN][oO][nN][eE]|[sS][iI][lL][hH][oO][uU][eE][tT][tT][eE]|[pP][rR][oO][fF][iI][lL][eE]|[bB][oO][uU][nN][dD][iI][nN][gG]-[bB][oO][xX]|[bB][bB][oO][xX]|[bB][oO][xX]|[oO][fF][fF])$", "u");
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
    if (data.name === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.name !== void 0) {
      let data0 = data.name;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err1 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err1];
          } else {
            vErrors.push(err1);
          }
          errors++;
        }
      } else {
        const err2 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
    if (data.enabled !== void 0) {
      let data1 = data.enabled;
      const _errs4 = errors;
      let valid1 = false;
      const _errs5 = errors;
      if (typeof data1 !== "boolean") {
        const err3 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      var _valid0 = _errs5 === errors;
      valid1 = valid1 || _valid0;
      const _errs7 = errors;
      if (data1 !== null) {
        const err4 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
      if (!(typeof data1 == "number")) {
        const err5 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid1 = valid1 || _valid0;
      const _errs11 = errors;
      if (typeof data1 === "string") {
        if (!pattern6.test(data1)) {
          const err6 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/3/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err6];
          } else {
            vErrors.push(err6);
          }
          errors++;
        }
      } else {
        const err7 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid0 = _errs11 === errors;
      valid1 = valid1 || _valid0;
      if (!valid1) {
        const err8 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
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
    if (data.group_id !== void 0) {
      let data2 = data.group_id;
      const _errs14 = errors;
      let valid2 = false;
      const _errs15 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/group_id", schemaPath: "#/properties/group_id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      valid2 = valid2 || _valid1;
      const _errs17 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/group_id", schemaPath: "#/properties/group_id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid1 = _errs17 === errors;
      valid2 = valid2 || _valid1;
      if (!valid2) {
        const err11 = { instancePath: instancePath + "/group_id", schemaPath: "#/properties/group_id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
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
    if (data.output_svg !== void 0) {
      let data3 = data.output_svg;
      const _errs20 = errors;
      let valid3 = false;
      const _errs21 = errors;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/output_svg", schemaPath: "#/properties/output_svg/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid3 = valid3 || _valid2;
      const _errs23 = errors;
      if (data3 !== null) {
        const err13 = { instancePath: instancePath + "/output_svg", schemaPath: "#/properties/output_svg/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid2 = _errs23 === errors;
      valid3 = valid3 || _valid2;
      if (!valid3) {
        const err14 = { instancePath: instancePath + "/output_svg", schemaPath: "#/properties/output_svg/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
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
    if (data.layers !== void 0) {
      let data4 = data.layers;
      const _errs26 = errors;
      let valid4 = false;
      const _errs27 = errors;
      if (Array.isArray(data4)) {
        const len0 = data4.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (typeof data4[i0] !== "string") {
            const err15 = { instancePath: instancePath + "/layers/" + i0, schemaPath: "#/properties/layers/anyOf/0/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err15];
            } else {
              vErrors.push(err15);
            }
            errors++;
          }
        }
      } else {
        const err16 = { instancePath: instancePath + "/layers", schemaPath: "#/properties/layers/anyOf/0/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid3 = _errs27 === errors;
      valid4 = valid4 || _valid3;
      const _errs31 = errors;
      if (data4 !== null) {
        const err17 = { instancePath: instancePath + "/layers", schemaPath: "#/properties/layers/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      var _valid3 = _errs31 === errors;
      valid4 = valid4 || _valid3;
      if (!valid4) {
        const err18 = { instancePath: instancePath + "/layers", schemaPath: "#/properties/layers/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
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
    if (data.mirror !== void 0) {
      let data6 = data.mirror;
      const _errs34 = errors;
      let valid7 = false;
      const _errs35 = errors;
      const _errs36 = errors;
      let valid8 = false;
      const _errs37 = errors;
      if (typeof data6 !== "boolean") {
        const err19 = { instancePath: instancePath + "/mirror", schemaPath: "#/properties/mirror/anyOf/0/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
      var _valid5 = _errs37 === errors;
      valid8 = valid8 || _valid5;
      const _errs39 = errors;
      if (data6 !== null) {
        const err20 = { instancePath: instancePath + "/mirror", schemaPath: "#/properties/mirror/anyOf/0/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      var _valid5 = _errs39 === errors;
      valid8 = valid8 || _valid5;
      if (!valid8) {
        const err21 = { instancePath: instancePath + "/mirror", schemaPath: "#/properties/mirror/anyOf/0/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
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
      var _valid4 = _errs35 === errors;
      valid7 = valid7 || _valid4;
      const _errs41 = errors;
      if (data6 !== null) {
        const err22 = { instancePath: instancePath + "/mirror", schemaPath: "#/properties/mirror/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
      var _valid4 = _errs41 === errors;
      valid7 = valid7 || _valid4;
      const _errs43 = errors;
      if (!(typeof data6 == "number")) {
        const err23 = { instancePath: instancePath + "/mirror", schemaPath: "#/properties/mirror/anyOf/2/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      var _valid4 = _errs43 === errors;
      valid7 = valid7 || _valid4;
      const _errs45 = errors;
      if (typeof data6 === "string") {
        if (!pattern6.test(data6)) {
          const err24 = { instancePath: instancePath + "/mirror", schemaPath: "#/properties/mirror/anyOf/3/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
          if (vErrors === null) {
            vErrors = [err24];
          } else {
            vErrors.push(err24);
          }
          errors++;
        }
      } else {
        const err25 = { instancePath: instancePath + "/mirror", schemaPath: "#/properties/mirror/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
      var _valid4 = _errs45 === errors;
      valid7 = valid7 || _valid4;
      if (!valid7) {
        const err26 = { instancePath: instancePath + "/mirror", schemaPath: "#/properties/mirror/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.assembly_hlr_mode !== void 0) {
      let data7 = data.assembly_hlr_mode;
      const _errs48 = errors;
      let valid9 = false;
      const _errs49 = errors;
      const _errs50 = errors;
      let valid10 = false;
      const _errs51 = errors;
      if (typeof data7 !== "string") {
        const err27 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/0/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
      if ("outline" !== data7) {
        const err28 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/0/anyOf/0/const", keyword: "const", params: { allowedValue: "outline" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
      var _valid7 = _errs51 === errors;
      valid10 = valid10 || _valid7;
      const _errs53 = errors;
      if (typeof data7 !== "string") {
        const err29 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/0/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      }
      if ("simple" !== data7) {
        const err30 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/0/anyOf/1/const", keyword: "const", params: { allowedValue: "simple" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
        }
        errors++;
      }
      var _valid7 = _errs53 === errors;
      valid10 = valid10 || _valid7;
      const _errs55 = errors;
      if (typeof data7 !== "string") {
        const err31 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/0/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      }
      if ("detail" !== data7) {
        const err32 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/0/anyOf/2/const", keyword: "const", params: { allowedValue: "detail" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
        }
        errors++;
      }
      var _valid7 = _errs55 === errors;
      valid10 = valid10 || _valid7;
      const _errs57 = errors;
      if (typeof data7 !== "string") {
        const err33 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/0/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
      if ("detailed" !== data7) {
        const err34 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/0/anyOf/3/const", keyword: "const", params: { allowedValue: "detailed" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
        }
        errors++;
      }
      var _valid7 = _errs57 === errors;
      valid10 = valid10 || _valid7;
      const _errs59 = errors;
      if (typeof data7 !== "string") {
        const err35 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/0/anyOf/4/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err35];
        } else {
          vErrors.push(err35);
        }
        errors++;
      }
      if ("bounding_box" !== data7) {
        const err36 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/0/anyOf/4/const", keyword: "const", params: { allowedValue: "bounding_box" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err36];
        } else {
          vErrors.push(err36);
        }
        errors++;
      }
      var _valid7 = _errs59 === errors;
      valid10 = valid10 || _valid7;
      const _errs61 = errors;
      if (typeof data7 !== "string") {
        const err37 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/0/anyOf/5/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err37];
        } else {
          vErrors.push(err37);
        }
        errors++;
      }
      if ("none" !== data7) {
        const err38 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/0/anyOf/5/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err38];
        } else {
          vErrors.push(err38);
        }
        errors++;
      }
      var _valid7 = _errs61 === errors;
      valid10 = valid10 || _valid7;
      const _errs63 = errors;
      if (typeof data7 !== "string") {
        const err39 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/0/anyOf/6/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err39];
        } else {
          vErrors.push(err39);
        }
        errors++;
      }
      if ("silhouette" !== data7) {
        const err40 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/0/anyOf/6/const", keyword: "const", params: { allowedValue: "silhouette" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err40];
        } else {
          vErrors.push(err40);
        }
        errors++;
      }
      var _valid7 = _errs63 === errors;
      valid10 = valid10 || _valid7;
      const _errs65 = errors;
      if (typeof data7 !== "string") {
        const err41 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/0/anyOf/7/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err41];
        } else {
          vErrors.push(err41);
        }
        errors++;
      }
      if ("profile" !== data7) {
        const err42 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/0/anyOf/7/const", keyword: "const", params: { allowedValue: "profile" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err42];
        } else {
          vErrors.push(err42);
        }
        errors++;
      }
      var _valid7 = _errs65 === errors;
      valid10 = valid10 || _valid7;
      const _errs67 = errors;
      if (typeof data7 !== "string") {
        const err43 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/0/anyOf/8/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err43];
        } else {
          vErrors.push(err43);
        }
        errors++;
      }
      if ("bounding-box" !== data7) {
        const err44 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/0/anyOf/8/const", keyword: "const", params: { allowedValue: "bounding-box" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err44];
        } else {
          vErrors.push(err44);
        }
        errors++;
      }
      var _valid7 = _errs67 === errors;
      valid10 = valid10 || _valid7;
      const _errs69 = errors;
      if (typeof data7 !== "string") {
        const err45 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/0/anyOf/9/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err45];
        } else {
          vErrors.push(err45);
        }
        errors++;
      }
      if ("bbox" !== data7) {
        const err46 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/0/anyOf/9/const", keyword: "const", params: { allowedValue: "bbox" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err46];
        } else {
          vErrors.push(err46);
        }
        errors++;
      }
      var _valid7 = _errs69 === errors;
      valid10 = valid10 || _valid7;
      const _errs71 = errors;
      if (typeof data7 !== "string") {
        const err47 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/0/anyOf/10/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err47];
        } else {
          vErrors.push(err47);
        }
        errors++;
      }
      if ("box" !== data7) {
        const err48 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/0/anyOf/10/const", keyword: "const", params: { allowedValue: "box" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err48];
        } else {
          vErrors.push(err48);
        }
        errors++;
      }
      var _valid7 = _errs71 === errors;
      valid10 = valid10 || _valid7;
      const _errs73 = errors;
      if (typeof data7 !== "string") {
        const err49 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/0/anyOf/11/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err49];
        } else {
          vErrors.push(err49);
        }
        errors++;
      }
      if ("off" !== data7) {
        const err50 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/0/anyOf/11/const", keyword: "const", params: { allowedValue: "off" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err50];
        } else {
          vErrors.push(err50);
        }
        errors++;
      }
      var _valid7 = _errs73 === errors;
      valid10 = valid10 || _valid7;
      if (!valid10) {
        const err51 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/0/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err51];
        } else {
          vErrors.push(err51);
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
      var _valid6 = _errs49 === errors;
      valid9 = valid9 || _valid6;
      const _errs75 = errors;
      if (data7 !== null) {
        const err52 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err52];
        } else {
          vErrors.push(err52);
        }
        errors++;
      }
      var _valid6 = _errs75 === errors;
      valid9 = valid9 || _valid6;
      const _errs77 = errors;
      if (typeof data7 === "string") {
        if (!pattern87.test(data7)) {
          const err53 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^(?:[oO][uU][tT][lL][iI][nN][eE]|[sS][iI][mM][pP][lL][eE]|[dD][eE][tT][aA][iI][lL]|[dD][eE][tT][aA][iI][lL][eE][dD]|[bB][oO][uU][nN][dD][iI][nN][gG]_[bB][oO][xX]|[nN][oO][nN][eE]|[sS][iI][lL][hH][oO][uU][eE][tT][tT][eE]|[pP][rR][oO][fF][iI][lL][eE]|[bB][oO][uU][nN][dD][iI][nN][gG]-[bB][oO][xX]|[bB][bB][oO][xX]|[bB][oO][xX]|[oO][fF][fF])$" }, message: 'must match pattern "^(?:[oO][uU][tT][lL][iI][nN][eE]|[sS][iI][mM][pP][lL][eE]|[dD][eE][tT][aA][iI][lL]|[dD][eE][tT][aA][iI][lL][eE][dD]|[bB][oO][uU][nN][dD][iI][nN][gG]_[bB][oO][xX]|[nN][oO][nN][eE]|[sS][iI][lL][hH][oO][uU][eE][tT][tT][eE]|[pP][rR][oO][fF][iI][lL][eE]|[bB][oO][uU][nN][dD][iI][nN][gG]-[bB][oO][xX]|[bB][bB][oO][xX]|[bB][oO][xX]|[oO][fF][fF])$"' };
          if (vErrors === null) {
            vErrors = [err53];
          } else {
            vErrors.push(err53);
          }
          errors++;
        }
      } else {
        const err54 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err54];
        } else {
          vErrors.push(err54);
        }
        errors++;
      }
      var _valid6 = _errs77 === errors;
      valid9 = valid9 || _valid6;
      if (!valid9) {
        const err55 = { instancePath: instancePath + "/assembly_hlr_mode", schemaPath: "#/properties/assembly_hlr_mode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err55];
        } else {
          vErrors.push(err55);
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
    if (data.styles !== void 0) {
      let data8 = data.styles;
      const _errs80 = errors;
      let valid11 = false;
      const _errs81 = errors;
      if (!validate22(data8, { instancePath: instancePath + "/styles", parentData: data, parentDataProperty: "styles", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate22.errors : vErrors.concat(validate22.errors);
        errors = vErrors.length;
      }
      var _valid8 = _errs81 === errors;
      valid11 = valid11 || _valid8;
      const _errs82 = errors;
      if (data8 !== null) {
        const err56 = { instancePath: instancePath + "/styles", schemaPath: "#/properties/styles/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err56];
        } else {
          vErrors.push(err56);
        }
        errors++;
      }
      var _valid8 = _errs82 === errors;
      valid11 = valid11 || _valid8;
      if (!valid11) {
        const err57 = { instancePath: instancePath + "/styles", schemaPath: "#/properties/styles/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err57];
        } else {
          vErrors.push(err57);
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
    if (data.description !== void 0) {
      let data9 = data.description;
      const _errs85 = errors;
      let valid12 = false;
      const _errs86 = errors;
      if (typeof data9 !== "string") {
        const err58 = { instancePath: instancePath + "/description", schemaPath: "#/properties/description/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err58];
        } else {
          vErrors.push(err58);
        }
        errors++;
      }
      var _valid9 = _errs86 === errors;
      valid12 = valid12 || _valid9;
      const _errs88 = errors;
      if (data9 !== null) {
        const err59 = { instancePath: instancePath + "/description", schemaPath: "#/properties/description/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err59];
        } else {
          vErrors.push(err59);
        }
        errors++;
      }
      var _valid9 = _errs88 === errors;
      valid12 = valid12 || _valid9;
      if (!valid12) {
        const err60 = { instancePath: instancePath + "/description", schemaPath: "#/properties/description/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err60];
        } else {
          vErrors.push(err60);
        }
        errors++;
      } else {
        errors = _errs85;
        if (vErrors !== null) {
          if (_errs85) {
            vErrors.length = _errs85;
          } else {
            vErrors = null;
          }
        }
      }
    }
    for (const key0 in data) {
      if (key0 !== "name" && key0 !== "enabled" && key0 !== "group_id" && key0 !== "output_svg" && key0 !== "layers" && key0 !== "mirror" && key0 !== "assembly_hlr_mode" && key0 !== "styles" && key0 !== "description") {
        const err61 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err61];
        } else {
          vErrors.push(err61);
        }
        errors++;
      }
    }
  } else {
    const err62 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err62];
    } else {
      vErrors.push(err62);
    }
    errors++;
  }
  validate73.errors = vErrors;
  return errors === 0;
}
validate73.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.schema !== void 0) {
      let data0 = data.schema;
      const _errs7 = errors;
      let valid3 = false;
      const _errs8 = errors;
      if (typeof data0 !== "string") {
        const err1 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      if ("pcb.svg.config.a0" !== data0) {
        const err2 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf/0/const", keyword: "const", params: { allowedValue: "pcb.svg.config.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs8 === errors;
      valid3 = valid3 || _valid0;
      const _errs10 = errors;
      if (data0 !== null) {
        const err3 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err4 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
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
    if (data.global !== void 0) {
      let data1 = data.global;
      const _errs13 = errors;
      let valid4 = false;
      const _errs14 = errors;
      if (!validate21(data1, { instancePath: instancePath + "/global", parentData: data, parentDataProperty: "global", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
        errors = vErrors.length;
      }
      var _valid1 = _errs14 === errors;
      valid4 = valid4 || _valid1;
      const _errs15 = errors;
      if (data1 !== null) {
        const err5 = { instancePath: instancePath + "/global", schemaPath: "#/properties/global/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err6 = { instancePath: instancePath + "/global", schemaPath: "#/properties/global/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
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
    if (data.assembly !== void 0) {
      let data2 = data.assembly;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (data2 && typeof data2 == "object" && !Array.isArray(data2)) {
        if (data2.default_projection !== void 0) {
          let data3 = data2.default_projection;
          const _errs23 = errors;
          let valid8 = false;
          const _errs24 = errors;
          const _errs25 = errors;
          let valid9 = false;
          const _errs26 = errors;
          if (typeof data3 !== "string") {
            const err7 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err7];
            } else {
              vErrors.push(err7);
            }
            errors++;
          }
          if ("detail" !== data3) {
            const err8 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf/0/const", keyword: "const", params: { allowedValue: "detail" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err8];
            } else {
              vErrors.push(err8);
            }
            errors++;
          }
          var _valid4 = _errs26 === errors;
          valid9 = valid9 || _valid4;
          const _errs28 = errors;
          if (typeof data3 !== "string") {
            const err9 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err9];
            } else {
              vErrors.push(err9);
            }
            errors++;
          }
          if ("outline" !== data3) {
            const err10 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf/1/const", keyword: "const", params: { allowedValue: "outline" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err10];
            } else {
              vErrors.push(err10);
            }
            errors++;
          }
          var _valid4 = _errs28 === errors;
          valid9 = valid9 || _valid4;
          const _errs30 = errors;
          if (typeof data3 !== "string") {
            const err11 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err11];
            } else {
              vErrors.push(err11);
            }
            errors++;
          }
          if ("simple" !== data3) {
            const err12 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf/2/const", keyword: "const", params: { allowedValue: "simple" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err12];
            } else {
              vErrors.push(err12);
            }
            errors++;
          }
          var _valid4 = _errs30 === errors;
          valid9 = valid9 || _valid4;
          const _errs32 = errors;
          if (typeof data3 !== "string") {
            const err13 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err13];
            } else {
              vErrors.push(err13);
            }
            errors++;
          }
          if ("bounding_box" !== data3) {
            const err14 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf/3/const", keyword: "const", params: { allowedValue: "bounding_box" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err14];
            } else {
              vErrors.push(err14);
            }
            errors++;
          }
          var _valid4 = _errs32 === errors;
          valid9 = valid9 || _valid4;
          const _errs34 = errors;
          if (typeof data3 !== "string") {
            const err15 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf/4/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err15];
            } else {
              vErrors.push(err15);
            }
            errors++;
          }
          if ("none" !== data3) {
            const err16 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf/4/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err16];
            } else {
              vErrors.push(err16);
            }
            errors++;
          }
          var _valid4 = _errs34 === errors;
          valid9 = valid9 || _valid4;
          const _errs36 = errors;
          if (typeof data3 !== "string") {
            const err17 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf/5/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err17];
            } else {
              vErrors.push(err17);
            }
            errors++;
          }
          if ("silhouette" !== data3) {
            const err18 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf/5/const", keyword: "const", params: { allowedValue: "silhouette" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err18];
            } else {
              vErrors.push(err18);
            }
            errors++;
          }
          var _valid4 = _errs36 === errors;
          valid9 = valid9 || _valid4;
          const _errs38 = errors;
          if (typeof data3 !== "string") {
            const err19 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf/6/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err19];
            } else {
              vErrors.push(err19);
            }
            errors++;
          }
          if ("profile" !== data3) {
            const err20 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf/6/const", keyword: "const", params: { allowedValue: "profile" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err20];
            } else {
              vErrors.push(err20);
            }
            errors++;
          }
          var _valid4 = _errs38 === errors;
          valid9 = valid9 || _valid4;
          const _errs40 = errors;
          if (typeof data3 !== "string") {
            const err21 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf/7/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err21];
            } else {
              vErrors.push(err21);
            }
            errors++;
          }
          if ("bounding-box" !== data3) {
            const err22 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf/7/const", keyword: "const", params: { allowedValue: "bounding-box" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err22];
            } else {
              vErrors.push(err22);
            }
            errors++;
          }
          var _valid4 = _errs40 === errors;
          valid9 = valid9 || _valid4;
          const _errs42 = errors;
          if (typeof data3 !== "string") {
            const err23 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf/8/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err23];
            } else {
              vErrors.push(err23);
            }
            errors++;
          }
          if ("bbox" !== data3) {
            const err24 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf/8/const", keyword: "const", params: { allowedValue: "bbox" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err24];
            } else {
              vErrors.push(err24);
            }
            errors++;
          }
          var _valid4 = _errs42 === errors;
          valid9 = valid9 || _valid4;
          const _errs44 = errors;
          if (typeof data3 !== "string") {
            const err25 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf/9/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err25];
            } else {
              vErrors.push(err25);
            }
            errors++;
          }
          if ("box" !== data3) {
            const err26 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf/9/const", keyword: "const", params: { allowedValue: "box" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err26];
            } else {
              vErrors.push(err26);
            }
            errors++;
          }
          var _valid4 = _errs44 === errors;
          valid9 = valid9 || _valid4;
          const _errs46 = errors;
          if (typeof data3 !== "string") {
            const err27 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf/10/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err27];
            } else {
              vErrors.push(err27);
            }
            errors++;
          }
          if ("bounds" !== data3) {
            const err28 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf/10/const", keyword: "const", params: { allowedValue: "bounds" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err28];
            } else {
              vErrors.push(err28);
            }
            errors++;
          }
          var _valid4 = _errs46 === errors;
          valid9 = valid9 || _valid4;
          const _errs48 = errors;
          if (typeof data3 !== "string") {
            const err29 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf/11/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err29];
            } else {
              vErrors.push(err29);
            }
            errors++;
          }
          if ("off" !== data3) {
            const err30 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf/11/const", keyword: "const", params: { allowedValue: "off" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err30];
            } else {
              vErrors.push(err30);
            }
            errors++;
          }
          var _valid4 = _errs48 === errors;
          valid9 = valid9 || _valid4;
          const _errs50 = errors;
          if (typeof data3 !== "string") {
            const err31 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf/12/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err31];
            } else {
              vErrors.push(err31);
            }
            errors++;
          }
          if ("disabled" !== data3) {
            const err32 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf/12/const", keyword: "const", params: { allowedValue: "disabled" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err32];
            } else {
              vErrors.push(err32);
            }
            errors++;
          }
          var _valid4 = _errs50 === errors;
          valid9 = valid9 || _valid4;
          if (!valid9) {
            const err33 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/0/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err33];
            } else {
              vErrors.push(err33);
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
          var _valid3 = _errs24 === errors;
          valid8 = valid8 || _valid3;
          const _errs52 = errors;
          if (data3 !== null) {
            const err34 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err34];
            } else {
              vErrors.push(err34);
            }
            errors++;
          }
          var _valid3 = _errs52 === errors;
          valid8 = valid8 || _valid3;
          const _errs54 = errors;
          if (typeof data3 === "string") {
            if (!pattern69.test(data3)) {
              const err35 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:[dD][eE][tT][aA][iI][lL]|[oO][uU][tT][lL][iI][nN][eE]|[sS][iI][mM][pP][lL][eE]|[bB][oO][uU][nN][dD][iI][nN][gG]_[bB][oO][xX]|[nN][oO][nN][eE]|[sS][iI][lL][hH][oO][uU][eE][tT][tT][eE]|[pP][rR][oO][fF][iI][lL][eE]|[bB][oO][uU][nN][dD][iI][nN][gG]-[bB][oO][xX]|[bB][bB][oO][xX]|[bB][oO][xX]|[bB][oO][uU][nN][dD][sS]|[oO][fF][fF]|[dD][iI][sS][aA][bB][lL][eE][dD])\\s*$" }, message: 'must match pattern "^\\s*(?:[dD][eE][tT][aA][iI][lL]|[oO][uU][tT][lL][iI][nN][eE]|[sS][iI][mM][pP][lL][eE]|[bB][oO][uU][nN][dD][iI][nN][gG]_[bB][oO][xX]|[nN][oO][nN][eE]|[sS][iI][lL][hH][oO][uU][eE][tT][tT][eE]|[pP][rR][oO][fF][iI][lL][eE]|[bB][oO][uU][nN][dD][iI][nN][gG]-[bB][oO][xX]|[bB][bB][oO][xX]|[bB][oO][xX]|[bB][oO][uU][nN][dD][sS]|[oO][fF][fF]|[dD][iI][sS][aA][bB][lL][eE][dD])\\s*$"' };
              if (vErrors === null) {
                vErrors = [err35];
              } else {
                vErrors.push(err35);
              }
              errors++;
            }
          } else {
            const err36 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err36];
            } else {
              vErrors.push(err36);
            }
            errors++;
          }
          var _valid3 = _errs54 === errors;
          valid8 = valid8 || _valid3;
          if (!valid8) {
            const err37 = { instancePath: instancePath + "/assembly/default_projection", schemaPath: "#/$defs/AssemblyOptions/properties/default_projection/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err37];
            } else {
              vErrors.push(err37);
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
        if (data2.dnp_projection !== void 0) {
          let data4 = data2.dnp_projection;
          const _errs57 = errors;
          let valid10 = false;
          const _errs58 = errors;
          const _errs59 = errors;
          let valid11 = false;
          const _errs60 = errors;
          if (typeof data4 !== "string") {
            const err38 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err38];
            } else {
              vErrors.push(err38);
            }
            errors++;
          }
          if ("detail" !== data4) {
            const err39 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf/0/const", keyword: "const", params: { allowedValue: "detail" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err39];
            } else {
              vErrors.push(err39);
            }
            errors++;
          }
          var _valid6 = _errs60 === errors;
          valid11 = valid11 || _valid6;
          const _errs62 = errors;
          if (typeof data4 !== "string") {
            const err40 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err40];
            } else {
              vErrors.push(err40);
            }
            errors++;
          }
          if ("outline" !== data4) {
            const err41 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf/1/const", keyword: "const", params: { allowedValue: "outline" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err41];
            } else {
              vErrors.push(err41);
            }
            errors++;
          }
          var _valid6 = _errs62 === errors;
          valid11 = valid11 || _valid6;
          const _errs64 = errors;
          if (typeof data4 !== "string") {
            const err42 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err42];
            } else {
              vErrors.push(err42);
            }
            errors++;
          }
          if ("simple" !== data4) {
            const err43 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf/2/const", keyword: "const", params: { allowedValue: "simple" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err43];
            } else {
              vErrors.push(err43);
            }
            errors++;
          }
          var _valid6 = _errs64 === errors;
          valid11 = valid11 || _valid6;
          const _errs66 = errors;
          if (typeof data4 !== "string") {
            const err44 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err44];
            } else {
              vErrors.push(err44);
            }
            errors++;
          }
          if ("bounding_box" !== data4) {
            const err45 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf/3/const", keyword: "const", params: { allowedValue: "bounding_box" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err45];
            } else {
              vErrors.push(err45);
            }
            errors++;
          }
          var _valid6 = _errs66 === errors;
          valid11 = valid11 || _valid6;
          const _errs68 = errors;
          if (typeof data4 !== "string") {
            const err46 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf/4/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err46];
            } else {
              vErrors.push(err46);
            }
            errors++;
          }
          if ("none" !== data4) {
            const err47 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf/4/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err47];
            } else {
              vErrors.push(err47);
            }
            errors++;
          }
          var _valid6 = _errs68 === errors;
          valid11 = valid11 || _valid6;
          const _errs70 = errors;
          if (typeof data4 !== "string") {
            const err48 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf/5/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err48];
            } else {
              vErrors.push(err48);
            }
            errors++;
          }
          if ("silhouette" !== data4) {
            const err49 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf/5/const", keyword: "const", params: { allowedValue: "silhouette" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err49];
            } else {
              vErrors.push(err49);
            }
            errors++;
          }
          var _valid6 = _errs70 === errors;
          valid11 = valid11 || _valid6;
          const _errs72 = errors;
          if (typeof data4 !== "string") {
            const err50 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf/6/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err50];
            } else {
              vErrors.push(err50);
            }
            errors++;
          }
          if ("profile" !== data4) {
            const err51 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf/6/const", keyword: "const", params: { allowedValue: "profile" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err51];
            } else {
              vErrors.push(err51);
            }
            errors++;
          }
          var _valid6 = _errs72 === errors;
          valid11 = valid11 || _valid6;
          const _errs74 = errors;
          if (typeof data4 !== "string") {
            const err52 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf/7/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err52];
            } else {
              vErrors.push(err52);
            }
            errors++;
          }
          if ("bounding-box" !== data4) {
            const err53 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf/7/const", keyword: "const", params: { allowedValue: "bounding-box" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err53];
            } else {
              vErrors.push(err53);
            }
            errors++;
          }
          var _valid6 = _errs74 === errors;
          valid11 = valid11 || _valid6;
          const _errs76 = errors;
          if (typeof data4 !== "string") {
            const err54 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf/8/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err54];
            } else {
              vErrors.push(err54);
            }
            errors++;
          }
          if ("bbox" !== data4) {
            const err55 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf/8/const", keyword: "const", params: { allowedValue: "bbox" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err55];
            } else {
              vErrors.push(err55);
            }
            errors++;
          }
          var _valid6 = _errs76 === errors;
          valid11 = valid11 || _valid6;
          const _errs78 = errors;
          if (typeof data4 !== "string") {
            const err56 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf/9/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err56];
            } else {
              vErrors.push(err56);
            }
            errors++;
          }
          if ("box" !== data4) {
            const err57 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf/9/const", keyword: "const", params: { allowedValue: "box" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err57];
            } else {
              vErrors.push(err57);
            }
            errors++;
          }
          var _valid6 = _errs78 === errors;
          valid11 = valid11 || _valid6;
          const _errs80 = errors;
          if (typeof data4 !== "string") {
            const err58 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf/10/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err58];
            } else {
              vErrors.push(err58);
            }
            errors++;
          }
          if ("bounds" !== data4) {
            const err59 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf/10/const", keyword: "const", params: { allowedValue: "bounds" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err59];
            } else {
              vErrors.push(err59);
            }
            errors++;
          }
          var _valid6 = _errs80 === errors;
          valid11 = valid11 || _valid6;
          const _errs82 = errors;
          if (typeof data4 !== "string") {
            const err60 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf/11/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err60];
            } else {
              vErrors.push(err60);
            }
            errors++;
          }
          if ("off" !== data4) {
            const err61 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf/11/const", keyword: "const", params: { allowedValue: "off" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err61];
            } else {
              vErrors.push(err61);
            }
            errors++;
          }
          var _valid6 = _errs82 === errors;
          valid11 = valid11 || _valid6;
          const _errs84 = errors;
          if (typeof data4 !== "string") {
            const err62 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf/12/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err62];
            } else {
              vErrors.push(err62);
            }
            errors++;
          }
          if ("disabled" !== data4) {
            const err63 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf/12/const", keyword: "const", params: { allowedValue: "disabled" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err63];
            } else {
              vErrors.push(err63);
            }
            errors++;
          }
          var _valid6 = _errs84 === errors;
          valid11 = valid11 || _valid6;
          if (!valid11) {
            const err64 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/0/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err64];
            } else {
              vErrors.push(err64);
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
          var _valid5 = _errs58 === errors;
          valid10 = valid10 || _valid5;
          const _errs86 = errors;
          if (data4 !== null) {
            const err65 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err65];
            } else {
              vErrors.push(err65);
            }
            errors++;
          }
          var _valid5 = _errs86 === errors;
          valid10 = valid10 || _valid5;
          const _errs88 = errors;
          if (typeof data4 === "string") {
            if (!pattern69.test(data4)) {
              const err66 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/2/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:[dD][eE][tT][aA][iI][lL]|[oO][uU][tT][lL][iI][nN][eE]|[sS][iI][mM][pP][lL][eE]|[bB][oO][uU][nN][dD][iI][nN][gG]_[bB][oO][xX]|[nN][oO][nN][eE]|[sS][iI][lL][hH][oO][uU][eE][tT][tT][eE]|[pP][rR][oO][fF][iI][lL][eE]|[bB][oO][uU][nN][dD][iI][nN][gG]-[bB][oO][xX]|[bB][bB][oO][xX]|[bB][oO][xX]|[bB][oO][uU][nN][dD][sS]|[oO][fF][fF]|[dD][iI][sS][aA][bB][lL][eE][dD])\\s*$" }, message: 'must match pattern "^\\s*(?:[dD][eE][tT][aA][iI][lL]|[oO][uU][tT][lL][iI][nN][eE]|[sS][iI][mM][pP][lL][eE]|[bB][oO][uU][nN][dD][iI][nN][gG]_[bB][oO][xX]|[nN][oO][nN][eE]|[sS][iI][lL][hH][oO][uU][eE][tT][tT][eE]|[pP][rR][oO][fF][iI][lL][eE]|[bB][oO][uU][nN][dD][iI][nN][gG]-[bB][oO][xX]|[bB][bB][oO][xX]|[bB][oO][xX]|[bB][oO][uU][nN][dD][sS]|[oO][fF][fF]|[dD][iI][sS][aA][bB][lL][eE][dD])\\s*$"' };
              if (vErrors === null) {
                vErrors = [err66];
              } else {
                vErrors.push(err66);
              }
              errors++;
            }
          } else {
            const err67 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err67];
            } else {
              vErrors.push(err67);
            }
            errors++;
          }
          var _valid5 = _errs88 === errors;
          valid10 = valid10 || _valid5;
          if (!valid10) {
            const err68 = { instancePath: instancePath + "/assembly/dnp_projection", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_projection/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err68];
            } else {
              vErrors.push(err68);
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
        if (data2.designator_color !== void 0) {
          let data5 = data2.designator_color;
          const _errs91 = errors;
          let valid12 = false;
          const _errs92 = errors;
          if (typeof data5 !== "string") {
            const err69 = { instancePath: instancePath + "/assembly/designator_color", schemaPath: "#/$defs/AssemblyOptions/properties/designator_color/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err69];
            } else {
              vErrors.push(err69);
            }
            errors++;
          }
          var _valid7 = _errs92 === errors;
          valid12 = valid12 || _valid7;
          const _errs94 = errors;
          if (data5 !== null) {
            const err70 = { instancePath: instancePath + "/assembly/designator_color", schemaPath: "#/$defs/AssemblyOptions/properties/designator_color/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err70];
            } else {
              vErrors.push(err70);
            }
            errors++;
          }
          var _valid7 = _errs94 === errors;
          valid12 = valid12 || _valid7;
          if (!valid12) {
            const err71 = { instancePath: instancePath + "/assembly/designator_color", schemaPath: "#/$defs/AssemblyOptions/properties/designator_color/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err71];
            } else {
              vErrors.push(err71);
            }
            errors++;
          } else {
            errors = _errs91;
            if (vErrors !== null) {
              if (_errs91) {
                vErrors.length = _errs91;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data2.dnp_designator_color !== void 0) {
          let data6 = data2.dnp_designator_color;
          const _errs97 = errors;
          let valid13 = false;
          const _errs98 = errors;
          if (typeof data6 !== "string") {
            const err72 = { instancePath: instancePath + "/assembly/dnp_designator_color", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_designator_color/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err72];
            } else {
              vErrors.push(err72);
            }
            errors++;
          }
          var _valid8 = _errs98 === errors;
          valid13 = valid13 || _valid8;
          const _errs100 = errors;
          if (data6 !== null) {
            const err73 = { instancePath: instancePath + "/assembly/dnp_designator_color", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_designator_color/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err73];
            } else {
              vErrors.push(err73);
            }
            errors++;
          }
          var _valid8 = _errs100 === errors;
          valid13 = valid13 || _valid8;
          if (!valid13) {
            const err74 = { instancePath: instancePath + "/assembly/dnp_designator_color", schemaPath: "#/$defs/AssemblyOptions/properties/dnp_designator_color/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err74];
            } else {
              vErrors.push(err74);
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
        for (const key1 in data2) {
          if (key1 !== "default_projection" && key1 !== "dnp_projection" && key1 !== "designator_color" && key1 !== "dnp_designator_color") {
            const err75 = { instancePath: instancePath + "/assembly/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/AssemblyOptions/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err75];
            } else {
              vErrors.push(err75);
            }
            errors++;
          }
        }
      } else {
        const err76 = { instancePath: instancePath + "/assembly", schemaPath: "#/$defs/AssemblyOptions/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err76];
        } else {
          vErrors.push(err76);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs105 = errors;
      if (data2 !== null) {
        const err77 = { instancePath: instancePath + "/assembly", schemaPath: "#/properties/assembly/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err77];
        } else {
          vErrors.push(err77);
        }
        errors++;
      }
      var _valid2 = _errs105 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err78 = { instancePath: instancePath + "/assembly", schemaPath: "#/properties/assembly/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err78];
        } else {
          vErrors.push(err78);
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
    if (data.dnp !== void 0) {
      let data8 = data.dnp;
      const _errs108 = errors;
      let valid15 = false;
      const _errs109 = errors;
      if (data8 && typeof data8 == "object" && !Array.isArray(data8)) {
        if (data8.color !== void 0) {
          let data9 = data8.color;
          const _errs113 = errors;
          let valid18 = false;
          const _errs114 = errors;
          if (typeof data9 !== "string") {
            const err79 = { instancePath: instancePath + "/dnp/color", schemaPath: "#/$defs/DnpOptions/properties/color/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err79];
            } else {
              vErrors.push(err79);
            }
            errors++;
          }
          var _valid10 = _errs114 === errors;
          valid18 = valid18 || _valid10;
          const _errs116 = errors;
          if (data9 !== null) {
            const err80 = { instancePath: instancePath + "/dnp/color", schemaPath: "#/$defs/DnpOptions/properties/color/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err80];
            } else {
              vErrors.push(err80);
            }
            errors++;
          }
          var _valid10 = _errs116 === errors;
          valid18 = valid18 || _valid10;
          if (!valid18) {
            const err81 = { instancePath: instancePath + "/dnp/color", schemaPath: "#/$defs/DnpOptions/properties/color/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err81];
            } else {
              vErrors.push(err81);
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
        if (data8.hatch !== void 0) {
          let data10 = data8.hatch;
          const _errs119 = errors;
          let valid19 = false;
          const _errs120 = errors;
          if (typeof data10 !== "boolean") {
            const err82 = { instancePath: instancePath + "/dnp/hatch", schemaPath: "#/$defs/DnpOptions/properties/hatch/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err82];
            } else {
              vErrors.push(err82);
            }
            errors++;
          }
          var _valid11 = _errs120 === errors;
          valid19 = valid19 || _valid11;
          const _errs122 = errors;
          if (data10 !== null) {
            const err83 = { instancePath: instancePath + "/dnp/hatch", schemaPath: "#/$defs/DnpOptions/properties/hatch/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err83];
            } else {
              vErrors.push(err83);
            }
            errors++;
          }
          var _valid11 = _errs122 === errors;
          valid19 = valid19 || _valid11;
          const _errs124 = errors;
          if (!(typeof data10 == "number")) {
            const err84 = { instancePath: instancePath + "/dnp/hatch", schemaPath: "#/$defs/DnpOptions/properties/hatch/anyOf/2/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err84];
            } else {
              vErrors.push(err84);
            }
            errors++;
          }
          var _valid11 = _errs124 === errors;
          valid19 = valid19 || _valid11;
          const _errs126 = errors;
          if (typeof data10 === "string") {
            if (!pattern6.test(data10)) {
              const err85 = { instancePath: instancePath + "/dnp/hatch", schemaPath: "#/$defs/DnpOptions/properties/hatch/anyOf/3/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
              if (vErrors === null) {
                vErrors = [err85];
              } else {
                vErrors.push(err85);
              }
              errors++;
            }
          } else {
            const err86 = { instancePath: instancePath + "/dnp/hatch", schemaPath: "#/$defs/DnpOptions/properties/hatch/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err86];
            } else {
              vErrors.push(err86);
            }
            errors++;
          }
          var _valid11 = _errs126 === errors;
          valid19 = valid19 || _valid11;
          if (!valid19) {
            const err87 = { instancePath: instancePath + "/dnp/hatch", schemaPath: "#/$defs/DnpOptions/properties/hatch/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err87];
            } else {
              vErrors.push(err87);
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
        if (data8.hatch_spacing_mm !== void 0) {
          let data11 = data8.hatch_spacing_mm;
          const _errs129 = errors;
          let valid20 = false;
          const _errs130 = errors;
          if (typeof data11 == "number") {
            if (data11 <= 0 || isNaN(data11)) {
              const err88 = { instancePath: instancePath + "/dnp/hatch_spacing_mm", schemaPath: "#/$defs/DnpOptions/properties/hatch_spacing_mm/anyOf/0/exclusiveMinimum", keyword: "exclusiveMinimum", params: { comparison: ">", limit: 0 }, message: "must be > 0" };
              if (vErrors === null) {
                vErrors = [err88];
              } else {
                vErrors.push(err88);
              }
              errors++;
            }
          } else {
            const err89 = { instancePath: instancePath + "/dnp/hatch_spacing_mm", schemaPath: "#/$defs/DnpOptions/properties/hatch_spacing_mm/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err89];
            } else {
              vErrors.push(err89);
            }
            errors++;
          }
          var _valid12 = _errs130 === errors;
          valid20 = valid20 || _valid12;
          const _errs132 = errors;
          if (data11 !== null) {
            const err90 = { instancePath: instancePath + "/dnp/hatch_spacing_mm", schemaPath: "#/$defs/DnpOptions/properties/hatch_spacing_mm/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err90];
            } else {
              vErrors.push(err90);
            }
            errors++;
          }
          var _valid12 = _errs132 === errors;
          valid20 = valid20 || _valid12;
          const _errs134 = errors;
          if (typeof data11 !== "boolean") {
            const err91 = { instancePath: instancePath + "/dnp/hatch_spacing_mm", schemaPath: "#/$defs/DnpOptions/properties/hatch_spacing_mm/anyOf/2/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err91];
            } else {
              vErrors.push(err91);
            }
            errors++;
          }
          var _valid12 = _errs134 === errors;
          valid20 = valid20 || _valid12;
          const _errs136 = errors;
          if (typeof data11 === "string") {
            if (!pattern5.test(data11)) {
              const err92 = { instancePath: instancePath + "/dnp/hatch_spacing_mm", schemaPath: "#/$defs/DnpOptions/properties/hatch_spacing_mm/anyOf/3/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
              if (vErrors === null) {
                vErrors = [err92];
              } else {
                vErrors.push(err92);
              }
              errors++;
            }
          } else {
            const err93 = { instancePath: instancePath + "/dnp/hatch_spacing_mm", schemaPath: "#/$defs/DnpOptions/properties/hatch_spacing_mm/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err93];
            } else {
              vErrors.push(err93);
            }
            errors++;
          }
          var _valid12 = _errs136 === errors;
          valid20 = valid20 || _valid12;
          if (!valid20) {
            const err94 = { instancePath: instancePath + "/dnp/hatch_spacing_mm", schemaPath: "#/$defs/DnpOptions/properties/hatch_spacing_mm/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err94];
            } else {
              vErrors.push(err94);
            }
            errors++;
          } else {
            errors = _errs129;
            if (vErrors !== null) {
              if (_errs129) {
                vErrors.length = _errs129;
              } else {
                vErrors = null;
              }
            }
          }
          if (typeof data11 === "string" || typeof data11 === "boolean") {
            if (!Number.isFinite(Number(data11))) {
              const err95 = { instancePath: instancePath + "/dnp/hatch_spacing_mm", schemaPath: "#/$defs/DnpOptions/properties/hatch_spacing_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
              if (vErrors === null) {
                vErrors = [err95];
              } else {
                vErrors.push(err95);
              }
              errors++;
            }
            if (Number(data11) <= 0) {
              const err96 = { instancePath: instancePath + "/dnp/hatch_spacing_mm", schemaPath: "#/$defs/DnpOptions/properties/hatch_spacing_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
              if (vErrors === null) {
                vErrors = [err96];
              } else {
                vErrors.push(err96);
              }
              errors++;
            }
          }
        }
        if (data8.hatch_angle_deg !== void 0) {
          let data12 = data8.hatch_angle_deg;
          const _errs139 = errors;
          let valid21 = false;
          const _errs140 = errors;
          if (!(typeof data12 == "number")) {
            const err97 = { instancePath: instancePath + "/dnp/hatch_angle_deg", schemaPath: "#/$defs/DnpOptions/properties/hatch_angle_deg/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err97];
            } else {
              vErrors.push(err97);
            }
            errors++;
          }
          var _valid13 = _errs140 === errors;
          valid21 = valid21 || _valid13;
          const _errs142 = errors;
          if (data12 !== null) {
            const err98 = { instancePath: instancePath + "/dnp/hatch_angle_deg", schemaPath: "#/$defs/DnpOptions/properties/hatch_angle_deg/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err98];
            } else {
              vErrors.push(err98);
            }
            errors++;
          }
          var _valid13 = _errs142 === errors;
          valid21 = valid21 || _valid13;
          const _errs144 = errors;
          if (typeof data12 !== "boolean") {
            const err99 = { instancePath: instancePath + "/dnp/hatch_angle_deg", schemaPath: "#/$defs/DnpOptions/properties/hatch_angle_deg/anyOf/2/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err99];
            } else {
              vErrors.push(err99);
            }
            errors++;
          }
          var _valid13 = _errs144 === errors;
          valid21 = valid21 || _valid13;
          const _errs146 = errors;
          if (typeof data12 === "string") {
            if (!pattern5.test(data12)) {
              const err100 = { instancePath: instancePath + "/dnp/hatch_angle_deg", schemaPath: "#/$defs/DnpOptions/properties/hatch_angle_deg/anyOf/3/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
              if (vErrors === null) {
                vErrors = [err100];
              } else {
                vErrors.push(err100);
              }
              errors++;
            }
          } else {
            const err101 = { instancePath: instancePath + "/dnp/hatch_angle_deg", schemaPath: "#/$defs/DnpOptions/properties/hatch_angle_deg/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err101];
            } else {
              vErrors.push(err101);
            }
            errors++;
          }
          var _valid13 = _errs146 === errors;
          valid21 = valid21 || _valid13;
          if (!valid21) {
            const err102 = { instancePath: instancePath + "/dnp/hatch_angle_deg", schemaPath: "#/$defs/DnpOptions/properties/hatch_angle_deg/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err102];
            } else {
              vErrors.push(err102);
            }
            errors++;
          } else {
            errors = _errs139;
            if (vErrors !== null) {
              if (_errs139) {
                vErrors.length = _errs139;
              } else {
                vErrors = null;
              }
            }
          }
          if (typeof data12 === "string" || typeof data12 === "boolean") {
            if (!Number.isFinite(Number(data12))) {
              const err103 = { instancePath: instancePath + "/dnp/hatch_angle_deg", schemaPath: "#/$defs/DnpOptions/properties/hatch_angle_deg/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
              if (vErrors === null) {
                vErrors = [err103];
              } else {
                vErrors.push(err103);
              }
              errors++;
            }
          }
        }
        if (data8.hatch_line_width_mm !== void 0) {
          let data13 = data8.hatch_line_width_mm;
          const _errs149 = errors;
          let valid22 = false;
          const _errs150 = errors;
          if (typeof data13 == "number") {
            if (data13 <= 0 || isNaN(data13)) {
              const err104 = { instancePath: instancePath + "/dnp/hatch_line_width_mm", schemaPath: "#/$defs/DnpOptions/properties/hatch_line_width_mm/anyOf/0/exclusiveMinimum", keyword: "exclusiveMinimum", params: { comparison: ">", limit: 0 }, message: "must be > 0" };
              if (vErrors === null) {
                vErrors = [err104];
              } else {
                vErrors.push(err104);
              }
              errors++;
            }
          } else {
            const err105 = { instancePath: instancePath + "/dnp/hatch_line_width_mm", schemaPath: "#/$defs/DnpOptions/properties/hatch_line_width_mm/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err105];
            } else {
              vErrors.push(err105);
            }
            errors++;
          }
          var _valid14 = _errs150 === errors;
          valid22 = valid22 || _valid14;
          const _errs152 = errors;
          if (data13 !== null) {
            const err106 = { instancePath: instancePath + "/dnp/hatch_line_width_mm", schemaPath: "#/$defs/DnpOptions/properties/hatch_line_width_mm/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err106];
            } else {
              vErrors.push(err106);
            }
            errors++;
          }
          var _valid14 = _errs152 === errors;
          valid22 = valid22 || _valid14;
          const _errs154 = errors;
          if (typeof data13 !== "boolean") {
            const err107 = { instancePath: instancePath + "/dnp/hatch_line_width_mm", schemaPath: "#/$defs/DnpOptions/properties/hatch_line_width_mm/anyOf/2/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err107];
            } else {
              vErrors.push(err107);
            }
            errors++;
          }
          var _valid14 = _errs154 === errors;
          valid22 = valid22 || _valid14;
          const _errs156 = errors;
          if (typeof data13 === "string") {
            if (!pattern5.test(data13)) {
              const err108 = { instancePath: instancePath + "/dnp/hatch_line_width_mm", schemaPath: "#/$defs/DnpOptions/properties/hatch_line_width_mm/anyOf/3/pattern", keyword: "pattern", params: { pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$" }, message: 'must match pattern "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"' };
              if (vErrors === null) {
                vErrors = [err108];
              } else {
                vErrors.push(err108);
              }
              errors++;
            }
          } else {
            const err109 = { instancePath: instancePath + "/dnp/hatch_line_width_mm", schemaPath: "#/$defs/DnpOptions/properties/hatch_line_width_mm/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err109];
            } else {
              vErrors.push(err109);
            }
            errors++;
          }
          var _valid14 = _errs156 === errors;
          valid22 = valid22 || _valid14;
          if (!valid22) {
            const err110 = { instancePath: instancePath + "/dnp/hatch_line_width_mm", schemaPath: "#/$defs/DnpOptions/properties/hatch_line_width_mm/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err110];
            } else {
              vErrors.push(err110);
            }
            errors++;
          } else {
            errors = _errs149;
            if (vErrors !== null) {
              if (_errs149) {
                vErrors.length = _errs149;
              } else {
                vErrors = null;
              }
            }
          }
          if (typeof data13 === "string" || typeof data13 === "boolean") {
            if (!Number.isFinite(Number(data13))) {
              const err111 = { instancePath: instancePath + "/dnp/hatch_line_width_mm", schemaPath: "#/$defs/DnpOptions/properties/hatch_line_width_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
              if (vErrors === null) {
                vErrors = [err111];
              } else {
                vErrors.push(err111);
              }
              errors++;
            }
            if (Number(data13) <= 0) {
              const err112 = { instancePath: instancePath + "/dnp/hatch_line_width_mm", schemaPath: "#/$defs/DnpOptions/properties/hatch_line_width_mm/x-acr-input", keyword: "x-acr-input", params: {}, message: 'must pass "x-acr-input" keyword validation' };
              if (vErrors === null) {
                vErrors = [err112];
              } else {
                vErrors.push(err112);
              }
              errors++;
            }
          }
        }
        for (const key2 in data8) {
          if (key2 !== "color" && key2 !== "hatch" && key2 !== "hatch_spacing_mm" && key2 !== "hatch_angle_deg" && key2 !== "hatch_line_width_mm") {
            const err113 = { instancePath: instancePath + "/dnp/" + key2.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/DnpOptions/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err113];
            } else {
              vErrors.push(err113);
            }
            errors++;
          }
        }
      } else {
        const err114 = { instancePath: instancePath + "/dnp", schemaPath: "#/$defs/DnpOptions/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err114];
        } else {
          vErrors.push(err114);
        }
        errors++;
      }
      var _valid9 = _errs109 === errors;
      valid15 = valid15 || _valid9;
      const _errs161 = errors;
      if (data8 !== null) {
        const err115 = { instancePath: instancePath + "/dnp", schemaPath: "#/properties/dnp/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err115];
        } else {
          vErrors.push(err115);
        }
        errors++;
      }
      var _valid9 = _errs161 === errors;
      valid15 = valid15 || _valid9;
      if (!valid15) {
        const err116 = { instancePath: instancePath + "/dnp", schemaPath: "#/properties/dnp/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err116];
        } else {
          vErrors.push(err116);
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
    if (data.diodes !== void 0) {
      let data15 = data.diodes;
      const _errs164 = errors;
      let valid24 = false;
      const _errs165 = errors;
      if (data15 && typeof data15 == "object" && !Array.isArray(data15)) {
        if (data15.enabled !== void 0) {
          let data16 = data15.enabled;
          const _errs169 = errors;
          let valid27 = false;
          const _errs170 = errors;
          if (typeof data16 !== "boolean") {
            const err117 = { instancePath: instancePath + "/diodes/enabled", schemaPath: "#/$defs/DiodeOptions/properties/enabled/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err117];
            } else {
              vErrors.push(err117);
            }
            errors++;
          }
          var _valid16 = _errs170 === errors;
          valid27 = valid27 || _valid16;
          const _errs172 = errors;
          if (data16 !== null) {
            const err118 = { instancePath: instancePath + "/diodes/enabled", schemaPath: "#/$defs/DiodeOptions/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err118];
            } else {
              vErrors.push(err118);
            }
            errors++;
          }
          var _valid16 = _errs172 === errors;
          valid27 = valid27 || _valid16;
          const _errs174 = errors;
          if (!(typeof data16 == "number")) {
            const err119 = { instancePath: instancePath + "/diodes/enabled", schemaPath: "#/$defs/DiodeOptions/properties/enabled/anyOf/2/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err119];
            } else {
              vErrors.push(err119);
            }
            errors++;
          }
          var _valid16 = _errs174 === errors;
          valid27 = valid27 || _valid16;
          const _errs176 = errors;
          if (typeof data16 === "string") {
            if (!pattern6.test(data16)) {
              const err120 = { instancePath: instancePath + "/diodes/enabled", schemaPath: "#/$defs/DiodeOptions/properties/enabled/anyOf/3/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
              if (vErrors === null) {
                vErrors = [err120];
              } else {
                vErrors.push(err120);
              }
              errors++;
            }
          } else {
            const err121 = { instancePath: instancePath + "/diodes/enabled", schemaPath: "#/$defs/DiodeOptions/properties/enabled/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err121];
            } else {
              vErrors.push(err121);
            }
            errors++;
          }
          var _valid16 = _errs176 === errors;
          valid27 = valid27 || _valid16;
          if (!valid27) {
            const err122 = { instancePath: instancePath + "/diodes/enabled", schemaPath: "#/$defs/DiodeOptions/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err122];
            } else {
              vErrors.push(err122);
            }
            errors++;
          } else {
            errors = _errs169;
            if (vErrors !== null) {
              if (_errs169) {
                vErrors.length = _errs169;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data15.line_art !== void 0) {
          let data17 = data15.line_art;
          const _errs179 = errors;
          let valid28 = false;
          const _errs180 = errors;
          if (typeof data17 !== "boolean") {
            const err123 = { instancePath: instancePath + "/diodes/line_art", schemaPath: "#/$defs/DiodeOptions/properties/line_art/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err123];
            } else {
              vErrors.push(err123);
            }
            errors++;
          }
          var _valid17 = _errs180 === errors;
          valid28 = valid28 || _valid17;
          const _errs182 = errors;
          if (data17 !== null) {
            const err124 = { instancePath: instancePath + "/diodes/line_art", schemaPath: "#/$defs/DiodeOptions/properties/line_art/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err124];
            } else {
              vErrors.push(err124);
            }
            errors++;
          }
          var _valid17 = _errs182 === errors;
          valid28 = valid28 || _valid17;
          const _errs184 = errors;
          if (!(typeof data17 == "number")) {
            const err125 = { instancePath: instancePath + "/diodes/line_art", schemaPath: "#/$defs/DiodeOptions/properties/line_art/anyOf/2/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err125];
            } else {
              vErrors.push(err125);
            }
            errors++;
          }
          var _valid17 = _errs184 === errors;
          valid28 = valid28 || _valid17;
          const _errs186 = errors;
          if (typeof data17 === "string") {
            if (!pattern6.test(data17)) {
              const err126 = { instancePath: instancePath + "/diodes/line_art", schemaPath: "#/$defs/DiodeOptions/properties/line_art/anyOf/3/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$" }, message: 'must match pattern "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"' };
              if (vErrors === null) {
                vErrors = [err126];
              } else {
                vErrors.push(err126);
              }
              errors++;
            }
          } else {
            const err127 = { instancePath: instancePath + "/diodes/line_art", schemaPath: "#/$defs/DiodeOptions/properties/line_art/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err127];
            } else {
              vErrors.push(err127);
            }
            errors++;
          }
          var _valid17 = _errs186 === errors;
          valid28 = valid28 || _valid17;
          if (!valid28) {
            const err128 = { instancePath: instancePath + "/diodes/line_art", schemaPath: "#/$defs/DiodeOptions/properties/line_art/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err128];
            } else {
              vErrors.push(err128);
            }
            errors++;
          } else {
            errors = _errs179;
            if (vErrors !== null) {
              if (_errs179) {
                vErrors.length = _errs179;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data15.marker_color !== void 0) {
          let data18 = data15.marker_color;
          const _errs189 = errors;
          let valid29 = false;
          const _errs190 = errors;
          if (typeof data18 !== "string") {
            const err129 = { instancePath: instancePath + "/diodes/marker_color", schemaPath: "#/$defs/DiodeOptions/properties/marker_color/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err129];
            } else {
              vErrors.push(err129);
            }
            errors++;
          }
          var _valid18 = _errs190 === errors;
          valid29 = valid29 || _valid18;
          const _errs192 = errors;
          if (data18 !== null) {
            const err130 = { instancePath: instancePath + "/diodes/marker_color", schemaPath: "#/$defs/DiodeOptions/properties/marker_color/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err130];
            } else {
              vErrors.push(err130);
            }
            errors++;
          }
          var _valid18 = _errs192 === errors;
          valid29 = valid29 || _valid18;
          if (!valid29) {
            const err131 = { instancePath: instancePath + "/diodes/marker_color", schemaPath: "#/$defs/DiodeOptions/properties/marker_color/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err131];
            } else {
              vErrors.push(err131);
            }
            errors++;
          } else {
            errors = _errs189;
            if (vErrors !== null) {
              if (_errs189) {
                vErrors.length = _errs189;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data15.numeric_cathode_pad !== void 0) {
          let data19 = data15.numeric_cathode_pad;
          const _errs195 = errors;
          let valid30 = false;
          const _errs196 = errors;
          if (typeof data19 !== "string") {
            const err132 = { instancePath: instancePath + "/diodes/numeric_cathode_pad", schemaPath: "#/$defs/DiodeOptions/properties/numeric_cathode_pad/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err132];
            } else {
              vErrors.push(err132);
            }
            errors++;
          }
          var _valid19 = _errs196 === errors;
          valid30 = valid30 || _valid19;
          const _errs198 = errors;
          if (data19 !== null) {
            const err133 = { instancePath: instancePath + "/diodes/numeric_cathode_pad", schemaPath: "#/$defs/DiodeOptions/properties/numeric_cathode_pad/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err133];
            } else {
              vErrors.push(err133);
            }
            errors++;
          }
          var _valid19 = _errs198 === errors;
          valid30 = valid30 || _valid19;
          if (!valid30) {
            const err134 = { instancePath: instancePath + "/diodes/numeric_cathode_pad", schemaPath: "#/$defs/DiodeOptions/properties/numeric_cathode_pad/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err134];
            } else {
              vErrors.push(err134);
            }
            errors++;
          } else {
            errors = _errs195;
            if (vErrors !== null) {
              if (_errs195) {
                vErrors.length = _errs195;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data15.cathode_pad_names !== void 0) {
          let data20 = data15.cathode_pad_names;
          const _errs201 = errors;
          let valid31 = false;
          const _errs202 = errors;
          if (Array.isArray(data20)) {
            const len0 = data20.length;
            for (let i0 = 0; i0 < len0; i0++) {
              if (typeof data20[i0] !== "string") {
                const err135 = { instancePath: instancePath + "/diodes/cathode_pad_names/" + i0, schemaPath: "#/$defs/DiodeOptions/properties/cathode_pad_names/anyOf/0/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err135];
                } else {
                  vErrors.push(err135);
                }
                errors++;
              }
            }
          } else {
            const err136 = { instancePath: instancePath + "/diodes/cathode_pad_names", schemaPath: "#/$defs/DiodeOptions/properties/cathode_pad_names/anyOf/0/type", keyword: "type", params: { type: "array" }, message: "must be array" };
            if (vErrors === null) {
              vErrors = [err136];
            } else {
              vErrors.push(err136);
            }
            errors++;
          }
          var _valid20 = _errs202 === errors;
          valid31 = valid31 || _valid20;
          const _errs206 = errors;
          if (data20 !== null) {
            const err137 = { instancePath: instancePath + "/diodes/cathode_pad_names", schemaPath: "#/$defs/DiodeOptions/properties/cathode_pad_names/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err137];
            } else {
              vErrors.push(err137);
            }
            errors++;
          }
          var _valid20 = _errs206 === errors;
          valid31 = valid31 || _valid20;
          if (!valid31) {
            const err138 = { instancePath: instancePath + "/diodes/cathode_pad_names", schemaPath: "#/$defs/DiodeOptions/properties/cathode_pad_names/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err138];
            } else {
              vErrors.push(err138);
            }
            errors++;
          } else {
            errors = _errs201;
            if (vErrors !== null) {
              if (_errs201) {
                vErrors.length = _errs201;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data15.designator_prefixes !== void 0) {
          let data22 = data15.designator_prefixes;
          const _errs209 = errors;
          let valid34 = false;
          const _errs210 = errors;
          if (Array.isArray(data22)) {
            const len1 = data22.length;
            for (let i1 = 0; i1 < len1; i1++) {
              if (typeof data22[i1] !== "string") {
                const err139 = { instancePath: instancePath + "/diodes/designator_prefixes/" + i1, schemaPath: "#/$defs/DiodeOptions/properties/designator_prefixes/anyOf/0/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err139];
                } else {
                  vErrors.push(err139);
                }
                errors++;
              }
            }
          } else {
            const err140 = { instancePath: instancePath + "/diodes/designator_prefixes", schemaPath: "#/$defs/DiodeOptions/properties/designator_prefixes/anyOf/0/type", keyword: "type", params: { type: "array" }, message: "must be array" };
            if (vErrors === null) {
              vErrors = [err140];
            } else {
              vErrors.push(err140);
            }
            errors++;
          }
          var _valid21 = _errs210 === errors;
          valid34 = valid34 || _valid21;
          const _errs214 = errors;
          if (data22 !== null) {
            const err141 = { instancePath: instancePath + "/diodes/designator_prefixes", schemaPath: "#/$defs/DiodeOptions/properties/designator_prefixes/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err141];
            } else {
              vErrors.push(err141);
            }
            errors++;
          }
          var _valid21 = _errs214 === errors;
          valid34 = valid34 || _valid21;
          if (!valid34) {
            const err142 = { instancePath: instancePath + "/diodes/designator_prefixes", schemaPath: "#/$defs/DiodeOptions/properties/designator_prefixes/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err142];
            } else {
              vErrors.push(err142);
            }
            errors++;
          } else {
            errors = _errs209;
            if (vErrors !== null) {
              if (_errs209) {
                vErrors.length = _errs209;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data15.parameter_terms !== void 0) {
          let data24 = data15.parameter_terms;
          const _errs217 = errors;
          let valid37 = false;
          const _errs218 = errors;
          if (Array.isArray(data24)) {
            const len2 = data24.length;
            for (let i2 = 0; i2 < len2; i2++) {
              if (typeof data24[i2] !== "string") {
                const err143 = { instancePath: instancePath + "/diodes/parameter_terms/" + i2, schemaPath: "#/$defs/DiodeOptions/properties/parameter_terms/anyOf/0/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err143];
                } else {
                  vErrors.push(err143);
                }
                errors++;
              }
            }
          } else {
            const err144 = { instancePath: instancePath + "/diodes/parameter_terms", schemaPath: "#/$defs/DiodeOptions/properties/parameter_terms/anyOf/0/type", keyword: "type", params: { type: "array" }, message: "must be array" };
            if (vErrors === null) {
              vErrors = [err144];
            } else {
              vErrors.push(err144);
            }
            errors++;
          }
          var _valid22 = _errs218 === errors;
          valid37 = valid37 || _valid22;
          const _errs222 = errors;
          if (data24 !== null) {
            const err145 = { instancePath: instancePath + "/diodes/parameter_terms", schemaPath: "#/$defs/DiodeOptions/properties/parameter_terms/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err145];
            } else {
              vErrors.push(err145);
            }
            errors++;
          }
          var _valid22 = _errs222 === errors;
          valid37 = valid37 || _valid22;
          if (!valid37) {
            const err146 = { instancePath: instancePath + "/diodes/parameter_terms", schemaPath: "#/$defs/DiodeOptions/properties/parameter_terms/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err146];
            } else {
              vErrors.push(err146);
            }
            errors++;
          } else {
            errors = _errs217;
            if (vErrors !== null) {
              if (_errs217) {
                vErrors.length = _errs217;
              } else {
                vErrors = null;
              }
            }
          }
        }
        for (const key3 in data15) {
          if (key3 !== "enabled" && key3 !== "line_art" && key3 !== "marker_color" && key3 !== "numeric_cathode_pad" && key3 !== "cathode_pad_names" && key3 !== "designator_prefixes" && key3 !== "parameter_terms") {
            const err147 = { instancePath: instancePath + "/diodes/" + key3.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/DiodeOptions/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err147];
            } else {
              vErrors.push(err147);
            }
            errors++;
          }
        }
      } else {
        const err148 = { instancePath: instancePath + "/diodes", schemaPath: "#/$defs/DiodeOptions/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err148];
        } else {
          vErrors.push(err148);
        }
        errors++;
      }
      var _valid15 = _errs165 === errors;
      valid24 = valid24 || _valid15;
      const _errs227 = errors;
      if (data15 !== null) {
        const err149 = { instancePath: instancePath + "/diodes", schemaPath: "#/properties/diodes/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err149];
        } else {
          vErrors.push(err149);
        }
        errors++;
      }
      var _valid15 = _errs227 === errors;
      valid24 = valid24 || _valid15;
      if (!valid24) {
        const err150 = { instancePath: instancePath + "/diodes", schemaPath: "#/properties/diodes/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err150];
        } else {
          vErrors.push(err150);
        }
        errors++;
      } else {
        errors = _errs164;
        if (vErrors !== null) {
          if (_errs164) {
            vErrors.length = _errs164;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.pin1 !== void 0) {
      let data27 = data.pin1;
      const _errs230 = errors;
      let valid41 = false;
      const _errs231 = errors;
      if (data27 && typeof data27 == "object" && !Array.isArray(data27)) {
        if (data27.exclude_designator_prefixes !== void 0) {
          let data28 = data27.exclude_designator_prefixes;
          const _errs235 = errors;
          let valid44 = false;
          const _errs236 = errors;
          if (Array.isArray(data28)) {
            const len3 = data28.length;
            for (let i3 = 0; i3 < len3; i3++) {
              if (typeof data28[i3] !== "string") {
                const err151 = { instancePath: instancePath + "/pin1/exclude_designator_prefixes/" + i3, schemaPath: "#/$defs/Pin1Options/properties/exclude_designator_prefixes/anyOf/0/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err151];
                } else {
                  vErrors.push(err151);
                }
                errors++;
              }
            }
          } else {
            const err152 = { instancePath: instancePath + "/pin1/exclude_designator_prefixes", schemaPath: "#/$defs/Pin1Options/properties/exclude_designator_prefixes/anyOf/0/type", keyword: "type", params: { type: "array" }, message: "must be array" };
            if (vErrors === null) {
              vErrors = [err152];
            } else {
              vErrors.push(err152);
            }
            errors++;
          }
          var _valid24 = _errs236 === errors;
          valid44 = valid44 || _valid24;
          const _errs240 = errors;
          if (data28 !== null) {
            const err153 = { instancePath: instancePath + "/pin1/exclude_designator_prefixes", schemaPath: "#/$defs/Pin1Options/properties/exclude_designator_prefixes/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err153];
            } else {
              vErrors.push(err153);
            }
            errors++;
          }
          var _valid24 = _errs240 === errors;
          valid44 = valid44 || _valid24;
          if (!valid44) {
            const err154 = { instancePath: instancePath + "/pin1/exclude_designator_prefixes", schemaPath: "#/$defs/Pin1Options/properties/exclude_designator_prefixes/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err154];
            } else {
              vErrors.push(err154);
            }
            errors++;
          } else {
            errors = _errs235;
            if (vErrors !== null) {
              if (_errs235) {
                vErrors.length = _errs235;
              } else {
                vErrors = null;
              }
            }
          }
        }
        for (const key4 in data27) {
          if (key4 !== "exclude_designator_prefixes") {
            const err155 = { instancePath: instancePath + "/pin1/" + key4.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/Pin1Options/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err155];
            } else {
              vErrors.push(err155);
            }
            errors++;
          }
        }
      } else {
        const err156 = { instancePath: instancePath + "/pin1", schemaPath: "#/$defs/Pin1Options/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err156];
        } else {
          vErrors.push(err156);
        }
        errors++;
      }
      var _valid23 = _errs231 === errors;
      valid41 = valid41 || _valid23;
      const _errs245 = errors;
      if (data27 !== null) {
        const err157 = { instancePath: instancePath + "/pin1", schemaPath: "#/properties/pin1/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err157];
        } else {
          vErrors.push(err157);
        }
        errors++;
      }
      var _valid23 = _errs245 === errors;
      valid41 = valid41 || _valid23;
      if (!valid41) {
        const err158 = { instancePath: instancePath + "/pin1", schemaPath: "#/properties/pin1/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err158];
        } else {
          vErrors.push(err158);
        }
        errors++;
      } else {
        errors = _errs230;
        if (vErrors !== null) {
          if (_errs230) {
            vErrors.length = _errs230;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.components !== void 0) {
      let data31 = data.components;
      const _errs248 = errors;
      let valid48 = false;
      const _errs249 = errors;
      if (!validate66(data31, { instancePath: instancePath + "/components", parentData: data, parentDataProperty: "components", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate66.errors : vErrors.concat(validate66.errors);
        errors = vErrors.length;
      }
      var _valid25 = _errs249 === errors;
      valid48 = valid48 || _valid25;
      const _errs250 = errors;
      if (data31 !== null) {
        const err159 = { instancePath: instancePath + "/components", schemaPath: "#/properties/components/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err159];
        } else {
          vErrors.push(err159);
        }
        errors++;
      }
      var _valid25 = _errs250 === errors;
      valid48 = valid48 || _valid25;
      if (!valid48) {
        const err160 = { instancePath: instancePath + "/components", schemaPath: "#/properties/components/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err160];
        } else {
          vErrors.push(err160);
        }
        errors++;
      } else {
        errors = _errs248;
        if (vErrors !== null) {
          if (_errs248) {
            vErrors.length = _errs248;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.layer_outputs !== void 0) {
      let data32 = data.layer_outputs;
      const _errs253 = errors;
      let valid49 = false;
      const _errs254 = errors;
      if (!validate71(data32, { instancePath: instancePath + "/layer_outputs", parentData: data, parentDataProperty: "layer_outputs", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate71.errors : vErrors.concat(validate71.errors);
        errors = vErrors.length;
      }
      var _valid26 = _errs254 === errors;
      valid49 = valid49 || _valid26;
      const _errs255 = errors;
      if (data32 !== null) {
        const err161 = { instancePath: instancePath + "/layer_outputs", schemaPath: "#/properties/layer_outputs/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err161];
        } else {
          vErrors.push(err161);
        }
        errors++;
      }
      var _valid26 = _errs255 === errors;
      valid49 = valid49 || _valid26;
      if (!valid49) {
        const err162 = { instancePath: instancePath + "/layer_outputs", schemaPath: "#/properties/layer_outputs/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err162];
        } else {
          vErrors.push(err162);
        }
        errors++;
      } else {
        errors = _errs253;
        if (vErrors !== null) {
          if (_errs253) {
            vErrors.length = _errs253;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.views !== void 0) {
      let data33 = data.views;
      const _errs258 = errors;
      let valid50 = false;
      const _errs259 = errors;
      if (Array.isArray(data33)) {
        const len4 = data33.length;
        for (let i4 = 0; i4 < len4; i4++) {
          if (!validate73(data33[i4], { instancePath: instancePath + "/views/" + i4, parentData: data33, parentDataProperty: i4, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate73.errors : vErrors.concat(validate73.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err163 = { instancePath: instancePath + "/views", schemaPath: "#/properties/views/anyOf/0/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err163];
        } else {
          vErrors.push(err163);
        }
        errors++;
      }
      var _valid27 = _errs259 === errors;
      valid50 = valid50 || _valid27;
      const _errs262 = errors;
      if (data33 !== null) {
        const err164 = { instancePath: instancePath + "/views", schemaPath: "#/properties/views/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err164];
        } else {
          vErrors.push(err164);
        }
        errors++;
      }
      var _valid27 = _errs262 === errors;
      valid50 = valid50 || _valid27;
      if (!valid50) {
        const err165 = { instancePath: instancePath + "/views", schemaPath: "#/properties/views/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err165];
        } else {
          vErrors.push(err165);
        }
        errors++;
      } else {
        errors = _errs258;
        if (vErrors !== null) {
          if (_errs258) {
            vErrors.length = _errs258;
          } else {
            vErrors = null;
          }
        }
      }
    }
  } else {
    const err166 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err166];
    } else {
      vErrors.push(err166);
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
