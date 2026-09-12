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
    if (data.left === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "left" }, message: "must have required property 'left'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.bottom === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "bottom" }, message: "must have required property 'bottom'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.right === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "right" }, message: "must have required property 'right'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.top === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "top" }, message: "must have required property 'top'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.left !== void 0) {
      let data0 = data.left;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (!(typeof data0 == "number")) {
        const err5 = { instancePath: instancePath + "/left", schemaPath: "#/properties/left/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid3 = valid3 || _valid0;
      const _errs9 = errors;
      if (typeof data0 !== "boolean") {
        const err6 = { instancePath: instancePath + "/left", schemaPath: "#/properties/left/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err7 = { instancePath: instancePath + "/left", schemaPath: "#/properties/left/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.bottom !== void 0) {
      let data1 = data.bottom;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (!(typeof data1 == "number")) {
        const err8 = { instancePath: instancePath + "/bottom", schemaPath: "#/properties/bottom/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid1 = _errs13 === errors;
      valid4 = valid4 || _valid1;
      const _errs15 = errors;
      if (typeof data1 !== "boolean") {
        const err9 = { instancePath: instancePath + "/bottom", schemaPath: "#/properties/bottom/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err10 = { instancePath: instancePath + "/bottom", schemaPath: "#/properties/bottom/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
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
    if (data.right !== void 0) {
      let data2 = data.right;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (!(typeof data2 == "number")) {
        const err11 = { instancePath: instancePath + "/right", schemaPath: "#/properties/right/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (typeof data2 !== "boolean") {
        const err12 = { instancePath: instancePath + "/right", schemaPath: "#/properties/right/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err13 = { instancePath: instancePath + "/right", schemaPath: "#/properties/right/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.top !== void 0) {
      let data3 = data.top;
      const _errs24 = errors;
      let valid6 = false;
      const _errs25 = errors;
      if (!(typeof data3 == "number")) {
        const err14 = { instancePath: instancePath + "/top", schemaPath: "#/properties/top/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid3 = _errs25 === errors;
      valid6 = valid6 || _valid3;
      const _errs27 = errors;
      if (typeof data3 !== "boolean") {
        const err15 = { instancePath: instancePath + "/top", schemaPath: "#/properties/top/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid3 = _errs27 === errors;
      valid6 = valid6 || _valid3;
      if (!valid6) {
        const err16 = { instancePath: instancePath + "/top", schemaPath: "#/properties/top/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
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
    const err17 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err17];
    } else {
      vErrors.push(err17);
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
    if (data.name === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.name !== void 0) {
      let data0 = data.name;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err2 = { instancePath: instancePath + "/name", schemaPath: "#/$defs/NonemptyString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err2];
          } else {
            vErrors.push(err2);
          }
          errors++;
        }
      } else {
        const err3 = { instancePath: instancePath + "/name", schemaPath: "#/$defs/NonemptyString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.copper_thickness_mils !== void 0) {
      let data1 = data.copper_thickness_mils;
      const _errs9 = errors;
      let valid4 = false;
      const _errs10 = errors;
      if (!(typeof data1 == "number")) {
        const err4 = { instancePath: instancePath + "/copper_thickness_mils", schemaPath: "#/properties/copper_thickness_mils/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
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
      if (data1 !== null) {
        const err5 = { instancePath: instancePath + "/copper_thickness_mils", schemaPath: "#/properties/copper_thickness_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid0 = _errs12 === errors;
      valid4 = valid4 || _valid0;
      if (!valid4) {
        const err6 = { instancePath: instancePath + "/copper_thickness_mils", schemaPath: "#/properties/copper_thickness_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
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
    if (data.component_placement !== void 0) {
      let data2 = data.component_placement;
      const _errs15 = errors;
      let valid5 = false;
      const _errs16 = errors;
      if (!(typeof data2 == "number" && (!(data2 % 1) && !isNaN(data2)))) {
        const err7 = { instancePath: instancePath + "/component_placement", schemaPath: "#/properties/component_placement/anyOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid1 = _errs16 === errors;
      valid5 = valid5 || _valid1;
      const _errs18 = errors;
      if (data2 !== null) {
        const err8 = { instancePath: instancePath + "/component_placement", schemaPath: "#/properties/component_placement/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid1 = _errs18 === errors;
      valid5 = valid5 || _valid1;
      if (!valid5) {
        const err9 = { instancePath: instancePath + "/component_placement", schemaPath: "#/properties/component_placement/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
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
    if (data.copper_orientation !== void 0) {
      let data3 = data.copper_orientation;
      const _errs21 = errors;
      let valid6 = false;
      const _errs22 = errors;
      if (!(typeof data3 == "number" && (!(data3 % 1) && !isNaN(data3)))) {
        const err10 = { instancePath: instancePath + "/copper_orientation", schemaPath: "#/properties/copper_orientation/anyOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs22 === errors;
      valid6 = valid6 || _valid2;
      const _errs24 = errors;
      if (data3 !== null) {
        const err11 = { instancePath: instancePath + "/copper_orientation", schemaPath: "#/properties/copper_orientation/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid2 = _errs24 === errors;
      valid6 = valid6 || _valid2;
      if (!valid6) {
        const err12 = { instancePath: instancePath + "/copper_orientation", schemaPath: "#/properties/copper_orientation/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
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
  validate24.errors = vErrors;
  return errors === 0;
}
validate24.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    const err0 = { instancePath, schemaPath: "#/$defs/RecordUnknown/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err0];
    } else {
      vErrors.push(err0);
    }
    errors++;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.name === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.material === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "material" }, message: "must have required property 'material'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.thickness_mils === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "thickness_mils" }, message: "must have required property 'thickness_mils'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.dielectric_constant === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "dielectric_constant" }, message: "must have required property 'dielectric_constant'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.name !== void 0) {
      let data0 = data.name;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err5 = { instancePath: instancePath + "/name", schemaPath: "#/$defs/NonemptyString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err5];
          } else {
            vErrors.push(err5);
          }
          errors++;
        }
      } else {
        const err6 = { instancePath: instancePath + "/name", schemaPath: "#/$defs/NonemptyString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.material !== void 0) {
      let data1 = data.material;
      if (typeof data1 === "string") {
        if (func1(data1) < 1) {
          const err7 = { instancePath: instancePath + "/material", schemaPath: "#/$defs/NonemptyString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err7];
          } else {
            vErrors.push(err7);
          }
          errors++;
        }
      } else {
        const err8 = { instancePath: instancePath + "/material", schemaPath: "#/$defs/NonemptyString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
    if (data.thickness_mils !== void 0) {
      if (!(typeof data.thickness_mils == "number")) {
        const err9 = { instancePath: instancePath + "/thickness_mils", schemaPath: "#/properties/thickness_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    if (data.dielectric_constant !== void 0) {
      if (!(typeof data.dielectric_constant == "number")) {
        const err10 = { instancePath: instancePath + "/dielectric_constant", schemaPath: "#/properties/dielectric_constant/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
    }
    if (data.dielectric_type !== void 0) {
      let data4 = data.dielectric_type;
      const _errs16 = errors;
      let valid5 = false;
      const _errs17 = errors;
      if (!(typeof data4 == "number" && (!(data4 % 1) && !isNaN(data4)))) {
        const err11 = { instancePath: instancePath + "/dielectric_type", schemaPath: "#/properties/dielectric_type/anyOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid0 = _errs17 === errors;
      valid5 = valid5 || _valid0;
      const _errs19 = errors;
      if (data4 !== null) {
        const err12 = { instancePath: instancePath + "/dielectric_type", schemaPath: "#/properties/dielectric_type/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid0 = _errs19 === errors;
      valid5 = valid5 || _valid0;
      if (!valid5) {
        const err13 = { instancePath: instancePath + "/dielectric_type", schemaPath: "#/properties/dielectric_type/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.loss_tangent !== void 0) {
      let data5 = data.loss_tangent;
      const _errs22 = errors;
      let valid6 = false;
      const _errs23 = errors;
      if (!(typeof data5 == "number")) {
        const err14 = { instancePath: instancePath + "/loss_tangent", schemaPath: "#/properties/loss_tangent/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid1 = _errs23 === errors;
      valid6 = valid6 || _valid1;
      const _errs25 = errors;
      if (data5 !== null) {
        const err15 = { instancePath: instancePath + "/loss_tangent", schemaPath: "#/properties/loss_tangent/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid1 = _errs25 === errors;
      valid6 = valid6 || _valid1;
      if (!valid6) {
        const err16 = { instancePath: instancePath + "/loss_tangent", schemaPath: "#/properties/loss_tangent/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
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
  } else {
    const err17 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err17];
    } else {
      vErrors.push(err17);
    }
    errors++;
  }
  validate26.errors = vErrors;
  return errors === 0;
}
validate26.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.copper_layers === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "copper_layers" }, message: "must have required property 'copper_layers'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.dielectrics_between === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "dielectrics_between" }, message: "must have required property 'dielectrics_between'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.mode !== void 0) {
      let data0 = data.mode;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      if ("generated_rigid" !== data0) {
        const err4 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf/0/const", keyword: "const", params: { allowedValue: "generated_rigid" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid3 = valid3 || _valid0;
      const _errs9 = errors;
      if (data0 !== null) {
        const err5 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err6 = { instancePath: instancePath + "/mode", schemaPath: "#/properties/mode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.name !== void 0) {
      let data1 = data.name;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err7 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid1 = _errs13 === errors;
      valid4 = valid4 || _valid1;
      const _errs15 = errors;
      if (data1 !== null) {
        const err8 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid1 = _errs15 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err9 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
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
    if (data.copper_layers !== void 0) {
      let data2 = data.copper_layers;
      if (Array.isArray(data2)) {
        if (data2.length < 2) {
          const err10 = { instancePath: instancePath + "/copper_layers", schemaPath: "#/properties/copper_layers/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err10];
          } else {
            vErrors.push(err10);
          }
          errors++;
        }
        const len0 = data2.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!validate24(data2[i0], { instancePath: instancePath + "/copper_layers/" + i0, parentData: data2, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate24.errors : vErrors.concat(validate24.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err11 = { instancePath: instancePath + "/copper_layers", schemaPath: "#/properties/copper_layers/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
    }
    if (data.dielectrics_between !== void 0) {
      let data4 = data.dielectrics_between;
      if (Array.isArray(data4)) {
        const len1 = data4.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (!validate26(data4[i1], { instancePath: instancePath + "/dielectrics_between/" + i1, parentData: data4, parentDataProperty: i1, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate26.errors : vErrors.concat(validate26.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err12 = { instancePath: instancePath + "/dielectrics_between", schemaPath: "#/properties/dielectrics_between/type", keyword: "type", params: { type: "array" }, message: "must be array" };
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
  validate23.errors = vErrors;
  return errors === 0;
}
validate23.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.layer === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "layer" }, message: "must have required property 'layer'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.layer !== void 0) {
      let data0 = data.layer;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err2 = { instancePath: instancePath + "/layer", schemaPath: "#/$defs/NonemptyString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err2];
          } else {
            vErrors.push(err2);
          }
          errors++;
        }
      } else {
        const err3 = { instancePath: instancePath + "/layer", schemaPath: "#/$defs/NonemptyString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.name !== void 0) {
      let data1 = data.name;
      const _errs9 = errors;
      let valid4 = false;
      const _errs10 = errors;
      if (typeof data1 === "string") {
        if (func1(data1) < 1) {
          const err4 = { instancePath: instancePath + "/name", schemaPath: "#/$defs/NonemptyString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err4];
          } else {
            vErrors.push(err4);
          }
          errors++;
        }
      } else {
        const err5 = { instancePath: instancePath + "/name", schemaPath: "#/$defs/NonemptyString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      valid4 = valid4 || _valid0;
      const _errs13 = errors;
      if (data1 !== null) {
        const err6 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs13 === errors;
      valid4 = valid4 || _valid0;
      if (!valid4) {
        const err7 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.enabled !== void 0) {
      let data2 = data.enabled;
      const _errs16 = errors;
      let valid6 = false;
      const _errs17 = errors;
      if (typeof data2 !== "boolean") {
        const err8 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid1 = _errs17 === errors;
      valid6 = valid6 || _valid1;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid1 = _errs19 === errors;
      valid6 = valid6 || _valid1;
      const _errs21 = errors;
      if (!(typeof data2 == "number")) {
        const err10 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid1 = _errs21 === errors;
      valid6 = valid6 || _valid1;
      const _errs23 = errors;
      if (data2 !== null) {
        const err11 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/3/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid1 = _errs23 === errors;
      valid6 = valid6 || _valid1;
      const _errs25 = errors;
      if (!Array.isArray(data2)) {
        const err12 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/4/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid1 = _errs25 === errors;
      valid6 = valid6 || _valid1;
      const _errs27 = errors;
      if (data2 && typeof data2 == "object" && !Array.isArray(data2)) {
      } else {
        const err13 = { instancePath: instancePath + "/enabled", schemaPath: "#/$defs/RecordUnknown/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid1 = _errs27 === errors;
      valid6 = valid6 || _valid1;
      if (!valid6) {
        const err14 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
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
    if (data.kind !== void 0) {
      let data3 = data.kind;
      const _errs32 = errors;
      let valid8 = false;
      const _errs33 = errors;
      if (typeof data3 === "string") {
        if (func1(data3) < 1) {
          const err15 = { instancePath: instancePath + "/kind", schemaPath: "#/$defs/NonemptyString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err15];
          } else {
            vErrors.push(err15);
          }
          errors++;
        }
      } else {
        const err16 = { instancePath: instancePath + "/kind", schemaPath: "#/$defs/NonemptyString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid2 = _errs33 === errors;
      valid8 = valid8 || _valid2;
      const _errs36 = errors;
      if (data3 !== null) {
        const err17 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      var _valid2 = _errs36 === errors;
      valid8 = valid8 || _valid2;
      if (!valid8) {
        const err18 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
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
  } else {
    const err19 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err19];
    } else {
      vErrors.push(err19);
    }
    errors++;
  }
  validate29.errors = vErrors;
  return errors === 0;
}
validate29.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.layer === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "layer" }, message: "must have required property 'layer'" };
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
    if (data.layer !== void 0) {
      let data0 = data.layer;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err3 = { instancePath: instancePath + "/layer", schemaPath: "#/$defs/NonemptyString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/layer", schemaPath: "#/$defs/NonemptyString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.name !== void 0) {
      let data1 = data.name;
      const _errs9 = errors;
      let valid4 = false;
      const _errs10 = errors;
      if (typeof data1 === "string") {
        if (func1(data1) < 1) {
          const err5 = { instancePath: instancePath + "/name", schemaPath: "#/$defs/NonemptyString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err5];
          } else {
            vErrors.push(err5);
          }
          errors++;
        }
      } else {
        const err6 = { instancePath: instancePath + "/name", schemaPath: "#/$defs/NonemptyString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      valid4 = valid4 || _valid0;
      const _errs13 = errors;
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid0 = _errs13 === errors;
      valid4 = valid4 || _valid0;
      if (!valid4) {
        const err8 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
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
    if (data.enabled !== void 0) {
      let data2 = data.enabled;
      const _errs16 = errors;
      let valid6 = false;
      const _errs17 = errors;
      if (typeof data2 !== "boolean") {
        const err9 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid1 = _errs17 === errors;
      valid6 = valid6 || _valid1;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err10 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid1 = _errs19 === errors;
      valid6 = valid6 || _valid1;
      const _errs21 = errors;
      if (!(typeof data2 == "number")) {
        const err11 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/2/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid1 = _errs21 === errors;
      valid6 = valid6 || _valid1;
      const _errs23 = errors;
      if (data2 !== null) {
        const err12 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/3/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid1 = _errs23 === errors;
      valid6 = valid6 || _valid1;
      const _errs25 = errors;
      if (!Array.isArray(data2)) {
        const err13 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/4/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid1 = _errs25 === errors;
      valid6 = valid6 || _valid1;
      const _errs27 = errors;
      if (data2 && typeof data2 == "object" && !Array.isArray(data2)) {
      } else {
        const err14 = { instancePath: instancePath + "/enabled", schemaPath: "#/$defs/RecordUnknown/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid1 = _errs27 === errors;
      valid6 = valid6 || _valid1;
      if (!valid6) {
        const err15 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.kind !== void 0) {
      let data3 = data.kind;
      if (typeof data3 === "string") {
        if (func1(data3) < 1) {
          const err16 = { instancePath: instancePath + "/kind", schemaPath: "#/$defs/NonemptyString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err16];
          } else {
            vErrors.push(err16);
          }
          errors++;
        }
      } else {
        const err17 = { instancePath: instancePath + "/kind", schemaPath: "#/$defs/NonemptyString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
  validate32.errors = vErrors;
  return errors === 0;
}
validate32.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.top === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "top" }, message: "must have required property 'top'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.bottom === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "bottom" }, message: "must have required property 'bottom'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.top !== void 0) {
      if (!validate32(data.top, { instancePath: instancePath + "/top", parentData: data, parentDataProperty: "top", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate32.errors : vErrors.concat(validate32.errors);
        errors = vErrors.length;
      }
    }
    if (data.bottom !== void 0) {
      if (!validate32(data.bottom, { instancePath: instancePath + "/bottom", parentData: data, parentDataProperty: "bottom", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate32.errors : vErrors.concat(validate32.errors);
        errors = vErrors.length;
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
  validate31.errors = vErrors;
  return errors === 0;
}
validate31.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.layer_1 === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "layer_1" }, message: "must have required property 'layer_1'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.layer_2 === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "layer_2" }, message: "must have required property 'layer_2'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.layer_1 !== void 0) {
      let data0 = data.layer_1;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err3 = { instancePath: instancePath + "/layer_1", schemaPath: "#/$defs/NonemptyString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/layer_1", schemaPath: "#/$defs/NonemptyString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.layer_2 !== void 0) {
      let data1 = data.layer_2;
      if (typeof data1 === "string") {
        if (func1(data1) < 1) {
          const err5 = { instancePath: instancePath + "/layer_2", schemaPath: "#/$defs/NonemptyString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err5];
          } else {
            vErrors.push(err5);
          }
          errors++;
        }
      } else {
        const err6 = { instancePath: instancePath + "/layer_2", schemaPath: "#/$defs/NonemptyString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.pair_index !== void 0) {
      let data2 = data.pair_index;
      const _errs12 = errors;
      let valid5 = false;
      const _errs13 = errors;
      if (!(typeof data2 == "number" && (!(data2 % 1) && !isNaN(data2)))) {
        const err7 = { instancePath: instancePath + "/pair_index", schemaPath: "#/properties/pair_index/anyOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid0 = _errs13 === errors;
      valid5 = valid5 || _valid0;
      const _errs15 = errors;
      if (data2 !== null) {
        const err8 = { instancePath: instancePath + "/pair_index", schemaPath: "#/properties/pair_index/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid0 = _errs15 === errors;
      valid5 = valid5 || _valid0;
      if (!valid5) {
        const err9 = { instancePath: instancePath + "/pair_index", schemaPath: "#/properties/pair_index/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
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
      if (typeof data2 == "number") {
        if (data2 < 0 || isNaN(data2)) {
          const err10 = { instancePath: instancePath + "/pair_index", schemaPath: "#/properties/pair_index/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err10];
          } else {
            vErrors.push(err10);
          }
          errors++;
        }
      }
    }
    if (data.top !== void 0) {
      const err11 = { instancePath: instancePath + "/top", schemaPath: "#/properties/top/not", keyword: "not", params: {}, message: "must NOT be valid" };
      if (vErrors === null) {
        vErrors = [err11];
      } else {
        vErrors.push(err11);
      }
      errors++;
    }
    if (data.bottom !== void 0) {
      const err12 = { instancePath: instancePath + "/bottom", schemaPath: "#/properties/bottom/not", keyword: "not", params: {}, message: "must NOT be valid" };
      if (vErrors === null) {
        vErrors = [err12];
      } else {
        vErrors.push(err12);
      }
      errors++;
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
  validate36.errors = vErrors;
  return errors === 0;
}
validate36.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.layer === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "layer" }, message: "must have required property 'layer'" };
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
    if (data.layer !== void 0) {
      let data0 = data.layer;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err3 = { instancePath: instancePath + "/layer", schemaPath: "#/$defs/NonemptyString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/layer", schemaPath: "#/$defs/NonemptyString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.kind !== void 0) {
      let data1 = data.kind;
      const _errs9 = errors;
      let valid4 = false;
      const _errs10 = errors;
      if (typeof data1 === "string") {
        if (func1(data1) < 1) {
          const err5 = { instancePath: instancePath + "/kind", schemaPath: "#/$defs/NonemptyString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err5];
          } else {
            vErrors.push(err5);
          }
          errors++;
        }
      } else {
        const err6 = { instancePath: instancePath + "/kind", schemaPath: "#/$defs/NonemptyString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      valid4 = valid4 || _valid0;
      const _errs13 = errors;
      if (!(typeof data1 == "number" && (!(data1 % 1) && !isNaN(data1)))) {
        const err7 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid0 = _errs13 === errors;
      valid4 = valid4 || _valid0;
      if (!valid4) {
        const err8 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
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
  } else {
    const err9 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err9];
    } else {
      vErrors.push(err9);
    }
    errors++;
  }
  validate38.errors = vErrors;
  return errors === 0;
}
validate38.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
var pattern4 = new RegExp("^\\s*(?:[nN][oO][nN][eE]||[sS][tT][aA][nN][dD][aA][rR][dD]_[cC][oO][mM][pP][oO][nN][eE][nN][tT]_[pP][aA][iI][rR][sS]|[sS][tT][aA][nN][dD][aA][rR][dD]-[cC][oO][mM][pP][oO][nN][eE][nN][tT]-[pP][aA][iI][rR][sS]|[vV]7_[mM][eE][cC][hH][aA][nN][iI][cC][aA][lL]_53|[vV]7-[mM][eE][cC][hH][aA][nN][iI][cC][aA][lL]-53)\\s*$", "u");
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
      if ("altium_cruncher.pcbdoc.create.config.a0" !== data0) {
        const err4 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.pcbdoc.create.config.a0" }, message: "must be equal to constant" };
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
    if (data.board_outline_mils !== void 0) {
      let data2 = data.board_outline_mils;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (!validate21(data2, { instancePath: instancePath + "/board_outline_mils", parentData: data, parentDataProperty: "board_outline_mils", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
        errors = vErrors.length;
      }
      var _valid0 = _errs13 === errors;
      valid4 = valid4 || _valid0;
      const _errs14 = errors;
      if (data2 !== null) {
        const err7 = { instancePath: instancePath + "/board_outline_mils", schemaPath: "#/properties/board_outline_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid0 = _errs14 === errors;
      valid4 = valid4 || _valid0;
      if (!valid4) {
        const err8 = { instancePath: instancePath + "/board_outline_mils", schemaPath: "#/properties/board_outline_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.layer_stack !== void 0) {
      let data3 = data.layer_stack;
      const _errs17 = errors;
      let valid5 = false;
      const _errs18 = errors;
      if (!validate23(data3, { instancePath: instancePath + "/layer_stack", parentData: data, parentDataProperty: "layer_stack", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate23.errors : vErrors.concat(validate23.errors);
        errors = vErrors.length;
      }
      var _valid1 = _errs18 === errors;
      valid5 = valid5 || _valid1;
      const _errs19 = errors;
      if (data3 !== null) {
        const err9 = { instancePath: instancePath + "/layer_stack", schemaPath: "#/properties/layer_stack/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid1 = _errs19 === errors;
      valid5 = valid5 || _valid1;
      if (!valid5) {
        const err10 = { instancePath: instancePath + "/layer_stack", schemaPath: "#/properties/layer_stack/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
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
    if (data.layer_stack_template !== void 0) {
      let data4 = data.layer_stack_template;
      const _errs22 = errors;
      let valid6 = false;
      const _errs23 = errors;
      if (typeof data4 !== "string") {
        const err11 = { instancePath: instancePath + "/layer_stack_template", schemaPath: "#/properties/layer_stack_template/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid2 = _errs23 === errors;
      valid6 = valid6 || _valid2;
      const _errs25 = errors;
      if (data4 !== null) {
        const err12 = { instancePath: instancePath + "/layer_stack_template", schemaPath: "#/properties/layer_stack_template/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid2 = _errs25 === errors;
      valid6 = valid6 || _valid2;
      if (!valid6) {
        const err13 = { instancePath: instancePath + "/layer_stack_template", schemaPath: "#/properties/layer_stack_template/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
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
    if (data.stackupx_file !== void 0) {
      let data5 = data.stackupx_file;
      const _errs28 = errors;
      let valid7 = false;
      const _errs29 = errors;
      if (typeof data5 === "string") {
        if (func1(data5) < 1) {
          const err14 = { instancePath: instancePath + "/stackupx_file", schemaPath: "#/$defs/NonemptyString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err14];
          } else {
            vErrors.push(err14);
          }
          errors++;
        }
      } else {
        const err15 = { instancePath: instancePath + "/stackupx_file", schemaPath: "#/$defs/NonemptyString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid3 = _errs29 === errors;
      valid7 = valid7 || _valid3;
      const _errs32 = errors;
      if (data5 !== null) {
        const err16 = { instancePath: instancePath + "/stackupx_file", schemaPath: "#/properties/stackupx_file/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid3 = _errs32 === errors;
      valid7 = valid7 || _valid3;
      if (!valid7) {
        const err17 = { instancePath: instancePath + "/stackupx_file", schemaPath: "#/properties/stackupx_file/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
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
    if (data.mechanical_layer_profile !== void 0) {
      let data6 = data.mechanical_layer_profile;
      const _errs35 = errors;
      let valid9 = false;
      const _errs36 = errors;
      const _errs37 = errors;
      let valid10 = false;
      const _errs38 = errors;
      if (typeof data6 !== "string") {
        const err18 = { instancePath: instancePath + "/mechanical_layer_profile", schemaPath: "#/properties/mechanical_layer_profile/anyOf/0/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
      if ("none" !== data6) {
        const err19 = { instancePath: instancePath + "/mechanical_layer_profile", schemaPath: "#/properties/mechanical_layer_profile/anyOf/0/anyOf/0/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
      var _valid5 = _errs38 === errors;
      valid10 = valid10 || _valid5;
      const _errs40 = errors;
      if (typeof data6 !== "string") {
        const err20 = { instancePath: instancePath + "/mechanical_layer_profile", schemaPath: "#/properties/mechanical_layer_profile/anyOf/0/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      if ("" !== data6) {
        const err21 = { instancePath: instancePath + "/mechanical_layer_profile", schemaPath: "#/properties/mechanical_layer_profile/anyOf/0/anyOf/1/const", keyword: "const", params: { allowedValue: "" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      var _valid5 = _errs40 === errors;
      valid10 = valid10 || _valid5;
      const _errs42 = errors;
      if (typeof data6 !== "string") {
        const err22 = { instancePath: instancePath + "/mechanical_layer_profile", schemaPath: "#/properties/mechanical_layer_profile/anyOf/0/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
      if ("standard_component_pairs" !== data6) {
        const err23 = { instancePath: instancePath + "/mechanical_layer_profile", schemaPath: "#/properties/mechanical_layer_profile/anyOf/0/anyOf/2/const", keyword: "const", params: { allowedValue: "standard_component_pairs" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      var _valid5 = _errs42 === errors;
      valid10 = valid10 || _valid5;
      const _errs44 = errors;
      if (typeof data6 !== "string") {
        const err24 = { instancePath: instancePath + "/mechanical_layer_profile", schemaPath: "#/properties/mechanical_layer_profile/anyOf/0/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      if ("standard-component-pairs" !== data6) {
        const err25 = { instancePath: instancePath + "/mechanical_layer_profile", schemaPath: "#/properties/mechanical_layer_profile/anyOf/0/anyOf/3/const", keyword: "const", params: { allowedValue: "standard-component-pairs" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
      var _valid5 = _errs44 === errors;
      valid10 = valid10 || _valid5;
      const _errs46 = errors;
      if (typeof data6 !== "string") {
        const err26 = { instancePath: instancePath + "/mechanical_layer_profile", schemaPath: "#/properties/mechanical_layer_profile/anyOf/0/anyOf/4/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
      if ("v7_mechanical_53" !== data6) {
        const err27 = { instancePath: instancePath + "/mechanical_layer_profile", schemaPath: "#/properties/mechanical_layer_profile/anyOf/0/anyOf/4/const", keyword: "const", params: { allowedValue: "v7_mechanical_53" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
      var _valid5 = _errs46 === errors;
      valid10 = valid10 || _valid5;
      const _errs48 = errors;
      if (typeof data6 !== "string") {
        const err28 = { instancePath: instancePath + "/mechanical_layer_profile", schemaPath: "#/properties/mechanical_layer_profile/anyOf/0/anyOf/5/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
      if ("v7-mechanical-53" !== data6) {
        const err29 = { instancePath: instancePath + "/mechanical_layer_profile", schemaPath: "#/properties/mechanical_layer_profile/anyOf/0/anyOf/5/const", keyword: "const", params: { allowedValue: "v7-mechanical-53" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      }
      var _valid5 = _errs48 === errors;
      valid10 = valid10 || _valid5;
      const _errs50 = errors;
      if (data6 !== null) {
        const err30 = { instancePath: instancePath + "/mechanical_layer_profile", schemaPath: "#/properties/mechanical_layer_profile/anyOf/0/anyOf/6/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
        }
        errors++;
      }
      var _valid5 = _errs50 === errors;
      valid10 = valid10 || _valid5;
      if (!valid10) {
        const err31 = { instancePath: instancePath + "/mechanical_layer_profile", schemaPath: "#/properties/mechanical_layer_profile/anyOf/0/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      } else {
        errors = _errs37;
        if (vErrors !== null) {
          if (_errs37) {
            vErrors.length = _errs37;
          } else {
            vErrors = null;
          }
        }
      }
      var _valid4 = _errs36 === errors;
      valid9 = valid9 || _valid4;
      const _errs52 = errors;
      if (typeof data6 === "string") {
        if (!pattern4.test(data6)) {
          const err32 = { instancePath: instancePath + "/mechanical_layer_profile", schemaPath: "#/properties/mechanical_layer_profile/anyOf/1/pattern", keyword: "pattern", params: { pattern: "^\\s*(?:[nN][oO][nN][eE]||[sS][tT][aA][nN][dD][aA][rR][dD]_[cC][oO][mM][pP][oO][nN][eE][nN][tT]_[pP][aA][iI][rR][sS]|[sS][tT][aA][nN][dD][aA][rR][dD]-[cC][oO][mM][pP][oO][nN][eE][nN][tT]-[pP][aA][iI][rR][sS]|[vV]7_[mM][eE][cC][hH][aA][nN][iI][cC][aA][lL]_53|[vV]7-[mM][eE][cC][hH][aA][nN][iI][cC][aA][lL]-53)\\s*$" }, message: 'must match pattern "^\\s*(?:[nN][oO][nN][eE]||[sS][tT][aA][nN][dD][aA][rR][dD]_[cC][oO][mM][pP][oO][nN][eE][nN][tT]_[pP][aA][iI][rR][sS]|[sS][tT][aA][nN][dD][aA][rR][dD]-[cC][oO][mM][pP][oO][nN][eE][nN][tT]-[pP][aA][iI][rR][sS]|[vV]7_[mM][eE][cC][hH][aA][nN][iI][cC][aA][lL]_53|[vV]7-[mM][eE][cC][hH][aA][nN][iI][cC][aA][lL]-53)\\s*$"' };
          if (vErrors === null) {
            vErrors = [err32];
          } else {
            vErrors.push(err32);
          }
          errors++;
        }
      } else {
        const err33 = { instancePath: instancePath + "/mechanical_layer_profile", schemaPath: "#/properties/mechanical_layer_profile/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
      var _valid4 = _errs52 === errors;
      valid9 = valid9 || _valid4;
      if (!valid9) {
        const err34 = { instancePath: instancePath + "/mechanical_layer_profile", schemaPath: "#/properties/mechanical_layer_profile/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
        }
        errors++;
      } else {
        errors = _errs35;
        if (vErrors !== null) {
          if (_errs35) {
            vErrors.length = _errs35;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.mechanical_layers !== void 0) {
      let data7 = data.mechanical_layers;
      const _errs55 = errors;
      let valid11 = false;
      const _errs56 = errors;
      if (Array.isArray(data7)) {
        const len0 = data7.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!validate29(data7[i0], { instancePath: instancePath + "/mechanical_layers/" + i0, parentData: data7, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate29.errors : vErrors.concat(validate29.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err35 = { instancePath: instancePath + "/mechanical_layers", schemaPath: "#/properties/mechanical_layers/anyOf/0/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err35];
        } else {
          vErrors.push(err35);
        }
        errors++;
      }
      var _valid6 = _errs56 === errors;
      valid11 = valid11 || _valid6;
      const _errs59 = errors;
      if (data7 !== null) {
        const err36 = { instancePath: instancePath + "/mechanical_layers", schemaPath: "#/properties/mechanical_layers/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err36];
        } else {
          vErrors.push(err36);
        }
        errors++;
      }
      var _valid6 = _errs59 === errors;
      valid11 = valid11 || _valid6;
      if (!valid11) {
        const err37 = { instancePath: instancePath + "/mechanical_layers", schemaPath: "#/properties/mechanical_layers/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err37];
        } else {
          vErrors.push(err37);
        }
        errors++;
      } else {
        errors = _errs55;
        if (vErrors !== null) {
          if (_errs55) {
            vErrors.length = _errs55;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.mechanical_layer_pairs !== void 0) {
      let data9 = data.mechanical_layer_pairs;
      const _errs62 = errors;
      let valid14 = false;
      const _errs63 = errors;
      if (Array.isArray(data9)) {
        const len1 = data9.length;
        for (let i1 = 0; i1 < len1; i1++) {
          let data10 = data9[i1];
          const _errs66 = errors;
          let valid17 = false;
          const _errs67 = errors;
          if (!validate31(data10, { instancePath: instancePath + "/mechanical_layer_pairs/" + i1, parentData: data9, parentDataProperty: i1, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate31.errors : vErrors.concat(validate31.errors);
            errors = vErrors.length;
          }
          var _valid8 = _errs67 === errors;
          valid17 = valid17 || _valid8;
          if (_valid8) {
            var props2 = true;
          }
          const _errs68 = errors;
          if (!validate36(data10, { instancePath: instancePath + "/mechanical_layer_pairs/" + i1, parentData: data9, parentDataProperty: i1, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate36.errors : vErrors.concat(validate36.errors);
            errors = vErrors.length;
          }
          var _valid8 = _errs68 === errors;
          valid17 = valid17 || _valid8;
          if (_valid8) {
            if (props2 !== true) {
              props2 = true;
            }
          }
          if (!valid17) {
            const err38 = { instancePath: instancePath + "/mechanical_layer_pairs/" + i1, schemaPath: "#/properties/mechanical_layer_pairs/anyOf/0/items/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err38];
            } else {
              vErrors.push(err38);
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
      } else {
        const err39 = { instancePath: instancePath + "/mechanical_layer_pairs", schemaPath: "#/properties/mechanical_layer_pairs/anyOf/0/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err39];
        } else {
          vErrors.push(err39);
        }
        errors++;
      }
      var _valid7 = _errs63 === errors;
      valid14 = valid14 || _valid7;
      const _errs69 = errors;
      if (data9 !== null) {
        const err40 = { instancePath: instancePath + "/mechanical_layer_pairs", schemaPath: "#/properties/mechanical_layer_pairs/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err40];
        } else {
          vErrors.push(err40);
        }
        errors++;
      }
      var _valid7 = _errs69 === errors;
      valid14 = valid14 || _valid7;
      if (!valid14) {
        const err41 = { instancePath: instancePath + "/mechanical_layer_pairs", schemaPath: "#/properties/mechanical_layer_pairs/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err41];
        } else {
          vErrors.push(err41);
        }
        errors++;
      } else {
        errors = _errs62;
        if (vErrors !== null) {
          if (_errs62) {
            vErrors.length = _errs62;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.mechanical_layer_kinds !== void 0) {
      let data11 = data.mechanical_layer_kinds;
      const _errs72 = errors;
      let valid18 = false;
      const _errs73 = errors;
      if (Array.isArray(data11)) {
        const len2 = data11.length;
        for (let i2 = 0; i2 < len2; i2++) {
          if (!validate38(data11[i2], { instancePath: instancePath + "/mechanical_layer_kinds/" + i2, parentData: data11, parentDataProperty: i2, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate38.errors : vErrors.concat(validate38.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err42 = { instancePath: instancePath + "/mechanical_layer_kinds", schemaPath: "#/properties/mechanical_layer_kinds/anyOf/0/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err42];
        } else {
          vErrors.push(err42);
        }
        errors++;
      }
      var _valid9 = _errs73 === errors;
      valid18 = valid18 || _valid9;
      const _errs76 = errors;
      if (data11 !== null) {
        const err43 = { instancePath: instancePath + "/mechanical_layer_kinds", schemaPath: "#/properties/mechanical_layer_kinds/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err43];
        } else {
          vErrors.push(err43);
        }
        errors++;
      }
      var _valid9 = _errs76 === errors;
      valid18 = valid18 || _valid9;
      if (!valid18) {
        const err44 = { instancePath: instancePath + "/mechanical_layer_kinds", schemaPath: "#/properties/mechanical_layer_kinds/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err44];
        } else {
          vErrors.push(err44);
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
    const err45 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err45];
    } else {
      vErrors.push(err45);
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
