// Generated from src/tsp/altium_cruncher/outputs/pcb-routing-context.tsp. Do not edit.
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
    for (const key0 in data) {
      let data0 = data[key0];
      if (!(typeof data0 == "number" && (!(data0 % 1) && !isNaN(data0)))) {
        const err0 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err0];
        } else {
          vErrors.push(err0);
        }
        errors++;
      }
      if (typeof data0 == "number") {
        if (data0 < 0 || isNaN(data0)) {
          const err1 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err1];
          } else {
            vErrors.push(err1);
          }
          errors++;
        }
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
    if (data.net_count === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "net_count" }, message: "must have required property 'net_count'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.net_class_count === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "net_class_count" }, message: "must have required property 'net_class_count'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.differential_pair_count === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "differential_pair_count" }, message: "must have required property 'differential_pair_count'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.differential_pair_class_count === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "differential_pair_class_count" }, message: "must have required property 'differential_pair_class_count'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.rule_count === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "rule_count" }, message: "must have required property 'rule_count'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.enabled_rule_count === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "enabled_rule_count" }, message: "must have required property 'enabled_rule_count'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.rules_by_kind === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "rules_by_kind" }, message: "must have required property 'rules_by_kind'" };
      if (vErrors === null) {
        vErrors = [err6];
      } else {
        vErrors.push(err6);
      }
      errors++;
    }
    if (data.net_count !== void 0) {
      let data0 = data.net_count;
      if (!(typeof data0 == "number" && (!(data0 % 1) && !isNaN(data0)))) {
        const err7 = { instancePath: instancePath + "/net_count", schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      if (typeof data0 == "number") {
        if (data0 < 0 || isNaN(data0)) {
          const err8 = { instancePath: instancePath + "/net_count", schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err8];
          } else {
            vErrors.push(err8);
          }
          errors++;
        }
      }
    }
    if (data.net_class_count !== void 0) {
      let data1 = data.net_class_count;
      if (!(typeof data1 == "number" && (!(data1 % 1) && !isNaN(data1)))) {
        const err9 = { instancePath: instancePath + "/net_class_count", schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      if (typeof data1 == "number") {
        if (data1 < 0 || isNaN(data1)) {
          const err10 = { instancePath: instancePath + "/net_class_count", schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err10];
          } else {
            vErrors.push(err10);
          }
          errors++;
        }
      }
    }
    if (data.differential_pair_count !== void 0) {
      let data2 = data.differential_pair_count;
      if (!(typeof data2 == "number" && (!(data2 % 1) && !isNaN(data2)))) {
        const err11 = { instancePath: instancePath + "/differential_pair_count", schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      if (typeof data2 == "number") {
        if (data2 < 0 || isNaN(data2)) {
          const err12 = { instancePath: instancePath + "/differential_pair_count", schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err12];
          } else {
            vErrors.push(err12);
          }
          errors++;
        }
      }
    }
    if (data.differential_pair_class_count !== void 0) {
      let data3 = data.differential_pair_class_count;
      if (!(typeof data3 == "number" && (!(data3 % 1) && !isNaN(data3)))) {
        const err13 = { instancePath: instancePath + "/differential_pair_class_count", schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      if (typeof data3 == "number") {
        if (data3 < 0 || isNaN(data3)) {
          const err14 = { instancePath: instancePath + "/differential_pair_class_count", schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err14];
          } else {
            vErrors.push(err14);
          }
          errors++;
        }
      }
    }
    if (data.rule_count !== void 0) {
      let data4 = data.rule_count;
      if (!(typeof data4 == "number" && (!(data4 % 1) && !isNaN(data4)))) {
        const err15 = { instancePath: instancePath + "/rule_count", schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      if (typeof data4 == "number") {
        if (data4 < 0 || isNaN(data4)) {
          const err16 = { instancePath: instancePath + "/rule_count", schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err16];
          } else {
            vErrors.push(err16);
          }
          errors++;
        }
      }
    }
    if (data.enabled_rule_count !== void 0) {
      let data5 = data.enabled_rule_count;
      if (!(typeof data5 == "number" && (!(data5 % 1) && !isNaN(data5)))) {
        const err17 = { instancePath: instancePath + "/enabled_rule_count", schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      if (typeof data5 == "number") {
        if (data5 < 0 || isNaN(data5)) {
          const err18 = { instancePath: instancePath + "/enabled_rule_count", schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err18];
          } else {
            vErrors.push(err18);
          }
          errors++;
        }
      }
    }
    if (data.rules_by_kind !== void 0) {
      if (!validate22(data.rules_by_kind, { instancePath: instancePath + "/rules_by_kind", parentData: data, parentDataProperty: "rules_by_kind", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate22.errors : vErrors.concat(validate22.errors);
        errors = vErrors.length;
      }
    }
    for (const key0 in data) {
      if (key0 !== "net_count" && key0 !== "net_class_count" && key0 !== "differential_pair_count" && key0 !== "differential_pair_class_count" && key0 !== "rule_count" && key0 !== "enabled_rule_count" && key0 !== "rules_by_kind") {
        const err19 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
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
  validate21.errors = vErrors;
  return errors === 0;
}
validate21.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.net === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "net" }, message: "must have required property 'net'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.unique_id === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "unique_id" }, message: "must have required property 'unique_id'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.net_classes === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "net_classes" }, message: "must have required property 'net_classes'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.differential_pairs === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "differential_pairs" }, message: "must have required property 'differential_pairs'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.differential_pair_classes === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "differential_pair_classes" }, message: "must have required property 'differential_pair_classes'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.net !== void 0) {
      if (typeof data.net !== "string") {
        const err5 = { instancePath: instancePath + "/net", schemaPath: "#/properties/net/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.unique_id !== void 0) {
      let data1 = data.unique_id;
      const _errs4 = errors;
      let valid1 = false;
      const _errs5 = errors;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/unique_id", schemaPath: "#/properties/unique_id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      var _valid0 = _errs5 === errors;
      valid1 = valid1 || _valid0;
      const _errs7 = errors;
      if (data1 !== null) {
        const err7 = { instancePath: instancePath + "/unique_id", schemaPath: "#/properties/unique_id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid1 = valid1 || _valid0;
      if (!valid1) {
        const err8 = { instancePath: instancePath + "/unique_id", schemaPath: "#/properties/unique_id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
    if (data.net_classes !== void 0) {
      let data2 = data.net_classes;
      if (Array.isArray(data2)) {
        const len0 = data2.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (typeof data2[i0] !== "string") {
            const err9 = { instancePath: instancePath + "/net_classes/" + i0, schemaPath: "#/properties/net_classes/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err9];
            } else {
              vErrors.push(err9);
            }
            errors++;
          }
        }
      } else {
        const err10 = { instancePath: instancePath + "/net_classes", schemaPath: "#/properties/net_classes/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
    }
    if (data.differential_pairs !== void 0) {
      let data4 = data.differential_pairs;
      if (Array.isArray(data4)) {
        const len1 = data4.length;
        for (let i1 = 0; i1 < len1; i1++) {
          let data5 = data4[i1];
          if (data5 && typeof data5 == "object" && !Array.isArray(data5)) {
            if (data5.name === void 0) {
              const err11 = { instancePath: instancePath + "/differential_pairs/" + i1, schemaPath: "#/$defs/DifferentialPairMembership/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
              if (vErrors === null) {
                vErrors = [err11];
              } else {
                vErrors.push(err11);
              }
              errors++;
            }
            if (data5.polarity === void 0) {
              const err12 = { instancePath: instancePath + "/differential_pairs/" + i1, schemaPath: "#/$defs/DifferentialPairMembership/required", keyword: "required", params: { missingProperty: "polarity" }, message: "must have required property 'polarity'" };
              if (vErrors === null) {
                vErrors = [err12];
              } else {
                vErrors.push(err12);
              }
              errors++;
            }
            if (data5.name !== void 0) {
              if (typeof data5.name !== "string") {
                const err13 = { instancePath: instancePath + "/differential_pairs/" + i1 + "/name", schemaPath: "#/$defs/DifferentialPairMembership/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err13];
                } else {
                  vErrors.push(err13);
                }
                errors++;
              }
            }
            if (data5.polarity !== void 0) {
              let data7 = data5.polarity;
              const _errs21 = errors;
              let valid8 = false;
              const _errs22 = errors;
              if (typeof data7 !== "string") {
                const err14 = { instancePath: instancePath + "/differential_pairs/" + i1 + "/polarity", schemaPath: "#/$defs/DifferentialPairMembership/properties/polarity/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err14];
                } else {
                  vErrors.push(err14);
                }
                errors++;
              }
              if ("positive" !== data7) {
                const err15 = { instancePath: instancePath + "/differential_pairs/" + i1 + "/polarity", schemaPath: "#/$defs/DifferentialPairMembership/properties/polarity/anyOf/0/const", keyword: "const", params: { allowedValue: "positive" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err15];
                } else {
                  vErrors.push(err15);
                }
                errors++;
              }
              var _valid1 = _errs22 === errors;
              valid8 = valid8 || _valid1;
              const _errs24 = errors;
              if (typeof data7 !== "string") {
                const err16 = { instancePath: instancePath + "/differential_pairs/" + i1 + "/polarity", schemaPath: "#/$defs/DifferentialPairMembership/properties/polarity/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err16];
                } else {
                  vErrors.push(err16);
                }
                errors++;
              }
              if ("negative" !== data7) {
                const err17 = { instancePath: instancePath + "/differential_pairs/" + i1 + "/polarity", schemaPath: "#/$defs/DifferentialPairMembership/properties/polarity/anyOf/1/const", keyword: "const", params: { allowedValue: "negative" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err17];
                } else {
                  vErrors.push(err17);
                }
                errors++;
              }
              var _valid1 = _errs24 === errors;
              valid8 = valid8 || _valid1;
              if (!valid8) {
                const err18 = { instancePath: instancePath + "/differential_pairs/" + i1 + "/polarity", schemaPath: "#/$defs/DifferentialPairMembership/properties/polarity/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err18];
                } else {
                  vErrors.push(err18);
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
            for (const key0 in data5) {
              if (key0 !== "name" && key0 !== "polarity") {
                const err19 = { instancePath: instancePath + "/differential_pairs/" + i1 + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/DifferentialPairMembership/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err19];
                } else {
                  vErrors.push(err19);
                }
                errors++;
              }
            }
          } else {
            const err20 = { instancePath: instancePath + "/differential_pairs/" + i1, schemaPath: "#/$defs/DifferentialPairMembership/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err20];
            } else {
              vErrors.push(err20);
            }
            errors++;
          }
        }
      } else {
        const err21 = { instancePath: instancePath + "/differential_pairs", schemaPath: "#/properties/differential_pairs/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
    }
    if (data.differential_pair_classes !== void 0) {
      let data9 = data.differential_pair_classes;
      if (Array.isArray(data9)) {
        const len2 = data9.length;
        for (let i2 = 0; i2 < len2; i2++) {
          if (typeof data9[i2] !== "string") {
            const err22 = { instancePath: instancePath + "/differential_pair_classes/" + i2, schemaPath: "#/properties/differential_pair_classes/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err22];
            } else {
              vErrors.push(err22);
            }
            errors++;
          }
        }
      } else {
        const err23 = { instancePath: instancePath + "/differential_pair_classes", schemaPath: "#/properties/differential_pair_classes/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "net" && key1 !== "unique_id" && key1 !== "net_classes" && key1 !== "differential_pairs" && key1 !== "differential_pair_classes") {
        const err24 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
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
    if (data.first === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "first" }, message: "must have required property 'first'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.second === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "second" }, message: "must have required property 'second'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.net_relation === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "net_relation" }, message: "must have required property 'net_relation'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.layer_relation === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "layer_relation" }, message: "must have required property 'layer_relation'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.references === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "references" }, message: "must have required property 'references'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.applicability === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "applicability" }, message: "must have required property 'applicability'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.first !== void 0) {
      if (typeof data.first !== "string") {
        const err6 = { instancePath: instancePath + "/first", schemaPath: "#/properties/first/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.second !== void 0) {
      if (typeof data.second !== "string") {
        const err7 = { instancePath: instancePath + "/second", schemaPath: "#/properties/second/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.net_relation !== void 0) {
      if (typeof data.net_relation !== "string") {
        const err8 = { instancePath: instancePath + "/net_relation", schemaPath: "#/properties/net_relation/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
    if (data.layer_relation !== void 0) {
      if (typeof data.layer_relation !== "string") {
        const err9 = { instancePath: instancePath + "/layer_relation", schemaPath: "#/properties/layer_relation/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    if (data.references !== void 0) {
      let data4 = data.references;
      if (Array.isArray(data4)) {
        const len0 = data4.length;
        for (let i0 = 0; i0 < len0; i0++) {
          let data5 = data4[i0];
          if (data5 && typeof data5 == "object" && !Array.isArray(data5)) {
            if (data5.expression === void 0) {
              const err10 = { instancePath: instancePath + "/references/" + i0, schemaPath: "#/$defs/RuleScopeReference/required", keyword: "required", params: { missingProperty: "expression" }, message: "must have required property 'expression'" };
              if (vErrors === null) {
                vErrors = [err10];
              } else {
                vErrors.push(err10);
              }
              errors++;
            }
            if (data5.function === void 0) {
              const err11 = { instancePath: instancePath + "/references/" + i0, schemaPath: "#/$defs/RuleScopeReference/required", keyword: "required", params: { missingProperty: "function" }, message: "must have required property 'function'" };
              if (vErrors === null) {
                vErrors = [err11];
              } else {
                vErrors.push(err11);
              }
              errors++;
            }
            if (data5.kind === void 0) {
              const err12 = { instancePath: instancePath + "/references/" + i0, schemaPath: "#/$defs/RuleScopeReference/required", keyword: "required", params: { missingProperty: "kind" }, message: "must have required property 'kind'" };
              if (vErrors === null) {
                vErrors = [err12];
              } else {
                vErrors.push(err12);
              }
              errors++;
            }
            if (data5.name === void 0) {
              const err13 = { instancePath: instancePath + "/references/" + i0, schemaPath: "#/$defs/RuleScopeReference/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
              if (vErrors === null) {
                vErrors = [err13];
              } else {
                vErrors.push(err13);
              }
              errors++;
            }
            if (data5.resolution === void 0) {
              const err14 = { instancePath: instancePath + "/references/" + i0, schemaPath: "#/$defs/RuleScopeReference/required", keyword: "required", params: { missingProperty: "resolution" }, message: "must have required property 'resolution'" };
              if (vErrors === null) {
                vErrors = [err14];
              } else {
                vErrors.push(err14);
              }
              errors++;
            }
            if (data5.matched_name === void 0) {
              const err15 = { instancePath: instancePath + "/references/" + i0, schemaPath: "#/$defs/RuleScopeReference/required", keyword: "required", params: { missingProperty: "matched_name" }, message: "must have required property 'matched_name'" };
              if (vErrors === null) {
                vErrors = [err15];
              } else {
                vErrors.push(err15);
              }
              errors++;
            }
            if (data5.matched_unique_id === void 0) {
              const err16 = { instancePath: instancePath + "/references/" + i0, schemaPath: "#/$defs/RuleScopeReference/required", keyword: "required", params: { missingProperty: "matched_unique_id" }, message: "must have required property 'matched_unique_id'" };
              if (vErrors === null) {
                vErrors = [err16];
              } else {
                vErrors.push(err16);
              }
              errors++;
            }
            if (data5.expression !== void 0) {
              let data6 = data5.expression;
              const _errs15 = errors;
              let valid5 = false;
              const _errs16 = errors;
              if (typeof data6 !== "string") {
                const err17 = { instancePath: instancePath + "/references/" + i0 + "/expression", schemaPath: "#/$defs/RuleScopeReference/properties/expression/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err17];
                } else {
                  vErrors.push(err17);
                }
                errors++;
              }
              if ("first" !== data6) {
                const err18 = { instancePath: instancePath + "/references/" + i0 + "/expression", schemaPath: "#/$defs/RuleScopeReference/properties/expression/anyOf/0/const", keyword: "const", params: { allowedValue: "first" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err18];
                } else {
                  vErrors.push(err18);
                }
                errors++;
              }
              var _valid0 = _errs16 === errors;
              valid5 = valid5 || _valid0;
              const _errs18 = errors;
              if (typeof data6 !== "string") {
                const err19 = { instancePath: instancePath + "/references/" + i0 + "/expression", schemaPath: "#/$defs/RuleScopeReference/properties/expression/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err19];
                } else {
                  vErrors.push(err19);
                }
                errors++;
              }
              if ("second" !== data6) {
                const err20 = { instancePath: instancePath + "/references/" + i0 + "/expression", schemaPath: "#/$defs/RuleScopeReference/properties/expression/anyOf/1/const", keyword: "const", params: { allowedValue: "second" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err20];
                } else {
                  vErrors.push(err20);
                }
                errors++;
              }
              var _valid0 = _errs18 === errors;
              valid5 = valid5 || _valid0;
              if (!valid5) {
                const err21 = { instancePath: instancePath + "/references/" + i0 + "/expression", schemaPath: "#/$defs/RuleScopeReference/properties/expression/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err21];
                } else {
                  vErrors.push(err21);
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
            if (data5.function !== void 0) {
              let data7 = data5.function;
              const _errs21 = errors;
              let valid6 = false;
              const _errs22 = errors;
              if (typeof data7 !== "string") {
                const err22 = { instancePath: instancePath + "/references/" + i0 + "/function", schemaPath: "#/$defs/RuleScopeReference/properties/function/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err22];
                } else {
                  vErrors.push(err22);
                }
                errors++;
              }
              if ("InNetClass" !== data7) {
                const err23 = { instancePath: instancePath + "/references/" + i0 + "/function", schemaPath: "#/$defs/RuleScopeReference/properties/function/anyOf/0/const", keyword: "const", params: { allowedValue: "InNetClass" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err23];
                } else {
                  vErrors.push(err23);
                }
                errors++;
              }
              var _valid1 = _errs22 === errors;
              valid6 = valid6 || _valid1;
              const _errs24 = errors;
              if (typeof data7 !== "string") {
                const err24 = { instancePath: instancePath + "/references/" + i0 + "/function", schemaPath: "#/$defs/RuleScopeReference/properties/function/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err24];
                } else {
                  vErrors.push(err24);
                }
                errors++;
              }
              if ("InDifferentialPairClass" !== data7) {
                const err25 = { instancePath: instancePath + "/references/" + i0 + "/function", schemaPath: "#/$defs/RuleScopeReference/properties/function/anyOf/1/const", keyword: "const", params: { allowedValue: "InDifferentialPairClass" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err25];
                } else {
                  vErrors.push(err25);
                }
                errors++;
              }
              var _valid1 = _errs24 === errors;
              valid6 = valid6 || _valid1;
              if (!valid6) {
                const err26 = { instancePath: instancePath + "/references/" + i0 + "/function", schemaPath: "#/$defs/RuleScopeReference/properties/function/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err26];
                } else {
                  vErrors.push(err26);
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
            if (data5.kind !== void 0) {
              let data8 = data5.kind;
              const _errs27 = errors;
              let valid7 = false;
              const _errs28 = errors;
              if (typeof data8 !== "string") {
                const err27 = { instancePath: instancePath + "/references/" + i0 + "/kind", schemaPath: "#/$defs/RuleScopeReference/properties/kind/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err27];
                } else {
                  vErrors.push(err27);
                }
                errors++;
              }
              if ("net_class" !== data8) {
                const err28 = { instancePath: instancePath + "/references/" + i0 + "/kind", schemaPath: "#/$defs/RuleScopeReference/properties/kind/anyOf/0/const", keyword: "const", params: { allowedValue: "net_class" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err28];
                } else {
                  vErrors.push(err28);
                }
                errors++;
              }
              var _valid2 = _errs28 === errors;
              valid7 = valid7 || _valid2;
              const _errs30 = errors;
              if (typeof data8 !== "string") {
                const err29 = { instancePath: instancePath + "/references/" + i0 + "/kind", schemaPath: "#/$defs/RuleScopeReference/properties/kind/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err29];
                } else {
                  vErrors.push(err29);
                }
                errors++;
              }
              if ("differential_pair_class" !== data8) {
                const err30 = { instancePath: instancePath + "/references/" + i0 + "/kind", schemaPath: "#/$defs/RuleScopeReference/properties/kind/anyOf/1/const", keyword: "const", params: { allowedValue: "differential_pair_class" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err30];
                } else {
                  vErrors.push(err30);
                }
                errors++;
              }
              var _valid2 = _errs30 === errors;
              valid7 = valid7 || _valid2;
              if (!valid7) {
                const err31 = { instancePath: instancePath + "/references/" + i0 + "/kind", schemaPath: "#/$defs/RuleScopeReference/properties/kind/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err31];
                } else {
                  vErrors.push(err31);
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
            if (data5.name !== void 0) {
              if (typeof data5.name !== "string") {
                const err32 = { instancePath: instancePath + "/references/" + i0 + "/name", schemaPath: "#/$defs/RuleScopeReference/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err32];
                } else {
                  vErrors.push(err32);
                }
                errors++;
              }
            }
            if (data5.resolution !== void 0) {
              let data10 = data5.resolution;
              const _errs35 = errors;
              let valid8 = false;
              const _errs36 = errors;
              if (typeof data10 !== "string") {
                const err33 = { instancePath: instancePath + "/references/" + i0 + "/resolution", schemaPath: "#/$defs/RuleScopeReference/properties/resolution/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err33];
                } else {
                  vErrors.push(err33);
                }
                errors++;
              }
              if ("resolved" !== data10) {
                const err34 = { instancePath: instancePath + "/references/" + i0 + "/resolution", schemaPath: "#/$defs/RuleScopeReference/properties/resolution/anyOf/0/const", keyword: "const", params: { allowedValue: "resolved" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err34];
                } else {
                  vErrors.push(err34);
                }
                errors++;
              }
              var _valid3 = _errs36 === errors;
              valid8 = valid8 || _valid3;
              const _errs38 = errors;
              if (typeof data10 !== "string") {
                const err35 = { instancePath: instancePath + "/references/" + i0 + "/resolution", schemaPath: "#/$defs/RuleScopeReference/properties/resolution/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err35];
                } else {
                  vErrors.push(err35);
                }
                errors++;
              }
              if ("missing" !== data10) {
                const err36 = { instancePath: instancePath + "/references/" + i0 + "/resolution", schemaPath: "#/$defs/RuleScopeReference/properties/resolution/anyOf/1/const", keyword: "const", params: { allowedValue: "missing" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err36];
                } else {
                  vErrors.push(err36);
                }
                errors++;
              }
              var _valid3 = _errs38 === errors;
              valid8 = valid8 || _valid3;
              const _errs40 = errors;
              if (typeof data10 !== "string") {
                const err37 = { instancePath: instancePath + "/references/" + i0 + "/resolution", schemaPath: "#/$defs/RuleScopeReference/properties/resolution/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err37];
                } else {
                  vErrors.push(err37);
                }
                errors++;
              }
              if ("ambiguous" !== data10) {
                const err38 = { instancePath: instancePath + "/references/" + i0 + "/resolution", schemaPath: "#/$defs/RuleScopeReference/properties/resolution/anyOf/2/const", keyword: "const", params: { allowedValue: "ambiguous" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err38];
                } else {
                  vErrors.push(err38);
                }
                errors++;
              }
              var _valid3 = _errs40 === errors;
              valid8 = valid8 || _valid3;
              if (!valid8) {
                const err39 = { instancePath: instancePath + "/references/" + i0 + "/resolution", schemaPath: "#/$defs/RuleScopeReference/properties/resolution/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err39];
                } else {
                  vErrors.push(err39);
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
            if (data5.matched_name !== void 0) {
              let data11 = data5.matched_name;
              const _errs43 = errors;
              let valid9 = false;
              const _errs44 = errors;
              if (typeof data11 !== "string") {
                const err40 = { instancePath: instancePath + "/references/" + i0 + "/matched_name", schemaPath: "#/$defs/RuleScopeReference/properties/matched_name/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err40];
                } else {
                  vErrors.push(err40);
                }
                errors++;
              }
              var _valid4 = _errs44 === errors;
              valid9 = valid9 || _valid4;
              const _errs46 = errors;
              if (data11 !== null) {
                const err41 = { instancePath: instancePath + "/references/" + i0 + "/matched_name", schemaPath: "#/$defs/RuleScopeReference/properties/matched_name/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
                if (vErrors === null) {
                  vErrors = [err41];
                } else {
                  vErrors.push(err41);
                }
                errors++;
              }
              var _valid4 = _errs46 === errors;
              valid9 = valid9 || _valid4;
              if (!valid9) {
                const err42 = { instancePath: instancePath + "/references/" + i0 + "/matched_name", schemaPath: "#/$defs/RuleScopeReference/properties/matched_name/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err42];
                } else {
                  vErrors.push(err42);
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
            if (data5.matched_unique_id !== void 0) {
              let data12 = data5.matched_unique_id;
              const _errs49 = errors;
              let valid10 = false;
              const _errs50 = errors;
              if (typeof data12 !== "string") {
                const err43 = { instancePath: instancePath + "/references/" + i0 + "/matched_unique_id", schemaPath: "#/$defs/RuleScopeReference/properties/matched_unique_id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err43];
                } else {
                  vErrors.push(err43);
                }
                errors++;
              }
              var _valid5 = _errs50 === errors;
              valid10 = valid10 || _valid5;
              const _errs52 = errors;
              if (data12 !== null) {
                const err44 = { instancePath: instancePath + "/references/" + i0 + "/matched_unique_id", schemaPath: "#/$defs/RuleScopeReference/properties/matched_unique_id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
                if (vErrors === null) {
                  vErrors = [err44];
                } else {
                  vErrors.push(err44);
                }
                errors++;
              }
              var _valid5 = _errs52 === errors;
              valid10 = valid10 || _valid5;
              if (!valid10) {
                const err45 = { instancePath: instancePath + "/references/" + i0 + "/matched_unique_id", schemaPath: "#/$defs/RuleScopeReference/properties/matched_unique_id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err45];
                } else {
                  vErrors.push(err45);
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
            for (const key0 in data5) {
              if (key0 !== "expression" && key0 !== "function" && key0 !== "kind" && key0 !== "name" && key0 !== "resolution" && key0 !== "matched_name" && key0 !== "matched_unique_id") {
                const err46 = { instancePath: instancePath + "/references/" + i0 + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/RuleScopeReference/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err46];
                } else {
                  vErrors.push(err46);
                }
                errors++;
              }
            }
          } else {
            const err47 = { instancePath: instancePath + "/references/" + i0, schemaPath: "#/$defs/RuleScopeReference/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err47];
            } else {
              vErrors.push(err47);
            }
            errors++;
          }
        }
      } else {
        const err48 = { instancePath: instancePath + "/references", schemaPath: "#/properties/references/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err48];
        } else {
          vErrors.push(err48);
        }
        errors++;
      }
    }
    if (data.applicability !== void 0) {
      let data14 = data.applicability;
      if (typeof data14 !== "string") {
        const err49 = { instancePath: instancePath + "/applicability", schemaPath: "#/properties/applicability/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err49];
        } else {
          vErrors.push(err49);
        }
        errors++;
      }
      if ("not_evaluated_by_cruncher" !== data14) {
        const err50 = { instancePath: instancePath + "/applicability", schemaPath: "#/properties/applicability/const", keyword: "const", params: { allowedValue: "not_evaluated_by_cruncher" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err50];
        } else {
          vErrors.push(err50);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "first" && key1 !== "second" && key1 !== "net_relation" && key1 !== "layer_relation" && key1 !== "references" && key1 !== "applicability") {
        const err51 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err51];
        } else {
          vErrors.push(err51);
        }
        errors++;
      }
    }
  } else {
    const err52 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err52];
    } else {
      vErrors.push(err52);
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
    if (data.index === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "index" }, message: "must have required property 'index'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.unique_id === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "unique_id" }, message: "must have required property 'unique_id'" };
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
    if (data.kind === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "kind" }, message: "must have required property 'kind'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.enabled === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "enabled" }, message: "must have required property 'enabled'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.priority === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "priority" }, message: "must have required property 'priority'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.comment === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "comment" }, message: "must have required property 'comment'" };
      if (vErrors === null) {
        vErrors = [err6];
      } else {
        vErrors.push(err6);
      }
      errors++;
    }
    if (data.defined_by_logical_document === void 0) {
      const err7 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "defined_by_logical_document" }, message: "must have required property 'defined_by_logical_document'" };
      if (vErrors === null) {
        vErrors = [err7];
      } else {
        vErrors.push(err7);
      }
      errors++;
    }
    if (data.scope === void 0) {
      const err8 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "scope" }, message: "must have required property 'scope'" };
      if (vErrors === null) {
        vErrors = [err8];
      } else {
        vErrors.push(err8);
      }
      errors++;
    }
    if (data.constraints === void 0) {
      const err9 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "constraints" }, message: "must have required property 'constraints'" };
      if (vErrors === null) {
        vErrors = [err9];
      } else {
        vErrors.push(err9);
      }
      errors++;
    }
    if (data.unmodeled_fields === void 0) {
      const err10 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "unmodeled_fields" }, message: "must have required property 'unmodeled_fields'" };
      if (vErrors === null) {
        vErrors = [err10];
      } else {
        vErrors.push(err10);
      }
      errors++;
    }
    if (data.index !== void 0) {
      let data0 = data.index;
      if (!(typeof data0 == "number" && (!(data0 % 1) && !isNaN(data0)))) {
        const err11 = { instancePath: instancePath + "/index", schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      if (typeof data0 == "number") {
        if (data0 < 0 || isNaN(data0)) {
          const err12 = { instancePath: instancePath + "/index", schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err12];
          } else {
            vErrors.push(err12);
          }
          errors++;
        }
      }
    }
    if (data.unique_id !== void 0) {
      let data1 = data.unique_id;
      const _errs5 = errors;
      let valid2 = false;
      const _errs6 = errors;
      if (typeof data1 !== "string") {
        const err13 = { instancePath: instancePath + "/unique_id", schemaPath: "#/properties/unique_id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      var _valid0 = _errs6 === errors;
      valid2 = valid2 || _valid0;
      const _errs8 = errors;
      if (data1 !== null) {
        const err14 = { instancePath: instancePath + "/unique_id", schemaPath: "#/properties/unique_id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid0 = _errs8 === errors;
      valid2 = valid2 || _valid0;
      if (!valid2) {
        const err15 = { instancePath: instancePath + "/unique_id", schemaPath: "#/properties/unique_id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
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
    if (data.name !== void 0) {
      if (typeof data.name !== "string") {
        const err16 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
    }
    if (data.kind !== void 0) {
      if (typeof data.kind !== "string") {
        const err17 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
    }
    if (data.enabled !== void 0) {
      let data4 = data.enabled;
      const _errs15 = errors;
      let valid3 = false;
      const _errs16 = errors;
      if (typeof data4 !== "boolean") {
        const err18 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
      var _valid1 = _errs16 === errors;
      valid3 = valid3 || _valid1;
      const _errs18 = errors;
      if (data4 !== null) {
        const err19 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
      var _valid1 = _errs18 === errors;
      valid3 = valid3 || _valid1;
      if (!valid3) {
        const err20 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
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
    if (data.priority !== void 0) {
      let data5 = data.priority;
      const _errs21 = errors;
      let valid4 = false;
      const _errs22 = errors;
      if (!(typeof data5 == "number" && (!(data5 % 1) && !isNaN(data5)))) {
        const err21 = { instancePath: instancePath + "/priority", schemaPath: "#/properties/priority/anyOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      var _valid2 = _errs22 === errors;
      valid4 = valid4 || _valid2;
      const _errs24 = errors;
      if (data5 !== null) {
        const err22 = { instancePath: instancePath + "/priority", schemaPath: "#/properties/priority/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
      var _valid2 = _errs24 === errors;
      valid4 = valid4 || _valid2;
      if (!valid4) {
        const err23 = { instancePath: instancePath + "/priority", schemaPath: "#/properties/priority/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
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
    if (data.comment !== void 0) {
      if (typeof data.comment !== "string") {
        const err24 = { instancePath: instancePath + "/comment", schemaPath: "#/properties/comment/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
    }
    if (data.defined_by_logical_document !== void 0) {
      let data7 = data.defined_by_logical_document;
      const _errs29 = errors;
      let valid5 = false;
      const _errs30 = errors;
      if (typeof data7 !== "boolean") {
        const err25 = { instancePath: instancePath + "/defined_by_logical_document", schemaPath: "#/properties/defined_by_logical_document/anyOf/0/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
      var _valid3 = _errs30 === errors;
      valid5 = valid5 || _valid3;
      const _errs32 = errors;
      if (data7 !== null) {
        const err26 = { instancePath: instancePath + "/defined_by_logical_document", schemaPath: "#/properties/defined_by_logical_document/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
      var _valid3 = _errs32 === errors;
      valid5 = valid5 || _valid3;
      if (!valid5) {
        const err27 = { instancePath: instancePath + "/defined_by_logical_document", schemaPath: "#/properties/defined_by_logical_document/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
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
    if (data.scope !== void 0) {
      if (!validate28(data.scope, { instancePath: instancePath + "/scope", parentData: data, parentDataProperty: "scope", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate28.errors : vErrors.concat(validate28.errors);
        errors = vErrors.length;
      }
    }
    if (data.constraints !== void 0) {
      let data9 = data.constraints;
      if (data9 && typeof data9 == "object" && !Array.isArray(data9)) {
      } else {
        const err28 = { instancePath: instancePath + "/constraints", schemaPath: "#/$defs/RecordUnknown/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
    }
    if (data.unmodeled_fields !== void 0) {
      let data10 = data.unmodeled_fields;
      if (data10 && typeof data10 == "object" && !Array.isArray(data10)) {
      } else {
        const err29 = { instancePath: instancePath + "/unmodeled_fields", schemaPath: "#/$defs/RecordUnknown/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      }
    }
    for (const key2 in data) {
      if (key2 !== "index" && key2 !== "unique_id" && key2 !== "name" && key2 !== "kind" && key2 !== "enabled" && key2 !== "priority" && key2 !== "comment" && key2 !== "defined_by_logical_document" && key2 !== "scope" && key2 !== "constraints" && key2 !== "unmodeled_fields") {
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
  validate27.errors = vErrors;
  return errors === 0;
}
validate27.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.code === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "code" }, message: "must have required property 'code'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.severity === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "severity" }, message: "must have required property 'severity'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.source_collection === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "source_collection" }, message: "must have required property 'source_collection'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.code !== void 0) {
      if (typeof data.code !== "string") {
        const err4 = { instancePath: instancePath + "/code", schemaPath: "#/properties/code/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.severity !== void 0) {
      let data1 = data.severity;
      if (typeof data1 !== "string") {
        const err5 = { instancePath: instancePath + "/severity", schemaPath: "#/properties/severity/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      if ("warning" !== data1) {
        const err6 = { instancePath: instancePath + "/severity", schemaPath: "#/properties/severity/const", keyword: "const", params: { allowedValue: "warning" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err7 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.source_collection !== void 0) {
      if (typeof data.source_collection !== "string") {
        const err8 = { instancePath: instancePath + "/source_collection", schemaPath: "#/properties/source_collection/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
    if (data.source_index !== void 0) {
      let data4 = data.source_index;
      if (!(typeof data4 == "number" && (!(data4 % 1) && !isNaN(data4)))) {
        const err9 = { instancePath: instancePath + "/source_index", schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      if (typeof data4 == "number") {
        if (data4 < 0 || isNaN(data4)) {
          const err10 = { instancePath: instancePath + "/source_index", schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err10];
          } else {
            vErrors.push(err10);
          }
          errors++;
        }
      }
    }
    if (data.identity !== void 0) {
      if (typeof data.identity !== "string") {
        const err11 = { instancePath: instancePath + "/identity", schemaPath: "#/properties/identity/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
    }
    for (const key0 in data) {
      if (key0 !== "code" && key0 !== "severity" && key0 !== "message" && key0 !== "source_collection" && key0 !== "source_index" && key0 !== "identity") {
        const err12 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
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
  validate31.errors = vErrors;
  return errors === 0;
}
validate31.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.source === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "source" }, message: "must have required property 'source'" };
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
    if (data.evidence === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "evidence" }, message: "must have required property 'evidence'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.summary === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "summary" }, message: "must have required property 'summary'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.net_classes === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "net_classes" }, message: "must have required property 'net_classes'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.differential_pairs === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "differential_pairs" }, message: "must have required property 'differential_pairs'" };
      if (vErrors === null) {
        vErrors = [err6];
      } else {
        vErrors.push(err6);
      }
      errors++;
    }
    if (data.differential_pair_classes === void 0) {
      const err7 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "differential_pair_classes" }, message: "must have required property 'differential_pair_classes'" };
      if (vErrors === null) {
        vErrors = [err7];
      } else {
        vErrors.push(err7);
      }
      errors++;
    }
    if (data.net_memberships === void 0) {
      const err8 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "net_memberships" }, message: "must have required property 'net_memberships'" };
      if (vErrors === null) {
        vErrors = [err8];
      } else {
        vErrors.push(err8);
      }
      errors++;
    }
    if (data.rules === void 0) {
      const err9 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "rules" }, message: "must have required property 'rules'" };
      if (vErrors === null) {
        vErrors = [err9];
      } else {
        vErrors.push(err9);
      }
      errors++;
    }
    if (data.diagnostics === void 0) {
      const err10 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "diagnostics" }, message: "must have required property 'diagnostics'" };
      if (vErrors === null) {
        vErrors = [err10];
      } else {
        vErrors.push(err10);
      }
      errors++;
    }
    if (data.schema !== void 0) {
      let data0 = data.schema;
      if (typeof data0 !== "string") {
        const err11 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      if ("altium_cruncher.pcb_routing_context.a0" !== data0) {
        const err12 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.pcb_routing_context.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
    }
    if (data.source !== void 0) {
      let data1 = data.source;
      if (typeof data1 === "string") {
        if (func1(data1) < 1) {
          const err13 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/Path/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err13];
          } else {
            vErrors.push(err13);
          }
          errors++;
        }
      } else {
        const err14 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/Path/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
    }
    if (data.board !== void 0) {
      let data2 = data.board;
      const _errs8 = errors;
      let valid2 = false;
      const _errs9 = errors;
      if (typeof data2 !== "string") {
        const err15 = { instancePath: instancePath + "/board", schemaPath: "#/properties/board/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid2 = valid2 || _valid0;
      const _errs11 = errors;
      if (data2 !== null) {
        const err16 = { instancePath: instancePath + "/board", schemaPath: "#/properties/board/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid0 = _errs11 === errors;
      valid2 = valid2 || _valid0;
      if (!valid2) {
        const err17 = { instancePath: instancePath + "/board", schemaPath: "#/properties/board/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
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
    if (data.evidence !== void 0) {
      let data3 = data.evidence;
      if (data3 && typeof data3 == "object" && !Array.isArray(data3)) {
        if (data3.authored_rules === void 0) {
          const err18 = { instancePath: instancePath + "/evidence", schemaPath: "#/$defs/RoutingContextEvidence/required", keyword: "required", params: { missingProperty: "authored_rules" }, message: "must have required property 'authored_rules'" };
          if (vErrors === null) {
            vErrors = [err18];
          } else {
            vErrors.push(err18);
          }
          errors++;
        }
        if (data3.class_membership === void 0) {
          const err19 = { instancePath: instancePath + "/evidence", schemaPath: "#/$defs/RoutingContextEvidence/required", keyword: "required", params: { missingProperty: "class_membership" }, message: "must have required property 'class_membership'" };
          if (vErrors === null) {
            vErrors = [err19];
          } else {
            vErrors.push(err19);
          }
          errors++;
        }
        if (data3.rule_applicability === void 0) {
          const err20 = { instancePath: instancePath + "/evidence", schemaPath: "#/$defs/RoutingContextEvidence/required", keyword: "required", params: { missingProperty: "rule_applicability" }, message: "must have required property 'rule_applicability'" };
          if (vErrors === null) {
            vErrors = [err20];
          } else {
            vErrors.push(err20);
          }
          errors++;
        }
        if (data3.drc_run_by_cruncher === void 0) {
          const err21 = { instancePath: instancePath + "/evidence", schemaPath: "#/$defs/RoutingContextEvidence/required", keyword: "required", params: { missingProperty: "drc_run_by_cruncher" }, message: "must have required property 'drc_run_by_cruncher'" };
          if (vErrors === null) {
            vErrors = [err21];
          } else {
            vErrors.push(err21);
          }
          errors++;
        }
        if (data3.drc_violations === void 0) {
          const err22 = { instancePath: instancePath + "/evidence", schemaPath: "#/$defs/RoutingContextEvidence/required", keyword: "required", params: { missingProperty: "drc_violations" }, message: "must have required property 'drc_violations'" };
          if (vErrors === null) {
            vErrors = [err22];
          } else {
            vErrors.push(err22);
          }
          errors++;
        }
        if (data3.authored_rules !== void 0) {
          let data4 = data3.authored_rules;
          if (typeof data4 !== "string") {
            const err23 = { instancePath: instancePath + "/evidence/authored_rules", schemaPath: "#/$defs/RoutingContextEvidence/properties/authored_rules/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err23];
            } else {
              vErrors.push(err23);
            }
            errors++;
          }
          if ("included" !== data4) {
            const err24 = { instancePath: instancePath + "/evidence/authored_rules", schemaPath: "#/$defs/RoutingContextEvidence/properties/authored_rules/const", keyword: "const", params: { allowedValue: "included" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err24];
            } else {
              vErrors.push(err24);
            }
            errors++;
          }
        }
        if (data3.class_membership !== void 0) {
          let data5 = data3.class_membership;
          if (typeof data5 !== "string") {
            const err25 = { instancePath: instancePath + "/evidence/class_membership", schemaPath: "#/$defs/RoutingContextEvidence/properties/class_membership/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err25];
            } else {
              vErrors.push(err25);
            }
            errors++;
          }
          if ("stored_members_only" !== data5) {
            const err26 = { instancePath: instancePath + "/evidence/class_membership", schemaPath: "#/$defs/RoutingContextEvidence/properties/class_membership/const", keyword: "const", params: { allowedValue: "stored_members_only" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err26];
            } else {
              vErrors.push(err26);
            }
            errors++;
          }
        }
        if (data3.rule_applicability !== void 0) {
          let data6 = data3.rule_applicability;
          if (typeof data6 !== "string") {
            const err27 = { instancePath: instancePath + "/evidence/rule_applicability", schemaPath: "#/$defs/RoutingContextEvidence/properties/rule_applicability/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err27];
            } else {
              vErrors.push(err27);
            }
            errors++;
          }
          if ("not_evaluated_by_cruncher" !== data6) {
            const err28 = { instancePath: instancePath + "/evidence/rule_applicability", schemaPath: "#/$defs/RoutingContextEvidence/properties/rule_applicability/const", keyword: "const", params: { allowedValue: "not_evaluated_by_cruncher" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err28];
            } else {
              vErrors.push(err28);
            }
            errors++;
          }
        }
        if (data3.drc_run_by_cruncher !== void 0) {
          let data7 = data3.drc_run_by_cruncher;
          if (typeof data7 !== "boolean") {
            const err29 = { instancePath: instancePath + "/evidence/drc_run_by_cruncher", schemaPath: "#/$defs/RoutingContextEvidence/properties/drc_run_by_cruncher/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err29];
            } else {
              vErrors.push(err29);
            }
            errors++;
          }
          if (false !== data7) {
            const err30 = { instancePath: instancePath + "/evidence/drc_run_by_cruncher", schemaPath: "#/$defs/RoutingContextEvidence/properties/drc_run_by_cruncher/const", keyword: "const", params: { allowedValue: false }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err30];
            } else {
              vErrors.push(err30);
            }
            errors++;
          }
        }
        if (data3.drc_violations !== void 0) {
          let data8 = data3.drc_violations;
          if (typeof data8 !== "string") {
            const err31 = { instancePath: instancePath + "/evidence/drc_violations", schemaPath: "#/$defs/RoutingContextEvidence/properties/drc_violations/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err31];
            } else {
              vErrors.push(err31);
            }
            errors++;
          }
          if ("not_included" !== data8) {
            const err32 = { instancePath: instancePath + "/evidence/drc_violations", schemaPath: "#/$defs/RoutingContextEvidence/properties/drc_violations/const", keyword: "const", params: { allowedValue: "not_included" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err32];
            } else {
              vErrors.push(err32);
            }
            errors++;
          }
        }
        for (const key0 in data3) {
          if (key0 !== "authored_rules" && key0 !== "class_membership" && key0 !== "rule_applicability" && key0 !== "drc_run_by_cruncher" && key0 !== "drc_violations") {
            const err33 = { instancePath: instancePath + "/evidence/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/RoutingContextEvidence/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err33];
            } else {
              vErrors.push(err33);
            }
            errors++;
          }
        }
      } else {
        const err34 = { instancePath: instancePath + "/evidence", schemaPath: "#/$defs/RoutingContextEvidence/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
        }
        errors++;
      }
    }
    if (data.summary !== void 0) {
      if (!validate21(data.summary, { instancePath: instancePath + "/summary", parentData: data, parentDataProperty: "summary", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
        errors = vErrors.length;
      }
    }
    if (data.net_classes !== void 0) {
      let data11 = data.net_classes;
      if (Array.isArray(data11)) {
        const len0 = data11.length;
        for (let i0 = 0; i0 < len0; i0++) {
          let data12 = data11[i0];
          if (data12 && typeof data12 == "object" && !Array.isArray(data12)) {
            if (data12.name === void 0) {
              const err35 = { instancePath: instancePath + "/net_classes/" + i0, schemaPath: "#/$defs/NetClass/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
              if (vErrors === null) {
                vErrors = [err35];
              } else {
                vErrors.push(err35);
              }
              errors++;
            }
            if (data12.unique_id === void 0) {
              const err36 = { instancePath: instancePath + "/net_classes/" + i0, schemaPath: "#/$defs/NetClass/required", keyword: "required", params: { missingProperty: "unique_id" }, message: "must have required property 'unique_id'" };
              if (vErrors === null) {
                vErrors = [err36];
              } else {
                vErrors.push(err36);
              }
              errors++;
            }
            if (data12.enabled === void 0) {
              const err37 = { instancePath: instancePath + "/net_classes/" + i0, schemaPath: "#/$defs/NetClass/required", keyword: "required", params: { missingProperty: "enabled" }, message: "must have required property 'enabled'" };
              if (vErrors === null) {
                vErrors = [err37];
              } else {
                vErrors.push(err37);
              }
              errors++;
            }
            if (data12.stored_members === void 0) {
              const err38 = { instancePath: instancePath + "/net_classes/" + i0, schemaPath: "#/$defs/NetClass/required", keyword: "required", params: { missingProperty: "stored_members" }, message: "must have required property 'stored_members'" };
              if (vErrors === null) {
                vErrors = [err38];
              } else {
                vErrors.push(err38);
              }
              errors++;
            }
            if (data12.resolved_nets === void 0) {
              const err39 = { instancePath: instancePath + "/net_classes/" + i0, schemaPath: "#/$defs/NetClass/required", keyword: "required", params: { missingProperty: "resolved_nets" }, message: "must have required property 'resolved_nets'" };
              if (vErrors === null) {
                vErrors = [err39];
              } else {
                vErrors.push(err39);
              }
              errors++;
            }
            if (data12.unresolved_members === void 0) {
              const err40 = { instancePath: instancePath + "/net_classes/" + i0, schemaPath: "#/$defs/NetClass/required", keyword: "required", params: { missingProperty: "unresolved_members" }, message: "must have required property 'unresolved_members'" };
              if (vErrors === null) {
                vErrors = [err40];
              } else {
                vErrors.push(err40);
              }
              errors++;
            }
            if (data12.name !== void 0) {
              if (typeof data12.name !== "string") {
                const err41 = { instancePath: instancePath + "/net_classes/" + i0 + "/name", schemaPath: "#/$defs/NetClass/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err41];
                } else {
                  vErrors.push(err41);
                }
                errors++;
              }
            }
            if (data12.unique_id !== void 0) {
              let data14 = data12.unique_id;
              const _errs38 = errors;
              let valid10 = false;
              const _errs39 = errors;
              if (typeof data14 !== "string") {
                const err42 = { instancePath: instancePath + "/net_classes/" + i0 + "/unique_id", schemaPath: "#/$defs/NetClass/properties/unique_id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err42];
                } else {
                  vErrors.push(err42);
                }
                errors++;
              }
              var _valid1 = _errs39 === errors;
              valid10 = valid10 || _valid1;
              const _errs41 = errors;
              if (data14 !== null) {
                const err43 = { instancePath: instancePath + "/net_classes/" + i0 + "/unique_id", schemaPath: "#/$defs/NetClass/properties/unique_id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
                if (vErrors === null) {
                  vErrors = [err43];
                } else {
                  vErrors.push(err43);
                }
                errors++;
              }
              var _valid1 = _errs41 === errors;
              valid10 = valid10 || _valid1;
              if (!valid10) {
                const err44 = { instancePath: instancePath + "/net_classes/" + i0 + "/unique_id", schemaPath: "#/$defs/NetClass/properties/unique_id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err44];
                } else {
                  vErrors.push(err44);
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
            if (data12.enabled !== void 0) {
              if (typeof data12.enabled !== "boolean") {
                const err45 = { instancePath: instancePath + "/net_classes/" + i0 + "/enabled", schemaPath: "#/$defs/NetClass/properties/enabled/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
                if (vErrors === null) {
                  vErrors = [err45];
                } else {
                  vErrors.push(err45);
                }
                errors++;
              }
            }
            if (data12.stored_members !== void 0) {
              let data16 = data12.stored_members;
              if (Array.isArray(data16)) {
                const len1 = data16.length;
                for (let i1 = 0; i1 < len1; i1++) {
                  if (typeof data16[i1] !== "string") {
                    const err46 = { instancePath: instancePath + "/net_classes/" + i0 + "/stored_members/" + i1, schemaPath: "#/$defs/NetClass/properties/stored_members/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                    if (vErrors === null) {
                      vErrors = [err46];
                    } else {
                      vErrors.push(err46);
                    }
                    errors++;
                  }
                }
              } else {
                const err47 = { instancePath: instancePath + "/net_classes/" + i0 + "/stored_members", schemaPath: "#/$defs/NetClass/properties/stored_members/type", keyword: "type", params: { type: "array" }, message: "must be array" };
                if (vErrors === null) {
                  vErrors = [err47];
                } else {
                  vErrors.push(err47);
                }
                errors++;
              }
            }
            if (data12.resolved_nets !== void 0) {
              let data18 = data12.resolved_nets;
              if (Array.isArray(data18)) {
                const len2 = data18.length;
                for (let i2 = 0; i2 < len2; i2++) {
                  if (typeof data18[i2] !== "string") {
                    const err48 = { instancePath: instancePath + "/net_classes/" + i0 + "/resolved_nets/" + i2, schemaPath: "#/$defs/NetClass/properties/resolved_nets/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                    if (vErrors === null) {
                      vErrors = [err48];
                    } else {
                      vErrors.push(err48);
                    }
                    errors++;
                  }
                }
              } else {
                const err49 = { instancePath: instancePath + "/net_classes/" + i0 + "/resolved_nets", schemaPath: "#/$defs/NetClass/properties/resolved_nets/type", keyword: "type", params: { type: "array" }, message: "must be array" };
                if (vErrors === null) {
                  vErrors = [err49];
                } else {
                  vErrors.push(err49);
                }
                errors++;
              }
            }
            if (data12.unresolved_members !== void 0) {
              let data20 = data12.unresolved_members;
              if (Array.isArray(data20)) {
                const len3 = data20.length;
                for (let i3 = 0; i3 < len3; i3++) {
                  if (typeof data20[i3] !== "string") {
                    const err50 = { instancePath: instancePath + "/net_classes/" + i0 + "/unresolved_members/" + i3, schemaPath: "#/$defs/NetClass/properties/unresolved_members/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                    if (vErrors === null) {
                      vErrors = [err50];
                    } else {
                      vErrors.push(err50);
                    }
                    errors++;
                  }
                }
              } else {
                const err51 = { instancePath: instancePath + "/net_classes/" + i0 + "/unresolved_members", schemaPath: "#/$defs/NetClass/properties/unresolved_members/type", keyword: "type", params: { type: "array" }, message: "must be array" };
                if (vErrors === null) {
                  vErrors = [err51];
                } else {
                  vErrors.push(err51);
                }
                errors++;
              }
            }
            for (const key1 in data12) {
              if (key1 !== "name" && key1 !== "unique_id" && key1 !== "enabled" && key1 !== "stored_members" && key1 !== "resolved_nets" && key1 !== "unresolved_members") {
                const err52 = { instancePath: instancePath + "/net_classes/" + i0 + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/NetClass/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err52];
                } else {
                  vErrors.push(err52);
                }
                errors++;
              }
            }
          } else {
            const err53 = { instancePath: instancePath + "/net_classes/" + i0, schemaPath: "#/$defs/NetClass/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err53];
            } else {
              vErrors.push(err53);
            }
            errors++;
          }
        }
      } else {
        const err54 = { instancePath: instancePath + "/net_classes", schemaPath: "#/properties/net_classes/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err54];
        } else {
          vErrors.push(err54);
        }
        errors++;
      }
    }
    if (data.differential_pairs !== void 0) {
      let data23 = data.differential_pairs;
      if (Array.isArray(data23)) {
        const len4 = data23.length;
        for (let i4 = 0; i4 < len4; i4++) {
          let data24 = data23[i4];
          if (data24 && typeof data24 == "object" && !Array.isArray(data24)) {
            if (data24.name === void 0) {
              const err55 = { instancePath: instancePath + "/differential_pairs/" + i4, schemaPath: "#/$defs/DifferentialPair/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
              if (vErrors === null) {
                vErrors = [err55];
              } else {
                vErrors.push(err55);
              }
              errors++;
            }
            if (data24.unique_id === void 0) {
              const err56 = { instancePath: instancePath + "/differential_pairs/" + i4, schemaPath: "#/$defs/DifferentialPair/required", keyword: "required", params: { missingProperty: "unique_id" }, message: "must have required property 'unique_id'" };
              if (vErrors === null) {
                vErrors = [err56];
              } else {
                vErrors.push(err56);
              }
              errors++;
            }
            if (data24.positive_net === void 0) {
              const err57 = { instancePath: instancePath + "/differential_pairs/" + i4, schemaPath: "#/$defs/DifferentialPair/required", keyword: "required", params: { missingProperty: "positive_net" }, message: "must have required property 'positive_net'" };
              if (vErrors === null) {
                vErrors = [err57];
              } else {
                vErrors.push(err57);
              }
              errors++;
            }
            if (data24.negative_net === void 0) {
              const err58 = { instancePath: instancePath + "/differential_pairs/" + i4, schemaPath: "#/$defs/DifferentialPair/required", keyword: "required", params: { missingProperty: "negative_net" }, message: "must have required property 'negative_net'" };
              if (vErrors === null) {
                vErrors = [err58];
              } else {
                vErrors.push(err58);
              }
              errors++;
            }
            if (data24.stored_classes === void 0) {
              const err59 = { instancePath: instancePath + "/differential_pairs/" + i4, schemaPath: "#/$defs/DifferentialPair/required", keyword: "required", params: { missingProperty: "stored_classes" }, message: "must have required property 'stored_classes'" };
              if (vErrors === null) {
                vErrors = [err59];
              } else {
                vErrors.push(err59);
              }
              errors++;
            }
            if (data24.name !== void 0) {
              if (typeof data24.name !== "string") {
                const err60 = { instancePath: instancePath + "/differential_pairs/" + i4 + "/name", schemaPath: "#/$defs/DifferentialPair/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err60];
                } else {
                  vErrors.push(err60);
                }
                errors++;
              }
            }
            if (data24.unique_id !== void 0) {
              let data26 = data24.unique_id;
              const _errs68 = errors;
              let valid22 = false;
              const _errs69 = errors;
              if (typeof data26 !== "string") {
                const err61 = { instancePath: instancePath + "/differential_pairs/" + i4 + "/unique_id", schemaPath: "#/$defs/DifferentialPair/properties/unique_id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err61];
                } else {
                  vErrors.push(err61);
                }
                errors++;
              }
              var _valid2 = _errs69 === errors;
              valid22 = valid22 || _valid2;
              const _errs71 = errors;
              if (data26 !== null) {
                const err62 = { instancePath: instancePath + "/differential_pairs/" + i4 + "/unique_id", schemaPath: "#/$defs/DifferentialPair/properties/unique_id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
                if (vErrors === null) {
                  vErrors = [err62];
                } else {
                  vErrors.push(err62);
                }
                errors++;
              }
              var _valid2 = _errs71 === errors;
              valid22 = valid22 || _valid2;
              if (!valid22) {
                const err63 = { instancePath: instancePath + "/differential_pairs/" + i4 + "/unique_id", schemaPath: "#/$defs/DifferentialPair/properties/unique_id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err63];
                } else {
                  vErrors.push(err63);
                }
                errors++;
              } else {
                errors = _errs68;
                if (vErrors !== null) {
                  if (_errs68) {
                    vErrors.length = _errs68;
                  } else {
                    vErrors = null;
                  }
                }
              }
            }
            if (data24.positive_net !== void 0) {
              if (typeof data24.positive_net !== "string") {
                const err64 = { instancePath: instancePath + "/differential_pairs/" + i4 + "/positive_net", schemaPath: "#/$defs/DifferentialPair/properties/positive_net/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err64];
                } else {
                  vErrors.push(err64);
                }
                errors++;
              }
            }
            if (data24.negative_net !== void 0) {
              if (typeof data24.negative_net !== "string") {
                const err65 = { instancePath: instancePath + "/differential_pairs/" + i4 + "/negative_net", schemaPath: "#/$defs/DifferentialPair/properties/negative_net/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err65];
                } else {
                  vErrors.push(err65);
                }
                errors++;
              }
            }
            if (data24.stored_classes !== void 0) {
              let data29 = data24.stored_classes;
              if (Array.isArray(data29)) {
                const len5 = data29.length;
                for (let i5 = 0; i5 < len5; i5++) {
                  if (typeof data29[i5] !== "string") {
                    const err66 = { instancePath: instancePath + "/differential_pairs/" + i4 + "/stored_classes/" + i5, schemaPath: "#/$defs/DifferentialPair/properties/stored_classes/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                    if (vErrors === null) {
                      vErrors = [err66];
                    } else {
                      vErrors.push(err66);
                    }
                    errors++;
                  }
                }
              } else {
                const err67 = { instancePath: instancePath + "/differential_pairs/" + i4 + "/stored_classes", schemaPath: "#/$defs/DifferentialPair/properties/stored_classes/type", keyword: "type", params: { type: "array" }, message: "must be array" };
                if (vErrors === null) {
                  vErrors = [err67];
                } else {
                  vErrors.push(err67);
                }
                errors++;
              }
            }
            for (const key2 in data24) {
              if (key2 !== "name" && key2 !== "unique_id" && key2 !== "positive_net" && key2 !== "negative_net" && key2 !== "stored_classes") {
                const err68 = { instancePath: instancePath + "/differential_pairs/" + i4 + "/" + key2.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/DifferentialPair/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err68];
                } else {
                  vErrors.push(err68);
                }
                errors++;
              }
            }
          } else {
            const err69 = { instancePath: instancePath + "/differential_pairs/" + i4, schemaPath: "#/$defs/DifferentialPair/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err69];
            } else {
              vErrors.push(err69);
            }
            errors++;
          }
        }
      } else {
        const err70 = { instancePath: instancePath + "/differential_pairs", schemaPath: "#/properties/differential_pairs/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err70];
        } else {
          vErrors.push(err70);
        }
        errors++;
      }
    }
    if (data.differential_pair_classes !== void 0) {
      let data32 = data.differential_pair_classes;
      if (Array.isArray(data32)) {
        const len6 = data32.length;
        for (let i6 = 0; i6 < len6; i6++) {
          let data33 = data32[i6];
          if (data33 && typeof data33 == "object" && !Array.isArray(data33)) {
            if (data33.name === void 0) {
              const err71 = { instancePath: instancePath + "/differential_pair_classes/" + i6, schemaPath: "#/$defs/DifferentialPairClass/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
              if (vErrors === null) {
                vErrors = [err71];
              } else {
                vErrors.push(err71);
              }
              errors++;
            }
            if (data33.unique_id === void 0) {
              const err72 = { instancePath: instancePath + "/differential_pair_classes/" + i6, schemaPath: "#/$defs/DifferentialPairClass/required", keyword: "required", params: { missingProperty: "unique_id" }, message: "must have required property 'unique_id'" };
              if (vErrors === null) {
                vErrors = [err72];
              } else {
                vErrors.push(err72);
              }
              errors++;
            }
            if (data33.enabled === void 0) {
              const err73 = { instancePath: instancePath + "/differential_pair_classes/" + i6, schemaPath: "#/$defs/DifferentialPairClass/required", keyword: "required", params: { missingProperty: "enabled" }, message: "must have required property 'enabled'" };
              if (vErrors === null) {
                vErrors = [err73];
              } else {
                vErrors.push(err73);
              }
              errors++;
            }
            if (data33.stored_members === void 0) {
              const err74 = { instancePath: instancePath + "/differential_pair_classes/" + i6, schemaPath: "#/$defs/DifferentialPairClass/required", keyword: "required", params: { missingProperty: "stored_members" }, message: "must have required property 'stored_members'" };
              if (vErrors === null) {
                vErrors = [err74];
              } else {
                vErrors.push(err74);
              }
              errors++;
            }
            if (data33.resolved_pairs === void 0) {
              const err75 = { instancePath: instancePath + "/differential_pair_classes/" + i6, schemaPath: "#/$defs/DifferentialPairClass/required", keyword: "required", params: { missingProperty: "resolved_pairs" }, message: "must have required property 'resolved_pairs'" };
              if (vErrors === null) {
                vErrors = [err75];
              } else {
                vErrors.push(err75);
              }
              errors++;
            }
            if (data33.resolved_nets === void 0) {
              const err76 = { instancePath: instancePath + "/differential_pair_classes/" + i6, schemaPath: "#/$defs/DifferentialPairClass/required", keyword: "required", params: { missingProperty: "resolved_nets" }, message: "must have required property 'resolved_nets'" };
              if (vErrors === null) {
                vErrors = [err76];
              } else {
                vErrors.push(err76);
              }
              errors++;
            }
            if (data33.unresolved_members === void 0) {
              const err77 = { instancePath: instancePath + "/differential_pair_classes/" + i6, schemaPath: "#/$defs/DifferentialPairClass/required", keyword: "required", params: { missingProperty: "unresolved_members" }, message: "must have required property 'unresolved_members'" };
              if (vErrors === null) {
                vErrors = [err77];
              } else {
                vErrors.push(err77);
              }
              errors++;
            }
            if (data33.name !== void 0) {
              if (typeof data33.name !== "string") {
                const err78 = { instancePath: instancePath + "/differential_pair_classes/" + i6 + "/name", schemaPath: "#/$defs/DifferentialPairClass/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err78];
                } else {
                  vErrors.push(err78);
                }
                errors++;
              }
            }
            if (data33.unique_id !== void 0) {
              let data35 = data33.unique_id;
              const _errs92 = errors;
              let valid30 = false;
              const _errs93 = errors;
              if (typeof data35 !== "string") {
                const err79 = { instancePath: instancePath + "/differential_pair_classes/" + i6 + "/unique_id", schemaPath: "#/$defs/DifferentialPairClass/properties/unique_id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err79];
                } else {
                  vErrors.push(err79);
                }
                errors++;
              }
              var _valid3 = _errs93 === errors;
              valid30 = valid30 || _valid3;
              const _errs95 = errors;
              if (data35 !== null) {
                const err80 = { instancePath: instancePath + "/differential_pair_classes/" + i6 + "/unique_id", schemaPath: "#/$defs/DifferentialPairClass/properties/unique_id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
                if (vErrors === null) {
                  vErrors = [err80];
                } else {
                  vErrors.push(err80);
                }
                errors++;
              }
              var _valid3 = _errs95 === errors;
              valid30 = valid30 || _valid3;
              if (!valid30) {
                const err81 = { instancePath: instancePath + "/differential_pair_classes/" + i6 + "/unique_id", schemaPath: "#/$defs/DifferentialPairClass/properties/unique_id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err81];
                } else {
                  vErrors.push(err81);
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
            }
            if (data33.enabled !== void 0) {
              if (typeof data33.enabled !== "boolean") {
                const err82 = { instancePath: instancePath + "/differential_pair_classes/" + i6 + "/enabled", schemaPath: "#/$defs/DifferentialPairClass/properties/enabled/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
                if (vErrors === null) {
                  vErrors = [err82];
                } else {
                  vErrors.push(err82);
                }
                errors++;
              }
            }
            if (data33.stored_members !== void 0) {
              let data37 = data33.stored_members;
              if (Array.isArray(data37)) {
                const len7 = data37.length;
                for (let i7 = 0; i7 < len7; i7++) {
                  if (typeof data37[i7] !== "string") {
                    const err83 = { instancePath: instancePath + "/differential_pair_classes/" + i6 + "/stored_members/" + i7, schemaPath: "#/$defs/DifferentialPairClass/properties/stored_members/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                    if (vErrors === null) {
                      vErrors = [err83];
                    } else {
                      vErrors.push(err83);
                    }
                    errors++;
                  }
                }
              } else {
                const err84 = { instancePath: instancePath + "/differential_pair_classes/" + i6 + "/stored_members", schemaPath: "#/$defs/DifferentialPairClass/properties/stored_members/type", keyword: "type", params: { type: "array" }, message: "must be array" };
                if (vErrors === null) {
                  vErrors = [err84];
                } else {
                  vErrors.push(err84);
                }
                errors++;
              }
            }
            if (data33.resolved_pairs !== void 0) {
              let data39 = data33.resolved_pairs;
              if (Array.isArray(data39)) {
                const len8 = data39.length;
                for (let i8 = 0; i8 < len8; i8++) {
                  if (typeof data39[i8] !== "string") {
                    const err85 = { instancePath: instancePath + "/differential_pair_classes/" + i6 + "/resolved_pairs/" + i8, schemaPath: "#/$defs/DifferentialPairClass/properties/resolved_pairs/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                    if (vErrors === null) {
                      vErrors = [err85];
                    } else {
                      vErrors.push(err85);
                    }
                    errors++;
                  }
                }
              } else {
                const err86 = { instancePath: instancePath + "/differential_pair_classes/" + i6 + "/resolved_pairs", schemaPath: "#/$defs/DifferentialPairClass/properties/resolved_pairs/type", keyword: "type", params: { type: "array" }, message: "must be array" };
                if (vErrors === null) {
                  vErrors = [err86];
                } else {
                  vErrors.push(err86);
                }
                errors++;
              }
            }
            if (data33.resolved_nets !== void 0) {
              let data41 = data33.resolved_nets;
              if (Array.isArray(data41)) {
                const len9 = data41.length;
                for (let i9 = 0; i9 < len9; i9++) {
                  if (typeof data41[i9] !== "string") {
                    const err87 = { instancePath: instancePath + "/differential_pair_classes/" + i6 + "/resolved_nets/" + i9, schemaPath: "#/$defs/DifferentialPairClass/properties/resolved_nets/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                    if (vErrors === null) {
                      vErrors = [err87];
                    } else {
                      vErrors.push(err87);
                    }
                    errors++;
                  }
                }
              } else {
                const err88 = { instancePath: instancePath + "/differential_pair_classes/" + i6 + "/resolved_nets", schemaPath: "#/$defs/DifferentialPairClass/properties/resolved_nets/type", keyword: "type", params: { type: "array" }, message: "must be array" };
                if (vErrors === null) {
                  vErrors = [err88];
                } else {
                  vErrors.push(err88);
                }
                errors++;
              }
            }
            if (data33.unresolved_members !== void 0) {
              let data43 = data33.unresolved_members;
              if (Array.isArray(data43)) {
                const len10 = data43.length;
                for (let i10 = 0; i10 < len10; i10++) {
                  if (typeof data43[i10] !== "string") {
                    const err89 = { instancePath: instancePath + "/differential_pair_classes/" + i6 + "/unresolved_members/" + i10, schemaPath: "#/$defs/DifferentialPairClass/properties/unresolved_members/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                    if (vErrors === null) {
                      vErrors = [err89];
                    } else {
                      vErrors.push(err89);
                    }
                    errors++;
                  }
                }
              } else {
                const err90 = { instancePath: instancePath + "/differential_pair_classes/" + i6 + "/unresolved_members", schemaPath: "#/$defs/DifferentialPairClass/properties/unresolved_members/type", keyword: "type", params: { type: "array" }, message: "must be array" };
                if (vErrors === null) {
                  vErrors = [err90];
                } else {
                  vErrors.push(err90);
                }
                errors++;
              }
            }
            for (const key3 in data33) {
              if (key3 !== "name" && key3 !== "unique_id" && key3 !== "enabled" && key3 !== "stored_members" && key3 !== "resolved_pairs" && key3 !== "resolved_nets" && key3 !== "unresolved_members") {
                const err91 = { instancePath: instancePath + "/differential_pair_classes/" + i6 + "/" + key3.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/DifferentialPairClass/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err91];
                } else {
                  vErrors.push(err91);
                }
                errors++;
              }
            }
          } else {
            const err92 = { instancePath: instancePath + "/differential_pair_classes/" + i6, schemaPath: "#/$defs/DifferentialPairClass/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err92];
            } else {
              vErrors.push(err92);
            }
            errors++;
          }
        }
      } else {
        const err93 = { instancePath: instancePath + "/differential_pair_classes", schemaPath: "#/properties/differential_pair_classes/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err93];
        } else {
          vErrors.push(err93);
        }
        errors++;
      }
    }
    if (data.net_memberships !== void 0) {
      let data46 = data.net_memberships;
      if (Array.isArray(data46)) {
        const len11 = data46.length;
        for (let i11 = 0; i11 < len11; i11++) {
          if (!validate25(data46[i11], { instancePath: instancePath + "/net_memberships/" + i11, parentData: data46, parentDataProperty: i11, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate25.errors : vErrors.concat(validate25.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err94 = { instancePath: instancePath + "/net_memberships", schemaPath: "#/properties/net_memberships/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err94];
        } else {
          vErrors.push(err94);
        }
        errors++;
      }
    }
    if (data.rules !== void 0) {
      let data48 = data.rules;
      if (Array.isArray(data48)) {
        const len12 = data48.length;
        for (let i12 = 0; i12 < len12; i12++) {
          if (!validate27(data48[i12], { instancePath: instancePath + "/rules/" + i12, parentData: data48, parentDataProperty: i12, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate27.errors : vErrors.concat(validate27.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err95 = { instancePath: instancePath + "/rules", schemaPath: "#/properties/rules/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err95];
        } else {
          vErrors.push(err95);
        }
        errors++;
      }
    }
    if (data.diagnostics !== void 0) {
      let data50 = data.diagnostics;
      if (Array.isArray(data50)) {
        const len13 = data50.length;
        for (let i13 = 0; i13 < len13; i13++) {
          if (!validate31(data50[i13], { instancePath: instancePath + "/diagnostics/" + i13, parentData: data50, parentDataProperty: i13, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate31.errors : vErrors.concat(validate31.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err96 = { instancePath: instancePath + "/diagnostics", schemaPath: "#/properties/diagnostics/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err96];
        } else {
          vErrors.push(err96);
        }
        errors++;
      }
    }
    for (const key4 in data) {
      if (key4 !== "schema" && key4 !== "source" && key4 !== "board" && key4 !== "evidence" && key4 !== "summary" && key4 !== "net_classes" && key4 !== "differential_pairs" && key4 !== "differential_pair_classes" && key4 !== "net_memberships" && key4 !== "rules" && key4 !== "diagnostics") {
        const err97 = { instancePath: instancePath + "/" + key4.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err97];
        } else {
          vErrors.push(err97);
        }
        errors++;
      }
    }
  } else {
    const err98 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err98];
    } else {
      vErrors.push(err98);
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
