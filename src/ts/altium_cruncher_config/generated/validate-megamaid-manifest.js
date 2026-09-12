// Generated from src/tsp/altium_cruncher/outputs/megamaid-manifest.tsp. Do not edit.
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
    if (data.output_kinds !== void 0) {
      let data0 = data.output_kinds;
      if (Array.isArray(data0)) {
        const len0 = data0.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (typeof data0[i0] !== "string") {
            const err1 = { instancePath: instancePath + "/output_kinds/" + i0, schemaPath: "#/properties/output_kinds/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err1];
            } else {
              vErrors.push(err1);
            }
            errors++;
          }
        }
      } else {
        const err2 = { instancePath: instancePath + "/output_kinds", schemaPath: "#/properties/output_kinds/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data2 = data.outputs;
      if (Array.isArray(data2)) {
        const len1 = data2.length;
        for (let i1 = 0; i1 < len1; i1++) {
          let data3 = data2[i1];
          if (data3 && typeof data3 == "object" && !Array.isArray(data3)) {
            if (data3.variant === void 0) {
              const err3 = { instancePath: instancePath + "/outputs/" + i1, schemaPath: "#/$defs/BomOutput/required", keyword: "required", params: { missingProperty: "variant" }, message: "must have required property 'variant'" };
              if (vErrors === null) {
                vErrors = [err3];
              } else {
                vErrors.push(err3);
              }
              errors++;
            }
            if (data3.component_count === void 0) {
              const err4 = { instancePath: instancePath + "/outputs/" + i1, schemaPath: "#/$defs/BomOutput/required", keyword: "required", params: { missingProperty: "component_count" }, message: "must have required property 'component_count'" };
              if (vErrors === null) {
                vErrors = [err4];
              } else {
                vErrors.push(err4);
              }
              errors++;
            }
            if (data3.artifacts === void 0) {
              const err5 = { instancePath: instancePath + "/outputs/" + i1, schemaPath: "#/$defs/BomOutput/required", keyword: "required", params: { missingProperty: "artifacts" }, message: "must have required property 'artifacts'" };
              if (vErrors === null) {
                vErrors = [err5];
              } else {
                vErrors.push(err5);
              }
              errors++;
            }
            if (data3.variant !== void 0) {
              if (typeof data3.variant !== "string") {
                const err6 = { instancePath: instancePath + "/outputs/" + i1 + "/variant", schemaPath: "#/$defs/BomOutput/properties/variant/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err6];
                } else {
                  vErrors.push(err6);
                }
                errors++;
              }
            }
            if (data3.component_count !== void 0) {
              let data5 = data3.component_count;
              if (!(typeof data5 == "number" && (!(data5 % 1) && !isNaN(data5)))) {
                const err7 = { instancePath: instancePath + "/outputs/" + i1 + "/component_count", schemaPath: "#/$defs/BomOutput/properties/component_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
                if (vErrors === null) {
                  vErrors = [err7];
                } else {
                  vErrors.push(err7);
                }
                errors++;
              }
            }
            if (data3.artifacts !== void 0) {
              let data6 = data3.artifacts;
              if (Array.isArray(data6)) {
                const len2 = data6.length;
                for (let i2 = 0; i2 < len2; i2++) {
                  if (typeof data6[i2] !== "string") {
                    const err8 = { instancePath: instancePath + "/outputs/" + i1 + "/artifacts/" + i2, schemaPath: "#/$defs/BomOutput/properties/artifacts/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                    if (vErrors === null) {
                      vErrors = [err8];
                    } else {
                      vErrors.push(err8);
                    }
                    errors++;
                  }
                }
              } else {
                const err9 = { instancePath: instancePath + "/outputs/" + i1 + "/artifacts", schemaPath: "#/$defs/BomOutput/properties/artifacts/type", keyword: "type", params: { type: "array" }, message: "must be array" };
                if (vErrors === null) {
                  vErrors = [err9];
                } else {
                  vErrors.push(err9);
                }
                errors++;
              }
            }
            for (const key1 in data3) {
              if (key1 !== "variant" && key1 !== "component_count" && key1 !== "artifacts") {
                const err10 = { instancePath: instancePath + "/outputs/" + i1 + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/BomOutput/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err10];
                } else {
                  vErrors.push(err10);
                }
                errors++;
              }
            }
          } else {
            const err11 = { instancePath: instancePath + "/outputs/" + i1, schemaPath: "#/$defs/BomOutput/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err11];
            } else {
              vErrors.push(err11);
            }
            errors++;
          }
        }
      } else {
        const err12 = { instancePath: instancePath + "/outputs", schemaPath: "#/properties/outputs/type", keyword: "type", params: { type: "array" }, message: "must be array" };
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
  validate21.errors = vErrors;
  return errors === 0;
}
validate21.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.output_kinds !== void 0) {
      let data0 = data.output_kinds;
      if (Array.isArray(data0)) {
        const len0 = data0.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (typeof data0[i0] !== "string") {
            const err1 = { instancePath: instancePath + "/output_kinds/" + i0, schemaPath: "#/properties/output_kinds/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err1];
            } else {
              vErrors.push(err1);
            }
            errors++;
          }
        }
      } else {
        const err2 = { instancePath: instancePath + "/output_kinds", schemaPath: "#/properties/output_kinds/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data2 = data.outputs;
      if (Array.isArray(data2)) {
        const len1 = data2.length;
        for (let i1 = 0; i1 < len1; i1++) {
          let data3 = data2[i1];
          if (data3 && typeof data3 == "object" && !Array.isArray(data3)) {
            if (data3.variant === void 0) {
              const err3 = { instancePath: instancePath + "/outputs/" + i1, schemaPath: "#/$defs/PnpOutput/required", keyword: "required", params: { missingProperty: "variant" }, message: "must have required property 'variant'" };
              if (vErrors === null) {
                vErrors = [err3];
              } else {
                vErrors.push(err3);
              }
              errors++;
            }
            if (data3.placement_count === void 0) {
              const err4 = { instancePath: instancePath + "/outputs/" + i1, schemaPath: "#/$defs/PnpOutput/required", keyword: "required", params: { missingProperty: "placement_count" }, message: "must have required property 'placement_count'" };
              if (vErrors === null) {
                vErrors = [err4];
              } else {
                vErrors.push(err4);
              }
              errors++;
            }
            if (data3.artifacts === void 0) {
              const err5 = { instancePath: instancePath + "/outputs/" + i1, schemaPath: "#/$defs/PnpOutput/required", keyword: "required", params: { missingProperty: "artifacts" }, message: "must have required property 'artifacts'" };
              if (vErrors === null) {
                vErrors = [err5];
              } else {
                vErrors.push(err5);
              }
              errors++;
            }
            if (data3.variant !== void 0) {
              if (typeof data3.variant !== "string") {
                const err6 = { instancePath: instancePath + "/outputs/" + i1 + "/variant", schemaPath: "#/$defs/PnpOutput/properties/variant/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err6];
                } else {
                  vErrors.push(err6);
                }
                errors++;
              }
            }
            if (data3.placement_count !== void 0) {
              let data5 = data3.placement_count;
              if (!(typeof data5 == "number" && (!(data5 % 1) && !isNaN(data5)))) {
                const err7 = { instancePath: instancePath + "/outputs/" + i1 + "/placement_count", schemaPath: "#/$defs/PnpOutput/properties/placement_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
                if (vErrors === null) {
                  vErrors = [err7];
                } else {
                  vErrors.push(err7);
                }
                errors++;
              }
            }
            if (data3.artifacts !== void 0) {
              let data6 = data3.artifacts;
              if (Array.isArray(data6)) {
                const len2 = data6.length;
                for (let i2 = 0; i2 < len2; i2++) {
                  if (typeof data6[i2] !== "string") {
                    const err8 = { instancePath: instancePath + "/outputs/" + i1 + "/artifacts/" + i2, schemaPath: "#/$defs/PnpOutput/properties/artifacts/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                    if (vErrors === null) {
                      vErrors = [err8];
                    } else {
                      vErrors.push(err8);
                    }
                    errors++;
                  }
                }
              } else {
                const err9 = { instancePath: instancePath + "/outputs/" + i1 + "/artifacts", schemaPath: "#/$defs/PnpOutput/properties/artifacts/type", keyword: "type", params: { type: "array" }, message: "must be array" };
                if (vErrors === null) {
                  vErrors = [err9];
                } else {
                  vErrors.push(err9);
                }
                errors++;
              }
            }
            for (const key1 in data3) {
              if (key1 !== "variant" && key1 !== "placement_count" && key1 !== "artifacts") {
                const err10 = { instancePath: instancePath + "/outputs/" + i1 + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/PnpOutput/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err10];
                } else {
                  vErrors.push(err10);
                }
                errors++;
              }
            }
          } else {
            const err11 = { instancePath: instancePath + "/outputs/" + i1, schemaPath: "#/$defs/PnpOutput/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err11];
            } else {
              vErrors.push(err11);
            }
            errors++;
          }
        }
      } else {
        const err12 = { instancePath: instancePath + "/outputs", schemaPath: "#/properties/outputs/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
    }
    if (data.skipped !== void 0) {
      if (typeof data.skipped !== "string") {
        const err13 = { instancePath: instancePath + "/skipped", schemaPath: "#/properties/skipped/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
    if (data.source !== void 0) {
      if (typeof data.source !== "string") {
        const err1 = { instancePath: instancePath + "/source", schemaPath: "#/properties/source/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
    }
    if (data.kind !== void 0) {
      if (typeof data.kind !== "string") {
        const err2 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
    if (data.json !== void 0) {
      if (typeof data.json !== "string") {
        const err3 = { instancePath: instancePath + "/json", schemaPath: "#/properties/json/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
    if (data.schlib !== void 0) {
      let data0 = data.schlib;
      if (Array.isArray(data0)) {
        const len0 = data0.length;
        for (let i0 = 0; i0 < len0; i0++) {
          let data1 = data0[i0];
          if (data1 && typeof data1 == "object" && !Array.isArray(data1)) {
            if (data1.source === void 0) {
              const err1 = { instancePath: instancePath + "/schlib/" + i0, schemaPath: "#/$defs/LibraryJsonEntry/required", keyword: "required", params: { missingProperty: "source" }, message: "must have required property 'source'" };
              if (vErrors === null) {
                vErrors = [err1];
              } else {
                vErrors.push(err1);
              }
              errors++;
            }
            if (data1.kind === void 0) {
              const err2 = { instancePath: instancePath + "/schlib/" + i0, schemaPath: "#/$defs/LibraryJsonEntry/required", keyword: "required", params: { missingProperty: "kind" }, message: "must have required property 'kind'" };
              if (vErrors === null) {
                vErrors = [err2];
              } else {
                vErrors.push(err2);
              }
              errors++;
            }
            if (data1.json === void 0) {
              const err3 = { instancePath: instancePath + "/schlib/" + i0, schemaPath: "#/$defs/LibraryJsonEntry/required", keyword: "required", params: { missingProperty: "json" }, message: "must have required property 'json'" };
              if (vErrors === null) {
                vErrors = [err3];
              } else {
                vErrors.push(err3);
              }
              errors++;
            }
            if (data1.scope === void 0) {
              const err4 = { instancePath: instancePath + "/schlib/" + i0, schemaPath: "#/$defs/LibraryJsonEntry/required", keyword: "required", params: { missingProperty: "scope" }, message: "must have required property 'scope'" };
              if (vErrors === null) {
                vErrors = [err4];
              } else {
                vErrors.push(err4);
              }
              errors++;
            }
            if (data1.source !== void 0) {
              if (typeof data1.source !== "string") {
                const err5 = { instancePath: instancePath + "/schlib/" + i0 + "/source", schemaPath: "#/$defs/LibraryJsonEntry/properties/source/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err5];
                } else {
                  vErrors.push(err5);
                }
                errors++;
              }
            }
            if (data1.kind !== void 0) {
              if (typeof data1.kind !== "string") {
                const err6 = { instancePath: instancePath + "/schlib/" + i0 + "/kind", schemaPath: "#/$defs/LibraryJsonEntry/properties/kind/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err6];
                } else {
                  vErrors.push(err6);
                }
                errors++;
              }
            }
            if (data1.json !== void 0) {
              if (typeof data1.json !== "string") {
                const err7 = { instancePath: instancePath + "/schlib/" + i0 + "/json", schemaPath: "#/$defs/LibraryJsonEntry/properties/json/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err7];
                } else {
                  vErrors.push(err7);
                }
                errors++;
              }
            }
            if (data1.scope !== void 0) {
              let data5 = data1.scope;
              const _errs17 = errors;
              let valid7 = false;
              const _errs18 = errors;
              if (typeof data5 !== "string") {
                const err8 = { instancePath: instancePath + "/schlib/" + i0 + "/scope", schemaPath: "#/$defs/LibraryJsonEntry/properties/scope/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err8];
                } else {
                  vErrors.push(err8);
                }
                errors++;
              }
              if ("combined" !== data5) {
                const err9 = { instancePath: instancePath + "/schlib/" + i0 + "/scope", schemaPath: "#/$defs/LibraryJsonEntry/properties/scope/anyOf/0/const", keyword: "const", params: { allowedValue: "combined" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err9];
                } else {
                  vErrors.push(err9);
                }
                errors++;
              }
              var _valid0 = _errs18 === errors;
              valid7 = valid7 || _valid0;
              const _errs20 = errors;
              if (typeof data5 !== "string") {
                const err10 = { instancePath: instancePath + "/schlib/" + i0 + "/scope", schemaPath: "#/$defs/LibraryJsonEntry/properties/scope/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err10];
                } else {
                  vErrors.push(err10);
                }
                errors++;
              }
              if ("split" !== data5) {
                const err11 = { instancePath: instancePath + "/schlib/" + i0 + "/scope", schemaPath: "#/$defs/LibraryJsonEntry/properties/scope/anyOf/1/const", keyword: "const", params: { allowedValue: "split" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err11];
                } else {
                  vErrors.push(err11);
                }
                errors++;
              }
              var _valid0 = _errs20 === errors;
              valid7 = valid7 || _valid0;
              if (!valid7) {
                const err12 = { instancePath: instancePath + "/schlib/" + i0 + "/scope", schemaPath: "#/$defs/LibraryJsonEntry/properties/scope/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err12];
                } else {
                  vErrors.push(err12);
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
            for (const key1 in data1) {
              if (key1 !== "source" && key1 !== "kind" && key1 !== "json" && key1 !== "scope") {
                const err13 = { instancePath: instancePath + "/schlib/" + i0 + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/LibraryJsonEntry/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err13];
                } else {
                  vErrors.push(err13);
                }
                errors++;
              }
            }
          } else {
            const err14 = { instancePath: instancePath + "/schlib/" + i0, schemaPath: "#/$defs/LibraryJsonEntry/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err14];
            } else {
              vErrors.push(err14);
            }
            errors++;
          }
        }
      } else {
        const err15 = { instancePath: instancePath + "/schlib", schemaPath: "#/properties/schlib/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
    }
    if (data.pcblib !== void 0) {
      let data7 = data.pcblib;
      if (Array.isArray(data7)) {
        const len1 = data7.length;
        for (let i1 = 0; i1 < len1; i1++) {
          let data8 = data7[i1];
          if (data8 && typeof data8 == "object" && !Array.isArray(data8)) {
            if (data8.source === void 0) {
              const err16 = { instancePath: instancePath + "/pcblib/" + i1, schemaPath: "#/$defs/LibraryJsonEntry/required", keyword: "required", params: { missingProperty: "source" }, message: "must have required property 'source'" };
              if (vErrors === null) {
                vErrors = [err16];
              } else {
                vErrors.push(err16);
              }
              errors++;
            }
            if (data8.kind === void 0) {
              const err17 = { instancePath: instancePath + "/pcblib/" + i1, schemaPath: "#/$defs/LibraryJsonEntry/required", keyword: "required", params: { missingProperty: "kind" }, message: "must have required property 'kind'" };
              if (vErrors === null) {
                vErrors = [err17];
              } else {
                vErrors.push(err17);
              }
              errors++;
            }
            if (data8.json === void 0) {
              const err18 = { instancePath: instancePath + "/pcblib/" + i1, schemaPath: "#/$defs/LibraryJsonEntry/required", keyword: "required", params: { missingProperty: "json" }, message: "must have required property 'json'" };
              if (vErrors === null) {
                vErrors = [err18];
              } else {
                vErrors.push(err18);
              }
              errors++;
            }
            if (data8.scope === void 0) {
              const err19 = { instancePath: instancePath + "/pcblib/" + i1, schemaPath: "#/$defs/LibraryJsonEntry/required", keyword: "required", params: { missingProperty: "scope" }, message: "must have required property 'scope'" };
              if (vErrors === null) {
                vErrors = [err19];
              } else {
                vErrors.push(err19);
              }
              errors++;
            }
            if (data8.source !== void 0) {
              if (typeof data8.source !== "string") {
                const err20 = { instancePath: instancePath + "/pcblib/" + i1 + "/source", schemaPath: "#/$defs/LibraryJsonEntry/properties/source/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err20];
                } else {
                  vErrors.push(err20);
                }
                errors++;
              }
            }
            if (data8.kind !== void 0) {
              if (typeof data8.kind !== "string") {
                const err21 = { instancePath: instancePath + "/pcblib/" + i1 + "/kind", schemaPath: "#/$defs/LibraryJsonEntry/properties/kind/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err21];
                } else {
                  vErrors.push(err21);
                }
                errors++;
              }
            }
            if (data8.json !== void 0) {
              if (typeof data8.json !== "string") {
                const err22 = { instancePath: instancePath + "/pcblib/" + i1 + "/json", schemaPath: "#/$defs/LibraryJsonEntry/properties/json/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err22];
                } else {
                  vErrors.push(err22);
                }
                errors++;
              }
            }
            if (data8.scope !== void 0) {
              let data12 = data8.scope;
              const _errs37 = errors;
              let valid13 = false;
              const _errs38 = errors;
              if (typeof data12 !== "string") {
                const err23 = { instancePath: instancePath + "/pcblib/" + i1 + "/scope", schemaPath: "#/$defs/LibraryJsonEntry/properties/scope/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err23];
                } else {
                  vErrors.push(err23);
                }
                errors++;
              }
              if ("combined" !== data12) {
                const err24 = { instancePath: instancePath + "/pcblib/" + i1 + "/scope", schemaPath: "#/$defs/LibraryJsonEntry/properties/scope/anyOf/0/const", keyword: "const", params: { allowedValue: "combined" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err24];
                } else {
                  vErrors.push(err24);
                }
                errors++;
              }
              var _valid1 = _errs38 === errors;
              valid13 = valid13 || _valid1;
              const _errs40 = errors;
              if (typeof data12 !== "string") {
                const err25 = { instancePath: instancePath + "/pcblib/" + i1 + "/scope", schemaPath: "#/$defs/LibraryJsonEntry/properties/scope/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err25];
                } else {
                  vErrors.push(err25);
                }
                errors++;
              }
              if ("split" !== data12) {
                const err26 = { instancePath: instancePath + "/pcblib/" + i1 + "/scope", schemaPath: "#/$defs/LibraryJsonEntry/properties/scope/anyOf/1/const", keyword: "const", params: { allowedValue: "split" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err26];
                } else {
                  vErrors.push(err26);
                }
                errors++;
              }
              var _valid1 = _errs40 === errors;
              valid13 = valid13 || _valid1;
              if (!valid13) {
                const err27 = { instancePath: instancePath + "/pcblib/" + i1 + "/scope", schemaPath: "#/$defs/LibraryJsonEntry/properties/scope/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err27];
                } else {
                  vErrors.push(err27);
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
            for (const key2 in data8) {
              if (key2 !== "source" && key2 !== "kind" && key2 !== "json" && key2 !== "scope") {
                const err28 = { instancePath: instancePath + "/pcblib/" + i1 + "/" + key2.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/LibraryJsonEntry/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err28];
                } else {
                  vErrors.push(err28);
                }
                errors++;
              }
            }
          } else {
            const err29 = { instancePath: instancePath + "/pcblib/" + i1, schemaPath: "#/$defs/LibraryJsonEntry/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err29];
            } else {
              vErrors.push(err29);
            }
            errors++;
          }
        }
      } else {
        const err30 = { instancePath: instancePath + "/pcblib", schemaPath: "#/properties/pcblib/type", keyword: "type", params: { type: "array" }, message: "must be array" };
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
    if (data.notes_json !== void 0) {
      if (typeof data.notes_json !== "string") {
        const err1 = { instancePath: instancePath + "/notes_json", schemaPath: "#/properties/notes_json/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
    if (data.source_schdoc === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "source_schdoc" }, message: "must have required property 'source_schdoc'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.split_results === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "split_results" }, message: "must have required property 'split_results'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.source_schdoc !== void 0) {
      if (typeof data.source_schdoc !== "string") {
        const err2 = { instancePath: instancePath + "/source_schdoc", schemaPath: "#/properties/source_schdoc/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
    if (data.split_results !== void 0) {
      let data1 = data.split_results;
      if (data1 && typeof data1 == "object" && !Array.isArray(data1)) {
        for (const key0 in data1) {
          if (typeof data1[key0] !== "boolean") {
            const err3 = { instancePath: instancePath + "/split_results/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/RecordBoolean/unevaluatedProperties/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err3];
            } else {
              vErrors.push(err3);
            }
            errors++;
          }
        }
      } else {
        const err4 = { instancePath: instancePath + "/split_results", schemaPath: "#/$defs/RecordBoolean/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "source_schdoc" && key1 !== "split_results") {
        const err5 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
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
    if (data.source_schdocs !== void 0) {
      let data0 = data.source_schdocs;
      if (Array.isArray(data0)) {
        const len0 = data0.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (typeof data0[i0] !== "string") {
            const err1 = { instancePath: instancePath + "/source_schdocs/" + i0, schemaPath: "#/properties/source_schdocs/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err1];
            } else {
              vErrors.push(err1);
            }
            errors++;
          }
        }
      } else {
        const err2 = { instancePath: instancePath + "/source_schdocs", schemaPath: "#/properties/source_schdocs/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
    if (data.combined_schlib !== void 0) {
      if (typeof data.combined_schlib !== "string") {
        const err3 = { instancePath: instancePath + "/combined_schlib", schemaPath: "#/properties/combined_schlib/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.split_dir !== void 0) {
      if (typeof data.split_dir !== "string") {
        const err4 = { instancePath: instancePath + "/split_dir", schemaPath: "#/properties/split_dir/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.symbol_count !== void 0) {
      let data4 = data.symbol_count;
      if (!(typeof data4 == "number" && (!(data4 % 1) && !isNaN(data4)))) {
        const err5 = { instancePath: instancePath + "/symbol_count", schemaPath: "#/properties/symbol_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.split_file_count !== void 0) {
      let data5 = data.split_file_count;
      if (!(typeof data5 == "number" && (!(data5 % 1) && !isNaN(data5)))) {
        const err6 = { instancePath: instancePath + "/split_file_count", schemaPath: "#/properties/split_file_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.split_files !== void 0) {
      let data6 = data.split_files;
      if (Array.isArray(data6)) {
        const len1 = data6.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (typeof data6[i1] !== "string") {
            const err7 = { instancePath: instancePath + "/split_files/" + i1, schemaPath: "#/properties/split_files/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err7];
            } else {
              vErrors.push(err7);
            }
            errors++;
          }
        }
      } else {
        const err8 = { instancePath: instancePath + "/split_files", schemaPath: "#/properties/split_files/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
    if (data.split_results_by_schdoc !== void 0) {
      let data8 = data.split_results_by_schdoc;
      if (Array.isArray(data8)) {
        const len2 = data8.length;
        for (let i2 = 0; i2 < len2; i2++) {
          if (!validate32(data8[i2], { instancePath: instancePath + "/split_results_by_schdoc/" + i2, parentData: data8, parentDataProperty: i2, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate32.errors : vErrors.concat(validate32.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err9 = { instancePath: instancePath + "/split_results_by_schdoc", schemaPath: "#/properties/split_results_by_schdoc/type", keyword: "type", params: { type: "array" }, message: "must be array" };
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
    if (data.source_pcbdoc !== void 0) {
      if (typeof data.source_pcbdoc !== "string") {
        const err1 = { instancePath: instancePath + "/source_pcbdoc", schemaPath: "#/properties/source_pcbdoc/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
    }
    if (data.combined_pcblib !== void 0) {
      if (typeof data.combined_pcblib !== "string") {
        const err2 = { instancePath: instancePath + "/combined_pcblib", schemaPath: "#/properties/combined_pcblib/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
    if (data.split_dir !== void 0) {
      if (typeof data.split_dir !== "string") {
        const err3 = { instancePath: instancePath + "/split_dir", schemaPath: "#/properties/split_dir/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.footprint_count !== void 0) {
      let data3 = data.footprint_count;
      if (!(typeof data3 == "number" && (!(data3 % 1) && !isNaN(data3)))) {
        const err4 = { instancePath: instancePath + "/footprint_count", schemaPath: "#/properties/footprint_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.split_file_count !== void 0) {
      let data4 = data.split_file_count;
      if (!(typeof data4 == "number" && (!(data4 % 1) && !isNaN(data4)))) {
        const err5 = { instancePath: instancePath + "/split_file_count", schemaPath: "#/properties/split_file_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.split_files !== void 0) {
      let data5 = data.split_files;
      if (Array.isArray(data5)) {
        const len0 = data5.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (typeof data5[i0] !== "string") {
            const err6 = { instancePath: instancePath + "/split_files/" + i0, schemaPath: "#/properties/split_files/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err6];
            } else {
              vErrors.push(err6);
            }
            errors++;
          }
        }
      } else {
        const err7 = { instancePath: instancePath + "/split_files", schemaPath: "#/properties/split_files/type", keyword: "type", params: { type: "array" }, message: "must be array" };
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
  validate35.errors = vErrors;
  return errors === 0;
}
validate35.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.fonts !== void 0) {
      let data0 = data.fonts;
      if (Array.isArray(data0)) {
        const len0 = data0.length;
        for (let i0 = 0; i0 < len0; i0++) {
          let data1 = data0[i0];
          if (data1 && typeof data1 == "object" && !Array.isArray(data1)) {
            if (data1.source_pcbdoc === void 0) {
              const err1 = { instancePath: instancePath + "/fonts/" + i0, schemaPath: "#/$defs/EmbeddedAsset/required", keyword: "required", params: { missingProperty: "source_pcbdoc" }, message: "must have required property 'source_pcbdoc'" };
              if (vErrors === null) {
                vErrors = [err1];
              } else {
                vErrors.push(err1);
              }
              errors++;
            }
            if (data1.source_name === void 0) {
              const err2 = { instancePath: instancePath + "/fonts/" + i0, schemaPath: "#/$defs/EmbeddedAsset/required", keyword: "required", params: { missingProperty: "source_name" }, message: "must have required property 'source_name'" };
              if (vErrors === null) {
                vErrors = [err2];
              } else {
                vErrors.push(err2);
              }
              errors++;
            }
            if (data1.output_file === void 0) {
              const err3 = { instancePath: instancePath + "/fonts/" + i0, schemaPath: "#/$defs/EmbeddedAsset/required", keyword: "required", params: { missingProperty: "output_file" }, message: "must have required property 'output_file'" };
              if (vErrors === null) {
                vErrors = [err3];
              } else {
                vErrors.push(err3);
              }
              errors++;
            }
            if (data1.deduplicated === void 0) {
              const err4 = { instancePath: instancePath + "/fonts/" + i0, schemaPath: "#/$defs/EmbeddedAsset/required", keyword: "required", params: { missingProperty: "deduplicated" }, message: "must have required property 'deduplicated'" };
              if (vErrors === null) {
                vErrors = [err4];
              } else {
                vErrors.push(err4);
              }
              errors++;
            }
            if (data1.source_pcbdoc !== void 0) {
              if (typeof data1.source_pcbdoc !== "string") {
                const err5 = { instancePath: instancePath + "/fonts/" + i0 + "/source_pcbdoc", schemaPath: "#/$defs/EmbeddedAsset/properties/source_pcbdoc/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err5];
                } else {
                  vErrors.push(err5);
                }
                errors++;
              }
            }
            if (data1.source_name !== void 0) {
              if (typeof data1.source_name !== "string") {
                const err6 = { instancePath: instancePath + "/fonts/" + i0 + "/source_name", schemaPath: "#/$defs/EmbeddedAsset/properties/source_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err6];
                } else {
                  vErrors.push(err6);
                }
                errors++;
              }
            }
            if (data1.output_file !== void 0) {
              if (typeof data1.output_file !== "string") {
                const err7 = { instancePath: instancePath + "/fonts/" + i0 + "/output_file", schemaPath: "#/$defs/EmbeddedAsset/properties/output_file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err7];
                } else {
                  vErrors.push(err7);
                }
                errors++;
              }
            }
            if (data1.deduplicated !== void 0) {
              if (typeof data1.deduplicated !== "boolean") {
                const err8 = { instancePath: instancePath + "/fonts/" + i0 + "/deduplicated", schemaPath: "#/$defs/EmbeddedAsset/properties/deduplicated/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
                if (vErrors === null) {
                  vErrors = [err8];
                } else {
                  vErrors.push(err8);
                }
                errors++;
              }
            }
            for (const key1 in data1) {
              if (key1 !== "source_pcbdoc" && key1 !== "source_name" && key1 !== "output_file" && key1 !== "deduplicated") {
                const err9 = { instancePath: instancePath + "/fonts/" + i0 + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/EmbeddedAsset/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err9];
                } else {
                  vErrors.push(err9);
                }
                errors++;
              }
            }
          } else {
            const err10 = { instancePath: instancePath + "/fonts/" + i0, schemaPath: "#/$defs/EmbeddedAsset/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err10];
            } else {
              vErrors.push(err10);
            }
            errors++;
          }
        }
      } else {
        const err11 = { instancePath: instancePath + "/fonts", schemaPath: "#/properties/fonts/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
    }
    if (data.models !== void 0) {
      let data7 = data.models;
      if (Array.isArray(data7)) {
        const len1 = data7.length;
        for (let i1 = 0; i1 < len1; i1++) {
          let data8 = data7[i1];
          if (data8 && typeof data8 == "object" && !Array.isArray(data8)) {
            if (data8.source_pcbdoc === void 0) {
              const err12 = { instancePath: instancePath + "/models/" + i1, schemaPath: "#/$defs/EmbeddedAsset/required", keyword: "required", params: { missingProperty: "source_pcbdoc" }, message: "must have required property 'source_pcbdoc'" };
              if (vErrors === null) {
                vErrors = [err12];
              } else {
                vErrors.push(err12);
              }
              errors++;
            }
            if (data8.source_name === void 0) {
              const err13 = { instancePath: instancePath + "/models/" + i1, schemaPath: "#/$defs/EmbeddedAsset/required", keyword: "required", params: { missingProperty: "source_name" }, message: "must have required property 'source_name'" };
              if (vErrors === null) {
                vErrors = [err13];
              } else {
                vErrors.push(err13);
              }
              errors++;
            }
            if (data8.output_file === void 0) {
              const err14 = { instancePath: instancePath + "/models/" + i1, schemaPath: "#/$defs/EmbeddedAsset/required", keyword: "required", params: { missingProperty: "output_file" }, message: "must have required property 'output_file'" };
              if (vErrors === null) {
                vErrors = [err14];
              } else {
                vErrors.push(err14);
              }
              errors++;
            }
            if (data8.deduplicated === void 0) {
              const err15 = { instancePath: instancePath + "/models/" + i1, schemaPath: "#/$defs/EmbeddedAsset/required", keyword: "required", params: { missingProperty: "deduplicated" }, message: "must have required property 'deduplicated'" };
              if (vErrors === null) {
                vErrors = [err15];
              } else {
                vErrors.push(err15);
              }
              errors++;
            }
            if (data8.source_pcbdoc !== void 0) {
              if (typeof data8.source_pcbdoc !== "string") {
                const err16 = { instancePath: instancePath + "/models/" + i1 + "/source_pcbdoc", schemaPath: "#/$defs/EmbeddedAsset/properties/source_pcbdoc/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err16];
                } else {
                  vErrors.push(err16);
                }
                errors++;
              }
            }
            if (data8.source_name !== void 0) {
              if (typeof data8.source_name !== "string") {
                const err17 = { instancePath: instancePath + "/models/" + i1 + "/source_name", schemaPath: "#/$defs/EmbeddedAsset/properties/source_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err17];
                } else {
                  vErrors.push(err17);
                }
                errors++;
              }
            }
            if (data8.output_file !== void 0) {
              if (typeof data8.output_file !== "string") {
                const err18 = { instancePath: instancePath + "/models/" + i1 + "/output_file", schemaPath: "#/$defs/EmbeddedAsset/properties/output_file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err18];
                } else {
                  vErrors.push(err18);
                }
                errors++;
              }
            }
            if (data8.deduplicated !== void 0) {
              if (typeof data8.deduplicated !== "boolean") {
                const err19 = { instancePath: instancePath + "/models/" + i1 + "/deduplicated", schemaPath: "#/$defs/EmbeddedAsset/properties/deduplicated/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
                if (vErrors === null) {
                  vErrors = [err19];
                } else {
                  vErrors.push(err19);
                }
                errors++;
              }
            }
            for (const key2 in data8) {
              if (key2 !== "source_pcbdoc" && key2 !== "source_name" && key2 !== "output_file" && key2 !== "deduplicated") {
                const err20 = { instancePath: instancePath + "/models/" + i1 + "/" + key2.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/EmbeddedAsset/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err20];
                } else {
                  vErrors.push(err20);
                }
                errors++;
              }
            }
          } else {
            const err21 = { instancePath: instancePath + "/models/" + i1, schemaPath: "#/$defs/EmbeddedAsset/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err21];
            } else {
              vErrors.push(err21);
            }
            errors++;
          }
        }
      } else {
        const err22 = { instancePath: instancePath + "/models", schemaPath: "#/properties/models/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
    }
    if (data.font_file_count !== void 0) {
      let data14 = data.font_file_count;
      if (!(typeof data14 == "number" && (!(data14 % 1) && !isNaN(data14)))) {
        const err23 = { instancePath: instancePath + "/font_file_count", schemaPath: "#/properties/font_file_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
    }
    if (data.model_file_count !== void 0) {
      let data15 = data.model_file_count;
      if (!(typeof data15 == "number" && (!(data15 % 1) && !isNaN(data15)))) {
        const err24 = { instancePath: instancePath + "/model_file_count", schemaPath: "#/properties/model_file_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
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
  validate37.errors = vErrors;
  return errors === 0;
}
validate37.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.images !== void 0) {
      let data0 = data.images;
      if (Array.isArray(data0)) {
        const len0 = data0.length;
        for (let i0 = 0; i0 < len0; i0++) {
          let data1 = data0[i0];
          if (data1 && typeof data1 == "object" && !Array.isArray(data1)) {
            if (data1.source_schdoc === void 0) {
              const err1 = { instancePath: instancePath + "/images/" + i0, schemaPath: "#/$defs/SchematicImage/required", keyword: "required", params: { missingProperty: "source_schdoc" }, message: "must have required property 'source_schdoc'" };
              if (vErrors === null) {
                vErrors = [err1];
              } else {
                vErrors.push(err1);
              }
              errors++;
            }
            if (data1.source_name === void 0) {
              const err2 = { instancePath: instancePath + "/images/" + i0, schemaPath: "#/$defs/SchematicImage/required", keyword: "required", params: { missingProperty: "source_name" }, message: "must have required property 'source_name'" };
              if (vErrors === null) {
                vErrors = [err2];
              } else {
                vErrors.push(err2);
              }
              errors++;
            }
            if (data1.output_file === void 0) {
              const err3 = { instancePath: instancePath + "/images/" + i0, schemaPath: "#/$defs/SchematicImage/required", keyword: "required", params: { missingProperty: "output_file" }, message: "must have required property 'output_file'" };
              if (vErrors === null) {
                vErrors = [err3];
              } else {
                vErrors.push(err3);
              }
              errors++;
            }
            if (data1.deduplicated === void 0) {
              const err4 = { instancePath: instancePath + "/images/" + i0, schemaPath: "#/$defs/SchematicImage/required", keyword: "required", params: { missingProperty: "deduplicated" }, message: "must have required property 'deduplicated'" };
              if (vErrors === null) {
                vErrors = [err4];
              } else {
                vErrors.push(err4);
              }
              errors++;
            }
            if (data1.source_schdoc !== void 0) {
              if (typeof data1.source_schdoc !== "string") {
                const err5 = { instancePath: instancePath + "/images/" + i0 + "/source_schdoc", schemaPath: "#/$defs/SchematicImage/properties/source_schdoc/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err5];
                } else {
                  vErrors.push(err5);
                }
                errors++;
              }
            }
            if (data1.source_name !== void 0) {
              if (typeof data1.source_name !== "string") {
                const err6 = { instancePath: instancePath + "/images/" + i0 + "/source_name", schemaPath: "#/$defs/SchematicImage/properties/source_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err6];
                } else {
                  vErrors.push(err6);
                }
                errors++;
              }
            }
            if (data1.output_file !== void 0) {
              if (typeof data1.output_file !== "string") {
                const err7 = { instancePath: instancePath + "/images/" + i0 + "/output_file", schemaPath: "#/$defs/SchematicImage/properties/output_file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err7];
                } else {
                  vErrors.push(err7);
                }
                errors++;
              }
            }
            if (data1.deduplicated !== void 0) {
              if (typeof data1.deduplicated !== "boolean") {
                const err8 = { instancePath: instancePath + "/images/" + i0 + "/deduplicated", schemaPath: "#/$defs/SchematicImage/properties/deduplicated/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
                if (vErrors === null) {
                  vErrors = [err8];
                } else {
                  vErrors.push(err8);
                }
                errors++;
              }
            }
            for (const key1 in data1) {
              if (key1 !== "source_schdoc" && key1 !== "source_name" && key1 !== "output_file" && key1 !== "deduplicated") {
                const err9 = { instancePath: instancePath + "/images/" + i0 + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/SchematicImage/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err9];
                } else {
                  vErrors.push(err9);
                }
                errors++;
              }
            }
          } else {
            const err10 = { instancePath: instancePath + "/images/" + i0, schemaPath: "#/$defs/SchematicImage/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err10];
            } else {
              vErrors.push(err10);
            }
            errors++;
          }
        }
      } else {
        const err11 = { instancePath: instancePath + "/images", schemaPath: "#/properties/images/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
    }
    if (data.image_file_count !== void 0) {
      let data7 = data.image_file_count;
      if (!(typeof data7 == "number" && (!(data7 % 1) && !isNaN(data7)))) {
        const err12 = { instancePath: instancePath + "/image_file_count", schemaPath: "#/properties/image_file_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
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
  validate39.errors = vErrors;
  return errors === 0;
}
validate39.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.kind === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "kind" }, message: "must have required property 'kind'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.input_project === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "input_project" }, message: "must have required property 'input_project'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.output_root === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "output_root" }, message: "must have required property 'output_root'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.variants === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "variants" }, message: "must have required property 'variants'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.bom_pnp_config === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "bom_pnp_config" }, message: "must have required property 'bom_pnp_config'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.schdoc_count === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "schdoc_count" }, message: "must have required property 'schdoc_count'" };
      if (vErrors === null) {
        vErrors = [err6];
      } else {
        vErrors.push(err6);
      }
      errors++;
    }
    if (data.pcbdoc_count === void 0) {
      const err7 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "pcbdoc_count" }, message: "must have required property 'pcbdoc_count'" };
      if (vErrors === null) {
        vErrors = [err7];
      } else {
        vErrors.push(err7);
      }
      errors++;
    }
    if (data.bom === void 0) {
      const err8 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "bom" }, message: "must have required property 'bom'" };
      if (vErrors === null) {
        vErrors = [err8];
      } else {
        vErrors.push(err8);
      }
      errors++;
    }
    if (data.pnp === void 0) {
      const err9 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "pnp" }, message: "must have required property 'pnp'" };
      if (vErrors === null) {
        vErrors = [err9];
      } else {
        vErrors.push(err9);
      }
      errors++;
    }
    if (data.netlist === void 0) {
      const err10 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "netlist" }, message: "must have required property 'netlist'" };
      if (vErrors === null) {
        vErrors = [err10];
      } else {
        vErrors.push(err10);
      }
      errors++;
    }
    if (data.document_jsons === void 0) {
      const err11 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "document_jsons" }, message: "must have required property 'document_jsons'" };
      if (vErrors === null) {
        vErrors = [err11];
      } else {
        vErrors.push(err11);
      }
      errors++;
    }
    if (data.library_jsons === void 0) {
      const err12 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "library_jsons" }, message: "must have required property 'library_jsons'" };
      if (vErrors === null) {
        vErrors = [err12];
      } else {
        vErrors.push(err12);
      }
      errors++;
    }
    if (data.notes === void 0) {
      const err13 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "notes" }, message: "must have required property 'notes'" };
      if (vErrors === null) {
        vErrors = [err13];
      } else {
        vErrors.push(err13);
      }
      errors++;
    }
    if (data.schlib === void 0) {
      const err14 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "schlib" }, message: "must have required property 'schlib'" };
      if (vErrors === null) {
        vErrors = [err14];
      } else {
        vErrors.push(err14);
      }
      errors++;
    }
    if (data.pcblib === void 0) {
      const err15 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "pcblib" }, message: "must have required property 'pcblib'" };
      if (vErrors === null) {
        vErrors = [err15];
      } else {
        vErrors.push(err15);
      }
      errors++;
    }
    if (data.embedded_assets === void 0) {
      const err16 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "embedded_assets" }, message: "must have required property 'embedded_assets'" };
      if (vErrors === null) {
        vErrors = [err16];
      } else {
        vErrors.push(err16);
      }
      errors++;
    }
    if (data.sch_images === void 0) {
      const err17 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "sch_images" }, message: "must have required property 'sch_images'" };
      if (vErrors === null) {
        vErrors = [err17];
      } else {
        vErrors.push(err17);
      }
      errors++;
    }
    if (data.schema !== void 0) {
      let data0 = data.schema;
      if (typeof data0 !== "string") {
        const err18 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
      if ("altium_cruncher.megamaid_manifest.b0" !== data0) {
        const err19 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.megamaid_manifest.b0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
    }
    if (data.kind !== void 0) {
      let data1 = data.kind;
      if (typeof data1 !== "string") {
        const err20 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      if ("megamaid" !== data1) {
        const err21 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/const", keyword: "const", params: { allowedValue: "megamaid" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
    }
    if (data.input_project !== void 0) {
      let data2 = data.input_project;
      if (typeof data2 === "string") {
        if (func1(data2) < 1) {
          const err22 = { instancePath: instancePath + "/input_project", schemaPath: "#/properties/input_project/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err22];
          } else {
            vErrors.push(err22);
          }
          errors++;
        }
      } else {
        const err23 = { instancePath: instancePath + "/input_project", schemaPath: "#/properties/input_project/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
    }
    if (data.output_root !== void 0) {
      let data3 = data.output_root;
      if (typeof data3 === "string") {
        if (func1(data3) < 1) {
          const err24 = { instancePath: instancePath + "/output_root", schemaPath: "#/properties/output_root/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err24];
          } else {
            vErrors.push(err24);
          }
          errors++;
        }
      } else {
        const err25 = { instancePath: instancePath + "/output_root", schemaPath: "#/properties/output_root/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
    }
    if (data.variants !== void 0) {
      let data4 = data.variants;
      if (Array.isArray(data4)) {
        const len0 = data4.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (typeof data4[i0] !== "string") {
            const err26 = { instancePath: instancePath + "/variants/" + i0, schemaPath: "#/properties/variants/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err26];
            } else {
              vErrors.push(err26);
            }
            errors++;
          }
        }
      } else {
        const err27 = { instancePath: instancePath + "/variants", schemaPath: "#/properties/variants/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
    }
    if (data.bom_pnp_config !== void 0) {
      let data6 = data.bom_pnp_config;
      const _errs15 = errors;
      let valid3 = false;
      const _errs16 = errors;
      if (typeof data6 !== "string") {
        const err28 = { instancePath: instancePath + "/bom_pnp_config", schemaPath: "#/properties/bom_pnp_config/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
      var _valid0 = _errs16 === errors;
      valid3 = valid3 || _valid0;
      const _errs18 = errors;
      if (data6 !== null) {
        const err29 = { instancePath: instancePath + "/bom_pnp_config", schemaPath: "#/properties/bom_pnp_config/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      }
      var _valid0 = _errs18 === errors;
      valid3 = valid3 || _valid0;
      if (!valid3) {
        const err30 = { instancePath: instancePath + "/bom_pnp_config", schemaPath: "#/properties/bom_pnp_config/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
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
    if (data.schdoc_count !== void 0) {
      let data7 = data.schdoc_count;
      if (!(typeof data7 == "number" && (!(data7 % 1) && !isNaN(data7)))) {
        const err31 = { instancePath: instancePath + "/schdoc_count", schemaPath: "#/properties/schdoc_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      }
      if (typeof data7 == "number") {
        if (data7 < 0 || isNaN(data7)) {
          const err32 = { instancePath: instancePath + "/schdoc_count", schemaPath: "#/properties/schdoc_count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err32];
          } else {
            vErrors.push(err32);
          }
          errors++;
        }
      }
    }
    if (data.pcbdoc_count !== void 0) {
      let data8 = data.pcbdoc_count;
      if (!(typeof data8 == "number" && (!(data8 % 1) && !isNaN(data8)))) {
        const err33 = { instancePath: instancePath + "/pcbdoc_count", schemaPath: "#/properties/pcbdoc_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
      if (typeof data8 == "number") {
        if (data8 < 0 || isNaN(data8)) {
          const err34 = { instancePath: instancePath + "/pcbdoc_count", schemaPath: "#/properties/pcbdoc_count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err34];
          } else {
            vErrors.push(err34);
          }
          errors++;
        }
      }
    }
    if (data.bom !== void 0) {
      if (!validate21(data.bom, { instancePath: instancePath + "/bom", parentData: data, parentDataProperty: "bom", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
        errors = vErrors.length;
      }
    }
    if (data.pnp !== void 0) {
      if (!validate23(data.pnp, { instancePath: instancePath + "/pnp", parentData: data, parentDataProperty: "pnp", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate23.errors : vErrors.concat(validate23.errors);
        errors = vErrors.length;
      }
    }
    if (data.netlist !== void 0) {
      let data11 = data.netlist;
      if (data11 && typeof data11 == "object" && !Array.isArray(data11)) {
        if (data11.design_json === void 0) {
          const err35 = { instancePath: instancePath + "/netlist", schemaPath: "#/$defs/Netlist/required", keyword: "required", params: { missingProperty: "design_json" }, message: "must have required property 'design_json'" };
          if (vErrors === null) {
            vErrors = [err35];
          } else {
            vErrors.push(err35);
          }
          errors++;
        }
        if (data11.design_schema === void 0) {
          const err36 = { instancePath: instancePath + "/netlist", schemaPath: "#/$defs/Netlist/required", keyword: "required", params: { missingProperty: "design_schema" }, message: "must have required property 'design_schema'" };
          if (vErrors === null) {
            vErrors = [err36];
          } else {
            vErrors.push(err36);
          }
          errors++;
        }
        if (data11.compiled_schematic_graph_schema === void 0) {
          const err37 = { instancePath: instancePath + "/netlist", schemaPath: "#/$defs/Netlist/required", keyword: "required", params: { missingProperty: "compiled_schematic_graph_schema" }, message: "must have required property 'compiled_schematic_graph_schema'" };
          if (vErrors === null) {
            vErrors = [err37];
          } else {
            vErrors.push(err37);
          }
          errors++;
        }
        if (data11.component_count === void 0) {
          const err38 = { instancePath: instancePath + "/netlist", schemaPath: "#/$defs/Netlist/required", keyword: "required", params: { missingProperty: "component_count" }, message: "must have required property 'component_count'" };
          if (vErrors === null) {
            vErrors = [err38];
          } else {
            vErrors.push(err38);
          }
          errors++;
        }
        if (data11.net_count === void 0) {
          const err39 = { instancePath: instancePath + "/netlist", schemaPath: "#/$defs/Netlist/required", keyword: "required", params: { missingProperty: "net_count" }, message: "must have required property 'net_count'" };
          if (vErrors === null) {
            vErrors = [err39];
          } else {
            vErrors.push(err39);
          }
          errors++;
        }
        if (data11.page_occurrence_count === void 0) {
          const err40 = { instancePath: instancePath + "/netlist", schemaPath: "#/$defs/Netlist/required", keyword: "required", params: { missingProperty: "page_occurrence_count" }, message: "must have required property 'page_occurrence_count'" };
          if (vErrors === null) {
            vErrors = [err40];
          } else {
            vErrors.push(err40);
          }
          errors++;
        }
        if (data11.graphical_artifact_link_count === void 0) {
          const err41 = { instancePath: instancePath + "/netlist", schemaPath: "#/$defs/Netlist/required", keyword: "required", params: { missingProperty: "graphical_artifact_link_count" }, message: "must have required property 'graphical_artifact_link_count'" };
          if (vErrors === null) {
            vErrors = [err41];
          } else {
            vErrors.push(err41);
          }
          errors++;
        }
        if (data11.design_json !== void 0) {
          let data12 = data11.design_json;
          if (typeof data12 === "string") {
            if (func1(data12) < 1) {
              const err42 = { instancePath: instancePath + "/netlist/design_json", schemaPath: "#/$defs/Netlist/properties/design_json/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
              if (vErrors === null) {
                vErrors = [err42];
              } else {
                vErrors.push(err42);
              }
              errors++;
            }
          } else {
            const err43 = { instancePath: instancePath + "/netlist/design_json", schemaPath: "#/$defs/Netlist/properties/design_json/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err43];
            } else {
              vErrors.push(err43);
            }
            errors++;
          }
        }
        if (data11.design_schema !== void 0) {
          let data13 = data11.design_schema;
          if (typeof data13 !== "string") {
            const err44 = { instancePath: instancePath + "/netlist/design_schema", schemaPath: "#/$defs/Netlist/properties/design_schema/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err44];
            } else {
              vErrors.push(err44);
            }
            errors++;
          }
          if ("altium_monkey.design.b0" !== data13) {
            const err45 = { instancePath: instancePath + "/netlist/design_schema", schemaPath: "#/$defs/Netlist/properties/design_schema/const", keyword: "const", params: { allowedValue: "altium_monkey.design.b0" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err45];
            } else {
              vErrors.push(err45);
            }
            errors++;
          }
        }
        if (data11.compiled_schematic_graph_schema !== void 0) {
          let data14 = data11.compiled_schematic_graph_schema;
          if (typeof data14 !== "string") {
            const err46 = { instancePath: instancePath + "/netlist/compiled_schematic_graph_schema", schemaPath: "#/$defs/Netlist/properties/compiled_schematic_graph_schema/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err46];
            } else {
              vErrors.push(err46);
            }
            errors++;
          }
          if ("altium_monkey.compiled_schematic_graph.a0" !== data14) {
            const err47 = { instancePath: instancePath + "/netlist/compiled_schematic_graph_schema", schemaPath: "#/$defs/Netlist/properties/compiled_schematic_graph_schema/const", keyword: "const", params: { allowedValue: "altium_monkey.compiled_schematic_graph.a0" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err47];
            } else {
              vErrors.push(err47);
            }
            errors++;
          }
        }
        if (data11.component_count !== void 0) {
          let data15 = data11.component_count;
          if (!(typeof data15 == "number" && (!(data15 % 1) && !isNaN(data15)))) {
            const err48 = { instancePath: instancePath + "/netlist/component_count", schemaPath: "#/$defs/Netlist/properties/component_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
            if (vErrors === null) {
              vErrors = [err48];
            } else {
              vErrors.push(err48);
            }
            errors++;
          }
          if (typeof data15 == "number") {
            if (data15 < 0 || isNaN(data15)) {
              const err49 = { instancePath: instancePath + "/netlist/component_count", schemaPath: "#/$defs/Netlist/properties/component_count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
              if (vErrors === null) {
                vErrors = [err49];
              } else {
                vErrors.push(err49);
              }
              errors++;
            }
          }
        }
        if (data11.net_count !== void 0) {
          let data16 = data11.net_count;
          if (!(typeof data16 == "number" && (!(data16 % 1) && !isNaN(data16)))) {
            const err50 = { instancePath: instancePath + "/netlist/net_count", schemaPath: "#/$defs/Netlist/properties/net_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
            if (vErrors === null) {
              vErrors = [err50];
            } else {
              vErrors.push(err50);
            }
            errors++;
          }
          if (typeof data16 == "number") {
            if (data16 < 0 || isNaN(data16)) {
              const err51 = { instancePath: instancePath + "/netlist/net_count", schemaPath: "#/$defs/Netlist/properties/net_count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
              if (vErrors === null) {
                vErrors = [err51];
              } else {
                vErrors.push(err51);
              }
              errors++;
            }
          }
        }
        if (data11.page_occurrence_count !== void 0) {
          let data17 = data11.page_occurrence_count;
          if (!(typeof data17 == "number" && (!(data17 % 1) && !isNaN(data17)))) {
            const err52 = { instancePath: instancePath + "/netlist/page_occurrence_count", schemaPath: "#/$defs/Netlist/properties/page_occurrence_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
            if (vErrors === null) {
              vErrors = [err52];
            } else {
              vErrors.push(err52);
            }
            errors++;
          }
          if (typeof data17 == "number") {
            if (data17 < 0 || isNaN(data17)) {
              const err53 = { instancePath: instancePath + "/netlist/page_occurrence_count", schemaPath: "#/$defs/Netlist/properties/page_occurrence_count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
              if (vErrors === null) {
                vErrors = [err53];
              } else {
                vErrors.push(err53);
              }
              errors++;
            }
          }
        }
        if (data11.graphical_artifact_link_count !== void 0) {
          let data18 = data11.graphical_artifact_link_count;
          if (!(typeof data18 == "number" && (!(data18 % 1) && !isNaN(data18)))) {
            const err54 = { instancePath: instancePath + "/netlist/graphical_artifact_link_count", schemaPath: "#/$defs/Netlist/properties/graphical_artifact_link_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
            if (vErrors === null) {
              vErrors = [err54];
            } else {
              vErrors.push(err54);
            }
            errors++;
          }
          if (typeof data18 == "number") {
            if (data18 < 0 || isNaN(data18)) {
              const err55 = { instancePath: instancePath + "/netlist/graphical_artifact_link_count", schemaPath: "#/$defs/Netlist/properties/graphical_artifact_link_count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
              if (vErrors === null) {
                vErrors = [err55];
              } else {
                vErrors.push(err55);
              }
              errors++;
            }
          }
        }
        for (const key0 in data11) {
          if (key0 !== "design_json" && key0 !== "design_schema" && key0 !== "compiled_schematic_graph_schema" && key0 !== "component_count" && key0 !== "net_count" && key0 !== "page_occurrence_count" && key0 !== "graphical_artifact_link_count") {
            const err56 = { instancePath: instancePath + "/netlist/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/Netlist/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err56];
            } else {
              vErrors.push(err56);
            }
            errors++;
          }
        }
      } else {
        const err57 = { instancePath: instancePath + "/netlist", schemaPath: "#/$defs/Netlist/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err57];
        } else {
          vErrors.push(err57);
        }
        errors++;
      }
    }
    if (data.document_jsons !== void 0) {
      let data20 = data.document_jsons;
      if (Array.isArray(data20)) {
        const len1 = data20.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (!validate25(data20[i1], { instancePath: instancePath + "/document_jsons/" + i1, parentData: data20, parentDataProperty: i1, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate25.errors : vErrors.concat(validate25.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err58 = { instancePath: instancePath + "/document_jsons", schemaPath: "#/properties/document_jsons/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err58];
        } else {
          vErrors.push(err58);
        }
        errors++;
      }
    }
    if (data.library_jsons !== void 0) {
      if (!validate27(data.library_jsons, { instancePath: instancePath + "/library_jsons", parentData: data, parentDataProperty: "library_jsons", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate27.errors : vErrors.concat(validate27.errors);
        errors = vErrors.length;
      }
    }
    if (data.notes !== void 0) {
      if (!validate29(data.notes, { instancePath: instancePath + "/notes", parentData: data, parentDataProperty: "notes", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate29.errors : vErrors.concat(validate29.errors);
        errors = vErrors.length;
      }
    }
    if (data.schlib !== void 0) {
      let data24 = data.schlib;
      if (Array.isArray(data24)) {
        const len2 = data24.length;
        for (let i2 = 0; i2 < len2; i2++) {
          if (!validate31(data24[i2], { instancePath: instancePath + "/schlib/" + i2, parentData: data24, parentDataProperty: i2, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate31.errors : vErrors.concat(validate31.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err59 = { instancePath: instancePath + "/schlib", schemaPath: "#/properties/schlib/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err59];
        } else {
          vErrors.push(err59);
        }
        errors++;
      }
    }
    if (data.pcblib !== void 0) {
      let data26 = data.pcblib;
      if (Array.isArray(data26)) {
        const len3 = data26.length;
        for (let i3 = 0; i3 < len3; i3++) {
          if (!validate35(data26[i3], { instancePath: instancePath + "/pcblib/" + i3, parentData: data26, parentDataProperty: i3, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate35.errors : vErrors.concat(validate35.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err60 = { instancePath: instancePath + "/pcblib", schemaPath: "#/properties/pcblib/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err60];
        } else {
          vErrors.push(err60);
        }
        errors++;
      }
    }
    if (data.embedded_assets !== void 0) {
      if (!validate37(data.embedded_assets, { instancePath: instancePath + "/embedded_assets", parentData: data, parentDataProperty: "embedded_assets", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate37.errors : vErrors.concat(validate37.errors);
        errors = vErrors.length;
      }
    }
    if (data.sch_images !== void 0) {
      if (!validate39(data.sch_images, { instancePath: instancePath + "/sch_images", parentData: data, parentDataProperty: "sch_images", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate39.errors : vErrors.concat(validate39.errors);
        errors = vErrors.length;
      }
    }
    for (const key1 in data) {
      if (key1 !== "schema" && key1 !== "kind" && key1 !== "input_project" && key1 !== "output_root" && key1 !== "variants" && key1 !== "bom_pnp_config" && key1 !== "schdoc_count" && key1 !== "pcbdoc_count" && key1 !== "bom" && key1 !== "pnp" && key1 !== "netlist" && key1 !== "document_jsons" && key1 !== "library_jsons" && key1 !== "notes" && key1 !== "schlib" && key1 !== "pcblib" && key1 !== "embedded_assets" && key1 !== "sch_images") {
        const err61 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
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
  validate20.errors = vErrors;
  return errors === 0;
}
validate20.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
export {
  validate_default as default,
  validate
};
