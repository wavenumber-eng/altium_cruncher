// Generated from src/tsp/altium_cruncher/outputs/toon-warning-report.tsp. Do not edit.
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
    if (data.unique_diagnostic_count === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "unique_diagnostic_count" }, message: "must have required property 'unique_diagnostic_count'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.occurrence_count === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "occurrence_count" }, message: "must have required property 'occurrence_count'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.groups === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "groups" }, message: "must have required property 'groups'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.unique_diagnostic_count !== void 0) {
      let data0 = data.unique_diagnostic_count;
      if (!(typeof data0 == "number" && (!(data0 % 1) && !isNaN(data0)))) {
        const err3 = { instancePath: instancePath + "/unique_diagnostic_count", schemaPath: "#/properties/unique_diagnostic_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      if (typeof data0 == "number") {
        if (data0 < 0 || isNaN(data0)) {
          const err4 = { instancePath: instancePath + "/unique_diagnostic_count", schemaPath: "#/properties/unique_diagnostic_count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err4];
          } else {
            vErrors.push(err4);
          }
          errors++;
        }
      }
    }
    if (data.occurrence_count !== void 0) {
      let data1 = data.occurrence_count;
      if (!(typeof data1 == "number" && (!(data1 % 1) && !isNaN(data1)))) {
        const err5 = { instancePath: instancePath + "/occurrence_count", schemaPath: "#/properties/occurrence_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      if (typeof data1 == "number") {
        if (data1 < 0 || isNaN(data1)) {
          const err6 = { instancePath: instancePath + "/occurrence_count", schemaPath: "#/properties/occurrence_count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err6];
          } else {
            vErrors.push(err6);
          }
          errors++;
        }
      }
    }
    if (data.groups !== void 0) {
      let data2 = data.groups;
      if (Array.isArray(data2)) {
        const len0 = data2.length;
        for (let i0 = 0; i0 < len0; i0++) {
          let data3 = data2[i0];
          if (data3 && typeof data3 == "object" && !Array.isArray(data3)) {
            if (data3.category === void 0) {
              const err7 = { instancePath: instancePath + "/groups/" + i0, schemaPath: "#/$defs/ToonWarningSummaryGroup/required", keyword: "required", params: { missingProperty: "category" }, message: "must have required property 'category'" };
              if (vErrors === null) {
                vErrors = [err7];
              } else {
                vErrors.push(err7);
              }
              errors++;
            }
            if (data3.code === void 0) {
              const err8 = { instancePath: instancePath + "/groups/" + i0, schemaPath: "#/$defs/ToonWarningSummaryGroup/required", keyword: "required", params: { missingProperty: "code" }, message: "must have required property 'code'" };
              if (vErrors === null) {
                vErrors = [err8];
              } else {
                vErrors.push(err8);
              }
              errors++;
            }
            if (data3.unique_diagnostic_count === void 0) {
              const err9 = { instancePath: instancePath + "/groups/" + i0, schemaPath: "#/$defs/ToonWarningSummaryGroup/required", keyword: "required", params: { missingProperty: "unique_diagnostic_count" }, message: "must have required property 'unique_diagnostic_count'" };
              if (vErrors === null) {
                vErrors = [err9];
              } else {
                vErrors.push(err9);
              }
              errors++;
            }
            if (data3.occurrence_count === void 0) {
              const err10 = { instancePath: instancePath + "/groups/" + i0, schemaPath: "#/$defs/ToonWarningSummaryGroup/required", keyword: "required", params: { missingProperty: "occurrence_count" }, message: "must have required property 'occurrence_count'" };
              if (vErrors === null) {
                vErrors = [err10];
              } else {
                vErrors.push(err10);
              }
              errors++;
            }
            if (data3.affected_component_count === void 0) {
              const err11 = { instancePath: instancePath + "/groups/" + i0, schemaPath: "#/$defs/ToonWarningSummaryGroup/required", keyword: "required", params: { missingProperty: "affected_component_count" }, message: "must have required property 'affected_component_count'" };
              if (vErrors === null) {
                vErrors = [err11];
              } else {
                vErrors.push(err11);
              }
              errors++;
            }
            if (data3.affected_body_count === void 0) {
              const err12 = { instancePath: instancePath + "/groups/" + i0, schemaPath: "#/$defs/ToonWarningSummaryGroup/required", keyword: "required", params: { missingProperty: "affected_body_count" }, message: "must have required property 'affected_body_count'" };
              if (vErrors === null) {
                vErrors = [err12];
              } else {
                vErrors.push(err12);
              }
              errors++;
            }
            if (data3.affected_model_count === void 0) {
              const err13 = { instancePath: instancePath + "/groups/" + i0, schemaPath: "#/$defs/ToonWarningSummaryGroup/required", keyword: "required", params: { missingProperty: "affected_model_count" }, message: "must have required property 'affected_model_count'" };
              if (vErrors === null) {
                vErrors = [err13];
              } else {
                vErrors.push(err13);
              }
              errors++;
            }
            if (data3.sample_designators === void 0) {
              const err14 = { instancePath: instancePath + "/groups/" + i0, schemaPath: "#/$defs/ToonWarningSummaryGroup/required", keyword: "required", params: { missingProperty: "sample_designators" }, message: "must have required property 'sample_designators'" };
              if (vErrors === null) {
                vErrors = [err14];
              } else {
                vErrors.push(err14);
              }
              errors++;
            }
            if (data3.category !== void 0) {
              let data4 = data3.category;
              const _errs11 = errors;
              let valid5 = false;
              const _errs12 = errors;
              if (typeof data4 !== "string") {
                const err15 = { instancePath: instancePath + "/groups/" + i0 + "/category", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/category/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err15];
                } else {
                  vErrors.push(err15);
                }
                errors++;
              }
              if ("missing_model" !== data4) {
                const err16 = { instancePath: instancePath + "/groups/" + i0 + "/category", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/category/anyOf/0/const", keyword: "const", params: { allowedValue: "missing_model" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err16];
                } else {
                  vErrors.push(err16);
                }
                errors++;
              }
              var _valid0 = _errs12 === errors;
              valid5 = valid5 || _valid0;
              const _errs14 = errors;
              if (typeof data4 !== "string") {
                const err17 = { instancePath: instancePath + "/groups/" + i0 + "/category", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/category/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err17];
                } else {
                  vErrors.push(err17);
                }
                errors++;
              }
              if ("unsupported_model" !== data4) {
                const err18 = { instancePath: instancePath + "/groups/" + i0 + "/category", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/category/anyOf/1/const", keyword: "const", params: { allowedValue: "unsupported_model" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err18];
                } else {
                  vErrors.push(err18);
                }
                errors++;
              }
              var _valid0 = _errs14 === errors;
              valid5 = valid5 || _valid0;
              const _errs16 = errors;
              if (typeof data4 !== "string") {
                const err19 = { instancePath: instancePath + "/groups/" + i0 + "/category", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/category/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err19];
                } else {
                  vErrors.push(err19);
                }
                errors++;
              }
              if ("invalid_model_geometry" !== data4) {
                const err20 = { instancePath: instancePath + "/groups/" + i0 + "/category", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/category/anyOf/2/const", keyword: "const", params: { allowedValue: "invalid_model_geometry" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err20];
                } else {
                  vErrors.push(err20);
                }
                errors++;
              }
              var _valid0 = _errs16 === errors;
              valid5 = valid5 || _valid0;
              const _errs18 = errors;
              if (typeof data4 !== "string") {
                const err21 = { instancePath: instancePath + "/groups/" + i0 + "/category", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/category/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err21];
                } else {
                  vErrors.push(err21);
                }
                errors++;
              }
              if ("geometer_geometry" !== data4) {
                const err22 = { instancePath: instancePath + "/groups/" + i0 + "/category", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/category/anyOf/3/const", keyword: "const", params: { allowedValue: "geometer_geometry" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err22];
                } else {
                  vErrors.push(err22);
                }
                errors++;
              }
              var _valid0 = _errs18 === errors;
              valid5 = valid5 || _valid0;
              const _errs20 = errors;
              if (typeof data4 !== "string") {
                const err23 = { instancePath: instancePath + "/groups/" + i0 + "/category", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/category/anyOf/4/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err23];
                } else {
                  vErrors.push(err23);
                }
                errors++;
              }
              if ("region_resolution" !== data4) {
                const err24 = { instancePath: instancePath + "/groups/" + i0 + "/category", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/category/anyOf/4/const", keyword: "const", params: { allowedValue: "region_resolution" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err24];
                } else {
                  vErrors.push(err24);
                }
                errors++;
              }
              var _valid0 = _errs20 === errors;
              valid5 = valid5 || _valid0;
              const _errs22 = errors;
              if (typeof data4 !== "string") {
                const err25 = { instancePath: instancePath + "/groups/" + i0 + "/category", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/category/anyOf/5/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err25];
                } else {
                  vErrors.push(err25);
                }
                errors++;
              }
              if ("rotation_resolution" !== data4) {
                const err26 = { instancePath: instancePath + "/groups/" + i0 + "/category", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/category/anyOf/5/const", keyword: "const", params: { allowedValue: "rotation_resolution" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err26];
                } else {
                  vErrors.push(err26);
                }
                errors++;
              }
              var _valid0 = _errs22 === errors;
              valid5 = valid5 || _valid0;
              const _errs24 = errors;
              if (typeof data4 !== "string") {
                const err27 = { instancePath: instancePath + "/groups/" + i0 + "/category", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/category/anyOf/6/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err27];
                } else {
                  vErrors.push(err27);
                }
                errors++;
              }
              if ("clipping" !== data4) {
                const err28 = { instancePath: instancePath + "/groups/" + i0 + "/category", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/category/anyOf/6/const", keyword: "const", params: { allowedValue: "clipping" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err28];
                } else {
                  vErrors.push(err28);
                }
                errors++;
              }
              var _valid0 = _errs24 === errors;
              valid5 = valid5 || _valid0;
              if (!valid5) {
                const err29 = { instancePath: instancePath + "/groups/" + i0 + "/category", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/category/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err29];
                } else {
                  vErrors.push(err29);
                }
                errors++;
              } else {
                errors = _errs11;
                if (vErrors !== null) {
                  if (_errs11) {
                    vErrors.length = _errs11;
                  } else {
                    vErrors = null;
                  }
                }
              }
            }
            if (data3.code !== void 0) {
              if (typeof data3.code !== "string") {
                const err30 = { instancePath: instancePath + "/groups/" + i0 + "/code", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/code/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err30];
                } else {
                  vErrors.push(err30);
                }
                errors++;
              }
            }
            if (data3.unique_diagnostic_count !== void 0) {
              let data6 = data3.unique_diagnostic_count;
              if (!(typeof data6 == "number" && (!(data6 % 1) && !isNaN(data6)))) {
                const err31 = { instancePath: instancePath + "/groups/" + i0 + "/unique_diagnostic_count", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/unique_diagnostic_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
                if (vErrors === null) {
                  vErrors = [err31];
                } else {
                  vErrors.push(err31);
                }
                errors++;
              }
              if (typeof data6 == "number") {
                if (data6 < 1 || isNaN(data6)) {
                  const err32 = { instancePath: instancePath + "/groups/" + i0 + "/unique_diagnostic_count", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/unique_diagnostic_count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 1 }, message: "must be >= 1" };
                  if (vErrors === null) {
                    vErrors = [err32];
                  } else {
                    vErrors.push(err32);
                  }
                  errors++;
                }
              }
            }
            if (data3.occurrence_count !== void 0) {
              let data7 = data3.occurrence_count;
              if (!(typeof data7 == "number" && (!(data7 % 1) && !isNaN(data7)))) {
                const err33 = { instancePath: instancePath + "/groups/" + i0 + "/occurrence_count", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/occurrence_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
                if (vErrors === null) {
                  vErrors = [err33];
                } else {
                  vErrors.push(err33);
                }
                errors++;
              }
              if (typeof data7 == "number") {
                if (data7 < 1 || isNaN(data7)) {
                  const err34 = { instancePath: instancePath + "/groups/" + i0 + "/occurrence_count", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/occurrence_count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 1 }, message: "must be >= 1" };
                  if (vErrors === null) {
                    vErrors = [err34];
                  } else {
                    vErrors.push(err34);
                  }
                  errors++;
                }
              }
            }
            if (data3.affected_component_count !== void 0) {
              let data8 = data3.affected_component_count;
              if (!(typeof data8 == "number" && (!(data8 % 1) && !isNaN(data8)))) {
                const err35 = { instancePath: instancePath + "/groups/" + i0 + "/affected_component_count", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/affected_component_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
                if (vErrors === null) {
                  vErrors = [err35];
                } else {
                  vErrors.push(err35);
                }
                errors++;
              }
              if (typeof data8 == "number") {
                if (data8 < 0 || isNaN(data8)) {
                  const err36 = { instancePath: instancePath + "/groups/" + i0 + "/affected_component_count", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/affected_component_count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
                  if (vErrors === null) {
                    vErrors = [err36];
                  } else {
                    vErrors.push(err36);
                  }
                  errors++;
                }
              }
            }
            if (data3.affected_body_count !== void 0) {
              let data9 = data3.affected_body_count;
              if (!(typeof data9 == "number" && (!(data9 % 1) && !isNaN(data9)))) {
                const err37 = { instancePath: instancePath + "/groups/" + i0 + "/affected_body_count", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/affected_body_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
                if (vErrors === null) {
                  vErrors = [err37];
                } else {
                  vErrors.push(err37);
                }
                errors++;
              }
              if (typeof data9 == "number") {
                if (data9 < 0 || isNaN(data9)) {
                  const err38 = { instancePath: instancePath + "/groups/" + i0 + "/affected_body_count", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/affected_body_count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
                  if (vErrors === null) {
                    vErrors = [err38];
                  } else {
                    vErrors.push(err38);
                  }
                  errors++;
                }
              }
            }
            if (data3.affected_model_count !== void 0) {
              let data10 = data3.affected_model_count;
              if (!(typeof data10 == "number" && (!(data10 % 1) && !isNaN(data10)))) {
                const err39 = { instancePath: instancePath + "/groups/" + i0 + "/affected_model_count", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/affected_model_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
                if (vErrors === null) {
                  vErrors = [err39];
                } else {
                  vErrors.push(err39);
                }
                errors++;
              }
              if (typeof data10 == "number") {
                if (data10 < 0 || isNaN(data10)) {
                  const err40 = { instancePath: instancePath + "/groups/" + i0 + "/affected_model_count", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/affected_model_count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
                  if (vErrors === null) {
                    vErrors = [err40];
                  } else {
                    vErrors.push(err40);
                  }
                  errors++;
                }
              }
            }
            if (data3.sample_designators !== void 0) {
              let data11 = data3.sample_designators;
              if (Array.isArray(data11)) {
                const len1 = data11.length;
                for (let i1 = 0; i1 < len1; i1++) {
                  if (typeof data11[i1] !== "string") {
                    const err41 = { instancePath: instancePath + "/groups/" + i0 + "/sample_designators/" + i1, schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/sample_designators/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                    if (vErrors === null) {
                      vErrors = [err41];
                    } else {
                      vErrors.push(err41);
                    }
                    errors++;
                  }
                }
              } else {
                const err42 = { instancePath: instancePath + "/groups/" + i0 + "/sample_designators", schemaPath: "#/$defs/ToonWarningSummaryGroup/properties/sample_designators/type", keyword: "type", params: { type: "array" }, message: "must be array" };
                if (vErrors === null) {
                  vErrors = [err42];
                } else {
                  vErrors.push(err42);
                }
                errors++;
              }
            }
            for (const key0 in data3) {
              if (key0 !== "category" && key0 !== "code" && key0 !== "unique_diagnostic_count" && key0 !== "occurrence_count" && key0 !== "affected_component_count" && key0 !== "affected_body_count" && key0 !== "affected_model_count" && key0 !== "sample_designators") {
                const err43 = { instancePath: instancePath + "/groups/" + i0 + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/ToonWarningSummaryGroup/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err43];
                } else {
                  vErrors.push(err43);
                }
                errors++;
              }
            }
          } else {
            const err44 = { instancePath: instancePath + "/groups/" + i0, schemaPath: "#/$defs/ToonWarningSummaryGroup/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err44];
            } else {
              vErrors.push(err44);
            }
            errors++;
          }
        }
      } else {
        const err45 = { instancePath: instancePath + "/groups", schemaPath: "#/properties/groups/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err45];
        } else {
          vErrors.push(err45);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "unique_diagnostic_count" && key1 !== "occurrence_count" && key1 !== "groups") {
        const err46 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err46];
        } else {
          vErrors.push(err46);
        }
        errors++;
      }
    }
  } else {
    const err47 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err47];
    } else {
      vErrors.push(err47);
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
    if (data.key === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "key" }, message: "must have required property 'key'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.code === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "code" }, message: "must have required property 'code'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.severity === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "severity" }, message: "must have required property 'severity'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.category === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "category" }, message: "must have required property 'category'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.producer === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "producer" }, message: "must have required property 'producer'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.message === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "message" }, message: "must have required property 'message'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.occurrence_count === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "occurrence_count" }, message: "must have required property 'occurrence_count'" };
      if (vErrors === null) {
        vErrors = [err6];
      } else {
        vErrors.push(err6);
      }
      errors++;
    }
    if (data.key !== void 0) {
      if (typeof data.key !== "string") {
        const err7 = { instancePath: instancePath + "/key", schemaPath: "#/properties/key/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.code !== void 0) {
      if (typeof data.code !== "string") {
        const err8 = { instancePath: instancePath + "/code", schemaPath: "#/properties/code/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
    if (data.severity !== void 0) {
      let data2 = data.severity;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/severity", schemaPath: "#/properties/severity/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      if ("warning" !== data2) {
        const err10 = { instancePath: instancePath + "/severity", schemaPath: "#/properties/severity/const", keyword: "const", params: { allowedValue: "warning" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
    }
    if (data.category !== void 0) {
      let data3 = data.category;
      const _errs8 = errors;
      let valid1 = false;
      const _errs9 = errors;
      if (typeof data3 !== "string") {
        const err11 = { instancePath: instancePath + "/category", schemaPath: "#/properties/category/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      if ("missing_model" !== data3) {
        const err12 = { instancePath: instancePath + "/category", schemaPath: "#/properties/category/anyOf/0/const", keyword: "const", params: { allowedValue: "missing_model" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
      var _valid0 = _errs9 === errors;
      valid1 = valid1 || _valid0;
      const _errs11 = errors;
      if (typeof data3 !== "string") {
        const err13 = { instancePath: instancePath + "/category", schemaPath: "#/properties/category/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
      if ("unsupported_model" !== data3) {
        const err14 = { instancePath: instancePath + "/category", schemaPath: "#/properties/category/anyOf/1/const", keyword: "const", params: { allowedValue: "unsupported_model" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
      var _valid0 = _errs11 === errors;
      valid1 = valid1 || _valid0;
      const _errs13 = errors;
      if (typeof data3 !== "string") {
        const err15 = { instancePath: instancePath + "/category", schemaPath: "#/properties/category/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
      if ("invalid_model_geometry" !== data3) {
        const err16 = { instancePath: instancePath + "/category", schemaPath: "#/properties/category/anyOf/2/const", keyword: "const", params: { allowedValue: "invalid_model_geometry" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
      var _valid0 = _errs13 === errors;
      valid1 = valid1 || _valid0;
      const _errs15 = errors;
      if (typeof data3 !== "string") {
        const err17 = { instancePath: instancePath + "/category", schemaPath: "#/properties/category/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
      if ("geometer_geometry" !== data3) {
        const err18 = { instancePath: instancePath + "/category", schemaPath: "#/properties/category/anyOf/3/const", keyword: "const", params: { allowedValue: "geometer_geometry" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
      var _valid0 = _errs15 === errors;
      valid1 = valid1 || _valid0;
      const _errs17 = errors;
      if (typeof data3 !== "string") {
        const err19 = { instancePath: instancePath + "/category", schemaPath: "#/properties/category/anyOf/4/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
      if ("region_resolution" !== data3) {
        const err20 = { instancePath: instancePath + "/category", schemaPath: "#/properties/category/anyOf/4/const", keyword: "const", params: { allowedValue: "region_resolution" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
      var _valid0 = _errs17 === errors;
      valid1 = valid1 || _valid0;
      const _errs19 = errors;
      if (typeof data3 !== "string") {
        const err21 = { instancePath: instancePath + "/category", schemaPath: "#/properties/category/anyOf/5/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
      if ("rotation_resolution" !== data3) {
        const err22 = { instancePath: instancePath + "/category", schemaPath: "#/properties/category/anyOf/5/const", keyword: "const", params: { allowedValue: "rotation_resolution" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
      var _valid0 = _errs19 === errors;
      valid1 = valid1 || _valid0;
      const _errs21 = errors;
      if (typeof data3 !== "string") {
        const err23 = { instancePath: instancePath + "/category", schemaPath: "#/properties/category/anyOf/6/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
      if ("clipping" !== data3) {
        const err24 = { instancePath: instancePath + "/category", schemaPath: "#/properties/category/anyOf/6/const", keyword: "const", params: { allowedValue: "clipping" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
      var _valid0 = _errs21 === errors;
      valid1 = valid1 || _valid0;
      if (!valid1) {
        const err25 = { instancePath: instancePath + "/category", schemaPath: "#/properties/category/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      } else {
        errors = _errs8;
        if (vErrors !== null) {
          if (_errs8) {
            vErrors.length = _errs8;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.producer !== void 0) {
      if (typeof data.producer !== "string") {
        const err26 = { instancePath: instancePath + "/producer", schemaPath: "#/properties/producer/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
    }
    if (data.message !== void 0) {
      if (typeof data.message !== "string") {
        const err27 = { instancePath: instancePath + "/message", schemaPath: "#/properties/message/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
    }
    if (data.occurrence_count !== void 0) {
      let data6 = data.occurrence_count;
      if (!(typeof data6 == "number" && (!(data6 % 1) && !isNaN(data6)))) {
        const err28 = { instancePath: instancePath + "/occurrence_count", schemaPath: "#/properties/occurrence_count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
      if (typeof data6 == "number") {
        if (data6 < 1 || isNaN(data6)) {
          const err29 = { instancePath: instancePath + "/occurrence_count", schemaPath: "#/properties/occurrence_count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 1 }, message: "must be >= 1" };
          if (vErrors === null) {
            vErrors = [err29];
          } else {
            vErrors.push(err29);
          }
          errors++;
        }
      }
    }
    if (data.input !== void 0) {
      if (typeof data.input !== "string") {
        const err30 = { instancePath: instancePath + "/input", schemaPath: "#/properties/input/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
        }
        errors++;
      }
    }
    if (data.board !== void 0) {
      if (typeof data.board !== "string") {
        const err31 = { instancePath: instancePath + "/board", schemaPath: "#/properties/board/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      }
    }
    if (data.variant !== void 0) {
      if (typeof data.variant !== "string") {
        const err32 = { instancePath: instancePath + "/variant", schemaPath: "#/properties/variant/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
        }
        errors++;
      }
    }
    if (data.view !== void 0) {
      if (typeof data.view !== "string") {
        const err33 = { instancePath: instancePath + "/view", schemaPath: "#/properties/view/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
    }
    if (data.component_designator !== void 0) {
      if (typeof data.component_designator !== "string") {
        const err34 = { instancePath: instancePath + "/component_designator", schemaPath: "#/properties/component_designator/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
        }
        errors++;
      }
    }
    if (data.body_index !== void 0) {
      let data12 = data.body_index;
      if (!(typeof data12 == "number" && (!(data12 % 1) && !isNaN(data12)))) {
        const err35 = { instancePath: instancePath + "/body_index", schemaPath: "#/properties/body_index/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err35];
        } else {
          vErrors.push(err35);
        }
        errors++;
      }
      if (typeof data12 == "number") {
        if (data12 < 0 || isNaN(data12)) {
          const err36 = { instancePath: instancePath + "/body_index", schemaPath: "#/properties/body_index/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err36];
          } else {
            vErrors.push(err36);
          }
          errors++;
        }
      }
    }
    if (data.model_identity !== void 0) {
      if (typeof data.model_identity !== "string") {
        const err37 = { instancePath: instancePath + "/model_identity", schemaPath: "#/properties/model_identity/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err37];
        } else {
          vErrors.push(err37);
        }
        errors++;
      }
    }
    if (data.detail !== void 0) {
      let data14 = data.detail;
      if (data14 && typeof data14 == "object" && !Array.isArray(data14)) {
      } else {
        const err38 = { instancePath: instancePath + "/detail", schemaPath: "#/$defs/RecordUnknown/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err38];
        } else {
          vErrors.push(err38);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "key" && key1 !== "code" && key1 !== "severity" && key1 !== "category" && key1 !== "producer" && key1 !== "message" && key1 !== "occurrence_count" && key1 !== "input" && key1 !== "board" && key1 !== "variant" && key1 !== "view" && key1 !== "component_designator" && key1 !== "body_index" && key1 !== "model_identity" && key1 !== "detail") {
        const err39 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err39];
        } else {
          vErrors.push(err39);
        }
        errors++;
      }
    }
  } else {
    const err40 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err40];
    } else {
      vErrors.push(err40);
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
    if (data.summary === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "summary" }, message: "must have required property 'summary'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.diagnostics === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "diagnostics" }, message: "must have required property 'diagnostics'" };
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
      if ("toon.warning_report.a0" !== data0) {
        const err4 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "toon.warning_report.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.summary !== void 0) {
      if (!validate21(data.summary, { instancePath: instancePath + "/summary", parentData: data, parentDataProperty: "summary", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
        errors = vErrors.length;
      }
    }
    if (data.diagnostics !== void 0) {
      let data2 = data.diagnostics;
      if (Array.isArray(data2)) {
        const len0 = data2.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!validate23(data2[i0], { instancePath: instancePath + "/diagnostics/" + i0, parentData: data2, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate23.errors : vErrors.concat(validate23.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err5 = { instancePath: instancePath + "/diagnostics", schemaPath: "#/properties/diagnostics/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    for (const key0 in data) {
      if (key0 !== "schema" && key0 !== "summary" && key0 !== "diagnostics") {
        const err6 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
  } else {
    const err7 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err7];
    } else {
      vErrors.push(err7);
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
