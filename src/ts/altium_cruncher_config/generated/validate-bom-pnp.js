// Generated from src/tsp/altium_cruncher/config/bom-pnp-config.tsp. Do not edit.
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
      if (Array.isArray(data0)) {
        const len0 = data0.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (typeof data0[i0] !== "string") {
            const err0 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1") + "/" + i0, schemaPath: "#/$defs/RecordArrayString/unevaluatedProperties/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err0];
            } else {
              vErrors.push(err0);
            }
            errors++;
          }
        }
      } else {
        const err1 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/RecordArrayString/unevaluatedProperties/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
    }
  } else {
    const err2 = { instancePath, schemaPath: "#/$defs/RecordArrayString/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err2];
    } else {
      vErrors.push(err2);
    }
    errors++;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
  } else {
    const err3 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err3];
    } else {
      vErrors.push(err3);
    }
    errors++;
  }
  validate21.errors = vErrors;
  return errors === 0;
}
validate21.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate25(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate25.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    for (const key0 in data) {
      if (typeof data[key0] !== "string") {
        const err0 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/RecordString/unevaluatedProperties/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err0];
        } else {
          vErrors.push(err0);
        }
        errors++;
      }
    }
  } else {
    const err1 = { instancePath, schemaPath: "#/$defs/RecordString/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err1];
    } else {
      vErrors.push(err1);
    }
    errors++;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
  } else {
    const err2 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err2];
    } else {
      vErrors.push(err2);
    }
    errors++;
  }
  validate25.errors = vErrors;
  return errors === 0;
}
validate25.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate24(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate24.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.enabled !== void 0) {
      if (typeof data.enabled !== "boolean") {
        const err0 = { instancePath: instancePath + "/enabled", schemaPath: "#/properties/enabled/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err0];
        } else {
          vErrors.push(err0);
        }
        errors++;
      }
    }
    if (data.designator !== void 0) {
      if (typeof data.designator !== "string") {
        const err1 = { instancePath: instancePath + "/designator", schemaPath: "#/properties/designator/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
    }
    if (data.fields !== void 0) {
      if (!validate25(data.fields, { instancePath: instancePath + "/fields", parentData: data, parentDataProperty: "fields", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate25.errors : vErrors.concat(validate25.errors);
        errors = vErrors.length;
      }
    }
    for (const key0 in data) {
      if (key0 !== "enabled" && key0 !== "designator" && key0 !== "fields") {
        const err2 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
    }
  } else {
    const err3 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err3];
    } else {
      vErrors.push(err3);
    }
    errors++;
  }
  validate24.errors = vErrors;
  return errors === 0;
}
validate24.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.source_mode !== void 0) {
      let data0 = data.source_mode;
      const _errs2 = errors;
      let valid1 = false;
      const _errs3 = errors;
      if (typeof data0 !== "string") {
        const err0 = { instancePath: instancePath + "/source_mode", schemaPath: "#/properties/source_mode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err0];
        } else {
          vErrors.push(err0);
        }
        errors++;
      }
      if ("schematic" !== data0) {
        const err1 = { instancePath: instancePath + "/source_mode", schemaPath: "#/properties/source_mode/anyOf/0/const", keyword: "const", params: { allowedValue: "schematic" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      var _valid0 = _errs3 === errors;
      valid1 = valid1 || _valid0;
      const _errs5 = errors;
      if (typeof data0 !== "string") {
        const err2 = { instancePath: instancePath + "/source_mode", schemaPath: "#/properties/source_mode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      if ("pcb" !== data0) {
        const err3 = { instancePath: instancePath + "/source_mode", schemaPath: "#/properties/source_mode/anyOf/1/const", keyword: "const", params: { allowedValue: "pcb" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
      var _valid0 = _errs5 === errors;
      valid1 = valid1 || _valid0;
      const _errs7 = errors;
      if (typeof data0 !== "string") {
        const err4 = { instancePath: instancePath + "/source_mode", schemaPath: "#/properties/source_mode/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      if ("merged" !== data0) {
        const err5 = { instancePath: instancePath + "/source_mode", schemaPath: "#/properties/source_mode/anyOf/2/const", keyword: "const", params: { allowedValue: "merged" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      var _valid0 = _errs7 === errors;
      valid1 = valid1 || _valid0;
      if (!valid1) {
        const err6 = { instancePath: instancePath + "/source_mode", schemaPath: "#/properties/source_mode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      } else {
        errors = _errs2;
        if (vErrors !== null) {
          if (_errs2) {
            vErrors.length = _errs2;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.outputs !== void 0) {
      let data1 = data.outputs;
      if (Array.isArray(data1)) {
        const len0 = data1.length;
        for (let i0 = 0; i0 < len0; i0++) {
          let data2 = data1[i0];
          const _errs12 = errors;
          let valid4 = false;
          const _errs13 = errors;
          if (typeof data2 !== "string") {
            const err7 = { instancePath: instancePath + "/outputs/" + i0, schemaPath: "#/properties/outputs/items/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err7];
            } else {
              vErrors.push(err7);
            }
            errors++;
          }
          if ("raw-json" !== data2) {
            const err8 = { instancePath: instancePath + "/outputs/" + i0, schemaPath: "#/properties/outputs/items/anyOf/0/const", keyword: "const", params: { allowedValue: "raw-json" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err8];
            } else {
              vErrors.push(err8);
            }
            errors++;
          }
          var _valid1 = _errs13 === errors;
          valid4 = valid4 || _valid1;
          const _errs15 = errors;
          if (typeof data2 !== "string") {
            const err9 = { instancePath: instancePath + "/outputs/" + i0, schemaPath: "#/properties/outputs/items/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err9];
            } else {
              vErrors.push(err9);
            }
            errors++;
          }
          if ("legacy-json" !== data2) {
            const err10 = { instancePath: instancePath + "/outputs/" + i0, schemaPath: "#/properties/outputs/items/anyOf/1/const", keyword: "const", params: { allowedValue: "legacy-json" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err10];
            } else {
              vErrors.push(err10);
            }
            errors++;
          }
          var _valid1 = _errs15 === errors;
          valid4 = valid4 || _valid1;
          const _errs17 = errors;
          if (typeof data2 !== "string") {
            const err11 = { instancePath: instancePath + "/outputs/" + i0, schemaPath: "#/properties/outputs/items/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err11];
            } else {
              vErrors.push(err11);
            }
            errors++;
          }
          if ("grouped-json" !== data2) {
            const err12 = { instancePath: instancePath + "/outputs/" + i0, schemaPath: "#/properties/outputs/items/anyOf/2/const", keyword: "const", params: { allowedValue: "grouped-json" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err12];
            } else {
              vErrors.push(err12);
            }
            errors++;
          }
          var _valid1 = _errs17 === errors;
          valid4 = valid4 || _valid1;
          const _errs19 = errors;
          if (typeof data2 !== "string") {
            const err13 = { instancePath: instancePath + "/outputs/" + i0, schemaPath: "#/properties/outputs/items/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err13];
            } else {
              vErrors.push(err13);
            }
            errors++;
          }
          if ("grouped-csv" !== data2) {
            const err14 = { instancePath: instancePath + "/outputs/" + i0, schemaPath: "#/properties/outputs/items/anyOf/3/const", keyword: "const", params: { allowedValue: "grouped-csv" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err14];
            } else {
              vErrors.push(err14);
            }
            errors++;
          }
          var _valid1 = _errs19 === errors;
          valid4 = valid4 || _valid1;
          const _errs21 = errors;
          if (typeof data2 !== "string") {
            const err15 = { instancePath: instancePath + "/outputs/" + i0, schemaPath: "#/properties/outputs/items/anyOf/4/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err15];
            } else {
              vErrors.push(err15);
            }
            errors++;
          }
          if ("grouped-xlsx" !== data2) {
            const err16 = { instancePath: instancePath + "/outputs/" + i0, schemaPath: "#/properties/outputs/items/anyOf/4/const", keyword: "const", params: { allowedValue: "grouped-xlsx" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err16];
            } else {
              vErrors.push(err16);
            }
            errors++;
          }
          var _valid1 = _errs21 === errors;
          valid4 = valid4 || _valid1;
          const _errs23 = errors;
          if (typeof data2 !== "string") {
            const err17 = { instancePath: instancePath + "/outputs/" + i0, schemaPath: "#/properties/outputs/items/anyOf/5/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err17];
            } else {
              vErrors.push(err17);
            }
            errors++;
          }
          if ("jlc-csv" !== data2) {
            const err18 = { instancePath: instancePath + "/outputs/" + i0, schemaPath: "#/properties/outputs/items/anyOf/5/const", keyword: "const", params: { allowedValue: "jlc-csv" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err18];
            } else {
              vErrors.push(err18);
            }
            errors++;
          }
          var _valid1 = _errs23 === errors;
          valid4 = valid4 || _valid1;
          const _errs25 = errors;
          if (typeof data2 !== "string") {
            const err19 = { instancePath: instancePath + "/outputs/" + i0, schemaPath: "#/properties/outputs/items/anyOf/6/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err19];
            } else {
              vErrors.push(err19);
            }
            errors++;
          }
          if ("jlc-xlsx" !== data2) {
            const err20 = { instancePath: instancePath + "/outputs/" + i0, schemaPath: "#/properties/outputs/items/anyOf/6/const", keyword: "const", params: { allowedValue: "jlc-xlsx" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err20];
            } else {
              vErrors.push(err20);
            }
            errors++;
          }
          var _valid1 = _errs25 === errors;
          valid4 = valid4 || _valid1;
          if (!valid4) {
            const err21 = { instancePath: instancePath + "/outputs/" + i0, schemaPath: "#/properties/outputs/items/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err21];
            } else {
              vErrors.push(err21);
            }
            errors++;
          } else {
            errors = _errs12;
            if (vErrors !== null) {
              if (_errs12) {
                vErrors.length = _errs12;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err22 = { instancePath: instancePath + "/outputs", schemaPath: "#/properties/outputs/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
    }
    if (data.group_fields !== void 0) {
      let data3 = data.group_fields;
      if (Array.isArray(data3)) {
        const len1 = data3.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (typeof data3[i1] !== "string") {
            const err23 = { instancePath: instancePath + "/group_fields/" + i1, schemaPath: "#/properties/group_fields/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err23];
            } else {
              vErrors.push(err23);
            }
            errors++;
          }
        }
      } else {
        const err24 = { instancePath: instancePath + "/group_fields", schemaPath: "#/properties/group_fields/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
    }
    if (data.output_fields !== void 0) {
      let data5 = data.output_fields;
      if (Array.isArray(data5)) {
        const len2 = data5.length;
        for (let i2 = 0; i2 < len2; i2++) {
          if (typeof data5[i2] !== "string") {
            const err25 = { instancePath: instancePath + "/output_fields/" + i2, schemaPath: "#/properties/output_fields/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err25];
            } else {
              vErrors.push(err25);
            }
            errors++;
          }
        }
      } else {
        const err26 = { instancePath: instancePath + "/output_fields", schemaPath: "#/properties/output_fields/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err26];
        } else {
          vErrors.push(err26);
        }
        errors++;
      }
    }
    if (data.include_dnp !== void 0) {
      if (typeof data.include_dnp !== "boolean") {
        const err27 = { instancePath: instancePath + "/include_dnp", schemaPath: "#/properties/include_dnp/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
    }
    if (data.split_dnp !== void 0) {
      if (typeof data.split_dnp !== "boolean") {
        const err28 = { instancePath: instancePath + "/split_dnp", schemaPath: "#/properties/split_dnp/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
    }
    if (data.dnp_placement !== void 0) {
      let data9 = data.dnp_placement;
      const _errs40 = errors;
      let valid9 = false;
      const _errs41 = errors;
      if (typeof data9 !== "string") {
        const err29 = { instancePath: instancePath + "/dnp_placement", schemaPath: "#/properties/dnp_placement/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      }
      if ("inline" !== data9) {
        const err30 = { instancePath: instancePath + "/dnp_placement", schemaPath: "#/properties/dnp_placement/anyOf/0/const", keyword: "const", params: { allowedValue: "inline" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err30];
        } else {
          vErrors.push(err30);
        }
        errors++;
      }
      var _valid2 = _errs41 === errors;
      valid9 = valid9 || _valid2;
      const _errs43 = errors;
      if (typeof data9 !== "string") {
        const err31 = { instancePath: instancePath + "/dnp_placement", schemaPath: "#/properties/dnp_placement/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      }
      if ("end" !== data9) {
        const err32 = { instancePath: instancePath + "/dnp_placement", schemaPath: "#/properties/dnp_placement/anyOf/1/const", keyword: "const", params: { allowedValue: "end" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
        }
        errors++;
      }
      var _valid2 = _errs43 === errors;
      valid9 = valid9 || _valid2;
      const _errs45 = errors;
      if (typeof data9 !== "string") {
        const err33 = { instancePath: instancePath + "/dnp_placement", schemaPath: "#/properties/dnp_placement/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
      if ("separate" !== data9) {
        const err34 = { instancePath: instancePath + "/dnp_placement", schemaPath: "#/properties/dnp_placement/anyOf/2/const", keyword: "const", params: { allowedValue: "separate" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
        }
        errors++;
      }
      var _valid2 = _errs45 === errors;
      valid9 = valid9 || _valid2;
      if (!valid9) {
        const err35 = { instancePath: instancePath + "/dnp_placement", schemaPath: "#/properties/dnp_placement/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err35];
        } else {
          vErrors.push(err35);
        }
        errors++;
      } else {
        errors = _errs40;
        if (vErrors !== null) {
          if (_errs40) {
            vErrors.length = _errs40;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.highlight_dnp_rows !== void 0) {
      if (typeof data.highlight_dnp_rows !== "boolean") {
        const err36 = { instancePath: instancePath + "/highlight_dnp_rows", schemaPath: "#/properties/highlight_dnp_rows/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err36];
        } else {
          vErrors.push(err36);
        }
        errors++;
      }
    }
    if (data.prefix_order !== void 0) {
      let data11 = data.prefix_order;
      if (Array.isArray(data11)) {
        const len3 = data11.length;
        for (let i3 = 0; i3 < len3; i3++) {
          if (typeof data11[i3] !== "string") {
            const err37 = { instancePath: instancePath + "/prefix_order/" + i3, schemaPath: "#/properties/prefix_order/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err37];
            } else {
              vErrors.push(err37);
            }
            errors++;
          }
        }
      } else {
        const err38 = { instancePath: instancePath + "/prefix_order", schemaPath: "#/properties/prefix_order/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err38];
        } else {
          vErrors.push(err38);
        }
        errors++;
      }
    }
    if (data.pcb_line_item !== void 0) {
      if (!validate24(data.pcb_line_item, { instancePath: instancePath + "/pcb_line_item", parentData: data, parentDataProperty: "pcb_line_item", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate24.errors : vErrors.concat(validate24.errors);
        errors = vErrors.length;
      }
    }
    for (const key0 in data) {
      if (key0 !== "source_mode" && key0 !== "outputs" && key0 !== "group_fields" && key0 !== "output_fields" && key0 !== "include_dnp" && key0 !== "split_dnp" && key0 !== "dnp_placement" && key0 !== "highlight_dnp_rows" && key0 !== "prefix_order" && key0 !== "pcb_line_item") {
        const err39 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
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
    if (data.schema !== void 0) {
      let data0 = data.schema;
      const _errs3 = errors;
      let valid1 = false;
      const _errs4 = errors;
      if (typeof data0 !== "string") {
        const err0 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err0];
        } else {
          vErrors.push(err0);
        }
        errors++;
      }
      if ("altium_cruncher.bom.config.a0" !== data0) {
        const err1 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf/0/const", keyword: "const", params: { allowedValue: "altium_cruncher.bom.config.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      }
      var _valid0 = _errs4 === errors;
      valid1 = valid1 || _valid0;
      const _errs6 = errors;
      if (data0 !== null) {
        const err2 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      var _valid0 = _errs6 === errors;
      valid1 = valid1 || _valid0;
      if (!valid1) {
        const err3 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      } else {
        errors = _errs3;
        if (vErrors !== null) {
          if (_errs3) {
            vErrors.length = _errs3;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.field_aliases !== void 0) {
      if (!validate21(data.field_aliases, { instancePath: instancePath + "/field_aliases", parentData: data, parentDataProperty: "field_aliases", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
        errors = vErrors.length;
      }
    }
    if (data.variants !== void 0) {
      let data2 = data.variants;
      if (data2 && typeof data2 == "object" && !Array.isArray(data2)) {
        if (data2.mode !== void 0) {
          let data3 = data2.mode;
          const _errs13 = errors;
          let valid4 = false;
          const _errs14 = errors;
          if (typeof data3 !== "string") {
            const err4 = { instancePath: instancePath + "/variants/mode", schemaPath: "#/$defs/BomPnpConfigInputVariants/properties/mode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err4];
            } else {
              vErrors.push(err4);
            }
            errors++;
          }
          if ("base" !== data3) {
            const err5 = { instancePath: instancePath + "/variants/mode", schemaPath: "#/$defs/BomPnpConfigInputVariants/properties/mode/anyOf/0/const", keyword: "const", params: { allowedValue: "base" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err5];
            } else {
              vErrors.push(err5);
            }
            errors++;
          }
          var _valid1 = _errs14 === errors;
          valid4 = valid4 || _valid1;
          const _errs16 = errors;
          if (typeof data3 !== "string") {
            const err6 = { instancePath: instancePath + "/variants/mode", schemaPath: "#/$defs/BomPnpConfigInputVariants/properties/mode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err6];
            } else {
              vErrors.push(err6);
            }
            errors++;
          }
          if ("all" !== data3) {
            const err7 = { instancePath: instancePath + "/variants/mode", schemaPath: "#/$defs/BomPnpConfigInputVariants/properties/mode/anyOf/1/const", keyword: "const", params: { allowedValue: "all" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err7];
            } else {
              vErrors.push(err7);
            }
            errors++;
          }
          var _valid1 = _errs16 === errors;
          valid4 = valid4 || _valid1;
          const _errs18 = errors;
          if (typeof data3 !== "string") {
            const err8 = { instancePath: instancePath + "/variants/mode", schemaPath: "#/$defs/BomPnpConfigInputVariants/properties/mode/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err8];
            } else {
              vErrors.push(err8);
            }
            errors++;
          }
          if ("named" !== data3) {
            const err9 = { instancePath: instancePath + "/variants/mode", schemaPath: "#/$defs/BomPnpConfigInputVariants/properties/mode/anyOf/2/const", keyword: "const", params: { allowedValue: "named" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err9];
            } else {
              vErrors.push(err9);
            }
            errors++;
          }
          var _valid1 = _errs18 === errors;
          valid4 = valid4 || _valid1;
          if (!valid4) {
            const err10 = { instancePath: instancePath + "/variants/mode", schemaPath: "#/$defs/BomPnpConfigInputVariants/properties/mode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err10];
            } else {
              vErrors.push(err10);
            }
            errors++;
          } else {
            errors = _errs13;
            if (vErrors !== null) {
              if (_errs13) {
                vErrors.length = _errs13;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data2.names !== void 0) {
          let data4 = data2.names;
          if (Array.isArray(data4)) {
            const len0 = data4.length;
            for (let i0 = 0; i0 < len0; i0++) {
              if (typeof data4[i0] !== "string") {
                const err11 = { instancePath: instancePath + "/variants/names/" + i0, schemaPath: "#/$defs/BomPnpConfigInputVariants/properties/names/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err11];
                } else {
                  vErrors.push(err11);
                }
                errors++;
              }
            }
          } else {
            const err12 = { instancePath: instancePath + "/variants/names", schemaPath: "#/$defs/BomPnpConfigInputVariants/properties/names/type", keyword: "type", params: { type: "array" }, message: "must be array" };
            if (vErrors === null) {
              vErrors = [err12];
            } else {
              vErrors.push(err12);
            }
            errors++;
          }
        }
        if (data2.include_base !== void 0) {
          if (typeof data2.include_base !== "boolean") {
            const err13 = { instancePath: instancePath + "/variants/include_base", schemaPath: "#/$defs/BomPnpConfigInputVariants/properties/include_base/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err13];
            } else {
              vErrors.push(err13);
            }
            errors++;
          }
        }
        for (const key0 in data2) {
          if (key0 !== "mode" && key0 !== "names" && key0 !== "include_base") {
            const err14 = { instancePath: instancePath + "/variants/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/BomPnpConfigInputVariants/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err14];
            } else {
              vErrors.push(err14);
            }
            errors++;
          }
        }
      } else {
        const err15 = { instancePath: instancePath + "/variants", schemaPath: "#/$defs/BomPnpConfigInputVariants/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
    }
    if (data.bom !== void 0) {
      if (!validate23(data.bom, { instancePath: instancePath + "/bom", parentData: data, parentDataProperty: "bom", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate23.errors : vErrors.concat(validate23.errors);
        errors = vErrors.length;
      }
    }
    if (data.pnp !== void 0) {
      let data9 = data.pnp;
      if (data9 && typeof data9 == "object" && !Array.isArray(data9)) {
        if (data9.outputs !== void 0) {
          let data10 = data9.outputs;
          if (Array.isArray(data10)) {
            const len1 = data10.length;
            for (let i1 = 0; i1 < len1; i1++) {
              let data11 = data10[i1];
              const _errs36 = errors;
              let valid12 = false;
              const _errs37 = errors;
              if (typeof data11 !== "string") {
                const err16 = { instancePath: instancePath + "/pnp/outputs/" + i1, schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/outputs/items/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err16];
                } else {
                  vErrors.push(err16);
                }
                errors++;
              }
              if ("json" !== data11) {
                const err17 = { instancePath: instancePath + "/pnp/outputs/" + i1, schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/outputs/items/anyOf/0/const", keyword: "const", params: { allowedValue: "json" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err17];
                } else {
                  vErrors.push(err17);
                }
                errors++;
              }
              var _valid2 = _errs37 === errors;
              valid12 = valid12 || _valid2;
              const _errs39 = errors;
              if (typeof data11 !== "string") {
                const err18 = { instancePath: instancePath + "/pnp/outputs/" + i1, schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/outputs/items/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err18];
                } else {
                  vErrors.push(err18);
                }
                errors++;
              }
              if ("csv" !== data11) {
                const err19 = { instancePath: instancePath + "/pnp/outputs/" + i1, schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/outputs/items/anyOf/1/const", keyword: "const", params: { allowedValue: "csv" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err19];
                } else {
                  vErrors.push(err19);
                }
                errors++;
              }
              var _valid2 = _errs39 === errors;
              valid12 = valid12 || _valid2;
              const _errs41 = errors;
              if (typeof data11 !== "string") {
                const err20 = { instancePath: instancePath + "/pnp/outputs/" + i1, schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/outputs/items/anyOf/2/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err20];
                } else {
                  vErrors.push(err20);
                }
                errors++;
              }
              if ("xlsx" !== data11) {
                const err21 = { instancePath: instancePath + "/pnp/outputs/" + i1, schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/outputs/items/anyOf/2/const", keyword: "const", params: { allowedValue: "xlsx" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err21];
                } else {
                  vErrors.push(err21);
                }
                errors++;
              }
              var _valid2 = _errs41 === errors;
              valid12 = valid12 || _valid2;
              const _errs43 = errors;
              if (typeof data11 !== "string") {
                const err22 = { instancePath: instancePath + "/pnp/outputs/" + i1, schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/outputs/items/anyOf/3/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err22];
                } else {
                  vErrors.push(err22);
                }
                errors++;
              }
              if ("jlc-cpl" !== data11) {
                const err23 = { instancePath: instancePath + "/pnp/outputs/" + i1, schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/outputs/items/anyOf/3/const", keyword: "const", params: { allowedValue: "jlc-cpl" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err23];
                } else {
                  vErrors.push(err23);
                }
                errors++;
              }
              var _valid2 = _errs43 === errors;
              valid12 = valid12 || _valid2;
              const _errs45 = errors;
              if (typeof data11 !== "string") {
                const err24 = { instancePath: instancePath + "/pnp/outputs/" + i1, schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/outputs/items/anyOf/4/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err24];
                } else {
                  vErrors.push(err24);
                }
                errors++;
              }
              if ("jlc-cpl-xlsx" !== data11) {
                const err25 = { instancePath: instancePath + "/pnp/outputs/" + i1, schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/outputs/items/anyOf/4/const", keyword: "const", params: { allowedValue: "jlc-cpl-xlsx" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err25];
                } else {
                  vErrors.push(err25);
                }
                errors++;
              }
              var _valid2 = _errs45 === errors;
              valid12 = valid12 || _valid2;
              if (!valid12) {
                const err26 = { instancePath: instancePath + "/pnp/outputs/" + i1, schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/outputs/items/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err26];
                } else {
                  vErrors.push(err26);
                }
                errors++;
              } else {
                errors = _errs36;
                if (vErrors !== null) {
                  if (_errs36) {
                    vErrors.length = _errs36;
                  } else {
                    vErrors = null;
                  }
                }
              }
            }
          } else {
            const err27 = { instancePath: instancePath + "/pnp/outputs", schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/outputs/type", keyword: "type", params: { type: "array" }, message: "must be array" };
            if (vErrors === null) {
              vErrors = [err27];
            } else {
              vErrors.push(err27);
            }
            errors++;
          }
        }
        if (data9.output_fields !== void 0) {
          let data12 = data9.output_fields;
          if (Array.isArray(data12)) {
            const len2 = data12.length;
            for (let i2 = 0; i2 < len2; i2++) {
              if (typeof data12[i2] !== "string") {
                const err28 = { instancePath: instancePath + "/pnp/output_fields/" + i2, schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/output_fields/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err28];
                } else {
                  vErrors.push(err28);
                }
                errors++;
              }
            }
          } else {
            const err29 = { instancePath: instancePath + "/pnp/output_fields", schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/output_fields/type", keyword: "type", params: { type: "array" }, message: "must be array" };
            if (vErrors === null) {
              vErrors = [err29];
            } else {
              vErrors.push(err29);
            }
            errors++;
          }
        }
        if (data9.units !== void 0) {
          let data14 = data9.units;
          const _errs52 = errors;
          let valid15 = false;
          const _errs53 = errors;
          if (typeof data14 !== "string") {
            const err30 = { instancePath: instancePath + "/pnp/units", schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/units/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err30];
            } else {
              vErrors.push(err30);
            }
            errors++;
          }
          if ("mm" !== data14) {
            const err31 = { instancePath: instancePath + "/pnp/units", schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/units/anyOf/0/const", keyword: "const", params: { allowedValue: "mm" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err31];
            } else {
              vErrors.push(err31);
            }
            errors++;
          }
          var _valid3 = _errs53 === errors;
          valid15 = valid15 || _valid3;
          const _errs55 = errors;
          if (typeof data14 !== "string") {
            const err32 = { instancePath: instancePath + "/pnp/units", schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/units/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err32];
            } else {
              vErrors.push(err32);
            }
            errors++;
          }
          if ("mils" !== data14) {
            const err33 = { instancePath: instancePath + "/pnp/units", schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/units/anyOf/1/const", keyword: "const", params: { allowedValue: "mils" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err33];
            } else {
              vErrors.push(err33);
            }
            errors++;
          }
          var _valid3 = _errs55 === errors;
          valid15 = valid15 || _valid3;
          if (!valid15) {
            const err34 = { instancePath: instancePath + "/pnp/units", schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/units/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err34];
            } else {
              vErrors.push(err34);
            }
            errors++;
          } else {
            errors = _errs52;
            if (vErrors !== null) {
              if (_errs52) {
                vErrors.length = _errs52;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data9.position_mode !== void 0) {
          let data15 = data9.position_mode;
          const _errs58 = errors;
          let valid16 = false;
          const _errs59 = errors;
          if (typeof data15 !== "string") {
            const err35 = { instancePath: instancePath + "/pnp/position_mode", schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/position_mode/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err35];
            } else {
              vErrors.push(err35);
            }
            errors++;
          }
          if ("altium-pick-place" !== data15) {
            const err36 = { instancePath: instancePath + "/pnp/position_mode", schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/position_mode/anyOf/0/const", keyword: "const", params: { allowedValue: "altium-pick-place" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err36];
            } else {
              vErrors.push(err36);
            }
            errors++;
          }
          var _valid4 = _errs59 === errors;
          valid16 = valid16 || _valid4;
          const _errs61 = errors;
          if (typeof data15 !== "string") {
            const err37 = { instancePath: instancePath + "/pnp/position_mode", schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/position_mode/anyOf/1/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err37];
            } else {
              vErrors.push(err37);
            }
            errors++;
          }
          if ("component-origin" !== data15) {
            const err38 = { instancePath: instancePath + "/pnp/position_mode", schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/position_mode/anyOf/1/const", keyword: "const", params: { allowedValue: "component-origin" }, message: "must be equal to constant" };
            if (vErrors === null) {
              vErrors = [err38];
            } else {
              vErrors.push(err38);
            }
            errors++;
          }
          var _valid4 = _errs61 === errors;
          valid16 = valid16 || _valid4;
          if (!valid16) {
            const err39 = { instancePath: instancePath + "/pnp/position_mode", schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/position_mode/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err39];
            } else {
              vErrors.push(err39);
            }
            errors++;
          } else {
            errors = _errs58;
            if (vErrors !== null) {
              if (_errs58) {
                vErrors.length = _errs58;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data9.exclude_no_bom !== void 0) {
          if (typeof data9.exclude_no_bom !== "boolean") {
            const err40 = { instancePath: instancePath + "/pnp/exclude_no_bom", schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/exclude_no_bom/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err40];
            } else {
              vErrors.push(err40);
            }
            errors++;
          }
        }
        if (data9.layer_order !== void 0) {
          let data17 = data9.layer_order;
          if (Array.isArray(data17)) {
            const len3 = data17.length;
            for (let i3 = 0; i3 < len3; i3++) {
              if (typeof data17[i3] !== "string") {
                const err41 = { instancePath: instancePath + "/pnp/layer_order/" + i3, schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/layer_order/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err41];
                } else {
                  vErrors.push(err41);
                }
                errors++;
              }
            }
          } else {
            const err42 = { instancePath: instancePath + "/pnp/layer_order", schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/layer_order/type", keyword: "type", params: { type: "array" }, message: "must be array" };
            if (vErrors === null) {
              vErrors = [err42];
            } else {
              vErrors.push(err42);
            }
            errors++;
          }
        }
        if (data9.prefix_order !== void 0) {
          let data19 = data9.prefix_order;
          if (Array.isArray(data19)) {
            const len4 = data19.length;
            for (let i4 = 0; i4 < len4; i4++) {
              if (typeof data19[i4] !== "string") {
                const err43 = { instancePath: instancePath + "/pnp/prefix_order/" + i4, schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/prefix_order/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err43];
                } else {
                  vErrors.push(err43);
                }
                errors++;
              }
            }
          } else {
            const err44 = { instancePath: instancePath + "/pnp/prefix_order", schemaPath: "#/$defs/BomPnpConfigInputPnp/properties/prefix_order/type", keyword: "type", params: { type: "array" }, message: "must be array" };
            if (vErrors === null) {
              vErrors = [err44];
            } else {
              vErrors.push(err44);
            }
            errors++;
          }
        }
        for (const key1 in data9) {
          if (key1 !== "outputs" && key1 !== "output_fields" && key1 !== "units" && key1 !== "position_mode" && key1 !== "exclude_no_bom" && key1 !== "layer_order" && key1 !== "prefix_order") {
            const err45 = { instancePath: instancePath + "/pnp/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/BomPnpConfigInputPnp/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err45];
            } else {
              vErrors.push(err45);
            }
            errors++;
          }
        }
      } else {
        const err46 = { instancePath: instancePath + "/pnp", schemaPath: "#/$defs/BomPnpConfigInputPnp/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err46];
        } else {
          vErrors.push(err46);
        }
        errors++;
      }
    }
    if (data.output !== void 0) {
      let data22 = data.output;
      if (data22 && typeof data22 == "object" && !Array.isArray(data22)) {
        if (data22.dir_template !== void 0) {
          if (typeof data22.dir_template !== "string") {
            const err47 = { instancePath: instancePath + "/output/dir_template", schemaPath: "#/$defs/BomPnpConfigInputOutput/properties/dir_template/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err47];
            } else {
              vErrors.push(err47);
            }
            errors++;
          }
        }
        if (data22.name_template !== void 0) {
          if (typeof data22.name_template !== "string") {
            const err48 = { instancePath: instancePath + "/output/name_template", schemaPath: "#/$defs/BomPnpConfigInputOutput/properties/name_template/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err48];
            } else {
              vErrors.push(err48);
            }
            errors++;
          }
        }
        for (const key2 in data22) {
          if (key2 !== "dir_template" && key2 !== "name_template") {
            const err49 = { instancePath: instancePath + "/output/" + key2.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/BomPnpConfigInputOutput/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err49];
            } else {
              vErrors.push(err49);
            }
            errors++;
          }
        }
      } else {
        const err50 = { instancePath: instancePath + "/output", schemaPath: "#/$defs/BomPnpConfigInputOutput/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err50];
        } else {
          vErrors.push(err50);
        }
        errors++;
      }
    }
    for (const key3 in data) {
      if (key3 !== "schema" && key3 !== "field_aliases" && key3 !== "variants" && key3 !== "bom" && key3 !== "pnp" && key3 !== "output") {
        const err51 = { instancePath: instancePath + "/" + key3.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err51];
        } else {
          vErrors.push(err51);
        }
        errors++;
      }
    }
  } else {
    const err52 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err52];
    } else {
      vErrors.push(err52);
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
