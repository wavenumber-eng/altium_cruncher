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
    if (data.source === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "source" }, message: "must have required property 'source'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.output_dir === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "output_dir" }, message: "must have required property 'output_dir'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.component_count === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "component_count" }, message: "must have required property 'component_count'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.component_parse_error === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "component_parse_error" }, message: "must have required property 'component_parse_error'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.source_count === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "source_count" }, message: "must have required property 'source_count'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.libpkg_path === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "libpkg_path" }, message: "must have required property 'libpkg_path'" };
      if (vErrors === null) {
        vErrors = [err6];
      } else {
        vErrors.push(err6);
      }
      errors++;
    }
    if (data.sources === void 0) {
      const err7 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "sources" }, message: "must have required property 'sources'" };
      if (vErrors === null) {
        vErrors = [err7];
      } else {
        vErrors.push(err7);
      }
      errors++;
    }
    if (data.schema !== void 0) {
      let data0 = data.schema;
      if (typeof data0 !== "string") {
        const err8 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      if ("altium_cruncher.extract.intlib.a0" !== data0) {
        const err9 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.extract.intlib.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    if (data.source !== void 0) {
      let data1 = data.source;
      if (data1 && typeof data1 == "object" && !Array.isArray(data1)) {
        if (data1.path === void 0) {
          const err10 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/Source/required", keyword: "required", params: { missingProperty: "path" }, message: "must have required property 'path'" };
          if (vErrors === null) {
            vErrors = [err10];
          } else {
            vErrors.push(err10);
          }
          errors++;
        }
        if (data1.name === void 0) {
          const err11 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/Source/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
          if (vErrors === null) {
            vErrors = [err11];
          } else {
            vErrors.push(err11);
          }
          errors++;
        }
        if (data1.stem === void 0) {
          const err12 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/Source/required", keyword: "required", params: { missingProperty: "stem" }, message: "must have required property 'stem'" };
          if (vErrors === null) {
            vErrors = [err12];
          } else {
            vErrors.push(err12);
          }
          errors++;
        }
        if (data1.path !== void 0) {
          if (typeof data1.path !== "string") {
            const err13 = { instancePath: instancePath + "/source/path", schemaPath: "#/$defs/Source/properties/path/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err13];
            } else {
              vErrors.push(err13);
            }
            errors++;
          }
        }
        if (data1.name !== void 0) {
          if (typeof data1.name !== "string") {
            const err14 = { instancePath: instancePath + "/source/name", schemaPath: "#/$defs/Source/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err14];
            } else {
              vErrors.push(err14);
            }
            errors++;
          }
        }
        if (data1.stem !== void 0) {
          if (typeof data1.stem !== "string") {
            const err15 = { instancePath: instancePath + "/source/stem", schemaPath: "#/$defs/Source/properties/stem/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err15];
            } else {
              vErrors.push(err15);
            }
            errors++;
          }
        }
        for (const key0 in data1) {
          if (key0 !== "path" && key0 !== "name" && key0 !== "stem") {
            const err16 = { instancePath: instancePath + "/source/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/Source/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err16];
            } else {
              vErrors.push(err16);
            }
            errors++;
          }
        }
      } else {
        const err17 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/Source/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
    }
    if (data.output_dir !== void 0) {
      if (typeof data.output_dir !== "string") {
        const err18 = { instancePath: instancePath + "/output_dir", schemaPath: "#/properties/output_dir/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
    }
    if (data.component_count !== void 0) {
      let data7 = data.component_count;
      if (!(typeof data7 == "number" && (!(data7 % 1) && !isNaN(data7)))) {
        const err19 = { instancePath: instancePath + "/component_count", schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
      if (typeof data7 == "number") {
        if (data7 < 0 || isNaN(data7)) {
          const err20 = { instancePath: instancePath + "/component_count", schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err20];
          } else {
            vErrors.push(err20);
          }
          errors++;
        }
      }
    }
    if (data.component_parse_error !== void 0) {
      let data8 = data.component_parse_error;
      const _errs22 = errors;
      let valid5 = false;
      const _errs23 = errors;
      if (typeof data8 !== "string") {
        const err21 = { instancePath: instancePath + "/component_parse_error", schemaPath: "#/properties/component_parse_error/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      var _valid0 = _errs23 === errors;
      valid5 = valid5 || _valid0;
      const _errs25 = errors;
      if (data8 !== null) {
        const err22 = { instancePath: instancePath + "/component_parse_error", schemaPath: "#/properties/component_parse_error/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
      var _valid0 = _errs25 === errors;
      valid5 = valid5 || _valid0;
      if (!valid5) {
        const err23 = { instancePath: instancePath + "/component_parse_error", schemaPath: "#/properties/component_parse_error/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
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
    if (data.source_count !== void 0) {
      let data9 = data.source_count;
      if (!(typeof data9 == "number" && (!(data9 % 1) && !isNaN(data9)))) {
        const err24 = { instancePath: instancePath + "/source_count", schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      if (typeof data9 == "number") {
        if (data9 < 0 || isNaN(data9)) {
          const err25 = { instancePath: instancePath + "/source_count", schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err25];
          } else {
            vErrors.push(err25);
          }
          errors++;
        }
      }
    }
    if (data.libpkg_path !== void 0) {
      let data10 = data.libpkg_path;
      const _errs31 = errors;
      let valid7 = false;
      const _errs32 = errors;
      if (typeof data10 !== "string") {
        const err26 = { instancePath: instancePath + "/libpkg_path", schemaPath: "#/properties/libpkg_path/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
      var _valid1 = _errs32 === errors;
      valid7 = valid7 || _valid1;
      const _errs34 = errors;
      if (data10 !== null) {
        const err27 = { instancePath: instancePath + "/libpkg_path", schemaPath: "#/properties/libpkg_path/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
      var _valid1 = _errs34 === errors;
      valid7 = valid7 || _valid1;
      if (!valid7) {
        const err28 = { instancePath: instancePath + "/libpkg_path", schemaPath: "#/properties/libpkg_path/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
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
    if (data.sources !== void 0) {
      let data11 = data.sources;
      if (Array.isArray(data11)) {
        const len0 = data11.length;
        for (let i0 = 0; i0 < len0; i0++) {
          let data12 = data11[i0];
          if (data12 && typeof data12 == "object" && !Array.isArray(data12)) {
            if (data12.kind === void 0) {
              const err29 = { instancePath: instancePath + "/sources/" + i0, schemaPath: "#/$defs/ExtractedSource/required", keyword: "required", params: { missingProperty: "kind" }, message: "must have required property 'kind'" };
              if (vErrors === null) {
                vErrors = [err29];
              } else {
                vErrors.push(err29);
              }
              errors++;
            }
            if (data12.stream_path === void 0) {
              const err30 = { instancePath: instancePath + "/sources/" + i0, schemaPath: "#/$defs/ExtractedSource/required", keyword: "required", params: { missingProperty: "stream_path" }, message: "must have required property 'stream_path'" };
              if (vErrors === null) {
                vErrors = [err30];
              } else {
                vErrors.push(err30);
              }
              errors++;
            }
            if (data12.original_path === void 0) {
              const err31 = { instancePath: instancePath + "/sources/" + i0, schemaPath: "#/$defs/ExtractedSource/required", keyword: "required", params: { missingProperty: "original_path" }, message: "must have required property 'original_path'" };
              if (vErrors === null) {
                vErrors = [err31];
              } else {
                vErrors.push(err31);
              }
              errors++;
            }
            if (data12.suggested_filename === void 0) {
              const err32 = { instancePath: instancePath + "/sources/" + i0, schemaPath: "#/$defs/ExtractedSource/required", keyword: "required", params: { missingProperty: "suggested_filename" }, message: "must have required property 'suggested_filename'" };
              if (vErrors === null) {
                vErrors = [err32];
              } else {
                vErrors.push(err32);
              }
              errors++;
            }
            if (data12.output_path === void 0) {
              const err33 = { instancePath: instancePath + "/sources/" + i0, schemaPath: "#/$defs/ExtractedSource/required", keyword: "required", params: { missingProperty: "output_path" }, message: "must have required property 'output_path'" };
              if (vErrors === null) {
                vErrors = [err33];
              } else {
                vErrors.push(err33);
              }
              errors++;
            }
            if (data12.output_relative_path === void 0) {
              const err34 = { instancePath: instancePath + "/sources/" + i0, schemaPath: "#/$defs/ExtractedSource/required", keyword: "required", params: { missingProperty: "output_relative_path" }, message: "must have required property 'output_relative_path'" };
              if (vErrors === null) {
                vErrors = [err34];
              } else {
                vErrors.push(err34);
              }
              errors++;
            }
            if (data12.kind !== void 0) {
              if (typeof data12.kind !== "string") {
                const err35 = { instancePath: instancePath + "/sources/" + i0 + "/kind", schemaPath: "#/$defs/ExtractedSource/properties/kind/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err35];
                } else {
                  vErrors.push(err35);
                }
                errors++;
              }
            }
            if (data12.stream_path !== void 0) {
              if (typeof data12.stream_path !== "string") {
                const err36 = { instancePath: instancePath + "/sources/" + i0 + "/stream_path", schemaPath: "#/$defs/ExtractedSource/properties/stream_path/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err36];
                } else {
                  vErrors.push(err36);
                }
                errors++;
              }
            }
            if (data12.original_path !== void 0) {
              if (typeof data12.original_path !== "string") {
                const err37 = { instancePath: instancePath + "/sources/" + i0 + "/original_path", schemaPath: "#/$defs/ExtractedSource/properties/original_path/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err37];
                } else {
                  vErrors.push(err37);
                }
                errors++;
              }
            }
            if (data12.suggested_filename !== void 0) {
              if (typeof data12.suggested_filename !== "string") {
                const err38 = { instancePath: instancePath + "/sources/" + i0 + "/suggested_filename", schemaPath: "#/$defs/ExtractedSource/properties/suggested_filename/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err38];
                } else {
                  vErrors.push(err38);
                }
                errors++;
              }
            }
            if (data12.output_path !== void 0) {
              let data17 = data12.output_path;
              const _errs50 = errors;
              let valid12 = false;
              const _errs51 = errors;
              if (typeof data17 !== "string") {
                const err39 = { instancePath: instancePath + "/sources/" + i0 + "/output_path", schemaPath: "#/$defs/ExtractedSource/properties/output_path/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err39];
                } else {
                  vErrors.push(err39);
                }
                errors++;
              }
              var _valid2 = _errs51 === errors;
              valid12 = valid12 || _valid2;
              const _errs53 = errors;
              if (data17 !== null) {
                const err40 = { instancePath: instancePath + "/sources/" + i0 + "/output_path", schemaPath: "#/$defs/ExtractedSource/properties/output_path/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
                if (vErrors === null) {
                  vErrors = [err40];
                } else {
                  vErrors.push(err40);
                }
                errors++;
              }
              var _valid2 = _errs53 === errors;
              valid12 = valid12 || _valid2;
              if (!valid12) {
                const err41 = { instancePath: instancePath + "/sources/" + i0 + "/output_path", schemaPath: "#/$defs/ExtractedSource/properties/output_path/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err41];
                } else {
                  vErrors.push(err41);
                }
                errors++;
              } else {
                errors = _errs50;
                if (vErrors !== null) {
                  if (_errs50) {
                    vErrors.length = _errs50;
                  } else {
                    vErrors = null;
                  }
                }
              }
            }
            if (data12.output_relative_path !== void 0) {
              let data18 = data12.output_relative_path;
              const _errs56 = errors;
              let valid13 = false;
              const _errs57 = errors;
              if (typeof data18 !== "string") {
                const err42 = { instancePath: instancePath + "/sources/" + i0 + "/output_relative_path", schemaPath: "#/$defs/ExtractedSource/properties/output_relative_path/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err42];
                } else {
                  vErrors.push(err42);
                }
                errors++;
              }
              var _valid3 = _errs57 === errors;
              valid13 = valid13 || _valid3;
              const _errs59 = errors;
              if (data18 !== null) {
                const err43 = { instancePath: instancePath + "/sources/" + i0 + "/output_relative_path", schemaPath: "#/$defs/ExtractedSource/properties/output_relative_path/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
                if (vErrors === null) {
                  vErrors = [err43];
                } else {
                  vErrors.push(err43);
                }
                errors++;
              }
              var _valid3 = _errs59 === errors;
              valid13 = valid13 || _valid3;
              if (!valid13) {
                const err44 = { instancePath: instancePath + "/sources/" + i0 + "/output_relative_path", schemaPath: "#/$defs/ExtractedSource/properties/output_relative_path/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err44];
                } else {
                  vErrors.push(err44);
                }
                errors++;
              } else {
                errors = _errs56;
                if (vErrors !== null) {
                  if (_errs56) {
                    vErrors.length = _errs56;
                  } else {
                    vErrors = null;
                  }
                }
              }
            }
            for (const key1 in data12) {
              if (key1 !== "kind" && key1 !== "stream_path" && key1 !== "original_path" && key1 !== "suggested_filename" && key1 !== "output_path" && key1 !== "output_relative_path") {
                const err45 = { instancePath: instancePath + "/sources/" + i0 + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/ExtractedSource/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err45];
                } else {
                  vErrors.push(err45);
                }
                errors++;
              }
            }
          } else {
            const err46 = { instancePath: instancePath + "/sources/" + i0, schemaPath: "#/$defs/ExtractedSource/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err46];
            } else {
              vErrors.push(err46);
            }
            errors++;
          }
        }
      } else {
        const err47 = { instancePath: instancePath + "/sources", schemaPath: "#/properties/sources/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err47];
        } else {
          vErrors.push(err47);
        }
        errors++;
      }
    }
    for (const key2 in data) {
      if (key2 !== "schema" && key2 !== "source" && key2 !== "output_dir" && key2 !== "component_count" && key2 !== "component_parse_error" && key2 !== "source_count" && key2 !== "libpkg_path" && key2 !== "sources") {
        const err48 = { instancePath: instancePath + "/" + key2.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err48];
        } else {
          vErrors.push(err48);
        }
        errors++;
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
  validate20.errors = vErrors;
  return errors === 0;
}
validate20.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
export {
  validate_default as default,
  validate
};
