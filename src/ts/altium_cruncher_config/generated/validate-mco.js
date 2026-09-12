// Generated from src/tsp/altium_cruncher/mco/main.tsp. Do not edit.
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
    if (data.source === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "source" }, message: "must have required property 'source'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.destination === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "destination" }, message: "must have required property 'destination'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.source !== void 0) {
      let data0 = data.source;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err3 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.destination !== void 0) {
      let data1 = data.destination;
      if (typeof data1 === "string") {
        if (func1(data1) < 1) {
          const err5 = { instancePath: instancePath + "/destination", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err5];
          } else {
            vErrors.push(err5);
          }
          errors++;
        }
      } else {
        const err6 = { instancePath: instancePath + "/destination", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.overwrite !== void 0) {
      let data2 = data.overwrite;
      const _errs12 = errors;
      let valid5 = false;
      const _errs13 = errors;
      if (typeof data2 !== "boolean") {
        const err7 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
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
        const err8 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err9 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
  } else {
    const err10 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err10];
    } else {
      vErrors.push(err10);
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("file.copy" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "file.copy" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate24(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate24.errors : vErrors.concat(validate24.errors);
        errors = vErrors.length;
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
  validate23.errors = vErrors;
  return errors === 0;
}
validate23.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.message !== void 0) {
      let data0 = data.message;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err1 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err2 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err3 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
  } else {
    const err4 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err4];
    } else {
      vErrors.push(err4);
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err2 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err5 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err8 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      const _errs24 = errors;
      let valid6 = false;
      const _errs25 = errors;
      if (typeof data3 !== "string") {
        const err11 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      if ("mco.fail" !== data3) {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/anyOf/0/const", keyword: "const", params: { allowedValue: "mco.fail" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid3 = _errs25 === errors;
      valid6 = valid6 || _valid3;
      const _errs27 = errors;
      if (typeof data3 !== "string") {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      if ("fail" !== data3) {
        const err14 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/anyOf/1/const", keyword: "const", params: { allowedValue: "fail" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid3 = _errs27 === errors;
      valid6 = valid6 || _valid3;
      if (!valid6) {
        const err15 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
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
    if (data.args !== void 0) {
      if (!validate28(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate28.errors : vErrors.concat(validate28.errors);
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
  validate27.errors = vErrors;
  return errors === 0;
}
validate27.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
  } else {
    const err4 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err4];
    } else {
      vErrors.push(err4);
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err2 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err5 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err8 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      const _errs24 = errors;
      let valid6 = false;
      const _errs25 = errors;
      if (typeof data3 !== "string") {
        const err11 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      if ("mco.message" !== data3) {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/anyOf/0/const", keyword: "const", params: { allowedValue: "mco.message" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid3 = _errs25 === errors;
      valid6 = valid6 || _valid3;
      const _errs27 = errors;
      if (typeof data3 !== "string") {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      if ("message" !== data3) {
        const err14 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/anyOf/1/const", keyword: "const", params: { allowedValue: "message" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid3 = _errs27 === errors;
      valid6 = valid6 || _valid3;
      if (!valid6) {
        const err15 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
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
    if (data.args !== void 0) {
      if (!validate32(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate32.errors : vErrors.concat(validate32.errors);
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.center_mils === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "center_mils" }, message: "must have required property 'center_mils'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.radius_mils === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "radius_mils" }, message: "must have required property 'radius_mils'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.start_angle_degrees === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "start_angle_degrees" }, message: "must have required property 'start_angle_degrees'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.end_angle_degrees === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "end_angle_degrees" }, message: "must have required property 'end_angle_degrees'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.width_mils === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "width_mils" }, message: "must have required property 'width_mils'" };
      if (vErrors === null) {
        vErrors = [err6];
      } else {
        vErrors.push(err6);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err7 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err7];
          } else {
            vErrors.push(err7);
          }
          errors++;
        }
      } else {
        const err8 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
    if (data.output_file !== void 0) {
      let data1 = data.output_file;
      const _errs9 = errors;
      let valid4 = false;
      const _errs10 = errors;
      if (typeof data1 !== "string") {
        const err9 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      valid4 = valid4 || _valid0;
      const _errs12 = errors;
      if (data1 !== null) {
        const err10 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid0 = _errs12 === errors;
      valid4 = valid4 || _valid0;
      if (!valid4) {
        const err11 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.overwrite !== void 0) {
      let data2 = data.overwrite;
      const _errs15 = errors;
      let valid5 = false;
      const _errs16 = errors;
      if (typeof data2 !== "boolean") {
        const err12 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid1 = _errs16 === errors;
      valid5 = valid5 || _valid1;
      const _errs18 = errors;
      if (data2 !== null) {
        const err13 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid1 = _errs18 === errors;
      valid5 = valid5 || _valid1;
      if (!valid5) {
        const err14 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
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
    if (data.center_mils !== void 0) {
      let data3 = data.center_mils;
      if (Array.isArray(data3)) {
        if (data3.length > 2) {
          const err15 = { instancePath: instancePath + "/center_mils", schemaPath: "#/$defs/PointMils/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err15];
          } else {
            vErrors.push(err15);
          }
          errors++;
        }
        if (data3.length < 2) {
          const err16 = { instancePath: instancePath + "/center_mils", schemaPath: "#/$defs/PointMils/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err16];
          } else {
            vErrors.push(err16);
          }
          errors++;
        }
        const len0 = data3.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!(typeof data3[i0] == "number")) {
            const err17 = { instancePath: instancePath + "/center_mils/" + i0, schemaPath: "#/$defs/PointMils/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err17];
            } else {
              vErrors.push(err17);
            }
            errors++;
          }
        }
      } else {
        const err18 = { instancePath: instancePath + "/center_mils", schemaPath: "#/$defs/PointMils/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
    }
    if (data.radius_mils !== void 0) {
      if (!(typeof data.radius_mils == "number")) {
        const err19 = { instancePath: instancePath + "/radius_mils", schemaPath: "#/properties/radius_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
    }
    if (data.start_angle_degrees !== void 0) {
      if (!(typeof data.start_angle_degrees == "number")) {
        const err20 = { instancePath: instancePath + "/start_angle_degrees", schemaPath: "#/properties/start_angle_degrees/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
    }
    if (data.end_angle_degrees !== void 0) {
      if (!(typeof data.end_angle_degrees == "number")) {
        const err21 = { instancePath: instancePath + "/end_angle_degrees", schemaPath: "#/properties/end_angle_degrees/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
    }
    if (data.width_mils !== void 0) {
      if (!(typeof data.width_mils == "number")) {
        const err22 = { instancePath: instancePath + "/width_mils", schemaPath: "#/properties/width_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
    }
    if (data.layer !== void 0) {
      let data9 = data.layer;
      const _errs34 = errors;
      let valid9 = false;
      const _errs35 = errors;
      if (typeof data9 !== "string") {
        const err23 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      var _valid2 = _errs35 === errors;
      valid9 = valid9 || _valid2;
      const _errs37 = errors;
      if (!(typeof data9 == "number" && (!(data9 % 1) && !isNaN(data9)))) {
        const err24 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      var _valid2 = _errs37 === errors;
      valid9 = valid9 || _valid2;
      const _errs39 = errors;
      if (data9 !== null) {
        const err25 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
      var _valid2 = _errs39 === errors;
      valid9 = valid9 || _valid2;
      if (!valid9) {
        const err26 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.net !== void 0) {
      let data10 = data.net;
      const _errs42 = errors;
      let valid10 = false;
      const _errs43 = errors;
      if (typeof data10 !== "string") {
        const err27 = { instancePath: instancePath + "/net", schemaPath: "#/properties/net/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
      var _valid3 = _errs43 === errors;
      valid10 = valid10 || _valid3;
      const _errs45 = errors;
      if (data10 !== null) {
        const err28 = { instancePath: instancePath + "/net", schemaPath: "#/properties/net/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
      var _valid3 = _errs45 === errors;
      valid10 = valid10 || _valid3;
      if (!valid10) {
        const err29 = { instancePath: instancePath + "/net", schemaPath: "#/properties/net/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
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
  } else {
    const err30 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err30];
    } else {
      vErrors.push(err30);
    }
    errors++;
  }
  validate36.errors = vErrors;
  return errors === 0;
}
validate36.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("pcbdoc.add_arc" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "pcbdoc.add_arc" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate36(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate36.errors : vErrors.concat(validate36.errors);
        errors = vErrors.length;
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
  validate35.errors = vErrors;
  return errors === 0;
}
validate35.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.library === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "library" }, message: "must have required property 'library'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.footprint === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "footprint" }, message: "must have required property 'footprint'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.designator === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "designator" }, message: "must have required property 'designator'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.position_mils === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "position_mils" }, message: "must have required property 'position_mils'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err6 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err6];
          } else {
            vErrors.push(err6);
          }
          errors++;
        }
      } else {
        const err7 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.output_file !== void 0) {
      let data1 = data.output_file;
      const _errs9 = errors;
      let valid4 = false;
      const _errs10 = errors;
      if (typeof data1 !== "string") {
        const err8 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      valid4 = valid4 || _valid0;
      const _errs12 = errors;
      if (data1 !== null) {
        const err9 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid0 = _errs12 === errors;
      valid4 = valid4 || _valid0;
      if (!valid4) {
        const err10 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
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
    if (data.overwrite !== void 0) {
      let data2 = data.overwrite;
      const _errs15 = errors;
      let valid5 = false;
      const _errs16 = errors;
      if (typeof data2 !== "boolean") {
        const err11 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid1 = _errs16 === errors;
      valid5 = valid5 || _valid1;
      const _errs18 = errors;
      if (data2 !== null) {
        const err12 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid1 = _errs18 === errors;
      valid5 = valid5 || _valid1;
      if (!valid5) {
        const err13 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
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
    if (data.library !== void 0) {
      let data3 = data.library;
      if (typeof data3 === "string") {
        if (func1(data3) < 1) {
          const err14 = { instancePath: instancePath + "/library", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err14];
          } else {
            vErrors.push(err14);
          }
          errors++;
        }
      } else {
        const err15 = { instancePath: instancePath + "/library", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
    }
    if (data.footprint !== void 0) {
      let data4 = data.footprint;
      if (typeof data4 === "string") {
        if (func1(data4) < 1) {
          const err16 = { instancePath: instancePath + "/footprint", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err16];
          } else {
            vErrors.push(err16);
          }
          errors++;
        }
      } else {
        const err17 = { instancePath: instancePath + "/footprint", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
    }
    if (data.designator !== void 0) {
      let data5 = data.designator;
      if (typeof data5 === "string") {
        if (func1(data5) < 1) {
          const err18 = { instancePath: instancePath + "/designator", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err18];
          } else {
            vErrors.push(err18);
          }
          errors++;
        }
      } else {
        const err19 = { instancePath: instancePath + "/designator", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
    }
    if (data.position_mils !== void 0) {
      let data6 = data.position_mils;
      if (Array.isArray(data6)) {
        if (data6.length > 2) {
          const err20 = { instancePath: instancePath + "/position_mils", schemaPath: "#/$defs/PointMils/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err20];
          } else {
            vErrors.push(err20);
          }
          errors++;
        }
        if (data6.length < 2) {
          const err21 = { instancePath: instancePath + "/position_mils", schemaPath: "#/$defs/PointMils/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err21];
          } else {
            vErrors.push(err21);
          }
          errors++;
        }
        const len0 = data6.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!(typeof data6[i0] == "number")) {
            const err22 = { instancePath: instancePath + "/position_mils/" + i0, schemaPath: "#/$defs/PointMils/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err22];
            } else {
              vErrors.push(err22);
            }
            errors++;
          }
        }
      } else {
        const err23 = { instancePath: instancePath + "/position_mils", schemaPath: "#/$defs/PointMils/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
    }
    if (data.layer !== void 0) {
      let data8 = data.layer;
      const _errs35 = errors;
      let valid12 = false;
      const _errs36 = errors;
      if (typeof data8 !== "string") {
        const err24 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      var _valid2 = _errs36 === errors;
      valid12 = valid12 || _valid2;
      const _errs38 = errors;
      if (!(typeof data8 == "number" && (!(data8 % 1) && !isNaN(data8)))) {
        const err25 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
      var _valid2 = _errs38 === errors;
      valid12 = valid12 || _valid2;
      const _errs40 = errors;
      if (data8 !== null) {
        const err26 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
      var _valid2 = _errs40 === errors;
      valid12 = valid12 || _valid2;
      if (!valid12) {
        const err27 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
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
    if (data.source_unique_id !== void 0) {
      let data9 = data.source_unique_id;
      const _errs43 = errors;
      let valid13 = false;
      const _errs44 = errors;
      if (typeof data9 !== "string") {
        const err28 = { instancePath: instancePath + "/source_unique_id", schemaPath: "#/properties/source_unique_id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
      var _valid3 = _errs44 === errors;
      valid13 = valid13 || _valid3;
      const _errs46 = errors;
      if (data9 !== null) {
        const err29 = { instancePath: instancePath + "/source_unique_id", schemaPath: "#/properties/source_unique_id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      }
      var _valid3 = _errs46 === errors;
      valid13 = valid13 || _valid3;
      if (!valid13) {
        const err30 = { instancePath: instancePath + "/source_unique_id", schemaPath: "#/properties/source_unique_id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
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
    }
    if (data.source_hierarchical_path !== void 0) {
      let data10 = data.source_hierarchical_path;
      const _errs49 = errors;
      let valid14 = false;
      const _errs50 = errors;
      if (typeof data10 !== "string") {
        const err31 = { instancePath: instancePath + "/source_hierarchical_path", schemaPath: "#/properties/source_hierarchical_path/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      }
      var _valid4 = _errs50 === errors;
      valid14 = valid14 || _valid4;
      const _errs52 = errors;
      if (data10 !== null) {
        const err32 = { instancePath: instancePath + "/source_hierarchical_path", schemaPath: "#/properties/source_hierarchical_path/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
        }
        errors++;
      }
      var _valid4 = _errs52 === errors;
      valid14 = valid14 || _valid4;
      if (!valid14) {
        const err33 = { instancePath: instancePath + "/source_hierarchical_path", schemaPath: "#/properties/source_hierarchical_path/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      } else {
        errors = _errs49;
        if (vErrors !== null) {
          if (_errs49) {
            vErrors.length = _errs49;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.source_component_library !== void 0) {
      let data11 = data.source_component_library;
      const _errs55 = errors;
      let valid15 = false;
      const _errs56 = errors;
      if (typeof data11 !== "string") {
        const err34 = { instancePath: instancePath + "/source_component_library", schemaPath: "#/properties/source_component_library/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
        }
        errors++;
      }
      var _valid5 = _errs56 === errors;
      valid15 = valid15 || _valid5;
      const _errs58 = errors;
      if (data11 !== null) {
        const err35 = { instancePath: instancePath + "/source_component_library", schemaPath: "#/properties/source_component_library/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err35];
        } else {
          vErrors.push(err35);
        }
        errors++;
      }
      var _valid5 = _errs58 === errors;
      valid15 = valid15 || _valid5;
      if (!valid15) {
        const err36 = { instancePath: instancePath + "/source_component_library", schemaPath: "#/properties/source_component_library/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err36];
        } else {
          vErrors.push(err36);
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
    if (data.source_lib_reference !== void 0) {
      let data12 = data.source_lib_reference;
      const _errs61 = errors;
      let valid16 = false;
      const _errs62 = errors;
      if (typeof data12 !== "string") {
        const err37 = { instancePath: instancePath + "/source_lib_reference", schemaPath: "#/properties/source_lib_reference/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err37];
        } else {
          vErrors.push(err37);
        }
        errors++;
      }
      var _valid6 = _errs62 === errors;
      valid16 = valid16 || _valid6;
      const _errs64 = errors;
      if (data12 !== null) {
        const err38 = { instancePath: instancePath + "/source_lib_reference", schemaPath: "#/properties/source_lib_reference/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err38];
        } else {
          vErrors.push(err38);
        }
        errors++;
      }
      var _valid6 = _errs64 === errors;
      valid16 = valid16 || _valid6;
      if (!valid16) {
        const err39 = { instancePath: instancePath + "/source_lib_reference", schemaPath: "#/properties/source_lib_reference/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err39];
        } else {
          vErrors.push(err39);
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
    if (data.source_description !== void 0) {
      let data13 = data.source_description;
      const _errs67 = errors;
      let valid17 = false;
      const _errs68 = errors;
      if (typeof data13 !== "string") {
        const err40 = { instancePath: instancePath + "/source_description", schemaPath: "#/properties/source_description/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err40];
        } else {
          vErrors.push(err40);
        }
        errors++;
      }
      var _valid7 = _errs68 === errors;
      valid17 = valid17 || _valid7;
      const _errs70 = errors;
      if (data13 !== null) {
        const err41 = { instancePath: instancePath + "/source_description", schemaPath: "#/properties/source_description/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err41];
        } else {
          vErrors.push(err41);
        }
        errors++;
      }
      var _valid7 = _errs70 === errors;
      valid17 = valid17 || _valid7;
      if (!valid17) {
        const err42 = { instancePath: instancePath + "/source_description", schemaPath: "#/properties/source_description/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err42];
        } else {
          vErrors.push(err42);
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
    if (data.channel_offset !== void 0) {
      let data14 = data.channel_offset;
      const _errs73 = errors;
      let valid18 = false;
      const _errs74 = errors;
      if (!(typeof data14 == "number" && (!(data14 % 1) && !isNaN(data14)))) {
        const err43 = { instancePath: instancePath + "/channel_offset", schemaPath: "#/properties/channel_offset/anyOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err43];
        } else {
          vErrors.push(err43);
        }
        errors++;
      }
      var _valid8 = _errs74 === errors;
      valid18 = valid18 || _valid8;
      const _errs76 = errors;
      if (data14 !== null) {
        const err44 = { instancePath: instancePath + "/channel_offset", schemaPath: "#/properties/channel_offset/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err44];
        } else {
          vErrors.push(err44);
        }
        errors++;
      }
      var _valid8 = _errs76 === errors;
      valid18 = valid18 || _valid8;
      if (!valid18) {
        const err45 = { instancePath: instancePath + "/channel_offset", schemaPath: "#/properties/channel_offset/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err45];
        } else {
          vErrors.push(err45);
        }
        errors++;
      } else {
        errors = _errs73;
        if (vErrors !== null) {
          if (_errs73) {
            vErrors.length = _errs73;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.comment_text !== void 0) {
      let data15 = data.comment_text;
      const _errs79 = errors;
      let valid19 = false;
      const _errs80 = errors;
      if (typeof data15 !== "string") {
        const err46 = { instancePath: instancePath + "/comment_text", schemaPath: "#/properties/comment_text/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err46];
        } else {
          vErrors.push(err46);
        }
        errors++;
      }
      var _valid9 = _errs80 === errors;
      valid19 = valid19 || _valid9;
      const _errs82 = errors;
      if (data15 !== null) {
        const err47 = { instancePath: instancePath + "/comment_text", schemaPath: "#/properties/comment_text/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err47];
        } else {
          vErrors.push(err47);
        }
        errors++;
      }
      var _valid9 = _errs82 === errors;
      valid19 = valid19 || _valid9;
      if (!valid19) {
        const err48 = { instancePath: instancePath + "/comment_text", schemaPath: "#/properties/comment_text/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err48];
        } else {
          vErrors.push(err48);
        }
        errors++;
      } else {
        errors = _errs79;
        if (vErrors !== null) {
          if (_errs79) {
            vErrors.length = _errs79;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.component_parameters !== void 0) {
      let data16 = data.component_parameters;
      const _errs85 = errors;
      let valid20 = false;
      const _errs86 = errors;
      if (data16 && typeof data16 == "object" && !Array.isArray(data16)) {
        for (const key1 in data16) {
          if (typeof data16[key1] !== "string") {
            const err49 = { instancePath: instancePath + "/component_parameters/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/RecordString/unevaluatedProperties/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err49];
            } else {
              vErrors.push(err49);
            }
            errors++;
          }
        }
      } else {
        const err50 = { instancePath: instancePath + "/component_parameters", schemaPath: "#/$defs/RecordString/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err50];
        } else {
          vErrors.push(err50);
        }
        errors++;
      }
      var _valid10 = _errs86 === errors;
      valid20 = valid20 || _valid10;
      const _errs92 = errors;
      if (data16 !== null) {
        const err51 = { instancePath: instancePath + "/component_parameters", schemaPath: "#/properties/component_parameters/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err51];
        } else {
          vErrors.push(err51);
        }
        errors++;
      }
      var _valid10 = _errs92 === errors;
      valid20 = valid20 || _valid10;
      if (!valid20) {
        const err52 = { instancePath: instancePath + "/component_parameters", schemaPath: "#/properties/component_parameters/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err52];
        } else {
          vErrors.push(err52);
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
    if (data.pad_nets !== void 0) {
      let data18 = data.pad_nets;
      const _errs95 = errors;
      let valid23 = false;
      const _errs96 = errors;
      if (data18 && typeof data18 == "object" && !Array.isArray(data18)) {
        for (const key2 in data18) {
          if (typeof data18[key2] !== "string") {
            const err53 = { instancePath: instancePath + "/pad_nets/" + key2.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/RecordString/unevaluatedProperties/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err53];
            } else {
              vErrors.push(err53);
            }
            errors++;
          }
        }
      } else {
        const err54 = { instancePath: instancePath + "/pad_nets", schemaPath: "#/$defs/RecordString/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err54];
        } else {
          vErrors.push(err54);
        }
        errors++;
      }
      var _valid11 = _errs96 === errors;
      valid23 = valid23 || _valid11;
      const _errs102 = errors;
      if (data18 !== null) {
        const err55 = { instancePath: instancePath + "/pad_nets", schemaPath: "#/properties/pad_nets/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err55];
        } else {
          vErrors.push(err55);
        }
        errors++;
      }
      var _valid11 = _errs102 === errors;
      valid23 = valid23 || _valid11;
      if (!valid23) {
        const err56 = { instancePath: instancePath + "/pad_nets", schemaPath: "#/properties/pad_nets/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err56];
        } else {
          vErrors.push(err56);
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
    if (data.rotation_degrees !== void 0) {
      let data20 = data.rotation_degrees;
      const _errs105 = errors;
      let valid26 = false;
      const _errs106 = errors;
      if (!(typeof data20 == "number")) {
        const err57 = { instancePath: instancePath + "/rotation_degrees", schemaPath: "#/properties/rotation_degrees/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err57];
        } else {
          vErrors.push(err57);
        }
        errors++;
      }
      var _valid12 = _errs106 === errors;
      valid26 = valid26 || _valid12;
      const _errs108 = errors;
      if (data20 !== null) {
        const err58 = { instancePath: instancePath + "/rotation_degrees", schemaPath: "#/properties/rotation_degrees/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err58];
        } else {
          vErrors.push(err58);
        }
        errors++;
      }
      var _valid12 = _errs108 === errors;
      valid26 = valid26 || _valid12;
      if (!valid26) {
        const err59 = { instancePath: instancePath + "/rotation_degrees", schemaPath: "#/properties/rotation_degrees/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err59];
        } else {
          vErrors.push(err59);
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
    if (data.source_footprint_library !== void 0) {
      let data21 = data.source_footprint_library;
      const _errs111 = errors;
      let valid27 = false;
      const _errs112 = errors;
      if (typeof data21 !== "string") {
        const err60 = { instancePath: instancePath + "/source_footprint_library", schemaPath: "#/properties/source_footprint_library/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err60];
        } else {
          vErrors.push(err60);
        }
        errors++;
      }
      var _valid13 = _errs112 === errors;
      valid27 = valid27 || _valid13;
      const _errs114 = errors;
      if (data21 !== null) {
        const err61 = { instancePath: instancePath + "/source_footprint_library", schemaPath: "#/properties/source_footprint_library/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err61];
        } else {
          vErrors.push(err61);
        }
        errors++;
      }
      var _valid13 = _errs114 === errors;
      valid27 = valid27 || _valid13;
      if (!valid27) {
        const err62 = { instancePath: instancePath + "/source_footprint_library", schemaPath: "#/properties/source_footprint_library/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err62];
        } else {
          vErrors.push(err62);
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
    }
    if (data.comment_visible !== void 0) {
      let data22 = data.comment_visible;
      const _errs117 = errors;
      let valid28 = false;
      const _errs118 = errors;
      if (typeof data22 !== "boolean") {
        const err63 = { instancePath: instancePath + "/comment_visible", schemaPath: "#/properties/comment_visible/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err63];
        } else {
          vErrors.push(err63);
        }
        errors++;
      }
      var _valid14 = _errs118 === errors;
      valid28 = valid28 || _valid14;
      const _errs120 = errors;
      if (data22 !== null) {
        const err64 = { instancePath: instancePath + "/comment_visible", schemaPath: "#/properties/comment_visible/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err64];
        } else {
          vErrors.push(err64);
        }
        errors++;
      }
      var _valid14 = _errs120 === errors;
      valid28 = valid28 || _valid14;
      if (!valid28) {
        const err65 = { instancePath: instancePath + "/comment_visible", schemaPath: "#/properties/comment_visible/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err65];
        } else {
          vErrors.push(err65);
        }
        errors++;
      } else {
        errors = _errs117;
        if (vErrors !== null) {
          if (_errs117) {
            vErrors.length = _errs117;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.source_designator !== void 0) {
      let data23 = data.source_designator;
      const _errs123 = errors;
      let valid29 = false;
      const _errs124 = errors;
      if (typeof data23 !== "string") {
        const err66 = { instancePath: instancePath + "/source_designator", schemaPath: "#/properties/source_designator/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err66];
        } else {
          vErrors.push(err66);
        }
        errors++;
      }
      var _valid15 = _errs124 === errors;
      valid29 = valid29 || _valid15;
      const _errs126 = errors;
      if (data23 !== null) {
        const err67 = { instancePath: instancePath + "/source_designator", schemaPath: "#/properties/source_designator/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err67];
        } else {
          vErrors.push(err67);
        }
        errors++;
      }
      var _valid15 = _errs126 === errors;
      valid29 = valid29 || _valid15;
      if (!valid29) {
        const err68 = { instancePath: instancePath + "/source_designator", schemaPath: "#/properties/source_designator/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err68];
        } else {
          vErrors.push(err68);
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
  } else {
    const err69 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err69];
    } else {
      vErrors.push(err69);
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("pcbdoc.add_component" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "pcbdoc.add_component" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate40(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate40.errors : vErrors.concat(validate40.errors);
        errors = vErrors.length;
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
  validate39.errors = vErrors;
  return errors === 0;
}
validate39.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
      if (!(typeof data.left == "number")) {
        const err5 = { instancePath: instancePath + "/left", schemaPath: "#/properties/left/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.bottom !== void 0) {
      if (!(typeof data.bottom == "number")) {
        const err6 = { instancePath: instancePath + "/bottom", schemaPath: "#/properties/bottom/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.right !== void 0) {
      if (!(typeof data.right == "number")) {
        const err7 = { instancePath: instancePath + "/right", schemaPath: "#/properties/right/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.top !== void 0) {
      if (!(typeof data.top == "number")) {
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
  validate45.errors = vErrors;
  return errors === 0;
}
validate45.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate47(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate47.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (Array.isArray(data)) {
    if (data.length < 3) {
      const err0 = { instancePath, schemaPath: "#/minItems", keyword: "minItems", params: { limit: 3 }, message: "must NOT have fewer than 3 items" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    const len0 = data.length;
    for (let i0 = 0; i0 < len0; i0++) {
      let data0 = data[i0];
      if (Array.isArray(data0)) {
        if (data0.length > 2) {
          const err1 = { instancePath: instancePath + "/" + i0, schemaPath: "#/$defs/PointMils/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err1];
          } else {
            vErrors.push(err1);
          }
          errors++;
        }
        if (data0.length < 2) {
          const err2 = { instancePath: instancePath + "/" + i0, schemaPath: "#/$defs/PointMils/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err2];
          } else {
            vErrors.push(err2);
          }
          errors++;
        }
        const len1 = data0.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (!(typeof data0[i1] == "number")) {
            const err3 = { instancePath: instancePath + "/" + i0 + "/" + i1, schemaPath: "#/$defs/PointMils/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err3];
            } else {
              vErrors.push(err3);
            }
            errors++;
          }
        }
      } else {
        const err4 = { instancePath: instancePath + "/" + i0, schemaPath: "#/$defs/PointMils/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
  } else {
    const err5 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "array" }, message: "must be array" };
    if (vErrors === null) {
      vErrors = [err5];
    } else {
      vErrors.push(err5);
    }
    errors++;
  }
  validate47.errors = vErrors;
  return errors === 0;
}
validate47.evaluated = { "items": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.model_file === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "model_file" }, message: "must have required property 'model_file'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err3 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.output_file !== void 0) {
      let data1 = data.output_file;
      const _errs9 = errors;
      let valid4 = false;
      const _errs10 = errors;
      if (typeof data1 !== "string") {
        const err5 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      valid4 = valid4 || _valid0;
      const _errs12 = errors;
      if (data1 !== null) {
        const err6 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs12 === errors;
      valid4 = valid4 || _valid0;
      if (!valid4) {
        const err7 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.overwrite !== void 0) {
      let data2 = data.overwrite;
      const _errs15 = errors;
      let valid5 = false;
      const _errs16 = errors;
      if (typeof data2 !== "boolean") {
        const err8 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid1 = _errs16 === errors;
      valid5 = valid5 || _valid1;
      const _errs18 = errors;
      if (data2 !== null) {
        const err9 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid1 = _errs18 === errors;
      valid5 = valid5 || _valid1;
      if (!valid5) {
        const err10 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
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
    if (data.model_file !== void 0) {
      let data3 = data.model_file;
      if (typeof data3 === "string") {
        if (func1(data3) < 1) {
          const err11 = { instancePath: instancePath + "/model_file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err11];
          } else {
            vErrors.push(err11);
          }
          errors++;
        }
      } else {
        const err12 = { instancePath: instancePath + "/model_file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
    }
    if (data.model_name !== void 0) {
      let data4 = data.model_name;
      const _errs24 = errors;
      let valid7 = false;
      const _errs25 = errors;
      if (typeof data4 !== "string") {
        const err13 = { instancePath: instancePath + "/model_name", schemaPath: "#/properties/model_name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid2 = _errs25 === errors;
      valid7 = valid7 || _valid2;
      const _errs27 = errors;
      if (data4 !== null) {
        const err14 = { instancePath: instancePath + "/model_name", schemaPath: "#/properties/model_name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid2 = _errs27 === errors;
      valid7 = valid7 || _valid2;
      if (!valid7) {
        const err15 = { instancePath: instancePath + "/model_name", schemaPath: "#/properties/model_name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
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
    if (data.name !== void 0) {
      let data5 = data.name;
      const _errs30 = errors;
      let valid8 = false;
      const _errs31 = errors;
      if (typeof data5 !== "string") {
        const err16 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid3 = _errs31 === errors;
      valid8 = valid8 || _valid3;
      const _errs33 = errors;
      if (data5 !== null) {
        const err17 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      var _valid3 = _errs33 === errors;
      valid8 = valid8 || _valid3;
      if (!valid8) {
        const err18 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.layer !== void 0) {
      let data6 = data.layer;
      const _errs36 = errors;
      let valid9 = false;
      const _errs37 = errors;
      if (typeof data6 !== "string") {
        const err19 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (!(typeof data6 == "number" && (!(data6 % 1) && !isNaN(data6)))) {
        const err20 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      var _valid4 = _errs39 === errors;
      valid9 = valid9 || _valid4;
      const _errs41 = errors;
      if (data6 !== null) {
        const err21 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      var _valid4 = _errs41 === errors;
      valid9 = valid9 || _valid4;
      if (!valid9) {
        const err22 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
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
    if (data.side !== void 0) {
      let data7 = data.side;
      const _errs44 = errors;
      let valid10 = false;
      const _errs45 = errors;
      if (typeof data7 !== "string") {
        const err23 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      var _valid5 = _errs45 === errors;
      valid10 = valid10 || _valid5;
      const _errs47 = errors;
      if (!(typeof data7 == "number" && (!(data7 % 1) && !isNaN(data7)))) {
        const err24 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      var _valid5 = _errs47 === errors;
      valid10 = valid10 || _valid5;
      const _errs49 = errors;
      if (data7 !== null) {
        const err25 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
      var _valid5 = _errs49 === errors;
      valid10 = valid10 || _valid5;
      if (!valid10) {
        const err26 = { instancePath: instancePath + "/side", schemaPath: "#/properties/side/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
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
    if (data.location_mils !== void 0) {
      let data8 = data.location_mils;
      const _errs52 = errors;
      let valid11 = false;
      const _errs53 = errors;
      if (Array.isArray(data8)) {
        if (data8.length > 2) {
          const err27 = { instancePath: instancePath + "/location_mils", schemaPath: "#/$defs/PointMils/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err27];
          } else {
            vErrors.push(err27);
          }
          errors++;
        }
        if (data8.length < 2) {
          const err28 = { instancePath: instancePath + "/location_mils", schemaPath: "#/$defs/PointMils/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err28];
          } else {
            vErrors.push(err28);
          }
          errors++;
        }
        const len0 = data8.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!(typeof data8[i0] == "number")) {
            const err29 = { instancePath: instancePath + "/location_mils/" + i0, schemaPath: "#/$defs/PointMils/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err29];
            } else {
              vErrors.push(err29);
            }
            errors++;
          }
        }
      } else {
        const err30 = { instancePath: instancePath + "/location_mils", schemaPath: "#/$defs/PointMils/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
        }
        errors++;
      }
      var _valid6 = _errs53 === errors;
      valid11 = valid11 || _valid6;
      const _errs58 = errors;
      if (data8 !== null) {
        const err31 = { instancePath: instancePath + "/location_mils", schemaPath: "#/properties/location_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      }
      var _valid6 = _errs58 === errors;
      valid11 = valid11 || _valid6;
      if (!valid11) {
        const err32 = { instancePath: instancePath + "/location_mils", schemaPath: "#/properties/location_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
        }
        errors++;
      } else {
        errors = _errs52;
        if (vErrors !== null) {
          if (_errs52) {
            vErrors.length = _errs52;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.rotation_x_degrees !== void 0) {
      let data10 = data.rotation_x_degrees;
      const _errs61 = errors;
      let valid15 = false;
      const _errs62 = errors;
      if (!(typeof data10 == "number")) {
        const err33 = { instancePath: instancePath + "/rotation_x_degrees", schemaPath: "#/properties/rotation_x_degrees/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
      var _valid7 = _errs62 === errors;
      valid15 = valid15 || _valid7;
      const _errs64 = errors;
      if (data10 !== null) {
        const err34 = { instancePath: instancePath + "/rotation_x_degrees", schemaPath: "#/properties/rotation_x_degrees/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
        }
        errors++;
      }
      var _valid7 = _errs64 === errors;
      valid15 = valid15 || _valid7;
      if (!valid15) {
        const err35 = { instancePath: instancePath + "/rotation_x_degrees", schemaPath: "#/properties/rotation_x_degrees/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.rotation_y_degrees !== void 0) {
      let data11 = data.rotation_y_degrees;
      const _errs67 = errors;
      let valid16 = false;
      const _errs68 = errors;
      if (!(typeof data11 == "number")) {
        const err36 = { instancePath: instancePath + "/rotation_y_degrees", schemaPath: "#/properties/rotation_y_degrees/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err36];
        } else {
          vErrors.push(err36);
        }
        errors++;
      }
      var _valid8 = _errs68 === errors;
      valid16 = valid16 || _valid8;
      const _errs70 = errors;
      if (data11 !== null) {
        const err37 = { instancePath: instancePath + "/rotation_y_degrees", schemaPath: "#/properties/rotation_y_degrees/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err37];
        } else {
          vErrors.push(err37);
        }
        errors++;
      }
      var _valid8 = _errs70 === errors;
      valid16 = valid16 || _valid8;
      if (!valid16) {
        const err38 = { instancePath: instancePath + "/rotation_y_degrees", schemaPath: "#/properties/rotation_y_degrees/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err38];
        } else {
          vErrors.push(err38);
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
    if (data.rotation_z_degrees !== void 0) {
      let data12 = data.rotation_z_degrees;
      const _errs73 = errors;
      let valid17 = false;
      const _errs74 = errors;
      if (!(typeof data12 == "number")) {
        const err39 = { instancePath: instancePath + "/rotation_z_degrees", schemaPath: "#/properties/rotation_z_degrees/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err39];
        } else {
          vErrors.push(err39);
        }
        errors++;
      }
      var _valid9 = _errs74 === errors;
      valid17 = valid17 || _valid9;
      const _errs76 = errors;
      if (data12 !== null) {
        const err40 = { instancePath: instancePath + "/rotation_z_degrees", schemaPath: "#/properties/rotation_z_degrees/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err40];
        } else {
          vErrors.push(err40);
        }
        errors++;
      }
      var _valid9 = _errs76 === errors;
      valid17 = valid17 || _valid9;
      if (!valid17) {
        const err41 = { instancePath: instancePath + "/rotation_z_degrees", schemaPath: "#/properties/rotation_z_degrees/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err41];
        } else {
          vErrors.push(err41);
        }
        errors++;
      } else {
        errors = _errs73;
        if (vErrors !== null) {
          if (_errs73) {
            vErrors.length = _errs73;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.z_mm !== void 0) {
      let data13 = data.z_mm;
      const _errs79 = errors;
      let valid18 = false;
      const _errs80 = errors;
      if (!(typeof data13 == "number")) {
        const err42 = { instancePath: instancePath + "/z_mm", schemaPath: "#/properties/z_mm/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err42];
        } else {
          vErrors.push(err42);
        }
        errors++;
      }
      var _valid10 = _errs80 === errors;
      valid18 = valid18 || _valid10;
      const _errs82 = errors;
      if (data13 !== null) {
        const err43 = { instancePath: instancePath + "/z_mm", schemaPath: "#/properties/z_mm/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err43];
        } else {
          vErrors.push(err43);
        }
        errors++;
      }
      var _valid10 = _errs82 === errors;
      valid18 = valid18 || _valid10;
      if (!valid18) {
        const err44 = { instancePath: instancePath + "/z_mm", schemaPath: "#/properties/z_mm/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err44];
        } else {
          vErrors.push(err44);
        }
        errors++;
      } else {
        errors = _errs79;
        if (vErrors !== null) {
          if (_errs79) {
            vErrors.length = _errs79;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.bounds_mils !== void 0) {
      let data14 = data.bounds_mils;
      const _errs85 = errors;
      let valid19 = false;
      const _errs86 = errors;
      if (!validate45(data14, { instancePath: instancePath + "/bounds_mils", parentData: data, parentDataProperty: "bounds_mils", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate45.errors : vErrors.concat(validate45.errors);
        errors = vErrors.length;
      }
      var _valid11 = _errs86 === errors;
      valid19 = valid19 || _valid11;
      const _errs87 = errors;
      if (Array.isArray(data14)) {
        if (data14.length > 4) {
          const err45 = { instancePath: instancePath + "/bounds_mils", schemaPath: "#/$defs/BoundsArray/maxItems", keyword: "maxItems", params: { limit: 4 }, message: "must NOT have more than 4 items" };
          if (vErrors === null) {
            vErrors = [err45];
          } else {
            vErrors.push(err45);
          }
          errors++;
        }
        if (data14.length < 4) {
          const err46 = { instancePath: instancePath + "/bounds_mils", schemaPath: "#/$defs/BoundsArray/minItems", keyword: "minItems", params: { limit: 4 }, message: "must NOT have fewer than 4 items" };
          if (vErrors === null) {
            vErrors = [err46];
          } else {
            vErrors.push(err46);
          }
          errors++;
        }
        const len1 = data14.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (!(typeof data14[i1] == "number")) {
            const err47 = { instancePath: instancePath + "/bounds_mils/" + i1, schemaPath: "#/$defs/BoundsArray/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err47];
            } else {
              vErrors.push(err47);
            }
            errors++;
          }
        }
      } else {
        const err48 = { instancePath: instancePath + "/bounds_mils", schemaPath: "#/$defs/BoundsArray/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err48];
        } else {
          vErrors.push(err48);
        }
        errors++;
      }
      var _valid11 = _errs87 === errors;
      valid19 = valid19 || _valid11;
      const _errs92 = errors;
      if (data14 !== null) {
        const err49 = { instancePath: instancePath + "/bounds_mils", schemaPath: "#/properties/bounds_mils/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err49];
        } else {
          vErrors.push(err49);
        }
        errors++;
      }
      var _valid11 = _errs92 === errors;
      valid19 = valid19 || _valid11;
      if (!valid19) {
        const err50 = { instancePath: instancePath + "/bounds_mils", schemaPath: "#/properties/bounds_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err50];
        } else {
          vErrors.push(err50);
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
    if (data.projection_outline_mils !== void 0) {
      let data16 = data.projection_outline_mils;
      const _errs95 = errors;
      let valid23 = false;
      const _errs96 = errors;
      if (!validate47(data16, { instancePath: instancePath + "/projection_outline_mils", parentData: data, parentDataProperty: "projection_outline_mils", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate47.errors : vErrors.concat(validate47.errors);
        errors = vErrors.length;
      }
      var _valid12 = _errs96 === errors;
      valid23 = valid23 || _valid12;
      const _errs97 = errors;
      if (data16 !== null) {
        const err51 = { instancePath: instancePath + "/projection_outline_mils", schemaPath: "#/properties/projection_outline_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err51];
        } else {
          vErrors.push(err51);
        }
        errors++;
      }
      var _valid12 = _errs97 === errors;
      valid23 = valid23 || _valid12;
      if (!valid23) {
        const err52 = { instancePath: instancePath + "/projection_outline_mils", schemaPath: "#/properties/projection_outline_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err52];
        } else {
          vErrors.push(err52);
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
    if (data.overall_height_mils !== void 0) {
      let data17 = data.overall_height_mils;
      const _errs100 = errors;
      let valid24 = false;
      const _errs101 = errors;
      if (!(typeof data17 == "number")) {
        const err53 = { instancePath: instancePath + "/overall_height_mils", schemaPath: "#/properties/overall_height_mils/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err53];
        } else {
          vErrors.push(err53);
        }
        errors++;
      }
      var _valid13 = _errs101 === errors;
      valid24 = valid24 || _valid13;
      const _errs103 = errors;
      if (data17 !== null) {
        const err54 = { instancePath: instancePath + "/overall_height_mils", schemaPath: "#/properties/overall_height_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err54];
        } else {
          vErrors.push(err54);
        }
        errors++;
      }
      var _valid13 = _errs103 === errors;
      valid24 = valid24 || _valid13;
      if (!valid24) {
        const err55 = { instancePath: instancePath + "/overall_height_mils", schemaPath: "#/properties/overall_height_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err55];
        } else {
          vErrors.push(err55);
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
    if (data.opacity !== void 0) {
      let data18 = data.opacity;
      const _errs106 = errors;
      let valid25 = false;
      const _errs107 = errors;
      if (!(typeof data18 == "number")) {
        const err56 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err56];
        } else {
          vErrors.push(err56);
        }
        errors++;
      }
      var _valid14 = _errs107 === errors;
      valid25 = valid25 || _valid14;
      const _errs109 = errors;
      if (data18 !== null) {
        const err57 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err57];
        } else {
          vErrors.push(err57);
        }
        errors++;
      }
      var _valid14 = _errs109 === errors;
      valid25 = valid25 || _valid14;
      if (!valid25) {
        const err58 = { instancePath: instancePath + "/opacity", schemaPath: "#/properties/opacity/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err58];
        } else {
          vErrors.push(err58);
        }
        errors++;
      } else {
        errors = _errs106;
        if (vErrors !== null) {
          if (_errs106) {
            vErrors.length = _errs106;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.z_mils !== void 0) {
      if (!(typeof data.z_mils == "number")) {
        const err59 = { instancePath: instancePath + "/z_mils", schemaPath: "#/properties/z_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err59];
        } else {
          vErrors.push(err59);
        }
        errors++;
      }
    }
  } else {
    const err60 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err60];
    } else {
      vErrors.push(err60);
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("pcbdoc.add_embedded_3d_model" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "pcbdoc.add_embedded_3d_model" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate44(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate44.errors : vErrors.concat(validate44.errors);
        errors = vErrors.length;
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.corner1_mils === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "corner1_mils" }, message: "must have required property 'corner1_mils'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.corner2_mils === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "corner2_mils" }, message: "must have required property 'corner2_mils'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err4 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err4];
          } else {
            vErrors.push(err4);
          }
          errors++;
        }
      } else {
        const err5 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.output_file !== void 0) {
      let data1 = data.output_file;
      const _errs9 = errors;
      let valid4 = false;
      const _errs10 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      valid4 = valid4 || _valid0;
      const _errs12 = errors;
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid0 = _errs12 === errors;
      valid4 = valid4 || _valid0;
      if (!valid4) {
        const err8 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.overwrite !== void 0) {
      let data2 = data.overwrite;
      const _errs15 = errors;
      let valid5 = false;
      const _errs16 = errors;
      if (typeof data2 !== "boolean") {
        const err9 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid1 = _errs16 === errors;
      valid5 = valid5 || _valid1;
      const _errs18 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid1 = _errs18 === errors;
      valid5 = valid5 || _valid1;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
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
    if (data.corner1_mils !== void 0) {
      let data3 = data.corner1_mils;
      if (Array.isArray(data3)) {
        if (data3.length > 2) {
          const err12 = { instancePath: instancePath + "/corner1_mils", schemaPath: "#/$defs/PointMils/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err12];
          } else {
            vErrors.push(err12);
          }
          errors++;
        }
        if (data3.length < 2) {
          const err13 = { instancePath: instancePath + "/corner1_mils", schemaPath: "#/$defs/PointMils/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err13];
          } else {
            vErrors.push(err13);
          }
          errors++;
        }
        const len0 = data3.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!(typeof data3[i0] == "number")) {
            const err14 = { instancePath: instancePath + "/corner1_mils/" + i0, schemaPath: "#/$defs/PointMils/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err14];
            } else {
              vErrors.push(err14);
            }
            errors++;
          }
        }
      } else {
        const err15 = { instancePath: instancePath + "/corner1_mils", schemaPath: "#/$defs/PointMils/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
    }
    if (data.corner2_mils !== void 0) {
      let data5 = data.corner2_mils;
      if (Array.isArray(data5)) {
        if (data5.length > 2) {
          const err16 = { instancePath: instancePath + "/corner2_mils", schemaPath: "#/$defs/PointMils/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err16];
          } else {
            vErrors.push(err16);
          }
          errors++;
        }
        if (data5.length < 2) {
          const err17 = { instancePath: instancePath + "/corner2_mils", schemaPath: "#/$defs/PointMils/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err17];
          } else {
            vErrors.push(err17);
          }
          errors++;
        }
        const len1 = data5.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (!(typeof data5[i1] == "number")) {
            const err18 = { instancePath: instancePath + "/corner2_mils/" + i1, schemaPath: "#/$defs/PointMils/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err18];
            } else {
              vErrors.push(err18);
            }
            errors++;
          }
        }
      } else {
        const err19 = { instancePath: instancePath + "/corner2_mils", schemaPath: "#/$defs/PointMils/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
    }
    if (data.rotation_degrees !== void 0) {
      let data7 = data.rotation_degrees;
      const _errs31 = errors;
      let valid12 = false;
      const _errs32 = errors;
      if (!(typeof data7 == "number")) {
        const err20 = { instancePath: instancePath + "/rotation_degrees", schemaPath: "#/properties/rotation_degrees/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      var _valid2 = _errs32 === errors;
      valid12 = valid12 || _valid2;
      const _errs34 = errors;
      if (data7 !== null) {
        const err21 = { instancePath: instancePath + "/rotation_degrees", schemaPath: "#/properties/rotation_degrees/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      var _valid2 = _errs34 === errors;
      valid12 = valid12 || _valid2;
      if (!valid12) {
        const err22 = { instancePath: instancePath + "/rotation_degrees", schemaPath: "#/properties/rotation_degrees/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
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
      let data8 = data.layer;
      const _errs37 = errors;
      let valid13 = false;
      const _errs38 = errors;
      if (typeof data8 !== "string") {
        const err23 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      var _valid3 = _errs38 === errors;
      valid13 = valid13 || _valid3;
      const _errs40 = errors;
      if (!(typeof data8 == "number" && (!(data8 % 1) && !isNaN(data8)))) {
        const err24 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      var _valid3 = _errs40 === errors;
      valid13 = valid13 || _valid3;
      const _errs42 = errors;
      if (data8 !== null) {
        const err25 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
      var _valid3 = _errs42 === errors;
      valid13 = valid13 || _valid3;
      if (!valid13) {
        const err26 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
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
    }
    if (data.net !== void 0) {
      let data9 = data.net;
      const _errs45 = errors;
      let valid14 = false;
      const _errs46 = errors;
      if (typeof data9 !== "string") {
        const err27 = { instancePath: instancePath + "/net", schemaPath: "#/properties/net/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
      var _valid4 = _errs46 === errors;
      valid14 = valid14 || _valid4;
      const _errs48 = errors;
      if (data9 !== null) {
        const err28 = { instancePath: instancePath + "/net", schemaPath: "#/properties/net/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
      var _valid4 = _errs48 === errors;
      valid14 = valid14 || _valid4;
      if (!valid14) {
        const err29 = { instancePath: instancePath + "/net", schemaPath: "#/properties/net/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
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
    const err30 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err30];
    } else {
      vErrors.push(err30);
    }
    errors++;
  }
  validate52.errors = vErrors;
  return errors === 0;
}
validate52.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("pcbdoc.add_fill" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "pcbdoc.add_fill" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate52(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate52.errors : vErrors.concat(validate52.errors);
        errors = vErrors.length;
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
  validate51.errors = vErrors;
  return errors === 0;
}
validate51.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
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
    if (data.position_mils === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "position_mils" }, message: "must have required property 'position_mils'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.width_mils === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "width_mils" }, message: "must have required property 'width_mils'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.height_mils === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "height_mils" }, message: "must have required property 'height_mils'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err6 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err6];
          } else {
            vErrors.push(err6);
          }
          errors++;
        }
      } else {
        const err7 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.output_file !== void 0) {
      let data1 = data.output_file;
      const _errs9 = errors;
      let valid4 = false;
      const _errs10 = errors;
      if (typeof data1 !== "string") {
        const err8 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      valid4 = valid4 || _valid0;
      const _errs12 = errors;
      if (data1 !== null) {
        const err9 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid0 = _errs12 === errors;
      valid4 = valid4 || _valid0;
      if (!valid4) {
        const err10 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
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
    if (data.overwrite !== void 0) {
      let data2 = data.overwrite;
      const _errs15 = errors;
      let valid5 = false;
      const _errs16 = errors;
      if (typeof data2 !== "boolean") {
        const err11 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid1 = _errs16 === errors;
      valid5 = valid5 || _valid1;
      const _errs18 = errors;
      if (data2 !== null) {
        const err12 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid1 = _errs18 === errors;
      valid5 = valid5 || _valid1;
      if (!valid5) {
        const err13 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
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
    if (data.designator !== void 0) {
      let data3 = data.designator;
      if (typeof data3 === "string") {
        if (func1(data3) < 1) {
          const err14 = { instancePath: instancePath + "/designator", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err14];
          } else {
            vErrors.push(err14);
          }
          errors++;
        }
      } else {
        const err15 = { instancePath: instancePath + "/designator", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
    }
    if (data.position_mils !== void 0) {
      let data4 = data.position_mils;
      if (Array.isArray(data4)) {
        if (data4.length > 2) {
          const err16 = { instancePath: instancePath + "/position_mils", schemaPath: "#/$defs/PointMils/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err16];
          } else {
            vErrors.push(err16);
          }
          errors++;
        }
        if (data4.length < 2) {
          const err17 = { instancePath: instancePath + "/position_mils", schemaPath: "#/$defs/PointMils/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err17];
          } else {
            vErrors.push(err17);
          }
          errors++;
        }
        const len0 = data4.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!(typeof data4[i0] == "number")) {
            const err18 = { instancePath: instancePath + "/position_mils/" + i0, schemaPath: "#/$defs/PointMils/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err18];
            } else {
              vErrors.push(err18);
            }
            errors++;
          }
        }
      } else {
        const err19 = { instancePath: instancePath + "/position_mils", schemaPath: "#/$defs/PointMils/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
    }
    if (data.width_mils !== void 0) {
      if (!(typeof data.width_mils == "number")) {
        const err20 = { instancePath: instancePath + "/width_mils", schemaPath: "#/properties/width_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
    }
    if (data.height_mils !== void 0) {
      if (!(typeof data.height_mils == "number")) {
        const err21 = { instancePath: instancePath + "/height_mils", schemaPath: "#/properties/height_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
    }
    if (data.shape !== void 0) {
      let data8 = data.shape;
      const _errs33 = errors;
      let valid10 = false;
      const _errs34 = errors;
      if (typeof data8 !== "string") {
        const err22 = { instancePath: instancePath + "/shape", schemaPath: "#/properties/shape/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
      var _valid2 = _errs34 === errors;
      valid10 = valid10 || _valid2;
      const _errs36 = errors;
      if (!(typeof data8 == "number" && (!(data8 % 1) && !isNaN(data8)))) {
        const err23 = { instancePath: instancePath + "/shape", schemaPath: "#/properties/shape/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      var _valid2 = _errs36 === errors;
      valid10 = valid10 || _valid2;
      const _errs38 = errors;
      if (data8 !== null) {
        const err24 = { instancePath: instancePath + "/shape", schemaPath: "#/properties/shape/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      var _valid2 = _errs38 === errors;
      valid10 = valid10 || _valid2;
      if (!valid10) {
        const err25 = { instancePath: instancePath + "/shape", schemaPath: "#/properties/shape/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    }
    if (data.corner_radius_percent !== void 0) {
      let data9 = data.corner_radius_percent;
      const _errs41 = errors;
      let valid11 = false;
      const _errs42 = errors;
      if (!(typeof data9 == "number")) {
        const err26 = { instancePath: instancePath + "/corner_radius_percent", schemaPath: "#/properties/corner_radius_percent/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
      var _valid3 = _errs42 === errors;
      valid11 = valid11 || _valid3;
      const _errs44 = errors;
      if (data9 !== null) {
        const err27 = { instancePath: instancePath + "/corner_radius_percent", schemaPath: "#/properties/corner_radius_percent/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
      var _valid3 = _errs44 === errors;
      valid11 = valid11 || _valid3;
      if (!valid11) {
        const err28 = { instancePath: instancePath + "/corner_radius_percent", schemaPath: "#/properties/corner_radius_percent/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
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
    if (data.rotation_degrees !== void 0) {
      let data10 = data.rotation_degrees;
      const _errs47 = errors;
      let valid12 = false;
      const _errs48 = errors;
      if (!(typeof data10 == "number")) {
        const err29 = { instancePath: instancePath + "/rotation_degrees", schemaPath: "#/properties/rotation_degrees/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      }
      var _valid4 = _errs48 === errors;
      valid12 = valid12 || _valid4;
      const _errs50 = errors;
      if (data10 !== null) {
        const err30 = { instancePath: instancePath + "/rotation_degrees", schemaPath: "#/properties/rotation_degrees/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
        }
        errors++;
      }
      var _valid4 = _errs50 === errors;
      valid12 = valid12 || _valid4;
      if (!valid12) {
        const err31 = { instancePath: instancePath + "/rotation_degrees", schemaPath: "#/properties/rotation_degrees/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
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
    if (data.hole_size_mils !== void 0) {
      let data11 = data.hole_size_mils;
      const _errs53 = errors;
      let valid13 = false;
      const _errs54 = errors;
      if (!(typeof data11 == "number")) {
        const err32 = { instancePath: instancePath + "/hole_size_mils", schemaPath: "#/properties/hole_size_mils/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
        }
        errors++;
      }
      var _valid5 = _errs54 === errors;
      valid13 = valid13 || _valid5;
      const _errs56 = errors;
      if (data11 !== null) {
        const err33 = { instancePath: instancePath + "/hole_size_mils", schemaPath: "#/properties/hole_size_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
      var _valid5 = _errs56 === errors;
      valid13 = valid13 || _valid5;
      if (!valid13) {
        const err34 = { instancePath: instancePath + "/hole_size_mils", schemaPath: "#/properties/hole_size_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
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
    if (data.plated !== void 0) {
      let data12 = data.plated;
      const _errs59 = errors;
      let valid14 = false;
      const _errs60 = errors;
      if (typeof data12 !== "boolean") {
        const err35 = { instancePath: instancePath + "/plated", schemaPath: "#/properties/plated/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err35];
        } else {
          vErrors.push(err35);
        }
        errors++;
      }
      var _valid6 = _errs60 === errors;
      valid14 = valid14 || _valid6;
      const _errs62 = errors;
      if (data12 !== null) {
        const err36 = { instancePath: instancePath + "/plated", schemaPath: "#/properties/plated/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err36];
        } else {
          vErrors.push(err36);
        }
        errors++;
      }
      var _valid6 = _errs62 === errors;
      valid14 = valid14 || _valid6;
      if (!valid14) {
        const err37 = { instancePath: instancePath + "/plated", schemaPath: "#/properties/plated/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err37];
        } else {
          vErrors.push(err37);
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
    if (data.layer !== void 0) {
      let data13 = data.layer;
      const _errs65 = errors;
      let valid15 = false;
      const _errs66 = errors;
      if (typeof data13 !== "string") {
        const err38 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err38];
        } else {
          vErrors.push(err38);
        }
        errors++;
      }
      var _valid7 = _errs66 === errors;
      valid15 = valid15 || _valid7;
      const _errs68 = errors;
      if (!(typeof data13 == "number" && (!(data13 % 1) && !isNaN(data13)))) {
        const err39 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err39];
        } else {
          vErrors.push(err39);
        }
        errors++;
      }
      var _valid7 = _errs68 === errors;
      valid15 = valid15 || _valid7;
      const _errs70 = errors;
      if (data13 !== null) {
        const err40 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err40];
        } else {
          vErrors.push(err40);
        }
        errors++;
      }
      var _valid7 = _errs70 === errors;
      valid15 = valid15 || _valid7;
      if (!valid15) {
        const err41 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err41];
        } else {
          vErrors.push(err41);
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
    if (data.net !== void 0) {
      let data14 = data.net;
      const _errs73 = errors;
      let valid16 = false;
      const _errs74 = errors;
      if (typeof data14 !== "string") {
        const err42 = { instancePath: instancePath + "/net", schemaPath: "#/properties/net/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err42];
        } else {
          vErrors.push(err42);
        }
        errors++;
      }
      var _valid8 = _errs74 === errors;
      valid16 = valid16 || _valid8;
      const _errs76 = errors;
      if (data14 !== null) {
        const err43 = { instancePath: instancePath + "/net", schemaPath: "#/properties/net/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err43];
        } else {
          vErrors.push(err43);
        }
        errors++;
      }
      var _valid8 = _errs76 === errors;
      valid16 = valid16 || _valid8;
      if (!valid16) {
        const err44 = { instancePath: instancePath + "/net", schemaPath: "#/properties/net/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err44];
        } else {
          vErrors.push(err44);
        }
        errors++;
      } else {
        errors = _errs73;
        if (vErrors !== null) {
          if (_errs73) {
            vErrors.length = _errs73;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.solder_mask_expansion_mils !== void 0) {
      let data15 = data.solder_mask_expansion_mils;
      const _errs79 = errors;
      let valid17 = false;
      const _errs80 = errors;
      if (!(typeof data15 == "number")) {
        const err45 = { instancePath: instancePath + "/solder_mask_expansion_mils", schemaPath: "#/properties/solder_mask_expansion_mils/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err45];
        } else {
          vErrors.push(err45);
        }
        errors++;
      }
      var _valid9 = _errs80 === errors;
      valid17 = valid17 || _valid9;
      const _errs82 = errors;
      if (data15 !== null) {
        const err46 = { instancePath: instancePath + "/solder_mask_expansion_mils", schemaPath: "#/properties/solder_mask_expansion_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err46];
        } else {
          vErrors.push(err46);
        }
        errors++;
      }
      var _valid9 = _errs82 === errors;
      valid17 = valid17 || _valid9;
      if (!valid17) {
        const err47 = { instancePath: instancePath + "/solder_mask_expansion_mils", schemaPath: "#/properties/solder_mask_expansion_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err47];
        } else {
          vErrors.push(err47);
        }
        errors++;
      } else {
        errors = _errs79;
        if (vErrors !== null) {
          if (_errs79) {
            vErrors.length = _errs79;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.paste_mask_expansion_mils !== void 0) {
      let data16 = data.paste_mask_expansion_mils;
      const _errs85 = errors;
      let valid18 = false;
      const _errs86 = errors;
      if (!(typeof data16 == "number")) {
        const err48 = { instancePath: instancePath + "/paste_mask_expansion_mils", schemaPath: "#/properties/paste_mask_expansion_mils/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err48];
        } else {
          vErrors.push(err48);
        }
        errors++;
      }
      var _valid10 = _errs86 === errors;
      valid18 = valid18 || _valid10;
      const _errs88 = errors;
      if (data16 !== null) {
        const err49 = { instancePath: instancePath + "/paste_mask_expansion_mils", schemaPath: "#/properties/paste_mask_expansion_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err49];
        } else {
          vErrors.push(err49);
        }
        errors++;
      }
      var _valid10 = _errs88 === errors;
      valid18 = valid18 || _valid10;
      if (!valid18) {
        const err50 = { instancePath: instancePath + "/paste_mask_expansion_mils", schemaPath: "#/properties/paste_mask_expansion_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err50];
        } else {
          vErrors.push(err50);
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
    if (data.tenting_top !== void 0) {
      let data17 = data.tenting_top;
      const _errs91 = errors;
      let valid19 = false;
      const _errs92 = errors;
      if (typeof data17 !== "boolean") {
        const err51 = { instancePath: instancePath + "/tenting_top", schemaPath: "#/properties/tenting_top/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err51];
        } else {
          vErrors.push(err51);
        }
        errors++;
      }
      var _valid11 = _errs92 === errors;
      valid19 = valid19 || _valid11;
      const _errs94 = errors;
      if (data17 !== null) {
        const err52 = { instancePath: instancePath + "/tenting_top", schemaPath: "#/properties/tenting_top/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err52];
        } else {
          vErrors.push(err52);
        }
        errors++;
      }
      var _valid11 = _errs94 === errors;
      valid19 = valid19 || _valid11;
      if (!valid19) {
        const err53 = { instancePath: instancePath + "/tenting_top", schemaPath: "#/properties/tenting_top/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err53];
        } else {
          vErrors.push(err53);
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
    if (data.tenting_bottom !== void 0) {
      let data18 = data.tenting_bottom;
      const _errs97 = errors;
      let valid20 = false;
      const _errs98 = errors;
      if (typeof data18 !== "boolean") {
        const err54 = { instancePath: instancePath + "/tenting_bottom", schemaPath: "#/properties/tenting_bottom/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err54];
        } else {
          vErrors.push(err54);
        }
        errors++;
      }
      var _valid12 = _errs98 === errors;
      valid20 = valid20 || _valid12;
      const _errs100 = errors;
      if (data18 !== null) {
        const err55 = { instancePath: instancePath + "/tenting_bottom", schemaPath: "#/properties/tenting_bottom/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err55];
        } else {
          vErrors.push(err55);
        }
        errors++;
      }
      var _valid12 = _errs100 === errors;
      valid20 = valid20 || _valid12;
      if (!valid20) {
        const err56 = { instancePath: instancePath + "/tenting_bottom", schemaPath: "#/properties/tenting_bottom/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err56];
        } else {
          vErrors.push(err56);
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
    if (data.solder_mask_expansion_mode !== void 0) {
      let data19 = data.solder_mask_expansion_mode;
      const _errs103 = errors;
      let valid21 = false;
      const _errs104 = errors;
      if (!(typeof data19 == "number" && (!(data19 % 1) && !isNaN(data19)))) {
        const err57 = { instancePath: instancePath + "/solder_mask_expansion_mode", schemaPath: "#/properties/solder_mask_expansion_mode/anyOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err57];
        } else {
          vErrors.push(err57);
        }
        errors++;
      }
      var _valid13 = _errs104 === errors;
      valid21 = valid21 || _valid13;
      const _errs106 = errors;
      if (data19 !== null) {
        const err58 = { instancePath: instancePath + "/solder_mask_expansion_mode", schemaPath: "#/properties/solder_mask_expansion_mode/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err58];
        } else {
          vErrors.push(err58);
        }
        errors++;
      }
      var _valid13 = _errs106 === errors;
      valid21 = valid21 || _valid13;
      if (!valid21) {
        const err59 = { instancePath: instancePath + "/solder_mask_expansion_mode", schemaPath: "#/properties/solder_mask_expansion_mode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err59];
        } else {
          vErrors.push(err59);
        }
        errors++;
      } else {
        errors = _errs103;
        if (vErrors !== null) {
          if (_errs103) {
            vErrors.length = _errs103;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.paste_mask_expansion_mode !== void 0) {
      let data20 = data.paste_mask_expansion_mode;
      const _errs109 = errors;
      let valid22 = false;
      const _errs110 = errors;
      if (!(typeof data20 == "number" && (!(data20 % 1) && !isNaN(data20)))) {
        const err60 = { instancePath: instancePath + "/paste_mask_expansion_mode", schemaPath: "#/properties/paste_mask_expansion_mode/anyOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err60];
        } else {
          vErrors.push(err60);
        }
        errors++;
      }
      var _valid14 = _errs110 === errors;
      valid22 = valid22 || _valid14;
      const _errs112 = errors;
      if (data20 !== null) {
        const err61 = { instancePath: instancePath + "/paste_mask_expansion_mode", schemaPath: "#/properties/paste_mask_expansion_mode/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err61];
        } else {
          vErrors.push(err61);
        }
        errors++;
      }
      var _valid14 = _errs112 === errors;
      valid22 = valid22 || _valid14;
      if (!valid22) {
        const err62 = { instancePath: instancePath + "/paste_mask_expansion_mode", schemaPath: "#/properties/paste_mask_expansion_mode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err62];
        } else {
          vErrors.push(err62);
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
  } else {
    const err63 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err63];
    } else {
      vErrors.push(err63);
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("pcbdoc.add_pad" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "pcbdoc.add_pad" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate56(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate56.errors : vErrors.concat(validate56.errors);
        errors = vErrors.length;
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
  validate55.errors = vErrors;
  return errors === 0;
}
validate55.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.outline_points_mils === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "outline_points_mils" }, message: "must have required property 'outline_points_mils'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err3 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.output_file !== void 0) {
      let data1 = data.output_file;
      const _errs9 = errors;
      let valid4 = false;
      const _errs10 = errors;
      if (typeof data1 !== "string") {
        const err5 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      valid4 = valid4 || _valid0;
      const _errs12 = errors;
      if (data1 !== null) {
        const err6 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs12 === errors;
      valid4 = valid4 || _valid0;
      if (!valid4) {
        const err7 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.overwrite !== void 0) {
      let data2 = data.overwrite;
      const _errs15 = errors;
      let valid5 = false;
      const _errs16 = errors;
      if (typeof data2 !== "boolean") {
        const err8 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid1 = _errs16 === errors;
      valid5 = valid5 || _valid1;
      const _errs18 = errors;
      if (data2 !== null) {
        const err9 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid1 = _errs18 === errors;
      valid5 = valid5 || _valid1;
      if (!valid5) {
        const err10 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
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
    if (data.outline_points_mils !== void 0) {
      if (!validate47(data.outline_points_mils, { instancePath: instancePath + "/outline_points_mils", parentData: data, parentDataProperty: "outline_points_mils", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate47.errors : vErrors.concat(validate47.errors);
        errors = vErrors.length;
      }
    }
    if (data.layer !== void 0) {
      let data4 = data.layer;
      const _errs22 = errors;
      let valid6 = false;
      const _errs23 = errors;
      if (typeof data4 !== "string") {
        const err11 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (!(typeof data4 == "number" && (!(data4 % 1) && !isNaN(data4)))) {
        const err12 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid2 = _errs25 === errors;
      valid6 = valid6 || _valid2;
      const _errs27 = errors;
      if (data4 !== null) {
        const err13 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid2 = _errs27 === errors;
      valid6 = valid6 || _valid2;
      if (!valid6) {
        const err14 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
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
    if (data.hole_points_mils !== void 0) {
      let data5 = data.hole_points_mils;
      const _errs30 = errors;
      let valid7 = false;
      const _errs31 = errors;
      if (Array.isArray(data5)) {
        const len0 = data5.length;
        for (let i0 = 0; i0 < len0; i0++) {
          let data6 = data5[i0];
          if (Array.isArray(data6)) {
            const len1 = data6.length;
            for (let i1 = 0; i1 < len1; i1++) {
              let data7 = data6[i1];
              if (Array.isArray(data7)) {
                if (data7.length > 2) {
                  const err15 = { instancePath: instancePath + "/hole_points_mils/" + i0 + "/" + i1, schemaPath: "#/$defs/PointMils/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
                  if (vErrors === null) {
                    vErrors = [err15];
                  } else {
                    vErrors.push(err15);
                  }
                  errors++;
                }
                if (data7.length < 2) {
                  const err16 = { instancePath: instancePath + "/hole_points_mils/" + i0 + "/" + i1, schemaPath: "#/$defs/PointMils/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
                  if (vErrors === null) {
                    vErrors = [err16];
                  } else {
                    vErrors.push(err16);
                  }
                  errors++;
                }
                const len2 = data7.length;
                for (let i2 = 0; i2 < len2; i2++) {
                  if (!(typeof data7[i2] == "number")) {
                    const err17 = { instancePath: instancePath + "/hole_points_mils/" + i0 + "/" + i1 + "/" + i2, schemaPath: "#/$defs/PointMils/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
                    if (vErrors === null) {
                      vErrors = [err17];
                    } else {
                      vErrors.push(err17);
                    }
                    errors++;
                  }
                }
              } else {
                const err18 = { instancePath: instancePath + "/hole_points_mils/" + i0 + "/" + i1, schemaPath: "#/$defs/PointMils/type", keyword: "type", params: { type: "array" }, message: "must be array" };
                if (vErrors === null) {
                  vErrors = [err18];
                } else {
                  vErrors.push(err18);
                }
                errors++;
              }
            }
          } else {
            const err19 = { instancePath: instancePath + "/hole_points_mils/" + i0, schemaPath: "#/properties/hole_points_mils/anyOf/0/items/type", keyword: "type", params: { type: "array" }, message: "must be array" };
            if (vErrors === null) {
              vErrors = [err19];
            } else {
              vErrors.push(err19);
            }
            errors++;
          }
        }
      } else {
        const err20 = { instancePath: instancePath + "/hole_points_mils", schemaPath: "#/properties/hole_points_mils/anyOf/0/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      var _valid3 = _errs31 === errors;
      valid7 = valid7 || _valid3;
      const _errs40 = errors;
      if (data5 !== null) {
        const err21 = { instancePath: instancePath + "/hole_points_mils", schemaPath: "#/properties/hole_points_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      var _valid3 = _errs40 === errors;
      valid7 = valid7 || _valid3;
      if (!valid7) {
        const err22 = { instancePath: instancePath + "/hole_points_mils", schemaPath: "#/properties/hole_points_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
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
    if (data.is_keepout !== void 0) {
      let data9 = data.is_keepout;
      const _errs43 = errors;
      let valid15 = false;
      const _errs44 = errors;
      if (typeof data9 !== "boolean") {
        const err23 = { instancePath: instancePath + "/is_keepout", schemaPath: "#/properties/is_keepout/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      var _valid4 = _errs44 === errors;
      valid15 = valid15 || _valid4;
      const _errs46 = errors;
      if (data9 !== null) {
        const err24 = { instancePath: instancePath + "/is_keepout", schemaPath: "#/properties/is_keepout/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      var _valid4 = _errs46 === errors;
      valid15 = valid15 || _valid4;
      if (!valid15) {
        const err25 = { instancePath: instancePath + "/is_keepout", schemaPath: "#/properties/is_keepout/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
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
    }
    if (data.keepout_restrictions !== void 0) {
      let data10 = data.keepout_restrictions;
      const _errs49 = errors;
      let valid16 = false;
      const _errs50 = errors;
      if (!(typeof data10 == "number")) {
        const err26 = { instancePath: instancePath + "/keepout_restrictions", schemaPath: "#/properties/keepout_restrictions/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
      var _valid5 = _errs50 === errors;
      valid16 = valid16 || _valid5;
      const _errs52 = errors;
      if (data10 !== null) {
        const err27 = { instancePath: instancePath + "/keepout_restrictions", schemaPath: "#/properties/keepout_restrictions/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
      var _valid5 = _errs52 === errors;
      valid16 = valid16 || _valid5;
      if (!valid16) {
        const err28 = { instancePath: instancePath + "/keepout_restrictions", schemaPath: "#/properties/keepout_restrictions/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      } else {
        errors = _errs49;
        if (vErrors !== null) {
          if (_errs49) {
            vErrors.length = _errs49;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.net !== void 0) {
      let data11 = data.net;
      const _errs55 = errors;
      let valid17 = false;
      const _errs56 = errors;
      if (typeof data11 !== "string") {
        const err29 = { instancePath: instancePath + "/net", schemaPath: "#/properties/net/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      }
      var _valid6 = _errs56 === errors;
      valid17 = valid17 || _valid6;
      const _errs58 = errors;
      if (data11 !== null) {
        const err30 = { instancePath: instancePath + "/net", schemaPath: "#/properties/net/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
        }
        errors++;
      }
      var _valid6 = _errs58 === errors;
      valid17 = valid17 || _valid6;
      if (!valid17) {
        const err31 = { instancePath: instancePath + "/net", schemaPath: "#/properties/net/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
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
    if (data.is_board_cutout !== void 0) {
      let data12 = data.is_board_cutout;
      const _errs61 = errors;
      let valid18 = false;
      const _errs62 = errors;
      if (typeof data12 !== "boolean") {
        const err32 = { instancePath: instancePath + "/is_board_cutout", schemaPath: "#/properties/is_board_cutout/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
        }
        errors++;
      }
      var _valid7 = _errs62 === errors;
      valid18 = valid18 || _valid7;
      const _errs64 = errors;
      if (data12 !== null) {
        const err33 = { instancePath: instancePath + "/is_board_cutout", schemaPath: "#/properties/is_board_cutout/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
      var _valid7 = _errs64 === errors;
      valid18 = valid18 || _valid7;
      if (!valid18) {
        const err34 = { instancePath: instancePath + "/is_board_cutout", schemaPath: "#/properties/is_board_cutout/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
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
  } else {
    const err35 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err35];
    } else {
      vErrors.push(err35);
    }
    errors++;
  }
  validate60.errors = vErrors;
  return errors === 0;
}
validate60.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate59(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate59.evaluated;
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("pcbdoc.add_region" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "pcbdoc.add_region" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate60(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate60.errors : vErrors.concat(validate60.errors);
        errors = vErrors.length;
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
  validate59.errors = vErrors;
  return errors === 0;
}
validate59.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.text === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "text" }, message: "must have required property 'text'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.position_mils === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "position_mils" }, message: "must have required property 'position_mils'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.height_mils === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "height_mils" }, message: "must have required property 'height_mils'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err5 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err5];
          } else {
            vErrors.push(err5);
          }
          errors++;
        }
      } else {
        const err6 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.output_file !== void 0) {
      let data1 = data.output_file;
      const _errs9 = errors;
      let valid4 = false;
      const _errs10 = errors;
      if (typeof data1 !== "string") {
        const err7 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      valid4 = valid4 || _valid0;
      const _errs12 = errors;
      if (data1 !== null) {
        const err8 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid0 = _errs12 === errors;
      valid4 = valid4 || _valid0;
      if (!valid4) {
        const err9 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
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
    if (data.overwrite !== void 0) {
      let data2 = data.overwrite;
      const _errs15 = errors;
      let valid5 = false;
      const _errs16 = errors;
      if (typeof data2 !== "boolean") {
        const err10 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid1 = _errs16 === errors;
      valid5 = valid5 || _valid1;
      const _errs18 = errors;
      if (data2 !== null) {
        const err11 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid1 = _errs18 === errors;
      valid5 = valid5 || _valid1;
      if (!valid5) {
        const err12 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.text !== void 0) {
      let data3 = data.text;
      if (typeof data3 === "string") {
        if (func1(data3) < 1) {
          const err13 = { instancePath: instancePath + "/text", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err13];
          } else {
            vErrors.push(err13);
          }
          errors++;
        }
      } else {
        const err14 = { instancePath: instancePath + "/text", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
    }
    if (data.position_mils !== void 0) {
      let data4 = data.position_mils;
      if (Array.isArray(data4)) {
        if (data4.length > 2) {
          const err15 = { instancePath: instancePath + "/position_mils", schemaPath: "#/$defs/PointMils/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err15];
          } else {
            vErrors.push(err15);
          }
          errors++;
        }
        if (data4.length < 2) {
          const err16 = { instancePath: instancePath + "/position_mils", schemaPath: "#/$defs/PointMils/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err16];
          } else {
            vErrors.push(err16);
          }
          errors++;
        }
        const len0 = data4.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!(typeof data4[i0] == "number")) {
            const err17 = { instancePath: instancePath + "/position_mils/" + i0, schemaPath: "#/$defs/PointMils/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err17];
            } else {
              vErrors.push(err17);
            }
            errors++;
          }
        }
      } else {
        const err18 = { instancePath: instancePath + "/position_mils", schemaPath: "#/$defs/PointMils/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
    }
    if (data.layer !== void 0) {
      let data6 = data.layer;
      const _errs29 = errors;
      let valid10 = false;
      const _errs30 = errors;
      if (typeof data6 !== "string") {
        const err19 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
      var _valid2 = _errs30 === errors;
      valid10 = valid10 || _valid2;
      const _errs32 = errors;
      if (!(typeof data6 == "number" && (!(data6 % 1) && !isNaN(data6)))) {
        const err20 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      var _valid2 = _errs32 === errors;
      valid10 = valid10 || _valid2;
      const _errs34 = errors;
      if (data6 !== null) {
        const err21 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      var _valid2 = _errs34 === errors;
      valid10 = valid10 || _valid2;
      if (!valid10) {
        const err22 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.height_mils !== void 0) {
      if (!(typeof data.height_mils == "number")) {
        const err23 = { instancePath: instancePath + "/height_mils", schemaPath: "#/properties/height_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
    }
    if (data.font_kind !== void 0) {
      let data8 = data.font_kind;
      const _errs39 = errors;
      let valid11 = false;
      const _errs40 = errors;
      if (typeof data8 !== "string") {
        const err24 = { instancePath: instancePath + "/font_kind", schemaPath: "#/properties/font_kind/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      var _valid3 = _errs40 === errors;
      valid11 = valid11 || _valid3;
      const _errs42 = errors;
      if (data8 !== null) {
        const err25 = { instancePath: instancePath + "/font_kind", schemaPath: "#/properties/font_kind/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
      var _valid3 = _errs42 === errors;
      valid11 = valid11 || _valid3;
      if (!valid11) {
        const err26 = { instancePath: instancePath + "/font_kind", schemaPath: "#/properties/font_kind/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
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
    if (data.font_name !== void 0) {
      let data9 = data.font_name;
      const _errs45 = errors;
      let valid12 = false;
      const _errs46 = errors;
      if (typeof data9 !== "string") {
        const err27 = { instancePath: instancePath + "/font_name", schemaPath: "#/properties/font_name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
      var _valid4 = _errs46 === errors;
      valid12 = valid12 || _valid4;
      const _errs48 = errors;
      if (data9 !== null) {
        const err28 = { instancePath: instancePath + "/font_name", schemaPath: "#/properties/font_name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
      var _valid4 = _errs48 === errors;
      valid12 = valid12 || _valid4;
      if (!valid12) {
        const err29 = { instancePath: instancePath + "/font_name", schemaPath: "#/properties/font_name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
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
    if (data.bold !== void 0) {
      let data10 = data.bold;
      const _errs51 = errors;
      let valid13 = false;
      const _errs52 = errors;
      if (typeof data10 !== "boolean") {
        const err30 = { instancePath: instancePath + "/bold", schemaPath: "#/properties/bold/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
        }
        errors++;
      }
      var _valid5 = _errs52 === errors;
      valid13 = valid13 || _valid5;
      const _errs54 = errors;
      if (data10 !== null) {
        const err31 = { instancePath: instancePath + "/bold", schemaPath: "#/properties/bold/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      }
      var _valid5 = _errs54 === errors;
      valid13 = valid13 || _valid5;
      if (!valid13) {
        const err32 = { instancePath: instancePath + "/bold", schemaPath: "#/properties/bold/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
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
    if (data.italic !== void 0) {
      let data11 = data.italic;
      const _errs57 = errors;
      let valid14 = false;
      const _errs58 = errors;
      if (typeof data11 !== "boolean") {
        const err33 = { instancePath: instancePath + "/italic", schemaPath: "#/properties/italic/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
      var _valid6 = _errs58 === errors;
      valid14 = valid14 || _valid6;
      const _errs60 = errors;
      if (data11 !== null) {
        const err34 = { instancePath: instancePath + "/italic", schemaPath: "#/properties/italic/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
        }
        errors++;
      }
      var _valid6 = _errs60 === errors;
      valid14 = valid14 || _valid6;
      if (!valid14) {
        const err35 = { instancePath: instancePath + "/italic", schemaPath: "#/properties/italic/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err35];
        } else {
          vErrors.push(err35);
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
    if (data.rotation_degrees !== void 0) {
      let data12 = data.rotation_degrees;
      const _errs63 = errors;
      let valid15 = false;
      const _errs64 = errors;
      if (!(typeof data12 == "number")) {
        const err36 = { instancePath: instancePath + "/rotation_degrees", schemaPath: "#/properties/rotation_degrees/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err36];
        } else {
          vErrors.push(err36);
        }
        errors++;
      }
      var _valid7 = _errs64 === errors;
      valid15 = valid15 || _valid7;
      const _errs66 = errors;
      if (data12 !== null) {
        const err37 = { instancePath: instancePath + "/rotation_degrees", schemaPath: "#/properties/rotation_degrees/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err37];
        } else {
          vErrors.push(err37);
        }
        errors++;
      }
      var _valid7 = _errs66 === errors;
      valid15 = valid15 || _valid7;
      if (!valid15) {
        const err38 = { instancePath: instancePath + "/rotation_degrees", schemaPath: "#/properties/rotation_degrees/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err38];
        } else {
          vErrors.push(err38);
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
    if (data.stroke_width_mils !== void 0) {
      let data13 = data.stroke_width_mils;
      const _errs69 = errors;
      let valid16 = false;
      const _errs70 = errors;
      if (!(typeof data13 == "number")) {
        const err39 = { instancePath: instancePath + "/stroke_width_mils", schemaPath: "#/properties/stroke_width_mils/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err39];
        } else {
          vErrors.push(err39);
        }
        errors++;
      }
      var _valid8 = _errs70 === errors;
      valid16 = valid16 || _valid8;
      const _errs72 = errors;
      if (data13 !== null) {
        const err40 = { instancePath: instancePath + "/stroke_width_mils", schemaPath: "#/properties/stroke_width_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err40];
        } else {
          vErrors.push(err40);
        }
        errors++;
      }
      var _valid8 = _errs72 === errors;
      valid16 = valid16 || _valid8;
      if (!valid16) {
        const err41 = { instancePath: instancePath + "/stroke_width_mils", schemaPath: "#/properties/stroke_width_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err41];
        } else {
          vErrors.push(err41);
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
    if (data.is_comment !== void 0) {
      let data14 = data.is_comment;
      const _errs75 = errors;
      let valid17 = false;
      const _errs76 = errors;
      if (typeof data14 !== "boolean") {
        const err42 = { instancePath: instancePath + "/is_comment", schemaPath: "#/properties/is_comment/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err42];
        } else {
          vErrors.push(err42);
        }
        errors++;
      }
      var _valid9 = _errs76 === errors;
      valid17 = valid17 || _valid9;
      const _errs78 = errors;
      if (data14 !== null) {
        const err43 = { instancePath: instancePath + "/is_comment", schemaPath: "#/properties/is_comment/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err43];
        } else {
          vErrors.push(err43);
        }
        errors++;
      }
      var _valid9 = _errs78 === errors;
      valid17 = valid17 || _valid9;
      if (!valid17) {
        const err44 = { instancePath: instancePath + "/is_comment", schemaPath: "#/properties/is_comment/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err44];
        } else {
          vErrors.push(err44);
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
    if (data.is_designator !== void 0) {
      let data15 = data.is_designator;
      const _errs81 = errors;
      let valid18 = false;
      const _errs82 = errors;
      if (typeof data15 !== "boolean") {
        const err45 = { instancePath: instancePath + "/is_designator", schemaPath: "#/properties/is_designator/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err45];
        } else {
          vErrors.push(err45);
        }
        errors++;
      }
      var _valid10 = _errs82 === errors;
      valid18 = valid18 || _valid10;
      const _errs84 = errors;
      if (data15 !== null) {
        const err46 = { instancePath: instancePath + "/is_designator", schemaPath: "#/properties/is_designator/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err46];
        } else {
          vErrors.push(err46);
        }
        errors++;
      }
      var _valid10 = _errs84 === errors;
      valid18 = valid18 || _valid10;
      if (!valid18) {
        const err47 = { instancePath: instancePath + "/is_designator", schemaPath: "#/properties/is_designator/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err47];
        } else {
          vErrors.push(err47);
        }
        errors++;
      } else {
        errors = _errs81;
        if (vErrors !== null) {
          if (_errs81) {
            vErrors.length = _errs81;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.is_mirrored !== void 0) {
      let data16 = data.is_mirrored;
      const _errs87 = errors;
      let valid19 = false;
      const _errs88 = errors;
      if (typeof data16 !== "boolean") {
        const err48 = { instancePath: instancePath + "/is_mirrored", schemaPath: "#/properties/is_mirrored/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err48];
        } else {
          vErrors.push(err48);
        }
        errors++;
      }
      var _valid11 = _errs88 === errors;
      valid19 = valid19 || _valid11;
      const _errs90 = errors;
      if (data16 !== null) {
        const err49 = { instancePath: instancePath + "/is_mirrored", schemaPath: "#/properties/is_mirrored/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err49];
        } else {
          vErrors.push(err49);
        }
        errors++;
      }
      var _valid11 = _errs90 === errors;
      valid19 = valid19 || _valid11;
      if (!valid19) {
        const err50 = { instancePath: instancePath + "/is_mirrored", schemaPath: "#/properties/is_mirrored/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err50];
        } else {
          vErrors.push(err50);
        }
        errors++;
      } else {
        errors = _errs87;
        if (vErrors !== null) {
          if (_errs87) {
            vErrors.length = _errs87;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.is_inverted !== void 0) {
      let data17 = data.is_inverted;
      const _errs93 = errors;
      let valid20 = false;
      const _errs94 = errors;
      if (typeof data17 !== "boolean") {
        const err51 = { instancePath: instancePath + "/is_inverted", schemaPath: "#/properties/is_inverted/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err51];
        } else {
          vErrors.push(err51);
        }
        errors++;
      }
      var _valid12 = _errs94 === errors;
      valid20 = valid20 || _valid12;
      const _errs96 = errors;
      if (data17 !== null) {
        const err52 = { instancePath: instancePath + "/is_inverted", schemaPath: "#/properties/is_inverted/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err52];
        } else {
          vErrors.push(err52);
        }
        errors++;
      }
      var _valid12 = _errs96 === errors;
      valid20 = valid20 || _valid12;
      if (!valid20) {
        const err53 = { instancePath: instancePath + "/is_inverted", schemaPath: "#/properties/is_inverted/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err53];
        } else {
          vErrors.push(err53);
        }
        errors++;
      } else {
        errors = _errs93;
        if (vErrors !== null) {
          if (_errs93) {
            vErrors.length = _errs93;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.inverted_margin_mils !== void 0) {
      let data18 = data.inverted_margin_mils;
      const _errs99 = errors;
      let valid21 = false;
      const _errs100 = errors;
      if (!(typeof data18 == "number")) {
        const err54 = { instancePath: instancePath + "/inverted_margin_mils", schemaPath: "#/properties/inverted_margin_mils/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err54];
        } else {
          vErrors.push(err54);
        }
        errors++;
      }
      var _valid13 = _errs100 === errors;
      valid21 = valid21 || _valid13;
      const _errs102 = errors;
      if (data18 !== null) {
        const err55 = { instancePath: instancePath + "/inverted_margin_mils", schemaPath: "#/properties/inverted_margin_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err55];
        } else {
          vErrors.push(err55);
        }
        errors++;
      }
      var _valid13 = _errs102 === errors;
      valid21 = valid21 || _valid13;
      if (!valid21) {
        const err56 = { instancePath: instancePath + "/inverted_margin_mils", schemaPath: "#/properties/inverted_margin_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err56];
        } else {
          vErrors.push(err56);
        }
        errors++;
      } else {
        errors = _errs99;
        if (vErrors !== null) {
          if (_errs99) {
            vErrors.length = _errs99;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.use_inverted_rectangle !== void 0) {
      let data19 = data.use_inverted_rectangle;
      const _errs105 = errors;
      let valid22 = false;
      const _errs106 = errors;
      if (typeof data19 !== "boolean") {
        const err57 = { instancePath: instancePath + "/use_inverted_rectangle", schemaPath: "#/properties/use_inverted_rectangle/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err57];
        } else {
          vErrors.push(err57);
        }
        errors++;
      }
      var _valid14 = _errs106 === errors;
      valid22 = valid22 || _valid14;
      const _errs108 = errors;
      if (data19 !== null) {
        const err58 = { instancePath: instancePath + "/use_inverted_rectangle", schemaPath: "#/properties/use_inverted_rectangle/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err58];
        } else {
          vErrors.push(err58);
        }
        errors++;
      }
      var _valid14 = _errs108 === errors;
      valid22 = valid22 || _valid14;
      if (!valid22) {
        const err59 = { instancePath: instancePath + "/use_inverted_rectangle", schemaPath: "#/properties/use_inverted_rectangle/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err59];
        } else {
          vErrors.push(err59);
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
    if (data.inverted_rectangle_size_mils !== void 0) {
      let data20 = data.inverted_rectangle_size_mils;
      const _errs111 = errors;
      let valid23 = false;
      const _errs112 = errors;
      if (Array.isArray(data20)) {
        if (data20.length > 2) {
          const err60 = { instancePath: instancePath + "/inverted_rectangle_size_mils", schemaPath: "#/$defs/PointMils/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err60];
          } else {
            vErrors.push(err60);
          }
          errors++;
        }
        if (data20.length < 2) {
          const err61 = { instancePath: instancePath + "/inverted_rectangle_size_mils", schemaPath: "#/$defs/PointMils/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err61];
          } else {
            vErrors.push(err61);
          }
          errors++;
        }
        const len1 = data20.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (!(typeof data20[i1] == "number")) {
            const err62 = { instancePath: instancePath + "/inverted_rectangle_size_mils/" + i1, schemaPath: "#/$defs/PointMils/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err62];
            } else {
              vErrors.push(err62);
            }
            errors++;
          }
        }
      } else {
        const err63 = { instancePath: instancePath + "/inverted_rectangle_size_mils", schemaPath: "#/$defs/PointMils/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err63];
        } else {
          vErrors.push(err63);
        }
        errors++;
      }
      var _valid15 = _errs112 === errors;
      valid23 = valid23 || _valid15;
      const _errs117 = errors;
      if (data20 !== null) {
        const err64 = { instancePath: instancePath + "/inverted_rectangle_size_mils", schemaPath: "#/properties/inverted_rectangle_size_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err64];
        } else {
          vErrors.push(err64);
        }
        errors++;
      }
      var _valid15 = _errs117 === errors;
      valid23 = valid23 || _valid15;
      if (!valid23) {
        const err65 = { instancePath: instancePath + "/inverted_rectangle_size_mils", schemaPath: "#/properties/inverted_rectangle_size_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err65];
        } else {
          vErrors.push(err65);
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
    }
    if (data.is_frame !== void 0) {
      let data22 = data.is_frame;
      const _errs120 = errors;
      let valid27 = false;
      const _errs121 = errors;
      if (typeof data22 !== "boolean") {
        const err66 = { instancePath: instancePath + "/is_frame", schemaPath: "#/properties/is_frame/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err66];
        } else {
          vErrors.push(err66);
        }
        errors++;
      }
      var _valid16 = _errs121 === errors;
      valid27 = valid27 || _valid16;
      const _errs123 = errors;
      if (data22 !== null) {
        const err67 = { instancePath: instancePath + "/is_frame", schemaPath: "#/properties/is_frame/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err67];
        } else {
          vErrors.push(err67);
        }
        errors++;
      }
      var _valid16 = _errs123 === errors;
      valid27 = valid27 || _valid16;
      if (!valid27) {
        const err68 = { instancePath: instancePath + "/is_frame", schemaPath: "#/properties/is_frame/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err68];
        } else {
          vErrors.push(err68);
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
    if (data.frame_size_mils !== void 0) {
      let data23 = data.frame_size_mils;
      const _errs126 = errors;
      let valid28 = false;
      const _errs127 = errors;
      if (Array.isArray(data23)) {
        if (data23.length > 2) {
          const err69 = { instancePath: instancePath + "/frame_size_mils", schemaPath: "#/$defs/PointMils/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err69];
          } else {
            vErrors.push(err69);
          }
          errors++;
        }
        if (data23.length < 2) {
          const err70 = { instancePath: instancePath + "/frame_size_mils", schemaPath: "#/$defs/PointMils/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err70];
          } else {
            vErrors.push(err70);
          }
          errors++;
        }
        const len2 = data23.length;
        for (let i2 = 0; i2 < len2; i2++) {
          if (!(typeof data23[i2] == "number")) {
            const err71 = { instancePath: instancePath + "/frame_size_mils/" + i2, schemaPath: "#/$defs/PointMils/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err71];
            } else {
              vErrors.push(err71);
            }
            errors++;
          }
        }
      } else {
        const err72 = { instancePath: instancePath + "/frame_size_mils", schemaPath: "#/$defs/PointMils/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err72];
        } else {
          vErrors.push(err72);
        }
        errors++;
      }
      var _valid17 = _errs127 === errors;
      valid28 = valid28 || _valid17;
      const _errs132 = errors;
      if (data23 !== null) {
        const err73 = { instancePath: instancePath + "/frame_size_mils", schemaPath: "#/properties/frame_size_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err73];
        } else {
          vErrors.push(err73);
        }
        errors++;
      }
      var _valid17 = _errs132 === errors;
      valid28 = valid28 || _valid17;
      if (!valid28) {
        const err74 = { instancePath: instancePath + "/frame_size_mils", schemaPath: "#/properties/frame_size_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err74];
        } else {
          vErrors.push(err74);
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
    if (data.barcode_full_size_mils !== void 0) {
      let data25 = data.barcode_full_size_mils;
      const _errs135 = errors;
      let valid32 = false;
      const _errs136 = errors;
      if (Array.isArray(data25)) {
        if (data25.length > 2) {
          const err75 = { instancePath: instancePath + "/barcode_full_size_mils", schemaPath: "#/$defs/PointMils/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err75];
          } else {
            vErrors.push(err75);
          }
          errors++;
        }
        if (data25.length < 2) {
          const err76 = { instancePath: instancePath + "/barcode_full_size_mils", schemaPath: "#/$defs/PointMils/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err76];
          } else {
            vErrors.push(err76);
          }
          errors++;
        }
        const len3 = data25.length;
        for (let i3 = 0; i3 < len3; i3++) {
          if (!(typeof data25[i3] == "number")) {
            const err77 = { instancePath: instancePath + "/barcode_full_size_mils/" + i3, schemaPath: "#/$defs/PointMils/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err77];
            } else {
              vErrors.push(err77);
            }
            errors++;
          }
        }
      } else {
        const err78 = { instancePath: instancePath + "/barcode_full_size_mils", schemaPath: "#/$defs/PointMils/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err78];
        } else {
          vErrors.push(err78);
        }
        errors++;
      }
      var _valid18 = _errs136 === errors;
      valid32 = valid32 || _valid18;
      const _errs141 = errors;
      if (data25 !== null) {
        const err79 = { instancePath: instancePath + "/barcode_full_size_mils", schemaPath: "#/properties/barcode_full_size_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err79];
        } else {
          vErrors.push(err79);
        }
        errors++;
      }
      var _valid18 = _errs141 === errors;
      valid32 = valid32 || _valid18;
      if (!valid32) {
        const err80 = { instancePath: instancePath + "/barcode_full_size_mils", schemaPath: "#/properties/barcode_full_size_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err80];
        } else {
          vErrors.push(err80);
        }
        errors++;
      } else {
        errors = _errs135;
        if (vErrors !== null) {
          if (_errs135) {
            vErrors.length = _errs135;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.barcode_margin_mils !== void 0) {
      let data27 = data.barcode_margin_mils;
      const _errs144 = errors;
      let valid36 = false;
      const _errs145 = errors;
      if (Array.isArray(data27)) {
        if (data27.length > 2) {
          const err81 = { instancePath: instancePath + "/barcode_margin_mils", schemaPath: "#/$defs/PointMils/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err81];
          } else {
            vErrors.push(err81);
          }
          errors++;
        }
        if (data27.length < 2) {
          const err82 = { instancePath: instancePath + "/barcode_margin_mils", schemaPath: "#/$defs/PointMils/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err82];
          } else {
            vErrors.push(err82);
          }
          errors++;
        }
        const len4 = data27.length;
        for (let i4 = 0; i4 < len4; i4++) {
          if (!(typeof data27[i4] == "number")) {
            const err83 = { instancePath: instancePath + "/barcode_margin_mils/" + i4, schemaPath: "#/$defs/PointMils/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err83];
            } else {
              vErrors.push(err83);
            }
            errors++;
          }
        }
      } else {
        const err84 = { instancePath: instancePath + "/barcode_margin_mils", schemaPath: "#/$defs/PointMils/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err84];
        } else {
          vErrors.push(err84);
        }
        errors++;
      }
      var _valid19 = _errs145 === errors;
      valid36 = valid36 || _valid19;
      const _errs150 = errors;
      if (data27 !== null) {
        const err85 = { instancePath: instancePath + "/barcode_margin_mils", schemaPath: "#/properties/barcode_margin_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err85];
        } else {
          vErrors.push(err85);
        }
        errors++;
      }
      var _valid19 = _errs150 === errors;
      valid36 = valid36 || _valid19;
      if (!valid36) {
        const err86 = { instancePath: instancePath + "/barcode_margin_mils", schemaPath: "#/properties/barcode_margin_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err86];
        } else {
          vErrors.push(err86);
        }
        errors++;
      } else {
        errors = _errs144;
        if (vErrors !== null) {
          if (_errs144) {
            vErrors.length = _errs144;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.barcode_min_width_mils !== void 0) {
      let data29 = data.barcode_min_width_mils;
      const _errs153 = errors;
      let valid40 = false;
      const _errs154 = errors;
      if (!(typeof data29 == "number")) {
        const err87 = { instancePath: instancePath + "/barcode_min_width_mils", schemaPath: "#/properties/barcode_min_width_mils/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err87];
        } else {
          vErrors.push(err87);
        }
        errors++;
      }
      var _valid20 = _errs154 === errors;
      valid40 = valid40 || _valid20;
      const _errs156 = errors;
      if (data29 !== null) {
        const err88 = { instancePath: instancePath + "/barcode_min_width_mils", schemaPath: "#/properties/barcode_min_width_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err88];
        } else {
          vErrors.push(err88);
        }
        errors++;
      }
      var _valid20 = _errs156 === errors;
      valid40 = valid40 || _valid20;
      if (!valid40) {
        const err89 = { instancePath: instancePath + "/barcode_min_width_mils", schemaPath: "#/properties/barcode_min_width_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err89];
        } else {
          vErrors.push(err89);
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
    if (data.barcode_show_text !== void 0) {
      let data30 = data.barcode_show_text;
      const _errs159 = errors;
      let valid41 = false;
      const _errs160 = errors;
      if (typeof data30 !== "boolean") {
        const err90 = { instancePath: instancePath + "/barcode_show_text", schemaPath: "#/properties/barcode_show_text/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err90];
        } else {
          vErrors.push(err90);
        }
        errors++;
      }
      var _valid21 = _errs160 === errors;
      valid41 = valid41 || _valid21;
      const _errs162 = errors;
      if (data30 !== null) {
        const err91 = { instancePath: instancePath + "/barcode_show_text", schemaPath: "#/properties/barcode_show_text/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err91];
        } else {
          vErrors.push(err91);
        }
        errors++;
      }
      var _valid21 = _errs162 === errors;
      valid41 = valid41 || _valid21;
      if (!valid41) {
        const err92 = { instancePath: instancePath + "/barcode_show_text", schemaPath: "#/properties/barcode_show_text/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err92];
        } else {
          vErrors.push(err92);
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
    if (data.barcode_inverted !== void 0) {
      let data31 = data.barcode_inverted;
      const _errs165 = errors;
      let valid42 = false;
      const _errs166 = errors;
      if (typeof data31 !== "boolean") {
        const err93 = { instancePath: instancePath + "/barcode_inverted", schemaPath: "#/properties/barcode_inverted/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err93];
        } else {
          vErrors.push(err93);
        }
        errors++;
      }
      var _valid22 = _errs166 === errors;
      valid42 = valid42 || _valid22;
      const _errs168 = errors;
      if (data31 !== null) {
        const err94 = { instancePath: instancePath + "/barcode_inverted", schemaPath: "#/properties/barcode_inverted/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err94];
        } else {
          vErrors.push(err94);
        }
        errors++;
      }
      var _valid22 = _errs168 === errors;
      valid42 = valid42 || _valid22;
      if (!valid42) {
        const err95 = { instancePath: instancePath + "/barcode_inverted", schemaPath: "#/properties/barcode_inverted/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err95];
        } else {
          vErrors.push(err95);
        }
        errors++;
      } else {
        errors = _errs165;
        if (vErrors !== null) {
          if (_errs165) {
            vErrors.length = _errs165;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.text_justification !== void 0) {
      let data32 = data.text_justification;
      const _errs171 = errors;
      let valid43 = false;
      const _errs172 = errors;
      if (typeof data32 !== "string") {
        const err96 = { instancePath: instancePath + "/text_justification", schemaPath: "#/properties/text_justification/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err96];
        } else {
          vErrors.push(err96);
        }
        errors++;
      }
      var _valid23 = _errs172 === errors;
      valid43 = valid43 || _valid23;
      const _errs174 = errors;
      if (!(typeof data32 == "number" && (!(data32 % 1) && !isNaN(data32)))) {
        const err97 = { instancePath: instancePath + "/text_justification", schemaPath: "#/properties/text_justification/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err97];
        } else {
          vErrors.push(err97);
        }
        errors++;
      }
      var _valid23 = _errs174 === errors;
      valid43 = valid43 || _valid23;
      const _errs176 = errors;
      if (data32 !== null) {
        const err98 = { instancePath: instancePath + "/text_justification", schemaPath: "#/properties/text_justification/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err98];
        } else {
          vErrors.push(err98);
        }
        errors++;
      }
      var _valid23 = _errs176 === errors;
      valid43 = valid43 || _valid23;
      if (!valid43) {
        const err99 = { instancePath: instancePath + "/text_justification", schemaPath: "#/properties/text_justification/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err99];
        } else {
          vErrors.push(err99);
        }
        errors++;
      } else {
        errors = _errs171;
        if (vErrors !== null) {
          if (_errs171) {
            vErrors.length = _errs171;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.barcode_kind !== void 0) {
      let data33 = data.barcode_kind;
      const _errs179 = errors;
      let valid44 = false;
      const _errs180 = errors;
      if (typeof data33 !== "string") {
        const err100 = { instancePath: instancePath + "/barcode_kind", schemaPath: "#/properties/barcode_kind/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err100];
        } else {
          vErrors.push(err100);
        }
        errors++;
      }
      var _valid24 = _errs180 === errors;
      valid44 = valid44 || _valid24;
      const _errs182 = errors;
      if (!(typeof data33 == "number" && (!(data33 % 1) && !isNaN(data33)))) {
        const err101 = { instancePath: instancePath + "/barcode_kind", schemaPath: "#/properties/barcode_kind/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err101];
        } else {
          vErrors.push(err101);
        }
        errors++;
      }
      var _valid24 = _errs182 === errors;
      valid44 = valid44 || _valid24;
      const _errs184 = errors;
      if (data33 !== null) {
        const err102 = { instancePath: instancePath + "/barcode_kind", schemaPath: "#/properties/barcode_kind/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err102];
        } else {
          vErrors.push(err102);
        }
        errors++;
      }
      var _valid24 = _errs184 === errors;
      valid44 = valid44 || _valid24;
      if (!valid44) {
        const err103 = { instancePath: instancePath + "/barcode_kind", schemaPath: "#/properties/barcode_kind/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err103];
        } else {
          vErrors.push(err103);
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
    if (data.barcode_render_mode !== void 0) {
      let data34 = data.barcode_render_mode;
      const _errs187 = errors;
      let valid45 = false;
      const _errs188 = errors;
      if (typeof data34 !== "string") {
        const err104 = { instancePath: instancePath + "/barcode_render_mode", schemaPath: "#/properties/barcode_render_mode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err104];
        } else {
          vErrors.push(err104);
        }
        errors++;
      }
      var _valid25 = _errs188 === errors;
      valid45 = valid45 || _valid25;
      const _errs190 = errors;
      if (!(typeof data34 == "number" && (!(data34 % 1) && !isNaN(data34)))) {
        const err105 = { instancePath: instancePath + "/barcode_render_mode", schemaPath: "#/properties/barcode_render_mode/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err105];
        } else {
          vErrors.push(err105);
        }
        errors++;
      }
      var _valid25 = _errs190 === errors;
      valid45 = valid45 || _valid25;
      const _errs192 = errors;
      if (data34 !== null) {
        const err106 = { instancePath: instancePath + "/barcode_render_mode", schemaPath: "#/properties/barcode_render_mode/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err106];
        } else {
          vErrors.push(err106);
        }
        errors++;
      }
      var _valid25 = _errs192 === errors;
      valid45 = valid45 || _valid25;
      if (!valid45) {
        const err107 = { instancePath: instancePath + "/barcode_render_mode", schemaPath: "#/properties/barcode_render_mode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err107];
        } else {
          vErrors.push(err107);
        }
        errors++;
      } else {
        errors = _errs187;
        if (vErrors !== null) {
          if (_errs187) {
            vErrors.length = _errs187;
          } else {
            vErrors = null;
          }
        }
      }
    }
  } else {
    const err108 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err108];
    } else {
      vErrors.push(err108);
    }
    errors++;
  }
  validate65.errors = vErrors;
  return errors === 0;
}
validate65.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate64(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate64.evaluated;
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("pcbdoc.add_text" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "pcbdoc.add_text" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate65(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate65.errors : vErrors.concat(validate65.errors);
        errors = vErrors.length;
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
  validate64.errors = vErrors;
  return errors === 0;
}
validate64.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.start_mils === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "start_mils" }, message: "must have required property 'start_mils'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.end_mils === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "end_mils" }, message: "must have required property 'end_mils'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.width_mils === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "width_mils" }, message: "must have required property 'width_mils'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err5 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err5];
          } else {
            vErrors.push(err5);
          }
          errors++;
        }
      } else {
        const err6 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.output_file !== void 0) {
      let data1 = data.output_file;
      const _errs9 = errors;
      let valid4 = false;
      const _errs10 = errors;
      if (typeof data1 !== "string") {
        const err7 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      valid4 = valid4 || _valid0;
      const _errs12 = errors;
      if (data1 !== null) {
        const err8 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid0 = _errs12 === errors;
      valid4 = valid4 || _valid0;
      if (!valid4) {
        const err9 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
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
    if (data.overwrite !== void 0) {
      let data2 = data.overwrite;
      const _errs15 = errors;
      let valid5 = false;
      const _errs16 = errors;
      if (typeof data2 !== "boolean") {
        const err10 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid1 = _errs16 === errors;
      valid5 = valid5 || _valid1;
      const _errs18 = errors;
      if (data2 !== null) {
        const err11 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid1 = _errs18 === errors;
      valid5 = valid5 || _valid1;
      if (!valid5) {
        const err12 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.start_mils !== void 0) {
      let data3 = data.start_mils;
      if (Array.isArray(data3)) {
        if (data3.length > 2) {
          const err13 = { instancePath: instancePath + "/start_mils", schemaPath: "#/$defs/PointMils/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err13];
          } else {
            vErrors.push(err13);
          }
          errors++;
        }
        if (data3.length < 2) {
          const err14 = { instancePath: instancePath + "/start_mils", schemaPath: "#/$defs/PointMils/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err14];
          } else {
            vErrors.push(err14);
          }
          errors++;
        }
        const len0 = data3.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!(typeof data3[i0] == "number")) {
            const err15 = { instancePath: instancePath + "/start_mils/" + i0, schemaPath: "#/$defs/PointMils/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err15];
            } else {
              vErrors.push(err15);
            }
            errors++;
          }
        }
      } else {
        const err16 = { instancePath: instancePath + "/start_mils", schemaPath: "#/$defs/PointMils/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
    }
    if (data.end_mils !== void 0) {
      let data5 = data.end_mils;
      if (Array.isArray(data5)) {
        if (data5.length > 2) {
          const err17 = { instancePath: instancePath + "/end_mils", schemaPath: "#/$defs/PointMils/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err17];
          } else {
            vErrors.push(err17);
          }
          errors++;
        }
        if (data5.length < 2) {
          const err18 = { instancePath: instancePath + "/end_mils", schemaPath: "#/$defs/PointMils/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err18];
          } else {
            vErrors.push(err18);
          }
          errors++;
        }
        const len1 = data5.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (!(typeof data5[i1] == "number")) {
            const err19 = { instancePath: instancePath + "/end_mils/" + i1, schemaPath: "#/$defs/PointMils/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err19];
            } else {
              vErrors.push(err19);
            }
            errors++;
          }
        }
      } else {
        const err20 = { instancePath: instancePath + "/end_mils", schemaPath: "#/$defs/PointMils/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
    }
    if (data.width_mils !== void 0) {
      if (!(typeof data.width_mils == "number")) {
        const err21 = { instancePath: instancePath + "/width_mils", schemaPath: "#/properties/width_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
    }
    if (data.layer !== void 0) {
      let data8 = data.layer;
      const _errs33 = errors;
      let valid12 = false;
      const _errs34 = errors;
      if (typeof data8 !== "string") {
        const err22 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
      var _valid2 = _errs34 === errors;
      valid12 = valid12 || _valid2;
      const _errs36 = errors;
      if (!(typeof data8 == "number" && (!(data8 % 1) && !isNaN(data8)))) {
        const err23 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      var _valid2 = _errs36 === errors;
      valid12 = valid12 || _valid2;
      const _errs38 = errors;
      if (data8 !== null) {
        const err24 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      var _valid2 = _errs38 === errors;
      valid12 = valid12 || _valid2;
      if (!valid12) {
        const err25 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    }
    if (data.net !== void 0) {
      let data9 = data.net;
      const _errs41 = errors;
      let valid13 = false;
      const _errs42 = errors;
      if (typeof data9 !== "string") {
        const err26 = { instancePath: instancePath + "/net", schemaPath: "#/properties/net/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
      var _valid3 = _errs42 === errors;
      valid13 = valid13 || _valid3;
      const _errs44 = errors;
      if (data9 !== null) {
        const err27 = { instancePath: instancePath + "/net", schemaPath: "#/properties/net/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
      var _valid3 = _errs44 === errors;
      valid13 = valid13 || _valid3;
      if (!valid13) {
        const err28 = { instancePath: instancePath + "/net", schemaPath: "#/properties/net/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
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
  } else {
    const err29 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err29];
    } else {
      vErrors.push(err29);
    }
    errors++;
  }
  validate69.errors = vErrors;
  return errors === 0;
}
validate69.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate68(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate68.evaluated;
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("pcbdoc.add_track" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "pcbdoc.add_track" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate69(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate69.errors : vErrors.concat(validate69.errors);
        errors = vErrors.length;
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
  validate68.errors = vErrors;
  return errors === 0;
}
validate68.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.position_mils === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "position_mils" }, message: "must have required property 'position_mils'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.diameter_mils === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "diameter_mils" }, message: "must have required property 'diameter_mils'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.hole_size_mils === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "hole_size_mils" }, message: "must have required property 'hole_size_mils'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err5 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err5];
          } else {
            vErrors.push(err5);
          }
          errors++;
        }
      } else {
        const err6 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.output_file !== void 0) {
      let data1 = data.output_file;
      const _errs9 = errors;
      let valid4 = false;
      const _errs10 = errors;
      if (typeof data1 !== "string") {
        const err7 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      valid4 = valid4 || _valid0;
      const _errs12 = errors;
      if (data1 !== null) {
        const err8 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid0 = _errs12 === errors;
      valid4 = valid4 || _valid0;
      if (!valid4) {
        const err9 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
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
    if (data.overwrite !== void 0) {
      let data2 = data.overwrite;
      const _errs15 = errors;
      let valid5 = false;
      const _errs16 = errors;
      if (typeof data2 !== "boolean") {
        const err10 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid1 = _errs16 === errors;
      valid5 = valid5 || _valid1;
      const _errs18 = errors;
      if (data2 !== null) {
        const err11 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid1 = _errs18 === errors;
      valid5 = valid5 || _valid1;
      if (!valid5) {
        const err12 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.position_mils !== void 0) {
      let data3 = data.position_mils;
      if (Array.isArray(data3)) {
        if (data3.length > 2) {
          const err13 = { instancePath: instancePath + "/position_mils", schemaPath: "#/$defs/PointMils/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err13];
          } else {
            vErrors.push(err13);
          }
          errors++;
        }
        if (data3.length < 2) {
          const err14 = { instancePath: instancePath + "/position_mils", schemaPath: "#/$defs/PointMils/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err14];
          } else {
            vErrors.push(err14);
          }
          errors++;
        }
        const len0 = data3.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!(typeof data3[i0] == "number")) {
            const err15 = { instancePath: instancePath + "/position_mils/" + i0, schemaPath: "#/$defs/PointMils/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err15];
            } else {
              vErrors.push(err15);
            }
            errors++;
          }
        }
      } else {
        const err16 = { instancePath: instancePath + "/position_mils", schemaPath: "#/$defs/PointMils/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
    }
    if (data.diameter_mils !== void 0) {
      if (!(typeof data.diameter_mils == "number")) {
        const err17 = { instancePath: instancePath + "/diameter_mils", schemaPath: "#/properties/diameter_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
    }
    if (data.hole_size_mils !== void 0) {
      if (!(typeof data.hole_size_mils == "number")) {
        const err18 = { instancePath: instancePath + "/hole_size_mils", schemaPath: "#/properties/hole_size_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
    }
    if (data.layer_start !== void 0) {
      let data7 = data.layer_start;
      const _errs30 = errors;
      let valid9 = false;
      const _errs31 = errors;
      if (typeof data7 !== "string") {
        const err19 = { instancePath: instancePath + "/layer_start", schemaPath: "#/properties/layer_start/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
      var _valid2 = _errs31 === errors;
      valid9 = valid9 || _valid2;
      const _errs33 = errors;
      if (!(typeof data7 == "number" && (!(data7 % 1) && !isNaN(data7)))) {
        const err20 = { instancePath: instancePath + "/layer_start", schemaPath: "#/properties/layer_start/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      var _valid2 = _errs33 === errors;
      valid9 = valid9 || _valid2;
      const _errs35 = errors;
      if (data7 !== null) {
        const err21 = { instancePath: instancePath + "/layer_start", schemaPath: "#/properties/layer_start/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      var _valid2 = _errs35 === errors;
      valid9 = valid9 || _valid2;
      if (!valid9) {
        const err22 = { instancePath: instancePath + "/layer_start", schemaPath: "#/properties/layer_start/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
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
    if (data.layer_end !== void 0) {
      let data8 = data.layer_end;
      const _errs38 = errors;
      let valid10 = false;
      const _errs39 = errors;
      if (typeof data8 !== "string") {
        const err23 = { instancePath: instancePath + "/layer_end", schemaPath: "#/properties/layer_end/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      var _valid3 = _errs39 === errors;
      valid10 = valid10 || _valid3;
      const _errs41 = errors;
      if (!(typeof data8 == "number" && (!(data8 % 1) && !isNaN(data8)))) {
        const err24 = { instancePath: instancePath + "/layer_end", schemaPath: "#/properties/layer_end/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      var _valid3 = _errs41 === errors;
      valid10 = valid10 || _valid3;
      const _errs43 = errors;
      if (data8 !== null) {
        const err25 = { instancePath: instancePath + "/layer_end", schemaPath: "#/properties/layer_end/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
      var _valid3 = _errs43 === errors;
      valid10 = valid10 || _valid3;
      if (!valid10) {
        const err26 = { instancePath: instancePath + "/layer_end", schemaPath: "#/properties/layer_end/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
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
    if (data.net !== void 0) {
      let data9 = data.net;
      const _errs46 = errors;
      let valid11 = false;
      const _errs47 = errors;
      if (typeof data9 !== "string") {
        const err27 = { instancePath: instancePath + "/net", schemaPath: "#/properties/net/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
      var _valid4 = _errs47 === errors;
      valid11 = valid11 || _valid4;
      const _errs49 = errors;
      if (data9 !== null) {
        const err28 = { instancePath: instancePath + "/net", schemaPath: "#/properties/net/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
      var _valid4 = _errs49 === errors;
      valid11 = valid11 || _valid4;
      if (!valid11) {
        const err29 = { instancePath: instancePath + "/net", schemaPath: "#/properties/net/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      } else {
        errors = _errs46;
        if (vErrors !== null) {
          if (_errs46) {
            vErrors.length = _errs46;
          } else {
            vErrors = null;
          }
        }
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
  validate73.errors = vErrors;
  return errors === 0;
}
validate73.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate72(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate72.evaluated;
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("pcbdoc.add_via" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "pcbdoc.add_via" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate73(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate73.errors : vErrors.concat(validate73.errors);
        errors = vErrors.length;
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
  validate72.errors = vErrors;
  return errors === 0;
}
validate72.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err2 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err2];
          } else {
            vErrors.push(err2);
          }
          errors++;
        }
      } else {
        const err3 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.output_file !== void 0) {
      let data1 = data.output_file;
      const _errs9 = errors;
      let valid4 = false;
      const _errs10 = errors;
      if (typeof data1 !== "string") {
        const err4 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err5 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err6 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.overwrite !== void 0) {
      let data2 = data.overwrite;
      const _errs15 = errors;
      let valid5 = false;
      const _errs16 = errors;
      if (typeof data2 !== "boolean") {
        const err7 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
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
        const err8 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err9 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.designators !== void 0) {
      let data3 = data.designators;
      const _errs21 = errors;
      let valid6 = false;
      const _errs22 = errors;
      if (Array.isArray(data3)) {
        const len0 = data3.length;
        for (let i0 = 0; i0 < len0; i0++) {
          let data4 = data3[i0];
          if (typeof data4 === "string") {
            if (func1(data4) < 1) {
              const err10 = { instancePath: instancePath + "/designators/" + i0, schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
              if (vErrors === null) {
                vErrors = [err10];
              } else {
                vErrors.push(err10);
              }
              errors++;
            }
          } else {
            const err11 = { instancePath: instancePath + "/designators/" + i0, schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err11];
            } else {
              vErrors.push(err11);
            }
            errors++;
          }
        }
      } else {
        const err12 = { instancePath: instancePath + "/designators", schemaPath: "#/properties/designators/anyOf/0/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid2 = _errs22 === errors;
      valid6 = valid6 || _valid2;
      const _errs27 = errors;
      if (data3 !== null) {
        const err13 = { instancePath: instancePath + "/designators", schemaPath: "#/properties/designators/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid2 = _errs27 === errors;
      valid6 = valid6 || _valid2;
      if (!valid6) {
        const err14 = { instancePath: instancePath + "/designators", schemaPath: "#/properties/designators/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
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
    if (data.placement !== void 0) {
      let data5 = data.placement;
      const _errs30 = errors;
      let valid10 = false;
      const _errs31 = errors;
      if (typeof data5 !== "string") {
        const err15 = { instancePath: instancePath + "/placement", schemaPath: "#/properties/placement/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid3 = _errs31 === errors;
      valid10 = valid10 || _valid3;
      const _errs33 = errors;
      if (data5 !== null) {
        const err16 = { instancePath: instancePath + "/placement", schemaPath: "#/properties/placement/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid3 = _errs33 === errors;
      valid10 = valid10 || _valid3;
      if (!valid10) {
        const err17 = { instancePath: instancePath + "/placement", schemaPath: "#/properties/placement/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
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
    if (data.offset_mils !== void 0) {
      let data6 = data.offset_mils;
      const _errs36 = errors;
      let valid11 = false;
      const _errs37 = errors;
      if (Array.isArray(data6)) {
        if (data6.length > 2) {
          const err18 = { instancePath: instancePath + "/offset_mils", schemaPath: "#/$defs/PointMils/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err18];
          } else {
            vErrors.push(err18);
          }
          errors++;
        }
        if (data6.length < 2) {
          const err19 = { instancePath: instancePath + "/offset_mils", schemaPath: "#/$defs/PointMils/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err19];
          } else {
            vErrors.push(err19);
          }
          errors++;
        }
        const len1 = data6.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (!(typeof data6[i1] == "number")) {
            const err20 = { instancePath: instancePath + "/offset_mils/" + i1, schemaPath: "#/$defs/PointMils/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err20];
            } else {
              vErrors.push(err20);
            }
            errors++;
          }
        }
      } else {
        const err21 = { instancePath: instancePath + "/offset_mils", schemaPath: "#/$defs/PointMils/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      var _valid4 = _errs37 === errors;
      valid11 = valid11 || _valid4;
      const _errs42 = errors;
      if (data6 !== null) {
        const err22 = { instancePath: instancePath + "/offset_mils", schemaPath: "#/properties/offset_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
      var _valid4 = _errs42 === errors;
      valid11 = valid11 || _valid4;
      if (!valid11) {
        const err23 = { instancePath: instancePath + "/offset_mils", schemaPath: "#/properties/offset_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
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
    if (data.height_mils !== void 0) {
      let data8 = data.height_mils;
      const _errs45 = errors;
      let valid15 = false;
      const _errs46 = errors;
      if (!(typeof data8 == "number")) {
        const err24 = { instancePath: instancePath + "/height_mils", schemaPath: "#/properties/height_mils/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      var _valid5 = _errs46 === errors;
      valid15 = valid15 || _valid5;
      const _errs48 = errors;
      if (data8 !== null) {
        const err25 = { instancePath: instancePath + "/height_mils", schemaPath: "#/properties/height_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
      var _valid5 = _errs48 === errors;
      valid15 = valid15 || _valid5;
      if (!valid15) {
        const err26 = { instancePath: instancePath + "/height_mils", schemaPath: "#/properties/height_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
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
    if (data.layer !== void 0) {
      let data9 = data.layer;
      const _errs51 = errors;
      let valid16 = false;
      const _errs52 = errors;
      if (typeof data9 !== "string") {
        const err27 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
      var _valid6 = _errs52 === errors;
      valid16 = valid16 || _valid6;
      const _errs54 = errors;
      if (!(typeof data9 == "number" && (!(data9 % 1) && !isNaN(data9)))) {
        const err28 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
      var _valid6 = _errs54 === errors;
      valid16 = valid16 || _valid6;
      const _errs56 = errors;
      if (data9 !== null) {
        const err29 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      }
      var _valid6 = _errs56 === errors;
      valid16 = valid16 || _valid6;
      if (!valid16) {
        const err30 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
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
    if (data.stroke_width_mils !== void 0) {
      let data10 = data.stroke_width_mils;
      const _errs59 = errors;
      let valid17 = false;
      const _errs60 = errors;
      if (!(typeof data10 == "number")) {
        const err31 = { instancePath: instancePath + "/stroke_width_mils", schemaPath: "#/properties/stroke_width_mils/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      }
      var _valid7 = _errs60 === errors;
      valid17 = valid17 || _valid7;
      const _errs62 = errors;
      if (data10 !== null) {
        const err32 = { instancePath: instancePath + "/stroke_width_mils", schemaPath: "#/properties/stroke_width_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
        }
        errors++;
      }
      var _valid7 = _errs62 === errors;
      valid17 = valid17 || _valid7;
      if (!valid17) {
        const err33 = { instancePath: instancePath + "/stroke_width_mils", schemaPath: "#/properties/stroke_width_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
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
    if (data.width_factor !== void 0) {
      let data11 = data.width_factor;
      const _errs65 = errors;
      let valid18 = false;
      const _errs66 = errors;
      if (!(typeof data11 == "number")) {
        const err34 = { instancePath: instancePath + "/width_factor", schemaPath: "#/properties/width_factor/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
        }
        errors++;
      }
      var _valid8 = _errs66 === errors;
      valid18 = valid18 || _valid8;
      const _errs68 = errors;
      if (data11 !== null) {
        const err35 = { instancePath: instancePath + "/width_factor", schemaPath: "#/properties/width_factor/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err35];
        } else {
          vErrors.push(err35);
        }
        errors++;
      }
      var _valid8 = _errs68 === errors;
      valid18 = valid18 || _valid8;
      if (!valid18) {
        const err36 = { instancePath: instancePath + "/width_factor", schemaPath: "#/properties/width_factor/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err36];
        } else {
          vErrors.push(err36);
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
    if (data.bold !== void 0) {
      let data12 = data.bold;
      const _errs71 = errors;
      let valid19 = false;
      const _errs72 = errors;
      if (typeof data12 !== "boolean") {
        const err37 = { instancePath: instancePath + "/bold", schemaPath: "#/properties/bold/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err37];
        } else {
          vErrors.push(err37);
        }
        errors++;
      }
      var _valid9 = _errs72 === errors;
      valid19 = valid19 || _valid9;
      const _errs74 = errors;
      if (data12 !== null) {
        const err38 = { instancePath: instancePath + "/bold", schemaPath: "#/properties/bold/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err38];
        } else {
          vErrors.push(err38);
        }
        errors++;
      }
      var _valid9 = _errs74 === errors;
      valid19 = valid19 || _valid9;
      if (!valid19) {
        const err39 = { instancePath: instancePath + "/bold", schemaPath: "#/properties/bold/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err39];
        } else {
          vErrors.push(err39);
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
    if (data.italic !== void 0) {
      let data13 = data.italic;
      const _errs77 = errors;
      let valid20 = false;
      const _errs78 = errors;
      if (typeof data13 !== "boolean") {
        const err40 = { instancePath: instancePath + "/italic", schemaPath: "#/properties/italic/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err40];
        } else {
          vErrors.push(err40);
        }
        errors++;
      }
      var _valid10 = _errs78 === errors;
      valid20 = valid20 || _valid10;
      const _errs80 = errors;
      if (data13 !== null) {
        const err41 = { instancePath: instancePath + "/italic", schemaPath: "#/properties/italic/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err41];
        } else {
          vErrors.push(err41);
        }
        errors++;
      }
      var _valid10 = _errs80 === errors;
      valid20 = valid20 || _valid10;
      if (!valid20) {
        const err42 = { instancePath: instancePath + "/italic", schemaPath: "#/properties/italic/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err42];
        } else {
          vErrors.push(err42);
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
    if (data.font_name !== void 0) {
      let data14 = data.font_name;
      const _errs83 = errors;
      let valid21 = false;
      const _errs84 = errors;
      if (typeof data14 !== "string") {
        const err43 = { instancePath: instancePath + "/font_name", schemaPath: "#/properties/font_name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err43];
        } else {
          vErrors.push(err43);
        }
        errors++;
      }
      var _valid11 = _errs84 === errors;
      valid21 = valid21 || _valid11;
      const _errs86 = errors;
      if (data14 !== null) {
        const err44 = { instancePath: instancePath + "/font_name", schemaPath: "#/properties/font_name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err44];
        } else {
          vErrors.push(err44);
        }
        errors++;
      }
      var _valid11 = _errs86 === errors;
      valid21 = valid21 || _valid11;
      if (!valid21) {
        const err45 = { instancePath: instancePath + "/font_name", schemaPath: "#/properties/font_name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err45];
        } else {
          vErrors.push(err45);
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
    if (data.font_kind !== void 0) {
      let data15 = data.font_kind;
      const _errs89 = errors;
      let valid22 = false;
      const _errs90 = errors;
      if (typeof data15 !== "string") {
        const err46 = { instancePath: instancePath + "/font_kind", schemaPath: "#/properties/font_kind/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err46];
        } else {
          vErrors.push(err46);
        }
        errors++;
      }
      var _valid12 = _errs90 === errors;
      valid22 = valid22 || _valid12;
      const _errs92 = errors;
      if (data15 !== null) {
        const err47 = { instancePath: instancePath + "/font_kind", schemaPath: "#/properties/font_kind/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err47];
        } else {
          vErrors.push(err47);
        }
        errors++;
      }
      var _valid12 = _errs92 === errors;
      valid22 = valid22 || _valid12;
      if (!valid22) {
        const err48 = { instancePath: instancePath + "/font_kind", schemaPath: "#/properties/font_kind/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err48];
        } else {
          vErrors.push(err48);
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
    const err49 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err49];
    } else {
      vErrors.push(err49);
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("pcbdoc.arrange_designators" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "pcbdoc.arrange_designators" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate77(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate77.errors : vErrors.concat(validate77.errors);
        errors = vErrors.length;
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
  validate83.errors = vErrors;
  return errors === 0;
}
validate83.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
  validate85.errors = vErrors;
  return errors === 0;
}
validate85.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
          if (!validate83(data2[i0], { instancePath: instancePath + "/copper_layers/" + i0, parentData: data2, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate83.errors : vErrors.concat(validate83.errors);
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
          if (!validate85(data4[i1], { instancePath: instancePath + "/dielectrics_between/" + i1, parentData: data4, parentDataProperty: i1, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate85.errors : vErrors.concat(validate85.errors);
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
  validate82.errors = vErrors;
  return errors === 0;
}
validate82.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate88(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate88.evaluated;
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
  validate88.errors = vErrors;
  return errors === 0;
}
validate88.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate90(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate90.evaluated;
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
    if (data.x === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "x" }, message: "must have required property 'x'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.y === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "y" }, message: "must have required property 'y'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.x !== void 0) {
      let data0 = data.x;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (!(typeof data0 == "number")) {
        const err3 = { instancePath: instancePath + "/x", schemaPath: "#/properties/x/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
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
        const err4 = { instancePath: instancePath + "/x", schemaPath: "#/properties/x/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
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
        const err5 = { instancePath: instancePath + "/x", schemaPath: "#/properties/x/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.y !== void 0) {
      let data1 = data.y;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (!(typeof data1 == "number")) {
        const err6 = { instancePath: instancePath + "/y", schemaPath: "#/properties/y/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
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
        const err7 = { instancePath: instancePath + "/y", schemaPath: "#/properties/y/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
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
        const err8 = { instancePath: instancePath + "/y", schemaPath: "#/properties/y/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
  validate90.errors = vErrors;
  return errors === 0;
}
validate90.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate92(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate92.evaluated;
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
    if (data.x === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "x" }, message: "must have required property 'x'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.y === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "y" }, message: "must have required property 'y'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.width === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "width" }, message: "must have required property 'width'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.height === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "height" }, message: "must have required property 'height'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.x !== void 0) {
      let data0 = data.x;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (!(typeof data0 == "number")) {
        const err5 = { instancePath: instancePath + "/x", schemaPath: "#/properties/x/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
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
        const err6 = { instancePath: instancePath + "/x", schemaPath: "#/properties/x/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
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
        const err7 = { instancePath: instancePath + "/x", schemaPath: "#/properties/x/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.y !== void 0) {
      let data1 = data.y;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (!(typeof data1 == "number")) {
        const err8 = { instancePath: instancePath + "/y", schemaPath: "#/properties/y/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
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
        const err9 = { instancePath: instancePath + "/y", schemaPath: "#/properties/y/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
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
        const err10 = { instancePath: instancePath + "/y", schemaPath: "#/properties/y/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.width !== void 0) {
      let data2 = data.width;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (!(typeof data2 == "number")) {
        const err11 = { instancePath: instancePath + "/width", schemaPath: "#/properties/width/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
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
        const err12 = { instancePath: instancePath + "/width", schemaPath: "#/properties/width/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
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
        const err13 = { instancePath: instancePath + "/width", schemaPath: "#/properties/width/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.height !== void 0) {
      let data3 = data.height;
      const _errs24 = errors;
      let valid6 = false;
      const _errs25 = errors;
      if (!(typeof data3 == "number")) {
        const err14 = { instancePath: instancePath + "/height", schemaPath: "#/properties/height/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
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
        const err15 = { instancePath: instancePath + "/height", schemaPath: "#/properties/height/anyOf/1/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
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
        const err16 = { instancePath: instancePath + "/height", schemaPath: "#/properties/height/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
  validate92.errors = vErrors;
  return errors === 0;
}
validate92.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate94(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate94.evaluated;
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
          const err2 = { instancePath: instancePath + "/layer", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err2];
          } else {
            vErrors.push(err2);
          }
          errors++;
        }
      } else {
        const err3 = { instancePath: instancePath + "/layer", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (typeof data1 !== "string") {
        const err4 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err5 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err6 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.enabled !== void 0) {
      let data2 = data.enabled;
      const _errs15 = errors;
      let valid5 = false;
      const _errs16 = errors;
      if (typeof data2 !== "boolean") {
        const err7 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
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
        const err8 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err9 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
  } else {
    const err10 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err10];
    } else {
      vErrors.push(err10);
    }
    errors++;
  }
  validate94.errors = vErrors;
  return errors === 0;
}
validate94.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
          const err3 = { instancePath: instancePath + "/layer_1", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/layer_1", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
          const err5 = { instancePath: instancePath + "/layer_2", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err5];
          } else {
            vErrors.push(err5);
          }
          errors++;
        }
      } else {
        const err6 = { instancePath: instancePath + "/layer_2", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
  validate96.errors = vErrors;
  return errors === 0;
}
validate96.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate98(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate98.evaluated;
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
          const err3 = { instancePath: instancePath + "/layer", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/layer", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (typeof data1 !== "string") {
        const err5 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      valid4 = valid4 || _valid0;
      const _errs12 = errors;
      if (!(typeof data1 == "number" && (!(data1 % 1) && !isNaN(data1)))) {
        const err6 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
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
      if (typeof data1 !== "boolean") {
        const err7 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/anyOf/2/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
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
  validate98.errors = vErrors;
  return errors === 0;
}
validate98.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate81(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate81.evaluated;
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err2 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err2];
          } else {
            vErrors.push(err2);
          }
          errors++;
        }
      } else {
        const err3 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.layer_stack_template !== void 0) {
      let data1 = data.layer_stack_template;
      const _errs9 = errors;
      let valid4 = false;
      const _errs10 = errors;
      if (typeof data1 !== "string") {
        const err4 = { instancePath: instancePath + "/layer_stack_template", schemaPath: "#/properties/layer_stack_template/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err5 = { instancePath: instancePath + "/layer_stack_template", schemaPath: "#/properties/layer_stack_template/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err6 = { instancePath: instancePath + "/layer_stack_template", schemaPath: "#/properties/layer_stack_template/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.rigid_stack !== void 0) {
      let data2 = data.rigid_stack;
      const _errs15 = errors;
      let valid5 = false;
      const _errs16 = errors;
      if (!validate82(data2, { instancePath: instancePath + "/rigid_stack", parentData: data, parentDataProperty: "rigid_stack", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate82.errors : vErrors.concat(validate82.errors);
        errors = vErrors.length;
      }
      var _valid1 = _errs16 === errors;
      valid5 = valid5 || _valid1;
      const _errs17 = errors;
      if (data2 !== null) {
        const err7 = { instancePath: instancePath + "/rigid_stack", schemaPath: "#/properties/rigid_stack/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid1 = _errs17 === errors;
      valid5 = valid5 || _valid1;
      if (!valid5) {
        const err8 = { instancePath: instancePath + "/rigid_stack", schemaPath: "#/properties/rigid_stack/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.stackupx_file !== void 0) {
      let data3 = data.stackupx_file;
      const _errs20 = errors;
      let valid6 = false;
      const _errs21 = errors;
      if (typeof data3 === "string") {
        if (func1(data3) < 1) {
          const err9 = { instancePath: instancePath + "/stackupx_file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err9];
          } else {
            vErrors.push(err9);
          }
          errors++;
        }
      } else {
        const err10 = { instancePath: instancePath + "/stackupx_file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid6 = valid6 || _valid2;
      const _errs24 = errors;
      if (data3 !== null) {
        const err11 = { instancePath: instancePath + "/stackupx_file", schemaPath: "#/properties/stackupx_file/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err12 = { instancePath: instancePath + "/stackupx_file", schemaPath: "#/properties/stackupx_file/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
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
    if (data.board_outline_mils !== void 0) {
      let data4 = data.board_outline_mils;
      const _errs27 = errors;
      let valid8 = false;
      const _errs28 = errors;
      if (!validate88(data4, { instancePath: instancePath + "/board_outline_mils", parentData: data, parentDataProperty: "board_outline_mils", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate88.errors : vErrors.concat(validate88.errors);
        errors = vErrors.length;
      }
      var _valid3 = _errs28 === errors;
      valid8 = valid8 || _valid3;
      const _errs29 = errors;
      if (data4 !== null) {
        const err13 = { instancePath: instancePath + "/board_outline_mils", schemaPath: "#/properties/board_outline_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid3 = _errs29 === errors;
      valid8 = valid8 || _valid3;
      if (!valid8) {
        const err14 = { instancePath: instancePath + "/board_outline_mils", schemaPath: "#/properties/board_outline_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
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
    if (data.board_origin_mils !== void 0) {
      let data5 = data.board_origin_mils;
      const _errs32 = errors;
      let valid9 = false;
      const _errs33 = errors;
      if (!validate90(data5, { instancePath: instancePath + "/board_origin_mils", parentData: data, parentDataProperty: "board_origin_mils", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate90.errors : vErrors.concat(validate90.errors);
        errors = vErrors.length;
      }
      var _valid4 = _errs33 === errors;
      valid9 = valid9 || _valid4;
      const _errs34 = errors;
      if (data5 !== null) {
        const err15 = { instancePath: instancePath + "/board_origin_mils", schemaPath: "#/properties/board_origin_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid4 = _errs34 === errors;
      valid9 = valid9 || _valid4;
      if (!valid9) {
        const err16 = { instancePath: instancePath + "/board_origin_mils", schemaPath: "#/properties/board_origin_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.sheet_frame_mils !== void 0) {
      let data6 = data.sheet_frame_mils;
      const _errs37 = errors;
      let valid10 = false;
      const _errs38 = errors;
      if (!validate92(data6, { instancePath: instancePath + "/sheet_frame_mils", parentData: data, parentDataProperty: "sheet_frame_mils", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate92.errors : vErrors.concat(validate92.errors);
        errors = vErrors.length;
      }
      var _valid5 = _errs38 === errors;
      valid10 = valid10 || _valid5;
      const _errs39 = errors;
      if (data6 !== null) {
        const err17 = { instancePath: instancePath + "/sheet_frame_mils", schemaPath: "#/properties/sheet_frame_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      var _valid5 = _errs39 === errors;
      valid10 = valid10 || _valid5;
      if (!valid10) {
        const err18 = { instancePath: instancePath + "/sheet_frame_mils", schemaPath: "#/properties/sheet_frame_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
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
    }
    if (data.mechanical_layer_profile !== void 0) {
      let data7 = data.mechanical_layer_profile;
      const _errs42 = errors;
      let valid11 = false;
      const _errs43 = errors;
      if (typeof data7 !== "string") {
        const err19 = { instancePath: instancePath + "/mechanical_layer_profile", schemaPath: "#/properties/mechanical_layer_profile/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
      var _valid6 = _errs43 === errors;
      valid11 = valid11 || _valid6;
      const _errs45 = errors;
      if (data7 !== null) {
        const err20 = { instancePath: instancePath + "/mechanical_layer_profile", schemaPath: "#/properties/mechanical_layer_profile/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      var _valid6 = _errs45 === errors;
      valid11 = valid11 || _valid6;
      if (!valid11) {
        const err21 = { instancePath: instancePath + "/mechanical_layer_profile", schemaPath: "#/properties/mechanical_layer_profile/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
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
    if (data.mechanical_layers !== void 0) {
      let data8 = data.mechanical_layers;
      const _errs48 = errors;
      let valid12 = false;
      const _errs49 = errors;
      if (Array.isArray(data8)) {
        const len0 = data8.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!validate94(data8[i0], { instancePath: instancePath + "/mechanical_layers/" + i0, parentData: data8, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate94.errors : vErrors.concat(validate94.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err22 = { instancePath: instancePath + "/mechanical_layers", schemaPath: "#/properties/mechanical_layers/anyOf/0/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
      var _valid7 = _errs49 === errors;
      valid12 = valid12 || _valid7;
      const _errs52 = errors;
      if (data8 !== null) {
        const err23 = { instancePath: instancePath + "/mechanical_layers", schemaPath: "#/properties/mechanical_layers/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      var _valid7 = _errs52 === errors;
      valid12 = valid12 || _valid7;
      if (!valid12) {
        const err24 = { instancePath: instancePath + "/mechanical_layers", schemaPath: "#/properties/mechanical_layers/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
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
    if (data.mechanical_layer_pairs !== void 0) {
      let data10 = data.mechanical_layer_pairs;
      const _errs55 = errors;
      let valid15 = false;
      const _errs56 = errors;
      if (Array.isArray(data10)) {
        const len1 = data10.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (!validate96(data10[i1], { instancePath: instancePath + "/mechanical_layer_pairs/" + i1, parentData: data10, parentDataProperty: i1, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate96.errors : vErrors.concat(validate96.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err25 = { instancePath: instancePath + "/mechanical_layer_pairs", schemaPath: "#/properties/mechanical_layer_pairs/anyOf/0/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
      var _valid8 = _errs56 === errors;
      valid15 = valid15 || _valid8;
      const _errs59 = errors;
      if (data10 !== null) {
        const err26 = { instancePath: instancePath + "/mechanical_layer_pairs", schemaPath: "#/properties/mechanical_layer_pairs/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
      var _valid8 = _errs59 === errors;
      valid15 = valid15 || _valid8;
      if (!valid15) {
        const err27 = { instancePath: instancePath + "/mechanical_layer_pairs", schemaPath: "#/properties/mechanical_layer_pairs/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
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
    if (data.mechanical_layer_kinds !== void 0) {
      let data12 = data.mechanical_layer_kinds;
      const _errs62 = errors;
      let valid18 = false;
      const _errs63 = errors;
      if (Array.isArray(data12)) {
        const len2 = data12.length;
        for (let i2 = 0; i2 < len2; i2++) {
          if (!validate98(data12[i2], { instancePath: instancePath + "/mechanical_layer_kinds/" + i2, parentData: data12, parentDataProperty: i2, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate98.errors : vErrors.concat(validate98.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err28 = { instancePath: instancePath + "/mechanical_layer_kinds", schemaPath: "#/properties/mechanical_layer_kinds/anyOf/0/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
      var _valid9 = _errs63 === errors;
      valid18 = valid18 || _valid9;
      const _errs66 = errors;
      if (data12 !== null) {
        const err29 = { instancePath: instancePath + "/mechanical_layer_kinds", schemaPath: "#/properties/mechanical_layer_kinds/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      }
      var _valid9 = _errs66 === errors;
      valid18 = valid18 || _valid9;
      if (!valid18) {
        const err30 = { instancePath: instancePath + "/mechanical_layer_kinds", schemaPath: "#/properties/mechanical_layer_kinds/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
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
    if (data.overwrite !== void 0) {
      let data14 = data.overwrite;
      const _errs69 = errors;
      let valid21 = false;
      const _errs70 = errors;
      if (typeof data14 !== "boolean") {
        const err31 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      }
      var _valid10 = _errs70 === errors;
      valid21 = valid21 || _valid10;
      const _errs72 = errors;
      if (data14 !== null) {
        const err32 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
        }
        errors++;
      }
      var _valid10 = _errs72 === errors;
      valid21 = valid21 || _valid10;
      if (!valid21) {
        const err33 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
  } else {
    const err34 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err34];
    } else {
      vErrors.push(err34);
    }
    errors++;
  }
  validate81.errors = vErrors;
  return errors === 0;
}
validate81.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate80(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate80.evaluated;
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("pcbdoc.create" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "pcbdoc.create" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate81(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate81.errors : vErrors.concat(validate81.errors);
        errors = vErrors.length;
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
  validate80.errors = vErrors;
  return errors === 0;
}
validate80.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate103(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate103.evaluated;
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.name === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err3 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.output_file !== void 0) {
      let data1 = data.output_file;
      const _errs9 = errors;
      let valid4 = false;
      const _errs10 = errors;
      if (typeof data1 !== "string") {
        const err5 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      valid4 = valid4 || _valid0;
      const _errs12 = errors;
      if (data1 !== null) {
        const err6 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs12 === errors;
      valid4 = valid4 || _valid0;
      if (!valid4) {
        const err7 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.overwrite !== void 0) {
      let data2 = data.overwrite;
      const _errs15 = errors;
      let valid5 = false;
      const _errs16 = errors;
      if (typeof data2 !== "boolean") {
        const err8 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid1 = _errs16 === errors;
      valid5 = valid5 || _valid1;
      const _errs18 = errors;
      if (data2 !== null) {
        const err9 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid1 = _errs18 === errors;
      valid5 = valid5 || _valid1;
      if (!valid5) {
        const err10 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
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
    if (data.name !== void 0) {
      let data3 = data.name;
      if (typeof data3 === "string") {
        if (func1(data3) < 1) {
          const err11 = { instancePath: instancePath + "/name", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err11];
          } else {
            vErrors.push(err11);
          }
          errors++;
        }
      } else {
        const err12 = { instancePath: instancePath + "/name", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
    }
    if (data.members !== void 0) {
      let data4 = data.members;
      const _errs24 = errors;
      let valid7 = false;
      const _errs25 = errors;
      if (typeof data4 !== "string") {
        const err13 = { instancePath: instancePath + "/members", schemaPath: "#/properties/members/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      if ("all" !== data4) {
        const err14 = { instancePath: instancePath + "/members", schemaPath: "#/properties/members/anyOf/0/const", keyword: "const", params: { allowedValue: "all" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid2 = _errs25 === errors;
      valid7 = valid7 || _valid2;
      const _errs27 = errors;
      if (data4 !== null) {
        const err15 = { instancePath: instancePath + "/members", schemaPath: "#/properties/members/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid2 = _errs27 === errors;
      valid7 = valid7 || _valid2;
      if (!valid7) {
        const err16 = { instancePath: instancePath + "/members", schemaPath: "#/properties/members/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
  validate103.errors = vErrors;
  return errors === 0;
}
validate103.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("pcbdoc.create_user_union" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "pcbdoc.create_user_union" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate103(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate103.errors : vErrors.concat(validate103.errors);
        errors = vErrors.length;
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
  validate102.errors = vErrors;
  return errors === 0;
}
validate102.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.id === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.color === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "color" }, message: "must have required property 'color'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err3 = { instancePath: instancePath + "/id", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (typeof data1 !== "string") {
        const err5 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      valid4 = valid4 || _valid0;
      const _errs12 = errors;
      if (data1 !== null) {
        const err6 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs12 === errors;
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
    if (data.color !== void 0) {
      let data2 = data.color;
      if (typeof data2 === "string") {
        if (func1(data2) < 1) {
          const err8 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err8];
          } else {
            vErrors.push(err8);
          }
          errors++;
        }
      } else {
        const err9 = { instancePath: instancePath + "/color", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    if (data.pad_geometries !== void 0) {
      if (!Array.isArray(data.pad_geometries)) {
        const err10 = { instancePath: instancePath + "/pad_geometries", schemaPath: "#/properties/pad_geometries/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
    }
    if (data.z_offset_mm !== void 0) {
      let data4 = data.z_offset_mm;
      const _errs20 = errors;
      let valid6 = false;
      const _errs21 = errors;
      if (!(typeof data4 == "number")) {
        const err11 = { instancePath: instancePath + "/z_offset_mm", schemaPath: "#/properties/z_offset_mm/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
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
      if (data4 !== null) {
        const err12 = { instancePath: instancePath + "/z_offset_mm", schemaPath: "#/properties/z_offset_mm/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid1 = _errs23 === errors;
      valid6 = valid6 || _valid1;
      if (!valid6) {
        const err13 = { instancePath: instancePath + "/z_offset_mm", schemaPath: "#/properties/z_offset_mm/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
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
      let data5 = data.thickness_mm;
      const _errs26 = errors;
      let valid7 = false;
      const _errs27 = errors;
      if (!(typeof data5 == "number")) {
        const err14 = { instancePath: instancePath + "/thickness_mm", schemaPath: "#/properties/thickness_mm/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid2 = _errs27 === errors;
      valid7 = valid7 || _valid2;
      const _errs29 = errors;
      if (data5 !== null) {
        const err15 = { instancePath: instancePath + "/thickness_mm", schemaPath: "#/properties/thickness_mm/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid2 = _errs29 === errors;
      valid7 = valid7 || _valid2;
      if (!valid7) {
        const err16 = { instancePath: instancePath + "/thickness_mm", schemaPath: "#/properties/thickness_mm/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
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
    const err17 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err17];
    } else {
      vErrors.push(err17);
    }
    errors++;
  }
  validate108.errors = vErrors;
  return errors === 0;
}
validate108.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate107(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate107.evaluated;
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.output_file === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "output_file" }, message: "must have required property 'output_file'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err3 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.output_file !== void 0) {
      let data1 = data.output_file;
      if (typeof data1 === "string") {
        if (func1(data1) < 1) {
          const err5 = { instancePath: instancePath + "/output_file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err5];
          } else {
            vErrors.push(err5);
          }
          errors++;
        }
      } else {
        const err6 = { instancePath: instancePath + "/output_file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.layer !== void 0) {
      let data2 = data.layer;
      const _errs12 = errors;
      let valid5 = false;
      const _errs13 = errors;
      if (typeof data2 !== "string") {
        const err7 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (!(typeof data2 == "number" && (!(data2 % 1) && !isNaN(data2)))) {
        const err8 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid0 = _errs15 === errors;
      valid5 = valid5 || _valid0;
      const _errs17 = errors;
      if (data2 !== null) {
        const err9 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid0 = _errs17 === errors;
      valid5 = valid5 || _valid0;
      if (!valid5) {
        const err10 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.board_name !== void 0) {
      let data3 = data.board_name;
      const _errs20 = errors;
      let valid6 = false;
      const _errs21 = errors;
      if (typeof data3 !== "string") {
        const err11 = { instancePath: instancePath + "/board_name", schemaPath: "#/properties/board_name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data3 !== null) {
        const err12 = { instancePath: instancePath + "/board_name", schemaPath: "#/properties/board_name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid1 = _errs23 === errors;
      valid6 = valid6 || _valid1;
      if (!valid6) {
        const err13 = { instancePath: instancePath + "/board_name", schemaPath: "#/properties/board_name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
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
    if (data.highlights !== void 0) {
      let data4 = data.highlights;
      const _errs26 = errors;
      let valid7 = false;
      const _errs27 = errors;
      if (Array.isArray(data4)) {
        const len0 = data4.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!validate108(data4[i0], { instancePath: instancePath + "/highlights/" + i0, parentData: data4, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate108.errors : vErrors.concat(validate108.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err14 = { instancePath: instancePath + "/highlights", schemaPath: "#/properties/highlights/anyOf/0/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid2 = _errs27 === errors;
      valid7 = valid7 || _valid2;
      const _errs30 = errors;
      if (data4 !== null) {
        const err15 = { instancePath: instancePath + "/highlights", schemaPath: "#/properties/highlights/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid2 = _errs30 === errors;
      valid7 = valid7 || _valid2;
      if (!valid7) {
        const err16 = { instancePath: instancePath + "/highlights", schemaPath: "#/properties/highlights/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
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
    if (data.overwrite !== void 0) {
      let data6 = data.overwrite;
      const _errs33 = errors;
      let valid10 = false;
      const _errs34 = errors;
      if (typeof data6 !== "boolean") {
        const err17 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      var _valid3 = _errs34 === errors;
      valid10 = valid10 || _valid3;
      const _errs36 = errors;
      if (data6 !== null) {
        const err18 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
      var _valid3 = _errs36 === errors;
      valid10 = valid10 || _valid3;
      if (!valid10) {
        const err19 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
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
  } else {
    const err20 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err20];
    } else {
      vErrors.push(err20);
    }
    errors++;
  }
  validate107.errors = vErrors;
  return errors === 0;
}
validate107.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate106(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate106.evaluated;
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("pcbdoc.export_layer_step" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "pcbdoc.export_layer_step" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate107(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate107.errors : vErrors.concat(validate107.errors);
        errors = vErrors.length;
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
  validate106.errors = vErrors;
  return errors === 0;
}
validate106.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.name === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err3 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.output_file !== void 0) {
      let data1 = data.output_file;
      const _errs9 = errors;
      let valid4 = false;
      const _errs10 = errors;
      if (typeof data1 !== "string") {
        const err5 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      valid4 = valid4 || _valid0;
      const _errs12 = errors;
      if (data1 !== null) {
        const err6 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs12 === errors;
      valid4 = valid4 || _valid0;
      if (!valid4) {
        const err7 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.overwrite !== void 0) {
      let data2 = data.overwrite;
      const _errs15 = errors;
      let valid5 = false;
      const _errs16 = errors;
      if (typeof data2 !== "boolean") {
        const err8 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid1 = _errs16 === errors;
      valid5 = valid5 || _valid1;
      const _errs18 = errors;
      if (data2 !== null) {
        const err9 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid1 = _errs18 === errors;
      valid5 = valid5 || _valid1;
      if (!valid5) {
        const err10 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
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
    if (data.name !== void 0) {
      let data3 = data.name;
      if (typeof data3 === "string") {
        if (func1(data3) < 1) {
          const err11 = { instancePath: instancePath + "/name", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err11];
          } else {
            vErrors.push(err11);
          }
          errors++;
        }
      } else {
        const err12 = { instancePath: instancePath + "/name", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
    }
    if (data.height !== void 0) {
      let data4 = data.height;
      const _errs24 = errors;
      let valid7 = false;
      const _errs25 = errors;
      if (typeof data4 !== "string") {
        const err13 = { instancePath: instancePath + "/height", schemaPath: "#/properties/height/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid2 = _errs25 === errors;
      valid7 = valid7 || _valid2;
      const _errs27 = errors;
      if (data4 !== null) {
        const err14 = { instancePath: instancePath + "/height", schemaPath: "#/properties/height/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid2 = _errs27 === errors;
      valid7 = valid7 || _valid2;
      if (!valid7) {
        const err15 = { instancePath: instancePath + "/height", schemaPath: "#/properties/height/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
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
    if (data.description !== void 0) {
      let data5 = data.description;
      const _errs30 = errors;
      let valid8 = false;
      const _errs31 = errors;
      if (typeof data5 !== "string") {
        const err16 = { instancePath: instancePath + "/description", schemaPath: "#/properties/description/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid3 = _errs31 === errors;
      valid8 = valid8 || _valid3;
      const _errs33 = errors;
      if (data5 !== null) {
        const err17 = { instancePath: instancePath + "/description", schemaPath: "#/properties/description/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      var _valid3 = _errs33 === errors;
      valid8 = valid8 || _valid3;
      if (!valid8) {
        const err18 = { instancePath: instancePath + "/description", schemaPath: "#/properties/description/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.item_guid !== void 0) {
      let data6 = data.item_guid;
      const _errs36 = errors;
      let valid9 = false;
      const _errs37 = errors;
      if (typeof data6 !== "string") {
        const err19 = { instancePath: instancePath + "/item_guid", schemaPath: "#/properties/item_guid/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data6 !== null) {
        const err20 = { instancePath: instancePath + "/item_guid", schemaPath: "#/properties/item_guid/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      var _valid4 = _errs39 === errors;
      valid9 = valid9 || _valid4;
      if (!valid9) {
        const err21 = { instancePath: instancePath + "/item_guid", schemaPath: "#/properties/item_guid/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    }
    if (data.revision_guid !== void 0) {
      let data7 = data.revision_guid;
      const _errs42 = errors;
      let valid10 = false;
      const _errs43 = errors;
      if (typeof data7 !== "string") {
        const err22 = { instancePath: instancePath + "/revision_guid", schemaPath: "#/properties/revision_guid/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
      var _valid5 = _errs43 === errors;
      valid10 = valid10 || _valid5;
      const _errs45 = errors;
      if (data7 !== null) {
        const err23 = { instancePath: instancePath + "/revision_guid", schemaPath: "#/properties/revision_guid/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      var _valid5 = _errs45 === errors;
      valid10 = valid10 || _valid5;
      if (!valid10) {
        const err24 = { instancePath: instancePath + "/revision_guid", schemaPath: "#/properties/revision_guid/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
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
    if (data.parameters !== void 0) {
      let data8 = data.parameters;
      const _errs48 = errors;
      let valid11 = false;
      const _errs49 = errors;
      if (data8 && typeof data8 == "object" && !Array.isArray(data8)) {
        for (const key1 in data8) {
          if (typeof data8[key1] !== "string") {
            const err25 = { instancePath: instancePath + "/parameters/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/RecordString/unevaluatedProperties/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err25];
            } else {
              vErrors.push(err25);
            }
            errors++;
          }
        }
      } else {
        const err26 = { instancePath: instancePath + "/parameters", schemaPath: "#/$defs/RecordString/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
      var _valid6 = _errs49 === errors;
      valid11 = valid11 || _valid6;
      const _errs55 = errors;
      if (data8 !== null) {
        const err27 = { instancePath: instancePath + "/parameters", schemaPath: "#/properties/parameters/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
      var _valid6 = _errs55 === errors;
      valid11 = valid11 || _valid6;
      if (!valid11) {
        const err28 = { instancePath: instancePath + "/parameters", schemaPath: "#/properties/parameters/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
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
    if (data.primitive_parameters !== void 0) {
      let data10 = data.primitive_parameters;
      const _errs58 = errors;
      let valid14 = false;
      const _errs59 = errors;
      if (data10 && typeof data10 == "object" && !Array.isArray(data10)) {
        for (const key2 in data10) {
          if (typeof data10[key2] !== "string") {
            const err29 = { instancePath: instancePath + "/primitive_parameters/" + key2.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/RecordString/unevaluatedProperties/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err29];
            } else {
              vErrors.push(err29);
            }
            errors++;
          }
        }
      } else {
        const err30 = { instancePath: instancePath + "/primitive_parameters", schemaPath: "#/$defs/RecordString/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
        }
        errors++;
      }
      var _valid7 = _errs59 === errors;
      valid14 = valid14 || _valid7;
      const _errs65 = errors;
      if (data10 !== null) {
        const err31 = { instancePath: instancePath + "/primitive_parameters", schemaPath: "#/properties/primitive_parameters/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      }
      var _valid7 = _errs65 === errors;
      valid14 = valid14 || _valid7;
      if (!valid14) {
        const err32 = { instancePath: instancePath + "/primitive_parameters", schemaPath: "#/properties/primitive_parameters/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
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
  } else {
    const err33 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err33];
    } else {
      vErrors.push(err33);
    }
    errors++;
  }
  validate113.errors = vErrors;
  return errors === 0;
}
validate113.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("pcblib.add_footprint" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "pcblib.add_footprint" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate113(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate113.errors : vErrors.concat(validate113.errors);
        errors = vErrors.length;
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
  validate112.errors = vErrors;
  return errors === 0;
}
validate112.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate117(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate117.evaluated;
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err2 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err2];
          } else {
            vErrors.push(err2);
          }
          errors++;
        }
      } else {
        const err3 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.overwrite !== void 0) {
      let data1 = data.overwrite;
      const _errs9 = errors;
      let valid4 = false;
      const _errs10 = errors;
      if (typeof data1 !== "boolean") {
        const err4 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
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
        const err5 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err6 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
  } else {
    const err7 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err7];
    } else {
      vErrors.push(err7);
    }
    errors++;
  }
  validate117.errors = vErrors;
  return errors === 0;
}
validate117.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("pcblib.create" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "pcblib.create" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate117(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate117.errors : vErrors.concat(validate117.errors);
        errors = vErrors.length;
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
  validate116.errors = vErrors;
  return errors === 0;
}
validate116.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.document === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "document" }, message: "must have required property 'document'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err3 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.document !== void 0) {
      let data1 = data.document;
      if (typeof data1 === "string") {
        if (func1(data1) < 1) {
          const err5 = { instancePath: instancePath + "/document", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err5];
          } else {
            vErrors.push(err5);
          }
          errors++;
        }
      } else {
        const err6 = { instancePath: instancePath + "/document", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.unique_id !== void 0) {
      let data2 = data.unique_id;
      const _errs12 = errors;
      let valid5 = false;
      const _errs13 = errors;
      if (typeof data2 !== "string") {
        const err7 = { instancePath: instancePath + "/unique_id", schemaPath: "#/properties/unique_id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err8 = { instancePath: instancePath + "/unique_id", schemaPath: "#/properties/unique_id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err9 = { instancePath: instancePath + "/unique_id", schemaPath: "#/properties/unique_id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
  } else {
    const err10 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err10];
    } else {
      vErrors.push(err10);
    }
    errors++;
  }
  validate121.errors = vErrors;
  return errors === 0;
}
validate121.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate120(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate120.evaluated;
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("project.add_document" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "project.add_document" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate121(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate121.errors : vErrors.concat(validate121.errors);
        errors = vErrors.length;
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
  validate120.errors = vErrors;
  return errors === 0;
}
validate120.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate125(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate125.evaluated;
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.name === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.value === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "value" }, message: "must have required property 'value'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err4 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err4];
          } else {
            vErrors.push(err4);
          }
          errors++;
        }
      } else {
        const err5 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.name !== void 0) {
      let data1 = data.name;
      if (typeof data1 === "string") {
        if (func1(data1) < 1) {
          const err6 = { instancePath: instancePath + "/name", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err6];
          } else {
            vErrors.push(err6);
          }
          errors++;
        }
      } else {
        const err7 = { instancePath: instancePath + "/name", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.value !== void 0) {
      let data2 = data.value;
      if (typeof data2 === "string") {
        if (func1(data2) < 1) {
          const err8 = { instancePath: instancePath + "/value", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err8];
          } else {
            vErrors.push(err8);
          }
          errors++;
        }
      } else {
        const err9 = { instancePath: instancePath + "/value", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
  validate125.errors = vErrors;
  return errors === 0;
}
validate125.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("project.add_parameter" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "project.add_parameter" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate125(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate125.errors : vErrors.concat(validate125.errors);
        errors = vErrors.length;
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
  validate124.errors = vErrors;
  return errors === 0;
}
validate124.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate129(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate129.evaluated;
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.name === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err3 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (typeof data1 === "string") {
        if (func1(data1) < 1) {
          const err5 = { instancePath: instancePath + "/name", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err5];
          } else {
            vErrors.push(err5);
          }
          errors++;
        }
      } else {
        const err6 = { instancePath: instancePath + "/name", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.unique_id !== void 0) {
      let data2 = data.unique_id;
      const _errs12 = errors;
      let valid5 = false;
      const _errs13 = errors;
      if (typeof data2 !== "string") {
        const err7 = { instancePath: instancePath + "/unique_id", schemaPath: "#/properties/unique_id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err8 = { instancePath: instancePath + "/unique_id", schemaPath: "#/properties/unique_id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err9 = { instancePath: instancePath + "/unique_id", schemaPath: "#/properties/unique_id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.allow_fabrication !== void 0) {
      let data3 = data.allow_fabrication;
      const _errs18 = errors;
      let valid6 = false;
      const _errs19 = errors;
      if (typeof data3 !== "boolean") {
        const err10 = { instancePath: instancePath + "/allow_fabrication", schemaPath: "#/properties/allow_fabrication/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
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
      if (data3 !== null) {
        const err11 = { instancePath: instancePath + "/allow_fabrication", schemaPath: "#/properties/allow_fabrication/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid1 = _errs21 === errors;
      valid6 = valid6 || _valid1;
      if (!valid6) {
        const err12 = { instancePath: instancePath + "/allow_fabrication", schemaPath: "#/properties/allow_fabrication/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.current !== void 0) {
      let data4 = data.current;
      const _errs24 = errors;
      let valid7 = false;
      const _errs25 = errors;
      if (typeof data4 !== "boolean") {
        const err13 = { instancePath: instancePath + "/current", schemaPath: "#/properties/current/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid2 = _errs25 === errors;
      valid7 = valid7 || _valid2;
      const _errs27 = errors;
      if (data4 !== null) {
        const err14 = { instancePath: instancePath + "/current", schemaPath: "#/properties/current/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid2 = _errs27 === errors;
      valid7 = valid7 || _valid2;
      if (!valid7) {
        const err15 = { instancePath: instancePath + "/current", schemaPath: "#/properties/current/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
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
    const err16 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err16];
    } else {
      vErrors.push(err16);
    }
    errors++;
  }
  validate129.errors = vErrors;
  return errors === 0;
}
validate129.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate128(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate128.evaluated;
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("project.add_variant" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "project.add_variant" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate129(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate129.errors : vErrors.concat(validate129.errors);
        errors = vErrors.length;
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
  validate128.errors = vErrors;
  return errors === 0;
}
validate128.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate133(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate133.evaluated;
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.variant === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "variant" }, message: "must have required property 'variant'" };
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
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err4 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err4];
          } else {
            vErrors.push(err4);
          }
          errors++;
        }
      } else {
        const err5 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.variant !== void 0) {
      let data1 = data.variant;
      if (typeof data1 === "string") {
        if (func1(data1) < 1) {
          const err6 = { instancePath: instancePath + "/variant", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err6];
          } else {
            vErrors.push(err6);
          }
          errors++;
        }
      } else {
        const err7 = { instancePath: instancePath + "/variant", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.designator !== void 0) {
      let data2 = data.designator;
      if (typeof data2 === "string") {
        if (func1(data2) < 1) {
          const err8 = { instancePath: instancePath + "/designator", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err8];
          } else {
            vErrors.push(err8);
          }
          errors++;
        }
      } else {
        const err9 = { instancePath: instancePath + "/designator", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    if (data.unique_id !== void 0) {
      let data3 = data.unique_id;
      const _errs15 = errors;
      let valid6 = false;
      const _errs16 = errors;
      if (typeof data3 !== "string") {
        const err10 = { instancePath: instancePath + "/unique_id", schemaPath: "#/properties/unique_id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid0 = _errs16 === errors;
      valid6 = valid6 || _valid0;
      const _errs18 = errors;
      if (data3 !== null) {
        const err11 = { instancePath: instancePath + "/unique_id", schemaPath: "#/properties/unique_id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid0 = _errs18 === errors;
      valid6 = valid6 || _valid0;
      if (!valid6) {
        const err12 = { instancePath: instancePath + "/unique_id", schemaPath: "#/properties/unique_id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.alternate_part !== void 0) {
      let data4 = data.alternate_part;
      const _errs21 = errors;
      let valid7 = false;
      const _errs22 = errors;
      if (typeof data4 !== "string") {
        const err13 = { instancePath: instancePath + "/alternate_part", schemaPath: "#/properties/alternate_part/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid1 = _errs22 === errors;
      valid7 = valid7 || _valid1;
      const _errs24 = errors;
      if (data4 !== null) {
        const err14 = { instancePath: instancePath + "/alternate_part", schemaPath: "#/properties/alternate_part/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid1 = _errs24 === errors;
      valid7 = valid7 || _valid1;
      if (!valid7) {
        const err15 = { instancePath: instancePath + "/alternate_part", schemaPath: "#/properties/alternate_part/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
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
    const err16 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err16];
    } else {
      vErrors.push(err16);
    }
    errors++;
  }
  validate133.errors = vErrors;
  return errors === 0;
}
validate133.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("project.add_variant_dnp" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "project.add_variant_dnp" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate133(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate133.errors : vErrors.concat(validate133.errors);
        errors = vErrors.length;
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
  validate132.errors = vErrors;
  return errors === 0;
}
validate132.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate137(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate137.evaluated;
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.source_name === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "source_name" }, message: "must have required property 'source_name'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.name === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err4 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err4];
          } else {
            vErrors.push(err4);
          }
          errors++;
        }
      } else {
        const err5 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.source_name !== void 0) {
      let data1 = data.source_name;
      if (typeof data1 === "string") {
        if (func1(data1) < 1) {
          const err6 = { instancePath: instancePath + "/source_name", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err6];
          } else {
            vErrors.push(err6);
          }
          errors++;
        }
      } else {
        const err7 = { instancePath: instancePath + "/source_name", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.name !== void 0) {
      let data2 = data.name;
      if (typeof data2 === "string") {
        if (func1(data2) < 1) {
          const err8 = { instancePath: instancePath + "/name", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err8];
          } else {
            vErrors.push(err8);
          }
          errors++;
        }
      } else {
        const err9 = { instancePath: instancePath + "/name", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    if (data.unique_id !== void 0) {
      let data3 = data.unique_id;
      const _errs15 = errors;
      let valid6 = false;
      const _errs16 = errors;
      if (typeof data3 !== "string") {
        const err10 = { instancePath: instancePath + "/unique_id", schemaPath: "#/properties/unique_id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid0 = _errs16 === errors;
      valid6 = valid6 || _valid0;
      const _errs18 = errors;
      if (data3 !== null) {
        const err11 = { instancePath: instancePath + "/unique_id", schemaPath: "#/properties/unique_id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid0 = _errs18 === errors;
      valid6 = valid6 || _valid0;
      if (!valid6) {
        const err12 = { instancePath: instancePath + "/unique_id", schemaPath: "#/properties/unique_id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.allow_fabrication !== void 0) {
      let data4 = data.allow_fabrication;
      const _errs21 = errors;
      let valid7 = false;
      const _errs22 = errors;
      if (typeof data4 !== "boolean") {
        const err13 = { instancePath: instancePath + "/allow_fabrication", schemaPath: "#/properties/allow_fabrication/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid1 = _errs22 === errors;
      valid7 = valid7 || _valid1;
      const _errs24 = errors;
      if (data4 !== null) {
        const err14 = { instancePath: instancePath + "/allow_fabrication", schemaPath: "#/properties/allow_fabrication/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid1 = _errs24 === errors;
      valid7 = valid7 || _valid1;
      if (!valid7) {
        const err15 = { instancePath: instancePath + "/allow_fabrication", schemaPath: "#/properties/allow_fabrication/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
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
    if (data.current !== void 0) {
      let data5 = data.current;
      const _errs27 = errors;
      let valid8 = false;
      const _errs28 = errors;
      if (typeof data5 !== "boolean") {
        const err16 = { instancePath: instancePath + "/current", schemaPath: "#/properties/current/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid2 = _errs28 === errors;
      valid8 = valid8 || _valid2;
      const _errs30 = errors;
      if (data5 !== null) {
        const err17 = { instancePath: instancePath + "/current", schemaPath: "#/properties/current/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      var _valid2 = _errs30 === errors;
      valid8 = valid8 || _valid2;
      if (!valid8) {
        const err18 = { instancePath: instancePath + "/current", schemaPath: "#/properties/current/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
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
  } else {
    const err19 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err19];
    } else {
      vErrors.push(err19);
    }
    errors++;
  }
  validate137.errors = vErrors;
  return errors === 0;
}
validate137.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate136(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate136.evaluated;
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("project.clone_variant" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "project.clone_variant" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate137(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate137.errors : vErrors.concat(validate137.errors);
        errors = vErrors.length;
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
  validate136.errors = vErrors;
  return errors === 0;
}
validate136.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate141(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate141.evaluated;
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err2 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err2];
          } else {
            vErrors.push(err2);
          }
          errors++;
        }
      } else {
        const err3 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (typeof data1 !== "string") {
        const err4 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err5 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err6 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.project_name !== void 0) {
      let data2 = data.project_name;
      const _errs15 = errors;
      let valid5 = false;
      const _errs16 = errors;
      if (typeof data2 !== "string") {
        const err7 = { instancePath: instancePath + "/project_name", schemaPath: "#/properties/project_name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err8 = { instancePath: instancePath + "/project_name", schemaPath: "#/properties/project_name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err9 = { instancePath: instancePath + "/project_name", schemaPath: "#/properties/project_name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.overwrite !== void 0) {
      let data3 = data.overwrite;
      const _errs21 = errors;
      let valid6 = false;
      const _errs22 = errors;
      if (typeof data3 !== "boolean") {
        const err10 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
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
        const err11 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err12 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
  validate141.errors = vErrors;
  return errors === 0;
}
validate141.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate140(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate140.evaluated;
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("project.create" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "project.create" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate141(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate141.errors : vErrors.concat(validate141.errors);
        errors = vErrors.length;
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
  validate140.errors = vErrors;
  return errors === 0;
}
validate140.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate145(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate145.evaluated;
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.name === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err3 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (typeof data1 === "string") {
        if (func1(data1) < 1) {
          const err5 = { instancePath: instancePath + "/name", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err5];
          } else {
            vErrors.push(err5);
          }
          errors++;
        }
      } else {
        const err6 = { instancePath: instancePath + "/name", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
  validate145.errors = vErrors;
  return errors === 0;
}
validate145.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate144(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate144.evaluated;
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("project.delete_variant" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "project.delete_variant" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate145(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate145.errors : vErrors.concat(validate145.errors);
        errors = vErrors.length;
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
  validate144.errors = vErrors;
  return errors === 0;
}
validate144.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate149(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate149.evaluated;
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err2 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err2];
          } else {
            vErrors.push(err2);
          }
          errors++;
        }
      } else {
        const err3 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
  } else {
    const err4 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err4];
    } else {
      vErrors.push(err4);
    }
    errors++;
  }
  validate149.errors = vErrors;
  return errors === 0;
}
validate149.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate148(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate148.evaluated;
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("project.list_variants" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "project.list_variants" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate149(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate149.errors : vErrors.concat(validate149.errors);
        errors = vErrors.length;
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
  validate148.errors = vErrors;
  return errors === 0;
}
validate148.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate153(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate153.evaluated;
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.name === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.new_name === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "new_name" }, message: "must have required property 'new_name'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err4 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err4];
          } else {
            vErrors.push(err4);
          }
          errors++;
        }
      } else {
        const err5 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.name !== void 0) {
      let data1 = data.name;
      if (typeof data1 === "string") {
        if (func1(data1) < 1) {
          const err6 = { instancePath: instancePath + "/name", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err6];
          } else {
            vErrors.push(err6);
          }
          errors++;
        }
      } else {
        const err7 = { instancePath: instancePath + "/name", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.new_name !== void 0) {
      let data2 = data.new_name;
      if (typeof data2 === "string") {
        if (func1(data2) < 1) {
          const err8 = { instancePath: instancePath + "/new_name", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err8];
          } else {
            vErrors.push(err8);
          }
          errors++;
        }
      } else {
        const err9 = { instancePath: instancePath + "/new_name", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
  validate153.errors = vErrors;
  return errors === 0;
}
validate153.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate152(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate152.evaluated;
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("project.rename_variant" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "project.rename_variant" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate153(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate153.errors : vErrors.concat(validate153.errors);
        errors = vErrors.length;
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
  validate152.errors = vErrors;
  return errors === 0;
}
validate152.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate157(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate157.evaluated;
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.variant === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "variant" }, message: "must have required property 'variant'" };
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
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err4 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err4];
          } else {
            vErrors.push(err4);
          }
          errors++;
        }
      } else {
        const err5 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.variant !== void 0) {
      let data1 = data.variant;
      if (typeof data1 === "string") {
        if (func1(data1) < 1) {
          const err6 = { instancePath: instancePath + "/variant", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err6];
          } else {
            vErrors.push(err6);
          }
          errors++;
        }
      } else {
        const err7 = { instancePath: instancePath + "/variant", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.designator !== void 0) {
      let data2 = data.designator;
      if (typeof data2 === "string") {
        if (func1(data2) < 1) {
          const err8 = { instancePath: instancePath + "/designator", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err8];
          } else {
            vErrors.push(err8);
          }
          errors++;
        }
      } else {
        const err9 = { instancePath: instancePath + "/designator", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    if (data.unique_id !== void 0) {
      let data3 = data.unique_id;
      const _errs15 = errors;
      let valid6 = false;
      const _errs16 = errors;
      if (typeof data3 !== "string") {
        const err10 = { instancePath: instancePath + "/unique_id", schemaPath: "#/properties/unique_id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid0 = _errs16 === errors;
      valid6 = valid6 || _valid0;
      const _errs18 = errors;
      if (data3 !== null) {
        const err11 = { instancePath: instancePath + "/unique_id", schemaPath: "#/properties/unique_id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid0 = _errs18 === errors;
      valid6 = valid6 || _valid0;
      if (!valid6) {
        const err12 = { instancePath: instancePath + "/unique_id", schemaPath: "#/properties/unique_id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.alternate_part !== void 0) {
      let data4 = data.alternate_part;
      const _errs21 = errors;
      let valid7 = false;
      const _errs22 = errors;
      if (typeof data4 !== "string") {
        const err13 = { instancePath: instancePath + "/alternate_part", schemaPath: "#/properties/alternate_part/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid1 = _errs22 === errors;
      valid7 = valid7 || _valid1;
      const _errs24 = errors;
      if (data4 !== null) {
        const err14 = { instancePath: instancePath + "/alternate_part", schemaPath: "#/properties/alternate_part/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid1 = _errs24 === errors;
      valid7 = valid7 || _valid1;
      if (!valid7) {
        const err15 = { instancePath: instancePath + "/alternate_part", schemaPath: "#/properties/alternate_part/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
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
    const err16 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err16];
    } else {
      vErrors.push(err16);
    }
    errors++;
  }
  validate157.errors = vErrors;
  return errors === 0;
}
validate157.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate156(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate156.evaluated;
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("project.toggle_variant_dnp" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "project.toggle_variant_dnp" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate157(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate157.errors : vErrors.concat(validate157.errors);
        errors = vErrors.length;
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
  validate156.errors = vErrors;
  return errors === 0;
}
validate156.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate162(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate162.evaluated;
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
    if (data.position_mils !== void 0) {
      let data0 = data.position_mils;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (Array.isArray(data0)) {
        if (data0.length > 2) {
          const err1 = { instancePath: instancePath + "/position_mils", schemaPath: "#/$defs/PointMils/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err1];
          } else {
            vErrors.push(err1);
          }
          errors++;
        }
        if (data0.length < 2) {
          const err2 = { instancePath: instancePath + "/position_mils", schemaPath: "#/$defs/PointMils/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err2];
          } else {
            vErrors.push(err2);
          }
          errors++;
        }
        const len0 = data0.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!(typeof data0[i0] == "number")) {
            const err3 = { instancePath: instancePath + "/position_mils/" + i0, schemaPath: "#/$defs/PointMils/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err3];
            } else {
              vErrors.push(err3);
            }
            errors++;
          }
        }
      } else {
        const err4 = { instancePath: instancePath + "/position_mils", schemaPath: "#/$defs/PointMils/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid3 = valid3 || _valid0;
      const _errs12 = errors;
      if (data0 !== null) {
        const err5 = { instancePath: instancePath + "/position_mils", schemaPath: "#/properties/position_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid0 = _errs12 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err6 = { instancePath: instancePath + "/position_mils", schemaPath: "#/properties/position_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.font_name !== void 0) {
      let data2 = data.font_name;
      const _errs15 = errors;
      let valid7 = false;
      const _errs16 = errors;
      if (typeof data2 !== "string") {
        const err7 = { instancePath: instancePath + "/font_name", schemaPath: "#/properties/font_name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid1 = _errs16 === errors;
      valid7 = valid7 || _valid1;
      const _errs18 = errors;
      if (data2 !== null) {
        const err8 = { instancePath: instancePath + "/font_name", schemaPath: "#/properties/font_name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid1 = _errs18 === errors;
      valid7 = valid7 || _valid1;
      if (!valid7) {
        const err9 = { instancePath: instancePath + "/font_name", schemaPath: "#/properties/font_name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.font_size !== void 0) {
      let data3 = data.font_size;
      const _errs21 = errors;
      let valid8 = false;
      const _errs22 = errors;
      if (!(typeof data3 == "number")) {
        const err10 = { instancePath: instancePath + "/font_size", schemaPath: "#/properties/font_size/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs22 === errors;
      valid8 = valid8 || _valid2;
      const _errs24 = errors;
      if (data3 !== null) {
        const err11 = { instancePath: instancePath + "/font_size", schemaPath: "#/properties/font_size/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid2 = _errs24 === errors;
      valid8 = valid8 || _valid2;
      if (!valid8) {
        const err12 = { instancePath: instancePath + "/font_size", schemaPath: "#/properties/font_size/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.bold !== void 0) {
      let data4 = data.bold;
      const _errs27 = errors;
      let valid9 = false;
      const _errs28 = errors;
      if (typeof data4 !== "boolean") {
        const err13 = { instancePath: instancePath + "/bold", schemaPath: "#/properties/bold/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
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
      if (data4 !== null) {
        const err14 = { instancePath: instancePath + "/bold", schemaPath: "#/properties/bold/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid3 = _errs30 === errors;
      valid9 = valid9 || _valid3;
      if (!valid9) {
        const err15 = { instancePath: instancePath + "/bold", schemaPath: "#/properties/bold/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
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
    if (data.justification !== void 0) {
      let data5 = data.justification;
      const _errs33 = errors;
      let valid10 = false;
      const _errs34 = errors;
      if (typeof data5 !== "string") {
        const err16 = { instancePath: instancePath + "/justification", schemaPath: "#/properties/justification/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid4 = _errs34 === errors;
      valid10 = valid10 || _valid4;
      const _errs36 = errors;
      if (!(typeof data5 == "number" && (!(data5 % 1) && !isNaN(data5)))) {
        const err17 = { instancePath: instancePath + "/justification", schemaPath: "#/properties/justification/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      var _valid4 = _errs36 === errors;
      valid10 = valid10 || _valid4;
      const _errs38 = errors;
      if (data5 !== null) {
        const err18 = { instancePath: instancePath + "/justification", schemaPath: "#/properties/justification/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
      var _valid4 = _errs38 === errors;
      valid10 = valid10 || _valid4;
      if (!valid10) {
        const err19 = { instancePath: instancePath + "/justification", schemaPath: "#/properties/justification/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
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
    if (data.hidden !== void 0) {
      let data6 = data.hidden;
      const _errs41 = errors;
      let valid11 = false;
      const _errs42 = errors;
      if (typeof data6 !== "boolean") {
        const err20 = { instancePath: instancePath + "/hidden", schemaPath: "#/properties/hidden/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      var _valid5 = _errs42 === errors;
      valid11 = valid11 || _valid5;
      const _errs44 = errors;
      if (data6 !== null) {
        const err21 = { instancePath: instancePath + "/hidden", schemaPath: "#/properties/hidden/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      var _valid5 = _errs44 === errors;
      valid11 = valid11 || _valid5;
      if (!valid11) {
        const err22 = { instancePath: instancePath + "/hidden", schemaPath: "#/properties/hidden/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
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
    if (data.visible !== void 0) {
      let data7 = data.visible;
      const _errs47 = errors;
      let valid12 = false;
      const _errs48 = errors;
      if (typeof data7 !== "boolean") {
        const err23 = { instancePath: instancePath + "/visible", schemaPath: "#/properties/visible/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      var _valid6 = _errs48 === errors;
      valid12 = valid12 || _valid6;
      const _errs50 = errors;
      if (data7 !== null) {
        const err24 = { instancePath: instancePath + "/visible", schemaPath: "#/properties/visible/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      var _valid6 = _errs50 === errors;
      valid12 = valid12 || _valid6;
      if (!valid12) {
        const err25 = { instancePath: instancePath + "/visible", schemaPath: "#/properties/visible/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
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
  } else {
    const err26 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err26];
    } else {
      vErrors.push(err26);
    }
    errors++;
  }
  validate162.errors = vErrors;
  return errors === 0;
}
validate162.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate161(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate161.evaluated;
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.library === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "library" }, message: "must have required property 'library'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.symbol === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "symbol" }, message: "must have required property 'symbol'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.designator === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "designator" }, message: "must have required property 'designator'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.position_mils === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "position_mils" }, message: "must have required property 'position_mils'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err6 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err6];
          } else {
            vErrors.push(err6);
          }
          errors++;
        }
      } else {
        const err7 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.output_file !== void 0) {
      let data1 = data.output_file;
      const _errs9 = errors;
      let valid4 = false;
      const _errs10 = errors;
      if (typeof data1 !== "string") {
        const err8 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      valid4 = valid4 || _valid0;
      const _errs12 = errors;
      if (data1 !== null) {
        const err9 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid0 = _errs12 === errors;
      valid4 = valid4 || _valid0;
      if (!valid4) {
        const err10 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
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
    if (data.overwrite !== void 0) {
      let data2 = data.overwrite;
      const _errs15 = errors;
      let valid5 = false;
      const _errs16 = errors;
      if (typeof data2 !== "boolean") {
        const err11 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid1 = _errs16 === errors;
      valid5 = valid5 || _valid1;
      const _errs18 = errors;
      if (data2 !== null) {
        const err12 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid1 = _errs18 === errors;
      valid5 = valid5 || _valid1;
      if (!valid5) {
        const err13 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
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
    if (data.library !== void 0) {
      let data3 = data.library;
      if (typeof data3 === "string") {
        if (func1(data3) < 1) {
          const err14 = { instancePath: instancePath + "/library", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err14];
          } else {
            vErrors.push(err14);
          }
          errors++;
        }
      } else {
        const err15 = { instancePath: instancePath + "/library", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
    }
    if (data.symbol !== void 0) {
      let data4 = data.symbol;
      if (typeof data4 === "string") {
        if (func1(data4) < 1) {
          const err16 = { instancePath: instancePath + "/symbol", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err16];
          } else {
            vErrors.push(err16);
          }
          errors++;
        }
      } else {
        const err17 = { instancePath: instancePath + "/symbol", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
    }
    if (data.designator !== void 0) {
      let data5 = data.designator;
      if (typeof data5 === "string") {
        if (func1(data5) < 1) {
          const err18 = { instancePath: instancePath + "/designator", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err18];
          } else {
            vErrors.push(err18);
          }
          errors++;
        }
      } else {
        const err19 = { instancePath: instancePath + "/designator", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
    }
    if (data.position_mils !== void 0) {
      let data6 = data.position_mils;
      if (Array.isArray(data6)) {
        if (data6.length > 2) {
          const err20 = { instancePath: instancePath + "/position_mils", schemaPath: "#/$defs/PointMils/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err20];
          } else {
            vErrors.push(err20);
          }
          errors++;
        }
        if (data6.length < 2) {
          const err21 = { instancePath: instancePath + "/position_mils", schemaPath: "#/$defs/PointMils/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err21];
          } else {
            vErrors.push(err21);
          }
          errors++;
        }
        const len0 = data6.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!(typeof data6[i0] == "number")) {
            const err22 = { instancePath: instancePath + "/position_mils/" + i0, schemaPath: "#/$defs/PointMils/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err22];
            } else {
              vErrors.push(err22);
            }
            errors++;
          }
        }
      } else {
        const err23 = { instancePath: instancePath + "/position_mils", schemaPath: "#/$defs/PointMils/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
    }
    if (data.unique_id !== void 0) {
      let data8 = data.unique_id;
      const _errs35 = errors;
      let valid12 = false;
      const _errs36 = errors;
      if (typeof data8 !== "string") {
        const err24 = { instancePath: instancePath + "/unique_id", schemaPath: "#/properties/unique_id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      var _valid2 = _errs36 === errors;
      valid12 = valid12 || _valid2;
      const _errs38 = errors;
      if (data8 !== null) {
        const err25 = { instancePath: instancePath + "/unique_id", schemaPath: "#/properties/unique_id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
      var _valid2 = _errs38 === errors;
      valid12 = valid12 || _valid2;
      if (!valid12) {
        const err26 = { instancePath: instancePath + "/unique_id", schemaPath: "#/properties/unique_id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
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
    if (data.design_item_id !== void 0) {
      let data9 = data.design_item_id;
      const _errs41 = errors;
      let valid13 = false;
      const _errs42 = errors;
      if (typeof data9 !== "string") {
        const err27 = { instancePath: instancePath + "/design_item_id", schemaPath: "#/properties/design_item_id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
      var _valid3 = _errs42 === errors;
      valid13 = valid13 || _valid3;
      const _errs44 = errors;
      if (data9 !== null) {
        const err28 = { instancePath: instancePath + "/design_item_id", schemaPath: "#/properties/design_item_id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
      var _valid3 = _errs44 === errors;
      valid13 = valid13 || _valid3;
      if (!valid13) {
        const err29 = { instancePath: instancePath + "/design_item_id", schemaPath: "#/properties/design_item_id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
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
    if (data.footprint_model !== void 0) {
      let data10 = data.footprint_model;
      const _errs47 = errors;
      let valid14 = false;
      const _errs48 = errors;
      if (typeof data10 !== "string") {
        const err30 = { instancePath: instancePath + "/footprint_model", schemaPath: "#/properties/footprint_model/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
        }
        errors++;
      }
      var _valid4 = _errs48 === errors;
      valid14 = valid14 || _valid4;
      const _errs50 = errors;
      if (data10 !== null) {
        const err31 = { instancePath: instancePath + "/footprint_model", schemaPath: "#/properties/footprint_model/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      }
      var _valid4 = _errs50 === errors;
      valid14 = valid14 || _valid4;
      if (!valid14) {
        const err32 = { instancePath: instancePath + "/footprint_model", schemaPath: "#/properties/footprint_model/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
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
    if (data.footprint_library !== void 0) {
      let data11 = data.footprint_library;
      const _errs53 = errors;
      let valid15 = false;
      const _errs54 = errors;
      if (typeof data11 !== "string") {
        const err33 = { instancePath: instancePath + "/footprint_library", schemaPath: "#/properties/footprint_library/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
      var _valid5 = _errs54 === errors;
      valid15 = valid15 || _valid5;
      const _errs56 = errors;
      if (data11 !== null) {
        const err34 = { instancePath: instancePath + "/footprint_library", schemaPath: "#/properties/footprint_library/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
        }
        errors++;
      }
      var _valid5 = _errs56 === errors;
      valid15 = valid15 || _valid5;
      if (!valid15) {
        const err35 = { instancePath: instancePath + "/footprint_library", schemaPath: "#/properties/footprint_library/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err35];
        } else {
          vErrors.push(err35);
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
    if (data.parameters !== void 0) {
      let data12 = data.parameters;
      const _errs59 = errors;
      let valid16 = false;
      const _errs60 = errors;
      if (data12 && typeof data12 == "object" && !Array.isArray(data12)) {
        for (const key1 in data12) {
          if (typeof data12[key1] !== "string") {
            const err36 = { instancePath: instancePath + "/parameters/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/RecordString/unevaluatedProperties/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err36];
            } else {
              vErrors.push(err36);
            }
            errors++;
          }
        }
      } else {
        const err37 = { instancePath: instancePath + "/parameters", schemaPath: "#/$defs/RecordString/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err37];
        } else {
          vErrors.push(err37);
        }
        errors++;
      }
      var _valid6 = _errs60 === errors;
      valid16 = valid16 || _valid6;
      const _errs66 = errors;
      if (data12 !== null) {
        const err38 = { instancePath: instancePath + "/parameters", schemaPath: "#/properties/parameters/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err38];
        } else {
          vErrors.push(err38);
        }
        errors++;
      }
      var _valid6 = _errs66 === errors;
      valid16 = valid16 || _valid6;
      if (!valid16) {
        const err39 = { instancePath: instancePath + "/parameters", schemaPath: "#/properties/parameters/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err39];
        } else {
          vErrors.push(err39);
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
    if (data.orientation !== void 0) {
      let data14 = data.orientation;
      const _errs69 = errors;
      let valid19 = false;
      const _errs70 = errors;
      if (!(typeof data14 == "number")) {
        const err40 = { instancePath: instancePath + "/orientation", schemaPath: "#/properties/orientation/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err40];
        } else {
          vErrors.push(err40);
        }
        errors++;
      }
      var _valid7 = _errs70 === errors;
      valid19 = valid19 || _valid7;
      const _errs72 = errors;
      if (data14 !== null) {
        const err41 = { instancePath: instancePath + "/orientation", schemaPath: "#/properties/orientation/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err41];
        } else {
          vErrors.push(err41);
        }
        errors++;
      }
      var _valid7 = _errs72 === errors;
      valid19 = valid19 || _valid7;
      if (!valid19) {
        const err42 = { instancePath: instancePath + "/orientation", schemaPath: "#/properties/orientation/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err42];
        } else {
          vErrors.push(err42);
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
    if (data.mirrored !== void 0) {
      let data15 = data.mirrored;
      const _errs75 = errors;
      let valid20 = false;
      const _errs76 = errors;
      if (typeof data15 !== "boolean") {
        const err43 = { instancePath: instancePath + "/mirrored", schemaPath: "#/properties/mirrored/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err43];
        } else {
          vErrors.push(err43);
        }
        errors++;
      }
      var _valid8 = _errs76 === errors;
      valid20 = valid20 || _valid8;
      const _errs78 = errors;
      if (data15 !== null) {
        const err44 = { instancePath: instancePath + "/mirrored", schemaPath: "#/properties/mirrored/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err44];
        } else {
          vErrors.push(err44);
        }
        errors++;
      }
      var _valid8 = _errs78 === errors;
      valid20 = valid20 || _valid8;
      if (!valid20) {
        const err45 = { instancePath: instancePath + "/mirrored", schemaPath: "#/properties/mirrored/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err45];
        } else {
          vErrors.push(err45);
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
    if (data.part_id !== void 0) {
      let data16 = data.part_id;
      const _errs81 = errors;
      let valid21 = false;
      const _errs82 = errors;
      if (!(typeof data16 == "number")) {
        const err46 = { instancePath: instancePath + "/part_id", schemaPath: "#/properties/part_id/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err46];
        } else {
          vErrors.push(err46);
        }
        errors++;
      }
      var _valid9 = _errs82 === errors;
      valid21 = valid21 || _valid9;
      const _errs84 = errors;
      if (data16 !== null) {
        const err47 = { instancePath: instancePath + "/part_id", schemaPath: "#/properties/part_id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err47];
        } else {
          vErrors.push(err47);
        }
        errors++;
      }
      var _valid9 = _errs84 === errors;
      valid21 = valid21 || _valid9;
      if (!valid21) {
        const err48 = { instancePath: instancePath + "/part_id", schemaPath: "#/properties/part_id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err48];
        } else {
          vErrors.push(err48);
        }
        errors++;
      } else {
        errors = _errs81;
        if (vErrors !== null) {
          if (_errs81) {
            vErrors.length = _errs81;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.display_mode !== void 0) {
      let data17 = data.display_mode;
      const _errs87 = errors;
      let valid22 = false;
      const _errs88 = errors;
      if (!(typeof data17 == "number")) {
        const err49 = { instancePath: instancePath + "/display_mode", schemaPath: "#/properties/display_mode/anyOf/0/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err49];
        } else {
          vErrors.push(err49);
        }
        errors++;
      }
      var _valid10 = _errs88 === errors;
      valid22 = valid22 || _valid10;
      const _errs90 = errors;
      if (data17 !== null) {
        const err50 = { instancePath: instancePath + "/display_mode", schemaPath: "#/properties/display_mode/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err50];
        } else {
          vErrors.push(err50);
        }
        errors++;
      }
      var _valid10 = _errs90 === errors;
      valid22 = valid22 || _valid10;
      if (!valid22) {
        const err51 = { instancePath: instancePath + "/display_mode", schemaPath: "#/properties/display_mode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err51];
        } else {
          vErrors.push(err51);
        }
        errors++;
      } else {
        errors = _errs87;
        if (vErrors !== null) {
          if (_errs87) {
            vErrors.length = _errs87;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.designator_style !== void 0) {
      let data18 = data.designator_style;
      const _errs93 = errors;
      let valid23 = false;
      const _errs94 = errors;
      if (!validate162(data18, { instancePath: instancePath + "/designator_style", parentData: data, parentDataProperty: "designator_style", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate162.errors : vErrors.concat(validate162.errors);
        errors = vErrors.length;
      }
      var _valid11 = _errs94 === errors;
      valid23 = valid23 || _valid11;
      const _errs95 = errors;
      if (data18 !== null) {
        const err52 = { instancePath: instancePath + "/designator_style", schemaPath: "#/properties/designator_style/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err52];
        } else {
          vErrors.push(err52);
        }
        errors++;
      }
      var _valid11 = _errs95 === errors;
      valid23 = valid23 || _valid11;
      if (!valid23) {
        const err53 = { instancePath: instancePath + "/designator_style", schemaPath: "#/properties/designator_style/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err53];
        } else {
          vErrors.push(err53);
        }
        errors++;
      } else {
        errors = _errs93;
        if (vErrors !== null) {
          if (_errs93) {
            vErrors.length = _errs93;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.comment_style !== void 0) {
      let data19 = data.comment_style;
      const _errs98 = errors;
      let valid24 = false;
      const _errs99 = errors;
      if (!validate162(data19, { instancePath: instancePath + "/comment_style", parentData: data, parentDataProperty: "comment_style", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate162.errors : vErrors.concat(validate162.errors);
        errors = vErrors.length;
      }
      var _valid12 = _errs99 === errors;
      valid24 = valid24 || _valid12;
      const _errs100 = errors;
      if (data19 !== null) {
        const err54 = { instancePath: instancePath + "/comment_style", schemaPath: "#/properties/comment_style/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err54];
        } else {
          vErrors.push(err54);
        }
        errors++;
      }
      var _valid12 = _errs100 === errors;
      valid24 = valid24 || _valid12;
      if (!valid24) {
        const err55 = { instancePath: instancePath + "/comment_style", schemaPath: "#/properties/comment_style/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err55];
        } else {
          vErrors.push(err55);
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
    if (data.footprint_description !== void 0) {
      let data20 = data.footprint_description;
      const _errs103 = errors;
      let valid25 = false;
      const _errs104 = errors;
      if (typeof data20 !== "string") {
        const err56 = { instancePath: instancePath + "/footprint_description", schemaPath: "#/properties/footprint_description/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err56];
        } else {
          vErrors.push(err56);
        }
        errors++;
      }
      var _valid13 = _errs104 === errors;
      valid25 = valid25 || _valid13;
      const _errs106 = errors;
      if (data20 !== null) {
        const err57 = { instancePath: instancePath + "/footprint_description", schemaPath: "#/properties/footprint_description/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err57];
        } else {
          vErrors.push(err57);
        }
        errors++;
      }
      var _valid13 = _errs106 === errors;
      valid25 = valid25 || _valid13;
      if (!valid25) {
        const err58 = { instancePath: instancePath + "/footprint_description", schemaPath: "#/properties/footprint_description/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err58];
        } else {
          vErrors.push(err58);
        }
        errors++;
      } else {
        errors = _errs103;
        if (vErrors !== null) {
          if (_errs103) {
            vErrors.length = _errs103;
          } else {
            vErrors = null;
          }
        }
      }
    }
  } else {
    const err59 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err59];
    } else {
      vErrors.push(err59);
    }
    errors++;
  }
  validate161.errors = vErrors;
  return errors === 0;
}
validate161.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate160(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate160.evaluated;
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("schdoc.add_component" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "schdoc.add_component" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate161(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate161.errors : vErrors.concat(validate161.errors);
        errors = vErrors.length;
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
  validate160.errors = vErrors;
  return errors === 0;
}
validate160.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate168(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate168.evaluated;
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.text === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "text" }, message: "must have required property 'text'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.location_mils === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "location_mils" }, message: "must have required property 'location_mils'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err4 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err4];
          } else {
            vErrors.push(err4);
          }
          errors++;
        }
      } else {
        const err5 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.output_file !== void 0) {
      let data1 = data.output_file;
      const _errs9 = errors;
      let valid4 = false;
      const _errs10 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      valid4 = valid4 || _valid0;
      const _errs12 = errors;
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid0 = _errs12 === errors;
      valid4 = valid4 || _valid0;
      if (!valid4) {
        const err8 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.overwrite !== void 0) {
      let data2 = data.overwrite;
      const _errs15 = errors;
      let valid5 = false;
      const _errs16 = errors;
      if (typeof data2 !== "boolean") {
        const err9 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid1 = _errs16 === errors;
      valid5 = valid5 || _valid1;
      const _errs18 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid1 = _errs18 === errors;
      valid5 = valid5 || _valid1;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
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
    if (data.text !== void 0) {
      let data3 = data.text;
      if (typeof data3 === "string") {
        if (func1(data3) < 1) {
          const err12 = { instancePath: instancePath + "/text", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err12];
          } else {
            vErrors.push(err12);
          }
          errors++;
        }
      } else {
        const err13 = { instancePath: instancePath + "/text", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.location_mils !== void 0) {
      let data4 = data.location_mils;
      if (Array.isArray(data4)) {
        if (data4.length > 2) {
          const err14 = { instancePath: instancePath + "/location_mils", schemaPath: "#/$defs/PointMils/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err14];
          } else {
            vErrors.push(err14);
          }
          errors++;
        }
        if (data4.length < 2) {
          const err15 = { instancePath: instancePath + "/location_mils", schemaPath: "#/$defs/PointMils/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err15];
          } else {
            vErrors.push(err15);
          }
          errors++;
        }
        const len0 = data4.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!(typeof data4[i0] == "number")) {
            const err16 = { instancePath: instancePath + "/location_mils/" + i0, schemaPath: "#/$defs/PointMils/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err16];
            } else {
              vErrors.push(err16);
            }
            errors++;
          }
        }
      } else {
        const err17 = { instancePath: instancePath + "/location_mils", schemaPath: "#/$defs/PointMils/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
    }
    if (data.orientation !== void 0) {
      let data6 = data.orientation;
      const _errs29 = errors;
      let valid10 = false;
      const _errs30 = errors;
      if (typeof data6 !== "string") {
        const err18 = { instancePath: instancePath + "/orientation", schemaPath: "#/properties/orientation/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
      var _valid2 = _errs30 === errors;
      valid10 = valid10 || _valid2;
      const _errs32 = errors;
      if (!(typeof data6 == "number" && (!(data6 % 1) && !isNaN(data6)))) {
        const err19 = { instancePath: instancePath + "/orientation", schemaPath: "#/properties/orientation/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
      var _valid2 = _errs32 === errors;
      valid10 = valid10 || _valid2;
      const _errs34 = errors;
      if (data6 !== null) {
        const err20 = { instancePath: instancePath + "/orientation", schemaPath: "#/properties/orientation/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      var _valid2 = _errs34 === errors;
      valid10 = valid10 || _valid2;
      if (!valid10) {
        const err21 = { instancePath: instancePath + "/orientation", schemaPath: "#/properties/orientation/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
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
    if (data.justification !== void 0) {
      let data7 = data.justification;
      const _errs37 = errors;
      let valid11 = false;
      const _errs38 = errors;
      if (typeof data7 !== "string") {
        const err22 = { instancePath: instancePath + "/justification", schemaPath: "#/properties/justification/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
      var _valid3 = _errs38 === errors;
      valid11 = valid11 || _valid3;
      const _errs40 = errors;
      if (!(typeof data7 == "number" && (!(data7 % 1) && !isNaN(data7)))) {
        const err23 = { instancePath: instancePath + "/justification", schemaPath: "#/properties/justification/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      var _valid3 = _errs40 === errors;
      valid11 = valid11 || _valid3;
      if (!valid11) {
        const err24 = { instancePath: instancePath + "/justification", schemaPath: "#/properties/justification/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
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
  validate168.errors = vErrors;
  return errors === 0;
}
validate168.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate167(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate167.evaluated;
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("schdoc.add_net_label" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "schdoc.add_net_label" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate168(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate168.errors : vErrors.concat(validate168.errors);
        errors = vErrors.length;
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
  validate167.errors = vErrors;
  return errors === 0;
}
validate167.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate172(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate172.evaluated;
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.text === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "text" }, message: "must have required property 'text'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.location_mils === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "location_mils" }, message: "must have required property 'location_mils'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err4 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err4];
          } else {
            vErrors.push(err4);
          }
          errors++;
        }
      } else {
        const err5 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.output_file !== void 0) {
      let data1 = data.output_file;
      const _errs9 = errors;
      let valid4 = false;
      const _errs10 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      valid4 = valid4 || _valid0;
      const _errs12 = errors;
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid0 = _errs12 === errors;
      valid4 = valid4 || _valid0;
      if (!valid4) {
        const err8 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.overwrite !== void 0) {
      let data2 = data.overwrite;
      const _errs15 = errors;
      let valid5 = false;
      const _errs16 = errors;
      if (typeof data2 !== "boolean") {
        const err9 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid1 = _errs16 === errors;
      valid5 = valid5 || _valid1;
      const _errs18 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid1 = _errs18 === errors;
      valid5 = valid5 || _valid1;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
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
    if (data.text !== void 0) {
      let data3 = data.text;
      if (typeof data3 === "string") {
        if (func1(data3) < 1) {
          const err12 = { instancePath: instancePath + "/text", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err12];
          } else {
            vErrors.push(err12);
          }
          errors++;
        }
      } else {
        const err13 = { instancePath: instancePath + "/text", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.location_mils !== void 0) {
      let data4 = data.location_mils;
      if (Array.isArray(data4)) {
        if (data4.length > 2) {
          const err14 = { instancePath: instancePath + "/location_mils", schemaPath: "#/$defs/PointMils/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err14];
          } else {
            vErrors.push(err14);
          }
          errors++;
        }
        if (data4.length < 2) {
          const err15 = { instancePath: instancePath + "/location_mils", schemaPath: "#/$defs/PointMils/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err15];
          } else {
            vErrors.push(err15);
          }
          errors++;
        }
        const len0 = data4.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!(typeof data4[i0] == "number")) {
            const err16 = { instancePath: instancePath + "/location_mils/" + i0, schemaPath: "#/$defs/PointMils/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err16];
            } else {
              vErrors.push(err16);
            }
            errors++;
          }
        }
      } else {
        const err17 = { instancePath: instancePath + "/location_mils", schemaPath: "#/$defs/PointMils/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
    }
    if (data.style !== void 0) {
      let data6 = data.style;
      const _errs29 = errors;
      let valid10 = false;
      const _errs30 = errors;
      if (typeof data6 !== "string") {
        const err18 = { instancePath: instancePath + "/style", schemaPath: "#/properties/style/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
      var _valid2 = _errs30 === errors;
      valid10 = valid10 || _valid2;
      const _errs32 = errors;
      if (!(typeof data6 == "number" && (!(data6 % 1) && !isNaN(data6)))) {
        const err19 = { instancePath: instancePath + "/style", schemaPath: "#/properties/style/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
      var _valid2 = _errs32 === errors;
      valid10 = valid10 || _valid2;
      if (!valid10) {
        const err20 = { instancePath: instancePath + "/style", schemaPath: "#/properties/style/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
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
    if (data.orientation !== void 0) {
      let data7 = data.orientation;
      const _errs35 = errors;
      let valid11 = false;
      const _errs36 = errors;
      if (typeof data7 !== "string") {
        const err21 = { instancePath: instancePath + "/orientation", schemaPath: "#/properties/orientation/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      var _valid3 = _errs36 === errors;
      valid11 = valid11 || _valid3;
      const _errs38 = errors;
      if (!(typeof data7 == "number" && (!(data7 % 1) && !isNaN(data7)))) {
        const err22 = { instancePath: instancePath + "/orientation", schemaPath: "#/properties/orientation/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
      var _valid3 = _errs38 === errors;
      valid11 = valid11 || _valid3;
      const _errs40 = errors;
      if (data7 !== null) {
        const err23 = { instancePath: instancePath + "/orientation", schemaPath: "#/properties/orientation/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      var _valid3 = _errs40 === errors;
      valid11 = valid11 || _valid3;
      if (!valid11) {
        const err24 = { instancePath: instancePath + "/orientation", schemaPath: "#/properties/orientation/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
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
    if (data.show_net_name !== void 0) {
      let data8 = data.show_net_name;
      const _errs43 = errors;
      let valid12 = false;
      const _errs44 = errors;
      if (typeof data8 !== "boolean") {
        const err25 = { instancePath: instancePath + "/show_net_name", schemaPath: "#/properties/show_net_name/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
      var _valid4 = _errs44 === errors;
      valid12 = valid12 || _valid4;
      const _errs46 = errors;
      if (data8 !== null) {
        const err26 = { instancePath: instancePath + "/show_net_name", schemaPath: "#/properties/show_net_name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
      var _valid4 = _errs46 === errors;
      valid12 = valid12 || _valid4;
      if (!valid12) {
        const err27 = { instancePath: instancePath + "/show_net_name", schemaPath: "#/properties/show_net_name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
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
    }
  } else {
    const err28 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err28];
    } else {
      vErrors.push(err28);
    }
    errors++;
  }
  validate172.errors = vErrors;
  return errors === 0;
}
validate172.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate171(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate171.evaluated;
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("schdoc.add_power_port" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "schdoc.add_power_port" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate172(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate172.errors : vErrors.concat(validate172.errors);
        errors = vErrors.length;
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
  validate171.errors = vErrors;
  return errors === 0;
}
validate171.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate177(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate177.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (Array.isArray(data)) {
    if (data.length < 2) {
      const err0 = { instancePath, schemaPath: "#/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    const len0 = data.length;
    for (let i0 = 0; i0 < len0; i0++) {
      let data0 = data[i0];
      if (Array.isArray(data0)) {
        if (data0.length > 2) {
          const err1 = { instancePath: instancePath + "/" + i0, schemaPath: "#/$defs/PointMils/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err1];
          } else {
            vErrors.push(err1);
          }
          errors++;
        }
        if (data0.length < 2) {
          const err2 = { instancePath: instancePath + "/" + i0, schemaPath: "#/$defs/PointMils/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err2];
          } else {
            vErrors.push(err2);
          }
          errors++;
        }
        const len1 = data0.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (!(typeof data0[i1] == "number")) {
            const err3 = { instancePath: instancePath + "/" + i0 + "/" + i1, schemaPath: "#/$defs/PointMils/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err3];
            } else {
              vErrors.push(err3);
            }
            errors++;
          }
        }
      } else {
        const err4 = { instancePath: instancePath + "/" + i0, schemaPath: "#/$defs/PointMils/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
  } else {
    const err5 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "array" }, message: "must be array" };
    if (vErrors === null) {
      vErrors = [err5];
    } else {
      vErrors.push(err5);
    }
    errors++;
  }
  validate177.errors = vErrors;
  return errors === 0;
}
validate177.evaluated = { "items": true, "dynamicProps": false, "dynamicItems": false };
function validate176(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate176.evaluated;
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.points_mils === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "points_mils" }, message: "must have required property 'points_mils'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err3 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.output_file !== void 0) {
      let data1 = data.output_file;
      const _errs9 = errors;
      let valid4 = false;
      const _errs10 = errors;
      if (typeof data1 !== "string") {
        const err5 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
      valid4 = valid4 || _valid0;
      const _errs12 = errors;
      if (data1 !== null) {
        const err6 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs12 === errors;
      valid4 = valid4 || _valid0;
      if (!valid4) {
        const err7 = { instancePath: instancePath + "/output_file", schemaPath: "#/properties/output_file/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.overwrite !== void 0) {
      let data2 = data.overwrite;
      const _errs15 = errors;
      let valid5 = false;
      const _errs16 = errors;
      if (typeof data2 !== "boolean") {
        const err8 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      var _valid1 = _errs16 === errors;
      valid5 = valid5 || _valid1;
      const _errs18 = errors;
      if (data2 !== null) {
        const err9 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid1 = _errs18 === errors;
      valid5 = valid5 || _valid1;
      if (!valid5) {
        const err10 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
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
    if (data.points_mils !== void 0) {
      if (!validate177(data.points_mils, { instancePath: instancePath + "/points_mils", parentData: data, parentDataProperty: "points_mils", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate177.errors : vErrors.concat(validate177.errors);
        errors = vErrors.length;
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
  validate176.errors = vErrors;
  return errors === 0;
}
validate176.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate175(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate175.evaluated;
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("schdoc.add_wire" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "schdoc.add_wire" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate176(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate176.errors : vErrors.concat(validate176.errors);
        errors = vErrors.length;
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
  validate175.errors = vErrors;
  return errors === 0;
}
validate175.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate183(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate183.evaluated;
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
  validate183.errors = vErrors;
  return errors === 0;
}
validate183.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate182(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate182.evaluated;
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err2 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err2];
          } else {
            vErrors.push(err2);
          }
          errors++;
        }
      } else {
        const err3 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.template !== void 0) {
      let data1 = data.template;
      const _errs9 = errors;
      let valid4 = false;
      const _errs10 = errors;
      if (typeof data1 === "string") {
        if (func1(data1) < 1) {
          const err4 = { instancePath: instancePath + "/template", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err4];
          } else {
            vErrors.push(err4);
          }
          errors++;
        }
      } else {
        const err5 = { instancePath: instancePath + "/template", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err6 = { instancePath: instancePath + "/template", schemaPath: "#/properties/template/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err7 = { instancePath: instancePath + "/template", schemaPath: "#/properties/template/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.sheet_style !== void 0) {
      let data2 = data.sheet_style;
      const _errs16 = errors;
      let valid6 = false;
      const _errs17 = errors;
      if (typeof data2 !== "string") {
        const err8 = { instancePath: instancePath + "/sheet_style", schemaPath: "#/properties/sheet_style/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data2 !== null) {
        const err9 = { instancePath: instancePath + "/sheet_style", schemaPath: "#/properties/sheet_style/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid1 = _errs19 === errors;
      valid6 = valid6 || _valid1;
      if (!valid6) {
        const err10 = { instancePath: instancePath + "/sheet_style", schemaPath: "#/properties/sheet_style/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.apply_template_visual_sheet_settings !== void 0) {
      let data3 = data.apply_template_visual_sheet_settings;
      const _errs22 = errors;
      let valid7 = false;
      const _errs23 = errors;
      if (typeof data3 !== "boolean") {
        const err11 = { instancePath: instancePath + "/apply_template_visual_sheet_settings", schemaPath: "#/properties/apply_template_visual_sheet_settings/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid2 = _errs23 === errors;
      valid7 = valid7 || _valid2;
      const _errs25 = errors;
      if (data3 !== null) {
        const err12 = { instancePath: instancePath + "/apply_template_visual_sheet_settings", schemaPath: "#/properties/apply_template_visual_sheet_settings/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid2 = _errs25 === errors;
      valid7 = valid7 || _valid2;
      if (!valid7) {
        const err13 = { instancePath: instancePath + "/apply_template_visual_sheet_settings", schemaPath: "#/properties/apply_template_visual_sheet_settings/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.custom_sheet_mils !== void 0) {
      let data4 = data.custom_sheet_mils;
      const _errs28 = errors;
      let valid8 = false;
      const _errs29 = errors;
      if (!validate183(data4, { instancePath: instancePath + "/custom_sheet_mils", parentData: data, parentDataProperty: "custom_sheet_mils", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate183.errors : vErrors.concat(validate183.errors);
        errors = vErrors.length;
      }
      var _valid3 = _errs29 === errors;
      valid8 = valid8 || _valid3;
      const _errs30 = errors;
      if (data4 !== null) {
        const err14 = { instancePath: instancePath + "/custom_sheet_mils", schemaPath: "#/properties/custom_sheet_mils/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid3 = _errs30 === errors;
      valid8 = valid8 || _valid3;
      if (!valid8) {
        const err15 = { instancePath: instancePath + "/custom_sheet_mils", schemaPath: "#/properties/custom_sheet_mils/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
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
    if (data.overwrite !== void 0) {
      let data5 = data.overwrite;
      const _errs33 = errors;
      let valid9 = false;
      const _errs34 = errors;
      if (typeof data5 !== "boolean") {
        const err16 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
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
      if (data5 !== null) {
        const err17 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      var _valid4 = _errs36 === errors;
      valid9 = valid9 || _valid4;
      if (!valid9) {
        const err18 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
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
  } else {
    const err19 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err19];
    } else {
      vErrors.push(err19);
    }
    errors++;
  }
  validate182.errors = vErrors;
  return errors === 0;
}
validate182.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate181(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate181.evaluated;
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("schdoc.create" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "schdoc.create" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate182(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate182.errors : vErrors.concat(validate182.errors);
        errors = vErrors.length;
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
  validate181.errors = vErrors;
  return errors === 0;
}
validate181.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate188(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate188.evaluated;
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.name === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err3 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
      } else {
        const err4 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (typeof data1 === "string") {
        if (func1(data1) < 1) {
          const err5 = { instancePath: instancePath + "/name", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err5];
          } else {
            vErrors.push(err5);
          }
          errors++;
        }
      } else {
        const err6 = { instancePath: instancePath + "/name", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.description !== void 0) {
      let data2 = data.description;
      const _errs12 = errors;
      let valid5 = false;
      const _errs13 = errors;
      if (typeof data2 !== "string") {
        const err7 = { instancePath: instancePath + "/description", schemaPath: "#/properties/description/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err8 = { instancePath: instancePath + "/description", schemaPath: "#/properties/description/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err9 = { instancePath: instancePath + "/description", schemaPath: "#/properties/description/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
  } else {
    const err10 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err10];
    } else {
      vErrors.push(err10);
    }
    errors++;
  }
  validate188.errors = vErrors;
  return errors === 0;
}
validate188.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate187(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate187.evaluated;
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("schlib.add_symbol" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "schlib.add_symbol" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate188(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate188.errors : vErrors.concat(validate188.errors);
        errors = vErrors.length;
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
  validate187.errors = vErrors;
  return errors === 0;
}
validate187.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate192(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate192.evaluated;
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
    if (data.file === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.file !== void 0) {
      let data0 = data.file;
      if (typeof data0 === "string") {
        if (func1(data0) < 1) {
          const err2 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err2];
          } else {
            vErrors.push(err2);
          }
          errors++;
        }
      } else {
        const err3 = { instancePath: instancePath + "/file", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.overwrite !== void 0) {
      let data1 = data.overwrite;
      const _errs9 = errors;
      let valid4 = false;
      const _errs10 = errors;
      if (typeof data1 !== "boolean") {
        const err4 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
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
        const err5 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err6 = { instancePath: instancePath + "/overwrite", schemaPath: "#/properties/overwrite/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
  } else {
    const err7 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err7];
    } else {
      vErrors.push(err7);
    }
    errors++;
  }
  validate192.errors = vErrors;
  return errors === 0;
}
validate192.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate191(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate191.evaluated;
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.args === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "args" }, message: "must have required property 'args'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err8 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      var _valid2 = _errs19 === errors;
      valid5 = valid5 || _valid2;
      const _errs21 = errors;
      if (data2 !== null) {
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid2 = _errs21 === errors;
      valid5 = valid5 || _valid2;
      if (!valid5) {
        const err11 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("schlib.create" !== data3) {
        const err13 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/const", keyword: "const", params: { allowedValue: "schlib.create" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.args !== void 0) {
      if (!validate192(data.args, { instancePath: instancePath + "/args", parentData: data, parentDataProperty: "args", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate192.errors : vErrors.concat(validate192.errors);
        errors = vErrors.length;
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
  validate191.errors = vErrors;
  return errors === 0;
}
validate191.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
  const _errs0 = errors;
  let valid0 = false;
  const _errs1 = errors;
  if (!validate23(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate23.errors : vErrors.concat(validate23.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs1 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    var props0 = true;
  }
  const _errs2 = errors;
  if (!validate27(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate27.errors : vErrors.concat(validate27.errors);
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
  if (!validate31(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate31.errors : vErrors.concat(validate31.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs3 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs4 = errors;
  if (!validate35(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate35.errors : vErrors.concat(validate35.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs4 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs5 = errors;
  if (!validate39(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate39.errors : vErrors.concat(validate39.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs5 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs6 = errors;
  if (!validate43(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate43.errors : vErrors.concat(validate43.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs6 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs7 = errors;
  if (!validate51(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate51.errors : vErrors.concat(validate51.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs7 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs8 = errors;
  if (!validate55(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate55.errors : vErrors.concat(validate55.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs8 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs9 = errors;
  if (!validate59(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate59.errors : vErrors.concat(validate59.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs9 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs10 = errors;
  if (!validate64(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate64.errors : vErrors.concat(validate64.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs10 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs11 = errors;
  if (!validate68(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate68.errors : vErrors.concat(validate68.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs11 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs12 = errors;
  if (!validate72(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate72.errors : vErrors.concat(validate72.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs12 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs13 = errors;
  if (!validate76(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate76.errors : vErrors.concat(validate76.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs13 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs14 = errors;
  if (!validate80(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate80.errors : vErrors.concat(validate80.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs14 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs15 = errors;
  if (!validate102(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate102.errors : vErrors.concat(validate102.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs15 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs16 = errors;
  if (!validate106(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate106.errors : vErrors.concat(validate106.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs16 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs17 = errors;
  if (!validate112(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate112.errors : vErrors.concat(validate112.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs17 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs18 = errors;
  if (!validate116(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate116.errors : vErrors.concat(validate116.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs18 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs19 = errors;
  if (!validate120(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate120.errors : vErrors.concat(validate120.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs19 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs20 = errors;
  if (!validate124(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate124.errors : vErrors.concat(validate124.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs20 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs21 = errors;
  if (!validate128(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate128.errors : vErrors.concat(validate128.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs21 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs22 = errors;
  if (!validate132(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate132.errors : vErrors.concat(validate132.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs22 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs23 = errors;
  if (!validate136(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate136.errors : vErrors.concat(validate136.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs23 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs24 = errors;
  if (!validate140(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate140.errors : vErrors.concat(validate140.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs24 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs25 = errors;
  if (!validate144(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate144.errors : vErrors.concat(validate144.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs25 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs26 = errors;
  if (!validate148(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate148.errors : vErrors.concat(validate148.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs26 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs27 = errors;
  if (!validate152(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate152.errors : vErrors.concat(validate152.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs27 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs28 = errors;
  if (!validate156(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate156.errors : vErrors.concat(validate156.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs28 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs29 = errors;
  if (!validate160(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate160.errors : vErrors.concat(validate160.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs29 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs30 = errors;
  if (!validate167(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate167.errors : vErrors.concat(validate167.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs30 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs31 = errors;
  if (!validate171(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate171.errors : vErrors.concat(validate171.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs31 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs32 = errors;
  if (!validate175(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate175.errors : vErrors.concat(validate175.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs32 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs33 = errors;
  if (!validate181(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate181.errors : vErrors.concat(validate181.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs33 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs34 = errors;
  if (!validate187(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate187.errors : vErrors.concat(validate187.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs34 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs35 = errors;
  if (!validate191(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate191.errors : vErrors.concat(validate191.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs35 === errors;
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
  validate22.errors = vErrors;
  evaluated0.props = props0;
  return errors === 0;
}
validate22.evaluated = { "dynamicProps": true, "dynamicItems": false };
function validate196(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate196.evaluated;
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
    if (data.op === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.id !== void 0) {
      let data0 = data.id;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err2 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err3 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err4 = { instancePath: instancePath + "/id", schemaPath: "#/properties/id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.message !== void 0) {
      let data1 = data.message;
      const _errs12 = errors;
      let valid4 = false;
      const _errs13 = errors;
      if (typeof data1 !== "string") {
        const err5 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err6 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.on_fail !== void 0) {
      let data2 = data.on_fail;
      const _errs18 = errors;
      let valid5 = false;
      const _errs19 = errors;
      if (typeof data2 !== "string") {
        const err8 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
        const err9 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err10 = { instancePath: instancePath + "/on_fail", schemaPath: "#/properties/on_fail/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.op !== void 0) {
      let data3 = data.op;
      if (typeof data3 === "string") {
        if (func1(data3) < 1) {
          const err11 = { instancePath: instancePath + "/op", schemaPath: "#/$defs/McoString/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err11];
          } else {
            vErrors.push(err11);
          }
          errors++;
        }
      } else {
        const err12 = { instancePath: instancePath + "/op", schemaPath: "#/$defs/McoString/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      const _errs26 = errors;
      const _errs27 = errors;
      if (!(data3 === "file.copy" || data3 === "mco.fail" || data3 === "fail" || data3 === "mco.message" || data3 === "message" || data3 === "pcbdoc.add_arc" || data3 === "pcbdoc.add_component" || data3 === "pcbdoc.add_embedded_3d_model" || data3 === "pcbdoc.add_fill" || data3 === "pcbdoc.add_pad" || data3 === "pcbdoc.add_region" || data3 === "pcbdoc.add_text" || data3 === "pcbdoc.add_track" || data3 === "pcbdoc.add_via" || data3 === "pcbdoc.arrange_designators" || data3 === "pcbdoc.create" || data3 === "pcbdoc.create_user_union" || data3 === "pcbdoc.export_layer_step" || data3 === "pcblib.add_footprint" || data3 === "pcblib.create" || data3 === "project.add_document" || data3 === "project.add_parameter" || data3 === "project.add_variant" || data3 === "project.add_variant_dnp" || data3 === "project.clone_variant" || data3 === "project.create" || data3 === "project.delete_variant" || data3 === "project.list_variants" || data3 === "project.rename_variant" || data3 === "project.toggle_variant_dnp" || data3 === "schdoc.add_component" || data3 === "schdoc.add_net_label" || data3 === "schdoc.add_power_port" || data3 === "schdoc.add_wire" || data3 === "schdoc.create" || data3 === "schlib.add_symbol" || data3 === "schlib.create")) {
        const err13 = {};
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var valid7 = _errs27 === errors;
      if (valid7) {
        const err14 = { instancePath: instancePath + "/op", schemaPath: "#/properties/op/not", keyword: "not", params: {}, message: "must NOT be valid" };
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
    if (data.args !== void 0) {
      let data4 = data.args;
      if (data4 && typeof data4 == "object" && !Array.isArray(data4)) {
      } else {
        const err15 = { instancePath: instancePath + "/args", schemaPath: "#/$defs/RecordUnknown/type", keyword: "type", params: { type: "object" }, message: "must be object" };
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
  validate196.errors = vErrors;
  return errors === 0;
}
validate196.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.operations === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "operations" }, message: "must have required property 'operations'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.schema !== void 0) {
      let data0 = data.schema;
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err2 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      if ("altium_cruncher.mco.a0" !== data0) {
        const err3 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf/0/const", keyword: "const", params: { allowedValue: "altium_cruncher.mco.a0" }, message: "must be equal to constant" };
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
      if (data0 !== null) {
        const err4 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
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
        const err5 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.operations !== void 0) {
      let data1 = data.operations;
      if (Array.isArray(data1)) {
        const len0 = data1.length;
        for (let i0 = 0; i0 < len0; i0++) {
          let data2 = data1[i0];
          const _errs14 = errors;
          let valid6 = false;
          const _errs15 = errors;
          if (!validate22(data2, { instancePath: instancePath + "/operations/" + i0, parentData: data1, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate22.errors : vErrors.concat(validate22.errors);
            errors = vErrors.length;
          } else {
            var props0 = validate22.evaluated.props;
          }
          var _valid1 = _errs15 === errors;
          valid6 = valid6 || _valid1;
          const _errs16 = errors;
          if (!validate196(data2, { instancePath: instancePath + "/operations/" + i0, parentData: data1, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate196.errors : vErrors.concat(validate196.errors);
            errors = vErrors.length;
          }
          var _valid1 = _errs16 === errors;
          valid6 = valid6 || _valid1;
          if (_valid1) {
            if (props0 !== true) {
              props0 = true;
            }
          }
          if (!valid6) {
            const err6 = { instancePath: instancePath + "/operations/" + i0, schemaPath: "#/properties/operations/items/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err6];
            } else {
              vErrors.push(err6);
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
      } else {
        const err7 = { instancePath: instancePath + "/operations", schemaPath: "#/properties/operations/type", keyword: "type", params: { type: "array" }, message: "must be array" };
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
  if (Array.isArray(data)) {
    const len0 = data.length;
    for (let i0 = 0; i0 < len0; i0++) {
      let data0 = data[i0];
      const _errs6 = errors;
      let valid3 = false;
      const _errs7 = errors;
      if (!validate22(data0, { instancePath: instancePath + "/" + i0, parentData: data, parentDataProperty: i0, rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate22.errors : vErrors.concat(validate22.errors);
        errors = vErrors.length;
      } else {
        var props1 = validate22.evaluated.props;
      }
      var _valid1 = _errs7 === errors;
      valid3 = valid3 || _valid1;
      const _errs8 = errors;
      if (!validate196(data0, { instancePath: instancePath + "/" + i0, parentData: data, parentDataProperty: i0, rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate196.errors : vErrors.concat(validate196.errors);
        errors = vErrors.length;
      }
      var _valid1 = _errs8 === errors;
      valid3 = valid3 || _valid1;
      if (_valid1) {
        if (props1 !== true) {
          props1 = true;
        }
      }
      if (!valid3) {
        const err0 = { instancePath: instancePath + "/" + i0, schemaPath: "#/anyOf/1/items/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err0];
        } else {
          vErrors.push(err0);
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
    const err1 = { instancePath, schemaPath: "#/anyOf/1/type", keyword: "type", params: { type: "array" }, message: "must be array" };
    if (vErrors === null) {
      vErrors = [err1];
    } else {
      vErrors.push(err1);
    }
    errors++;
  }
  var _valid0 = _errs3 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    var items0 = true;
  }
  if (!valid0) {
    const err2 = { instancePath, schemaPath: "#/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
    if (vErrors === null) {
      vErrors = [err2];
    } else {
      vErrors.push(err2);
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
  evaluated0.items = items0;
  return errors === 0;
}
validate20.evaluated = { "dynamicProps": true, "dynamicItems": true };
export {
  validate_default as default,
  validate
};
