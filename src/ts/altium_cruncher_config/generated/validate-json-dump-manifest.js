// Generated from src/tsp/altium_cruncher/outputs/json-dump.tsp. Do not edit.
// validate.js
var validate = validate20;
var validate_default = validate20;
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
    if (data.outputs === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.schema !== void 0) {
      let data0 = data.schema;
      if (typeof data0 !== "string") {
        const err2 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      if ("altium_cruncher.json_dump.manifest.a0" !== data0) {
        const err3 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.json_dump.manifest.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data1 = data.outputs;
      if (Array.isArray(data1)) {
        const len0 = data1.length;
        for (let i0 = 0; i0 < len0; i0++) {
          let data2 = data1[i0];
          if (data2 && typeof data2 == "object" && !Array.isArray(data2)) {
            if (data2.source_path === void 0) {
              const err4 = { instancePath: instancePath + "/outputs/" + i0, schemaPath: "#/$defs/DumpOutput/required", keyword: "required", params: { missingProperty: "source_path" }, message: "must have required property 'source_path'" };
              if (vErrors === null) {
                vErrors = [err4];
              } else {
                vErrors.push(err4);
              }
              errors++;
            }
            if (data2.output_path === void 0) {
              const err5 = { instancePath: instancePath + "/outputs/" + i0, schemaPath: "#/$defs/DumpOutput/required", keyword: "required", params: { missingProperty: "output_path" }, message: "must have required property 'output_path'" };
              if (vErrors === null) {
                vErrors = [err5];
              } else {
                vErrors.push(err5);
              }
              errors++;
            }
            if (data2.kind === void 0) {
              const err6 = { instancePath: instancePath + "/outputs/" + i0, schemaPath: "#/$defs/DumpOutput/required", keyword: "required", params: { missingProperty: "kind" }, message: "must have required property 'kind'" };
              if (vErrors === null) {
                vErrors = [err6];
              } else {
                vErrors.push(err6);
              }
              errors++;
            }
            if (data2.source_path !== void 0) {
              if (typeof data2.source_path !== "string") {
                const err7 = { instancePath: instancePath + "/outputs/" + i0 + "/source_path", schemaPath: "#/$defs/DumpOutput/properties/source_path/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err7];
                } else {
                  vErrors.push(err7);
                }
                errors++;
              }
            }
            if (data2.output_path !== void 0) {
              if (typeof data2.output_path !== "string") {
                const err8 = { instancePath: instancePath + "/outputs/" + i0 + "/output_path", schemaPath: "#/$defs/DumpOutput/properties/output_path/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err8];
                } else {
                  vErrors.push(err8);
                }
                errors++;
              }
            }
            if (data2.kind !== void 0) {
              let data5 = data2.kind;
              const _errs14 = errors;
              let valid5 = false;
              const _errs15 = errors;
              if (typeof data5 !== "string") {
                const err9 = { instancePath: instancePath + "/outputs/" + i0 + "/kind", schemaPath: "#/$defs/DumpOutput/properties/kind/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err9];
                } else {
                  vErrors.push(err9);
                }
                errors++;
              }
              if ("SchDoc" !== data5) {
                const err10 = { instancePath: instancePath + "/outputs/" + i0 + "/kind", schemaPath: "#/$defs/DumpOutput/properties/kind/anyOf/0/const", keyword: "const", params: { allowedValue: "SchDoc" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err10];
                } else {
                  vErrors.push(err10);
                }
                errors++;
              }
              var _valid0 = _errs15 === errors;
              valid5 = valid5 || _valid0;
              const _errs17 = errors;
              if (typeof data5 !== "string") {
                const err11 = { instancePath: instancePath + "/outputs/" + i0 + "/kind", schemaPath: "#/$defs/DumpOutput/properties/kind/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err11];
                } else {
                  vErrors.push(err11);
                }
                errors++;
              }
              if ("SchLib" !== data5) {
                const err12 = { instancePath: instancePath + "/outputs/" + i0 + "/kind", schemaPath: "#/$defs/DumpOutput/properties/kind/anyOf/1/const", keyword: "const", params: { allowedValue: "SchLib" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err12];
                } else {
                  vErrors.push(err12);
                }
                errors++;
              }
              var _valid0 = _errs17 === errors;
              valid5 = valid5 || _valid0;
              const _errs19 = errors;
              if (typeof data5 !== "string") {
                const err13 = { instancePath: instancePath + "/outputs/" + i0 + "/kind", schemaPath: "#/$defs/DumpOutput/properties/kind/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err13];
                } else {
                  vErrors.push(err13);
                }
                errors++;
              }
              if ("PcbDoc" !== data5) {
                const err14 = { instancePath: instancePath + "/outputs/" + i0 + "/kind", schemaPath: "#/$defs/DumpOutput/properties/kind/anyOf/2/const", keyword: "const", params: { allowedValue: "PcbDoc" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err14];
                } else {
                  vErrors.push(err14);
                }
                errors++;
              }
              var _valid0 = _errs19 === errors;
              valid5 = valid5 || _valid0;
              const _errs21 = errors;
              if (typeof data5 !== "string") {
                const err15 = { instancePath: instancePath + "/outputs/" + i0 + "/kind", schemaPath: "#/$defs/DumpOutput/properties/kind/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err15];
                } else {
                  vErrors.push(err15);
                }
                errors++;
              }
              if ("PcbLib" !== data5) {
                const err16 = { instancePath: instancePath + "/outputs/" + i0 + "/kind", schemaPath: "#/$defs/DumpOutput/properties/kind/anyOf/3/const", keyword: "const", params: { allowedValue: "PcbLib" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err16];
                } else {
                  vErrors.push(err16);
                }
                errors++;
              }
              var _valid0 = _errs21 === errors;
              valid5 = valid5 || _valid0;
              if (!valid5) {
                const err17 = { instancePath: instancePath + "/outputs/" + i0 + "/kind", schemaPath: "#/$defs/DumpOutput/properties/kind/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err17];
                } else {
                  vErrors.push(err17);
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
            for (const key0 in data2) {
              if (key0 !== "source_path" && key0 !== "output_path" && key0 !== "kind") {
                const err18 = { instancePath: instancePath + "/outputs/" + i0 + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/DumpOutput/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err18];
                } else {
                  vErrors.push(err18);
                }
                errors++;
              }
            }
          } else {
            const err19 = { instancePath: instancePath + "/outputs/" + i0, schemaPath: "#/$defs/DumpOutput/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err19];
            } else {
              vErrors.push(err19);
            }
            errors++;
          }
        }
      } else {
        const err20 = { instancePath: instancePath + "/outputs", schemaPath: "#/properties/outputs/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "schema" && key1 !== "outputs") {
        const err21 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
    }
  } else {
    const err22 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err22];
    } else {
      vErrors.push(err22);
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
