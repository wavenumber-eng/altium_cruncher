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
    if (data.project === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "project" }, message: "must have required property 'project'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.success === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "success" }, message: "must have required property 'success'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.results === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "results" }, message: "must have required property 'results'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.schema !== void 0) {
      let data0 = data.schema;
      if (typeof data0 !== "string") {
        const err4 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      if ("altium_cruncher.outjob.run.a0" !== data0) {
        const err5 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.outjob.run.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.project !== void 0) {
      if (typeof data.project !== "string") {
        const err6 = { instancePath: instancePath + "/project", schemaPath: "#/properties/project/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.success !== void 0) {
      if (typeof data.success !== "boolean") {
        const err7 = { instancePath: instancePath + "/success", schemaPath: "#/properties/success/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.results !== void 0) {
      let data3 = data.results;
      if (Array.isArray(data3)) {
        const len0 = data3.length;
        for (let i0 = 0; i0 < len0; i0++) {
          let data4 = data3[i0];
          if (data4 && typeof data4 == "object" && !Array.isArray(data4)) {
            if (data4.project === void 0) {
              const err8 = { instancePath: instancePath + "/results/" + i0, schemaPath: "#/$defs/OutjobResult/required", keyword: "required", params: { missingProperty: "project" }, message: "must have required property 'project'" };
              if (vErrors === null) {
                vErrors = [err8];
              } else {
                vErrors.push(err8);
              }
              errors++;
            }
            if (data4.outjob === void 0) {
              const err9 = { instancePath: instancePath + "/results/" + i0, schemaPath: "#/$defs/OutjobResult/required", keyword: "required", params: { missingProperty: "outjob" }, message: "must have required property 'outjob'" };
              if (vErrors === null) {
                vErrors = [err9];
              } else {
                vErrors.push(err9);
              }
              errors++;
            }
            if (data4.success === void 0) {
              const err10 = { instancePath: instancePath + "/results/" + i0, schemaPath: "#/$defs/OutjobResult/required", keyword: "required", params: { missingProperty: "success" }, message: "must have required property 'success'" };
              if (vErrors === null) {
                vErrors = [err10];
              } else {
                vErrors.push(err10);
              }
              errors++;
            }
            if (data4.launch_code === void 0) {
              const err11 = { instancePath: instancePath + "/results/" + i0, schemaPath: "#/$defs/OutjobResult/required", keyword: "required", params: { missingProperty: "launch_code" }, message: "must have required property 'launch_code'" };
              if (vErrors === null) {
                vErrors = [err11];
              } else {
                vErrors.push(err11);
              }
              errors++;
            }
            if (data4.timed_out === void 0) {
              const err12 = { instancePath: instancePath + "/results/" + i0, schemaPath: "#/$defs/OutjobResult/required", keyword: "required", params: { missingProperty: "timed_out" }, message: "must have required property 'timed_out'" };
              if (vErrors === null) {
                vErrors = [err12];
              } else {
                vErrors.push(err12);
              }
              errors++;
            }
            if (data4.error_count === void 0) {
              const err13 = { instancePath: instancePath + "/results/" + i0, schemaPath: "#/$defs/OutjobResult/required", keyword: "required", params: { missingProperty: "error_count" }, message: "must have required property 'error_count'" };
              if (vErrors === null) {
                vErrors = [err13];
              } else {
                vErrors.push(err13);
              }
              errors++;
            }
            if (data4.marker_text === void 0) {
              const err14 = { instancePath: instancePath + "/results/" + i0, schemaPath: "#/$defs/OutjobResult/required", keyword: "required", params: { missingProperty: "marker_text" }, message: "must have required property 'marker_text'" };
              if (vErrors === null) {
                vErrors = [err14];
              } else {
                vErrors.push(err14);
              }
              errors++;
            }
            if (data4.normalized_changed === void 0) {
              const err15 = { instancePath: instancePath + "/results/" + i0, schemaPath: "#/$defs/OutjobResult/required", keyword: "required", params: { missingProperty: "normalized_changed" }, message: "must have required property 'normalized_changed'" };
              if (vErrors === null) {
                vErrors = [err15];
              } else {
                vErrors.push(err15);
              }
              errors++;
            }
            if (data4.rebound_document_paths === void 0) {
              const err16 = { instancePath: instancePath + "/results/" + i0, schemaPath: "#/$defs/OutjobResult/required", keyword: "required", params: { missingProperty: "rebound_document_paths" }, message: "must have required property 'rebound_document_paths'" };
              if (vErrors === null) {
                vErrors = [err16];
              } else {
                vErrors.push(err16);
              }
              errors++;
            }
            if (data4.marker_path === void 0) {
              const err17 = { instancePath: instancePath + "/results/" + i0, schemaPath: "#/$defs/OutjobResult/required", keyword: "required", params: { missingProperty: "marker_path" }, message: "must have required property 'marker_path'" };
              if (vErrors === null) {
                vErrors = [err17];
              } else {
                vErrors.push(err17);
              }
              errors++;
            }
            if (data4.log_path === void 0) {
              const err18 = { instancePath: instancePath + "/results/" + i0, schemaPath: "#/$defs/OutjobResult/required", keyword: "required", params: { missingProperty: "log_path" }, message: "must have required property 'log_path'" };
              if (vErrors === null) {
                vErrors = [err18];
              } else {
                vErrors.push(err18);
              }
              errors++;
            }
            if (data4.project !== void 0) {
              if (typeof data4.project !== "string") {
                const err19 = { instancePath: instancePath + "/results/" + i0 + "/project", schemaPath: "#/$defs/OutjobResult/properties/project/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err19];
                } else {
                  vErrors.push(err19);
                }
                errors++;
              }
            }
            if (data4.outjob !== void 0) {
              if (typeof data4.outjob !== "string") {
                const err20 = { instancePath: instancePath + "/results/" + i0 + "/outjob", schemaPath: "#/$defs/OutjobResult/properties/outjob/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err20];
                } else {
                  vErrors.push(err20);
                }
                errors++;
              }
            }
            if (data4.success !== void 0) {
              if (typeof data4.success !== "boolean") {
                const err21 = { instancePath: instancePath + "/results/" + i0 + "/success", schemaPath: "#/$defs/OutjobResult/properties/success/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
                if (vErrors === null) {
                  vErrors = [err21];
                } else {
                  vErrors.push(err21);
                }
                errors++;
              }
            }
            if (data4.launch_code !== void 0) {
              let data8 = data4.launch_code;
              if (!(typeof data8 == "number" && (!(data8 % 1) && !isNaN(data8)))) {
                const err22 = { instancePath: instancePath + "/results/" + i0 + "/launch_code", schemaPath: "#/$defs/OutjobResult/properties/launch_code/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
                if (vErrors === null) {
                  vErrors = [err22];
                } else {
                  vErrors.push(err22);
                }
                errors++;
              }
            }
            if (data4.timed_out !== void 0) {
              if (typeof data4.timed_out !== "boolean") {
                const err23 = { instancePath: instancePath + "/results/" + i0 + "/timed_out", schemaPath: "#/$defs/OutjobResult/properties/timed_out/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
                if (vErrors === null) {
                  vErrors = [err23];
                } else {
                  vErrors.push(err23);
                }
                errors++;
              }
            }
            if (data4.error_count !== void 0) {
              let data10 = data4.error_count;
              if (!(typeof data10 == "number" && (!(data10 % 1) && !isNaN(data10)))) {
                const err24 = { instancePath: instancePath + "/results/" + i0 + "/error_count", schemaPath: "#/$defs/OutjobResult/properties/error_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
                if (vErrors === null) {
                  vErrors = [err24];
                } else {
                  vErrors.push(err24);
                }
                errors++;
              }
            }
            if (data4.marker_text !== void 0) {
              if (typeof data4.marker_text !== "string") {
                const err25 = { instancePath: instancePath + "/results/" + i0 + "/marker_text", schemaPath: "#/$defs/OutjobResult/properties/marker_text/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err25];
                } else {
                  vErrors.push(err25);
                }
                errors++;
              }
            }
            if (data4.normalized_changed !== void 0) {
              if (typeof data4.normalized_changed !== "boolean") {
                const err26 = { instancePath: instancePath + "/results/" + i0 + "/normalized_changed", schemaPath: "#/$defs/OutjobResult/properties/normalized_changed/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
                if (vErrors === null) {
                  vErrors = [err26];
                } else {
                  vErrors.push(err26);
                }
                errors++;
              }
            }
            if (data4.rebound_document_paths !== void 0) {
              let data13 = data4.rebound_document_paths;
              if (!(typeof data13 == "number" && (!(data13 % 1) && !isNaN(data13)))) {
                const err27 = { instancePath: instancePath + "/results/" + i0 + "/rebound_document_paths", schemaPath: "#/$defs/OutjobResult/properties/rebound_document_paths/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
                if (vErrors === null) {
                  vErrors = [err27];
                } else {
                  vErrors.push(err27);
                }
                errors++;
              }
            }
            if (data4.marker_path !== void 0) {
              if (typeof data4.marker_path !== "string") {
                const err28 = { instancePath: instancePath + "/results/" + i0 + "/marker_path", schemaPath: "#/$defs/OutjobResult/properties/marker_path/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err28];
                } else {
                  vErrors.push(err28);
                }
                errors++;
              }
            }
            if (data4.log_path !== void 0) {
              if (typeof data4.log_path !== "string") {
                const err29 = { instancePath: instancePath + "/results/" + i0 + "/log_path", schemaPath: "#/$defs/OutjobResult/properties/log_path/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err29];
                } else {
                  vErrors.push(err29);
                }
                errors++;
              }
            }
            for (const key0 in data4) {
              if (key0 !== "project" && key0 !== "outjob" && key0 !== "success" && key0 !== "launch_code" && key0 !== "timed_out" && key0 !== "error_count" && key0 !== "marker_text" && key0 !== "normalized_changed" && key0 !== "rebound_document_paths" && key0 !== "marker_path" && key0 !== "log_path") {
                const err30 = { instancePath: instancePath + "/results/" + i0 + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/OutjobResult/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err30];
                } else {
                  vErrors.push(err30);
                }
                errors++;
              }
            }
          } else {
            const err31 = { instancePath: instancePath + "/results/" + i0, schemaPath: "#/$defs/OutjobResult/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err31];
            } else {
              vErrors.push(err31);
            }
            errors++;
          }
        }
      } else {
        const err32 = { instancePath: instancePath + "/results", schemaPath: "#/properties/results/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "schema" && key1 !== "project" && key1 !== "success" && key1 !== "results") {
        const err33 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
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
  validate20.errors = vErrors;
  return errors === 0;
}
validate20.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
export {
  validate_default as default,
  validate
};
