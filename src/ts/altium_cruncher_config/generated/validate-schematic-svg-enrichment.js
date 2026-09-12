// Generated from src/tsp/altium_cruncher/outputs/schematic-svg-enrichment.tsp. Do not edit.
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
  } else {
    const err1 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err1];
    } else {
      vErrors.push(err1);
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
    if (data.kind === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "kind" }, message: "must have required property 'kind'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.profile === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "profile" }, message: "must have required property 'profile'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.sheet_name === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "sheet_name" }, message: "must have required property 'sheet_name'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.sheet_file === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "sheet_file" }, message: "must have required property 'sheet_file'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.page_occurrence_ref === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "page_occurrence_ref" }, message: "must have required property 'page_occurrence_ref'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.artifact_key === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "artifact_key" }, message: "must have required property 'artifact_key'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.physical_page_metadata === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "physical_page_metadata" }, message: "must have required property 'physical_page_metadata'" };
      if (vErrors === null) {
        vErrors = [err6];
      } else {
        vErrors.push(err6);
      }
      errors++;
    }
    if (data.kind !== void 0) {
      let data0 = data.kind;
      if (typeof data0 !== "string") {
        const err7 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      if ("compiled_schematic_page" !== data0) {
        const err8 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/const", keyword: "const", params: { allowedValue: "compiled_schematic_page" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
    if (data.profile !== void 0) {
      let data1 = data.profile;
      if (typeof data1 !== "string") {
        const err9 = { instancePath: instancePath + "/profile", schemaPath: "#/properties/profile/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      if ("design_review" !== data1) {
        const err10 = { instancePath: instancePath + "/profile", schemaPath: "#/properties/profile/const", keyword: "const", params: { allowedValue: "design_review" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
    }
    if (data.sheet_name !== void 0) {
      if (typeof data.sheet_name !== "string") {
        const err11 = { instancePath: instancePath + "/sheet_name", schemaPath: "#/properties/sheet_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
    }
    if (data.sheet_file !== void 0) {
      let data3 = data.sheet_file;
      if (typeof data3 === "string") {
        if (func1(data3) < 1) {
          const err12 = { instancePath: instancePath + "/sheet_file", schemaPath: "#/properties/sheet_file/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err12];
          } else {
            vErrors.push(err12);
          }
          errors++;
        }
      } else {
        const err13 = { instancePath: instancePath + "/sheet_file", schemaPath: "#/properties/sheet_file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.page_occurrence_ref !== void 0) {
      let data4 = data.page_occurrence_ref;
      if (typeof data4 === "string") {
        if (func1(data4) < 1) {
          const err14 = { instancePath: instancePath + "/page_occurrence_ref", schemaPath: "#/properties/page_occurrence_ref/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
          if (vErrors === null) {
            vErrors = [err14];
          } else {
            vErrors.push(err14);
          }
          errors++;
        }
      } else {
        const err15 = { instancePath: instancePath + "/page_occurrence_ref", schemaPath: "#/properties/page_occurrence_ref/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
    }
    if (data.artifact_key !== void 0) {
      let data5 = data.artifact_key;
      if (typeof data5 !== "string") {
        const err16 = { instancePath: instancePath + "/artifact_key", schemaPath: "#/properties/artifact_key/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      if ("sch.dwg_scene" !== data5) {
        const err17 = { instancePath: instancePath + "/artifact_key", schemaPath: "#/properties/artifact_key/const", keyword: "const", params: { allowedValue: "sch.dwg_scene" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
    }
    if (data.physical_page_metadata !== void 0) {
      if (!validate22(data.physical_page_metadata, { instancePath: instancePath + "/physical_page_metadata", parentData: data, parentDataProperty: "physical_page_metadata", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate22.errors : vErrors.concat(validate22.errors);
        errors = vErrors.length;
      }
    }
    for (const key0 in data) {
      if (key0 !== "kind" && key0 !== "profile" && key0 !== "sheet_name" && key0 !== "sheet_file" && key0 !== "page_occurrence_ref" && key0 !== "artifact_key" && key0 !== "physical_page_metadata") {
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
    if (data.view === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "view" }, message: "must have required property 'view'" };
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
      if ("altium_cruncher.schematic.svg.enrichment.b0" !== data0) {
        const err4 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.schematic.svg.enrichment.b0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.source !== void 0) {
      let data1 = data.source;
      if (data1 && typeof data1 == "object" && !Array.isArray(data1)) {
        if (data1.altium_schdoc_file === void 0) {
          const err5 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/SchematicSvgEnrichmentSource/required", keyword: "required", params: { missingProperty: "altium_schdoc_file" }, message: "must have required property 'altium_schdoc_file'" };
          if (vErrors === null) {
            vErrors = [err5];
          } else {
            vErrors.push(err5);
          }
          errors++;
        }
        if (data1.page_occurrence_ref === void 0) {
          const err6 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/SchematicSvgEnrichmentSource/required", keyword: "required", params: { missingProperty: "page_occurrence_ref" }, message: "must have required property 'page_occurrence_ref'" };
          if (vErrors === null) {
            vErrors = [err6];
          } else {
            vErrors.push(err6);
          }
          errors++;
        }
        if (data1.artifact_key === void 0) {
          const err7 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/SchematicSvgEnrichmentSource/required", keyword: "required", params: { missingProperty: "artifact_key" }, message: "must have required property 'artifact_key'" };
          if (vErrors === null) {
            vErrors = [err7];
          } else {
            vErrors.push(err7);
          }
          errors++;
        }
        if (data1.altium_schdoc_file !== void 0) {
          let data2 = data1.altium_schdoc_file;
          if (typeof data2 === "string") {
            if (func1(data2) < 1) {
              const err8 = { instancePath: instancePath + "/source/altium_schdoc_file", schemaPath: "#/$defs/SchematicSvgEnrichmentSource/properties/altium_schdoc_file/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
              if (vErrors === null) {
                vErrors = [err8];
              } else {
                vErrors.push(err8);
              }
              errors++;
            }
          } else {
            const err9 = { instancePath: instancePath + "/source/altium_schdoc_file", schemaPath: "#/$defs/SchematicSvgEnrichmentSource/properties/altium_schdoc_file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err9];
            } else {
              vErrors.push(err9);
            }
            errors++;
          }
        }
        if (data1.page_occurrence_ref !== void 0) {
          let data3 = data1.page_occurrence_ref;
          if (typeof data3 === "string") {
            if (func1(data3) < 1) {
              const err10 = { instancePath: instancePath + "/source/page_occurrence_ref", schemaPath: "#/$defs/SchematicSvgEnrichmentSource/properties/page_occurrence_ref/minLength", keyword: "minLength", params: { limit: 1 }, message: "must NOT have fewer than 1 characters" };
              if (vErrors === null) {
                vErrors = [err10];
              } else {
                vErrors.push(err10);
              }
              errors++;
            }
          } else {
            const err11 = { instancePath: instancePath + "/source/page_occurrence_ref", schemaPath: "#/$defs/SchematicSvgEnrichmentSource/properties/page_occurrence_ref/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err11];
            } else {
              vErrors.push(err11);
            }
            errors++;
          }
        }
        if (data1.artifact_key !== void 0) {
          let data4 = data1.artifact_key;
          if (typeof data4 !== "string") {
            const err12 = { instancePath: instancePath + "/source/artifact_key", schemaPath: "#/$defs/SchematicSvgEnrichmentSource/properties/artifact_key/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err12];
            } else {
              vErrors.push(err12);
            }
            errors++;
          }
          if ("sch.dwg_scene" !== data4) {
            const err13 = { instancePath: instancePath + "/source/artifact_key", schemaPath: "#/$defs/SchematicSvgEnrichmentSource/properties/artifact_key/const", keyword: "const", params: { allowedValue: "sch.dwg_scene" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err13];
            } else {
              vErrors.push(err13);
            }
            errors++;
          }
        }
        for (const key0 in data1) {
          if (key0 !== "altium_schdoc_file" && key0 !== "page_occurrence_ref" && key0 !== "artifact_key") {
            const err14 = { instancePath: instancePath + "/source/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/SchematicSvgEnrichmentSource/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err14];
            } else {
              vErrors.push(err14);
            }
            errors++;
          }
        }
      } else {
        const err15 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/SchematicSvgEnrichmentSource/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
    }
    if (data.view !== void 0) {
      if (!validate21(data.view, { instancePath: instancePath + "/view", parentData: data, parentDataProperty: "view", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
        errors = vErrors.length;
      }
    }
    for (const key1 in data) {
      if (key1 !== "schema" && key1 !== "source" && key1 !== "view") {
        const err16 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
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
  validate20.errors = vErrors;
  return errors === 0;
}
validate20.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
export {
  validate_default as default,
  validate
};
