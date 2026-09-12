// Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit.
// validate.js
var validate = validate20;
var validate_default = validate20;
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
    for (const key0 in data) {
      let data0 = data[key0];
      if (data0 && typeof data0 == "object" && !Array.isArray(data0)) {
        if (data0.file === void 0) {
          const err0 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/SvgLayerOutput/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
          if (vErrors === null) {
            vErrors = [err0];
          } else {
            vErrors.push(err0);
          }
          errors++;
        }
        if (data0.layers === void 0) {
          const err1 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/SvgLayerOutput/required", keyword: "required", params: { missingProperty: "layers" }, message: "must have required property 'layers'" };
          if (vErrors === null) {
            vErrors = [err1];
          } else {
            vErrors.push(err1);
          }
          errors++;
        }
        if (data0.group_id === void 0) {
          const err2 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/SvgLayerOutput/required", keyword: "required", params: { missingProperty: "group_id" }, message: "must have required property 'group_id'" };
          if (vErrors === null) {
            vErrors = [err2];
          } else {
            vErrors.push(err2);
          }
          errors++;
        }
        if (data0.file !== void 0) {
          if (typeof data0.file !== "string") {
            const err3 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1") + "/file", schemaPath: "#/$defs/SvgLayerOutput/properties/file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err3];
            } else {
              vErrors.push(err3);
            }
            errors++;
          }
        }
        if (data0.layers !== void 0) {
          let data2 = data0.layers;
          if (Array.isArray(data2)) {
            const len0 = data2.length;
            for (let i0 = 0; i0 < len0; i0++) {
              if (typeof data2[i0] !== "string") {
                const err4 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1") + "/layers/" + i0, schemaPath: "#/$defs/SvgLayerOutput/properties/layers/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err4];
                } else {
                  vErrors.push(err4);
                }
                errors++;
              }
            }
          } else {
            const err5 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1") + "/layers", schemaPath: "#/$defs/SvgLayerOutput/properties/layers/type", keyword: "type", params: { type: "array" }, message: "must be array" };
            if (vErrors === null) {
              vErrors = [err5];
            } else {
              vErrors.push(err5);
            }
            errors++;
          }
        }
        if (data0.group_id !== void 0) {
          if (typeof data0.group_id !== "string") {
            const err6 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1") + "/group_id", schemaPath: "#/$defs/SvgLayerOutput/properties/group_id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err6];
            } else {
              vErrors.push(err6);
            }
            errors++;
          }
        }
        for (const key1 in data0) {
          if (key1 !== "file" && key1 !== "layers" && key1 !== "group_id") {
            const err7 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1") + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/SvgLayerOutput/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err7];
            } else {
              vErrors.push(err7);
            }
            errors++;
          }
        }
      } else {
        const err8 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/SvgLayerOutput/type", keyword: "type", params: { type: "object" }, message: "must be object" };
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
    for (const key0 in data) {
      let data0 = data[key0];
      if (data0 && typeof data0 == "object" && !Array.isArray(data0)) {
        if (data0.file === void 0) {
          const err0 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/SvgViewOutput/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
          if (vErrors === null) {
            vErrors = [err0];
          } else {
            vErrors.push(err0);
          }
          errors++;
        }
        if (data0.group_id === void 0) {
          const err1 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/SvgViewOutput/required", keyword: "required", params: { missingProperty: "group_id" }, message: "must have required property 'group_id'" };
          if (vErrors === null) {
            vErrors = [err1];
          } else {
            vErrors.push(err1);
          }
          errors++;
        }
        if (data0.layers === void 0) {
          const err2 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/SvgViewOutput/required", keyword: "required", params: { missingProperty: "layers" }, message: "must have required property 'layers'" };
          if (vErrors === null) {
            vErrors = [err2];
          } else {
            vErrors.push(err2);
          }
          errors++;
        }
        if (data0.mirrored === void 0) {
          const err3 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/SvgViewOutput/required", keyword: "required", params: { missingProperty: "mirrored" }, message: "must have required property 'mirrored'" };
          if (vErrors === null) {
            vErrors = [err3];
          } else {
            vErrors.push(err3);
          }
          errors++;
        }
        if (data0.assembly_hlr_mode === void 0) {
          const err4 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/SvgViewOutput/required", keyword: "required", params: { missingProperty: "assembly_hlr_mode" }, message: "must have required property 'assembly_hlr_mode'" };
          if (vErrors === null) {
            vErrors = [err4];
          } else {
            vErrors.push(err4);
          }
          errors++;
        }
        if (data0.file !== void 0) {
          if (typeof data0.file !== "string") {
            const err5 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1") + "/file", schemaPath: "#/$defs/SvgViewOutput/properties/file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err5];
            } else {
              vErrors.push(err5);
            }
            errors++;
          }
        }
        if (data0.group_id !== void 0) {
          if (typeof data0.group_id !== "string") {
            const err6 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1") + "/group_id", schemaPath: "#/$defs/SvgViewOutput/properties/group_id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err6];
            } else {
              vErrors.push(err6);
            }
            errors++;
          }
        }
        if (data0.layers !== void 0) {
          let data3 = data0.layers;
          if (Array.isArray(data3)) {
            const len0 = data3.length;
            for (let i0 = 0; i0 < len0; i0++) {
              if (typeof data3[i0] !== "string") {
                const err7 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1") + "/layers/" + i0, schemaPath: "#/$defs/SvgViewOutput/properties/layers/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err7];
                } else {
                  vErrors.push(err7);
                }
                errors++;
              }
            }
          } else {
            const err8 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1") + "/layers", schemaPath: "#/$defs/SvgViewOutput/properties/layers/type", keyword: "type", params: { type: "array" }, message: "must be array" };
            if (vErrors === null) {
              vErrors = [err8];
            } else {
              vErrors.push(err8);
            }
            errors++;
          }
        }
        if (data0.mirrored !== void 0) {
          if (typeof data0.mirrored !== "boolean") {
            const err9 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1") + "/mirrored", schemaPath: "#/$defs/SvgViewOutput/properties/mirrored/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err9];
            } else {
              vErrors.push(err9);
            }
            errors++;
          }
        }
        if (data0.assembly_hlr_mode !== void 0) {
          if (typeof data0.assembly_hlr_mode !== "string") {
            const err10 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1") + "/assembly_hlr_mode", schemaPath: "#/$defs/SvgViewOutput/properties/assembly_hlr_mode/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err10];
            } else {
              vErrors.push(err10);
            }
            errors++;
          }
        }
        for (const key1 in data0) {
          if (key1 !== "file" && key1 !== "group_id" && key1 !== "layers" && key1 !== "mirrored" && key1 !== "assembly_hlr_mode") {
            const err11 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1") + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/SvgViewOutput/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err11];
            } else {
              vErrors.push(err11);
            }
            errors++;
          }
        }
      } else {
        const err12 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/SvgViewOutput/type", keyword: "type", params: { type: "object" }, message: "must be object" };
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
    if (data.board === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "board" }, message: "must have required property 'board'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.source_input === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "source_input" }, message: "must have required property 'source_input'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.layer_outputs === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "layer_outputs" }, message: "must have required property 'layer_outputs'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.views === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "views" }, message: "must have required property 'views'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.schema !== void 0) {
      let data0 = data.schema;
      if (typeof data0 !== "string") {
        const err5 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      if ("pcb.svg.manifest.a0" !== data0) {
        const err6 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "pcb.svg.manifest.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.board !== void 0) {
      if (typeof data.board !== "string") {
        const err7 = { instancePath: instancePath + "/board", schemaPath: "#/properties/board/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.source_input !== void 0) {
      if (typeof data.source_input !== "string") {
        const err8 = { instancePath: instancePath + "/source_input", schemaPath: "#/properties/source_input/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
    if (data.layer_outputs !== void 0) {
      if (!validate21(data.layer_outputs, { instancePath: instancePath + "/layer_outputs", parentData: data, parentDataProperty: "layer_outputs", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
        errors = vErrors.length;
      }
    }
    if (data.views !== void 0) {
      if (!validate23(data.views, { instancePath: instancePath + "/views", parentData: data, parentDataProperty: "views", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate23.errors : vErrors.concat(validate23.errors);
        errors = vErrors.length;
      }
    }
    for (const key0 in data) {
      if (key0 !== "schema" && key0 !== "board" && key0 !== "source_input" && key0 !== "layer_outputs" && key0 !== "views") {
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
  validate20.errors = vErrors;
  return errors === 0;
}
validate20.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
export {
  validate_default as default,
  validate
};
