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
    if (data.roots === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "roots" }, message: "must have required property 'roots'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.recursive === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "recursive" }, message: "must have required property 'recursive'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.symbols === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "symbols" }, message: "must have required property 'symbols'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.footprints === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "footprints" }, message: "must have required property 'footprints'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.warnings === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "warnings" }, message: "must have required property 'warnings'" };
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
      if ("altium_cruncher.libraries.scan.a0" !== data0) {
        const err7 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.libraries.scan.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.roots !== void 0) {
      let data1 = data.roots;
      if (Array.isArray(data1)) {
        const len0 = data1.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (typeof data1[i0] !== "string") {
            const err8 = { instancePath: instancePath + "/roots/" + i0, schemaPath: "#/properties/roots/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err8];
            } else {
              vErrors.push(err8);
            }
            errors++;
          }
        }
      } else {
        const err9 = { instancePath: instancePath + "/roots", schemaPath: "#/properties/roots/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    if (data.recursive !== void 0) {
      if (typeof data.recursive !== "boolean") {
        const err10 = { instancePath: instancePath + "/recursive", schemaPath: "#/properties/recursive/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
    }
    if (data.symbols !== void 0) {
      let data4 = data.symbols;
      if (Array.isArray(data4)) {
        const len1 = data4.length;
        for (let i1 = 0; i1 < len1; i1++) {
          let data5 = data4[i1];
          if (data5 && typeof data5 == "object" && !Array.isArray(data5)) {
            if (data5.name === void 0) {
              const err11 = { instancePath: instancePath + "/symbols/" + i1, schemaPath: "#/$defs/LibraryEntry/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
              if (vErrors === null) {
                vErrors = [err11];
              } else {
                vErrors.push(err11);
              }
              errors++;
            }
            if (data5.library === void 0) {
              const err12 = { instancePath: instancePath + "/symbols/" + i1, schemaPath: "#/$defs/LibraryEntry/required", keyword: "required", params: { missingProperty: "library" }, message: "must have required property 'library'" };
              if (vErrors === null) {
                vErrors = [err12];
              } else {
                vErrors.push(err12);
              }
              errors++;
            }
            if (data5.name !== void 0) {
              if (typeof data5.name !== "string") {
                const err13 = { instancePath: instancePath + "/symbols/" + i1 + "/name", schemaPath: "#/$defs/LibraryEntry/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err13];
                } else {
                  vErrors.push(err13);
                }
                errors++;
              }
            }
            if (data5.library !== void 0) {
              if (typeof data5.library !== "string") {
                const err14 = { instancePath: instancePath + "/symbols/" + i1 + "/library", schemaPath: "#/$defs/LibraryEntry/properties/library/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err14];
                } else {
                  vErrors.push(err14);
                }
                errors++;
              }
            }
            for (const key0 in data5) {
              if (key0 !== "name" && key0 !== "library") {
                const err15 = { instancePath: instancePath + "/symbols/" + i1 + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/LibraryEntry/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err15];
                } else {
                  vErrors.push(err15);
                }
                errors++;
              }
            }
          } else {
            const err16 = { instancePath: instancePath + "/symbols/" + i1, schemaPath: "#/$defs/LibraryEntry/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err16];
            } else {
              vErrors.push(err16);
            }
            errors++;
          }
        }
      } else {
        const err17 = { instancePath: instancePath + "/symbols", schemaPath: "#/properties/symbols/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
    }
    if (data.footprints !== void 0) {
      let data9 = data.footprints;
      if (Array.isArray(data9)) {
        const len2 = data9.length;
        for (let i2 = 0; i2 < len2; i2++) {
          let data10 = data9[i2];
          if (data10 && typeof data10 == "object" && !Array.isArray(data10)) {
            if (data10.name === void 0) {
              const err18 = { instancePath: instancePath + "/footprints/" + i2, schemaPath: "#/$defs/LibraryEntry/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
              if (vErrors === null) {
                vErrors = [err18];
              } else {
                vErrors.push(err18);
              }
              errors++;
            }
            if (data10.library === void 0) {
              const err19 = { instancePath: instancePath + "/footprints/" + i2, schemaPath: "#/$defs/LibraryEntry/required", keyword: "required", params: { missingProperty: "library" }, message: "must have required property 'library'" };
              if (vErrors === null) {
                vErrors = [err19];
              } else {
                vErrors.push(err19);
              }
              errors++;
            }
            if (data10.name !== void 0) {
              if (typeof data10.name !== "string") {
                const err20 = { instancePath: instancePath + "/footprints/" + i2 + "/name", schemaPath: "#/$defs/LibraryEntry/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err20];
                } else {
                  vErrors.push(err20);
                }
                errors++;
              }
            }
            if (data10.library !== void 0) {
              if (typeof data10.library !== "string") {
                const err21 = { instancePath: instancePath + "/footprints/" + i2 + "/library", schemaPath: "#/$defs/LibraryEntry/properties/library/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err21];
                } else {
                  vErrors.push(err21);
                }
                errors++;
              }
            }
            for (const key1 in data10) {
              if (key1 !== "name" && key1 !== "library") {
                const err22 = { instancePath: instancePath + "/footprints/" + i2 + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/LibraryEntry/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err22];
                } else {
                  vErrors.push(err22);
                }
                errors++;
              }
            }
          } else {
            const err23 = { instancePath: instancePath + "/footprints/" + i2, schemaPath: "#/$defs/LibraryEntry/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err23];
            } else {
              vErrors.push(err23);
            }
            errors++;
          }
        }
      } else {
        const err24 = { instancePath: instancePath + "/footprints", schemaPath: "#/properties/footprints/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
    }
    if (data.warnings !== void 0) {
      let data14 = data.warnings;
      if (Array.isArray(data14)) {
        const len3 = data14.length;
        for (let i3 = 0; i3 < len3; i3++) {
          if (typeof data14[i3] !== "string") {
            const err25 = { instancePath: instancePath + "/warnings/" + i3, schemaPath: "#/properties/warnings/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err25];
            } else {
              vErrors.push(err25);
            }
            errors++;
          }
        }
      } else {
        const err26 = { instancePath: instancePath + "/warnings", schemaPath: "#/properties/warnings/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
    }
    for (const key2 in data) {
      if (key2 !== "schema" && key2 !== "roots" && key2 !== "recursive" && key2 !== "symbols" && key2 !== "footprints" && key2 !== "warnings") {
        const err27 = { instancePath: instancePath + "/" + key2.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
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
  validate20.errors = vErrors;
  return errors === 0;
}
validate20.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
export {
  validate_default as default,
  validate
};
