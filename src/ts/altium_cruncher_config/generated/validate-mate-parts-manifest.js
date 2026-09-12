// Generated from src/tsp/altium_cruncher/outputs/mate.tsp. Do not edit.
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
        for (const key1 in data0) {
          if (typeof data0[key1] !== "string") {
            const err0 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1") + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/RecordString/unevaluatedProperties/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err0];
            } else {
              vErrors.push(err0);
            }
            errors++;
          }
        }
      } else {
        const err1 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/RecordString/type", keyword: "type", params: { type: "object" }, message: "must be object" };
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
    if (data.parts === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "parts" }, message: "must have required property 'parts'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.designator_normalization === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "designator_normalization" }, message: "must have required property 'designator_normalization'" };
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
      if ("altium_cruncher.mate.parts_cache.a0" !== data0) {
        const err5 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.mate.parts_cache.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.source !== void 0) {
      let data1 = data.source;
      if (data1 && typeof data1 == "object" && !Array.isArray(data1)) {
        if (data1.kind === void 0) {
          const err6 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/PartSource/required", keyword: "required", params: { missingProperty: "kind" }, message: "must have required property 'kind'" };
          if (vErrors === null) {
            vErrors = [err6];
          } else {
            vErrors.push(err6);
          }
          errors++;
        }
        if (data1.project === void 0) {
          const err7 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/PartSource/required", keyword: "required", params: { missingProperty: "project" }, message: "must have required property 'project'" };
          if (vErrors === null) {
            vErrors = [err7];
          } else {
            vErrors.push(err7);
          }
          errors++;
        }
        if (data1.kind !== void 0) {
          if (typeof data1.kind !== "string") {
            const err8 = { instancePath: instancePath + "/source/kind", schemaPath: "#/$defs/PartSource/properties/kind/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err8];
            } else {
              vErrors.push(err8);
            }
            errors++;
          }
        }
        if (data1.project !== void 0) {
          if (typeof data1.project !== "string") {
            const err9 = { instancePath: instancePath + "/source/project", schemaPath: "#/$defs/PartSource/properties/project/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err9];
            } else {
              vErrors.push(err9);
            }
            errors++;
          }
        }
        for (const key0 in data1) {
          if (key0 !== "kind" && key0 !== "project") {
            const err10 = { instancePath: instancePath + "/source/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/PartSource/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err10];
            } else {
              vErrors.push(err10);
            }
            errors++;
          }
        }
      } else {
        const err11 = { instancePath: instancePath + "/source", schemaPath: "#/$defs/PartSource/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
    }
    if (data.parts !== void 0) {
      let data5 = data.parts;
      if (Array.isArray(data5)) {
        const len0 = data5.length;
        for (let i0 = 0; i0 < len0; i0++) {
          let data6 = data5[i0];
          if (data6 && typeof data6 == "object" && !Array.isArray(data6)) {
            if (data6.role === void 0) {
              const err12 = { instancePath: instancePath + "/parts/" + i0, schemaPath: "#/$defs/KnownPart/required", keyword: "required", params: { missingProperty: "role" }, message: "must have required property 'role'" };
              if (vErrors === null) {
                vErrors = [err12];
              } else {
                vErrors.push(err12);
              }
              errors++;
            }
            if (data6.description === void 0) {
              const err13 = { instancePath: instancePath + "/parts/" + i0, schemaPath: "#/$defs/KnownPart/required", keyword: "required", params: { missingProperty: "description" }, message: "must have required property 'description'" };
              if (vErrors === null) {
                vErrors = [err13];
              } else {
                vErrors.push(err13);
              }
              errors++;
            }
            if (data6.symbol_name === void 0) {
              const err14 = { instancePath: instancePath + "/parts/" + i0, schemaPath: "#/$defs/KnownPart/required", keyword: "required", params: { missingProperty: "symbol_name" }, message: "must have required property 'symbol_name'" };
              if (vErrors === null) {
                vErrors = [err14];
              } else {
                vErrors.push(err14);
              }
              errors++;
            }
            if (data6.symbol_library === void 0) {
              const err15 = { instancePath: instancePath + "/parts/" + i0, schemaPath: "#/$defs/KnownPart/required", keyword: "required", params: { missingProperty: "symbol_library" }, message: "must have required property 'symbol_library'" };
              if (vErrors === null) {
                vErrors = [err15];
              } else {
                vErrors.push(err15);
              }
              errors++;
            }
            if (data6.footprint_name === void 0) {
              const err16 = { instancePath: instancePath + "/parts/" + i0, schemaPath: "#/$defs/KnownPart/required", keyword: "required", params: { missingProperty: "footprint_name" }, message: "must have required property 'footprint_name'" };
              if (vErrors === null) {
                vErrors = [err16];
              } else {
                vErrors.push(err16);
              }
              errors++;
            }
            if (data6.footprint_library === void 0) {
              const err17 = { instancePath: instancePath + "/parts/" + i0, schemaPath: "#/$defs/KnownPart/required", keyword: "required", params: { missingProperty: "footprint_library" }, message: "must have required property 'footprint_library'" };
              if (vErrors === null) {
                vErrors = [err17];
              } else {
                vErrors.push(err17);
              }
              errors++;
            }
            if (data6.target_kinds === void 0) {
              const err18 = { instancePath: instancePath + "/parts/" + i0, schemaPath: "#/$defs/KnownPart/required", keyword: "required", params: { missingProperty: "target_kinds" }, message: "must have required property 'target_kinds'" };
              if (vErrors === null) {
                vErrors = [err18];
              } else {
                vErrors.push(err18);
              }
              errors++;
            }
            if (data6.designator_prefix === void 0) {
              const err19 = { instancePath: instancePath + "/parts/" + i0, schemaPath: "#/$defs/KnownPart/required", keyword: "required", params: { missingProperty: "designator_prefix" }, message: "must have required property 'designator_prefix'" };
              if (vErrors === null) {
                vErrors = [err19];
              } else {
                vErrors.push(err19);
              }
              errors++;
            }
            if (data6.signal_pad_designator === void 0) {
              const err20 = { instancePath: instancePath + "/parts/" + i0, schemaPath: "#/$defs/KnownPart/required", keyword: "required", params: { missingProperty: "signal_pad_designator" }, message: "must have required property 'signal_pad_designator'" };
              if (vErrors === null) {
                vErrors = [err20];
              } else {
                vErrors.push(err20);
              }
              errors++;
            }
            if (data6.role !== void 0) {
              if (typeof data6.role !== "string") {
                const err21 = { instancePath: instancePath + "/parts/" + i0 + "/role", schemaPath: "#/$defs/KnownPart/properties/role/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err21];
                } else {
                  vErrors.push(err21);
                }
                errors++;
              }
            }
            if (data6.description !== void 0) {
              if (typeof data6.description !== "string") {
                const err22 = { instancePath: instancePath + "/parts/" + i0 + "/description", schemaPath: "#/$defs/KnownPart/properties/description/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err22];
                } else {
                  vErrors.push(err22);
                }
                errors++;
              }
            }
            if (data6.symbol_name !== void 0) {
              if (typeof data6.symbol_name !== "string") {
                const err23 = { instancePath: instancePath + "/parts/" + i0 + "/symbol_name", schemaPath: "#/$defs/KnownPart/properties/symbol_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err23];
                } else {
                  vErrors.push(err23);
                }
                errors++;
              }
            }
            if (data6.symbol_library !== void 0) {
              if (typeof data6.symbol_library !== "string") {
                const err24 = { instancePath: instancePath + "/parts/" + i0 + "/symbol_library", schemaPath: "#/$defs/KnownPart/properties/symbol_library/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err24];
                } else {
                  vErrors.push(err24);
                }
                errors++;
              }
            }
            if (data6.footprint_name !== void 0) {
              if (typeof data6.footprint_name !== "string") {
                const err25 = { instancePath: instancePath + "/parts/" + i0 + "/footprint_name", schemaPath: "#/$defs/KnownPart/properties/footprint_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err25];
                } else {
                  vErrors.push(err25);
                }
                errors++;
              }
            }
            if (data6.footprint_library !== void 0) {
              if (typeof data6.footprint_library !== "string") {
                const err26 = { instancePath: instancePath + "/parts/" + i0 + "/footprint_library", schemaPath: "#/$defs/KnownPart/properties/footprint_library/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err26];
                } else {
                  vErrors.push(err26);
                }
                errors++;
              }
            }
            if (data6.target_kinds !== void 0) {
              let data13 = data6.target_kinds;
              if (Array.isArray(data13)) {
                const len1 = data13.length;
                for (let i1 = 0; i1 < len1; i1++) {
                  if (typeof data13[i1] !== "string") {
                    const err27 = { instancePath: instancePath + "/parts/" + i0 + "/target_kinds/" + i1, schemaPath: "#/$defs/KnownPart/properties/target_kinds/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                    if (vErrors === null) {
                      vErrors = [err27];
                    } else {
                      vErrors.push(err27);
                    }
                    errors++;
                  }
                }
              } else {
                const err28 = { instancePath: instancePath + "/parts/" + i0 + "/target_kinds", schemaPath: "#/$defs/KnownPart/properties/target_kinds/type", keyword: "type", params: { type: "array" }, message: "must be array" };
                if (vErrors === null) {
                  vErrors = [err28];
                } else {
                  vErrors.push(err28);
                }
                errors++;
              }
            }
            if (data6.designator_prefix !== void 0) {
              if (typeof data6.designator_prefix !== "string") {
                const err29 = { instancePath: instancePath + "/parts/" + i0 + "/designator_prefix", schemaPath: "#/$defs/KnownPart/properties/designator_prefix/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err29];
                } else {
                  vErrors.push(err29);
                }
                errors++;
              }
            }
            if (data6.signal_pad_designator !== void 0) {
              let data16 = data6.signal_pad_designator;
              const _errs38 = errors;
              let valid10 = false;
              const _errs39 = errors;
              if (typeof data16 !== "string") {
                const err30 = { instancePath: instancePath + "/parts/" + i0 + "/signal_pad_designator", schemaPath: "#/$defs/KnownPart/properties/signal_pad_designator/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err30];
                } else {
                  vErrors.push(err30);
                }
                errors++;
              }
              var _valid0 = _errs39 === errors;
              valid10 = valid10 || _valid0;
              const _errs41 = errors;
              if (data16 !== null) {
                const err31 = { instancePath: instancePath + "/parts/" + i0 + "/signal_pad_designator", schemaPath: "#/$defs/KnownPart/properties/signal_pad_designator/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
                if (vErrors === null) {
                  vErrors = [err31];
                } else {
                  vErrors.push(err31);
                }
                errors++;
              }
              var _valid0 = _errs41 === errors;
              valid10 = valid10 || _valid0;
              if (!valid10) {
                const err32 = { instancePath: instancePath + "/parts/" + i0 + "/signal_pad_designator", schemaPath: "#/$defs/KnownPart/properties/signal_pad_designator/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err32];
                } else {
                  vErrors.push(err32);
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
            for (const key1 in data6) {
              if (key1 !== "role" && key1 !== "description" && key1 !== "symbol_name" && key1 !== "symbol_library" && key1 !== "footprint_name" && key1 !== "footprint_library" && key1 !== "target_kinds" && key1 !== "designator_prefix" && key1 !== "signal_pad_designator") {
                const err33 = { instancePath: instancePath + "/parts/" + i0 + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/KnownPart/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err33];
                } else {
                  vErrors.push(err33);
                }
                errors++;
              }
            }
          } else {
            const err34 = { instancePath: instancePath + "/parts/" + i0, schemaPath: "#/$defs/KnownPart/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err34];
            } else {
              vErrors.push(err34);
            }
            errors++;
          }
        }
      } else {
        const err35 = { instancePath: instancePath + "/parts", schemaPath: "#/properties/parts/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err35];
        } else {
          vErrors.push(err35);
        }
        errors++;
      }
    }
    if (data.designator_normalization !== void 0) {
      if (!validate21(data.designator_normalization, { instancePath: instancePath + "/designator_normalization", parentData: data, parentDataProperty: "designator_normalization", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
        errors = vErrors.length;
      }
    }
    for (const key2 in data) {
      if (key2 !== "schema" && key2 !== "source" && key2 !== "parts" && key2 !== "designator_normalization") {
        const err36 = { instancePath: instancePath + "/" + key2.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err36];
        } else {
          vErrors.push(err36);
        }
        errors++;
      }
    }
  } else {
    const err37 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err37];
    } else {
      vErrors.push(err37);
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
