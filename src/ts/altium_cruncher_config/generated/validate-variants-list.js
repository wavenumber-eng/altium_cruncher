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
        const err15 = { instancePath: instancePath + "/variation_count", schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      if (typeof data6 == "number") {
        if (data6 < 0 || isNaN(data6)) {
          const err16 = { instancePath: instancePath + "/variation_count", schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
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
        const err17 = { instancePath: instancePath + "/parameter_count", schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      if (typeof data7 == "number") {
        if (data7 < 0 || isNaN(data7)) {
          const err18 = { instancePath: instancePath + "/parameter_count", schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
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
        const err19 = { instancePath: instancePath + "/param_variation_count", schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
      if (typeof data8 == "number") {
        if (data8 < 0 || isNaN(data8)) {
          const err20 = { instancePath: instancePath + "/param_variation_count", schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
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
              const err21 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/VariantRow/required", keyword: "required", params: { missingProperty: "variant" }, message: "must have required property 'variant'" };
              if (vErrors === null) {
                vErrors = [err21];
              } else {
                vErrors.push(err21);
              }
              errors++;
            }
            if (data10.sheet === void 0) {
              const err22 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/VariantRow/required", keyword: "required", params: { missingProperty: "sheet" }, message: "must have required property 'sheet'" };
              if (vErrors === null) {
                vErrors = [err22];
              } else {
                vErrors.push(err22);
              }
              errors++;
            }
            if (data10.designator === void 0) {
              const err23 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/VariantRow/required", keyword: "required", params: { missingProperty: "designator" }, message: "must have required property 'designator'" };
              if (vErrors === null) {
                vErrors = [err23];
              } else {
                vErrors.push(err23);
              }
              errors++;
            }
            if (data10.operation === void 0) {
              const err24 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/VariantRow/required", keyword: "required", params: { missingProperty: "operation" }, message: "must have required property 'operation'" };
              if (vErrors === null) {
                vErrors = [err24];
              } else {
                vErrors.push(err24);
              }
              errors++;
            }
            if (data10.detail === void 0) {
              const err25 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/VariantRow/required", keyword: "required", params: { missingProperty: "detail" }, message: "must have required property 'detail'" };
              if (vErrors === null) {
                vErrors = [err25];
              } else {
                vErrors.push(err25);
              }
              errors++;
            }
            if (data10.component_value === void 0) {
              const err26 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/VariantRow/required", keyword: "required", params: { missingProperty: "component_value" }, message: "must have required property 'component_value'" };
              if (vErrors === null) {
                vErrors = [err26];
              } else {
                vErrors.push(err26);
              }
              errors++;
            }
            if (data10.parameter_name === void 0) {
              const err27 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/VariantRow/required", keyword: "required", params: { missingProperty: "parameter_name" }, message: "must have required property 'parameter_name'" };
              if (vErrors === null) {
                vErrors = [err27];
              } else {
                vErrors.push(err27);
              }
              errors++;
            }
            if (data10.value === void 0) {
              const err28 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/VariantRow/required", keyword: "required", params: { missingProperty: "value" }, message: "must have required property 'value'" };
              if (vErrors === null) {
                vErrors = [err28];
              } else {
                vErrors.push(err28);
              }
              errors++;
            }
            if (data10.unique_id === void 0) {
              const err29 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/VariantRow/required", keyword: "required", params: { missingProperty: "unique_id" }, message: "must have required property 'unique_id'" };
              if (vErrors === null) {
                vErrors = [err29];
              } else {
                vErrors.push(err29);
              }
              errors++;
            }
            if (data10.variant !== void 0) {
              if (typeof data10.variant !== "string") {
                const err30 = { instancePath: instancePath + "/rows/" + i1 + "/variant", schemaPath: "#/$defs/VariantRow/properties/variant/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
                const err31 = { instancePath: instancePath + "/rows/" + i1 + "/sheet", schemaPath: "#/$defs/VariantRow/properties/sheet/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
                const err32 = { instancePath: instancePath + "/rows/" + i1 + "/designator", schemaPath: "#/$defs/VariantRow/properties/designator/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
                const err33 = { instancePath: instancePath + "/rows/" + i1 + "/operation", schemaPath: "#/$defs/VariantRow/properties/operation/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
                const err34 = { instancePath: instancePath + "/rows/" + i1 + "/detail", schemaPath: "#/$defs/VariantRow/properties/detail/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
                const err35 = { instancePath: instancePath + "/rows/" + i1 + "/component_value", schemaPath: "#/$defs/VariantRow/properties/component_value/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
                const err36 = { instancePath: instancePath + "/rows/" + i1 + "/parameter_name", schemaPath: "#/$defs/VariantRow/properties/parameter_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
                const err37 = { instancePath: instancePath + "/rows/" + i1 + "/value", schemaPath: "#/$defs/VariantRow/properties/value/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
                const err38 = { instancePath: instancePath + "/rows/" + i1 + "/unique_id", schemaPath: "#/$defs/VariantRow/properties/unique_id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
                const err39 = { instancePath: instancePath + "/rows/" + i1 + "/alternate_part", schemaPath: "#/$defs/VariantRow/properties/alternate_part/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
                const err40 = { instancePath: instancePath + "/rows/" + i1 + "/alternate_part_resolved", schemaPath: "#/$defs/VariantRow/properties/alternate_part_resolved/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
                const err41 = { instancePath: instancePath + "/rows/" + i1 + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/VariantRow/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err41];
                } else {
                  vErrors.push(err41);
                }
                errors++;
              }
            }
          } else {
            const err42 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/VariantRow/type", keyword: "type", params: { type: "object" }, message: "must be object" };
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
      const _errs7 = errors;
      let valid1 = false;
      const _errs8 = errors;
      if (typeof data2 !== "string") {
        const err10 = { instancePath: instancePath + "/current_variant", schemaPath: "#/properties/current_variant/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
      var _valid0 = _errs8 === errors;
      valid1 = valid1 || _valid0;
      const _errs10 = errors;
      if (data2 !== null) {
        const err11 = { instancePath: instancePath + "/current_variant", schemaPath: "#/properties/current_variant/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid0 = _errs10 === errors;
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
        errors = _errs7;
        if (vErrors !== null) {
          if (_errs7) {
            vErrors.length = _errs7;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.variant_count !== void 0) {
      let data3 = data.variant_count;
      if (!(typeof data3 == "number" && (!(data3 % 1) && !isNaN(data3)))) {
        const err13 = { instancePath: instancePath + "/variant_count", schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      if (typeof data3 == "number") {
        if (data3 < 0 || isNaN(data3)) {
          const err14 = { instancePath: instancePath + "/variant_count", schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
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
          if (!validate21(data4[i0], { instancePath: instancePath + "/variants/" + i0, parentData: data4, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
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
              const err16 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/VariantRow/required", keyword: "required", params: { missingProperty: "variant" }, message: "must have required property 'variant'" };
              if (vErrors === null) {
                vErrors = [err16];
              } else {
                vErrors.push(err16);
              }
              errors++;
            }
            if (data7.sheet === void 0) {
              const err17 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/VariantRow/required", keyword: "required", params: { missingProperty: "sheet" }, message: "must have required property 'sheet'" };
              if (vErrors === null) {
                vErrors = [err17];
              } else {
                vErrors.push(err17);
              }
              errors++;
            }
            if (data7.designator === void 0) {
              const err18 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/VariantRow/required", keyword: "required", params: { missingProperty: "designator" }, message: "must have required property 'designator'" };
              if (vErrors === null) {
                vErrors = [err18];
              } else {
                vErrors.push(err18);
              }
              errors++;
            }
            if (data7.operation === void 0) {
              const err19 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/VariantRow/required", keyword: "required", params: { missingProperty: "operation" }, message: "must have required property 'operation'" };
              if (vErrors === null) {
                vErrors = [err19];
              } else {
                vErrors.push(err19);
              }
              errors++;
            }
            if (data7.detail === void 0) {
              const err20 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/VariantRow/required", keyword: "required", params: { missingProperty: "detail" }, message: "must have required property 'detail'" };
              if (vErrors === null) {
                vErrors = [err20];
              } else {
                vErrors.push(err20);
              }
              errors++;
            }
            if (data7.component_value === void 0) {
              const err21 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/VariantRow/required", keyword: "required", params: { missingProperty: "component_value" }, message: "must have required property 'component_value'" };
              if (vErrors === null) {
                vErrors = [err21];
              } else {
                vErrors.push(err21);
              }
              errors++;
            }
            if (data7.parameter_name === void 0) {
              const err22 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/VariantRow/required", keyword: "required", params: { missingProperty: "parameter_name" }, message: "must have required property 'parameter_name'" };
              if (vErrors === null) {
                vErrors = [err22];
              } else {
                vErrors.push(err22);
              }
              errors++;
            }
            if (data7.value === void 0) {
              const err23 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/VariantRow/required", keyword: "required", params: { missingProperty: "value" }, message: "must have required property 'value'" };
              if (vErrors === null) {
                vErrors = [err23];
              } else {
                vErrors.push(err23);
              }
              errors++;
            }
            if (data7.unique_id === void 0) {
              const err24 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/VariantRow/required", keyword: "required", params: { missingProperty: "unique_id" }, message: "must have required property 'unique_id'" };
              if (vErrors === null) {
                vErrors = [err24];
              } else {
                vErrors.push(err24);
              }
              errors++;
            }
            if (data7.variant !== void 0) {
              if (typeof data7.variant !== "string") {
                const err25 = { instancePath: instancePath + "/rows/" + i1 + "/variant", schemaPath: "#/$defs/VariantRow/properties/variant/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
                const err26 = { instancePath: instancePath + "/rows/" + i1 + "/sheet", schemaPath: "#/$defs/VariantRow/properties/sheet/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
                const err27 = { instancePath: instancePath + "/rows/" + i1 + "/designator", schemaPath: "#/$defs/VariantRow/properties/designator/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
                const err28 = { instancePath: instancePath + "/rows/" + i1 + "/operation", schemaPath: "#/$defs/VariantRow/properties/operation/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
                const err29 = { instancePath: instancePath + "/rows/" + i1 + "/detail", schemaPath: "#/$defs/VariantRow/properties/detail/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
                const err30 = { instancePath: instancePath + "/rows/" + i1 + "/component_value", schemaPath: "#/$defs/VariantRow/properties/component_value/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
                const err31 = { instancePath: instancePath + "/rows/" + i1 + "/parameter_name", schemaPath: "#/$defs/VariantRow/properties/parameter_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
                const err32 = { instancePath: instancePath + "/rows/" + i1 + "/value", schemaPath: "#/$defs/VariantRow/properties/value/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
                const err33 = { instancePath: instancePath + "/rows/" + i1 + "/unique_id", schemaPath: "#/$defs/VariantRow/properties/unique_id/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
                const err34 = { instancePath: instancePath + "/rows/" + i1 + "/alternate_part", schemaPath: "#/$defs/VariantRow/properties/alternate_part/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
                const err35 = { instancePath: instancePath + "/rows/" + i1 + "/alternate_part_resolved", schemaPath: "#/$defs/VariantRow/properties/alternate_part_resolved/type", keyword: "type", params: { type: "string" }, message: "must be string" };
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
                const err36 = { instancePath: instancePath + "/rows/" + i1 + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/VariantRow/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err36];
                } else {
                  vErrors.push(err36);
                }
                errors++;
              }
            }
          } else {
            const err37 = { instancePath: instancePath + "/rows/" + i1, schemaPath: "#/$defs/VariantRow/type", keyword: "type", params: { type: "object" }, message: "must be object" };
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
  validate20.errors = vErrors;
  return errors === 0;
}
validate20.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
export {
  validate_default as default,
  validate
};
