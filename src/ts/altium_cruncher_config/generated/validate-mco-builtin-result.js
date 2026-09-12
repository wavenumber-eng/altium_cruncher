// Generated from src/tsp/altium_cruncher/outputs/mco-builtins.tsp. Do not edit.
// validate.js
var validate = validate20;
var validate_default = validate20;
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
    if (data.name === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.unique_id === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "unique_id" }, message: "must have required property 'unique_id'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.allow_fabrication === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "allow_fabrication" }, message: "must have required property 'allow_fabrication'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.current === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "current" }, message: "must have required property 'current'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.dnp === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "dnp" }, message: "must have required property 'dnp'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.variation_count === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "variation_count" }, message: "must have required property 'variation_count'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.parameter_count === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "parameter_count" }, message: "must have required property 'parameter_count'" };
      if (vErrors === null) {
        vErrors = [err6];
      } else {
        vErrors.push(err6);
      }
      errors++;
    }
    if (data.param_variation_count === void 0) {
      const err7 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "param_variation_count" }, message: "must have required property 'param_variation_count'" };
      if (vErrors === null) {
        vErrors = [err7];
      } else {
        vErrors.push(err7);
      }
      errors++;
    }
    if (data.rows === void 0) {
      const err8 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "rows" }, message: "must have required property 'rows'" };
      if (vErrors === null) {
        vErrors = [err8];
      } else {
        vErrors.push(err8);
      }
      errors++;
    }
    if (data.name !== void 0) {
      if (typeof data.name !== "string") {
        const err9 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    if (data.unique_id !== void 0) {
      if (typeof data.unique_id !== "string") {
        const err10 = { instancePath: instancePath + "/unique_id", schemaPath: "#/properties/unique_id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
    }
    if (data.allow_fabrication !== void 0) {
      if (typeof data.allow_fabrication !== "boolean") {
        const err11 = { instancePath: instancePath + "/allow_fabrication", schemaPath: "#/properties/allow_fabrication/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
    }
    if (data.current !== void 0) {
      if (typeof data.current !== "boolean") {
        const err12 = { instancePath: instancePath + "/current", schemaPath: "#/properties/current/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
    }
    if (data.dnp !== void 0) {
      let data4 = data.dnp;
      if (Array.isArray(data4)) {
        const len0 = data4.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (typeof data4[i0] !== "string") {
            const err13 = { instancePath: instancePath + "/dnp/" + i0, schemaPath: "#/properties/dnp/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err13];
            } else {
              vErrors.push(err13);
            }
            errors++;
          }
        }
      } else {
        const err14 = { instancePath: instancePath + "/dnp", schemaPath: "#/properties/dnp/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
    }
    if (data.variation_count !== void 0) {
      let data6 = data.variation_count;
      if (!(typeof data6 == "number" && (!(data6 % 1) && !isNaN(data6)))) {
        const err15 = { instancePath: instancePath + "/variation_count", schemaPath: "#/$defs/ImportedVariantsList_Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      if (typeof data6 == "number") {
        if (data6 < 0 || isNaN(data6)) {
          const err16 = { instancePath: instancePath + "/variation_count", schemaPath: "#/$defs/ImportedVariantsList_Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err16];
          } else {
            vErrors.push(err16);
          }
          errors++;
        }
      }
    }
    if (data.parameter_count !== void 0) {
      let data7 = data.parameter_count;
      if (!(typeof data7 == "number" && (!(data7 % 1) && !isNaN(data7)))) {
        const err17 = { instancePath: instancePath + "/parameter_count", schemaPath: "#/$defs/ImportedVariantsList_Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      if (typeof data7 == "number") {
        if (data7 < 0 || isNaN(data7)) {
          const err18 = { instancePath: instancePath + "/parameter_count", schemaPath: "#/$defs/ImportedVariantsList_Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err18];
          } else {
            vErrors.push(err18);
          }
          errors++;
        }
      }
    }
    if (data.param_variation_count !== void 0) {
      let data8 = data.param_variation_count;
      if (!(typeof data8 == "number" && (!(data8 % 1) && !isNaN(data8)))) {
        const err19 = { instancePath: instancePath + "/param_variation_count", schemaPath: "#/$defs/ImportedVariantsList_Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
      if (typeof data8 == "number") {
        if (data8 < 0 || isNaN(data8)) {
          const err20 = { instancePath: instancePath + "/param_variation_count", schemaPath: "#/$defs/ImportedVariantsList_Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err20];
          } else {
            vErrors.push(err20);
          }
          errors++;
        }
      }
    }
    if (data.rows !== void 0) {
      let data9 = data.rows;
      if (Array.isArray(data9)) {
        const len1 = data9.length;
        for (let i1 = 0; i1 < len1; i1++) {
          let data10 = data9[i1];
          if (data10 && typeof data10 == "object" && !Array.isArray(data10)) {
            if (data10.variant === void 0) {
              const err21 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/ImportedVariantsList_VariantRow/required", keyword: "required", params: { missingProperty: "variant" }, message: "must have required property 'variant'" };
              if (vErrors === null) {
                vErrors = [err21];
              } else {
                vErrors.push(err21);
              }
              errors++;
            }
            if (data10.sheet === void 0) {
              const err22 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/ImportedVariantsList_VariantRow/required", keyword: "required", params: { missingProperty: "sheet" }, message: "must have required property 'sheet'" };
              if (vErrors === null) {
                vErrors = [err22];
              } else {
                vErrors.push(err22);
              }
              errors++;
            }
            if (data10.designator === void 0) {
              const err23 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/ImportedVariantsList_VariantRow/required", keyword: "required", params: { missingProperty: "designator" }, message: "must have required property 'designator'" };
              if (vErrors === null) {
                vErrors = [err23];
              } else {
                vErrors.push(err23);
              }
              errors++;
            }
            if (data10.operation === void 0) {
              const err24 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/ImportedVariantsList_VariantRow/required", keyword: "required", params: { missingProperty: "operation" }, message: "must have required property 'operation'" };
              if (vErrors === null) {
                vErrors = [err24];
              } else {
                vErrors.push(err24);
              }
              errors++;
            }
            if (data10.detail === void 0) {
              const err25 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/ImportedVariantsList_VariantRow/required", keyword: "required", params: { missingProperty: "detail" }, message: "must have required property 'detail'" };
              if (vErrors === null) {
                vErrors = [err25];
              } else {
                vErrors.push(err25);
              }
              errors++;
            }
            if (data10.component_value === void 0) {
              const err26 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/ImportedVariantsList_VariantRow/required", keyword: "required", params: { missingProperty: "component_value" }, message: "must have required property 'component_value'" };
              if (vErrors === null) {
                vErrors = [err26];
              } else {
                vErrors.push(err26);
              }
              errors++;
            }
            if (data10.parameter_name === void 0) {
              const err27 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/ImportedVariantsList_VariantRow/required", keyword: "required", params: { missingProperty: "parameter_name" }, message: "must have required property 'parameter_name'" };
              if (vErrors === null) {
                vErrors = [err27];
              } else {
                vErrors.push(err27);
              }
              errors++;
            }
            if (data10.value === void 0) {
              const err28 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/ImportedVariantsList_VariantRow/required", keyword: "required", params: { missingProperty: "value" }, message: "must have required property 'value'" };
              if (vErrors === null) {
                vErrors = [err28];
              } else {
                vErrors.push(err28);
              }
              errors++;
            }
            if (data10.unique_id === void 0) {
              const err29 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/ImportedVariantsList_VariantRow/required", keyword: "required", params: { missingProperty: "unique_id" }, message: "must have required property 'unique_id'" };
              if (vErrors === null) {
                vErrors = [err29];
              } else {
                vErrors.push(err29);
              }
              errors++;
            }
            if (data10.variant !== void 0) {
              if (typeof data10.variant !== "string") {
                const err30 = { instancePath: instancePath + "/rows/" + i1 + "/variant", schemaPath: "#/$defs/ImportedVariantsList_VariantRow/properties/variant/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err30];
                } else {
                  vErrors.push(err30);
                }
                errors++;
              }
            }
            if (data10.sheet !== void 0) {
              if (typeof data10.sheet !== "string") {
                const err31 = { instancePath: instancePath + "/rows/" + i1 + "/sheet", schemaPath: "#/$defs/ImportedVariantsList_VariantRow/properties/sheet/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err31];
                } else {
                  vErrors.push(err31);
                }
                errors++;
              }
            }
            if (data10.designator !== void 0) {
              if (typeof data10.designator !== "string") {
                const err32 = { instancePath: instancePath + "/rows/" + i1 + "/designator", schemaPath: "#/$defs/ImportedVariantsList_VariantRow/properties/designator/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err32];
                } else {
                  vErrors.push(err32);
                }
                errors++;
              }
            }
            if (data10.operation !== void 0) {
              if (typeof data10.operation !== "string") {
                const err33 = { instancePath: instancePath + "/rows/" + i1 + "/operation", schemaPath: "#/$defs/ImportedVariantsList_VariantRow/properties/operation/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err33];
                } else {
                  vErrors.push(err33);
                }
                errors++;
              }
            }
            if (data10.detail !== void 0) {
              if (typeof data10.detail !== "string") {
                const err34 = { instancePath: instancePath + "/rows/" + i1 + "/detail", schemaPath: "#/$defs/ImportedVariantsList_VariantRow/properties/detail/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err34];
                } else {
                  vErrors.push(err34);
                }
                errors++;
              }
            }
            if (data10.component_value !== void 0) {
              if (typeof data10.component_value !== "string") {
                const err35 = { instancePath: instancePath + "/rows/" + i1 + "/component_value", schemaPath: "#/$defs/ImportedVariantsList_VariantRow/properties/component_value/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err35];
                } else {
                  vErrors.push(err35);
                }
                errors++;
              }
            }
            if (data10.parameter_name !== void 0) {
              if (typeof data10.parameter_name !== "string") {
                const err36 = { instancePath: instancePath + "/rows/" + i1 + "/parameter_name", schemaPath: "#/$defs/ImportedVariantsList_VariantRow/properties/parameter_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err36];
                } else {
                  vErrors.push(err36);
                }
                errors++;
              }
            }
            if (data10.value !== void 0) {
              if (typeof data10.value !== "string") {
                const err37 = { instancePath: instancePath + "/rows/" + i1 + "/value", schemaPath: "#/$defs/ImportedVariantsList_VariantRow/properties/value/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err37];
                } else {
                  vErrors.push(err37);
                }
                errors++;
              }
            }
            if (data10.unique_id !== void 0) {
              if (typeof data10.unique_id !== "string") {
                const err38 = { instancePath: instancePath + "/rows/" + i1 + "/unique_id", schemaPath: "#/$defs/ImportedVariantsList_VariantRow/properties/unique_id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err38];
                } else {
                  vErrors.push(err38);
                }
                errors++;
              }
            }
            if (data10.alternate_part !== void 0) {
              if (typeof data10.alternate_part !== "string") {
                const err39 = { instancePath: instancePath + "/rows/" + i1 + "/alternate_part", schemaPath: "#/$defs/ImportedVariantsList_VariantRow/properties/alternate_part/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err39];
                } else {
                  vErrors.push(err39);
                }
                errors++;
              }
            }
            if (data10.alternate_part_resolved !== void 0) {
              if (typeof data10.alternate_part_resolved !== "string") {
                const err40 = { instancePath: instancePath + "/rows/" + i1 + "/alternate_part_resolved", schemaPath: "#/$defs/ImportedVariantsList_VariantRow/properties/alternate_part_resolved/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err40];
                } else {
                  vErrors.push(err40);
                }
                errors++;
              }
            }
            for (const key0 in data10) {
              if (key0 !== "variant" && key0 !== "sheet" && key0 !== "designator" && key0 !== "operation" && key0 !== "detail" && key0 !== "component_value" && key0 !== "parameter_name" && key0 !== "value" && key0 !== "unique_id" && key0 !== "alternate_part" && key0 !== "alternate_part_resolved") {
                const err41 = { instancePath: instancePath + "/rows/" + i1 + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/ImportedVariantsList_VariantRow/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err41];
                } else {
                  vErrors.push(err41);
                }
                errors++;
              }
            }
          } else {
            const err42 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/ImportedVariantsList_VariantRow/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err42];
            } else {
              vErrors.push(err42);
            }
            errors++;
          }
        }
      } else {
        const err43 = { instancePath: instancePath + "/rows", schemaPath: "#/properties/rows/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err43];
        } else {
          vErrors.push(err43);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "name" && key1 !== "unique_id" && key1 !== "allow_fabrication" && key1 !== "current" && key1 !== "dnp" && key1 !== "variation_count" && key1 !== "parameter_count" && key1 !== "param_variation_count" && key1 !== "rows") {
        const err44 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err44];
        } else {
          vErrors.push(err44);
        }
        errors++;
      }
    }
  } else {
    const err45 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err45];
    } else {
      vErrors.push(err45);
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
    if (data.current_variant === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "current_variant" }, message: "must have required property 'current_variant'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.variant_count === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "variant_count" }, message: "must have required property 'variant_count'" };
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
    if (data.rows === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "rows" }, message: "must have required property 'rows'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.index_errors === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "index_errors" }, message: "must have required property 'index_errors'" };
      if (vErrors === null) {
        vErrors = [err6];
      } else {
        vErrors.push(err6);
      }
      errors++;
    }
    if (data.schema !== void 0) {
      let data0 = data.schema;
      if (typeof data0 !== "string") {
        const err7 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      if ("altium_cruncher.variants.list.a0" !== data0) {
        const err8 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.variants.list.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
    if (data.project !== void 0) {
      if (typeof data.project !== "string") {
        const err9 = { instancePath: instancePath + "/project", schemaPath: "#/properties/project/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    if (data.current_variant !== void 0) {
      let data2 = data.current_variant;
      const _errs6 = errors;
      let valid1 = false;
      const _errs7 = errors;
      if (typeof data2 !== "string") {
        const err10 = { instancePath: instancePath + "/current_variant", schemaPath: "#/properties/current_variant/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid1 = valid1 || _valid0;
      const _errs9 = errors;
      if (data2 !== null) {
        const err11 = { instancePath: instancePath + "/current_variant", schemaPath: "#/properties/current_variant/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid1 = valid1 || _valid0;
      if (!valid1) {
        const err12 = { instancePath: instancePath + "/current_variant", schemaPath: "#/properties/current_variant/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      } else {
        errors = _errs6;
        if (vErrors !== null) {
          if (_errs6) {
            vErrors.length = _errs6;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.variant_count !== void 0) {
      let data3 = data.variant_count;
      if (!(typeof data3 == "number" && (!(data3 % 1) && !isNaN(data3)))) {
        const err13 = { instancePath: instancePath + "/variant_count", schemaPath: "#/$defs/ImportedVariantsList_Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      if (typeof data3 == "number") {
        if (data3 < 0 || isNaN(data3)) {
          const err14 = { instancePath: instancePath + "/variant_count", schemaPath: "#/$defs/ImportedVariantsList_Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err14];
          } else {
            vErrors.push(err14);
          }
          errors++;
        }
      }
    }
    if (data.variants !== void 0) {
      let data4 = data.variants;
      if (Array.isArray(data4)) {
        const len0 = data4.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!validate22(data4[i0], { instancePath: instancePath + "/variants/" + i0, parentData: data4, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate22.errors : vErrors.concat(validate22.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err15 = { instancePath: instancePath + "/variants", schemaPath: "#/properties/variants/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
    }
    if (data.rows !== void 0) {
      let data6 = data.rows;
      if (Array.isArray(data6)) {
        const len1 = data6.length;
        for (let i1 = 0; i1 < len1; i1++) {
          let data7 = data6[i1];
          if (data7 && typeof data7 == "object" && !Array.isArray(data7)) {
            if (data7.variant === void 0) {
              const err16 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/ImportedVariantsList_VariantRow/required", keyword: "required", params: { missingProperty: "variant" }, message: "must have required property 'variant'" };
              if (vErrors === null) {
                vErrors = [err16];
              } else {
                vErrors.push(err16);
              }
              errors++;
            }
            if (data7.sheet === void 0) {
              const err17 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/ImportedVariantsList_VariantRow/required", keyword: "required", params: { missingProperty: "sheet" }, message: "must have required property 'sheet'" };
              if (vErrors === null) {
                vErrors = [err17];
              } else {
                vErrors.push(err17);
              }
              errors++;
            }
            if (data7.designator === void 0) {
              const err18 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/ImportedVariantsList_VariantRow/required", keyword: "required", params: { missingProperty: "designator" }, message: "must have required property 'designator'" };
              if (vErrors === null) {
                vErrors = [err18];
              } else {
                vErrors.push(err18);
              }
              errors++;
            }
            if (data7.operation === void 0) {
              const err19 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/ImportedVariantsList_VariantRow/required", keyword: "required", params: { missingProperty: "operation" }, message: "must have required property 'operation'" };
              if (vErrors === null) {
                vErrors = [err19];
              } else {
                vErrors.push(err19);
              }
              errors++;
            }
            if (data7.detail === void 0) {
              const err20 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/ImportedVariantsList_VariantRow/required", keyword: "required", params: { missingProperty: "detail" }, message: "must have required property 'detail'" };
              if (vErrors === null) {
                vErrors = [err20];
              } else {
                vErrors.push(err20);
              }
              errors++;
            }
            if (data7.component_value === void 0) {
              const err21 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/ImportedVariantsList_VariantRow/required", keyword: "required", params: { missingProperty: "component_value" }, message: "must have required property 'component_value'" };
              if (vErrors === null) {
                vErrors = [err21];
              } else {
                vErrors.push(err21);
              }
              errors++;
            }
            if (data7.parameter_name === void 0) {
              const err22 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/ImportedVariantsList_VariantRow/required", keyword: "required", params: { missingProperty: "parameter_name" }, message: "must have required property 'parameter_name'" };
              if (vErrors === null) {
                vErrors = [err22];
              } else {
                vErrors.push(err22);
              }
              errors++;
            }
            if (data7.value === void 0) {
              const err23 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/ImportedVariantsList_VariantRow/required", keyword: "required", params: { missingProperty: "value" }, message: "must have required property 'value'" };
              if (vErrors === null) {
                vErrors = [err23];
              } else {
                vErrors.push(err23);
              }
              errors++;
            }
            if (data7.unique_id === void 0) {
              const err24 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/ImportedVariantsList_VariantRow/required", keyword: "required", params: { missingProperty: "unique_id" }, message: "must have required property 'unique_id'" };
              if (vErrors === null) {
                vErrors = [err24];
              } else {
                vErrors.push(err24);
              }
              errors++;
            }
            if (data7.variant !== void 0) {
              if (typeof data7.variant !== "string") {
                const err25 = { instancePath: instancePath + "/rows/" + i1 + "/variant", schemaPath: "#/$defs/ImportedVariantsList_VariantRow/properties/variant/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err25];
                } else {
                  vErrors.push(err25);
                }
                errors++;
              }
            }
            if (data7.sheet !== void 0) {
              if (typeof data7.sheet !== "string") {
                const err26 = { instancePath: instancePath + "/rows/" + i1 + "/sheet", schemaPath: "#/$defs/ImportedVariantsList_VariantRow/properties/sheet/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err26];
                } else {
                  vErrors.push(err26);
                }
                errors++;
              }
            }
            if (data7.designator !== void 0) {
              if (typeof data7.designator !== "string") {
                const err27 = { instancePath: instancePath + "/rows/" + i1 + "/designator", schemaPath: "#/$defs/ImportedVariantsList_VariantRow/properties/designator/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err27];
                } else {
                  vErrors.push(err27);
                }
                errors++;
              }
            }
            if (data7.operation !== void 0) {
              if (typeof data7.operation !== "string") {
                const err28 = { instancePath: instancePath + "/rows/" + i1 + "/operation", schemaPath: "#/$defs/ImportedVariantsList_VariantRow/properties/operation/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err28];
                } else {
                  vErrors.push(err28);
                }
                errors++;
              }
            }
            if (data7.detail !== void 0) {
              if (typeof data7.detail !== "string") {
                const err29 = { instancePath: instancePath + "/rows/" + i1 + "/detail", schemaPath: "#/$defs/ImportedVariantsList_VariantRow/properties/detail/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err29];
                } else {
                  vErrors.push(err29);
                }
                errors++;
              }
            }
            if (data7.component_value !== void 0) {
              if (typeof data7.component_value !== "string") {
                const err30 = { instancePath: instancePath + "/rows/" + i1 + "/component_value", schemaPath: "#/$defs/ImportedVariantsList_VariantRow/properties/component_value/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err30];
                } else {
                  vErrors.push(err30);
                }
                errors++;
              }
            }
            if (data7.parameter_name !== void 0) {
              if (typeof data7.parameter_name !== "string") {
                const err31 = { instancePath: instancePath + "/rows/" + i1 + "/parameter_name", schemaPath: "#/$defs/ImportedVariantsList_VariantRow/properties/parameter_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err31];
                } else {
                  vErrors.push(err31);
                }
                errors++;
              }
            }
            if (data7.value !== void 0) {
              if (typeof data7.value !== "string") {
                const err32 = { instancePath: instancePath + "/rows/" + i1 + "/value", schemaPath: "#/$defs/ImportedVariantsList_VariantRow/properties/value/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err32];
                } else {
                  vErrors.push(err32);
                }
                errors++;
              }
            }
            if (data7.unique_id !== void 0) {
              if (typeof data7.unique_id !== "string") {
                const err33 = { instancePath: instancePath + "/rows/" + i1 + "/unique_id", schemaPath: "#/$defs/ImportedVariantsList_VariantRow/properties/unique_id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err33];
                } else {
                  vErrors.push(err33);
                }
                errors++;
              }
            }
            if (data7.alternate_part !== void 0) {
              if (typeof data7.alternate_part !== "string") {
                const err34 = { instancePath: instancePath + "/rows/" + i1 + "/alternate_part", schemaPath: "#/$defs/ImportedVariantsList_VariantRow/properties/alternate_part/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err34];
                } else {
                  vErrors.push(err34);
                }
                errors++;
              }
            }
            if (data7.alternate_part_resolved !== void 0) {
              if (typeof data7.alternate_part_resolved !== "string") {
                const err35 = { instancePath: instancePath + "/rows/" + i1 + "/alternate_part_resolved", schemaPath: "#/$defs/ImportedVariantsList_VariantRow/properties/alternate_part_resolved/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err35];
                } else {
                  vErrors.push(err35);
                }
                errors++;
              }
            }
            for (const key0 in data7) {
              if (key0 !== "variant" && key0 !== "sheet" && key0 !== "designator" && key0 !== "operation" && key0 !== "detail" && key0 !== "component_value" && key0 !== "parameter_name" && key0 !== "value" && key0 !== "unique_id" && key0 !== "alternate_part" && key0 !== "alternate_part_resolved") {
                const err36 = { instancePath: instancePath + "/rows/" + i1 + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/ImportedVariantsList_VariantRow/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err36];
                } else {
                  vErrors.push(err36);
                }
                errors++;
              }
            }
          } else {
            const err37 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/ImportedVariantsList_VariantRow/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err37];
            } else {
              vErrors.push(err37);
            }
            errors++;
          }
        }
      } else {
        const err38 = { instancePath: instancePath + "/rows", schemaPath: "#/properties/rows/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err38];
        } else {
          vErrors.push(err38);
        }
        errors++;
      }
    }
    if (data.index_errors !== void 0) {
      let data20 = data.index_errors;
      if (Array.isArray(data20)) {
        const len2 = data20.length;
        for (let i2 = 0; i2 < len2; i2++) {
          if (typeof data20[i2] !== "string") {
            const err39 = { instancePath: instancePath + "/index_errors/" + i2, schemaPath: "#/properties/index_errors/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err39];
            } else {
              vErrors.push(err39);
            }
            errors++;
          }
        }
      } else {
        const err40 = { instancePath: instancePath + "/index_errors", schemaPath: "#/properties/index_errors/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err40];
        } else {
          vErrors.push(err40);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "schema" && key1 !== "project" && key1 !== "current_variant" && key1 !== "variant_count" && key1 !== "variants" && key1 !== "rows" && key1 !== "index_errors") {
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
  const _errs1 = errors;
  let valid0 = false;
  const _errs2 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err0 = { instancePath, schemaPath: "#/$defs/Failure/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err1 = { instancePath, schemaPath: "#/$defs/Failure/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err2 = { instancePath, schemaPath: "#/$defs/Failure/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err3 = { instancePath, schemaPath: "#/$defs/Failure/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err4 = { instancePath, schemaPath: "#/$defs/Failure/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.op !== void 0) {
      if (typeof data.op !== "string") {
        const err5 = { instancePath: instancePath + "/op", schemaPath: "#/$defs/Failure/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err6 = { instancePath: instancePath + "/id", schemaPath: "#/$defs/Failure/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data2 = data.status;
      if (typeof data2 !== "string") {
        const err7 = { instancePath: instancePath + "/status", schemaPath: "#/$defs/Failure/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      if ("fail" !== data2) {
        const err8 = { instancePath: instancePath + "/status", schemaPath: "#/$defs/Failure/properties/status/const", keyword: "const", params: { allowedValue: "fail" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err9 = { instancePath: instancePath + "/message", schemaPath: "#/$defs/Failure/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data4 = data.outputs;
      if (data4 && typeof data4 == "object" && !Array.isArray(data4)) {
        for (const key0 in data4) {
          const err10 = { instancePath: instancePath + "/outputs/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/Failure/properties/outputs/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
          if (vErrors === null) {
            vErrors = [err10];
          } else {
            vErrors.push(err10);
          }
          errors++;
        }
      } else {
        const err11 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/Failure/properties/outputs/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
    }
    if (data.error !== void 0) {
      if (typeof data.error !== "string") {
        const err12 = { instancePath: instancePath + "/error", schemaPath: "#/$defs/Failure/properties/error/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "op" && key1 !== "id" && key1 !== "status" && key1 !== "message" && key1 !== "outputs" && key1 !== "error") {
        const err13 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/Failure/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
  } else {
    const err14 = { instancePath, schemaPath: "#/$defs/Failure/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err14];
    } else {
      vErrors.push(err14);
    }
    errors++;
  }
  var _valid0 = _errs2 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    var props0 = true;
  }
  const _errs23 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err15 = { instancePath, schemaPath: "#/anyOf/1/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err15];
      } else {
        vErrors.push(err15);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err16 = { instancePath, schemaPath: "#/anyOf/1/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err16];
      } else {
        vErrors.push(err16);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err17 = { instancePath, schemaPath: "#/anyOf/1/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err17];
      } else {
        vErrors.push(err17);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err18 = { instancePath, schemaPath: "#/anyOf/1/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err18];
      } else {
        vErrors.push(err18);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err19 = { instancePath, schemaPath: "#/anyOf/1/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err19];
      } else {
        vErrors.push(err19);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data8 = data.op;
      const _errs26 = errors;
      let valid6 = false;
      const _errs27 = errors;
      if (typeof data8 !== "string") {
        const err20 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/1/properties/op/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      if ("mco.message" !== data8) {
        const err21 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/1/properties/op/anyOf/0/const", keyword: "const", params: { allowedValue: "mco.message" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      var _valid1 = _errs27 === errors;
      valid6 = valid6 || _valid1;
      const _errs29 = errors;
      if (typeof data8 !== "string") {
        const err22 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/1/properties/op/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
      if ("message" !== data8) {
        const err23 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/1/properties/op/anyOf/1/const", keyword: "const", params: { allowedValue: "message" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      var _valid1 = _errs29 === errors;
      valid6 = valid6 || _valid1;
      if (!valid6) {
        const err24 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/1/properties/op/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      } else {
        errors = _errs26;
        if (vErrors !== null) {
          if (_errs26) {
            vErrors.length = _errs26;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err25 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/1/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data10 = data.status;
      if (typeof data10 !== "string") {
        const err26 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/1/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
      if ("ok" !== data10) {
        const err27 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/1/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err28 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/1/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data12 = data.outputs;
      if (data12 && typeof data12 == "object" && !Array.isArray(data12)) {
        for (const key2 in data12) {
          const err29 = { instancePath: instancePath + "/outputs/" + key2.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/1/properties/outputs/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
          if (vErrors === null) {
            vErrors = [err29];
          } else {
            vErrors.push(err29);
          }
          errors++;
        }
      } else {
        const err30 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/1/properties/outputs/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
        }
        errors++;
      }
    }
    for (const key3 in data) {
      if (key3 !== "op" && key3 !== "id" && key3 !== "status" && key3 !== "message" && key3 !== "outputs") {
        const err31 = { instancePath: instancePath + "/" + key3.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/1/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      }
    }
  } else {
    const err32 = { instancePath, schemaPath: "#/anyOf/1/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err32];
    } else {
      vErrors.push(err32);
    }
    errors++;
  }
  var _valid0 = _errs23 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs45 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err33 = { instancePath, schemaPath: "#/anyOf/2/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err33];
      } else {
        vErrors.push(err33);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err34 = { instancePath, schemaPath: "#/anyOf/2/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err34];
      } else {
        vErrors.push(err34);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err35 = { instancePath, schemaPath: "#/anyOf/2/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err35];
      } else {
        vErrors.push(err35);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err36 = { instancePath, schemaPath: "#/anyOf/2/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err36];
      } else {
        vErrors.push(err36);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err37 = { instancePath, schemaPath: "#/anyOf/2/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err37];
      } else {
        vErrors.push(err37);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data15 = data.op;
      if (typeof data15 !== "string") {
        const err38 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/2/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err38];
        } else {
          vErrors.push(err38);
        }
        errors++;
      }
      if ("project.create" !== data15) {
        const err39 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/2/properties/op/const", keyword: "const", params: { allowedValue: "project.create" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err39];
        } else {
          vErrors.push(err39);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err40 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/2/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err40];
        } else {
          vErrors.push(err40);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data17 = data.status;
      if (typeof data17 !== "string") {
        const err41 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/2/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err41];
        } else {
          vErrors.push(err41);
        }
        errors++;
      }
      if ("ok" !== data17) {
        const err42 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/2/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err42];
        } else {
          vErrors.push(err42);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err43 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/2/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err43];
        } else {
          vErrors.push(err43);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data19 = data.outputs;
      if (data19 && typeof data19 == "object" && !Array.isArray(data19)) {
        if (data19.project === void 0) {
          const err44 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/ProjectPath/required", keyword: "required", params: { missingProperty: "project" }, message: "must have required property 'project'" };
          if (vErrors === null) {
            vErrors = [err44];
          } else {
            vErrors.push(err44);
          }
          errors++;
        }
        if (data19.project !== void 0) {
          if (typeof data19.project !== "string") {
            const err45 = { instancePath: instancePath + "/outputs/project", schemaPath: "#/$defs/ProjectPath/properties/project/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err45];
            } else {
              vErrors.push(err45);
            }
            errors++;
          }
        }
        for (const key4 in data19) {
          if (key4 !== "project") {
            const err46 = { instancePath: instancePath + "/outputs/" + key4.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/ProjectPath/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err46];
            } else {
              vErrors.push(err46);
            }
            errors++;
          }
        }
      } else {
        const err47 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/ProjectPath/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err47];
        } else {
          vErrors.push(err47);
        }
        errors++;
      }
    }
    for (const key5 in data) {
      if (key5 !== "op" && key5 !== "id" && key5 !== "status" && key5 !== "message" && key5 !== "outputs") {
        const err48 = { instancePath: instancePath + "/" + key5.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/2/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err48];
        } else {
          vErrors.push(err48);
        }
        errors++;
      }
    }
  } else {
    const err49 = { instancePath, schemaPath: "#/anyOf/2/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err49];
    } else {
      vErrors.push(err49);
    }
    errors++;
  }
  var _valid0 = _errs45 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs66 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err50 = { instancePath, schemaPath: "#/anyOf/3/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err50];
      } else {
        vErrors.push(err50);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err51 = { instancePath, schemaPath: "#/anyOf/3/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err51];
      } else {
        vErrors.push(err51);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err52 = { instancePath, schemaPath: "#/anyOf/3/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err52];
      } else {
        vErrors.push(err52);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err53 = { instancePath, schemaPath: "#/anyOf/3/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err53];
      } else {
        vErrors.push(err53);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err54 = { instancePath, schemaPath: "#/anyOf/3/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err54];
      } else {
        vErrors.push(err54);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data23 = data.op;
      if (typeof data23 !== "string") {
        const err55 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/3/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err55];
        } else {
          vErrors.push(err55);
        }
        errors++;
      }
      if ("project.add_document" !== data23) {
        const err56 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/3/properties/op/const", keyword: "const", params: { allowedValue: "project.add_document" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err56];
        } else {
          vErrors.push(err56);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err57 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/3/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err57];
        } else {
          vErrors.push(err57);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data25 = data.status;
      if (typeof data25 !== "string") {
        const err58 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/3/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err58];
        } else {
          vErrors.push(err58);
        }
        errors++;
      }
      if ("ok" !== data25) {
        const err59 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/3/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err59];
        } else {
          vErrors.push(err59);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err60 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/3/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err60];
        } else {
          vErrors.push(err60);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data27 = data.outputs;
      if (data27 && typeof data27 == "object" && !Array.isArray(data27)) {
        if (data27.project === void 0) {
          const err61 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/3/properties/outputs/required", keyword: "required", params: { missingProperty: "project" }, message: "must have required property 'project'" };
          if (vErrors === null) {
            vErrors = [err61];
          } else {
            vErrors.push(err61);
          }
          errors++;
        }
        if (data27.document === void 0) {
          const err62 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/3/properties/outputs/required", keyword: "required", params: { missingProperty: "document" }, message: "must have required property 'document'" };
          if (vErrors === null) {
            vErrors = [err62];
          } else {
            vErrors.push(err62);
          }
          errors++;
        }
        if (data27.project !== void 0) {
          if (typeof data27.project !== "string") {
            const err63 = { instancePath: instancePath + "/outputs/project", schemaPath: "#/anyOf/3/properties/outputs/properties/project/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err63];
            } else {
              vErrors.push(err63);
            }
            errors++;
          }
        }
        if (data27.document !== void 0) {
          if (typeof data27.document !== "string") {
            const err64 = { instancePath: instancePath + "/outputs/document", schemaPath: "#/anyOf/3/properties/outputs/properties/document/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err64];
            } else {
              vErrors.push(err64);
            }
            errors++;
          }
        }
        for (const key6 in data27) {
          if (key6 !== "project" && key6 !== "document") {
            const err65 = { instancePath: instancePath + "/outputs/" + key6.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/3/properties/outputs/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err65];
            } else {
              vErrors.push(err65);
            }
            errors++;
          }
        }
      } else {
        const err66 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/3/properties/outputs/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err66];
        } else {
          vErrors.push(err66);
        }
        errors++;
      }
    }
    for (const key7 in data) {
      if (key7 !== "op" && key7 !== "id" && key7 !== "status" && key7 !== "message" && key7 !== "outputs") {
        const err67 = { instancePath: instancePath + "/" + key7.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/3/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err67];
        } else {
          vErrors.push(err67);
        }
        errors++;
      }
    }
  } else {
    const err68 = { instancePath, schemaPath: "#/anyOf/3/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err68];
    } else {
      vErrors.push(err68);
    }
    errors++;
  }
  var _valid0 = _errs66 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs88 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err69 = { instancePath, schemaPath: "#/anyOf/4/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err69];
      } else {
        vErrors.push(err69);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err70 = { instancePath, schemaPath: "#/anyOf/4/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err70];
      } else {
        vErrors.push(err70);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err71 = { instancePath, schemaPath: "#/anyOf/4/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err71];
      } else {
        vErrors.push(err71);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err72 = { instancePath, schemaPath: "#/anyOf/4/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err72];
      } else {
        vErrors.push(err72);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err73 = { instancePath, schemaPath: "#/anyOf/4/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err73];
      } else {
        vErrors.push(err73);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data32 = data.op;
      const _errs91 = errors;
      let valid19 = false;
      const _errs92 = errors;
      if (typeof data32 !== "string") {
        const err74 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/4/properties/op/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err74];
        } else {
          vErrors.push(err74);
        }
        errors++;
      }
      if ("project.add_parameter" !== data32) {
        const err75 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/4/properties/op/anyOf/0/const", keyword: "const", params: { allowedValue: "project.add_parameter" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err75];
        } else {
          vErrors.push(err75);
        }
        errors++;
      }
      var _valid2 = _errs92 === errors;
      valid19 = valid19 || _valid2;
      const _errs94 = errors;
      if (typeof data32 !== "string") {
        const err76 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/4/properties/op/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err76];
        } else {
          vErrors.push(err76);
        }
        errors++;
      }
      if ("project.add_variant" !== data32) {
        const err77 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/4/properties/op/anyOf/1/const", keyword: "const", params: { allowedValue: "project.add_variant" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err77];
        } else {
          vErrors.push(err77);
        }
        errors++;
      }
      var _valid2 = _errs94 === errors;
      valid19 = valid19 || _valid2;
      if (!valid19) {
        const err78 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/4/properties/op/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err78];
        } else {
          vErrors.push(err78);
        }
        errors++;
      } else {
        errors = _errs91;
        if (vErrors !== null) {
          if (_errs91) {
            vErrors.length = _errs91;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err79 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/4/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err79];
        } else {
          vErrors.push(err79);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data34 = data.status;
      if (typeof data34 !== "string") {
        const err80 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/4/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err80];
        } else {
          vErrors.push(err80);
        }
        errors++;
      }
      if ("ok" !== data34) {
        const err81 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/4/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err81];
        } else {
          vErrors.push(err81);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err82 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/4/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err82];
        } else {
          vErrors.push(err82);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data36 = data.outputs;
      if (data36 && typeof data36 == "object" && !Array.isArray(data36)) {
        if (data36.project === void 0) {
          const err83 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/NamedProject/required", keyword: "required", params: { missingProperty: "project" }, message: "must have required property 'project'" };
          if (vErrors === null) {
            vErrors = [err83];
          } else {
            vErrors.push(err83);
          }
          errors++;
        }
        if (data36.name === void 0) {
          const err84 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/NamedProject/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
          if (vErrors === null) {
            vErrors = [err84];
          } else {
            vErrors.push(err84);
          }
          errors++;
        }
        if (data36.project !== void 0) {
          if (typeof data36.project !== "string") {
            const err85 = { instancePath: instancePath + "/outputs/project", schemaPath: "#/$defs/NamedProject/properties/project/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err85];
            } else {
              vErrors.push(err85);
            }
            errors++;
          }
        }
        if (data36.name !== void 0) {
          if (typeof data36.name !== "string") {
            const err86 = { instancePath: instancePath + "/outputs/name", schemaPath: "#/$defs/NamedProject/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err86];
            } else {
              vErrors.push(err86);
            }
            errors++;
          }
        }
        for (const key8 in data36) {
          if (key8 !== "project" && key8 !== "name") {
            const err87 = { instancePath: instancePath + "/outputs/" + key8.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/NamedProject/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err87];
            } else {
              vErrors.push(err87);
            }
            errors++;
          }
        }
      } else {
        const err88 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/NamedProject/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err88];
        } else {
          vErrors.push(err88);
        }
        errors++;
      }
    }
    for (const key9 in data) {
      if (key9 !== "op" && key9 !== "id" && key9 !== "status" && key9 !== "message" && key9 !== "outputs") {
        const err89 = { instancePath: instancePath + "/" + key9.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/4/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err89];
        } else {
          vErrors.push(err89);
        }
        errors++;
      }
    }
  } else {
    const err90 = { instancePath, schemaPath: "#/anyOf/4/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err90];
    } else {
      vErrors.push(err90);
    }
    errors++;
  }
  var _valid0 = _errs88 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs115 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err91 = { instancePath, schemaPath: "#/anyOf/5/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err91];
      } else {
        vErrors.push(err91);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err92 = { instancePath, schemaPath: "#/anyOf/5/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err92];
      } else {
        vErrors.push(err92);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err93 = { instancePath, schemaPath: "#/anyOf/5/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err93];
      } else {
        vErrors.push(err93);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err94 = { instancePath, schemaPath: "#/anyOf/5/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err94];
      } else {
        vErrors.push(err94);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err95 = { instancePath, schemaPath: "#/anyOf/5/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err95];
      } else {
        vErrors.push(err95);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data41 = data.op;
      if (typeof data41 !== "string") {
        const err96 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/5/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err96];
        } else {
          vErrors.push(err96);
        }
        errors++;
      }
      if ("project.list_variants" !== data41) {
        const err97 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/5/properties/op/const", keyword: "const", params: { allowedValue: "project.list_variants" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err97];
        } else {
          vErrors.push(err97);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err98 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/5/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err98];
        } else {
          vErrors.push(err98);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data43 = data.status;
      if (typeof data43 !== "string") {
        const err99 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/5/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err99];
        } else {
          vErrors.push(err99);
        }
        errors++;
      }
      if ("ok" !== data43) {
        const err100 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/5/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err100];
        } else {
          vErrors.push(err100);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err101 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/5/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err101];
        } else {
          vErrors.push(err101);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      if (!validate21(data.outputs, { instancePath: instancePath + "/outputs", parentData: data, parentDataProperty: "outputs", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
        errors = vErrors.length;
      }
    }
    for (const key10 in data) {
      if (key10 !== "op" && key10 !== "id" && key10 !== "status" && key10 !== "message" && key10 !== "outputs") {
        const err102 = { instancePath: instancePath + "/" + key10.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/5/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err102];
        } else {
          vErrors.push(err102);
        }
        errors++;
      }
    }
  } else {
    const err103 = { instancePath, schemaPath: "#/anyOf/5/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err103];
    } else {
      vErrors.push(err103);
    }
    errors++;
  }
  var _valid0 = _errs115 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs129 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err104 = { instancePath, schemaPath: "#/anyOf/6/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err104];
      } else {
        vErrors.push(err104);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err105 = { instancePath, schemaPath: "#/anyOf/6/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err105];
      } else {
        vErrors.push(err105);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err106 = { instancePath, schemaPath: "#/anyOf/6/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err106];
      } else {
        vErrors.push(err106);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err107 = { instancePath, schemaPath: "#/anyOf/6/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err107];
      } else {
        vErrors.push(err107);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err108 = { instancePath, schemaPath: "#/anyOf/6/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err108];
      } else {
        vErrors.push(err108);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data47 = data.op;
      if (typeof data47 !== "string") {
        const err109 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/6/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err109];
        } else {
          vErrors.push(err109);
        }
        errors++;
      }
      if ("project.delete_variant" !== data47) {
        const err110 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/6/properties/op/const", keyword: "const", params: { allowedValue: "project.delete_variant" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err110];
        } else {
          vErrors.push(err110);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err111 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/6/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err111];
        } else {
          vErrors.push(err111);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data49 = data.status;
      if (typeof data49 !== "string") {
        const err112 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/6/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err112];
        } else {
          vErrors.push(err112);
        }
        errors++;
      }
      if ("ok" !== data49) {
        const err113 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/6/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err113];
        } else {
          vErrors.push(err113);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err114 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/6/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err114];
        } else {
          vErrors.push(err114);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data51 = data.outputs;
      if (data51 && typeof data51 == "object" && !Array.isArray(data51)) {
        if (data51.project === void 0) {
          const err115 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/SectionProject/required", keyword: "required", params: { missingProperty: "project" }, message: "must have required property 'project'" };
          if (vErrors === null) {
            vErrors = [err115];
          } else {
            vErrors.push(err115);
          }
          errors++;
        }
        if (data51.name === void 0) {
          const err116 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/SectionProject/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
          if (vErrors === null) {
            vErrors = [err116];
          } else {
            vErrors.push(err116);
          }
          errors++;
        }
        if (data51.section === void 0) {
          const err117 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/SectionProject/required", keyword: "required", params: { missingProperty: "section" }, message: "must have required property 'section'" };
          if (vErrors === null) {
            vErrors = [err117];
          } else {
            vErrors.push(err117);
          }
          errors++;
        }
        if (data51.project !== void 0) {
          if (typeof data51.project !== "string") {
            const err118 = { instancePath: instancePath + "/outputs/project", schemaPath: "#/$defs/SectionProject/properties/project/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err118];
            } else {
              vErrors.push(err118);
            }
            errors++;
          }
        }
        if (data51.name !== void 0) {
          if (typeof data51.name !== "string") {
            const err119 = { instancePath: instancePath + "/outputs/name", schemaPath: "#/$defs/SectionProject/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err119];
            } else {
              vErrors.push(err119);
            }
            errors++;
          }
        }
        if (data51.section !== void 0) {
          if (typeof data51.section !== "string") {
            const err120 = { instancePath: instancePath + "/outputs/section", schemaPath: "#/$defs/SectionProject/properties/section/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err120];
            } else {
              vErrors.push(err120);
            }
            errors++;
          }
        }
        for (const key11 in data51) {
          if (key11 !== "project" && key11 !== "name" && key11 !== "section") {
            const err121 = { instancePath: instancePath + "/outputs/" + key11.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/SectionProject/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err121];
            } else {
              vErrors.push(err121);
            }
            errors++;
          }
        }
      } else {
        const err122 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/SectionProject/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err122];
        } else {
          vErrors.push(err122);
        }
        errors++;
      }
    }
    for (const key12 in data) {
      if (key12 !== "op" && key12 !== "id" && key12 !== "status" && key12 !== "message" && key12 !== "outputs") {
        const err123 = { instancePath: instancePath + "/" + key12.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/6/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err123];
        } else {
          vErrors.push(err123);
        }
        errors++;
      }
    }
  } else {
    const err124 = { instancePath, schemaPath: "#/anyOf/6/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err124];
    } else {
      vErrors.push(err124);
    }
    errors++;
  }
  var _valid0 = _errs129 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs154 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err125 = { instancePath, schemaPath: "#/anyOf/7/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err125];
      } else {
        vErrors.push(err125);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err126 = { instancePath, schemaPath: "#/anyOf/7/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err126];
      } else {
        vErrors.push(err126);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err127 = { instancePath, schemaPath: "#/anyOf/7/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err127];
      } else {
        vErrors.push(err127);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err128 = { instancePath, schemaPath: "#/anyOf/7/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err128];
      } else {
        vErrors.push(err128);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err129 = { instancePath, schemaPath: "#/anyOf/7/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err129];
      } else {
        vErrors.push(err129);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data57 = data.op;
      if (typeof data57 !== "string") {
        const err130 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/7/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err130];
        } else {
          vErrors.push(err130);
        }
        errors++;
      }
      if ("project.rename_variant" !== data57) {
        const err131 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/7/properties/op/const", keyword: "const", params: { allowedValue: "project.rename_variant" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err131];
        } else {
          vErrors.push(err131);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err132 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/7/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err132];
        } else {
          vErrors.push(err132);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data59 = data.status;
      if (typeof data59 !== "string") {
        const err133 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/7/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err133];
        } else {
          vErrors.push(err133);
        }
        errors++;
      }
      if ("ok" !== data59) {
        const err134 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/7/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err134];
        } else {
          vErrors.push(err134);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err135 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/7/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err135];
        } else {
          vErrors.push(err135);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data61 = data.outputs;
      if (data61 && typeof data61 == "object" && !Array.isArray(data61)) {
        if (data61.project === void 0) {
          const err136 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/7/properties/outputs/required", keyword: "required", params: { missingProperty: "project" }, message: "must have required property 'project'" };
          if (vErrors === null) {
            vErrors = [err136];
          } else {
            vErrors.push(err136);
          }
          errors++;
        }
        if (data61.name === void 0) {
          const err137 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/7/properties/outputs/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
          if (vErrors === null) {
            vErrors = [err137];
          } else {
            vErrors.push(err137);
          }
          errors++;
        }
        if (data61.section === void 0) {
          const err138 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/7/properties/outputs/required", keyword: "required", params: { missingProperty: "section" }, message: "must have required property 'section'" };
          if (vErrors === null) {
            vErrors = [err138];
          } else {
            vErrors.push(err138);
          }
          errors++;
        }
        if (data61.new_name === void 0) {
          const err139 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/7/properties/outputs/required", keyword: "required", params: { missingProperty: "new_name" }, message: "must have required property 'new_name'" };
          if (vErrors === null) {
            vErrors = [err139];
          } else {
            vErrors.push(err139);
          }
          errors++;
        }
        if (data61.project !== void 0) {
          if (typeof data61.project !== "string") {
            const err140 = { instancePath: instancePath + "/outputs/project", schemaPath: "#/anyOf/7/properties/outputs/properties/project/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err140];
            } else {
              vErrors.push(err140);
            }
            errors++;
          }
        }
        if (data61.name !== void 0) {
          if (typeof data61.name !== "string") {
            const err141 = { instancePath: instancePath + "/outputs/name", schemaPath: "#/anyOf/7/properties/outputs/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err141];
            } else {
              vErrors.push(err141);
            }
            errors++;
          }
        }
        if (data61.section !== void 0) {
          if (typeof data61.section !== "string") {
            const err142 = { instancePath: instancePath + "/outputs/section", schemaPath: "#/anyOf/7/properties/outputs/properties/section/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err142];
            } else {
              vErrors.push(err142);
            }
            errors++;
          }
        }
        if (data61.new_name !== void 0) {
          if (typeof data61.new_name !== "string") {
            const err143 = { instancePath: instancePath + "/outputs/new_name", schemaPath: "#/anyOf/7/properties/outputs/properties/new_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err143];
            } else {
              vErrors.push(err143);
            }
            errors++;
          }
        }
        for (const key13 in data61) {
          if (key13 !== "project" && key13 !== "name" && key13 !== "section" && key13 !== "new_name") {
            const err144 = { instancePath: instancePath + "/outputs/" + key13.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/7/properties/outputs/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err144];
            } else {
              vErrors.push(err144);
            }
            errors++;
          }
        }
      } else {
        const err145 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/7/properties/outputs/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err145];
        } else {
          vErrors.push(err145);
        }
        errors++;
      }
    }
    for (const key14 in data) {
      if (key14 !== "op" && key14 !== "id" && key14 !== "status" && key14 !== "message" && key14 !== "outputs") {
        const err146 = { instancePath: instancePath + "/" + key14.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/7/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err146];
        } else {
          vErrors.push(err146);
        }
        errors++;
      }
    }
  } else {
    const err147 = { instancePath, schemaPath: "#/anyOf/7/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err147];
    } else {
      vErrors.push(err147);
    }
    errors++;
  }
  var _valid0 = _errs154 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs180 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err148 = { instancePath, schemaPath: "#/anyOf/8/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err148];
      } else {
        vErrors.push(err148);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err149 = { instancePath, schemaPath: "#/anyOf/8/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err149];
      } else {
        vErrors.push(err149);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err150 = { instancePath, schemaPath: "#/anyOf/8/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err150];
      } else {
        vErrors.push(err150);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err151 = { instancePath, schemaPath: "#/anyOf/8/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err151];
      } else {
        vErrors.push(err151);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err152 = { instancePath, schemaPath: "#/anyOf/8/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err152];
      } else {
        vErrors.push(err152);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data68 = data.op;
      if (typeof data68 !== "string") {
        const err153 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/8/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err153];
        } else {
          vErrors.push(err153);
        }
        errors++;
      }
      if ("project.clone_variant" !== data68) {
        const err154 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/8/properties/op/const", keyword: "const", params: { allowedValue: "project.clone_variant" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err154];
        } else {
          vErrors.push(err154);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err155 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/8/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err155];
        } else {
          vErrors.push(err155);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data70 = data.status;
      if (typeof data70 !== "string") {
        const err156 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/8/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err156];
        } else {
          vErrors.push(err156);
        }
        errors++;
      }
      if ("ok" !== data70) {
        const err157 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/8/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err157];
        } else {
          vErrors.push(err157);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err158 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/8/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err158];
        } else {
          vErrors.push(err158);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data72 = data.outputs;
      if (data72 && typeof data72 == "object" && !Array.isArray(data72)) {
        if (data72.project === void 0) {
          const err159 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/8/properties/outputs/required", keyword: "required", params: { missingProperty: "project" }, message: "must have required property 'project'" };
          if (vErrors === null) {
            vErrors = [err159];
          } else {
            vErrors.push(err159);
          }
          errors++;
        }
        if (data72.name === void 0) {
          const err160 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/8/properties/outputs/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
          if (vErrors === null) {
            vErrors = [err160];
          } else {
            vErrors.push(err160);
          }
          errors++;
        }
        if (data72.section === void 0) {
          const err161 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/8/properties/outputs/required", keyword: "required", params: { missingProperty: "section" }, message: "must have required property 'section'" };
          if (vErrors === null) {
            vErrors = [err161];
          } else {
            vErrors.push(err161);
          }
          errors++;
        }
        if (data72.source_name === void 0) {
          const err162 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/8/properties/outputs/required", keyword: "required", params: { missingProperty: "source_name" }, message: "must have required property 'source_name'" };
          if (vErrors === null) {
            vErrors = [err162];
          } else {
            vErrors.push(err162);
          }
          errors++;
        }
        if (data72.unique_id === void 0) {
          const err163 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/8/properties/outputs/required", keyword: "required", params: { missingProperty: "unique_id" }, message: "must have required property 'unique_id'" };
          if (vErrors === null) {
            vErrors = [err163];
          } else {
            vErrors.push(err163);
          }
          errors++;
        }
        if (data72.project !== void 0) {
          if (typeof data72.project !== "string") {
            const err164 = { instancePath: instancePath + "/outputs/project", schemaPath: "#/anyOf/8/properties/outputs/properties/project/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err164];
            } else {
              vErrors.push(err164);
            }
            errors++;
          }
        }
        if (data72.name !== void 0) {
          if (typeof data72.name !== "string") {
            const err165 = { instancePath: instancePath + "/outputs/name", schemaPath: "#/anyOf/8/properties/outputs/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err165];
            } else {
              vErrors.push(err165);
            }
            errors++;
          }
        }
        if (data72.section !== void 0) {
          if (typeof data72.section !== "string") {
            const err166 = { instancePath: instancePath + "/outputs/section", schemaPath: "#/anyOf/8/properties/outputs/properties/section/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err166];
            } else {
              vErrors.push(err166);
            }
            errors++;
          }
        }
        if (data72.source_name !== void 0) {
          if (typeof data72.source_name !== "string") {
            const err167 = { instancePath: instancePath + "/outputs/source_name", schemaPath: "#/anyOf/8/properties/outputs/properties/source_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err167];
            } else {
              vErrors.push(err167);
            }
            errors++;
          }
        }
        if (data72.unique_id !== void 0) {
          if (typeof data72.unique_id !== "string") {
            const err168 = { instancePath: instancePath + "/outputs/unique_id", schemaPath: "#/anyOf/8/properties/outputs/properties/unique_id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err168];
            } else {
              vErrors.push(err168);
            }
            errors++;
          }
        }
        for (const key15 in data72) {
          if (key15 !== "project" && key15 !== "name" && key15 !== "section" && key15 !== "source_name" && key15 !== "unique_id") {
            const err169 = { instancePath: instancePath + "/outputs/" + key15.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/8/properties/outputs/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err169];
            } else {
              vErrors.push(err169);
            }
            errors++;
          }
        }
      } else {
        const err170 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/8/properties/outputs/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err170];
        } else {
          vErrors.push(err170);
        }
        errors++;
      }
    }
    for (const key16 in data) {
      if (key16 !== "op" && key16 !== "id" && key16 !== "status" && key16 !== "message" && key16 !== "outputs") {
        const err171 = { instancePath: instancePath + "/" + key16.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/8/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err171];
        } else {
          vErrors.push(err171);
        }
        errors++;
      }
    }
  } else {
    const err172 = { instancePath, schemaPath: "#/anyOf/8/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err172];
    } else {
      vErrors.push(err172);
    }
    errors++;
  }
  var _valid0 = _errs180 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs208 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err173 = { instancePath, schemaPath: "#/anyOf/9/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err173];
      } else {
        vErrors.push(err173);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err174 = { instancePath, schemaPath: "#/anyOf/9/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err174];
      } else {
        vErrors.push(err174);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err175 = { instancePath, schemaPath: "#/anyOf/9/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err175];
      } else {
        vErrors.push(err175);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err176 = { instancePath, schemaPath: "#/anyOf/9/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err176];
      } else {
        vErrors.push(err176);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err177 = { instancePath, schemaPath: "#/anyOf/9/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err177];
      } else {
        vErrors.push(err177);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data80 = data.op;
      if (typeof data80 !== "string") {
        const err178 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/9/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err178];
        } else {
          vErrors.push(err178);
        }
        errors++;
      }
      if ("project.add_variant_dnp" !== data80) {
        const err179 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/9/properties/op/const", keyword: "const", params: { allowedValue: "project.add_variant_dnp" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err179];
        } else {
          vErrors.push(err179);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err180 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/9/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err180];
        } else {
          vErrors.push(err180);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data82 = data.status;
      if (typeof data82 !== "string") {
        const err181 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/9/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err181];
        } else {
          vErrors.push(err181);
        }
        errors++;
      }
      if ("ok" !== data82) {
        const err182 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/9/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err182];
        } else {
          vErrors.push(err182);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err183 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/9/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err183];
        } else {
          vErrors.push(err183);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data84 = data.outputs;
      if (data84 && typeof data84 == "object" && !Array.isArray(data84)) {
        if (data84.project === void 0) {
          const err184 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/DnpAdded/required", keyword: "required", params: { missingProperty: "project" }, message: "must have required property 'project'" };
          if (vErrors === null) {
            vErrors = [err184];
          } else {
            vErrors.push(err184);
          }
          errors++;
        }
        if (data84.variant === void 0) {
          const err185 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/DnpAdded/required", keyword: "required", params: { missingProperty: "variant" }, message: "must have required property 'variant'" };
          if (vErrors === null) {
            vErrors = [err185];
          } else {
            vErrors.push(err185);
          }
          errors++;
        }
        if (data84.designator === void 0) {
          const err186 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/DnpAdded/required", keyword: "required", params: { missingProperty: "designator" }, message: "must have required property 'designator'" };
          if (vErrors === null) {
            vErrors = [err186];
          } else {
            vErrors.push(err186);
          }
          errors++;
        }
        if (data84.unique_id === void 0) {
          const err187 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/DnpAdded/required", keyword: "required", params: { missingProperty: "unique_id" }, message: "must have required property 'unique_id'" };
          if (vErrors === null) {
            vErrors = [err187];
          } else {
            vErrors.push(err187);
          }
          errors++;
        }
        if (data84.variation === void 0) {
          const err188 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/DnpAdded/required", keyword: "required", params: { missingProperty: "variation" }, message: "must have required property 'variation'" };
          if (vErrors === null) {
            vErrors = [err188];
          } else {
            vErrors.push(err188);
          }
          errors++;
        }
        if (data84.project !== void 0) {
          if (typeof data84.project !== "string") {
            const err189 = { instancePath: instancePath + "/outputs/project", schemaPath: "#/$defs/DnpAdded/properties/project/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err189];
            } else {
              vErrors.push(err189);
            }
            errors++;
          }
        }
        if (data84.variant !== void 0) {
          if (typeof data84.variant !== "string") {
            const err190 = { instancePath: instancePath + "/outputs/variant", schemaPath: "#/$defs/DnpAdded/properties/variant/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err190];
            } else {
              vErrors.push(err190);
            }
            errors++;
          }
        }
        if (data84.designator !== void 0) {
          if (typeof data84.designator !== "string") {
            const err191 = { instancePath: instancePath + "/outputs/designator", schemaPath: "#/$defs/DnpAdded/properties/designator/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err191];
            } else {
              vErrors.push(err191);
            }
            errors++;
          }
        }
        if (data84.unique_id !== void 0) {
          if (typeof data84.unique_id !== "string") {
            const err192 = { instancePath: instancePath + "/outputs/unique_id", schemaPath: "#/$defs/DnpAdded/properties/unique_id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err192];
            } else {
              vErrors.push(err192);
            }
            errors++;
          }
        }
        if (data84.variation !== void 0) {
          if (typeof data84.variation !== "string") {
            const err193 = { instancePath: instancePath + "/outputs/variation", schemaPath: "#/$defs/DnpAdded/properties/variation/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err193];
            } else {
              vErrors.push(err193);
            }
            errors++;
          }
        }
        for (const key17 in data84) {
          if (key17 !== "project" && key17 !== "variant" && key17 !== "designator" && key17 !== "unique_id" && key17 !== "variation") {
            const err194 = { instancePath: instancePath + "/outputs/" + key17.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/DnpAdded/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err194];
            } else {
              vErrors.push(err194);
            }
            errors++;
          }
        }
      } else {
        const err195 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/DnpAdded/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err195];
        } else {
          vErrors.push(err195);
        }
        errors++;
      }
    }
    for (const key18 in data) {
      if (key18 !== "op" && key18 !== "id" && key18 !== "status" && key18 !== "message" && key18 !== "outputs") {
        const err196 = { instancePath: instancePath + "/" + key18.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/9/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err196];
        } else {
          vErrors.push(err196);
        }
        errors++;
      }
    }
  } else {
    const err197 = { instancePath, schemaPath: "#/anyOf/9/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err197];
    } else {
      vErrors.push(err197);
    }
    errors++;
  }
  var _valid0 = _errs208 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs237 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err198 = { instancePath, schemaPath: "#/anyOf/10/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err198];
      } else {
        vErrors.push(err198);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err199 = { instancePath, schemaPath: "#/anyOf/10/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err199];
      } else {
        vErrors.push(err199);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err200 = { instancePath, schemaPath: "#/anyOf/10/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err200];
      } else {
        vErrors.push(err200);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err201 = { instancePath, schemaPath: "#/anyOf/10/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err201];
      } else {
        vErrors.push(err201);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err202 = { instancePath, schemaPath: "#/anyOf/10/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err202];
      } else {
        vErrors.push(err202);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data92 = data.op;
      if (typeof data92 !== "string") {
        const err203 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/10/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err203];
        } else {
          vErrors.push(err203);
        }
        errors++;
      }
      if ("project.toggle_variant_dnp" !== data92) {
        const err204 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/10/properties/op/const", keyword: "const", params: { allowedValue: "project.toggle_variant_dnp" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err204];
        } else {
          vErrors.push(err204);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err205 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/10/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err205];
        } else {
          vErrors.push(err205);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data94 = data.status;
      if (typeof data94 !== "string") {
        const err206 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/10/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err206];
        } else {
          vErrors.push(err206);
        }
        errors++;
      }
      if ("ok" !== data94) {
        const err207 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/10/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err207];
        } else {
          vErrors.push(err207);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err208 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/10/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err208];
        } else {
          vErrors.push(err208);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data96 = data.outputs;
      const _errs248 = errors;
      let valid45 = false;
      const _errs249 = errors;
      if (data96 && typeof data96 == "object" && !Array.isArray(data96)) {
        if (data96.project === void 0) {
          const err209 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/ToggleAdded/required", keyword: "required", params: { missingProperty: "project" }, message: "must have required property 'project'" };
          if (vErrors === null) {
            vErrors = [err209];
          } else {
            vErrors.push(err209);
          }
          errors++;
        }
        if (data96.variant === void 0) {
          const err210 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/ToggleAdded/required", keyword: "required", params: { missingProperty: "variant" }, message: "must have required property 'variant'" };
          if (vErrors === null) {
            vErrors = [err210];
          } else {
            vErrors.push(err210);
          }
          errors++;
        }
        if (data96.designator === void 0) {
          const err211 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/ToggleAdded/required", keyword: "required", params: { missingProperty: "designator" }, message: "must have required property 'designator'" };
          if (vErrors === null) {
            vErrors = [err211];
          } else {
            vErrors.push(err211);
          }
          errors++;
        }
        if (data96.unique_id === void 0) {
          const err212 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/ToggleAdded/required", keyword: "required", params: { missingProperty: "unique_id" }, message: "must have required property 'unique_id'" };
          if (vErrors === null) {
            vErrors = [err212];
          } else {
            vErrors.push(err212);
          }
          errors++;
        }
        if (data96.variation === void 0) {
          const err213 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/ToggleAdded/required", keyword: "required", params: { missingProperty: "variation" }, message: "must have required property 'variation'" };
          if (vErrors === null) {
            vErrors = [err213];
          } else {
            vErrors.push(err213);
          }
          errors++;
        }
        if (data96.action === void 0) {
          const err214 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/ToggleAdded/required", keyword: "required", params: { missingProperty: "action" }, message: "must have required property 'action'" };
          if (vErrors === null) {
            vErrors = [err214];
          } else {
            vErrors.push(err214);
          }
          errors++;
        }
        if (data96.dnp === void 0) {
          const err215 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/ToggleAdded/required", keyword: "required", params: { missingProperty: "dnp" }, message: "must have required property 'dnp'" };
          if (vErrors === null) {
            vErrors = [err215];
          } else {
            vErrors.push(err215);
          }
          errors++;
        }
        if (data96.project !== void 0) {
          if (typeof data96.project !== "string") {
            const err216 = { instancePath: instancePath + "/outputs/project", schemaPath: "#/$defs/ToggleAdded/properties/project/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err216];
            } else {
              vErrors.push(err216);
            }
            errors++;
          }
        }
        if (data96.variant !== void 0) {
          if (typeof data96.variant !== "string") {
            const err217 = { instancePath: instancePath + "/outputs/variant", schemaPath: "#/$defs/ToggleAdded/properties/variant/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err217];
            } else {
              vErrors.push(err217);
            }
            errors++;
          }
        }
        if (data96.designator !== void 0) {
          if (typeof data96.designator !== "string") {
            const err218 = { instancePath: instancePath + "/outputs/designator", schemaPath: "#/$defs/ToggleAdded/properties/designator/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err218];
            } else {
              vErrors.push(err218);
            }
            errors++;
          }
        }
        if (data96.unique_id !== void 0) {
          if (typeof data96.unique_id !== "string") {
            const err219 = { instancePath: instancePath + "/outputs/unique_id", schemaPath: "#/$defs/ToggleAdded/properties/unique_id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err219];
            } else {
              vErrors.push(err219);
            }
            errors++;
          }
        }
        if (data96.variation !== void 0) {
          if (typeof data96.variation !== "string") {
            const err220 = { instancePath: instancePath + "/outputs/variation", schemaPath: "#/$defs/ToggleAdded/properties/variation/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err220];
            } else {
              vErrors.push(err220);
            }
            errors++;
          }
        }
        if (data96.action !== void 0) {
          let data102 = data96.action;
          if (typeof data102 !== "string") {
            const err221 = { instancePath: instancePath + "/outputs/action", schemaPath: "#/$defs/ToggleAdded/properties/action/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err221];
            } else {
              vErrors.push(err221);
            }
            errors++;
          }
          if ("added" !== data102) {
            const err222 = { instancePath: instancePath + "/outputs/action", schemaPath: "#/$defs/ToggleAdded/properties/action/const", keyword: "const", params: { allowedValue: "added" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err222];
            } else {
              vErrors.push(err222);
            }
            errors++;
          }
        }
        if (data96.dnp !== void 0) {
          let data103 = data96.dnp;
          if (typeof data103 !== "boolean") {
            const err223 = { instancePath: instancePath + "/outputs/dnp", schemaPath: "#/$defs/ToggleAdded/properties/dnp/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err223];
            } else {
              vErrors.push(err223);
            }
            errors++;
          }
          if (true !== data103) {
            const err224 = { instancePath: instancePath + "/outputs/dnp", schemaPath: "#/$defs/ToggleAdded/properties/dnp/const", keyword: "const", params: { allowedValue: true }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err224];
            } else {
              vErrors.push(err224);
            }
            errors++;
          }
        }
        for (const key19 in data96) {
          if (key19 !== "project" && key19 !== "variant" && key19 !== "designator" && key19 !== "unique_id" && key19 !== "variation" && key19 !== "action" && key19 !== "dnp") {
            const err225 = { instancePath: instancePath + "/outputs/" + key19.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/ToggleAdded/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err225];
            } else {
              vErrors.push(err225);
            }
            errors++;
          }
        }
      } else {
        const err226 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/ToggleAdded/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err226];
        } else {
          vErrors.push(err226);
        }
        errors++;
      }
      var _valid3 = _errs249 === errors;
      valid45 = valid45 || _valid3;
      if (_valid3) {
        var props1 = true;
      }
      const _errs269 = errors;
      if (data96 && typeof data96 == "object" && !Array.isArray(data96)) {
        if (data96.project === void 0) {
          const err227 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/ToggleRemoved/required", keyword: "required", params: { missingProperty: "project" }, message: "must have required property 'project'" };
          if (vErrors === null) {
            vErrors = [err227];
          } else {
            vErrors.push(err227);
          }
          errors++;
        }
        if (data96.variant === void 0) {
          const err228 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/ToggleRemoved/required", keyword: "required", params: { missingProperty: "variant" }, message: "must have required property 'variant'" };
          if (vErrors === null) {
            vErrors = [err228];
          } else {
            vErrors.push(err228);
          }
          errors++;
        }
        if (data96.designator === void 0) {
          const err229 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/ToggleRemoved/required", keyword: "required", params: { missingProperty: "designator" }, message: "must have required property 'designator'" };
          if (vErrors === null) {
            vErrors = [err229];
          } else {
            vErrors.push(err229);
          }
          errors++;
        }
        if (data96.action === void 0) {
          const err230 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/ToggleRemoved/required", keyword: "required", params: { missingProperty: "action" }, message: "must have required property 'action'" };
          if (vErrors === null) {
            vErrors = [err230];
          } else {
            vErrors.push(err230);
          }
          errors++;
        }
        if (data96.dnp === void 0) {
          const err231 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/ToggleRemoved/required", keyword: "required", params: { missingProperty: "dnp" }, message: "must have required property 'dnp'" };
          if (vErrors === null) {
            vErrors = [err231];
          } else {
            vErrors.push(err231);
          }
          errors++;
        }
        if (data96.project !== void 0) {
          if (typeof data96.project !== "string") {
            const err232 = { instancePath: instancePath + "/outputs/project", schemaPath: "#/$defs/ToggleRemoved/properties/project/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err232];
            } else {
              vErrors.push(err232);
            }
            errors++;
          }
        }
        if (data96.variant !== void 0) {
          if (typeof data96.variant !== "string") {
            const err233 = { instancePath: instancePath + "/outputs/variant", schemaPath: "#/$defs/ToggleRemoved/properties/variant/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err233];
            } else {
              vErrors.push(err233);
            }
            errors++;
          }
        }
        if (data96.designator !== void 0) {
          if (typeof data96.designator !== "string") {
            const err234 = { instancePath: instancePath + "/outputs/designator", schemaPath: "#/$defs/ToggleRemoved/properties/designator/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err234];
            } else {
              vErrors.push(err234);
            }
            errors++;
          }
        }
        if (data96.action !== void 0) {
          let data108 = data96.action;
          if (typeof data108 !== "string") {
            const err235 = { instancePath: instancePath + "/outputs/action", schemaPath: "#/$defs/ToggleRemoved/properties/action/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err235];
            } else {
              vErrors.push(err235);
            }
            errors++;
          }
          if ("removed" !== data108) {
            const err236 = { instancePath: instancePath + "/outputs/action", schemaPath: "#/$defs/ToggleRemoved/properties/action/const", keyword: "const", params: { allowedValue: "removed" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err236];
            } else {
              vErrors.push(err236);
            }
            errors++;
          }
        }
        if (data96.dnp !== void 0) {
          let data109 = data96.dnp;
          if (typeof data109 !== "boolean") {
            const err237 = { instancePath: instancePath + "/outputs/dnp", schemaPath: "#/$defs/ToggleRemoved/properties/dnp/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err237];
            } else {
              vErrors.push(err237);
            }
            errors++;
          }
          if (false !== data109) {
            const err238 = { instancePath: instancePath + "/outputs/dnp", schemaPath: "#/$defs/ToggleRemoved/properties/dnp/const", keyword: "const", params: { allowedValue: false }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err238];
            } else {
              vErrors.push(err238);
            }
            errors++;
          }
        }
        for (const key20 in data96) {
          if (key20 !== "project" && key20 !== "variant" && key20 !== "designator" && key20 !== "action" && key20 !== "dnp") {
            const err239 = { instancePath: instancePath + "/outputs/" + key20.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/ToggleRemoved/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err239];
            } else {
              vErrors.push(err239);
            }
            errors++;
          }
        }
      } else {
        const err240 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/ToggleRemoved/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err240];
        } else {
          vErrors.push(err240);
        }
        errors++;
      }
      var _valid3 = _errs269 === errors;
      valid45 = valid45 || _valid3;
      if (_valid3) {
        if (props1 !== true) {
          props1 = true;
        }
      }
      if (!valid45) {
        const err241 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/10/properties/outputs/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err241];
        } else {
          vErrors.push(err241);
        }
        errors++;
      } else {
        errors = _errs248;
        if (vErrors !== null) {
          if (_errs248) {
            vErrors.length = _errs248;
          } else {
            vErrors = null;
          }
        }
      }
    }
    for (const key21 in data) {
      if (key21 !== "op" && key21 !== "id" && key21 !== "status" && key21 !== "message" && key21 !== "outputs") {
        const err242 = { instancePath: instancePath + "/" + key21.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/10/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err242];
        } else {
          vErrors.push(err242);
        }
        errors++;
      }
    }
  } else {
    const err243 = { instancePath, schemaPath: "#/anyOf/10/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err243];
    } else {
      vErrors.push(err243);
    }
    errors++;
  }
  var _valid0 = _errs237 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs288 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err244 = { instancePath, schemaPath: "#/anyOf/11/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err244];
      } else {
        vErrors.push(err244);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err245 = { instancePath, schemaPath: "#/anyOf/11/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err245];
      } else {
        vErrors.push(err245);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err246 = { instancePath, schemaPath: "#/anyOf/11/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err246];
      } else {
        vErrors.push(err246);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err247 = { instancePath, schemaPath: "#/anyOf/11/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err247];
      } else {
        vErrors.push(err247);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err248 = { instancePath, schemaPath: "#/anyOf/11/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err248];
      } else {
        vErrors.push(err248);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data112 = data.op;
      if (typeof data112 !== "string") {
        const err249 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/11/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err249];
        } else {
          vErrors.push(err249);
        }
        errors++;
      }
      if ("schdoc.create" !== data112) {
        const err250 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/11/properties/op/const", keyword: "const", params: { allowedValue: "schdoc.create" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err250];
        } else {
          vErrors.push(err250);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err251 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/11/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err251];
        } else {
          vErrors.push(err251);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data114 = data.status;
      if (typeof data114 !== "string") {
        const err252 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/11/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err252];
        } else {
          vErrors.push(err252);
        }
        errors++;
      }
      if ("ok" !== data114) {
        const err253 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/11/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err253];
        } else {
          vErrors.push(err253);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err254 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/11/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err254];
        } else {
          vErrors.push(err254);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data116 = data.outputs;
      if (data116 && typeof data116 == "object" && !Array.isArray(data116)) {
        if (data116.schematic === void 0) {
          const err255 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/11/properties/outputs/required", keyword: "required", params: { missingProperty: "schematic" }, message: "must have required property 'schematic'" };
          if (vErrors === null) {
            vErrors = [err255];
          } else {
            vErrors.push(err255);
          }
          errors++;
        }
        if (data116.schematic !== void 0) {
          if (typeof data116.schematic !== "string") {
            const err256 = { instancePath: instancePath + "/outputs/schematic", schemaPath: "#/anyOf/11/properties/outputs/properties/schematic/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err256];
            } else {
              vErrors.push(err256);
            }
            errors++;
          }
        }
        for (const key22 in data116) {
          if (key22 !== "schematic") {
            const err257 = { instancePath: instancePath + "/outputs/" + key22.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/11/properties/outputs/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err257];
            } else {
              vErrors.push(err257);
            }
            errors++;
          }
        }
      } else {
        const err258 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/11/properties/outputs/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err258];
        } else {
          vErrors.push(err258);
        }
        errors++;
      }
    }
    for (const key23 in data) {
      if (key23 !== "op" && key23 !== "id" && key23 !== "status" && key23 !== "message" && key23 !== "outputs") {
        const err259 = { instancePath: instancePath + "/" + key23.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/11/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err259];
        } else {
          vErrors.push(err259);
        }
        errors++;
      }
    }
  } else {
    const err260 = { instancePath, schemaPath: "#/anyOf/11/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err260];
    } else {
      vErrors.push(err260);
    }
    errors++;
  }
  var _valid0 = _errs288 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs308 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err261 = { instancePath, schemaPath: "#/anyOf/12/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err261];
      } else {
        vErrors.push(err261);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err262 = { instancePath, schemaPath: "#/anyOf/12/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err262];
      } else {
        vErrors.push(err262);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err263 = { instancePath, schemaPath: "#/anyOf/12/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err263];
      } else {
        vErrors.push(err263);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err264 = { instancePath, schemaPath: "#/anyOf/12/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err264];
      } else {
        vErrors.push(err264);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err265 = { instancePath, schemaPath: "#/anyOf/12/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err265];
      } else {
        vErrors.push(err265);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data120 = data.op;
      if (typeof data120 !== "string") {
        const err266 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/12/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err266];
        } else {
          vErrors.push(err266);
        }
        errors++;
      }
      if ("pcbdoc.create" !== data120) {
        const err267 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/12/properties/op/const", keyword: "const", params: { allowedValue: "pcbdoc.create" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err267];
        } else {
          vErrors.push(err267);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err268 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/12/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err268];
        } else {
          vErrors.push(err268);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data122 = data.status;
      if (typeof data122 !== "string") {
        const err269 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/12/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err269];
        } else {
          vErrors.push(err269);
        }
        errors++;
      }
      if ("ok" !== data122) {
        const err270 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/12/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err270];
        } else {
          vErrors.push(err270);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err271 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/12/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err271];
        } else {
          vErrors.push(err271);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data124 = data.outputs;
      if (data124 && typeof data124 == "object" && !Array.isArray(data124)) {
        if (data124.board === void 0) {
          const err272 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/12/properties/outputs/required", keyword: "required", params: { missingProperty: "board" }, message: "must have required property 'board'" };
          if (vErrors === null) {
            vErrors = [err272];
          } else {
            vErrors.push(err272);
          }
          errors++;
        }
        if (data124.board !== void 0) {
          if (typeof data124.board !== "string") {
            const err273 = { instancePath: instancePath + "/outputs/board", schemaPath: "#/anyOf/12/properties/outputs/properties/board/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err273];
            } else {
              vErrors.push(err273);
            }
            errors++;
          }
        }
        for (const key24 in data124) {
          if (key24 !== "board") {
            const err274 = { instancePath: instancePath + "/outputs/" + key24.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/12/properties/outputs/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err274];
            } else {
              vErrors.push(err274);
            }
            errors++;
          }
        }
      } else {
        const err275 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/12/properties/outputs/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err275];
        } else {
          vErrors.push(err275);
        }
        errors++;
      }
    }
    for (const key25 in data) {
      if (key25 !== "op" && key25 !== "id" && key25 !== "status" && key25 !== "message" && key25 !== "outputs") {
        const err276 = { instancePath: instancePath + "/" + key25.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/12/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err276];
        } else {
          vErrors.push(err276);
        }
        errors++;
      }
    }
  } else {
    const err277 = { instancePath, schemaPath: "#/anyOf/12/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err277];
    } else {
      vErrors.push(err277);
    }
    errors++;
  }
  var _valid0 = _errs308 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs328 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err278 = { instancePath, schemaPath: "#/anyOf/13/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err278];
      } else {
        vErrors.push(err278);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err279 = { instancePath, schemaPath: "#/anyOf/13/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err279];
      } else {
        vErrors.push(err279);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err280 = { instancePath, schemaPath: "#/anyOf/13/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err280];
      } else {
        vErrors.push(err280);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err281 = { instancePath, schemaPath: "#/anyOf/13/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err281];
      } else {
        vErrors.push(err281);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err282 = { instancePath, schemaPath: "#/anyOf/13/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err282];
      } else {
        vErrors.push(err282);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data128 = data.op;
      const _errs331 = errors;
      let valid62 = false;
      const _errs332 = errors;
      if (typeof data128 !== "string") {
        const err283 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/13/properties/op/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err283];
        } else {
          vErrors.push(err283);
        }
        errors++;
      }
      if ("schlib.create" !== data128) {
        const err284 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/13/properties/op/anyOf/0/const", keyword: "const", params: { allowedValue: "schlib.create" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err284];
        } else {
          vErrors.push(err284);
        }
        errors++;
      }
      var _valid4 = _errs332 === errors;
      valid62 = valid62 || _valid4;
      const _errs334 = errors;
      if (typeof data128 !== "string") {
        const err285 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/13/properties/op/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err285];
        } else {
          vErrors.push(err285);
        }
        errors++;
      }
      if ("pcblib.create" !== data128) {
        const err286 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/13/properties/op/anyOf/1/const", keyword: "const", params: { allowedValue: "pcblib.create" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err286];
        } else {
          vErrors.push(err286);
        }
        errors++;
      }
      var _valid4 = _errs334 === errors;
      valid62 = valid62 || _valid4;
      if (!valid62) {
        const err287 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/13/properties/op/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err287];
        } else {
          vErrors.push(err287);
        }
        errors++;
      } else {
        errors = _errs331;
        if (vErrors !== null) {
          if (_errs331) {
            vErrors.length = _errs331;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err288 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/13/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err288];
        } else {
          vErrors.push(err288);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data130 = data.status;
      if (typeof data130 !== "string") {
        const err289 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/13/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err289];
        } else {
          vErrors.push(err289);
        }
        errors++;
      }
      if ("ok" !== data130) {
        const err290 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/13/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err290];
        } else {
          vErrors.push(err290);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err291 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/13/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err291];
        } else {
          vErrors.push(err291);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data132 = data.outputs;
      if (data132 && typeof data132 == "object" && !Array.isArray(data132)) {
        if (data132.library === void 0) {
          const err292 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/13/properties/outputs/required", keyword: "required", params: { missingProperty: "library" }, message: "must have required property 'library'" };
          if (vErrors === null) {
            vErrors = [err292];
          } else {
            vErrors.push(err292);
          }
          errors++;
        }
        if (data132.library !== void 0) {
          if (typeof data132.library !== "string") {
            const err293 = { instancePath: instancePath + "/outputs/library", schemaPath: "#/anyOf/13/properties/outputs/properties/library/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err293];
            } else {
              vErrors.push(err293);
            }
            errors++;
          }
        }
        for (const key26 in data132) {
          if (key26 !== "library") {
            const err294 = { instancePath: instancePath + "/outputs/" + key26.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/13/properties/outputs/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err294];
            } else {
              vErrors.push(err294);
            }
            errors++;
          }
        }
      } else {
        const err295 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/13/properties/outputs/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err295];
        } else {
          vErrors.push(err295);
        }
        errors++;
      }
    }
    for (const key27 in data) {
      if (key27 !== "op" && key27 !== "id" && key27 !== "status" && key27 !== "message" && key27 !== "outputs") {
        const err296 = { instancePath: instancePath + "/" + key27.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/13/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err296];
        } else {
          vErrors.push(err296);
        }
        errors++;
      }
    }
  } else {
    const err297 = { instancePath, schemaPath: "#/anyOf/13/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err297];
    } else {
      vErrors.push(err297);
    }
    errors++;
  }
  var _valid0 = _errs328 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs352 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err298 = { instancePath, schemaPath: "#/anyOf/14/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err298];
      } else {
        vErrors.push(err298);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err299 = { instancePath, schemaPath: "#/anyOf/14/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err299];
      } else {
        vErrors.push(err299);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err300 = { instancePath, schemaPath: "#/anyOf/14/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err300];
      } else {
        vErrors.push(err300);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err301 = { instancePath, schemaPath: "#/anyOf/14/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err301];
      } else {
        vErrors.push(err301);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err302 = { instancePath, schemaPath: "#/anyOf/14/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err302];
      } else {
        vErrors.push(err302);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data136 = data.op;
      if (typeof data136 !== "string") {
        const err303 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/14/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err303];
        } else {
          vErrors.push(err303);
        }
        errors++;
      }
      if ("schlib.add_symbol" !== data136) {
        const err304 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/14/properties/op/const", keyword: "const", params: { allowedValue: "schlib.add_symbol" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err304];
        } else {
          vErrors.push(err304);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err305 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/14/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err305];
        } else {
          vErrors.push(err305);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data138 = data.status;
      if (typeof data138 !== "string") {
        const err306 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/14/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err306];
        } else {
          vErrors.push(err306);
        }
        errors++;
      }
      if ("ok" !== data138) {
        const err307 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/14/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err307];
        } else {
          vErrors.push(err307);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err308 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/14/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err308];
        } else {
          vErrors.push(err308);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data140 = data.outputs;
      if (data140 && typeof data140 == "object" && !Array.isArray(data140)) {
        if (data140.library === void 0) {
          const err309 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/14/properties/outputs/required", keyword: "required", params: { missingProperty: "library" }, message: "must have required property 'library'" };
          if (vErrors === null) {
            vErrors = [err309];
          } else {
            vErrors.push(err309);
          }
          errors++;
        }
        if (data140.symbol === void 0) {
          const err310 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/14/properties/outputs/required", keyword: "required", params: { missingProperty: "symbol" }, message: "must have required property 'symbol'" };
          if (vErrors === null) {
            vErrors = [err310];
          } else {
            vErrors.push(err310);
          }
          errors++;
        }
        if (data140.library !== void 0) {
          if (typeof data140.library !== "string") {
            const err311 = { instancePath: instancePath + "/outputs/library", schemaPath: "#/anyOf/14/properties/outputs/properties/library/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err311];
            } else {
              vErrors.push(err311);
            }
            errors++;
          }
        }
        if (data140.symbol !== void 0) {
          if (typeof data140.symbol !== "string") {
            const err312 = { instancePath: instancePath + "/outputs/symbol", schemaPath: "#/anyOf/14/properties/outputs/properties/symbol/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err312];
            } else {
              vErrors.push(err312);
            }
            errors++;
          }
        }
        for (const key28 in data140) {
          if (key28 !== "library" && key28 !== "symbol") {
            const err313 = { instancePath: instancePath + "/outputs/" + key28.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/14/properties/outputs/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err313];
            } else {
              vErrors.push(err313);
            }
            errors++;
          }
        }
      } else {
        const err314 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/14/properties/outputs/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err314];
        } else {
          vErrors.push(err314);
        }
        errors++;
      }
    }
    for (const key29 in data) {
      if (key29 !== "op" && key29 !== "id" && key29 !== "status" && key29 !== "message" && key29 !== "outputs") {
        const err315 = { instancePath: instancePath + "/" + key29.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/14/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err315];
        } else {
          vErrors.push(err315);
        }
        errors++;
      }
    }
  } else {
    const err316 = { instancePath, schemaPath: "#/anyOf/14/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err316];
    } else {
      vErrors.push(err316);
    }
    errors++;
  }
  var _valid0 = _errs352 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs374 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err317 = { instancePath, schemaPath: "#/anyOf/15/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err317];
      } else {
        vErrors.push(err317);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err318 = { instancePath, schemaPath: "#/anyOf/15/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err318];
      } else {
        vErrors.push(err318);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err319 = { instancePath, schemaPath: "#/anyOf/15/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err319];
      } else {
        vErrors.push(err319);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err320 = { instancePath, schemaPath: "#/anyOf/15/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err320];
      } else {
        vErrors.push(err320);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err321 = { instancePath, schemaPath: "#/anyOf/15/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err321];
      } else {
        vErrors.push(err321);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data145 = data.op;
      if (typeof data145 !== "string") {
        const err322 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/15/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err322];
        } else {
          vErrors.push(err322);
        }
        errors++;
      }
      if ("file.copy" !== data145) {
        const err323 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/15/properties/op/const", keyword: "const", params: { allowedValue: "file.copy" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err323];
        } else {
          vErrors.push(err323);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err324 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/15/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err324];
        } else {
          vErrors.push(err324);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data147 = data.status;
      if (typeof data147 !== "string") {
        const err325 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/15/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err325];
        } else {
          vErrors.push(err325);
        }
        errors++;
      }
      if ("ok" !== data147) {
        const err326 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/15/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err326];
        } else {
          vErrors.push(err326);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err327 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/15/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err327];
        } else {
          vErrors.push(err327);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data149 = data.outputs;
      if (data149 && typeof data149 == "object" && !Array.isArray(data149)) {
        if (data149.source === void 0) {
          const err328 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/15/properties/outputs/required", keyword: "required", params: { missingProperty: "source" }, message: "must have required property 'source'" };
          if (vErrors === null) {
            vErrors = [err328];
          } else {
            vErrors.push(err328);
          }
          errors++;
        }
        if (data149.destination === void 0) {
          const err329 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/15/properties/outputs/required", keyword: "required", params: { missingProperty: "destination" }, message: "must have required property 'destination'" };
          if (vErrors === null) {
            vErrors = [err329];
          } else {
            vErrors.push(err329);
          }
          errors++;
        }
        if (data149.source !== void 0) {
          if (typeof data149.source !== "string") {
            const err330 = { instancePath: instancePath + "/outputs/source", schemaPath: "#/anyOf/15/properties/outputs/properties/source/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err330];
            } else {
              vErrors.push(err330);
            }
            errors++;
          }
        }
        if (data149.destination !== void 0) {
          if (typeof data149.destination !== "string") {
            const err331 = { instancePath: instancePath + "/outputs/destination", schemaPath: "#/anyOf/15/properties/outputs/properties/destination/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err331];
            } else {
              vErrors.push(err331);
            }
            errors++;
          }
        }
        for (const key30 in data149) {
          if (key30 !== "source" && key30 !== "destination") {
            const err332 = { instancePath: instancePath + "/outputs/" + key30.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/15/properties/outputs/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err332];
            } else {
              vErrors.push(err332);
            }
            errors++;
          }
        }
      } else {
        const err333 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/15/properties/outputs/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err333];
        } else {
          vErrors.push(err333);
        }
        errors++;
      }
    }
    for (const key31 in data) {
      if (key31 !== "op" && key31 !== "id" && key31 !== "status" && key31 !== "message" && key31 !== "outputs") {
        const err334 = { instancePath: instancePath + "/" + key31.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/15/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err334];
        } else {
          vErrors.push(err334);
        }
        errors++;
      }
    }
  } else {
    const err335 = { instancePath, schemaPath: "#/anyOf/15/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err335];
    } else {
      vErrors.push(err335);
    }
    errors++;
  }
  var _valid0 = _errs374 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs396 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err336 = { instancePath, schemaPath: "#/anyOf/16/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err336];
      } else {
        vErrors.push(err336);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err337 = { instancePath, schemaPath: "#/anyOf/16/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err337];
      } else {
        vErrors.push(err337);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err338 = { instancePath, schemaPath: "#/anyOf/16/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err338];
      } else {
        vErrors.push(err338);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err339 = { instancePath, schemaPath: "#/anyOf/16/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err339];
      } else {
        vErrors.push(err339);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err340 = { instancePath, schemaPath: "#/anyOf/16/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err340];
      } else {
        vErrors.push(err340);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data154 = data.op;
      if (typeof data154 !== "string") {
        const err341 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/16/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err341];
        } else {
          vErrors.push(err341);
        }
        errors++;
      }
      if ("schdoc.add_wire" !== data154) {
        const err342 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/16/properties/op/const", keyword: "const", params: { allowedValue: "schdoc.add_wire" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err342];
        } else {
          vErrors.push(err342);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err343 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/16/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err343];
        } else {
          vErrors.push(err343);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data156 = data.status;
      if (typeof data156 !== "string") {
        const err344 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/16/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err344];
        } else {
          vErrors.push(err344);
        }
        errors++;
      }
      if ("ok" !== data156) {
        const err345 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/16/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err345];
        } else {
          vErrors.push(err345);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err346 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/16/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err346];
        } else {
          vErrors.push(err346);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data158 = data.outputs;
      if (data158 && typeof data158 == "object" && !Array.isArray(data158)) {
        if (data158.file === void 0) {
          const err347 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/16/properties/outputs/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
          if (vErrors === null) {
            vErrors = [err347];
          } else {
            vErrors.push(err347);
          }
          errors++;
        }
        if (data158.points === void 0) {
          const err348 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/16/properties/outputs/required", keyword: "required", params: { missingProperty: "points" }, message: "must have required property 'points'" };
          if (vErrors === null) {
            vErrors = [err348];
          } else {
            vErrors.push(err348);
          }
          errors++;
        }
        if (data158.file !== void 0) {
          if (typeof data158.file !== "string") {
            const err349 = { instancePath: instancePath + "/outputs/file", schemaPath: "#/anyOf/16/properties/outputs/properties/file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err349];
            } else {
              vErrors.push(err349);
            }
            errors++;
          }
        }
        if (data158.points !== void 0) {
          let data160 = data158.points;
          if (!(typeof data160 == "number" && (!(data160 % 1) && !isNaN(data160)))) {
            const err350 = { instancePath: instancePath + "/outputs/points", schemaPath: "#/anyOf/16/properties/outputs/properties/points/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
            if (vErrors === null) {
              vErrors = [err350];
            } else {
              vErrors.push(err350);
            }
            errors++;
          }
        }
        for (const key32 in data158) {
          if (key32 !== "file" && key32 !== "points") {
            const err351 = { instancePath: instancePath + "/outputs/" + key32.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/16/properties/outputs/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err351];
            } else {
              vErrors.push(err351);
            }
            errors++;
          }
        }
      } else {
        const err352 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/16/properties/outputs/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err352];
        } else {
          vErrors.push(err352);
        }
        errors++;
      }
    }
    for (const key33 in data) {
      if (key33 !== "op" && key33 !== "id" && key33 !== "status" && key33 !== "message" && key33 !== "outputs") {
        const err353 = { instancePath: instancePath + "/" + key33.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/16/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err353];
        } else {
          vErrors.push(err353);
        }
        errors++;
      }
    }
  } else {
    const err354 = { instancePath, schemaPath: "#/anyOf/16/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err354];
    } else {
      vErrors.push(err354);
    }
    errors++;
  }
  var _valid0 = _errs396 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs418 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err355 = { instancePath, schemaPath: "#/anyOf/17/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err355];
      } else {
        vErrors.push(err355);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err356 = { instancePath, schemaPath: "#/anyOf/17/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err356];
      } else {
        vErrors.push(err356);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err357 = { instancePath, schemaPath: "#/anyOf/17/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err357];
      } else {
        vErrors.push(err357);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err358 = { instancePath, schemaPath: "#/anyOf/17/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err358];
      } else {
        vErrors.push(err358);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err359 = { instancePath, schemaPath: "#/anyOf/17/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err359];
      } else {
        vErrors.push(err359);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data163 = data.op;
      const _errs421 = errors;
      let valid79 = false;
      const _errs422 = errors;
      if (typeof data163 !== "string") {
        const err360 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/17/properties/op/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err360];
        } else {
          vErrors.push(err360);
        }
        errors++;
      }
      if ("schdoc.add_net_label" !== data163) {
        const err361 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/17/properties/op/anyOf/0/const", keyword: "const", params: { allowedValue: "schdoc.add_net_label" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err361];
        } else {
          vErrors.push(err361);
        }
        errors++;
      }
      var _valid5 = _errs422 === errors;
      valid79 = valid79 || _valid5;
      const _errs424 = errors;
      if (typeof data163 !== "string") {
        const err362 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/17/properties/op/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err362];
        } else {
          vErrors.push(err362);
        }
        errors++;
      }
      if ("schdoc.add_power_port" !== data163) {
        const err363 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/17/properties/op/anyOf/1/const", keyword: "const", params: { allowedValue: "schdoc.add_power_port" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err363];
        } else {
          vErrors.push(err363);
        }
        errors++;
      }
      var _valid5 = _errs424 === errors;
      valid79 = valid79 || _valid5;
      if (!valid79) {
        const err364 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/17/properties/op/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err364];
        } else {
          vErrors.push(err364);
        }
        errors++;
      } else {
        errors = _errs421;
        if (vErrors !== null) {
          if (_errs421) {
            vErrors.length = _errs421;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err365 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/17/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err365];
        } else {
          vErrors.push(err365);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data165 = data.status;
      if (typeof data165 !== "string") {
        const err366 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/17/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err366];
        } else {
          vErrors.push(err366);
        }
        errors++;
      }
      if ("ok" !== data165) {
        const err367 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/17/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err367];
        } else {
          vErrors.push(err367);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err368 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/17/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err368];
        } else {
          vErrors.push(err368);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data167 = data.outputs;
      if (data167 && typeof data167 == "object" && !Array.isArray(data167)) {
        if (data167.file === void 0) {
          const err369 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/TextOutput/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
          if (vErrors === null) {
            vErrors = [err369];
          } else {
            vErrors.push(err369);
          }
          errors++;
        }
        if (data167.text === void 0) {
          const err370 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/TextOutput/required", keyword: "required", params: { missingProperty: "text" }, message: "must have required property 'text'" };
          if (vErrors === null) {
            vErrors = [err370];
          } else {
            vErrors.push(err370);
          }
          errors++;
        }
        if (data167.file !== void 0) {
          if (typeof data167.file !== "string") {
            const err371 = { instancePath: instancePath + "/outputs/file", schemaPath: "#/$defs/TextOutput/properties/file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err371];
            } else {
              vErrors.push(err371);
            }
            errors++;
          }
        }
        if (data167.text !== void 0) {
          if (typeof data167.text !== "string") {
            const err372 = { instancePath: instancePath + "/outputs/text", schemaPath: "#/$defs/TextOutput/properties/text/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err372];
            } else {
              vErrors.push(err372);
            }
            errors++;
          }
        }
        for (const key34 in data167) {
          if (key34 !== "file" && key34 !== "text") {
            const err373 = { instancePath: instancePath + "/outputs/" + key34.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/TextOutput/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err373];
            } else {
              vErrors.push(err373);
            }
            errors++;
          }
        }
      } else {
        const err374 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/TextOutput/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err374];
        } else {
          vErrors.push(err374);
        }
        errors++;
      }
    }
    for (const key35 in data) {
      if (key35 !== "op" && key35 !== "id" && key35 !== "status" && key35 !== "message" && key35 !== "outputs") {
        const err375 = { instancePath: instancePath + "/" + key35.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/17/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err375];
        } else {
          vErrors.push(err375);
        }
        errors++;
      }
    }
  } else {
    const err376 = { instancePath, schemaPath: "#/anyOf/17/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err376];
    } else {
      vErrors.push(err376);
    }
    errors++;
  }
  var _valid0 = _errs418 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs445 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err377 = { instancePath, schemaPath: "#/anyOf/18/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err377];
      } else {
        vErrors.push(err377);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err378 = { instancePath, schemaPath: "#/anyOf/18/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err378];
      } else {
        vErrors.push(err378);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err379 = { instancePath, schemaPath: "#/anyOf/18/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err379];
      } else {
        vErrors.push(err379);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err380 = { instancePath, schemaPath: "#/anyOf/18/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err380];
      } else {
        vErrors.push(err380);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err381 = { instancePath, schemaPath: "#/anyOf/18/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err381];
      } else {
        vErrors.push(err381);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data172 = data.op;
      if (typeof data172 !== "string") {
        const err382 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/18/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err382];
        } else {
          vErrors.push(err382);
        }
        errors++;
      }
      if ("pcbdoc.add_text" !== data172) {
        const err383 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/18/properties/op/const", keyword: "const", params: { allowedValue: "pcbdoc.add_text" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err383];
        } else {
          vErrors.push(err383);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err384 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/18/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err384];
        } else {
          vErrors.push(err384);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data174 = data.status;
      if (typeof data174 !== "string") {
        const err385 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/18/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err385];
        } else {
          vErrors.push(err385);
        }
        errors++;
      }
      if ("ok" !== data174) {
        const err386 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/18/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err386];
        } else {
          vErrors.push(err386);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err387 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/18/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err387];
        } else {
          vErrors.push(err387);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data176 = data.outputs;
      const _errs456 = errors;
      let valid85 = false;
      const _errs457 = errors;
      if (data176 && typeof data176 == "object" && !Array.isArray(data176)) {
        if (data176.file === void 0) {
          const err388 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/TextOutput/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
          if (vErrors === null) {
            vErrors = [err388];
          } else {
            vErrors.push(err388);
          }
          errors++;
        }
        if (data176.text === void 0) {
          const err389 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/TextOutput/required", keyword: "required", params: { missingProperty: "text" }, message: "must have required property 'text'" };
          if (vErrors === null) {
            vErrors = [err389];
          } else {
            vErrors.push(err389);
          }
          errors++;
        }
        if (data176.file !== void 0) {
          if (typeof data176.file !== "string") {
            const err390 = { instancePath: instancePath + "/outputs/file", schemaPath: "#/$defs/TextOutput/properties/file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err390];
            } else {
              vErrors.push(err390);
            }
            errors++;
          }
        }
        if (data176.text !== void 0) {
          if (typeof data176.text !== "string") {
            const err391 = { instancePath: instancePath + "/outputs/text", schemaPath: "#/$defs/TextOutput/properties/text/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err391];
            } else {
              vErrors.push(err391);
            }
            errors++;
          }
        }
        for (const key36 in data176) {
          if (key36 !== "file" && key36 !== "text") {
            const err392 = { instancePath: instancePath + "/outputs/" + key36.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/TextOutput/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err392];
            } else {
              vErrors.push(err392);
            }
            errors++;
          }
        }
      } else {
        const err393 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/TextOutput/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err393];
        } else {
          vErrors.push(err393);
        }
        errors++;
      }
      var _valid6 = _errs457 === errors;
      valid85 = valid85 || _valid6;
      if (_valid6) {
        var props2 = true;
      }
      const _errs467 = errors;
      if (data176 && typeof data176 == "object" && !Array.isArray(data176)) {
        if (data176.file === void 0) {
          const err394 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/TextDryRun/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
          if (vErrors === null) {
            vErrors = [err394];
          } else {
            vErrors.push(err394);
          }
          errors++;
        }
        if (data176.text === void 0) {
          const err395 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/TextDryRun/required", keyword: "required", params: { missingProperty: "text" }, message: "must have required property 'text'" };
          if (vErrors === null) {
            vErrors = [err395];
          } else {
            vErrors.push(err395);
          }
          errors++;
        }
        if (data176.font_kind === void 0) {
          const err396 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/TextDryRun/required", keyword: "required", params: { missingProperty: "font_kind" }, message: "must have required property 'font_kind'" };
          if (vErrors === null) {
            vErrors = [err396];
          } else {
            vErrors.push(err396);
          }
          errors++;
        }
        if (data176.text_justification === void 0) {
          const err397 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/TextDryRun/required", keyword: "required", params: { missingProperty: "text_justification" }, message: "must have required property 'text_justification'" };
          if (vErrors === null) {
            vErrors = [err397];
          } else {
            vErrors.push(err397);
          }
          errors++;
        }
        if (data176.file !== void 0) {
          if (typeof data176.file !== "string") {
            const err398 = { instancePath: instancePath + "/outputs/file", schemaPath: "#/$defs/TextDryRun/properties/file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err398];
            } else {
              vErrors.push(err398);
            }
            errors++;
          }
        }
        if (data176.text !== void 0) {
          if (typeof data176.text !== "string") {
            const err399 = { instancePath: instancePath + "/outputs/text", schemaPath: "#/$defs/TextDryRun/properties/text/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err399];
            } else {
              vErrors.push(err399);
            }
            errors++;
          }
        }
        if (data176.font_kind !== void 0) {
          if (typeof data176.font_kind !== "string") {
            const err400 = { instancePath: instancePath + "/outputs/font_kind", schemaPath: "#/$defs/TextDryRun/properties/font_kind/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err400];
            } else {
              vErrors.push(err400);
            }
            errors++;
          }
        }
        if (data176.text_justification !== void 0) {
          let data183 = data176.text_justification;
          const _errs477 = errors;
          let valid91 = false;
          const _errs478 = errors;
          if (typeof data183 !== "string") {
            const err401 = { instancePath: instancePath + "/outputs/text_justification", schemaPath: "#/$defs/TextDryRun/properties/text_justification/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err401];
            } else {
              vErrors.push(err401);
            }
            errors++;
          }
          var _valid7 = _errs478 === errors;
          valid91 = valid91 || _valid7;
          const _errs480 = errors;
          if (!(typeof data183 == "number" && (!(data183 % 1) && !isNaN(data183)))) {
            const err402 = { instancePath: instancePath + "/outputs/text_justification", schemaPath: "#/$defs/TextDryRun/properties/text_justification/anyOf/1/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
            if (vErrors === null) {
              vErrors = [err402];
            } else {
              vErrors.push(err402);
            }
            errors++;
          }
          var _valid7 = _errs480 === errors;
          valid91 = valid91 || _valid7;
          const _errs482 = errors;
          if (data183 !== null) {
            const err403 = { instancePath: instancePath + "/outputs/text_justification", schemaPath: "#/$defs/TextDryRun/properties/text_justification/anyOf/2/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err403];
            } else {
              vErrors.push(err403);
            }
            errors++;
          }
          var _valid7 = _errs482 === errors;
          valid91 = valid91 || _valid7;
          if (!valid91) {
            const err404 = { instancePath: instancePath + "/outputs/text_justification", schemaPath: "#/$defs/TextDryRun/properties/text_justification/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err404];
            } else {
              vErrors.push(err404);
            }
            errors++;
          } else {
            errors = _errs477;
            if (vErrors !== null) {
              if (_errs477) {
                vErrors.length = _errs477;
              } else {
                vErrors = null;
              }
            }
          }
        }
        for (const key37 in data176) {
          if (key37 !== "file" && key37 !== "text" && key37 !== "font_kind" && key37 !== "text_justification") {
            const err405 = { instancePath: instancePath + "/outputs/" + key37.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/TextDryRun/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err405];
            } else {
              vErrors.push(err405);
            }
            errors++;
          }
        }
      } else {
        const err406 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/TextDryRun/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err406];
        } else {
          vErrors.push(err406);
        }
        errors++;
      }
      var _valid6 = _errs467 === errors;
      valid85 = valid85 || _valid6;
      if (_valid6) {
        if (props2 !== true) {
          props2 = true;
        }
      }
      if (!valid85) {
        const err407 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/18/properties/outputs/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err407];
        } else {
          vErrors.push(err407);
        }
        errors++;
      } else {
        errors = _errs456;
        if (vErrors !== null) {
          if (_errs456) {
            vErrors.length = _errs456;
          } else {
            vErrors = null;
          }
        }
      }
    }
    for (const key38 in data) {
      if (key38 !== "op" && key38 !== "id" && key38 !== "status" && key38 !== "message" && key38 !== "outputs") {
        const err408 = { instancePath: instancePath + "/" + key38.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/18/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err408];
        } else {
          vErrors.push(err408);
        }
        errors++;
      }
    }
  } else {
    const err409 = { instancePath, schemaPath: "#/anyOf/18/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err409];
    } else {
      vErrors.push(err409);
    }
    errors++;
  }
  var _valid0 = _errs445 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs490 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err410 = { instancePath, schemaPath: "#/anyOf/19/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err410];
      } else {
        vErrors.push(err410);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err411 = { instancePath, schemaPath: "#/anyOf/19/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err411];
      } else {
        vErrors.push(err411);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err412 = { instancePath, schemaPath: "#/anyOf/19/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err412];
      } else {
        vErrors.push(err412);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err413 = { instancePath, schemaPath: "#/anyOf/19/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err413];
      } else {
        vErrors.push(err413);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err414 = { instancePath, schemaPath: "#/anyOf/19/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err414];
      } else {
        vErrors.push(err414);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data186 = data.op;
      if (typeof data186 !== "string") {
        const err415 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/19/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err415];
        } else {
          vErrors.push(err415);
        }
        errors++;
      }
      if ("schdoc.add_component" !== data186) {
        const err416 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/19/properties/op/const", keyword: "const", params: { allowedValue: "schdoc.add_component" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err416];
        } else {
          vErrors.push(err416);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err417 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/19/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err417];
        } else {
          vErrors.push(err417);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data188 = data.status;
      if (typeof data188 !== "string") {
        const err418 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/19/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err418];
        } else {
          vErrors.push(err418);
        }
        errors++;
      }
      if ("ok" !== data188) {
        const err419 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/19/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err419];
        } else {
          vErrors.push(err419);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err420 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/19/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err420];
        } else {
          vErrors.push(err420);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data190 = data.outputs;
      if (data190 && typeof data190 == "object" && !Array.isArray(data190)) {
        if (data190.file === void 0) {
          const err421 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/19/properties/outputs/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
          if (vErrors === null) {
            vErrors = [err421];
          } else {
            vErrors.push(err421);
          }
          errors++;
        }
        if (data190.library === void 0) {
          const err422 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/19/properties/outputs/required", keyword: "required", params: { missingProperty: "library" }, message: "must have required property 'library'" };
          if (vErrors === null) {
            vErrors = [err422];
          } else {
            vErrors.push(err422);
          }
          errors++;
        }
        if (data190.symbol === void 0) {
          const err423 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/19/properties/outputs/required", keyword: "required", params: { missingProperty: "symbol" }, message: "must have required property 'symbol'" };
          if (vErrors === null) {
            vErrors = [err423];
          } else {
            vErrors.push(err423);
          }
          errors++;
        }
        if (data190.designator === void 0) {
          const err424 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/19/properties/outputs/required", keyword: "required", params: { missingProperty: "designator" }, message: "must have required property 'designator'" };
          if (vErrors === null) {
            vErrors = [err424];
          } else {
            vErrors.push(err424);
          }
          errors++;
        }
        if (data190.file !== void 0) {
          if (typeof data190.file !== "string") {
            const err425 = { instancePath: instancePath + "/outputs/file", schemaPath: "#/anyOf/19/properties/outputs/properties/file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err425];
            } else {
              vErrors.push(err425);
            }
            errors++;
          }
        }
        if (data190.library !== void 0) {
          if (typeof data190.library !== "string") {
            const err426 = { instancePath: instancePath + "/outputs/library", schemaPath: "#/anyOf/19/properties/outputs/properties/library/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err426];
            } else {
              vErrors.push(err426);
            }
            errors++;
          }
        }
        if (data190.symbol !== void 0) {
          if (typeof data190.symbol !== "string") {
            const err427 = { instancePath: instancePath + "/outputs/symbol", schemaPath: "#/anyOf/19/properties/outputs/properties/symbol/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err427];
            } else {
              vErrors.push(err427);
            }
            errors++;
          }
        }
        if (data190.designator !== void 0) {
          if (typeof data190.designator !== "string") {
            const err428 = { instancePath: instancePath + "/outputs/designator", schemaPath: "#/anyOf/19/properties/outputs/properties/designator/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err428];
            } else {
              vErrors.push(err428);
            }
            errors++;
          }
        }
        for (const key39 in data190) {
          if (key39 !== "file" && key39 !== "library" && key39 !== "symbol" && key39 !== "designator") {
            const err429 = { instancePath: instancePath + "/outputs/" + key39.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/19/properties/outputs/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err429];
            } else {
              vErrors.push(err429);
            }
            errors++;
          }
        }
      } else {
        const err430 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/19/properties/outputs/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err430];
        } else {
          vErrors.push(err430);
        }
        errors++;
      }
    }
    for (const key40 in data) {
      if (key40 !== "op" && key40 !== "id" && key40 !== "status" && key40 !== "message" && key40 !== "outputs") {
        const err431 = { instancePath: instancePath + "/" + key40.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/19/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err431];
        } else {
          vErrors.push(err431);
        }
        errors++;
      }
    }
  } else {
    const err432 = { instancePath, schemaPath: "#/anyOf/19/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err432];
    } else {
      vErrors.push(err432);
    }
    errors++;
  }
  var _valid0 = _errs490 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs516 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err433 = { instancePath, schemaPath: "#/anyOf/20/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err433];
      } else {
        vErrors.push(err433);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err434 = { instancePath, schemaPath: "#/anyOf/20/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err434];
      } else {
        vErrors.push(err434);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err435 = { instancePath, schemaPath: "#/anyOf/20/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err435];
      } else {
        vErrors.push(err435);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err436 = { instancePath, schemaPath: "#/anyOf/20/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err436];
      } else {
        vErrors.push(err436);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err437 = { instancePath, schemaPath: "#/anyOf/20/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err437];
      } else {
        vErrors.push(err437);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data197 = data.op;
      if (typeof data197 !== "string") {
        const err438 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/20/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err438];
        } else {
          vErrors.push(err438);
        }
        errors++;
      }
      if ("pcbdoc.add_component" !== data197) {
        const err439 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/20/properties/op/const", keyword: "const", params: { allowedValue: "pcbdoc.add_component" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err439];
        } else {
          vErrors.push(err439);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err440 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/20/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err440];
        } else {
          vErrors.push(err440);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data199 = data.status;
      if (typeof data199 !== "string") {
        const err441 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/20/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err441];
        } else {
          vErrors.push(err441);
        }
        errors++;
      }
      if ("ok" !== data199) {
        const err442 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/20/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err442];
        } else {
          vErrors.push(err442);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err443 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/20/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err443];
        } else {
          vErrors.push(err443);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data201 = data.outputs;
      if (data201 && typeof data201 == "object" && !Array.isArray(data201)) {
        if (data201.file === void 0) {
          const err444 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/20/properties/outputs/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
          if (vErrors === null) {
            vErrors = [err444];
          } else {
            vErrors.push(err444);
          }
          errors++;
        }
        if (data201.library === void 0) {
          const err445 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/20/properties/outputs/required", keyword: "required", params: { missingProperty: "library" }, message: "must have required property 'library'" };
          if (vErrors === null) {
            vErrors = [err445];
          } else {
            vErrors.push(err445);
          }
          errors++;
        }
        if (data201.footprint === void 0) {
          const err446 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/20/properties/outputs/required", keyword: "required", params: { missingProperty: "footprint" }, message: "must have required property 'footprint'" };
          if (vErrors === null) {
            vErrors = [err446];
          } else {
            vErrors.push(err446);
          }
          errors++;
        }
        if (data201.designator === void 0) {
          const err447 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/20/properties/outputs/required", keyword: "required", params: { missingProperty: "designator" }, message: "must have required property 'designator'" };
          if (vErrors === null) {
            vErrors = [err447];
          } else {
            vErrors.push(err447);
          }
          errors++;
        }
        if (data201.file !== void 0) {
          if (typeof data201.file !== "string") {
            const err448 = { instancePath: instancePath + "/outputs/file", schemaPath: "#/anyOf/20/properties/outputs/properties/file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err448];
            } else {
              vErrors.push(err448);
            }
            errors++;
          }
        }
        if (data201.library !== void 0) {
          if (typeof data201.library !== "string") {
            const err449 = { instancePath: instancePath + "/outputs/library", schemaPath: "#/anyOf/20/properties/outputs/properties/library/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err449];
            } else {
              vErrors.push(err449);
            }
            errors++;
          }
        }
        if (data201.footprint !== void 0) {
          if (typeof data201.footprint !== "string") {
            const err450 = { instancePath: instancePath + "/outputs/footprint", schemaPath: "#/anyOf/20/properties/outputs/properties/footprint/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err450];
            } else {
              vErrors.push(err450);
            }
            errors++;
          }
        }
        if (data201.designator !== void 0) {
          if (typeof data201.designator !== "string") {
            const err451 = { instancePath: instancePath + "/outputs/designator", schemaPath: "#/anyOf/20/properties/outputs/properties/designator/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err451];
            } else {
              vErrors.push(err451);
            }
            errors++;
          }
        }
        for (const key41 in data201) {
          if (key41 !== "file" && key41 !== "library" && key41 !== "footprint" && key41 !== "designator") {
            const err452 = { instancePath: instancePath + "/outputs/" + key41.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/20/properties/outputs/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err452];
            } else {
              vErrors.push(err452);
            }
            errors++;
          }
        }
      } else {
        const err453 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/20/properties/outputs/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err453];
        } else {
          vErrors.push(err453);
        }
        errors++;
      }
    }
    for (const key42 in data) {
      if (key42 !== "op" && key42 !== "id" && key42 !== "status" && key42 !== "message" && key42 !== "outputs") {
        const err454 = { instancePath: instancePath + "/" + key42.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/20/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err454];
        } else {
          vErrors.push(err454);
        }
        errors++;
      }
    }
  } else {
    const err455 = { instancePath, schemaPath: "#/anyOf/20/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err455];
    } else {
      vErrors.push(err455);
    }
    errors++;
  }
  var _valid0 = _errs516 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs542 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err456 = { instancePath, schemaPath: "#/anyOf/21/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err456];
      } else {
        vErrors.push(err456);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err457 = { instancePath, schemaPath: "#/anyOf/21/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err457];
      } else {
        vErrors.push(err457);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err458 = { instancePath, schemaPath: "#/anyOf/21/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err458];
      } else {
        vErrors.push(err458);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err459 = { instancePath, schemaPath: "#/anyOf/21/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err459];
      } else {
        vErrors.push(err459);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err460 = { instancePath, schemaPath: "#/anyOf/21/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err460];
      } else {
        vErrors.push(err460);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data208 = data.op;
      if (typeof data208 !== "string") {
        const err461 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/21/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err461];
        } else {
          vErrors.push(err461);
        }
        errors++;
      }
      if ("pcblib.add_footprint" !== data208) {
        const err462 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/21/properties/op/const", keyword: "const", params: { allowedValue: "pcblib.add_footprint" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err462];
        } else {
          vErrors.push(err462);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err463 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/21/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err463];
        } else {
          vErrors.push(err463);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data210 = data.status;
      if (typeof data210 !== "string") {
        const err464 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/21/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err464];
        } else {
          vErrors.push(err464);
        }
        errors++;
      }
      if ("ok" !== data210) {
        const err465 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/21/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err465];
        } else {
          vErrors.push(err465);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err466 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/21/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err466];
        } else {
          vErrors.push(err466);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data212 = data.outputs;
      if (data212 && typeof data212 == "object" && !Array.isArray(data212)) {
        if (data212.file === void 0) {
          const err467 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/21/properties/outputs/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
          if (vErrors === null) {
            vErrors = [err467];
          } else {
            vErrors.push(err467);
          }
          errors++;
        }
        if (data212.footprint === void 0) {
          const err468 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/21/properties/outputs/required", keyword: "required", params: { missingProperty: "footprint" }, message: "must have required property 'footprint'" };
          if (vErrors === null) {
            vErrors = [err468];
          } else {
            vErrors.push(err468);
          }
          errors++;
        }
        if (data212.parameters === void 0) {
          const err469 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/21/properties/outputs/required", keyword: "required", params: { missingProperty: "parameters" }, message: "must have required property 'parameters'" };
          if (vErrors === null) {
            vErrors = [err469];
          } else {
            vErrors.push(err469);
          }
          errors++;
        }
        if (data212.primitive_parameters === void 0) {
          const err470 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/21/properties/outputs/required", keyword: "required", params: { missingProperty: "primitive_parameters" }, message: "must have required property 'primitive_parameters'" };
          if (vErrors === null) {
            vErrors = [err470];
          } else {
            vErrors.push(err470);
          }
          errors++;
        }
        if (data212.file !== void 0) {
          if (typeof data212.file !== "string") {
            const err471 = { instancePath: instancePath + "/outputs/file", schemaPath: "#/anyOf/21/properties/outputs/properties/file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err471];
            } else {
              vErrors.push(err471);
            }
            errors++;
          }
        }
        if (data212.footprint !== void 0) {
          if (typeof data212.footprint !== "string") {
            const err472 = { instancePath: instancePath + "/outputs/footprint", schemaPath: "#/anyOf/21/properties/outputs/properties/footprint/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err472];
            } else {
              vErrors.push(err472);
            }
            errors++;
          }
        }
        if (data212.parameters !== void 0) {
          let data215 = data212.parameters;
          if (!(typeof data215 == "number" && (!(data215 % 1) && !isNaN(data215)))) {
            const err473 = { instancePath: instancePath + "/outputs/parameters", schemaPath: "#/anyOf/21/properties/outputs/properties/parameters/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
            if (vErrors === null) {
              vErrors = [err473];
            } else {
              vErrors.push(err473);
            }
            errors++;
          }
        }
        if (data212.primitive_parameters !== void 0) {
          let data216 = data212.primitive_parameters;
          if (!(typeof data216 == "number" && (!(data216 % 1) && !isNaN(data216)))) {
            const err474 = { instancePath: instancePath + "/outputs/primitive_parameters", schemaPath: "#/anyOf/21/properties/outputs/properties/primitive_parameters/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
            if (vErrors === null) {
              vErrors = [err474];
            } else {
              vErrors.push(err474);
            }
            errors++;
          }
        }
        for (const key43 in data212) {
          if (key43 !== "file" && key43 !== "footprint" && key43 !== "parameters" && key43 !== "primitive_parameters") {
            const err475 = { instancePath: instancePath + "/outputs/" + key43.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/21/properties/outputs/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err475];
            } else {
              vErrors.push(err475);
            }
            errors++;
          }
        }
      } else {
        const err476 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/21/properties/outputs/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err476];
        } else {
          vErrors.push(err476);
        }
        errors++;
      }
    }
    for (const key44 in data) {
      if (key44 !== "op" && key44 !== "id" && key44 !== "status" && key44 !== "message" && key44 !== "outputs") {
        const err477 = { instancePath: instancePath + "/" + key44.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/21/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err477];
        } else {
          vErrors.push(err477);
        }
        errors++;
      }
    }
  } else {
    const err478 = { instancePath, schemaPath: "#/anyOf/21/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err478];
    } else {
      vErrors.push(err478);
    }
    errors++;
  }
  var _valid0 = _errs542 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs568 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err479 = { instancePath, schemaPath: "#/anyOf/22/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err479];
      } else {
        vErrors.push(err479);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err480 = { instancePath, schemaPath: "#/anyOf/22/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err480];
      } else {
        vErrors.push(err480);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err481 = { instancePath, schemaPath: "#/anyOf/22/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err481];
      } else {
        vErrors.push(err481);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err482 = { instancePath, schemaPath: "#/anyOf/22/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err482];
      } else {
        vErrors.push(err482);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err483 = { instancePath, schemaPath: "#/anyOf/22/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err483];
      } else {
        vErrors.push(err483);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data219 = data.op;
      if (typeof data219 !== "string") {
        const err484 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/22/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err484];
        } else {
          vErrors.push(err484);
        }
        errors++;
      }
      if ("pcbdoc.arrange_designators" !== data219) {
        const err485 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/22/properties/op/const", keyword: "const", params: { allowedValue: "pcbdoc.arrange_designators" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err485];
        } else {
          vErrors.push(err485);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err486 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/22/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err486];
        } else {
          vErrors.push(err486);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data221 = data.status;
      if (typeof data221 !== "string") {
        const err487 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/22/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err487];
        } else {
          vErrors.push(err487);
        }
        errors++;
      }
      if ("ok" !== data221) {
        const err488 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/22/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err488];
        } else {
          vErrors.push(err488);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err489 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/22/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err489];
        } else {
          vErrors.push(err489);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data223 = data.outputs;
      const _errs579 = errors;
      let valid107 = false;
      const _errs580 = errors;
      if (data223 && typeof data223 == "object" && !Array.isArray(data223)) {
        if (data223.file === void 0) {
          const err490 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/ArrangeDone/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
          if (vErrors === null) {
            vErrors = [err490];
          } else {
            vErrors.push(err490);
          }
          errors++;
        }
        if (data223.updated === void 0) {
          const err491 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/ArrangeDone/required", keyword: "required", params: { missingProperty: "updated" }, message: "must have required property 'updated'" };
          if (vErrors === null) {
            vErrors = [err491];
          } else {
            vErrors.push(err491);
          }
          errors++;
        }
        if (data223.file !== void 0) {
          if (typeof data223.file !== "string") {
            const err492 = { instancePath: instancePath + "/outputs/file", schemaPath: "#/$defs/ArrangeDone/properties/file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err492];
            } else {
              vErrors.push(err492);
            }
            errors++;
          }
        }
        if (data223.updated !== void 0) {
          let data225 = data223.updated;
          if (!(typeof data225 == "number" && (!(data225 % 1) && !isNaN(data225)))) {
            const err493 = { instancePath: instancePath + "/outputs/updated", schemaPath: "#/$defs/ArrangeDone/properties/updated/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
            if (vErrors === null) {
              vErrors = [err493];
            } else {
              vErrors.push(err493);
            }
            errors++;
          }
        }
        for (const key45 in data223) {
          if (key45 !== "file" && key45 !== "updated") {
            const err494 = { instancePath: instancePath + "/outputs/" + key45.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/ArrangeDone/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err494];
            } else {
              vErrors.push(err494);
            }
            errors++;
          }
        }
      } else {
        const err495 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/ArrangeDone/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err495];
        } else {
          vErrors.push(err495);
        }
        errors++;
      }
      var _valid8 = _errs580 === errors;
      valid107 = valid107 || _valid8;
      if (_valid8) {
        var props3 = true;
      }
      const _errs590 = errors;
      if (data223 && typeof data223 == "object" && !Array.isArray(data223)) {
        if (data223.file === void 0) {
          const err496 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/ArrangeDryRun/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
          if (vErrors === null) {
            vErrors = [err496];
          } else {
            vErrors.push(err496);
          }
          errors++;
        }
        if (data223.designators === void 0) {
          const err497 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/ArrangeDryRun/required", keyword: "required", params: { missingProperty: "designators" }, message: "must have required property 'designators'" };
          if (vErrors === null) {
            vErrors = [err497];
          } else {
            vErrors.push(err497);
          }
          errors++;
        }
        if (data223.placement === void 0) {
          const err498 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/ArrangeDryRun/required", keyword: "required", params: { missingProperty: "placement" }, message: "must have required property 'placement'" };
          if (vErrors === null) {
            vErrors = [err498];
          } else {
            vErrors.push(err498);
          }
          errors++;
        }
        if (data223.file !== void 0) {
          if (typeof data223.file !== "string") {
            const err499 = { instancePath: instancePath + "/outputs/file", schemaPath: "#/$defs/ArrangeDryRun/properties/file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err499];
            } else {
              vErrors.push(err499);
            }
            errors++;
          }
        }
        if (data223.designators !== void 0) {
          let data228 = data223.designators;
          const _errs596 = errors;
          let valid113 = false;
          const _errs597 = errors;
          if (!(typeof data228 == "number" && (!(data228 % 1) && !isNaN(data228)))) {
            const err500 = { instancePath: instancePath + "/outputs/designators", schemaPath: "#/$defs/ArrangeDryRun/properties/designators/anyOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
            if (vErrors === null) {
              vErrors = [err500];
            } else {
              vErrors.push(err500);
            }
            errors++;
          }
          var _valid9 = _errs597 === errors;
          valid113 = valid113 || _valid9;
          const _errs599 = errors;
          if (typeof data228 !== "string") {
            const err501 = { instancePath: instancePath + "/outputs/designators", schemaPath: "#/$defs/ArrangeDryRun/properties/designators/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err501];
            } else {
              vErrors.push(err501);
            }
            errors++;
          }
          if ("all" !== data228) {
            const err502 = { instancePath: instancePath + "/outputs/designators", schemaPath: "#/$defs/ArrangeDryRun/properties/designators/anyOf/1/const", keyword: "const", params: { allowedValue: "all" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err502];
            } else {
              vErrors.push(err502);
            }
            errors++;
          }
          var _valid9 = _errs599 === errors;
          valid113 = valid113 || _valid9;
          if (!valid113) {
            const err503 = { instancePath: instancePath + "/outputs/designators", schemaPath: "#/$defs/ArrangeDryRun/properties/designators/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err503];
            } else {
              vErrors.push(err503);
            }
            errors++;
          } else {
            errors = _errs596;
            if (vErrors !== null) {
              if (_errs596) {
                vErrors.length = _errs596;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data223.placement !== void 0) {
          if (typeof data223.placement !== "string") {
            const err504 = { instancePath: instancePath + "/outputs/placement", schemaPath: "#/$defs/ArrangeDryRun/properties/placement/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err504];
            } else {
              vErrors.push(err504);
            }
            errors++;
          }
        }
        for (const key46 in data223) {
          if (key46 !== "file" && key46 !== "designators" && key46 !== "placement") {
            const err505 = { instancePath: instancePath + "/outputs/" + key46.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/ArrangeDryRun/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err505];
            } else {
              vErrors.push(err505);
            }
            errors++;
          }
        }
      } else {
        const err506 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/ArrangeDryRun/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err506];
        } else {
          vErrors.push(err506);
        }
        errors++;
      }
      var _valid8 = _errs590 === errors;
      valid107 = valid107 || _valid8;
      if (_valid8) {
        if (props3 !== true) {
          props3 = true;
        }
      }
      if (!valid107) {
        const err507 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/22/properties/outputs/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err507];
        } else {
          vErrors.push(err507);
        }
        errors++;
      } else {
        errors = _errs579;
        if (vErrors !== null) {
          if (_errs579) {
            vErrors.length = _errs579;
          } else {
            vErrors = null;
          }
        }
      }
    }
    for (const key47 in data) {
      if (key47 !== "op" && key47 !== "id" && key47 !== "status" && key47 !== "message" && key47 !== "outputs") {
        const err508 = { instancePath: instancePath + "/" + key47.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/22/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err508];
        } else {
          vErrors.push(err508);
        }
        errors++;
      }
    }
  } else {
    const err509 = { instancePath, schemaPath: "#/anyOf/22/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err509];
    } else {
      vErrors.push(err509);
    }
    errors++;
  }
  var _valid0 = _errs568 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs609 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err510 = { instancePath, schemaPath: "#/anyOf/23/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err510];
      } else {
        vErrors.push(err510);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err511 = { instancePath, schemaPath: "#/anyOf/23/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err511];
      } else {
        vErrors.push(err511);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err512 = { instancePath, schemaPath: "#/anyOf/23/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err512];
      } else {
        vErrors.push(err512);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err513 = { instancePath, schemaPath: "#/anyOf/23/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err513];
      } else {
        vErrors.push(err513);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err514 = { instancePath, schemaPath: "#/anyOf/23/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err514];
      } else {
        vErrors.push(err514);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data232 = data.op;
      if (typeof data232 !== "string") {
        const err515 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/23/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err515];
        } else {
          vErrors.push(err515);
        }
        errors++;
      }
      if ("pcbdoc.add_track" !== data232) {
        const err516 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/23/properties/op/const", keyword: "const", params: { allowedValue: "pcbdoc.add_track" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err516];
        } else {
          vErrors.push(err516);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err517 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/23/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err517];
        } else {
          vErrors.push(err517);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data234 = data.status;
      if (typeof data234 !== "string") {
        const err518 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/23/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err518];
        } else {
          vErrors.push(err518);
        }
        errors++;
      }
      if ("ok" !== data234) {
        const err519 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/23/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err519];
        } else {
          vErrors.push(err519);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err520 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/23/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err520];
        } else {
          vErrors.push(err520);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data236 = data.outputs;
      if (data236 && typeof data236 == "object" && !Array.isArray(data236)) {
        if (data236.file === void 0) {
          const err521 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/23/properties/outputs/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
          if (vErrors === null) {
            vErrors = [err521];
          } else {
            vErrors.push(err521);
          }
          errors++;
        }
        if (data236.width_mils === void 0) {
          const err522 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/23/properties/outputs/required", keyword: "required", params: { missingProperty: "width_mils" }, message: "must have required property 'width_mils'" };
          if (vErrors === null) {
            vErrors = [err522];
          } else {
            vErrors.push(err522);
          }
          errors++;
        }
        if (data236.file !== void 0) {
          if (typeof data236.file !== "string") {
            const err523 = { instancePath: instancePath + "/outputs/file", schemaPath: "#/anyOf/23/properties/outputs/properties/file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err523];
            } else {
              vErrors.push(err523);
            }
            errors++;
          }
        }
        if (data236.width_mils !== void 0) {
          if (!(typeof data236.width_mils == "number")) {
            const err524 = { instancePath: instancePath + "/outputs/width_mils", schemaPath: "#/anyOf/23/properties/outputs/properties/width_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err524];
            } else {
              vErrors.push(err524);
            }
            errors++;
          }
        }
        for (const key48 in data236) {
          if (key48 !== "file" && key48 !== "width_mils") {
            const err525 = { instancePath: instancePath + "/outputs/" + key48.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/23/properties/outputs/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err525];
            } else {
              vErrors.push(err525);
            }
            errors++;
          }
        }
      } else {
        const err526 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/23/properties/outputs/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err526];
        } else {
          vErrors.push(err526);
        }
        errors++;
      }
    }
    for (const key49 in data) {
      if (key49 !== "op" && key49 !== "id" && key49 !== "status" && key49 !== "message" && key49 !== "outputs") {
        const err527 = { instancePath: instancePath + "/" + key49.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/23/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err527];
        } else {
          vErrors.push(err527);
        }
        errors++;
      }
    }
  } else {
    const err528 = { instancePath, schemaPath: "#/anyOf/23/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err528];
    } else {
      vErrors.push(err528);
    }
    errors++;
  }
  var _valid0 = _errs609 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs631 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err529 = { instancePath, schemaPath: "#/anyOf/24/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err529];
      } else {
        vErrors.push(err529);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err530 = { instancePath, schemaPath: "#/anyOf/24/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err530];
      } else {
        vErrors.push(err530);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err531 = { instancePath, schemaPath: "#/anyOf/24/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err531];
      } else {
        vErrors.push(err531);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err532 = { instancePath, schemaPath: "#/anyOf/24/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err532];
      } else {
        vErrors.push(err532);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err533 = { instancePath, schemaPath: "#/anyOf/24/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err533];
      } else {
        vErrors.push(err533);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data241 = data.op;
      if (typeof data241 !== "string") {
        const err534 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/24/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err534];
        } else {
          vErrors.push(err534);
        }
        errors++;
      }
      if ("pcbdoc.add_arc" !== data241) {
        const err535 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/24/properties/op/const", keyword: "const", params: { allowedValue: "pcbdoc.add_arc" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err535];
        } else {
          vErrors.push(err535);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err536 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/24/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err536];
        } else {
          vErrors.push(err536);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data243 = data.status;
      if (typeof data243 !== "string") {
        const err537 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/24/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err537];
        } else {
          vErrors.push(err537);
        }
        errors++;
      }
      if ("ok" !== data243) {
        const err538 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/24/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err538];
        } else {
          vErrors.push(err538);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err539 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/24/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err539];
        } else {
          vErrors.push(err539);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data245 = data.outputs;
      if (data245 && typeof data245 == "object" && !Array.isArray(data245)) {
        if (data245.file === void 0) {
          const err540 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/24/properties/outputs/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
          if (vErrors === null) {
            vErrors = [err540];
          } else {
            vErrors.push(err540);
          }
          errors++;
        }
        if (data245.radius_mils === void 0) {
          const err541 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/24/properties/outputs/required", keyword: "required", params: { missingProperty: "radius_mils" }, message: "must have required property 'radius_mils'" };
          if (vErrors === null) {
            vErrors = [err541];
          } else {
            vErrors.push(err541);
          }
          errors++;
        }
        if (data245.file !== void 0) {
          if (typeof data245.file !== "string") {
            const err542 = { instancePath: instancePath + "/outputs/file", schemaPath: "#/anyOf/24/properties/outputs/properties/file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err542];
            } else {
              vErrors.push(err542);
            }
            errors++;
          }
        }
        if (data245.radius_mils !== void 0) {
          if (!(typeof data245.radius_mils == "number")) {
            const err543 = { instancePath: instancePath + "/outputs/radius_mils", schemaPath: "#/anyOf/24/properties/outputs/properties/radius_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err543];
            } else {
              vErrors.push(err543);
            }
            errors++;
          }
        }
        for (const key50 in data245) {
          if (key50 !== "file" && key50 !== "radius_mils") {
            const err544 = { instancePath: instancePath + "/outputs/" + key50.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/24/properties/outputs/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err544];
            } else {
              vErrors.push(err544);
            }
            errors++;
          }
        }
      } else {
        const err545 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/24/properties/outputs/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err545];
        } else {
          vErrors.push(err545);
        }
        errors++;
      }
    }
    for (const key51 in data) {
      if (key51 !== "op" && key51 !== "id" && key51 !== "status" && key51 !== "message" && key51 !== "outputs") {
        const err546 = { instancePath: instancePath + "/" + key51.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/24/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err546];
        } else {
          vErrors.push(err546);
        }
        errors++;
      }
    }
  } else {
    const err547 = { instancePath, schemaPath: "#/anyOf/24/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err547];
    } else {
      vErrors.push(err547);
    }
    errors++;
  }
  var _valid0 = _errs631 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs653 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err548 = { instancePath, schemaPath: "#/anyOf/25/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err548];
      } else {
        vErrors.push(err548);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err549 = { instancePath, schemaPath: "#/anyOf/25/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err549];
      } else {
        vErrors.push(err549);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err550 = { instancePath, schemaPath: "#/anyOf/25/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err550];
      } else {
        vErrors.push(err550);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err551 = { instancePath, schemaPath: "#/anyOf/25/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err551];
      } else {
        vErrors.push(err551);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err552 = { instancePath, schemaPath: "#/anyOf/25/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err552];
      } else {
        vErrors.push(err552);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data250 = data.op;
      if (typeof data250 !== "string") {
        const err553 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/25/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err553];
        } else {
          vErrors.push(err553);
        }
        errors++;
      }
      if ("pcbdoc.add_pad" !== data250) {
        const err554 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/25/properties/op/const", keyword: "const", params: { allowedValue: "pcbdoc.add_pad" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err554];
        } else {
          vErrors.push(err554);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err555 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/25/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err555];
        } else {
          vErrors.push(err555);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data252 = data.status;
      if (typeof data252 !== "string") {
        const err556 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/25/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err556];
        } else {
          vErrors.push(err556);
        }
        errors++;
      }
      if ("ok" !== data252) {
        const err557 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/25/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err557];
        } else {
          vErrors.push(err557);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err558 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/25/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err558];
        } else {
          vErrors.push(err558);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data254 = data.outputs;
      if (data254 && typeof data254 == "object" && !Array.isArray(data254)) {
        if (data254.file === void 0) {
          const err559 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/25/properties/outputs/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
          if (vErrors === null) {
            vErrors = [err559];
          } else {
            vErrors.push(err559);
          }
          errors++;
        }
        if (data254.designator === void 0) {
          const err560 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/25/properties/outputs/required", keyword: "required", params: { missingProperty: "designator" }, message: "must have required property 'designator'" };
          if (vErrors === null) {
            vErrors = [err560];
          } else {
            vErrors.push(err560);
          }
          errors++;
        }
        if (data254.file !== void 0) {
          if (typeof data254.file !== "string") {
            const err561 = { instancePath: instancePath + "/outputs/file", schemaPath: "#/anyOf/25/properties/outputs/properties/file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err561];
            } else {
              vErrors.push(err561);
            }
            errors++;
          }
        }
        if (data254.designator !== void 0) {
          if (typeof data254.designator !== "string") {
            const err562 = { instancePath: instancePath + "/outputs/designator", schemaPath: "#/anyOf/25/properties/outputs/properties/designator/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err562];
            } else {
              vErrors.push(err562);
            }
            errors++;
          }
        }
        for (const key52 in data254) {
          if (key52 !== "file" && key52 !== "designator") {
            const err563 = { instancePath: instancePath + "/outputs/" + key52.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/25/properties/outputs/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err563];
            } else {
              vErrors.push(err563);
            }
            errors++;
          }
        }
      } else {
        const err564 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/25/properties/outputs/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err564];
        } else {
          vErrors.push(err564);
        }
        errors++;
      }
    }
    for (const key53 in data) {
      if (key53 !== "op" && key53 !== "id" && key53 !== "status" && key53 !== "message" && key53 !== "outputs") {
        const err565 = { instancePath: instancePath + "/" + key53.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/25/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err565];
        } else {
          vErrors.push(err565);
        }
        errors++;
      }
    }
  } else {
    const err566 = { instancePath, schemaPath: "#/anyOf/25/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err566];
    } else {
      vErrors.push(err566);
    }
    errors++;
  }
  var _valid0 = _errs653 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs675 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err567 = { instancePath, schemaPath: "#/anyOf/26/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err567];
      } else {
        vErrors.push(err567);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err568 = { instancePath, schemaPath: "#/anyOf/26/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err568];
      } else {
        vErrors.push(err568);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err569 = { instancePath, schemaPath: "#/anyOf/26/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err569];
      } else {
        vErrors.push(err569);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err570 = { instancePath, schemaPath: "#/anyOf/26/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err570];
      } else {
        vErrors.push(err570);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err571 = { instancePath, schemaPath: "#/anyOf/26/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err571];
      } else {
        vErrors.push(err571);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data259 = data.op;
      if (typeof data259 !== "string") {
        const err572 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/26/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err572];
        } else {
          vErrors.push(err572);
        }
        errors++;
      }
      if ("pcbdoc.add_via" !== data259) {
        const err573 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/26/properties/op/const", keyword: "const", params: { allowedValue: "pcbdoc.add_via" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err573];
        } else {
          vErrors.push(err573);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err574 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/26/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err574];
        } else {
          vErrors.push(err574);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data261 = data.status;
      if (typeof data261 !== "string") {
        const err575 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/26/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err575];
        } else {
          vErrors.push(err575);
        }
        errors++;
      }
      if ("ok" !== data261) {
        const err576 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/26/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err576];
        } else {
          vErrors.push(err576);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err577 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/26/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err577];
        } else {
          vErrors.push(err577);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data263 = data.outputs;
      if (data263 && typeof data263 == "object" && !Array.isArray(data263)) {
        if (data263.file === void 0) {
          const err578 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/26/properties/outputs/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
          if (vErrors === null) {
            vErrors = [err578];
          } else {
            vErrors.push(err578);
          }
          errors++;
        }
        if (data263.position_mils === void 0) {
          const err579 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/26/properties/outputs/required", keyword: "required", params: { missingProperty: "position_mils" }, message: "must have required property 'position_mils'" };
          if (vErrors === null) {
            vErrors = [err579];
          } else {
            vErrors.push(err579);
          }
          errors++;
        }
        if (data263.file !== void 0) {
          if (typeof data263.file !== "string") {
            const err580 = { instancePath: instancePath + "/outputs/file", schemaPath: "#/anyOf/26/properties/outputs/properties/file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err580];
            } else {
              vErrors.push(err580);
            }
            errors++;
          }
        }
        if (data263.position_mils !== void 0) {
          let data265 = data263.position_mils;
          if (Array.isArray(data265)) {
            if (data265.length > 2) {
              const err581 = { instancePath: instancePath + "/outputs/position_mils", schemaPath: "#/$defs/Pair/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
              if (vErrors === null) {
                vErrors = [err581];
              } else {
                vErrors.push(err581);
              }
              errors++;
            }
            if (data265.length < 2) {
              const err582 = { instancePath: instancePath + "/outputs/position_mils", schemaPath: "#/$defs/Pair/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
              if (vErrors === null) {
                vErrors = [err582];
              } else {
                vErrors.push(err582);
              }
              errors++;
            }
            const len0 = data265.length;
            for (let i0 = 0; i0 < len0; i0++) {
              if (!(typeof data265[i0] == "number")) {
                const err583 = { instancePath: instancePath + "/outputs/position_mils/" + i0, schemaPath: "#/$defs/Pair/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
                if (vErrors === null) {
                  vErrors = [err583];
                } else {
                  vErrors.push(err583);
                }
                errors++;
              }
            }
          } else {
            const err584 = { instancePath: instancePath + "/outputs/position_mils", schemaPath: "#/$defs/Pair/type", keyword: "type", params: { type: "array" }, message: "must be array" };
            if (vErrors === null) {
              vErrors = [err584];
            } else {
              vErrors.push(err584);
            }
            errors++;
          }
        }
        for (const key54 in data263) {
          if (key54 !== "file" && key54 !== "position_mils") {
            const err585 = { instancePath: instancePath + "/outputs/" + key54.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/26/properties/outputs/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err585];
            } else {
              vErrors.push(err585);
            }
            errors++;
          }
        }
      } else {
        const err586 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/26/properties/outputs/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err586];
        } else {
          vErrors.push(err586);
        }
        errors++;
      }
    }
    for (const key55 in data) {
      if (key55 !== "op" && key55 !== "id" && key55 !== "status" && key55 !== "message" && key55 !== "outputs") {
        const err587 = { instancePath: instancePath + "/" + key55.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/26/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err587];
        } else {
          vErrors.push(err587);
        }
        errors++;
      }
    }
  } else {
    const err588 = { instancePath, schemaPath: "#/anyOf/26/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err588];
    } else {
      vErrors.push(err588);
    }
    errors++;
  }
  var _valid0 = _errs675 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs700 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err589 = { instancePath, schemaPath: "#/anyOf/27/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err589];
      } else {
        vErrors.push(err589);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err590 = { instancePath, schemaPath: "#/anyOf/27/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err590];
      } else {
        vErrors.push(err590);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err591 = { instancePath, schemaPath: "#/anyOf/27/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err591];
      } else {
        vErrors.push(err591);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err592 = { instancePath, schemaPath: "#/anyOf/27/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err592];
      } else {
        vErrors.push(err592);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err593 = { instancePath, schemaPath: "#/anyOf/27/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err593];
      } else {
        vErrors.push(err593);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data269 = data.op;
      if (typeof data269 !== "string") {
        const err594 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/27/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err594];
        } else {
          vErrors.push(err594);
        }
        errors++;
      }
      if ("pcbdoc.add_fill" !== data269) {
        const err595 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/27/properties/op/const", keyword: "const", params: { allowedValue: "pcbdoc.add_fill" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err595];
        } else {
          vErrors.push(err595);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err596 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/27/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err596];
        } else {
          vErrors.push(err596);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data271 = data.status;
      if (typeof data271 !== "string") {
        const err597 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/27/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err597];
        } else {
          vErrors.push(err597);
        }
        errors++;
      }
      if ("ok" !== data271) {
        const err598 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/27/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err598];
        } else {
          vErrors.push(err598);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err599 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/27/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err599];
        } else {
          vErrors.push(err599);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data273 = data.outputs;
      if (data273 && typeof data273 == "object" && !Array.isArray(data273)) {
        if (data273.file === void 0) {
          const err600 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/27/properties/outputs/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
          if (vErrors === null) {
            vErrors = [err600];
          } else {
            vErrors.push(err600);
          }
          errors++;
        }
        if (data273.corner1_mils === void 0) {
          const err601 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/27/properties/outputs/required", keyword: "required", params: { missingProperty: "corner1_mils" }, message: "must have required property 'corner1_mils'" };
          if (vErrors === null) {
            vErrors = [err601];
          } else {
            vErrors.push(err601);
          }
          errors++;
        }
        if (data273.file !== void 0) {
          if (typeof data273.file !== "string") {
            const err602 = { instancePath: instancePath + "/outputs/file", schemaPath: "#/anyOf/27/properties/outputs/properties/file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err602];
            } else {
              vErrors.push(err602);
            }
            errors++;
          }
        }
        if (data273.corner1_mils !== void 0) {
          let data275 = data273.corner1_mils;
          if (Array.isArray(data275)) {
            if (data275.length > 2) {
              const err603 = { instancePath: instancePath + "/outputs/corner1_mils", schemaPath: "#/$defs/Pair/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
              if (vErrors === null) {
                vErrors = [err603];
              } else {
                vErrors.push(err603);
              }
              errors++;
            }
            if (data275.length < 2) {
              const err604 = { instancePath: instancePath + "/outputs/corner1_mils", schemaPath: "#/$defs/Pair/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
              if (vErrors === null) {
                vErrors = [err604];
              } else {
                vErrors.push(err604);
              }
              errors++;
            }
            const len1 = data275.length;
            for (let i1 = 0; i1 < len1; i1++) {
              if (!(typeof data275[i1] == "number")) {
                const err605 = { instancePath: instancePath + "/outputs/corner1_mils/" + i1, schemaPath: "#/$defs/Pair/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
                if (vErrors === null) {
                  vErrors = [err605];
                } else {
                  vErrors.push(err605);
                }
                errors++;
              }
            }
          } else {
            const err606 = { instancePath: instancePath + "/outputs/corner1_mils", schemaPath: "#/$defs/Pair/type", keyword: "type", params: { type: "array" }, message: "must be array" };
            if (vErrors === null) {
              vErrors = [err606];
            } else {
              vErrors.push(err606);
            }
            errors++;
          }
        }
        for (const key56 in data273) {
          if (key56 !== "file" && key56 !== "corner1_mils") {
            const err607 = { instancePath: instancePath + "/outputs/" + key56.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/27/properties/outputs/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err607];
            } else {
              vErrors.push(err607);
            }
            errors++;
          }
        }
      } else {
        const err608 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/27/properties/outputs/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err608];
        } else {
          vErrors.push(err608);
        }
        errors++;
      }
    }
    for (const key57 in data) {
      if (key57 !== "op" && key57 !== "id" && key57 !== "status" && key57 !== "message" && key57 !== "outputs") {
        const err609 = { instancePath: instancePath + "/" + key57.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/27/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err609];
        } else {
          vErrors.push(err609);
        }
        errors++;
      }
    }
  } else {
    const err610 = { instancePath, schemaPath: "#/anyOf/27/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err610];
    } else {
      vErrors.push(err610);
    }
    errors++;
  }
  var _valid0 = _errs700 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs725 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err611 = { instancePath, schemaPath: "#/anyOf/28/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err611];
      } else {
        vErrors.push(err611);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err612 = { instancePath, schemaPath: "#/anyOf/28/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err612];
      } else {
        vErrors.push(err612);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err613 = { instancePath, schemaPath: "#/anyOf/28/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err613];
      } else {
        vErrors.push(err613);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err614 = { instancePath, schemaPath: "#/anyOf/28/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err614];
      } else {
        vErrors.push(err614);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err615 = { instancePath, schemaPath: "#/anyOf/28/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err615];
      } else {
        vErrors.push(err615);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data279 = data.op;
      if (typeof data279 !== "string") {
        const err616 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/28/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err616];
        } else {
          vErrors.push(err616);
        }
        errors++;
      }
      if ("pcbdoc.add_region" !== data279) {
        const err617 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/28/properties/op/const", keyword: "const", params: { allowedValue: "pcbdoc.add_region" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err617];
        } else {
          vErrors.push(err617);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err618 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/28/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err618];
        } else {
          vErrors.push(err618);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data281 = data.status;
      if (typeof data281 !== "string") {
        const err619 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/28/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err619];
        } else {
          vErrors.push(err619);
        }
        errors++;
      }
      if ("ok" !== data281) {
        const err620 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/28/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err620];
        } else {
          vErrors.push(err620);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err621 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/28/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err621];
        } else {
          vErrors.push(err621);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data283 = data.outputs;
      if (data283 && typeof data283 == "object" && !Array.isArray(data283)) {
        if (data283.file === void 0) {
          const err622 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/28/properties/outputs/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
          if (vErrors === null) {
            vErrors = [err622];
          } else {
            vErrors.push(err622);
          }
          errors++;
        }
        if (data283.points === void 0) {
          const err623 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/28/properties/outputs/required", keyword: "required", params: { missingProperty: "points" }, message: "must have required property 'points'" };
          if (vErrors === null) {
            vErrors = [err623];
          } else {
            vErrors.push(err623);
          }
          errors++;
        }
        if (data283.is_board_cutout === void 0) {
          const err624 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/28/properties/outputs/required", keyword: "required", params: { missingProperty: "is_board_cutout" }, message: "must have required property 'is_board_cutout'" };
          if (vErrors === null) {
            vErrors = [err624];
          } else {
            vErrors.push(err624);
          }
          errors++;
        }
        if (data283.file !== void 0) {
          if (typeof data283.file !== "string") {
            const err625 = { instancePath: instancePath + "/outputs/file", schemaPath: "#/anyOf/28/properties/outputs/properties/file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err625];
            } else {
              vErrors.push(err625);
            }
            errors++;
          }
        }
        if (data283.points !== void 0) {
          let data285 = data283.points;
          if (!(typeof data285 == "number" && (!(data285 % 1) && !isNaN(data285)))) {
            const err626 = { instancePath: instancePath + "/outputs/points", schemaPath: "#/anyOf/28/properties/outputs/properties/points/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
            if (vErrors === null) {
              vErrors = [err626];
            } else {
              vErrors.push(err626);
            }
            errors++;
          }
        }
        if (data283.is_board_cutout !== void 0) {
          if (typeof data283.is_board_cutout !== "boolean") {
            const err627 = { instancePath: instancePath + "/outputs/is_board_cutout", schemaPath: "#/anyOf/28/properties/outputs/properties/is_board_cutout/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err627];
            } else {
              vErrors.push(err627);
            }
            errors++;
          }
        }
        for (const key58 in data283) {
          if (key58 !== "file" && key58 !== "points" && key58 !== "is_board_cutout") {
            const err628 = { instancePath: instancePath + "/outputs/" + key58.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/28/properties/outputs/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err628];
            } else {
              vErrors.push(err628);
            }
            errors++;
          }
        }
      } else {
        const err629 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/28/properties/outputs/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err629];
        } else {
          vErrors.push(err629);
        }
        errors++;
      }
    }
    for (const key59 in data) {
      if (key59 !== "op" && key59 !== "id" && key59 !== "status" && key59 !== "message" && key59 !== "outputs") {
        const err630 = { instancePath: instancePath + "/" + key59.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/28/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err630];
        } else {
          vErrors.push(err630);
        }
        errors++;
      }
    }
  } else {
    const err631 = { instancePath, schemaPath: "#/anyOf/28/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err631];
    } else {
      vErrors.push(err631);
    }
    errors++;
  }
  var _valid0 = _errs725 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs749 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err632 = { instancePath, schemaPath: "#/anyOf/29/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err632];
      } else {
        vErrors.push(err632);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err633 = { instancePath, schemaPath: "#/anyOf/29/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err633];
      } else {
        vErrors.push(err633);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err634 = { instancePath, schemaPath: "#/anyOf/29/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err634];
      } else {
        vErrors.push(err634);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err635 = { instancePath, schemaPath: "#/anyOf/29/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err635];
      } else {
        vErrors.push(err635);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err636 = { instancePath, schemaPath: "#/anyOf/29/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err636];
      } else {
        vErrors.push(err636);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data289 = data.op;
      if (typeof data289 !== "string") {
        const err637 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/29/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err637];
        } else {
          vErrors.push(err637);
        }
        errors++;
      }
      if ("pcbdoc.create_user_union" !== data289) {
        const err638 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/29/properties/op/const", keyword: "const", params: { allowedValue: "pcbdoc.create_user_union" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err638];
        } else {
          vErrors.push(err638);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err639 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/29/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err639];
        } else {
          vErrors.push(err639);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data291 = data.status;
      if (typeof data291 !== "string") {
        const err640 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/29/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err640];
        } else {
          vErrors.push(err640);
        }
        errors++;
      }
      if ("ok" !== data291) {
        const err641 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/29/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err641];
        } else {
          vErrors.push(err641);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err642 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/29/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err642];
        } else {
          vErrors.push(err642);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data293 = data.outputs;
      const _errs760 = errors;
      let valid147 = false;
      const _errs761 = errors;
      if (data293 && typeof data293 == "object" && !Array.isArray(data293)) {
        if (data293.file === void 0) {
          const err643 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/UnionDone/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
          if (vErrors === null) {
            vErrors = [err643];
          } else {
            vErrors.push(err643);
          }
          errors++;
        }
        if (data293.name === void 0) {
          const err644 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/UnionDone/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
          if (vErrors === null) {
            vErrors = [err644];
          } else {
            vErrors.push(err644);
          }
          errors++;
        }
        if (data293.union_index === void 0) {
          const err645 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/UnionDone/required", keyword: "required", params: { missingProperty: "union_index" }, message: "must have required property 'union_index'" };
          if (vErrors === null) {
            vErrors = [err645];
          } else {
            vErrors.push(err645);
          }
          errors++;
        }
        if (data293.member_count === void 0) {
          const err646 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/UnionDone/required", keyword: "required", params: { missingProperty: "member_count" }, message: "must have required property 'member_count'" };
          if (vErrors === null) {
            vErrors = [err646];
          } else {
            vErrors.push(err646);
          }
          errors++;
        }
        if (data293.file !== void 0) {
          if (typeof data293.file !== "string") {
            const err647 = { instancePath: instancePath + "/outputs/file", schemaPath: "#/$defs/UnionDone/properties/file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err647];
            } else {
              vErrors.push(err647);
            }
            errors++;
          }
        }
        if (data293.name !== void 0) {
          if (typeof data293.name !== "string") {
            const err648 = { instancePath: instancePath + "/outputs/name", schemaPath: "#/$defs/UnionDone/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err648];
            } else {
              vErrors.push(err648);
            }
            errors++;
          }
        }
        if (data293.union_index !== void 0) {
          let data296 = data293.union_index;
          if (!(typeof data296 == "number" && (!(data296 % 1) && !isNaN(data296)))) {
            const err649 = { instancePath: instancePath + "/outputs/union_index", schemaPath: "#/$defs/UnionDone/properties/union_index/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
            if (vErrors === null) {
              vErrors = [err649];
            } else {
              vErrors.push(err649);
            }
            errors++;
          }
        }
        if (data293.member_count !== void 0) {
          let data297 = data293.member_count;
          if (!(typeof data297 == "number" && (!(data297 % 1) && !isNaN(data297)))) {
            const err650 = { instancePath: instancePath + "/outputs/member_count", schemaPath: "#/$defs/UnionDone/properties/member_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
            if (vErrors === null) {
              vErrors = [err650];
            } else {
              vErrors.push(err650);
            }
            errors++;
          }
        }
        for (const key60 in data293) {
          if (key60 !== "file" && key60 !== "name" && key60 !== "union_index" && key60 !== "member_count") {
            const err651 = { instancePath: instancePath + "/outputs/" + key60.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/UnionDone/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err651];
            } else {
              vErrors.push(err651);
            }
            errors++;
          }
        }
      } else {
        const err652 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/UnionDone/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err652];
        } else {
          vErrors.push(err652);
        }
        errors++;
      }
      var _valid10 = _errs761 === errors;
      valid147 = valid147 || _valid10;
      if (_valid10) {
        var props4 = true;
      }
      const _errs775 = errors;
      if (data293 && typeof data293 == "object" && !Array.isArray(data293)) {
        if (data293.file === void 0) {
          const err653 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/UnionDryRun/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
          if (vErrors === null) {
            vErrors = [err653];
          } else {
            vErrors.push(err653);
          }
          errors++;
        }
        if (data293.name === void 0) {
          const err654 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/UnionDryRun/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
          if (vErrors === null) {
            vErrors = [err654];
          } else {
            vErrors.push(err654);
          }
          errors++;
        }
        if (data293.file !== void 0) {
          if (typeof data293.file !== "string") {
            const err655 = { instancePath: instancePath + "/outputs/file", schemaPath: "#/$defs/UnionDryRun/properties/file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err655];
            } else {
              vErrors.push(err655);
            }
            errors++;
          }
        }
        if (data293.name !== void 0) {
          if (typeof data293.name !== "string") {
            const err656 = { instancePath: instancePath + "/outputs/name", schemaPath: "#/$defs/UnionDryRun/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err656];
            } else {
              vErrors.push(err656);
            }
            errors++;
          }
        }
        for (const key61 in data293) {
          if (key61 !== "file" && key61 !== "name") {
            const err657 = { instancePath: instancePath + "/outputs/" + key61.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/UnionDryRun/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err657];
            } else {
              vErrors.push(err657);
            }
            errors++;
          }
        }
      } else {
        const err658 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/UnionDryRun/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err658];
        } else {
          vErrors.push(err658);
        }
        errors++;
      }
      var _valid10 = _errs775 === errors;
      valid147 = valid147 || _valid10;
      if (_valid10) {
        if (props4 !== true) {
          props4 = true;
        }
      }
      if (!valid147) {
        const err659 = { instancePath: instancePath + "/outputs", schemaPath: "#/anyOf/29/properties/outputs/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err659];
        } else {
          vErrors.push(err659);
        }
        errors++;
      } else {
        errors = _errs760;
        if (vErrors !== null) {
          if (_errs760) {
            vErrors.length = _errs760;
          } else {
            vErrors = null;
          }
        }
      }
    }
    for (const key62 in data) {
      if (key62 !== "op" && key62 !== "id" && key62 !== "status" && key62 !== "message" && key62 !== "outputs") {
        const err660 = { instancePath: instancePath + "/" + key62.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/29/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err660];
        } else {
          vErrors.push(err660);
        }
        errors++;
      }
    }
  } else {
    const err661 = { instancePath, schemaPath: "#/anyOf/29/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err661];
    } else {
      vErrors.push(err661);
    }
    errors++;
  }
  var _valid0 = _errs749 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs788 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err662 = { instancePath, schemaPath: "#/anyOf/30/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err662];
      } else {
        vErrors.push(err662);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err663 = { instancePath, schemaPath: "#/anyOf/30/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err663];
      } else {
        vErrors.push(err663);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err664 = { instancePath, schemaPath: "#/anyOf/30/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err664];
      } else {
        vErrors.push(err664);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err665 = { instancePath, schemaPath: "#/anyOf/30/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err665];
      } else {
        vErrors.push(err665);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err666 = { instancePath, schemaPath: "#/anyOf/30/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err666];
      } else {
        vErrors.push(err666);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data303 = data.op;
      if (typeof data303 !== "string") {
        const err667 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/30/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err667];
        } else {
          vErrors.push(err667);
        }
        errors++;
      }
      if ("pcbdoc.export_layer_step" !== data303) {
        const err668 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/30/properties/op/const", keyword: "const", params: { allowedValue: "pcbdoc.export_layer_step" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err668];
        } else {
          vErrors.push(err668);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err669 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/30/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err669];
        } else {
          vErrors.push(err669);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data305 = data.status;
      if (typeof data305 !== "string") {
        const err670 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/30/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err670];
        } else {
          vErrors.push(err670);
        }
        errors++;
      }
      if ("ok" !== data305) {
        const err671 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/30/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err671];
        } else {
          vErrors.push(err671);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err672 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/30/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err672];
        } else {
          vErrors.push(err672);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data307 = data.outputs;
      if (data307 && typeof data307 == "object" && !Array.isArray(data307)) {
        if (data307.file === void 0) {
          const err673 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/StepExport/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
          if (vErrors === null) {
            vErrors = [err673];
          } else {
            vErrors.push(err673);
          }
          errors++;
        }
        if (data307.step_file === void 0) {
          const err674 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/StepExport/required", keyword: "required", params: { missingProperty: "step_file" }, message: "must have required property 'step_file'" };
          if (vErrors === null) {
            vErrors = [err674];
          } else {
            vErrors.push(err674);
          }
          errors++;
        }
        if (data307.manifest_file === void 0) {
          const err675 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/StepExport/required", keyword: "required", params: { missingProperty: "manifest_file" }, message: "must have required property 'manifest_file'" };
          if (vErrors === null) {
            vErrors = [err675];
          } else {
            vErrors.push(err675);
          }
          errors++;
        }
        if (data307.highlight_count === void 0) {
          const err676 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/StepExport/required", keyword: "required", params: { missingProperty: "highlight_count" }, message: "must have required property 'highlight_count'" };
          if (vErrors === null) {
            vErrors = [err676];
          } else {
            vErrors.push(err676);
          }
          errors++;
        }
        if (data307.file !== void 0) {
          if (typeof data307.file !== "string") {
            const err677 = { instancePath: instancePath + "/outputs/file", schemaPath: "#/$defs/StepExport/properties/file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err677];
            } else {
              vErrors.push(err677);
            }
            errors++;
          }
        }
        if (data307.step_file !== void 0) {
          if (typeof data307.step_file !== "string") {
            const err678 = { instancePath: instancePath + "/outputs/step_file", schemaPath: "#/$defs/StepExport/properties/step_file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err678];
            } else {
              vErrors.push(err678);
            }
            errors++;
          }
        }
        if (data307.manifest_file !== void 0) {
          if (typeof data307.manifest_file !== "string") {
            const err679 = { instancePath: instancePath + "/outputs/manifest_file", schemaPath: "#/$defs/StepExport/properties/manifest_file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err679];
            } else {
              vErrors.push(err679);
            }
            errors++;
          }
        }
        if (data307.highlight_count !== void 0) {
          let data311 = data307.highlight_count;
          if (!(typeof data311 == "number" && (!(data311 % 1) && !isNaN(data311)))) {
            const err680 = { instancePath: instancePath + "/outputs/highlight_count", schemaPath: "#/$defs/StepExport/properties/highlight_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
            if (vErrors === null) {
              vErrors = [err680];
            } else {
              vErrors.push(err680);
            }
            errors++;
          }
        }
        if (data307.layer !== void 0) {
          if (typeof data307.layer !== "string") {
            const err681 = { instancePath: instancePath + "/outputs/layer", schemaPath: "#/$defs/StepExport/properties/layer/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err681];
            } else {
              vErrors.push(err681);
            }
            errors++;
          }
        }
        for (const key63 in data307) {
          if (key63 !== "file" && key63 !== "step_file" && key63 !== "manifest_file" && key63 !== "highlight_count" && key63 !== "layer") {
            const err682 = { instancePath: instancePath + "/outputs/" + key63.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/StepExport/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err682];
            } else {
              vErrors.push(err682);
            }
            errors++;
          }
        }
      } else {
        const err683 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/StepExport/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err683];
        } else {
          vErrors.push(err683);
        }
        errors++;
      }
    }
    for (const key64 in data) {
      if (key64 !== "op" && key64 !== "id" && key64 !== "status" && key64 !== "message" && key64 !== "outputs") {
        const err684 = { instancePath: instancePath + "/" + key64.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/30/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err684];
        } else {
          vErrors.push(err684);
        }
        errors++;
      }
    }
  } else {
    const err685 = { instancePath, schemaPath: "#/anyOf/30/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err685];
    } else {
      vErrors.push(err685);
    }
    errors++;
  }
  var _valid0 = _errs788 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs817 = errors;
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.op === void 0) {
      const err686 = { instancePath, schemaPath: "#/anyOf/31/required", keyword: "required", params: { missingProperty: "op" }, message: "must have required property 'op'" };
      if (vErrors === null) {
        vErrors = [err686];
      } else {
        vErrors.push(err686);
      }
      errors++;
    }
    if (data.id === void 0) {
      const err687 = { instancePath, schemaPath: "#/anyOf/31/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
      if (vErrors === null) {
        vErrors = [err687];
      } else {
        vErrors.push(err687);
      }
      errors++;
    }
    if (data.status === void 0) {
      const err688 = { instancePath, schemaPath: "#/anyOf/31/required", keyword: "required", params: { missingProperty: "status" }, message: "must have required property 'status'" };
      if (vErrors === null) {
        vErrors = [err688];
      } else {
        vErrors.push(err688);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err689 = { instancePath, schemaPath: "#/anyOf/31/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err689];
      } else {
        vErrors.push(err689);
      }
      errors++;
    }
    if (data.outputs === void 0) {
      const err690 = { instancePath, schemaPath: "#/anyOf/31/required", keyword: "required", params: { missingProperty: "outputs" }, message: "must have required property 'outputs'" };
      if (vErrors === null) {
        vErrors = [err690];
      } else {
        vErrors.push(err690);
      }
      errors++;
    }
    if (data.op !== void 0) {
      let data315 = data.op;
      if (typeof data315 !== "string") {
        const err691 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/31/properties/op/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err691];
        } else {
          vErrors.push(err691);
        }
        errors++;
      }
      if ("pcbdoc.add_embedded_3d_model" !== data315) {
        const err692 = { instancePath: instancePath + "/op", schemaPath: "#/anyOf/31/properties/op/const", keyword: "const", params: { allowedValue: "pcbdoc.add_embedded_3d_model" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err692];
        } else {
          vErrors.push(err692);
        }
        errors++;
      }
    }
    if (data.id !== void 0) {
      if (typeof data.id !== "string") {
        const err693 = { instancePath: instancePath + "/id", schemaPath: "#/anyOf/31/properties/id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err693];
        } else {
          vErrors.push(err693);
        }
        errors++;
      }
    }
    if (data.status !== void 0) {
      let data317 = data.status;
      if (typeof data317 !== "string") {
        const err694 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/31/properties/status/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err694];
        } else {
          vErrors.push(err694);
        }
        errors++;
      }
      if ("ok" !== data317) {
        const err695 = { instancePath: instancePath + "/status", schemaPath: "#/anyOf/31/properties/status/const", keyword: "const", params: { allowedValue: "ok" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err695];
        } else {
          vErrors.push(err695);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err696 = { instancePath: instancePath + "/message", schemaPath: "#/anyOf/31/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err696];
        } else {
          vErrors.push(err696);
        }
        errors++;
      }
    }
    if (data.outputs !== void 0) {
      let data319 = data.outputs;
      if (data319 && typeof data319 == "object" && !Array.isArray(data319)) {
        if (data319.file === void 0) {
          const err697 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/EmbeddedModel/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
          if (vErrors === null) {
            vErrors = [err697];
          } else {
            vErrors.push(err697);
          }
          errors++;
        }
        if (data319.model_file === void 0) {
          const err698 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/EmbeddedModel/required", keyword: "required", params: { missingProperty: "model_file" }, message: "must have required property 'model_file'" };
          if (vErrors === null) {
            vErrors = [err698];
          } else {
            vErrors.push(err698);
          }
          errors++;
        }
        if (data319.name === void 0) {
          const err699 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/EmbeddedModel/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
          if (vErrors === null) {
            vErrors = [err699];
          } else {
            vErrors.push(err699);
          }
          errors++;
        }
        if (data319.file !== void 0) {
          if (typeof data319.file !== "string") {
            const err700 = { instancePath: instancePath + "/outputs/file", schemaPath: "#/$defs/EmbeddedModel/properties/file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err700];
            } else {
              vErrors.push(err700);
            }
            errors++;
          }
        }
        if (data319.model_file !== void 0) {
          if (typeof data319.model_file !== "string") {
            const err701 = { instancePath: instancePath + "/outputs/model_file", schemaPath: "#/$defs/EmbeddedModel/properties/model_file/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err701];
            } else {
              vErrors.push(err701);
            }
            errors++;
          }
        }
        if (data319.name !== void 0) {
          if (typeof data319.name !== "string") {
            const err702 = { instancePath: instancePath + "/outputs/name", schemaPath: "#/$defs/EmbeddedModel/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err702];
            } else {
              vErrors.push(err702);
            }
            errors++;
          }
        }
        if (data319.z_mils !== void 0) {
          if (!(typeof data319.z_mils == "number")) {
            const err703 = { instancePath: instancePath + "/outputs/z_mils", schemaPath: "#/$defs/EmbeddedModel/properties/z_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err703];
            } else {
              vErrors.push(err703);
            }
            errors++;
          }
        }
        for (const key65 in data319) {
          if (key65 !== "file" && key65 !== "model_file" && key65 !== "name" && key65 !== "z_mils") {
            const err704 = { instancePath: instancePath + "/outputs/" + key65.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/EmbeddedModel/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err704];
            } else {
              vErrors.push(err704);
            }
            errors++;
          }
        }
      } else {
        const err705 = { instancePath: instancePath + "/outputs", schemaPath: "#/$defs/EmbeddedModel/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err705];
        } else {
          vErrors.push(err705);
        }
        errors++;
      }
    }
    for (const key66 in data) {
      if (key66 !== "op" && key66 !== "id" && key66 !== "status" && key66 !== "message" && key66 !== "outputs") {
        const err706 = { instancePath: instancePath + "/" + key66.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/anyOf/31/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err706];
        } else {
          vErrors.push(err706);
        }
        errors++;
      }
    }
  } else {
    const err707 = { instancePath, schemaPath: "#/anyOf/31/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err707];
    } else {
      vErrors.push(err707);
    }
    errors++;
  }
  var _valid0 = _errs817 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  if (!valid0) {
    const err708 = { instancePath, schemaPath: "#/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
    if (vErrors === null) {
      vErrors = [err708];
    } else {
      vErrors.push(err708);
    }
    errors++;
  } else {
    errors = _errs1;
    if (vErrors !== null) {
      if (_errs1) {
        vErrors.length = _errs1;
      } else {
        vErrors = null;
      }
    }
  }
  validate20.errors = vErrors;
  evaluated0.props = props0;
  return errors === 0;
}
validate20.evaluated = { "dynamicProps": true, "dynamicItems": false };
export {
  validate_default as default,
  validate
};
