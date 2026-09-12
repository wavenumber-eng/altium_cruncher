// Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit.
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
      if (typeof data0 !== "string") {
        const err2 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      if ("altium_cruncher.mco.operations.a0" !== data0) {
        const err3 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.mco.operations.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.operations !== void 0) {
      let data1 = data.operations;
      if (Array.isArray(data1)) {
        const len0 = data1.length;
        for (let i0 = 0; i0 < len0; i0++) {
          let data2 = data1[i0];
          if (data2 && typeof data2 == "object" && !Array.isArray(data2)) {
            if (data2.op === void 0) {
              const err4 = { instancePath: instancePath + "/operations/" + i0, schemaPath: "#/$defs/McoCatalogEntry/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
              if (vErrors === null) {
                vErrors = [err4];
              } else {
                vErrors.push(err4);
              }
              errors++;
            }
            if (data2.group === void 0) {
              const err5 = { instancePath: instancePath + "/operations/" + i0, schemaPath: "#/$defs/McoCatalogEntry/required", keyword: "required", params: { missingProperty: "group" }, message: "must have required property 'group'" };
              if (vErrors === null) {
                vErrors = [err5];
              } else {
                vErrors.push(err5);
              }
              errors++;
            }
            if (data2.summary === void 0) {
              const err6 = { instancePath: instancePath + "/operations/" + i0, schemaPath: "#/$defs/McoCatalogEntry/required", keyword: "required", params: { missingProperty: "summary" }, message: "must have required property 'summary'" };
              if (vErrors === null) {
                vErrors = [err6];
              } else {
                vErrors.push(err6);
              }
              errors++;
            }
            if (data2.required_args === void 0) {
              const err7 = { instancePath: instancePath + "/operations/" + i0, schemaPath: "#/$defs/McoCatalogEntry/required", keyword: "required", params: { missingProperty: "required_args" }, message: "must have required property 'required_args'" };
              if (vErrors === null) {
                vErrors = [err7];
              } else {
                vErrors.push(err7);
              }
              errors++;
            }
            if (data2.optional_args === void 0) {
              const err8 = { instancePath: instancePath + "/operations/" + i0, schemaPath: "#/$defs/McoCatalogEntry/required", keyword: "required", params: { missingProperty: "optional_args" }, message: "must have required property 'optional_args'" };
              if (vErrors === null) {
                vErrors = [err8];
              } else {
                vErrors.push(err8);
              }
              errors++;
            }
            if (data2.op !== void 0) {
              if (typeof data2.op !== "string") {
                const err9 = { instancePath: instancePath + "/operations/" + i0 + "/op", schemaPath: "#/$defs/McoCatalogEntry/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err9];
                } else {
                  vErrors.push(err9);
                }
                errors++;
              }
            }
            if (data2.group !== void 0) {
              if (typeof data2.group !== "string") {
                const err10 = { instancePath: instancePath + "/operations/" + i0 + "/group", schemaPath: "#/$defs/McoCatalogEntry/properties/group/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err10];
                } else {
                  vErrors.push(err10);
                }
                errors++;
              }
            }
            if (data2.summary !== void 0) {
              if (typeof data2.summary !== "string") {
                const err11 = { instancePath: instancePath + "/operations/" + i0 + "/summary", schemaPath: "#/$defs/McoCatalogEntry/properties/summary/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err11];
                } else {
                  vErrors.push(err11);
                }
                errors++;
              }
            }
            if (data2.required_args !== void 0) {
              let data6 = data2.required_args;
              if (Array.isArray(data6)) {
                const len1 = data6.length;
                for (let i1 = 0; i1 < len1; i1++) {
                  if (typeof data6[i1] !== "string") {
                    const err12 = { instancePath: instancePath + "/operations/" + i0 + "/required_args/" + i1, schemaPath: "#/$defs/McoCatalogEntry/properties/required_args/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                    if (vErrors === null) {
                      vErrors = [err12];
                    } else {
                      vErrors.push(err12);
                    }
                    errors++;
                  }
                }
              } else {
                const err13 = { instancePath: instancePath + "/operations/" + i0 + "/required_args", schemaPath: "#/$defs/McoCatalogEntry/properties/required_args/type", keyword: "type", params: { type: "array" }, message: "must be array" };
                if (vErrors === null) {
                  vErrors = [err13];
                } else {
                  vErrors.push(err13);
                }
                errors++;
              }
            }
            if (data2.optional_args !== void 0) {
              let data8 = data2.optional_args;
              if (Array.isArray(data8)) {
                const len2 = data8.length;
                for (let i2 = 0; i2 < len2; i2++) {
                  if (typeof data8[i2] !== "string") {
                    const err14 = { instancePath: instancePath + "/operations/" + i0 + "/optional_args/" + i2, schemaPath: "#/$defs/McoCatalogEntry/properties/optional_args/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                    if (vErrors === null) {
                      vErrors = [err14];
                    } else {
                      vErrors.push(err14);
                    }
                    errors++;
                  }
                }
              } else {
                const err15 = { instancePath: instancePath + "/operations/" + i0 + "/optional_args", schemaPath: "#/$defs/McoCatalogEntry/properties/optional_args/type", keyword: "type", params: { type: "array" }, message: "must be array" };
                if (vErrors === null) {
                  vErrors = [err15];
                } else {
                  vErrors.push(err15);
                }
                errors++;
              }
            }
            if (data2.aliases !== void 0) {
              let data10 = data2.aliases;
              if (Array.isArray(data10)) {
                const len3 = data10.length;
                for (let i3 = 0; i3 < len3; i3++) {
                  if (typeof data10[i3] !== "string") {
                    const err16 = { instancePath: instancePath + "/operations/" + i0 + "/aliases/" + i3, schemaPath: "#/$defs/McoCatalogEntry/properties/aliases/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                    if (vErrors === null) {
                      vErrors = [err16];
                    } else {
                      vErrors.push(err16);
                    }
                    errors++;
                  }
                }
              } else {
                const err17 = { instancePath: instancePath + "/operations/" + i0 + "/aliases", schemaPath: "#/$defs/McoCatalogEntry/properties/aliases/type", keyword: "type", params: { type: "array" }, message: "must be array" };
                if (vErrors === null) {
                  vErrors = [err17];
                } else {
                  vErrors.push(err17);
                }
                errors++;
              }
            }
            for (const key0 in data2) {
              if (key0 !== "op" && key0 !== "group" && key0 !== "summary" && key0 !== "required_args" && key0 !== "optional_args" && key0 !== "aliases") {
                const err18 = { instancePath: instancePath + "/operations/" + i0 + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/McoCatalogEntry/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err18];
                } else {
                  vErrors.push(err18);
                }
                errors++;
              }
            }
          } else {
            const err19 = { instancePath: instancePath + "/operations/" + i0, schemaPath: "#/$defs/McoCatalogEntry/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err19];
            } else {
              vErrors.push(err19);
            }
            errors++;
          }
        }
      } else {
        const err20 = { instancePath: instancePath + "/operations", schemaPath: "#/properties/operations/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "schema" && key1 !== "operations") {
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
