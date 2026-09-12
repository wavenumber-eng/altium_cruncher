// Generated from src/tsp/altium_cruncher/outputs/pcb-svg-timings.tsp. Do not edit.
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
    if (data.directory === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "directory" }, message: "must have required property 'directory'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.counts === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "counts" }, message: "must have required property 'counts'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.read_seconds === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "read_seconds" }, message: "must have required property 'read_seconds'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.write_seconds === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "write_seconds" }, message: "must have required property 'write_seconds'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.directory !== void 0) {
      if (typeof data.directory !== "string") {
        const err4 = { instancePath: instancePath + "/directory", schemaPath: "#/properties/directory/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.counts !== void 0) {
      let data1 = data.counts;
      if (data1 && typeof data1 == "object" && !Array.isArray(data1)) {
        if (data1.hits === void 0) {
          const err5 = { instancePath: instancePath + "/counts", schemaPath: "#/$defs/PcbSvgTimingsModelCacheObjectCounts/required", keyword: "required", params: { missingProperty: "hits" }, message: "must have required property 'hits'" };
          if (vErrors === null) {
            vErrors = [err5];
          } else {
            vErrors.push(err5);
          }
          errors++;
        }
        if (data1.misses === void 0) {
          const err6 = { instancePath: instancePath + "/counts", schemaPath: "#/$defs/PcbSvgTimingsModelCacheObjectCounts/required", keyword: "required", params: { missingProperty: "misses" }, message: "must have required property 'misses'" };
          if (vErrors === null) {
            vErrors = [err6];
          } else {
            vErrors.push(err6);
          }
          errors++;
        }
        if (data1.writes === void 0) {
          const err7 = { instancePath: instancePath + "/counts", schemaPath: "#/$defs/PcbSvgTimingsModelCacheObjectCounts/required", keyword: "required", params: { missingProperty: "writes" }, message: "must have required property 'writes'" };
          if (vErrors === null) {
            vErrors = [err7];
          } else {
            vErrors.push(err7);
          }
          errors++;
        }
        if (data1.invalid === void 0) {
          const err8 = { instancePath: instancePath + "/counts", schemaPath: "#/$defs/PcbSvgTimingsModelCacheObjectCounts/required", keyword: "required", params: { missingProperty: "invalid" }, message: "must have required property 'invalid'" };
          if (vErrors === null) {
            vErrors = [err8];
          } else {
            vErrors.push(err8);
          }
          errors++;
        }
        if (data1.evictions === void 0) {
          const err9 = { instancePath: instancePath + "/counts", schemaPath: "#/$defs/PcbSvgTimingsModelCacheObjectCounts/required", keyword: "required", params: { missingProperty: "evictions" }, message: "must have required property 'evictions'" };
          if (vErrors === null) {
            vErrors = [err9];
          } else {
            vErrors.push(err9);
          }
          errors++;
        }
        if (data1.hits !== void 0) {
          let data2 = data1.hits;
          if (!(typeof data2 == "number" && (!(data2 % 1) && !isNaN(data2)))) {
            const err10 = { instancePath: instancePath + "/counts/hits", schemaPath: "#/$defs/PcbSvgTimingsModelCacheObjectCounts/properties/hits/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
            if (vErrors === null) {
              vErrors = [err10];
            } else {
              vErrors.push(err10);
            }
            errors++;
          }
          if (typeof data2 == "number") {
            if (data2 < 0 || isNaN(data2)) {
              const err11 = { instancePath: instancePath + "/counts/hits", schemaPath: "#/$defs/PcbSvgTimingsModelCacheObjectCounts/properties/hits/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
              if (vErrors === null) {
                vErrors = [err11];
              } else {
                vErrors.push(err11);
              }
              errors++;
            }
          }
        }
        if (data1.misses !== void 0) {
          let data3 = data1.misses;
          if (!(typeof data3 == "number" && (!(data3 % 1) && !isNaN(data3)))) {
            const err12 = { instancePath: instancePath + "/counts/misses", schemaPath: "#/$defs/PcbSvgTimingsModelCacheObjectCounts/properties/misses/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
            if (vErrors === null) {
              vErrors = [err12];
            } else {
              vErrors.push(err12);
            }
            errors++;
          }
          if (typeof data3 == "number") {
            if (data3 < 0 || isNaN(data3)) {
              const err13 = { instancePath: instancePath + "/counts/misses", schemaPath: "#/$defs/PcbSvgTimingsModelCacheObjectCounts/properties/misses/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
              if (vErrors === null) {
                vErrors = [err13];
              } else {
                vErrors.push(err13);
              }
              errors++;
            }
          }
        }
        if (data1.writes !== void 0) {
          let data4 = data1.writes;
          if (!(typeof data4 == "number" && (!(data4 % 1) && !isNaN(data4)))) {
            const err14 = { instancePath: instancePath + "/counts/writes", schemaPath: "#/$defs/PcbSvgTimingsModelCacheObjectCounts/properties/writes/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
            if (vErrors === null) {
              vErrors = [err14];
            } else {
              vErrors.push(err14);
            }
            errors++;
          }
          if (typeof data4 == "number") {
            if (data4 < 0 || isNaN(data4)) {
              const err15 = { instancePath: instancePath + "/counts/writes", schemaPath: "#/$defs/PcbSvgTimingsModelCacheObjectCounts/properties/writes/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
              if (vErrors === null) {
                vErrors = [err15];
              } else {
                vErrors.push(err15);
              }
              errors++;
            }
          }
        }
        if (data1.invalid !== void 0) {
          let data5 = data1.invalid;
          if (!(typeof data5 == "number" && (!(data5 % 1) && !isNaN(data5)))) {
            const err16 = { instancePath: instancePath + "/counts/invalid", schemaPath: "#/$defs/PcbSvgTimingsModelCacheObjectCounts/properties/invalid/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
            if (vErrors === null) {
              vErrors = [err16];
            } else {
              vErrors.push(err16);
            }
            errors++;
          }
          if (typeof data5 == "number") {
            if (data5 < 0 || isNaN(data5)) {
              const err17 = { instancePath: instancePath + "/counts/invalid", schemaPath: "#/$defs/PcbSvgTimingsModelCacheObjectCounts/properties/invalid/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
              if (vErrors === null) {
                vErrors = [err17];
              } else {
                vErrors.push(err17);
              }
              errors++;
            }
          }
        }
        if (data1.evictions !== void 0) {
          let data6 = data1.evictions;
          if (!(typeof data6 == "number" && (!(data6 % 1) && !isNaN(data6)))) {
            const err18 = { instancePath: instancePath + "/counts/evictions", schemaPath: "#/$defs/PcbSvgTimingsModelCacheObjectCounts/properties/evictions/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
            if (vErrors === null) {
              vErrors = [err18];
            } else {
              vErrors.push(err18);
            }
            errors++;
          }
          if (typeof data6 == "number") {
            if (data6 < 0 || isNaN(data6)) {
              const err19 = { instancePath: instancePath + "/counts/evictions", schemaPath: "#/$defs/PcbSvgTimingsModelCacheObjectCounts/properties/evictions/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
              if (vErrors === null) {
                vErrors = [err19];
              } else {
                vErrors.push(err19);
              }
              errors++;
            }
          }
        }
        for (const key0 in data1) {
          if (key0 !== "hits" && key0 !== "misses" && key0 !== "writes" && key0 !== "invalid" && key0 !== "evictions") {
            const err20 = { instancePath: instancePath + "/counts/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/PcbSvgTimingsModelCacheObjectCounts/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err20];
            } else {
              vErrors.push(err20);
            }
            errors++;
          }
        }
      } else {
        const err21 = { instancePath: instancePath + "/counts", schemaPath: "#/$defs/PcbSvgTimingsModelCacheObjectCounts/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
    }
    if (data.read_seconds !== void 0) {
      let data8 = data.read_seconds;
      if (typeof data8 == "number") {
        if (data8 < 0 || isNaN(data8)) {
          const err22 = { instancePath: instancePath + "/read_seconds", schemaPath: "#/properties/read_seconds/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err22];
          } else {
            vErrors.push(err22);
          }
          errors++;
        }
      } else {
        const err23 = { instancePath: instancePath + "/read_seconds", schemaPath: "#/properties/read_seconds/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
    }
    if (data.write_seconds !== void 0) {
      let data9 = data.write_seconds;
      if (typeof data9 == "number") {
        if (data9 < 0 || isNaN(data9)) {
          const err24 = { instancePath: instancePath + "/write_seconds", schemaPath: "#/properties/write_seconds/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err24];
          } else {
            vErrors.push(err24);
          }
          errors++;
        }
      } else {
        const err25 = { instancePath: instancePath + "/write_seconds", schemaPath: "#/properties/write_seconds/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "directory" && key1 !== "counts" && key1 !== "read_seconds" && key1 !== "write_seconds") {
        const err26 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
    }
  } else {
    const err27 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err27];
    } else {
      vErrors.push(err27);
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
    if (data.clock === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "clock" }, message: "must have required property 'clock'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.notes === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "notes" }, message: "must have required property 'notes'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.events === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "events" }, message: "must have required property 'events'" };
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
      if ("pcb.svg.timings.a0" !== data0) {
        const err5 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "pcb.svg.timings.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.clock !== void 0) {
      let data1 = data.clock;
      if (typeof data1 !== "string") {
        const err6 = { instancePath: instancePath + "/clock", schemaPath: "#/properties/clock/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      if ("wall" !== data1) {
        const err7 = { instancePath: instancePath + "/clock", schemaPath: "#/properties/clock/const", keyword: "const", params: { allowedValue: "wall" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.workers !== void 0) {
      let data2 = data.workers;
      if (!(typeof data2 == "number" && (!(data2 % 1) && !isNaN(data2)))) {
        const err8 = { instancePath: instancePath + "/workers", schemaPath: "#/properties/workers/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
      if (typeof data2 == "number") {
        if (data2 < 1 || isNaN(data2)) {
          const err9 = { instancePath: instancePath + "/workers", schemaPath: "#/properties/workers/minimum", keyword: "minimum", params: { comparison: ">=", limit: 1 }, message: "must be >= 1" };
          if (vErrors === null) {
            vErrors = [err9];
          } else {
            vErrors.push(err9);
          }
          errors++;
        }
      }
    }
    if (data.notes !== void 0) {
      if (typeof data.notes !== "string") {
        const err10 = { instancePath: instancePath + "/notes", schemaPath: "#/properties/notes/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
    }
    if (data.model_cache !== void 0) {
      let data4 = data.model_cache;
      const _errs11 = errors;
      let valid1 = false;
      const _errs12 = errors;
      if (!validate21(data4, { instancePath: instancePath + "/model_cache", parentData: data, parentDataProperty: "model_cache", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
        errors = vErrors.length;
      }
      var _valid0 = _errs12 === errors;
      valid1 = valid1 || _valid0;
      const _errs13 = errors;
      if (data4 !== null) {
        const err11 = { instancePath: instancePath + "/model_cache", schemaPath: "#/properties/model_cache/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
      var _valid0 = _errs13 === errors;
      valid1 = valid1 || _valid0;
      if (!valid1) {
        const err12 = { instancePath: instancePath + "/model_cache", schemaPath: "#/properties/model_cache/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
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
    if (data.events !== void 0) {
      let data5 = data.events;
      if (Array.isArray(data5)) {
        const len0 = data5.length;
        for (let i0 = 0; i0 < len0; i0++) {
          let data6 = data5[i0];
          if (data6 && typeof data6 == "object" && !Array.isArray(data6)) {
            if (data6.id === void 0) {
              const err13 = { instancePath: instancePath + "/events/" + i0, schemaPath: "#/$defs/PcbSvgTimingsEventsItem/required", keyword: "required", params: { missingProperty: "id" }, message: "must have required property 'id'" };
              if (vErrors === null) {
                vErrors = [err13];
              } else {
                vErrors.push(err13);
              }
              errors++;
            }
            if (data6.parent_id === void 0) {
              const err14 = { instancePath: instancePath + "/events/" + i0, schemaPath: "#/$defs/PcbSvgTimingsEventsItem/required", keyword: "required", params: { missingProperty: "parent_id" }, message: "must have required property 'parent_id'" };
              if (vErrors === null) {
                vErrors = [err14];
              } else {
                vErrors.push(err14);
              }
              errors++;
            }
            if (data6.stage === void 0) {
              const err15 = { instancePath: instancePath + "/events/" + i0, schemaPath: "#/$defs/PcbSvgTimingsEventsItem/required", keyword: "required", params: { missingProperty: "stage" }, message: "must have required property 'stage'" };
              if (vErrors === null) {
                vErrors = [err15];
              } else {
                vErrors.push(err15);
              }
              errors++;
            }
            if (data6.cache === void 0) {
              const err16 = { instancePath: instancePath + "/events/" + i0, schemaPath: "#/$defs/PcbSvgTimingsEventsItem/required", keyword: "required", params: { missingProperty: "cache" }, message: "must have required property 'cache'" };
              if (vErrors === null) {
                vErrors = [err16];
              } else {
                vErrors.push(err16);
              }
              errors++;
            }
            if (data6.failed === void 0) {
              const err17 = { instancePath: instancePath + "/events/" + i0, schemaPath: "#/$defs/PcbSvgTimingsEventsItem/required", keyword: "required", params: { missingProperty: "failed" }, message: "must have required property 'failed'" };
              if (vErrors === null) {
                vErrors = [err17];
              } else {
                vErrors.push(err17);
              }
              errors++;
            }
            if (data6.seconds === void 0) {
              const err18 = { instancePath: instancePath + "/events/" + i0, schemaPath: "#/$defs/PcbSvgTimingsEventsItem/required", keyword: "required", params: { missingProperty: "seconds" }, message: "must have required property 'seconds'" };
              if (vErrors === null) {
                vErrors = [err18];
              } else {
                vErrors.push(err18);
              }
              errors++;
            }
            if (data6.exclusive_seconds === void 0) {
              const err19 = { instancePath: instancePath + "/events/" + i0, schemaPath: "#/$defs/PcbSvgTimingsEventsItem/required", keyword: "required", params: { missingProperty: "exclusive_seconds" }, message: "must have required property 'exclusive_seconds'" };
              if (vErrors === null) {
                vErrors = [err19];
              } else {
                vErrors.push(err19);
              }
              errors++;
            }
            if (data6.id !== void 0) {
              let data7 = data6.id;
              if (!(typeof data7 == "number" && (!(data7 % 1) && !isNaN(data7)))) {
                const err20 = { instancePath: instancePath + "/events/" + i0 + "/id", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/id/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
                if (vErrors === null) {
                  vErrors = [err20];
                } else {
                  vErrors.push(err20);
                }
                errors++;
              }
              if (typeof data7 == "number") {
                if (data7 < 0 || isNaN(data7)) {
                  const err21 = { instancePath: instancePath + "/events/" + i0 + "/id", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/id/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
                  if (vErrors === null) {
                    vErrors = [err21];
                  } else {
                    vErrors.push(err21);
                  }
                  errors++;
                }
              }
            }
            if (data6.parent_id !== void 0) {
              let data8 = data6.parent_id;
              const _errs23 = errors;
              let valid6 = false;
              const _errs24 = errors;
              if (!(typeof data8 == "number" && (!(data8 % 1) && !isNaN(data8)))) {
                const err22 = { instancePath: instancePath + "/events/" + i0 + "/parent_id", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/parent_id/anyOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
                if (vErrors === null) {
                  vErrors = [err22];
                } else {
                  vErrors.push(err22);
                }
                errors++;
              }
              var _valid1 = _errs24 === errors;
              valid6 = valid6 || _valid1;
              const _errs26 = errors;
              if (data8 !== null) {
                const err23 = { instancePath: instancePath + "/events/" + i0 + "/parent_id", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/parent_id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
                if (vErrors === null) {
                  vErrors = [err23];
                } else {
                  vErrors.push(err23);
                }
                errors++;
              }
              var _valid1 = _errs26 === errors;
              valid6 = valid6 || _valid1;
              if (!valid6) {
                const err24 = { instancePath: instancePath + "/events/" + i0 + "/parent_id", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/parent_id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err24];
                } else {
                  vErrors.push(err24);
                }
                errors++;
              } else {
                errors = _errs23;
                if (vErrors !== null) {
                  if (_errs23) {
                    vErrors.length = _errs23;
                  } else {
                    vErrors = null;
                  }
                }
              }
              if (typeof data8 == "number") {
                if (data8 < 0 || isNaN(data8)) {
                  const err25 = { instancePath: instancePath + "/events/" + i0 + "/parent_id", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/parent_id/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
                  if (vErrors === null) {
                    vErrors = [err25];
                  } else {
                    vErrors.push(err25);
                  }
                  errors++;
                }
              }
            }
            if (data6.stage !== void 0) {
              if (typeof data6.stage !== "string") {
                const err26 = { instancePath: instancePath + "/events/" + i0 + "/stage", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/stage/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err26];
                } else {
                  vErrors.push(err26);
                }
                errors++;
              }
            }
            if (data6.command !== void 0) {
              if (typeof data6.command !== "string") {
                const err27 = { instancePath: instancePath + "/events/" + i0 + "/command", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/command/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err27];
                } else {
                  vErrors.push(err27);
                }
                errors++;
              }
            }
            if (data6.board !== void 0) {
              if (typeof data6.board !== "string") {
                const err28 = { instancePath: instancePath + "/events/" + i0 + "/board", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/board/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err28];
                } else {
                  vErrors.push(err28);
                }
                errors++;
              }
            }
            if (data6.variant !== void 0) {
              if (typeof data6.variant !== "string") {
                const err29 = { instancePath: instancePath + "/events/" + i0 + "/variant", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/variant/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err29];
                } else {
                  vErrors.push(err29);
                }
                errors++;
              }
            }
            if (data6.view !== void 0) {
              if (typeof data6.view !== "string") {
                const err30 = { instancePath: instancePath + "/events/" + i0 + "/view", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/view/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err30];
                } else {
                  vErrors.push(err30);
                }
                errors++;
              }
            }
            if (data6.side !== void 0) {
              let data14 = data6.side;
              const _errs39 = errors;
              let valid7 = false;
              const _errs40 = errors;
              if (typeof data14 !== "string") {
                const err31 = { instancePath: instancePath + "/events/" + i0 + "/side", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/side/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err31];
                } else {
                  vErrors.push(err31);
                }
                errors++;
              }
              if ("top" !== data14) {
                const err32 = { instancePath: instancePath + "/events/" + i0 + "/side", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/side/anyOf/0/const", keyword: "const", params: { allowedValue: "top" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err32];
                } else {
                  vErrors.push(err32);
                }
                errors++;
              }
              var _valid2 = _errs40 === errors;
              valid7 = valid7 || _valid2;
              const _errs42 = errors;
              if (typeof data14 !== "string") {
                const err33 = { instancePath: instancePath + "/events/" + i0 + "/side", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/side/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err33];
                } else {
                  vErrors.push(err33);
                }
                errors++;
              }
              if ("bottom" !== data14) {
                const err34 = { instancePath: instancePath + "/events/" + i0 + "/side", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/side/anyOf/1/const", keyword: "const", params: { allowedValue: "bottom" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err34];
                } else {
                  vErrors.push(err34);
                }
                errors++;
              }
              var _valid2 = _errs42 === errors;
              valid7 = valid7 || _valid2;
              const _errs44 = errors;
              if (typeof data14 !== "string") {
                const err35 = { instancePath: instancePath + "/events/" + i0 + "/side", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/side/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err35];
                } else {
                  vErrors.push(err35);
                }
                errors++;
              }
              if ("both" !== data14) {
                const err36 = { instancePath: instancePath + "/events/" + i0 + "/side", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/side/anyOf/2/const", keyword: "const", params: { allowedValue: "both" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err36];
                } else {
                  vErrors.push(err36);
                }
                errors++;
              }
              var _valid2 = _errs44 === errors;
              valid7 = valid7 || _valid2;
              const _errs46 = errors;
              if (typeof data14 !== "string") {
                const err37 = { instancePath: instancePath + "/events/" + i0 + "/side", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/side/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err37];
                } else {
                  vErrors.push(err37);
                }
                errors++;
              }
              if ("board" !== data14) {
                const err38 = { instancePath: instancePath + "/events/" + i0 + "/side", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/side/anyOf/3/const", keyword: "const", params: { allowedValue: "board" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err38];
                } else {
                  vErrors.push(err38);
                }
                errors++;
              }
              var _valid2 = _errs46 === errors;
              valid7 = valid7 || _valid2;
              if (!valid7) {
                const err39 = { instancePath: instancePath + "/events/" + i0 + "/side", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/side/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err39];
                } else {
                  vErrors.push(err39);
                }
                errors++;
              } else {
                errors = _errs39;
                if (vErrors !== null) {
                  if (_errs39) {
                    vErrors.length = _errs39;
                  } else {
                    vErrors = null;
                  }
                }
              }
            }
            if (data6.layer !== void 0) {
              if (typeof data6.layer !== "string") {
                const err40 = { instancePath: instancePath + "/events/" + i0 + "/layer", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/layer/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err40];
                } else {
                  vErrors.push(err40);
                }
                errors++;
              }
            }
            if (data6.part !== void 0) {
              if (typeof data6.part !== "string") {
                const err41 = { instancePath: instancePath + "/events/" + i0 + "/part", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/part/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err41];
                } else {
                  vErrors.push(err41);
                }
                errors++;
              }
            }
            if (data6.cache !== void 0) {
              let data17 = data6.cache;
              const _errs53 = errors;
              let valid8 = false;
              const _errs54 = errors;
              if (typeof data17 !== "string") {
                const err42 = { instancePath: instancePath + "/events/" + i0 + "/cache", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/cache/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err42];
                } else {
                  vErrors.push(err42);
                }
                errors++;
              }
              if ("none" !== data17) {
                const err43 = { instancePath: instancePath + "/events/" + i0 + "/cache", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/cache/anyOf/0/const", keyword: "const", params: { allowedValue: "none" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err43];
                } else {
                  vErrors.push(err43);
                }
                errors++;
              }
              var _valid3 = _errs54 === errors;
              valid8 = valid8 || _valid3;
              const _errs56 = errors;
              if (typeof data17 !== "string") {
                const err44 = { instancePath: instancePath + "/events/" + i0 + "/cache", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/cache/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err44];
                } else {
                  vErrors.push(err44);
                }
                errors++;
              }
              if ("built" !== data17) {
                const err45 = { instancePath: instancePath + "/events/" + i0 + "/cache", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/cache/anyOf/1/const", keyword: "const", params: { allowedValue: "built" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err45];
                } else {
                  vErrors.push(err45);
                }
                errors++;
              }
              var _valid3 = _errs56 === errors;
              valid8 = valid8 || _valid3;
              const _errs58 = errors;
              if (typeof data17 !== "string") {
                const err46 = { instancePath: instancePath + "/events/" + i0 + "/cache", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/cache/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err46];
                } else {
                  vErrors.push(err46);
                }
                errors++;
              }
              if ("hit" !== data17) {
                const err47 = { instancePath: instancePath + "/events/" + i0 + "/cache", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/cache/anyOf/2/const", keyword: "const", params: { allowedValue: "hit" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err47];
                } else {
                  vErrors.push(err47);
                }
                errors++;
              }
              var _valid3 = _errs58 === errors;
              valid8 = valid8 || _valid3;
              const _errs60 = errors;
              if (typeof data17 !== "string") {
                const err48 = { instancePath: instancePath + "/events/" + i0 + "/cache", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/cache/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err48];
                } else {
                  vErrors.push(err48);
                }
                errors++;
              }
              if ("assembled" !== data17) {
                const err49 = { instancePath: instancePath + "/events/" + i0 + "/cache", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/cache/anyOf/3/const", keyword: "const", params: { allowedValue: "assembled" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err49];
                } else {
                  vErrors.push(err49);
                }
                errors++;
              }
              var _valid3 = _errs60 === errors;
              valid8 = valid8 || _valid3;
              const _errs62 = errors;
              if (typeof data17 !== "string") {
                const err50 = { instancePath: instancePath + "/events/" + i0 + "/cache", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/cache/anyOf/4/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err50];
                } else {
                  vErrors.push(err50);
                }
                errors++;
              }
              if ("disabled" !== data17) {
                const err51 = { instancePath: instancePath + "/events/" + i0 + "/cache", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/cache/anyOf/4/const", keyword: "const", params: { allowedValue: "disabled" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err51];
                } else {
                  vErrors.push(err51);
                }
                errors++;
              }
              var _valid3 = _errs62 === errors;
              valid8 = valid8 || _valid3;
              if (!valid8) {
                const err52 = { instancePath: instancePath + "/events/" + i0 + "/cache", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/cache/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err52];
                } else {
                  vErrors.push(err52);
                }
                errors++;
              } else {
                errors = _errs53;
                if (vErrors !== null) {
                  if (_errs53) {
                    vErrors.length = _errs53;
                  } else {
                    vErrors = null;
                  }
                }
              }
            }
            if (data6.failed !== void 0) {
              if (typeof data6.failed !== "boolean") {
                const err53 = { instancePath: instancePath + "/events/" + i0 + "/failed", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/failed/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
                if (vErrors === null) {
                  vErrors = [err53];
                } else {
                  vErrors.push(err53);
                }
                errors++;
              }
            }
            if (data6.seconds !== void 0) {
              let data19 = data6.seconds;
              if (typeof data19 == "number") {
                if (data19 < 0 || isNaN(data19)) {
                  const err54 = { instancePath: instancePath + "/events/" + i0 + "/seconds", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/seconds/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
                  if (vErrors === null) {
                    vErrors = [err54];
                  } else {
                    vErrors.push(err54);
                  }
                  errors++;
                }
              } else {
                const err55 = { instancePath: instancePath + "/events/" + i0 + "/seconds", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/seconds/type", keyword: "type", params: { type: "number" }, message: "must be number" };
                if (vErrors === null) {
                  vErrors = [err55];
                } else {
                  vErrors.push(err55);
                }
                errors++;
              }
            }
            if (data6.exclusive_seconds !== void 0) {
              let data20 = data6.exclusive_seconds;
              if (typeof data20 == "number") {
                if (data20 < 0 || isNaN(data20)) {
                  const err56 = { instancePath: instancePath + "/events/" + i0 + "/exclusive_seconds", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/exclusive_seconds/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
                  if (vErrors === null) {
                    vErrors = [err56];
                  } else {
                    vErrors.push(err56);
                  }
                  errors++;
                }
              } else {
                const err57 = { instancePath: instancePath + "/events/" + i0 + "/exclusive_seconds", schemaPath: "#/$defs/PcbSvgTimingsEventsItem/properties/exclusive_seconds/type", keyword: "type", params: { type: "number" }, message: "must be number" };
                if (vErrors === null) {
                  vErrors = [err57];
                } else {
                  vErrors.push(err57);
                }
                errors++;
              }
            }
            for (const key0 in data6) {
              if (key0 !== "id" && key0 !== "parent_id" && key0 !== "stage" && key0 !== "command" && key0 !== "board" && key0 !== "variant" && key0 !== "view" && key0 !== "side" && key0 !== "layer" && key0 !== "part" && key0 !== "cache" && key0 !== "failed" && key0 !== "seconds" && key0 !== "exclusive_seconds") {
                const err58 = { instancePath: instancePath + "/events/" + i0 + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/PcbSvgTimingsEventsItem/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err58];
                } else {
                  vErrors.push(err58);
                }
                errors++;
              }
            }
          } else {
            const err59 = { instancePath: instancePath + "/events/" + i0, schemaPath: "#/$defs/PcbSvgTimingsEventsItem/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err59];
            } else {
              vErrors.push(err59);
            }
            errors++;
          }
        }
      } else {
        const err60 = { instancePath: instancePath + "/events", schemaPath: "#/properties/events/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err60];
        } else {
          vErrors.push(err60);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "schema" && key1 !== "clock" && key1 !== "workers" && key1 !== "notes" && key1 !== "model_cache" && key1 !== "events") {
        const err61 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err61];
        } else {
          vErrors.push(err61);
        }
        errors++;
      }
    }
  } else {
    const err62 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err62];
    } else {
      vErrors.push(err62);
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
