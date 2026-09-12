// Generated from src/tsp/altium_cruncher/outputs/schematic-svg-manifest.tsp. Do not edit.
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
    if (data.input === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "input" }, message: "must have required property 'input'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.design_json === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "design_json" }, message: "must have required property 'design_json'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.design_schema === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "design_schema" }, message: "must have required property 'design_schema'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.compiled_schematic_graph_schema === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "compiled_schematic_graph_schema" }, message: "must have required property 'compiled_schematic_graph_schema'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.svgs === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "svgs" }, message: "must have required property 'svgs'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.schema !== void 0) {
      let data0 = data.schema;
      if (typeof data0 !== "string") {
        const err6 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      if ("altium_cruncher.schematic_svg_manifest.b0" !== data0) {
        const err7 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.schematic_svg_manifest.b0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.input !== void 0) {
      let data1 = data.input;
      if (typeof data1 === "string") {
        if (func1(data1) < 1) {
          const err8 = { instancePath: instancePath + "/input", schemaPath: "#/properties/input/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err8];
          } else {
            vErrors.push(err8);
          }
          errors++;
        }
      } else {
        const err9 = { instancePath: instancePath + "/input", schemaPath: "#/properties/input/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    if (data.design_json !== void 0) {
      let data2 = data.design_json;
      if (typeof data2 === "string") {
        if (func1(data2) < 1) {
          const err10 = { instancePath: instancePath + "/design_json", schemaPath: "#/properties/design_json/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err10];
          } else {
            vErrors.push(err10);
          }
          errors++;
        }
      } else {
        const err11 = { instancePath: instancePath + "/design_json", schemaPath: "#/properties/design_json/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
    }
    if (data.design_schema !== void 0) {
      let data3 = data.design_schema;
      if (typeof data3 !== "string") {
        const err12 = { instancePath: instancePath + "/design_schema", schemaPath: "#/properties/design_schema/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      if ("altium_monkey.design.b0" !== data3) {
        const err13 = { instancePath: instancePath + "/design_schema", schemaPath: "#/properties/design_schema/const", keyword: "const", params: { allowedValue: "altium_monkey.design.b0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.compiled_schematic_graph_schema !== void 0) {
      let data4 = data.compiled_schematic_graph_schema;
      if (typeof data4 !== "string") {
        const err14 = { instancePath: instancePath + "/compiled_schematic_graph_schema", schemaPath: "#/properties/compiled_schematic_graph_schema/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      if ("altium_monkey.compiled_schematic_graph.a0" !== data4) {
        const err15 = { instancePath: instancePath + "/compiled_schematic_graph_schema", schemaPath: "#/properties/compiled_schematic_graph_schema/const", keyword: "const", params: { allowedValue: "altium_monkey.compiled_schematic_graph.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
    }
    if (data.svgs !== void 0) {
      let data5 = data.svgs;
      if (Array.isArray(data5)) {
        if (data5.length < 1) {
          const err16 = { instancePath: instancePath + "/svgs", schemaPath: "#/properties/svgs/minItems", keyword: "minItems", params: { limit: 1 }, message: "must NOT have fewer than 1 items" };
          if (vErrors === null) {
            vErrors = [err16];
          } else {
            vErrors.push(err16);
          }
          errors++;
        }
        const len0 = data5.length;
        for (let i0 = 0; i0 < len0; i0++) {
          let data6 = data5[i0];
          if (data6 && typeof data6 == "object" && !Array.isArray(data6)) {
            if (data6.file === void 0) {
              const err17 = { instancePath: instancePath + "/svgs/" + i0, schemaPath: "#/$defs/SvgArtifact/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
              if (vErrors === null) {
                vErrors = [err17];
              } else {
                vErrors.push(err17);
              }
              errors++;
            }
            if (data6.page_occurrence_ref === void 0) {
              const err18 = { instancePath: instancePath + "/svgs/" + i0, schemaPath: "#/$defs/SvgArtifact/required", keyword: "required", params: { missingProperty: "page_occurrence_ref" }, message: "must have required property 'page_occurrence_ref'" };
              if (vErrors === null) {
                vErrors = [err18];
              } else {
                vErrors.push(err18);
              }
              errors++;
            }
            if (data6.artifact_key === void 0) {
              const err19 = { instancePath: instancePath + "/svgs/" + i0, schemaPath: "#/$defs/SvgArtifact/required", keyword: "required", params: { missingProperty: "artifact_key" }, message: "must have required property 'artifact_key'" };
              if (vErrors === null) {
                vErrors = [err19];
              } else {
                vErrors.push(err19);
              }
              errors++;
            }
            if (data6.source === void 0) {
              const err20 = { instancePath: instancePath + "/svgs/" + i0, schemaPath: "#/$defs/SvgArtifact/required", keyword: "required", params: { missingProperty: "source" }, message: "must have required property 'source'" };
              if (vErrors === null) {
                vErrors = [err20];
              } else {
                vErrors.push(err20);
              }
              errors++;
            }
            if (data6.source_sheet === void 0) {
              const err21 = { instancePath: instancePath + "/svgs/" + i0, schemaPath: "#/$defs/SvgArtifact/required", keyword: "required", params: { missingProperty: "source_sheet" }, message: "must have required property 'source_sheet'" };
              if (vErrors === null) {
                vErrors = [err21];
              } else {
                vErrors.push(err21);
              }
              errors++;
            }
            if (data6.page_number === void 0) {
              const err22 = { instancePath: instancePath + "/svgs/" + i0, schemaPath: "#/$defs/SvgArtifact/required", keyword: "required", params: { missingProperty: "page_number" }, message: "must have required property 'page_number'" };
              if (vErrors === null) {
                vErrors = [err22];
              } else {
                vErrors.push(err22);
              }
              errors++;
            }
            if (data6.page_count === void 0) {
              const err23 = { instancePath: instancePath + "/svgs/" + i0, schemaPath: "#/$defs/SvgArtifact/required", keyword: "required", params: { missingProperty: "page_count" }, message: "must have required property 'page_count'" };
              if (vErrors === null) {
                vErrors = [err23];
              } else {
                vErrors.push(err23);
              }
              errors++;
            }
            if (data6.file !== void 0) {
              let data7 = data6.file;
              if (typeof data7 === "string") {
                if (func1(data7) < 1) {
                  const err24 = { instancePath: instancePath + "/svgs/" + i0 + "/file", schemaPath: "#/$defs/SvgArtifact/properties/file/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
                  if (vErrors === null) {
                    vErrors = [err24];
                  } else {
                    vErrors.push(err24);
                  }
                  errors++;
                }
              } else {
                const err25 = { instancePath: instancePath + "/svgs/" + i0 + "/file", schemaPath: "#/$defs/SvgArtifact/properties/file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err25];
                } else {
                  vErrors.push(err25);
                }
                errors++;
              }
            }
            if (data6.page_occurrence_ref !== void 0) {
              let data8 = data6.page_occurrence_ref;
              if (typeof data8 === "string") {
                if (func1(data8) < 1) {
                  const err26 = { instancePath: instancePath + "/svgs/" + i0 + "/page_occurrence_ref", schemaPath: "#/$defs/SvgArtifact/properties/page_occurrence_ref/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
                  if (vErrors === null) {
                    vErrors = [err26];
                  } else {
                    vErrors.push(err26);
                  }
                  errors++;
                }
              } else {
                const err27 = { instancePath: instancePath + "/svgs/" + i0 + "/page_occurrence_ref", schemaPath: "#/$defs/SvgArtifact/properties/page_occurrence_ref/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err27];
                } else {
                  vErrors.push(err27);
                }
                errors++;
              }
            }
            if (data6.artifact_key !== void 0) {
              let data9 = data6.artifact_key;
              if (typeof data9 !== "string") {
                const err28 = { instancePath: instancePath + "/svgs/" + i0 + "/artifact_key", schemaPath: "#/$defs/SvgArtifact/properties/artifact_key/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err28];
                } else {
                  vErrors.push(err28);
                }
                errors++;
              }
              if ("sch.dwg_scene" !== data9) {
                const err29 = { instancePath: instancePath + "/svgs/" + i0 + "/artifact_key", schemaPath: "#/$defs/SvgArtifact/properties/artifact_key/const", keyword: "const", params: { allowedValue: "sch.dwg_scene" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err29];
                } else {
                  vErrors.push(err29);
                }
                errors++;
              }
            }
            if (data6.source !== void 0) {
              let data10 = data6.source;
              if (typeof data10 === "string") {
                if (func1(data10) < 1) {
                  const err30 = { instancePath: instancePath + "/svgs/" + i0 + "/source", schemaPath: "#/$defs/SvgArtifact/properties/source/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
                  if (vErrors === null) {
                    vErrors = [err30];
                  } else {
                    vErrors.push(err30);
                  }
                  errors++;
                }
              } else {
                const err31 = { instancePath: instancePath + "/svgs/" + i0 + "/source", schemaPath: "#/$defs/SvgArtifact/properties/source/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err31];
                } else {
                  vErrors.push(err31);
                }
                errors++;
              }
            }
            if (data6.source_sheet !== void 0) {
              let data11 = data6.source_sheet;
              if (typeof data11 === "string") {
                if (func1(data11) < 1) {
                  const err32 = { instancePath: instancePath + "/svgs/" + i0 + "/source_sheet", schemaPath: "#/$defs/SvgArtifact/properties/source_sheet/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
                  if (vErrors === null) {
                    vErrors = [err32];
                  } else {
                    vErrors.push(err32);
                  }
                  errors++;
                }
              } else {
                const err33 = { instancePath: instancePath + "/svgs/" + i0 + "/source_sheet", schemaPath: "#/$defs/SvgArtifact/properties/source_sheet/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err33];
                } else {
                  vErrors.push(err33);
                }
                errors++;
              }
            }
            if (data6.page_number !== void 0) {
              let data12 = data6.page_number;
              if (!(typeof data12 == "number" && (!(data12 % 1) && !isNaN(data12)))) {
                const err34 = { instancePath: instancePath + "/svgs/" + i0 + "/page_number", schemaPath: "#/$defs/SvgArtifact/properties/page_number/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
                if (vErrors === null) {
                  vErrors = [err34];
                } else {
                  vErrors.push(err34);
                }
                errors++;
              }
              if (typeof data12 == "number") {
                if (data12 < 1 || isNaN(data12)) {
                  const err35 = { instancePath: instancePath + "/svgs/" + i0 + "/page_number", schemaPath: "#/$defs/SvgArtifact/properties/page_number/minimum", keyword: "minimum", params: { comparison: ">=", limit: 1 }, message: "must be >= 1" };
                  if (vErrors === null) {
                    vErrors = [err35];
                  } else {
                    vErrors.push(err35);
                  }
                  errors++;
                }
              }
            }
            if (data6.page_count !== void 0) {
              let data13 = data6.page_count;
              if (!(typeof data13 == "number" && (!(data13 % 1) && !isNaN(data13)))) {
                const err36 = { instancePath: instancePath + "/svgs/" + i0 + "/page_count", schemaPath: "#/$defs/SvgArtifact/properties/page_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
                if (vErrors === null) {
                  vErrors = [err36];
                } else {
                  vErrors.push(err36);
                }
                errors++;
              }
              if (typeof data13 == "number") {
                if (data13 < 1 || isNaN(data13)) {
                  const err37 = { instancePath: instancePath + "/svgs/" + i0 + "/page_count", schemaPath: "#/$defs/SvgArtifact/properties/page_count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 1 }, message: "must be >= 1" };
                  if (vErrors === null) {
                    vErrors = [err37];
                  } else {
                    vErrors.push(err37);
                  }
                  errors++;
                }
              }
            }
            for (const key0 in data6) {
              if (key0 !== "file" && key0 !== "page_occurrence_ref" && key0 !== "artifact_key" && key0 !== "source" && key0 !== "source_sheet" && key0 !== "page_number" && key0 !== "page_count") {
                const err38 = { instancePath: instancePath + "/svgs/" + i0 + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/SvgArtifact/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err38];
                } else {
                  vErrors.push(err38);
                }
                errors++;
              }
            }
          } else {
            const err39 = { instancePath: instancePath + "/svgs/" + i0, schemaPath: "#/$defs/SvgArtifact/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err39];
            } else {
              vErrors.push(err39);
            }
            errors++;
          }
        }
      } else {
        const err40 = { instancePath: instancePath + "/svgs", schemaPath: "#/properties/svgs/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err40];
        } else {
          vErrors.push(err40);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "schema" && key1 !== "input" && key1 !== "design_json" && key1 !== "design_schema" && key1 !== "compiled_schematic_graph_schema" && key1 !== "svgs") {
        const err41 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err41];
        } else {
          vErrors.push(err41);
        }
        errors++;
      }
    }
  } else {
    const err42 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err42];
    } else {
      vErrors.push(err42);
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
