// Generated from src/tsp/altium_cruncher/config/pcb-layer-step-config.tsp. Do not edit.
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
var wrapper0 = { validate: validate21 };
var func1 = require_ucs2length().default;
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
  validate22.errors = vErrors;
  return errors === 0;
}
validate22.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
  validate25.errors = vErrors;
  return errors === 0;
}
validate25.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
  validate28.errors = vErrors;
  return errors === 0;
}
validate28.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
  if (!validate28(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate28.errors : vErrors.concat(validate28.errors);
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
  validate27.errors = vErrors;
  evaluated0.props = props0;
  return errors === 0;
}
validate27.evaluated = { "dynamicProps": true, "dynamicItems": false };
function validate42(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate42.evaluated;
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
  validate42.errors = vErrors;
  return errors === 0;
}
validate42.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
  if (Array.isArray(data)) {
    const len0 = data.length;
    for (let i0 = 0; i0 < len0; i0++) {
      if (!validate42(data[i0], { instancePath: instancePath + "/" + i0, parentData: data, parentDataProperty: i0, rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate42.errors : vErrors.concat(validate42.errors);
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
  validate41.errors = vErrors;
  return errors === 0;
}
validate41.evaluated = { "items": true, "dynamicProps": false, "dynamicItems": false };
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
      if (!validate41(data.highlight_rules, { instancePath: instancePath + "/highlight_rules", parentData: data, parentDataProperty: "highlight_rules", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate41.errors : vErrors.concat(validate41.errors);
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
  validate40.errors = vErrors;
  return errors === 0;
}
validate40.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
  if (!validate40(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate40.errors : vErrors.concat(validate40.errors);
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
  validate39.errors = vErrors;
  evaluated0.props = props0;
  return errors === 0;
}
validate39.evaluated = { "dynamicProps": true, "dynamicItems": false };
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
    if (data.defaults !== void 0) {
      if (!validate25(data.defaults, { instancePath: instancePath + "/defaults", parentData: data, parentDataProperty: "defaults", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate25.errors : vErrors.concat(validate25.errors);
        errors = vErrors.length;
      }
    }
    if (data.tracks !== void 0) {
      if (!validate27(data.tracks, { instancePath: instancePath + "/tracks", parentData: data, parentDataProperty: "tracks", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate27.errors : vErrors.concat(validate27.errors);
        errors = vErrors.length;
      }
    }
    if (data.traces !== void 0) {
      if (!validate27(data.traces, { instancePath: instancePath + "/traces", parentData: data, parentDataProperty: "traces", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate27.errors : vErrors.concat(validate27.errors);
        errors = vErrors.length;
      }
    }
    if (data.arcs !== void 0) {
      if (!validate27(data.arcs, { instancePath: instancePath + "/arcs", parentData: data, parentDataProperty: "arcs", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate27.errors : vErrors.concat(validate27.errors);
        errors = vErrors.length;
      }
    }
    if (data.fills !== void 0) {
      if (!validate27(data.fills, { instancePath: instancePath + "/fills", parentData: data, parentDataProperty: "fills", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate27.errors : vErrors.concat(validate27.errors);
        errors = vErrors.length;
      }
    }
    if (data.polygons !== void 0) {
      if (!validate27(data.polygons, { instancePath: instancePath + "/polygons", parentData: data, parentDataProperty: "polygons", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate27.errors : vErrors.concat(validate27.errors);
        errors = vErrors.length;
      }
    }
    if (data.poured_polygons !== void 0) {
      if (!validate27(data.poured_polygons, { instancePath: instancePath + "/poured_polygons", parentData: data, parentDataProperty: "poured_polygons", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate27.errors : vErrors.concat(validate27.errors);
        errors = vErrors.length;
      }
    }
    if (data.regions !== void 0) {
      if (!validate27(data.regions, { instancePath: instancePath + "/regions", parentData: data, parentDataProperty: "regions", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate27.errors : vErrors.concat(validate27.errors);
        errors = vErrors.length;
      }
    }
    if (data.shapebased_regions !== void 0) {
      if (!validate27(data.shapebased_regions, { instancePath: instancePath + "/shapebased_regions", parentData: data, parentDataProperty: "shapebased_regions", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate27.errors : vErrors.concat(validate27.errors);
        errors = vErrors.length;
      }
    }
    if (data.vias !== void 0) {
      if (!validate27(data.vias, { instancePath: instancePath + "/vias", parentData: data, parentDataProperty: "vias", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate27.errors : vErrors.concat(validate27.errors);
        errors = vErrors.length;
      }
    }
    if (data.component_pads !== void 0) {
      if (!validate39(data.component_pads, { instancePath: instancePath + "/component_pads", parentData: data, parentDataProperty: "component_pads", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate39.errors : vErrors.concat(validate39.errors);
        errors = vErrors.length;
      }
    }
    if (data.free_pads !== void 0) {
      if (!validate27(data.free_pads, { instancePath: instancePath + "/free_pads", parentData: data, parentDataProperty: "free_pads", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate27.errors : vErrors.concat(validate27.errors);
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
  validate24.errors = vErrors;
  return errors === 0;
}
validate24.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate49(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate49.evaluated;
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
  validate49.errors = vErrors;
  return errors === 0;
}
validate49.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.options !== void 0) {
      if (!wrapper0.validate(data.options, { instancePath: instancePath + "/options", parentData: data, parentDataProperty: "options", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? wrapper0.validate.errors : vErrors.concat(wrapper0.validate.errors);
        errors = vErrors.length;
      }
    }
    if (data.name !== void 0) {
      let data1 = data.name;
      const _errs3 = errors;
      let valid1 = false;
      const _errs4 = errors;
      if (typeof data1 !== "string") {
        const err0 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err0];
        } else {
          vErrors.push(err0);
        }
        errors++;
      }
      var _valid0 = _errs4 === errors;
      valid1 = valid1 || _valid0;
      const _errs6 = errors;
      if (data1 !== null) {
        const err1 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      var _valid0 = _errs6 === errors;
      valid1 = valid1 || _valid0;
      if (!valid1) {
        const err2 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
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
    if (data.output_step !== void 0) {
      let data2 = data.output_step;
      const _errs9 = errors;
      let valid2 = false;
      const _errs10 = errors;
      if (typeof data2 !== "string") {
        const err3 = { instancePath: instancePath + "/output_step", schemaPath: "#/properties/output_step/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      var _valid1 = _errs10 === errors;
      valid2 = valid2 || _valid1;
      const _errs12 = errors;
      if (data2 !== null) {
        const err4 = { instancePath: instancePath + "/output_step", schemaPath: "#/properties/output_step/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid1 = _errs12 === errors;
      valid2 = valid2 || _valid1;
      if (!valid2) {
        const err5 = { instancePath: instancePath + "/output_step", schemaPath: "#/properties/output_step/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
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
    if (data.pcbdoc !== void 0) {
      let data3 = data.pcbdoc;
      const _errs15 = errors;
      let valid3 = false;
      const _errs16 = errors;
      if (typeof data3 !== "string") {
        const err6 = { instancePath: instancePath + "/pcbdoc", schemaPath: "#/properties/pcbdoc/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid2 = _errs16 === errors;
      valid3 = valid3 || _valid2;
      const _errs18 = errors;
      if (data3 !== null) {
        const err7 = { instancePath: instancePath + "/pcbdoc", schemaPath: "#/properties/pcbdoc/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid2 = _errs18 === errors;
      valid3 = valid3 || _valid2;
      if (!valid3) {
        const err8 = { instancePath: instancePath + "/pcbdoc", schemaPath: "#/properties/pcbdoc/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.layer !== void 0) {
      let data4 = data.layer;
      const _errs22 = errors;
      let valid5 = false;
      const _errs23 = errors;
      if (typeof data4 !== "string") {
        const err9 = { instancePath: instancePath + "/layer", schemaPath: "#/$defs/LayerSelector/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid3 = _errs23 === errors;
      valid5 = valid5 || _valid3;
      const _errs25 = errors;
      if (!(typeof data4 == "number" && (!(data4 % 1) && !isNaN(data4)))) {
        const err10 = { instancePath: instancePath + "/layer", schemaPath: "#/$defs/LayerSelector/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid3 = _errs25 === errors;
      valid5 = valid5 || _valid3;
      const _errs27 = errors;
      if (data4 !== null) {
        const err11 = { instancePath: instancePath + "/layer", schemaPath: "#/$defs/LayerSelector/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid3 = _errs27 === errors;
      valid5 = valid5 || _valid3;
      if (!valid5) {
        const err12 = { instancePath: instancePath + "/layer", schemaPath: "#/$defs/LayerSelector/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
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
    if (data.thickness_mm !== void 0) {
      let data5 = data.thickness_mm;
      if (typeof data5 == "number") {
        if (data5 <= 0 || isNaN(data5)) {
          const err13 = { instancePath: instancePath + "/thickness_mm", schemaPath: "#/properties/thickness_mm/exclusiveMinimum", keyword: "exclusiveMinimum", params: { comparison: ">", limit: 0 }, message: "must be > 0" };
          if (vErrors === null) {
            vErrors = [err13];
          } else {
            vErrors.push(err13);
          }
          errors++;
        }
      } else {
        const err14 = { instancePath: instancePath + "/thickness_mm", schemaPath: "#/properties/thickness_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
    }
    if (data.z_mm !== void 0) {
      if (!(typeof data.z_mm == "number")) {
        const err15 = { instancePath: instancePath + "/z_mm", schemaPath: "#/properties/z_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
    }
    if (data.copper_color !== void 0) {
      let data7 = data.copper_color;
      if (typeof data7 === "string") {
        if (func1(data7) < 1) {
          const err16 = { instancePath: instancePath + "/copper_color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err16];
          } else {
            vErrors.push(err16);
          }
          errors++;
        }
      } else {
        const err17 = { instancePath: instancePath + "/copper_color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
    }
    if (data.outline_width_mm !== void 0) {
      let data8 = data.outline_width_mm;
      if (typeof data8 == "number") {
        if (data8 < 0 || isNaN(data8)) {
          const err18 = { instancePath: instancePath + "/outline_width_mm", schemaPath: "#/properties/outline_width_mm/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err18];
          } else {
            vErrors.push(err18);
          }
          errors++;
        }
      } else {
        const err19 = { instancePath: instancePath + "/outline_width_mm", schemaPath: "#/properties/outline_width_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
    }
    if (data.outline_color !== void 0) {
      let data9 = data.outline_color;
      if (typeof data9 === "string") {
        if (func1(data9) < 1) {
          const err20 = { instancePath: instancePath + "/outline_color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err20];
          } else {
            vErrors.push(err20);
          }
          errors++;
        }
      } else {
        const err21 = { instancePath: instancePath + "/outline_color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
    }
    if (data.board_cutout_color !== void 0) {
      let data10 = data.board_cutout_color;
      if (typeof data10 === "string") {
        if (func1(data10) < 1) {
          const err22 = { instancePath: instancePath + "/board_cutout_color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err22];
          } else {
            vErrors.push(err22);
          }
          errors++;
        }
      } else {
        const err23 = { instancePath: instancePath + "/board_cutout_color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
    }
    if (data.include_board_cutouts !== void 0) {
      if (typeof data.include_board_cutouts !== "boolean") {
        const err24 = { instancePath: instancePath + "/include_board_cutouts", schemaPath: "#/properties/include_board_cutouts/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
    }
    if (data.include_copper !== void 0) {
      if (typeof data.include_copper !== "boolean") {
        const err25 = { instancePath: instancePath + "/include_copper", schemaPath: "#/properties/include_copper/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
    }
    if (data.include_board_outline !== void 0) {
      if (typeof data.include_board_outline !== "boolean") {
        const err26 = { instancePath: instancePath + "/include_board_outline", schemaPath: "#/properties/include_board_outline/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
    }
    if (data.include_poured_polygons !== void 0) {
      if (typeof data.include_poured_polygons !== "boolean") {
        const err27 = { instancePath: instancePath + "/include_poured_polygons", schemaPath: "#/properties/include_poured_polygons/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
    }
    if (data.cut_holes !== void 0) {
      if (typeof data.cut_holes !== "boolean") {
        const err28 = { instancePath: instancePath + "/cut_holes", schemaPath: "#/properties/cut_holes/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
    }
    if (data.drill_hole_mode !== void 0) {
      let data16 = data.drill_hole_mode;
      const _errs56 = errors;
      let valid10 = false;
      const _errs57 = errors;
      if (typeof data16 !== "string") {
        const err29 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      }
      if ("auto" !== data16) {
        const err30 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf/0/const", keyword: "const", params: { allowedValue: "auto" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
        }
        errors++;
      }
      var _valid4 = _errs57 === errors;
      valid10 = valid10 || _valid4;
      const _errs59 = errors;
      if (typeof data16 !== "string") {
        const err31 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      }
      if ("cut" !== data16) {
        const err32 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf/1/const", keyword: "const", params: { allowedValue: "cut" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
        }
        errors++;
      }
      var _valid4 = _errs59 === errors;
      valid10 = valid10 || _valid4;
      const _errs61 = errors;
      if (typeof data16 !== "string") {
        const err33 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
      if ("overlay" !== data16) {
        const err34 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf/2/const", keyword: "const", params: { allowedValue: "overlay" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
        }
        errors++;
      }
      var _valid4 = _errs61 === errors;
      valid10 = valid10 || _valid4;
      const _errs63 = errors;
      if (typeof data16 !== "string") {
        const err35 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err35];
        } else {
          vErrors.push(err35);
        }
        errors++;
      }
      if ("none" !== data16) {
        const err36 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf/3/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err36];
        } else {
          vErrors.push(err36);
        }
        errors++;
      }
      var _valid4 = _errs63 === errors;
      valid10 = valid10 || _valid4;
      if (!valid10) {
        const err37 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err37];
        } else {
          vErrors.push(err37);
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
    if (data.max_boolean_drill_cuts !== void 0) {
      let data17 = data.max_boolean_drill_cuts;
      if (!(typeof data17 == "number" && (!(data17 % 1) && !isNaN(data17)))) {
        const err38 = { instancePath: instancePath + "/max_boolean_drill_cuts", schemaPath: "#/properties/max_boolean_drill_cuts/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err38];
        } else {
          vErrors.push(err38);
        }
        errors++;
      }
      if (typeof data17 == "number") {
        if (data17 < 0 || isNaN(data17)) {
          const err39 = { instancePath: instancePath + "/max_boolean_drill_cuts", schemaPath: "#/properties/max_boolean_drill_cuts/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err39];
          } else {
            vErrors.push(err39);
          }
          errors++;
        }
      }
    }
    if (data.drill_hole_color !== void 0) {
      let data18 = data.drill_hole_color;
      if (typeof data18 === "string") {
        if (func1(data18) < 1) {
          const err40 = { instancePath: instancePath + "/drill_hole_color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err40];
          } else {
            vErrors.push(err40);
          }
          errors++;
        }
      } else {
        const err41 = { instancePath: instancePath + "/drill_hole_color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err41];
        } else {
          vErrors.push(err41);
        }
        errors++;
      }
    }
    if (data.drill_plated_hole_color !== void 0) {
      let data19 = data.drill_plated_hole_color;
      if (typeof data19 === "string") {
        if (func1(data19) < 1) {
          const err42 = { instancePath: instancePath + "/drill_plated_hole_color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err42];
          } else {
            vErrors.push(err42);
          }
          errors++;
        }
      } else {
        const err43 = { instancePath: instancePath + "/drill_plated_hole_color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err43];
        } else {
          vErrors.push(err43);
        }
        errors++;
      }
    }
    if (data.drill_non_plated_hole_color !== void 0) {
      let data20 = data.drill_non_plated_hole_color;
      if (typeof data20 === "string") {
        if (func1(data20) < 1) {
          const err44 = { instancePath: instancePath + "/drill_non_plated_hole_color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err44];
          } else {
            vErrors.push(err44);
          }
          errors++;
        }
      } else {
        const err45 = { instancePath: instancePath + "/drill_non_plated_hole_color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err45];
        } else {
          vErrors.push(err45);
        }
        errors++;
      }
    }
    if (data.drill_overlay_thickness_mm !== void 0) {
      let data21 = data.drill_overlay_thickness_mm;
      if (typeof data21 == "number") {
        if (data21 < 0 || isNaN(data21)) {
          const err46 = { instancePath: instancePath + "/drill_overlay_thickness_mm", schemaPath: "#/properties/drill_overlay_thickness_mm/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err46];
          } else {
            vErrors.push(err46);
          }
          errors++;
        }
      } else {
        const err47 = { instancePath: instancePath + "/drill_overlay_thickness_mm", schemaPath: "#/properties/drill_overlay_thickness_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err47];
        } else {
          vErrors.push(err47);
        }
        errors++;
      }
    }
    if (data.drill_minimum_diameter_mm !== void 0) {
      let data22 = data.drill_minimum_diameter_mm;
      if (typeof data22 == "number") {
        if (data22 < 0 || isNaN(data22)) {
          const err48 = { instancePath: instancePath + "/drill_minimum_diameter_mm", schemaPath: "#/properties/drill_minimum_diameter_mm/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err48];
          } else {
            vErrors.push(err48);
          }
          errors++;
        }
      } else {
        const err49 = { instancePath: instancePath + "/drill_minimum_diameter_mm", schemaPath: "#/properties/drill_minimum_diameter_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err49];
        } else {
          vErrors.push(err49);
        }
        errors++;
      }
    }
    if (data.drill_hole_shape !== void 0) {
      let data23 = data.drill_hole_shape;
      const _errs82 = errors;
      let valid15 = false;
      const _errs83 = errors;
      if (typeof data23 !== "string") {
        const err50 = { instancePath: instancePath + "/drill_hole_shape", schemaPath: "#/$defs/DrillShape/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err50];
        } else {
          vErrors.push(err50);
        }
        errors++;
      }
      if ("solid" !== data23) {
        const err51 = { instancePath: instancePath + "/drill_hole_shape", schemaPath: "#/$defs/DrillShape/anyOf/0/const", keyword: "const", params: { allowedValue: "solid" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err51];
        } else {
          vErrors.push(err51);
        }
        errors++;
      }
      var _valid5 = _errs83 === errors;
      valid15 = valid15 || _valid5;
      const _errs85 = errors;
      if (typeof data23 !== "string") {
        const err52 = { instancePath: instancePath + "/drill_hole_shape", schemaPath: "#/$defs/DrillShape/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err52];
        } else {
          vErrors.push(err52);
        }
        errors++;
      }
      if ("ring" !== data23) {
        const err53 = { instancePath: instancePath + "/drill_hole_shape", schemaPath: "#/$defs/DrillShape/anyOf/1/const", keyword: "const", params: { allowedValue: "ring" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err53];
        } else {
          vErrors.push(err53);
        }
        errors++;
      }
      var _valid5 = _errs85 === errors;
      valid15 = valid15 || _valid5;
      if (!valid15) {
        const err54 = { instancePath: instancePath + "/drill_hole_shape", schemaPath: "#/$defs/DrillShape/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err54];
        } else {
          vErrors.push(err54);
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
    if (data.drill_ring_width_mm !== void 0) {
      let data24 = data.drill_ring_width_mm;
      if (typeof data24 == "number") {
        if (data24 < 0 || isNaN(data24)) {
          const err55 = { instancePath: instancePath + "/drill_ring_width_mm", schemaPath: "#/properties/drill_ring_width_mm/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err55];
          } else {
            vErrors.push(err55);
          }
          errors++;
        }
      } else {
        const err56 = { instancePath: instancePath + "/drill_ring_width_mm", schemaPath: "#/properties/drill_ring_width_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err56];
        } else {
          vErrors.push(err56);
        }
        errors++;
      }
    }
    if (data.drill_plated_ring_shape !== void 0) {
      let data25 = data.drill_plated_ring_shape;
      const _errs91 = errors;
      let valid17 = false;
      const _errs92 = errors;
      if (typeof data25 !== "string") {
        const err57 = { instancePath: instancePath + "/drill_plated_ring_shape", schemaPath: "#/$defs/PlatedRingShape/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err57];
        } else {
          vErrors.push(err57);
        }
        errors++;
      }
      if ("annulus" !== data25) {
        const err58 = { instancePath: instancePath + "/drill_plated_ring_shape", schemaPath: "#/$defs/PlatedRingShape/anyOf/0/const", keyword: "const", params: { allowedValue: "annulus" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err58];
        } else {
          vErrors.push(err58);
        }
        errors++;
      }
      var _valid6 = _errs92 === errors;
      valid17 = valid17 || _valid6;
      if (!valid17) {
        const err59 = { instancePath: instancePath + "/drill_plated_ring_shape", schemaPath: "#/$defs/PlatedRingShape/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err59];
        } else {
          vErrors.push(err59);
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
    if (data.drill_selected_component_mode !== void 0) {
      let data26 = data.drill_selected_component_mode;
      const _errs96 = errors;
      let valid19 = false;
      const _errs97 = errors;
      if (typeof data26 !== "string") {
        const err60 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err60];
        } else {
          vErrors.push(err60);
        }
        errors++;
      }
      if ("inherit" !== data26) {
        const err61 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/const", keyword: "const", params: { allowedValue: "inherit" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err61];
        } else {
          vErrors.push(err61);
        }
        errors++;
      }
      var _valid7 = _errs97 === errors;
      valid19 = valid19 || _valid7;
      const _errs99 = errors;
      if (typeof data26 !== "string") {
        const err62 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err62];
        } else {
          vErrors.push(err62);
        }
        errors++;
      }
      if ("cut" !== data26) {
        const err63 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/const", keyword: "const", params: { allowedValue: "cut" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err63];
        } else {
          vErrors.push(err63);
        }
        errors++;
      }
      var _valid7 = _errs99 === errors;
      valid19 = valid19 || _valid7;
      const _errs101 = errors;
      if (typeof data26 !== "string") {
        const err64 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err64];
        } else {
          vErrors.push(err64);
        }
        errors++;
      }
      if ("overlay" !== data26) {
        const err65 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/const", keyword: "const", params: { allowedValue: "overlay" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err65];
        } else {
          vErrors.push(err65);
        }
        errors++;
      }
      var _valid7 = _errs101 === errors;
      valid19 = valid19 || _valid7;
      const _errs103 = errors;
      if (typeof data26 !== "string") {
        const err66 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err66];
        } else {
          vErrors.push(err66);
        }
        errors++;
      }
      if ("none" !== data26) {
        const err67 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err67];
        } else {
          vErrors.push(err67);
        }
        errors++;
      }
      var _valid7 = _errs103 === errors;
      valid19 = valid19 || _valid7;
      if (!valid19) {
        const err68 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err68];
        } else {
          vErrors.push(err68);
        }
        errors++;
      } else {
        errors = _errs96;
        if (vErrors !== null) {
          if (_errs96) {
            vErrors.length = _errs96;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.drill_other_component_mode !== void 0) {
      let data27 = data.drill_other_component_mode;
      const _errs107 = errors;
      let valid21 = false;
      const _errs108 = errors;
      if (typeof data27 !== "string") {
        const err69 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err69];
        } else {
          vErrors.push(err69);
        }
        errors++;
      }
      if ("inherit" !== data27) {
        const err70 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/const", keyword: "const", params: { allowedValue: "inherit" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err70];
        } else {
          vErrors.push(err70);
        }
        errors++;
      }
      var _valid8 = _errs108 === errors;
      valid21 = valid21 || _valid8;
      const _errs110 = errors;
      if (typeof data27 !== "string") {
        const err71 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err71];
        } else {
          vErrors.push(err71);
        }
        errors++;
      }
      if ("cut" !== data27) {
        const err72 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/const", keyword: "const", params: { allowedValue: "cut" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err72];
        } else {
          vErrors.push(err72);
        }
        errors++;
      }
      var _valid8 = _errs110 === errors;
      valid21 = valid21 || _valid8;
      const _errs112 = errors;
      if (typeof data27 !== "string") {
        const err73 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err73];
        } else {
          vErrors.push(err73);
        }
        errors++;
      }
      if ("overlay" !== data27) {
        const err74 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/const", keyword: "const", params: { allowedValue: "overlay" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err74];
        } else {
          vErrors.push(err74);
        }
        errors++;
      }
      var _valid8 = _errs112 === errors;
      valid21 = valid21 || _valid8;
      const _errs114 = errors;
      if (typeof data27 !== "string") {
        const err75 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err75];
        } else {
          vErrors.push(err75);
        }
        errors++;
      }
      if ("none" !== data27) {
        const err76 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err76];
        } else {
          vErrors.push(err76);
        }
        errors++;
      }
      var _valid8 = _errs114 === errors;
      valid21 = valid21 || _valid8;
      if (!valid21) {
        const err77 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err77];
        } else {
          vErrors.push(err77);
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
    if (data.drill_free_pad_mode !== void 0) {
      let data28 = data.drill_free_pad_mode;
      const _errs118 = errors;
      let valid23 = false;
      const _errs119 = errors;
      if (typeof data28 !== "string") {
        const err78 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err78];
        } else {
          vErrors.push(err78);
        }
        errors++;
      }
      if ("inherit" !== data28) {
        const err79 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/const", keyword: "const", params: { allowedValue: "inherit" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err79];
        } else {
          vErrors.push(err79);
        }
        errors++;
      }
      var _valid9 = _errs119 === errors;
      valid23 = valid23 || _valid9;
      const _errs121 = errors;
      if (typeof data28 !== "string") {
        const err80 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err80];
        } else {
          vErrors.push(err80);
        }
        errors++;
      }
      if ("cut" !== data28) {
        const err81 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/const", keyword: "const", params: { allowedValue: "cut" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err81];
        } else {
          vErrors.push(err81);
        }
        errors++;
      }
      var _valid9 = _errs121 === errors;
      valid23 = valid23 || _valid9;
      const _errs123 = errors;
      if (typeof data28 !== "string") {
        const err82 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err82];
        } else {
          vErrors.push(err82);
        }
        errors++;
      }
      if ("overlay" !== data28) {
        const err83 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/const", keyword: "const", params: { allowedValue: "overlay" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err83];
        } else {
          vErrors.push(err83);
        }
        errors++;
      }
      var _valid9 = _errs123 === errors;
      valid23 = valid23 || _valid9;
      const _errs125 = errors;
      if (typeof data28 !== "string") {
        const err84 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err84];
        } else {
          vErrors.push(err84);
        }
        errors++;
      }
      if ("none" !== data28) {
        const err85 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err85];
        } else {
          vErrors.push(err85);
        }
        errors++;
      }
      var _valid9 = _errs125 === errors;
      valid23 = valid23 || _valid9;
      if (!valid23) {
        const err86 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err86];
        } else {
          vErrors.push(err86);
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
    }
    if (data.drill_via_mode !== void 0) {
      let data29 = data.drill_via_mode;
      const _errs129 = errors;
      let valid25 = false;
      const _errs130 = errors;
      if (typeof data29 !== "string") {
        const err87 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err87];
        } else {
          vErrors.push(err87);
        }
        errors++;
      }
      if ("inherit" !== data29) {
        const err88 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/const", keyword: "const", params: { allowedValue: "inherit" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err88];
        } else {
          vErrors.push(err88);
        }
        errors++;
      }
      var _valid10 = _errs130 === errors;
      valid25 = valid25 || _valid10;
      const _errs132 = errors;
      if (typeof data29 !== "string") {
        const err89 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err89];
        } else {
          vErrors.push(err89);
        }
        errors++;
      }
      if ("cut" !== data29) {
        const err90 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/const", keyword: "const", params: { allowedValue: "cut" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err90];
        } else {
          vErrors.push(err90);
        }
        errors++;
      }
      var _valid10 = _errs132 === errors;
      valid25 = valid25 || _valid10;
      const _errs134 = errors;
      if (typeof data29 !== "string") {
        const err91 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err91];
        } else {
          vErrors.push(err91);
        }
        errors++;
      }
      if ("overlay" !== data29) {
        const err92 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/const", keyword: "const", params: { allowedValue: "overlay" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err92];
        } else {
          vErrors.push(err92);
        }
        errors++;
      }
      var _valid10 = _errs134 === errors;
      valid25 = valid25 || _valid10;
      const _errs136 = errors;
      if (typeof data29 !== "string") {
        const err93 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err93];
        } else {
          vErrors.push(err93);
        }
        errors++;
      }
      if ("none" !== data29) {
        const err94 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err94];
        } else {
          vErrors.push(err94);
        }
        errors++;
      }
      var _valid10 = _errs136 === errors;
      valid25 = valid25 || _valid10;
      if (!valid25) {
        const err95 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err95];
        } else {
          vErrors.push(err95);
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
    }
    if (data.fuse_copper !== void 0) {
      if (typeof data.fuse_copper !== "boolean") {
        const err96 = { instancePath: instancePath + "/fuse_copper", schemaPath: "#/properties/fuse_copper/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err96];
        } else {
          vErrors.push(err96);
        }
        errors++;
      }
    }
    if (data.fuse_board_outline !== void 0) {
      if (typeof data.fuse_board_outline !== "boolean") {
        const err97 = { instancePath: instancePath + "/fuse_board_outline", schemaPath: "#/properties/fuse_board_outline/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err97];
        } else {
          vErrors.push(err97);
        }
        errors++;
      }
    }
    if (data.arc_segments !== void 0) {
      let data32 = data.arc_segments;
      if (!(typeof data32 == "number" && (!(data32 % 1) && !isNaN(data32)))) {
        const err98 = { instancePath: instancePath + "/arc_segments", schemaPath: "#/properties/arc_segments/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err98];
        } else {
          vErrors.push(err98);
        }
        errors++;
      }
      if (typeof data32 == "number") {
        if (data32 < 1 || isNaN(data32)) {
          const err99 = { instancePath: instancePath + "/arc_segments", schemaPath: "#/properties/arc_segments/minimum", keyword: "minimum", params: { comparison: ">=", limit: 1 }, message: "must be >= 1" };
          if (vErrors === null) {
            vErrors = [err99];
          } else {
            vErrors.push(err99);
          }
          errors++;
        }
      }
    }
    if (data.include_tracks !== void 0) {
      if (typeof data.include_tracks !== "boolean") {
        const err100 = { instancePath: instancePath + "/include_tracks", schemaPath: "#/properties/include_tracks/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err100];
        } else {
          vErrors.push(err100);
        }
        errors++;
      }
    }
    if (data.include_arcs !== void 0) {
      if (typeof data.include_arcs !== "boolean") {
        const err101 = { instancePath: instancePath + "/include_arcs", schemaPath: "#/properties/include_arcs/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err101];
        } else {
          vErrors.push(err101);
        }
        errors++;
      }
    }
    if (data.include_fills !== void 0) {
      if (typeof data.include_fills !== "boolean") {
        const err102 = { instancePath: instancePath + "/include_fills", schemaPath: "#/properties/include_fills/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err102];
        } else {
          vErrors.push(err102);
        }
        errors++;
      }
    }
    if (data.include_regions !== void 0) {
      if (typeof data.include_regions !== "boolean") {
        const err103 = { instancePath: instancePath + "/include_regions", schemaPath: "#/properties/include_regions/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err103];
        } else {
          vErrors.push(err103);
        }
        errors++;
      }
    }
    if (data.include_vias !== void 0) {
      if (typeof data.include_vias !== "boolean") {
        const err104 = { instancePath: instancePath + "/include_vias", schemaPath: "#/properties/include_vias/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err104];
        } else {
          vErrors.push(err104);
        }
        errors++;
      }
    }
    if (data.include_component_pads !== void 0) {
      if (typeof data.include_component_pads !== "boolean") {
        const err105 = { instancePath: instancePath + "/include_component_pads", schemaPath: "#/properties/include_component_pads/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err105];
        } else {
          vErrors.push(err105);
        }
        errors++;
      }
    }
    if (data.include_free_pads !== void 0) {
      if (typeof data.include_free_pads !== "boolean") {
        const err106 = { instancePath: instancePath + "/include_free_pads", schemaPath: "#/properties/include_free_pads/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err106];
        } else {
          vErrors.push(err106);
        }
        errors++;
      }
    }
    if (data.include_designators !== void 0) {
      let data40 = data.include_designators;
      const _errs160 = errors;
      let valid27 = false;
      let passing0 = null;
      const _errs161 = errors;
      if (typeof data40 !== "string") {
        const err107 = { instancePath: instancePath + "/include_designators", schemaPath: "#/$defs/StringList/oneOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err107];
        } else {
          vErrors.push(err107);
        }
        errors++;
      }
      var _valid11 = _errs161 === errors;
      if (_valid11) {
        valid27 = true;
        passing0 = 0;
      }
      const _errs163 = errors;
      if (Array.isArray(data40)) {
        const len0 = data40.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (typeof data40[i0] !== "string") {
            const err108 = { instancePath: instancePath + "/include_designators/" + i0, schemaPath: "#/$defs/StringList/oneOf/1/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err108];
            } else {
              vErrors.push(err108);
            }
            errors++;
          }
        }
      } else {
        const err109 = { instancePath: instancePath + "/include_designators", schemaPath: "#/$defs/StringList/oneOf/1/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err109];
        } else {
          vErrors.push(err109);
        }
        errors++;
      }
      var _valid11 = _errs163 === errors;
      if (_valid11 && valid27) {
        valid27 = false;
        passing0 = [passing0, 1];
      } else {
        if (_valid11) {
          valid27 = true;
          passing0 = 1;
        }
      }
      if (!valid27) {
        const err110 = { instancePath: instancePath + "/include_designators", schemaPath: "#/$defs/StringList/oneOf", keyword: "oneOf", params: { passingSchemas: passing0 }, message: "must match exactly one schema in oneOf" };
        if (vErrors === null) {
          vErrors = [err110];
        } else {
          vErrors.push(err110);
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
    if (data.board_outline !== void 0) {
      if (!validate22(data.board_outline, { instancePath: instancePath + "/board_outline", parentData: data, parentDataProperty: "board_outline", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate22.errors : vErrors.concat(validate22.errors);
        errors = vErrors.length;
      }
    }
    if (data.features !== void 0) {
      if (!validate24(data.features, { instancePath: instancePath + "/features", parentData: data, parentDataProperty: "features", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate24.errors : vErrors.concat(validate24.errors);
        errors = vErrors.length;
      }
    }
    if (data.drills !== void 0) {
      if (!validate49(data.drills, { instancePath: instancePath + "/drills", parentData: data, parentDataProperty: "drills", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate49.errors : vErrors.concat(validate49.errors);
        errors = vErrors.length;
      }
    }
    for (const key0 in data) {
      if (key0 !== "options" && key0 !== "name" && key0 !== "output_step" && key0 !== "pcbdoc" && key0 !== "layer" && key0 !== "thickness_mm" && key0 !== "z_mm" && key0 !== "copper_color" && key0 !== "outline_width_mm" && key0 !== "outline_color" && key0 !== "board_cutout_color" && key0 !== "include_board_cutouts" && key0 !== "include_copper" && key0 !== "include_board_outline" && key0 !== "include_poured_polygons" && key0 !== "cut_holes" && key0 !== "drill_hole_mode" && key0 !== "max_boolean_drill_cuts" && key0 !== "drill_hole_color" && key0 !== "drill_plated_hole_color" && key0 !== "drill_non_plated_hole_color" && key0 !== "drill_overlay_thickness_mm" && key0 !== "drill_minimum_diameter_mm" && key0 !== "drill_hole_shape" && key0 !== "drill_ring_width_mm" && key0 !== "drill_plated_ring_shape" && key0 !== "drill_selected_component_mode" && key0 !== "drill_other_component_mode" && key0 !== "drill_free_pad_mode" && key0 !== "drill_via_mode" && key0 !== "fuse_copper" && key0 !== "fuse_board_outline" && key0 !== "arc_segments" && key0 !== "include_tracks" && key0 !== "include_arcs" && key0 !== "include_fills" && key0 !== "include_regions" && key0 !== "include_vias" && key0 !== "include_component_pads" && key0 !== "include_free_pads" && key0 !== "include_designators" && key0 !== "board_outline" && key0 !== "features" && key0 !== "drills") {
        const err111 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err111];
        } else {
          vErrors.push(err111);
        }
        errors++;
      }
    }
  } else {
    const err112 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err112];
    } else {
      vErrors.push(err112);
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
  const _errs3 = errors;
  let valid1 = true;
  const _errs4 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    let missing0;
    if (data.outputs === void 0 && (missing0 = "outputs")) {
      const err0 = {};
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
  }
  var _valid0 = _errs4 === errors;
  errors = _errs3;
  if (vErrors !== null) {
    if (_errs3) {
      vErrors.length = _errs3;
    } else {
      vErrors = null;
    }
  }
  if (_valid0) {
    const _errs5 = errors;
    if (data && typeof data == "object" && !Array.isArray(data)) {
      if (data.schema !== void 0) {
        if ("altium_cruncher.pcb_layer_step.config.a0" !== data.schema) {
          const err1 = { instancePath: instancePath + "/schema", schemaPath: "#/allOf/0/then/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.pcb_layer_step.config.a0" }, message: "must be equal to constant" };
          if (vErrors === null) {
            vErrors = [err1];
          } else {
            vErrors.push(err1);
          }
          errors++;
        }
      }
    }
    var _valid0 = _errs5 === errors;
    valid1 = _valid0;
    if (valid1) {
      var props0 = {};
      props0.schema = true;
    }
  }
  if (!valid1) {
    const err2 = { instancePath, schemaPath: "#/allOf/0/if", keyword: "if", params: { failingKeyword: "then" }, message: 'must match "then" schema' };
    if (vErrors === null) {
      vErrors = [err2];
    } else {
      vErrors.push(err2);
    }
    errors++;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (props0 !== true) {
      props0 = props0 || {};
      props0.schema = true;
      props0.defaults = true;
      props0.outputs = true;
      props0.options = true;
      props0.name = true;
      props0.output_step = true;
      props0.pcbdoc = true;
      props0.layer = true;
      props0.thickness_mm = true;
      props0.z_mm = true;
      props0.copper_color = true;
      props0.outline_width_mm = true;
      props0.outline_color = true;
      props0.board_cutout_color = true;
      props0.include_board_cutouts = true;
      props0.include_copper = true;
      props0.include_board_outline = true;
      props0.include_poured_polygons = true;
      props0.cut_holes = true;
      props0.drill_hole_mode = true;
      props0.max_boolean_drill_cuts = true;
      props0.drill_hole_color = true;
      props0.drill_plated_hole_color = true;
      props0.drill_non_plated_hole_color = true;
      props0.drill_overlay_thickness_mm = true;
      props0.drill_minimum_diameter_mm = true;
      props0.drill_hole_shape = true;
      props0.drill_ring_width_mm = true;
      props0.drill_plated_ring_shape = true;
      props0.drill_selected_component_mode = true;
      props0.drill_other_component_mode = true;
      props0.drill_free_pad_mode = true;
      props0.drill_via_mode = true;
      props0.fuse_copper = true;
      props0.fuse_board_outline = true;
      props0.arc_segments = true;
      props0.include_tracks = true;
      props0.include_arcs = true;
      props0.include_fills = true;
      props0.include_regions = true;
      props0.include_vias = true;
      props0.include_component_pads = true;
      props0.include_free_pads = true;
      props0.include_designators = true;
      props0.board_outline = true;
      props0.features = true;
      props0.drills = true;
    }
    if (data.schema !== void 0) {
      let data1 = data.schema;
      const _errs8 = errors;
      let valid4 = false;
      const _errs9 = errors;
      if (typeof data1 !== "string") {
        const err3 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      if ("altium_cruncher.pcb_layer_step.config.a0" !== data1) {
        const err4 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf/0/const", keyword: "const", params: { allowedValue: "altium_cruncher.pcb_layer_step.config.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid1 = _errs9 === errors;
      valid4 = valid4 || _valid1;
      const _errs11 = errors;
      if (data1 !== null) {
        const err5 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid1 = _errs11 === errors;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err6 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.defaults !== void 0) {
      if (!validate21(data.defaults, { instancePath: instancePath + "/defaults", parentData: data, parentDataProperty: "defaults", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
        errors = vErrors.length;
      }
    }
    if (data.outputs !== void 0) {
      let data3 = data.outputs;
      if (Array.isArray(data3)) {
        if (data3.length < 1) {
          const err7 = { instancePath: instancePath + "/outputs", schemaPath: "#/properties/outputs/minItems", keyword: "minItems", params: { limit: 1 }, message: "must NOT have fewer than 1 items" };
          if (vErrors === null) {
            vErrors = [err7];
          } else {
            vErrors.push(err7);
          }
          errors++;
        }
        const len0 = data3.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!validate21(data3[i0], { instancePath: instancePath + "/outputs/" + i0, parentData: data3, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err8 = { instancePath: instancePath + "/outputs", schemaPath: "#/properties/outputs/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
    if (data.options !== void 0) {
      if (!validate21(data.options, { instancePath: instancePath + "/options", parentData: data, parentDataProperty: "options", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
        errors = vErrors.length;
      }
    }
    if (data.name !== void 0) {
      let data6 = data.name;
      const _errs19 = errors;
      let valid7 = false;
      const _errs20 = errors;
      if (typeof data6 !== "string") {
        const err9 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs20 === errors;
      valid7 = valid7 || _valid2;
      const _errs22 = errors;
      if (data6 !== null) {
        const err10 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs22 === errors;
      valid7 = valid7 || _valid2;
      if (!valid7) {
        const err11 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.output_step !== void 0) {
      let data7 = data.output_step;
      const _errs25 = errors;
      let valid8 = false;
      const _errs26 = errors;
      if (typeof data7 !== "string") {
        const err12 = { instancePath: instancePath + "/output_step", schemaPath: "#/properties/output_step/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid3 = _errs26 === errors;
      valid8 = valid8 || _valid3;
      const _errs28 = errors;
      if (data7 !== null) {
        const err13 = { instancePath: instancePath + "/output_step", schemaPath: "#/properties/output_step/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid3 = _errs28 === errors;
      valid8 = valid8 || _valid3;
      if (!valid8) {
        const err14 = { instancePath: instancePath + "/output_step", schemaPath: "#/properties/output_step/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.pcbdoc !== void 0) {
      let data8 = data.pcbdoc;
      const _errs31 = errors;
      let valid9 = false;
      const _errs32 = errors;
      if (typeof data8 !== "string") {
        const err15 = { instancePath: instancePath + "/pcbdoc", schemaPath: "#/properties/pcbdoc/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid4 = _errs32 === errors;
      valid9 = valid9 || _valid4;
      const _errs34 = errors;
      if (data8 !== null) {
        const err16 = { instancePath: instancePath + "/pcbdoc", schemaPath: "#/properties/pcbdoc/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid4 = _errs34 === errors;
      valid9 = valid9 || _valid4;
      if (!valid9) {
        const err17 = { instancePath: instancePath + "/pcbdoc", schemaPath: "#/properties/pcbdoc/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
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
    if (data.layer !== void 0) {
      let data9 = data.layer;
      const _errs38 = errors;
      let valid11 = false;
      const _errs39 = errors;
      if (typeof data9 !== "string") {
        const err18 = { instancePath: instancePath + "/layer", schemaPath: "#/$defs/LayerSelector/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
      var _valid5 = _errs39 === errors;
      valid11 = valid11 || _valid5;
      const _errs41 = errors;
      if (!(typeof data9 == "number" && (!(data9 % 1) && !isNaN(data9)))) {
        const err19 = { instancePath: instancePath + "/layer", schemaPath: "#/$defs/LayerSelector/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
      var _valid5 = _errs41 === errors;
      valid11 = valid11 || _valid5;
      const _errs43 = errors;
      if (data9 !== null) {
        const err20 = { instancePath: instancePath + "/layer", schemaPath: "#/$defs/LayerSelector/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      var _valid5 = _errs43 === errors;
      valid11 = valid11 || _valid5;
      if (!valid11) {
        const err21 = { instancePath: instancePath + "/layer", schemaPath: "#/$defs/LayerSelector/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
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
    if (data.thickness_mm !== void 0) {
      let data10 = data.thickness_mm;
      if (typeof data10 == "number") {
        if (data10 <= 0 || isNaN(data10)) {
          const err22 = { instancePath: instancePath + "/thickness_mm", schemaPath: "#/properties/thickness_mm/exclusiveMinimum", keyword: "exclusiveMinimum", params: { comparison: ">", limit: 0 }, message: "must be > 0" };
          if (vErrors === null) {
            vErrors = [err22];
          } else {
            vErrors.push(err22);
          }
          errors++;
        }
      } else {
        const err23 = { instancePath: instancePath + "/thickness_mm", schemaPath: "#/properties/thickness_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
    }
    if (data.z_mm !== void 0) {
      if (!(typeof data.z_mm == "number")) {
        const err24 = { instancePath: instancePath + "/z_mm", schemaPath: "#/properties/z_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
    }
    if (data.copper_color !== void 0) {
      let data12 = data.copper_color;
      if (typeof data12 === "string") {
        if (func1(data12) < 1) {
          const err25 = { instancePath: instancePath + "/copper_color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err25];
          } else {
            vErrors.push(err25);
          }
          errors++;
        }
      } else {
        const err26 = { instancePath: instancePath + "/copper_color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
    }
    if (data.outline_width_mm !== void 0) {
      let data13 = data.outline_width_mm;
      if (typeof data13 == "number") {
        if (data13 < 0 || isNaN(data13)) {
          const err27 = { instancePath: instancePath + "/outline_width_mm", schemaPath: "#/properties/outline_width_mm/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err27];
          } else {
            vErrors.push(err27);
          }
          errors++;
        }
      } else {
        const err28 = { instancePath: instancePath + "/outline_width_mm", schemaPath: "#/properties/outline_width_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
    }
    if (data.outline_color !== void 0) {
      let data14 = data.outline_color;
      if (typeof data14 === "string") {
        if (func1(data14) < 1) {
          const err29 = { instancePath: instancePath + "/outline_color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err29];
          } else {
            vErrors.push(err29);
          }
          errors++;
        }
      } else {
        const err30 = { instancePath: instancePath + "/outline_color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
        }
        errors++;
      }
    }
    if (data.board_cutout_color !== void 0) {
      let data15 = data.board_cutout_color;
      if (typeof data15 === "string") {
        if (func1(data15) < 1) {
          const err31 = { instancePath: instancePath + "/board_cutout_color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err31];
          } else {
            vErrors.push(err31);
          }
          errors++;
        }
      } else {
        const err32 = { instancePath: instancePath + "/board_cutout_color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
        }
        errors++;
      }
    }
    if (data.include_board_cutouts !== void 0) {
      if (typeof data.include_board_cutouts !== "boolean") {
        const err33 = { instancePath: instancePath + "/include_board_cutouts", schemaPath: "#/properties/include_board_cutouts/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
    }
    if (data.include_copper !== void 0) {
      if (typeof data.include_copper !== "boolean") {
        const err34 = { instancePath: instancePath + "/include_copper", schemaPath: "#/properties/include_copper/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
        }
        errors++;
      }
    }
    if (data.include_board_outline !== void 0) {
      if (typeof data.include_board_outline !== "boolean") {
        const err35 = { instancePath: instancePath + "/include_board_outline", schemaPath: "#/properties/include_board_outline/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err35];
        } else {
          vErrors.push(err35);
        }
        errors++;
      }
    }
    if (data.include_poured_polygons !== void 0) {
      if (typeof data.include_poured_polygons !== "boolean") {
        const err36 = { instancePath: instancePath + "/include_poured_polygons", schemaPath: "#/properties/include_poured_polygons/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err36];
        } else {
          vErrors.push(err36);
        }
        errors++;
      }
    }
    if (data.cut_holes !== void 0) {
      if (typeof data.cut_holes !== "boolean") {
        const err37 = { instancePath: instancePath + "/cut_holes", schemaPath: "#/properties/cut_holes/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err37];
        } else {
          vErrors.push(err37);
        }
        errors++;
      }
    }
    if (data.drill_hole_mode !== void 0) {
      let data21 = data.drill_hole_mode;
      const _errs72 = errors;
      let valid16 = false;
      const _errs73 = errors;
      if (typeof data21 !== "string") {
        const err38 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err38];
        } else {
          vErrors.push(err38);
        }
        errors++;
      }
      if ("auto" !== data21) {
        const err39 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf/0/const", keyword: "const", params: { allowedValue: "auto" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err39];
        } else {
          vErrors.push(err39);
        }
        errors++;
      }
      var _valid6 = _errs73 === errors;
      valid16 = valid16 || _valid6;
      const _errs75 = errors;
      if (typeof data21 !== "string") {
        const err40 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err40];
        } else {
          vErrors.push(err40);
        }
        errors++;
      }
      if ("cut" !== data21) {
        const err41 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf/1/const", keyword: "const", params: { allowedValue: "cut" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err41];
        } else {
          vErrors.push(err41);
        }
        errors++;
      }
      var _valid6 = _errs75 === errors;
      valid16 = valid16 || _valid6;
      const _errs77 = errors;
      if (typeof data21 !== "string") {
        const err42 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err42];
        } else {
          vErrors.push(err42);
        }
        errors++;
      }
      if ("overlay" !== data21) {
        const err43 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf/2/const", keyword: "const", params: { allowedValue: "overlay" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err43];
        } else {
          vErrors.push(err43);
        }
        errors++;
      }
      var _valid6 = _errs77 === errors;
      valid16 = valid16 || _valid6;
      const _errs79 = errors;
      if (typeof data21 !== "string") {
        const err44 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err44];
        } else {
          vErrors.push(err44);
        }
        errors++;
      }
      if ("none" !== data21) {
        const err45 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf/3/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err45];
        } else {
          vErrors.push(err45);
        }
        errors++;
      }
      var _valid6 = _errs79 === errors;
      valid16 = valid16 || _valid6;
      if (!valid16) {
        const err46 = { instancePath: instancePath + "/drill_hole_mode", schemaPath: "#/$defs/DrillMode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err46];
        } else {
          vErrors.push(err46);
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
    if (data.max_boolean_drill_cuts !== void 0) {
      let data22 = data.max_boolean_drill_cuts;
      if (!(typeof data22 == "number" && (!(data22 % 1) && !isNaN(data22)))) {
        const err47 = { instancePath: instancePath + "/max_boolean_drill_cuts", schemaPath: "#/properties/max_boolean_drill_cuts/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err47];
        } else {
          vErrors.push(err47);
        }
        errors++;
      }
      if (typeof data22 == "number") {
        if (data22 < 0 || isNaN(data22)) {
          const err48 = { instancePath: instancePath + "/max_boolean_drill_cuts", schemaPath: "#/properties/max_boolean_drill_cuts/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err48];
          } else {
            vErrors.push(err48);
          }
          errors++;
        }
      }
    }
    if (data.drill_hole_color !== void 0) {
      let data23 = data.drill_hole_color;
      if (typeof data23 === "string") {
        if (func1(data23) < 1) {
          const err49 = { instancePath: instancePath + "/drill_hole_color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err49];
          } else {
            vErrors.push(err49);
          }
          errors++;
        }
      } else {
        const err50 = { instancePath: instancePath + "/drill_hole_color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err50];
        } else {
          vErrors.push(err50);
        }
        errors++;
      }
    }
    if (data.drill_plated_hole_color !== void 0) {
      let data24 = data.drill_plated_hole_color;
      if (typeof data24 === "string") {
        if (func1(data24) < 1) {
          const err51 = { instancePath: instancePath + "/drill_plated_hole_color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err51];
          } else {
            vErrors.push(err51);
          }
          errors++;
        }
      } else {
        const err52 = { instancePath: instancePath + "/drill_plated_hole_color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err52];
        } else {
          vErrors.push(err52);
        }
        errors++;
      }
    }
    if (data.drill_non_plated_hole_color !== void 0) {
      let data25 = data.drill_non_plated_hole_color;
      if (typeof data25 === "string") {
        if (func1(data25) < 1) {
          const err53 = { instancePath: instancePath + "/drill_non_plated_hole_color", schemaPath: "#/$defs/Color/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err53];
          } else {
            vErrors.push(err53);
          }
          errors++;
        }
      } else {
        const err54 = { instancePath: instancePath + "/drill_non_plated_hole_color", schemaPath: "#/$defs/Color/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err54];
        } else {
          vErrors.push(err54);
        }
        errors++;
      }
    }
    if (data.drill_overlay_thickness_mm !== void 0) {
      let data26 = data.drill_overlay_thickness_mm;
      if (typeof data26 == "number") {
        if (data26 < 0 || isNaN(data26)) {
          const err55 = { instancePath: instancePath + "/drill_overlay_thickness_mm", schemaPath: "#/properties/drill_overlay_thickness_mm/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err55];
          } else {
            vErrors.push(err55);
          }
          errors++;
        }
      } else {
        const err56 = { instancePath: instancePath + "/drill_overlay_thickness_mm", schemaPath: "#/properties/drill_overlay_thickness_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err56];
        } else {
          vErrors.push(err56);
        }
        errors++;
      }
    }
    if (data.drill_minimum_diameter_mm !== void 0) {
      let data27 = data.drill_minimum_diameter_mm;
      if (typeof data27 == "number") {
        if (data27 < 0 || isNaN(data27)) {
          const err57 = { instancePath: instancePath + "/drill_minimum_diameter_mm", schemaPath: "#/properties/drill_minimum_diameter_mm/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err57];
          } else {
            vErrors.push(err57);
          }
          errors++;
        }
      } else {
        const err58 = { instancePath: instancePath + "/drill_minimum_diameter_mm", schemaPath: "#/properties/drill_minimum_diameter_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err58];
        } else {
          vErrors.push(err58);
        }
        errors++;
      }
    }
    if (data.drill_hole_shape !== void 0) {
      let data28 = data.drill_hole_shape;
      const _errs98 = errors;
      let valid21 = false;
      const _errs99 = errors;
      if (typeof data28 !== "string") {
        const err59 = { instancePath: instancePath + "/drill_hole_shape", schemaPath: "#/$defs/DrillShape/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err59];
        } else {
          vErrors.push(err59);
        }
        errors++;
      }
      if ("solid" !== data28) {
        const err60 = { instancePath: instancePath + "/drill_hole_shape", schemaPath: "#/$defs/DrillShape/anyOf/0/const", keyword: "const", params: { allowedValue: "solid" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err60];
        } else {
          vErrors.push(err60);
        }
        errors++;
      }
      var _valid7 = _errs99 === errors;
      valid21 = valid21 || _valid7;
      const _errs101 = errors;
      if (typeof data28 !== "string") {
        const err61 = { instancePath: instancePath + "/drill_hole_shape", schemaPath: "#/$defs/DrillShape/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err61];
        } else {
          vErrors.push(err61);
        }
        errors++;
      }
      if ("ring" !== data28) {
        const err62 = { instancePath: instancePath + "/drill_hole_shape", schemaPath: "#/$defs/DrillShape/anyOf/1/const", keyword: "const", params: { allowedValue: "ring" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err62];
        } else {
          vErrors.push(err62);
        }
        errors++;
      }
      var _valid7 = _errs101 === errors;
      valid21 = valid21 || _valid7;
      if (!valid21) {
        const err63 = { instancePath: instancePath + "/drill_hole_shape", schemaPath: "#/$defs/DrillShape/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err63];
        } else {
          vErrors.push(err63);
        }
        errors++;
      } else {
        errors = _errs98;
        if (vErrors !== null) {
          if (_errs98) {
            vErrors.length = _errs98;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.drill_ring_width_mm !== void 0) {
      let data29 = data.drill_ring_width_mm;
      if (typeof data29 == "number") {
        if (data29 < 0 || isNaN(data29)) {
          const err64 = { instancePath: instancePath + "/drill_ring_width_mm", schemaPath: "#/properties/drill_ring_width_mm/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err64];
          } else {
            vErrors.push(err64);
          }
          errors++;
        }
      } else {
        const err65 = { instancePath: instancePath + "/drill_ring_width_mm", schemaPath: "#/properties/drill_ring_width_mm/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err65];
        } else {
          vErrors.push(err65);
        }
        errors++;
      }
    }
    if (data.drill_plated_ring_shape !== void 0) {
      let data30 = data.drill_plated_ring_shape;
      const _errs107 = errors;
      let valid23 = false;
      const _errs108 = errors;
      if (typeof data30 !== "string") {
        const err66 = { instancePath: instancePath + "/drill_plated_ring_shape", schemaPath: "#/$defs/PlatedRingShape/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err66];
        } else {
          vErrors.push(err66);
        }
        errors++;
      }
      if ("annulus" !== data30) {
        const err67 = { instancePath: instancePath + "/drill_plated_ring_shape", schemaPath: "#/$defs/PlatedRingShape/anyOf/0/const", keyword: "const", params: { allowedValue: "annulus" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err67];
        } else {
          vErrors.push(err67);
        }
        errors++;
      }
      var _valid8 = _errs108 === errors;
      valid23 = valid23 || _valid8;
      if (!valid23) {
        const err68 = { instancePath: instancePath + "/drill_plated_ring_shape", schemaPath: "#/$defs/PlatedRingShape/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err68];
        } else {
          vErrors.push(err68);
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
    if (data.drill_selected_component_mode !== void 0) {
      let data31 = data.drill_selected_component_mode;
      const _errs112 = errors;
      let valid25 = false;
      const _errs113 = errors;
      if (typeof data31 !== "string") {
        const err69 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err69];
        } else {
          vErrors.push(err69);
        }
        errors++;
      }
      if ("inherit" !== data31) {
        const err70 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/const", keyword: "const", params: { allowedValue: "inherit" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err70];
        } else {
          vErrors.push(err70);
        }
        errors++;
      }
      var _valid9 = _errs113 === errors;
      valid25 = valid25 || _valid9;
      const _errs115 = errors;
      if (typeof data31 !== "string") {
        const err71 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err71];
        } else {
          vErrors.push(err71);
        }
        errors++;
      }
      if ("cut" !== data31) {
        const err72 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/const", keyword: "const", params: { allowedValue: "cut" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err72];
        } else {
          vErrors.push(err72);
        }
        errors++;
      }
      var _valid9 = _errs115 === errors;
      valid25 = valid25 || _valid9;
      const _errs117 = errors;
      if (typeof data31 !== "string") {
        const err73 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err73];
        } else {
          vErrors.push(err73);
        }
        errors++;
      }
      if ("overlay" !== data31) {
        const err74 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/const", keyword: "const", params: { allowedValue: "overlay" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err74];
        } else {
          vErrors.push(err74);
        }
        errors++;
      }
      var _valid9 = _errs117 === errors;
      valid25 = valid25 || _valid9;
      const _errs119 = errors;
      if (typeof data31 !== "string") {
        const err75 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err75];
        } else {
          vErrors.push(err75);
        }
        errors++;
      }
      if ("none" !== data31) {
        const err76 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err76];
        } else {
          vErrors.push(err76);
        }
        errors++;
      }
      var _valid9 = _errs119 === errors;
      valid25 = valid25 || _valid9;
      if (!valid25) {
        const err77 = { instancePath: instancePath + "/drill_selected_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err77];
        } else {
          vErrors.push(err77);
        }
        errors++;
      } else {
        errors = _errs112;
        if (vErrors !== null) {
          if (_errs112) {
            vErrors.length = _errs112;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.drill_other_component_mode !== void 0) {
      let data32 = data.drill_other_component_mode;
      const _errs123 = errors;
      let valid27 = false;
      const _errs124 = errors;
      if (typeof data32 !== "string") {
        const err78 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err78];
        } else {
          vErrors.push(err78);
        }
        errors++;
      }
      if ("inherit" !== data32) {
        const err79 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/const", keyword: "const", params: { allowedValue: "inherit" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err79];
        } else {
          vErrors.push(err79);
        }
        errors++;
      }
      var _valid10 = _errs124 === errors;
      valid27 = valid27 || _valid10;
      const _errs126 = errors;
      if (typeof data32 !== "string") {
        const err80 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err80];
        } else {
          vErrors.push(err80);
        }
        errors++;
      }
      if ("cut" !== data32) {
        const err81 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/const", keyword: "const", params: { allowedValue: "cut" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err81];
        } else {
          vErrors.push(err81);
        }
        errors++;
      }
      var _valid10 = _errs126 === errors;
      valid27 = valid27 || _valid10;
      const _errs128 = errors;
      if (typeof data32 !== "string") {
        const err82 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err82];
        } else {
          vErrors.push(err82);
        }
        errors++;
      }
      if ("overlay" !== data32) {
        const err83 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/const", keyword: "const", params: { allowedValue: "overlay" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err83];
        } else {
          vErrors.push(err83);
        }
        errors++;
      }
      var _valid10 = _errs128 === errors;
      valid27 = valid27 || _valid10;
      const _errs130 = errors;
      if (typeof data32 !== "string") {
        const err84 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err84];
        } else {
          vErrors.push(err84);
        }
        errors++;
      }
      if ("none" !== data32) {
        const err85 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err85];
        } else {
          vErrors.push(err85);
        }
        errors++;
      }
      var _valid10 = _errs130 === errors;
      valid27 = valid27 || _valid10;
      if (!valid27) {
        const err86 = { instancePath: instancePath + "/drill_other_component_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err86];
        } else {
          vErrors.push(err86);
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
    if (data.drill_free_pad_mode !== void 0) {
      let data33 = data.drill_free_pad_mode;
      const _errs134 = errors;
      let valid29 = false;
      const _errs135 = errors;
      if (typeof data33 !== "string") {
        const err87 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err87];
        } else {
          vErrors.push(err87);
        }
        errors++;
      }
      if ("inherit" !== data33) {
        const err88 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/const", keyword: "const", params: { allowedValue: "inherit" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err88];
        } else {
          vErrors.push(err88);
        }
        errors++;
      }
      var _valid11 = _errs135 === errors;
      valid29 = valid29 || _valid11;
      const _errs137 = errors;
      if (typeof data33 !== "string") {
        const err89 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err89];
        } else {
          vErrors.push(err89);
        }
        errors++;
      }
      if ("cut" !== data33) {
        const err90 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/const", keyword: "const", params: { allowedValue: "cut" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err90];
        } else {
          vErrors.push(err90);
        }
        errors++;
      }
      var _valid11 = _errs137 === errors;
      valid29 = valid29 || _valid11;
      const _errs139 = errors;
      if (typeof data33 !== "string") {
        const err91 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err91];
        } else {
          vErrors.push(err91);
        }
        errors++;
      }
      if ("overlay" !== data33) {
        const err92 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/const", keyword: "const", params: { allowedValue: "overlay" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err92];
        } else {
          vErrors.push(err92);
        }
        errors++;
      }
      var _valid11 = _errs139 === errors;
      valid29 = valid29 || _valid11;
      const _errs141 = errors;
      if (typeof data33 !== "string") {
        const err93 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err93];
        } else {
          vErrors.push(err93);
        }
        errors++;
      }
      if ("none" !== data33) {
        const err94 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err94];
        } else {
          vErrors.push(err94);
        }
        errors++;
      }
      var _valid11 = _errs141 === errors;
      valid29 = valid29 || _valid11;
      if (!valid29) {
        const err95 = { instancePath: instancePath + "/drill_free_pad_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err95];
        } else {
          vErrors.push(err95);
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
    if (data.drill_via_mode !== void 0) {
      let data34 = data.drill_via_mode;
      const _errs145 = errors;
      let valid31 = false;
      const _errs146 = errors;
      if (typeof data34 !== "string") {
        const err96 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err96];
        } else {
          vErrors.push(err96);
        }
        errors++;
      }
      if ("inherit" !== data34) {
        const err97 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/0/const", keyword: "const", params: { allowedValue: "inherit" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err97];
        } else {
          vErrors.push(err97);
        }
        errors++;
      }
      var _valid12 = _errs146 === errors;
      valid31 = valid31 || _valid12;
      const _errs148 = errors;
      if (typeof data34 !== "string") {
        const err98 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err98];
        } else {
          vErrors.push(err98);
        }
        errors++;
      }
      if ("cut" !== data34) {
        const err99 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/1/const", keyword: "const", params: { allowedValue: "cut" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err99];
        } else {
          vErrors.push(err99);
        }
        errors++;
      }
      var _valid12 = _errs148 === errors;
      valid31 = valid31 || _valid12;
      const _errs150 = errors;
      if (typeof data34 !== "string") {
        const err100 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err100];
        } else {
          vErrors.push(err100);
        }
        errors++;
      }
      if ("overlay" !== data34) {
        const err101 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/2/const", keyword: "const", params: { allowedValue: "overlay" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err101];
        } else {
          vErrors.push(err101);
        }
        errors++;
      }
      var _valid12 = _errs150 === errors;
      valid31 = valid31 || _valid12;
      const _errs152 = errors;
      if (typeof data34 !== "string") {
        const err102 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err102];
        } else {
          vErrors.push(err102);
        }
        errors++;
      }
      if ("none" !== data34) {
        const err103 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf/3/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err103];
        } else {
          vErrors.push(err103);
        }
        errors++;
      }
      var _valid12 = _errs152 === errors;
      valid31 = valid31 || _valid12;
      if (!valid31) {
        const err104 = { instancePath: instancePath + "/drill_via_mode", schemaPath: "#/$defs/DrillScopedMode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err104];
        } else {
          vErrors.push(err104);
        }
        errors++;
      } else {
        errors = _errs145;
        if (vErrors !== null) {
          if (_errs145) {
            vErrors.length = _errs145;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.fuse_copper !== void 0) {
      if (typeof data.fuse_copper !== "boolean") {
        const err105 = { instancePath: instancePath + "/fuse_copper", schemaPath: "#/properties/fuse_copper/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err105];
        } else {
          vErrors.push(err105);
        }
        errors++;
      }
    }
    if (data.fuse_board_outline !== void 0) {
      if (typeof data.fuse_board_outline !== "boolean") {
        const err106 = { instancePath: instancePath + "/fuse_board_outline", schemaPath: "#/properties/fuse_board_outline/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err106];
        } else {
          vErrors.push(err106);
        }
        errors++;
      }
    }
    if (data.arc_segments !== void 0) {
      let data37 = data.arc_segments;
      if (!(typeof data37 == "number" && (!(data37 % 1) && !isNaN(data37)))) {
        const err107 = { instancePath: instancePath + "/arc_segments", schemaPath: "#/properties/arc_segments/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err107];
        } else {
          vErrors.push(err107);
        }
        errors++;
      }
      if (typeof data37 == "number") {
        if (data37 < 1 || isNaN(data37)) {
          const err108 = { instancePath: instancePath + "/arc_segments", schemaPath: "#/properties/arc_segments/minimum", keyword: "minimum", params: { comparison: ">=", limit: 1 }, message: "must be >= 1" };
          if (vErrors === null) {
            vErrors = [err108];
          } else {
            vErrors.push(err108);
          }
          errors++;
        }
      }
    }
    if (data.include_tracks !== void 0) {
      if (typeof data.include_tracks !== "boolean") {
        const err109 = { instancePath: instancePath + "/include_tracks", schemaPath: "#/properties/include_tracks/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err109];
        } else {
          vErrors.push(err109);
        }
        errors++;
      }
    }
    if (data.include_arcs !== void 0) {
      if (typeof data.include_arcs !== "boolean") {
        const err110 = { instancePath: instancePath + "/include_arcs", schemaPath: "#/properties/include_arcs/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err110];
        } else {
          vErrors.push(err110);
        }
        errors++;
      }
    }
    if (data.include_fills !== void 0) {
      if (typeof data.include_fills !== "boolean") {
        const err111 = { instancePath: instancePath + "/include_fills", schemaPath: "#/properties/include_fills/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err111];
        } else {
          vErrors.push(err111);
        }
        errors++;
      }
    }
    if (data.include_regions !== void 0) {
      if (typeof data.include_regions !== "boolean") {
        const err112 = { instancePath: instancePath + "/include_regions", schemaPath: "#/properties/include_regions/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err112];
        } else {
          vErrors.push(err112);
        }
        errors++;
      }
    }
    if (data.include_vias !== void 0) {
      if (typeof data.include_vias !== "boolean") {
        const err113 = { instancePath: instancePath + "/include_vias", schemaPath: "#/properties/include_vias/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err113];
        } else {
          vErrors.push(err113);
        }
        errors++;
      }
    }
    if (data.include_component_pads !== void 0) {
      if (typeof data.include_component_pads !== "boolean") {
        const err114 = { instancePath: instancePath + "/include_component_pads", schemaPath: "#/properties/include_component_pads/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err114];
        } else {
          vErrors.push(err114);
        }
        errors++;
      }
    }
    if (data.include_free_pads !== void 0) {
      if (typeof data.include_free_pads !== "boolean") {
        const err115 = { instancePath: instancePath + "/include_free_pads", schemaPath: "#/properties/include_free_pads/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err115];
        } else {
          vErrors.push(err115);
        }
        errors++;
      }
    }
    if (data.include_designators !== void 0) {
      let data45 = data.include_designators;
      const _errs176 = errors;
      let valid33 = false;
      let passing0 = null;
      const _errs177 = errors;
      if (typeof data45 !== "string") {
        const err116 = { instancePath: instancePath + "/include_designators", schemaPath: "#/$defs/StringList/oneOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err116];
        } else {
          vErrors.push(err116);
        }
        errors++;
      }
      var _valid13 = _errs177 === errors;
      if (_valid13) {
        valid33 = true;
        passing0 = 0;
      }
      const _errs179 = errors;
      if (Array.isArray(data45)) {
        const len1 = data45.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (typeof data45[i1] !== "string") {
            const err117 = { instancePath: instancePath + "/include_designators/" + i1, schemaPath: "#/$defs/StringList/oneOf/1/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err117];
            } else {
              vErrors.push(err117);
            }
            errors++;
          }
        }
      } else {
        const err118 = { instancePath: instancePath + "/include_designators", schemaPath: "#/$defs/StringList/oneOf/1/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err118];
        } else {
          vErrors.push(err118);
        }
        errors++;
      }
      var _valid13 = _errs179 === errors;
      if (_valid13 && valid33) {
        valid33 = false;
        passing0 = [passing0, 1];
      } else {
        if (_valid13) {
          valid33 = true;
          passing0 = 1;
        }
      }
      if (!valid33) {
        const err119 = { instancePath: instancePath + "/include_designators", schemaPath: "#/$defs/StringList/oneOf", keyword: "oneOf", params: { passingSchemas: passing0 }, message: "must match exactly one schema in oneOf" };
        if (vErrors === null) {
          vErrors = [err119];
        } else {
          vErrors.push(err119);
        }
        errors++;
      } else {
        errors = _errs176;
        if (vErrors !== null) {
          if (_errs176) {
            vErrors.length = _errs176;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.board_outline !== void 0) {
      if (!validate22(data.board_outline, { instancePath: instancePath + "/board_outline", parentData: data, parentDataProperty: "board_outline", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate22.errors : vErrors.concat(validate22.errors);
        errors = vErrors.length;
      }
    }
    if (data.features !== void 0) {
      if (!validate24(data.features, { instancePath: instancePath + "/features", parentData: data, parentDataProperty: "features", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate24.errors : vErrors.concat(validate24.errors);
        errors = vErrors.length;
      }
    }
    if (data.drills !== void 0) {
      if (!validate49(data.drills, { instancePath: instancePath + "/drills", parentData: data, parentDataProperty: "drills", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate49.errors : vErrors.concat(validate49.errors);
        errors = vErrors.length;
      }
    }
    if (props0 !== true) {
      for (const key0 in data) {
        if (!props0 || !props0[key0]) {
          const err120 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
          if (vErrors === null) {
            vErrors = [err120];
          } else {
            vErrors.push(err120);
          }
          errors++;
        }
      }
    }
  } else {
    const err121 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err121];
    } else {
      vErrors.push(err121);
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
