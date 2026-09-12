// Generated from src/tsp/altium_cruncher/outputs/json-dump.tsp. Do not edit.
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
    if (data.format === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "format" }, message: "must have required property 'format'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.format !== void 0) {
      let data0 = data.format;
      if (typeof data0 !== "string") {
        const err2 = { instancePath: instancePath + "/format", schemaPath: "#/properties/format/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      if ("altium_monkey.schdoc.interop.a0" !== data0) {
        const err3 = { instancePath: instancePath + "/format", schemaPath: "#/properties/format/const", keyword: "const", params: { allowedValue: "altium_monkey.schdoc.interop.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
  } else {
    const err4 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err4];
    } else {
      vErrors.push(err4);
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
    if (data.kind === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "kind" }, message: "must have required property 'kind'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.document === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "document" }, message: "must have required property 'document'" };
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
      if ("altium_cruncher.json_dump.a0" !== data0) {
        const err4 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.json_dump.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.kind !== void 0) {
      let data1 = data.kind;
      if (typeof data1 !== "string") {
        const err5 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      if ("SchDoc" !== data1) {
        const err6 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/const", keyword: "const", params: { allowedValue: "SchDoc" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.document !== void 0) {
      if (!validate22(data.document, { instancePath: instancePath + "/document", parentData: data, parentDataProperty: "document", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate22.errors : vErrors.concat(validate22.errors);
        errors = vErrors.length;
      }
    }
    for (const key0 in data) {
      if (key0 !== "schema" && key0 !== "kind" && key0 !== "document") {
        const err7 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
  } else {
    const err8 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err8];
    } else {
      vErrors.push(err8);
    }
    errors++;
  }
  validate21.errors = vErrors;
  return errors === 0;
}
validate21.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate26(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate26.evaluated;
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
    if (data.format === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "format" }, message: "must have required property 'format'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.format !== void 0) {
      let data0 = data.format;
      if (typeof data0 !== "string") {
        const err2 = { instancePath: instancePath + "/format", schemaPath: "#/properties/format/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      if ("altium_monkey.schlib.interop.a0" !== data0) {
        const err3 = { instancePath: instancePath + "/format", schemaPath: "#/properties/format/const", keyword: "const", params: { allowedValue: "altium_monkey.schlib.interop.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
  } else {
    const err4 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err4];
    } else {
      vErrors.push(err4);
    }
    errors++;
  }
  validate26.errors = vErrors;
  return errors === 0;
}
validate26.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.schema === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "schema" }, message: "must have required property 'schema'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.kind === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "kind" }, message: "must have required property 'kind'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.document === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "document" }, message: "must have required property 'document'" };
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
      if ("altium_cruncher.json_dump.a0" !== data0) {
        const err4 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.json_dump.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.kind !== void 0) {
      let data1 = data.kind;
      if (typeof data1 !== "string") {
        const err5 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      if ("SchLib" !== data1) {
        const err6 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/const", keyword: "const", params: { allowedValue: "SchLib" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.document !== void 0) {
      if (!validate26(data.document, { instancePath: instancePath + "/document", parentData: data, parentDataProperty: "document", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate26.errors : vErrors.concat(validate26.errors);
        errors = vErrors.length;
      }
    }
    for (const key0 in data) {
      if (key0 !== "schema" && key0 !== "kind" && key0 !== "document") {
        const err7 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
  } else {
    const err8 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err8];
    } else {
      vErrors.push(err8);
    }
    errors++;
  }
  validate25.errors = vErrors;
  return errors === 0;
}
validate25.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate31(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate31.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    for (const key0 in data) {
      let data0 = data[key0];
      if (!(typeof data0 == "number" && (!(data0 % 1) && !isNaN(data0)))) {
        const err0 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err0];
        } else {
          vErrors.push(err0);
        }
        errors++;
      }
      if (typeof data0 == "number") {
        if (data0 < 0 || isNaN(data0)) {
          const err1 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err1];
          } else {
            vErrors.push(err1);
          }
          errors++;
        }
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
  validate31.errors = vErrors;
  return errors === 0;
}
validate31.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
var pattern4 = new RegExp("^[0-9a-f]{64}$", "u");
function validate33(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate33.evaluated;
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
    if (data.byte_count === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "byte_count" }, message: "must have required property 'byte_count'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.sha256 === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "sha256" }, message: "must have required property 'sha256'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.name !== void 0) {
      if (typeof data.name !== "string") {
        const err3 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.byte_count !== void 0) {
      let data1 = data.byte_count;
      if (!(typeof data1 == "number" && (!(data1 % 1) && !isNaN(data1)))) {
        const err4 = { instancePath: instancePath + "/byte_count", schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
      if (typeof data1 == "number") {
        if (data1 < 0 || isNaN(data1)) {
          const err5 = { instancePath: instancePath + "/byte_count", schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err5];
          } else {
            vErrors.push(err5);
          }
          errors++;
        }
      }
    }
    if (data.sha256 !== void 0) {
      let data2 = data.sha256;
      if (typeof data2 === "string") {
        if (!pattern4.test(data2)) {
          const err6 = { instancePath: instancePath + "/sha256", schemaPath: "#/properties/sha256/pattern", keyword: "pattern", params: { pattern: "^[0-9a-f]{64}$" }, message: 'must match pattern "^[0-9a-f]{64}$"' };
          if (vErrors === null) {
            vErrors = [err6];
          } else {
            vErrors.push(err6);
          }
          errors++;
        }
      } else {
        const err7 = { instancePath: instancePath + "/sha256", schemaPath: "#/properties/sha256/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    for (const key0 in data) {
      if (key0 !== "name" && key0 !== "byte_count" && key0 !== "sha256") {
        const err8 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
  } else {
    const err9 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err9];
    } else {
      vErrors.push(err9);
    }
    errors++;
  }
  validate33.errors = vErrors;
  return errors === 0;
}
validate33.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate37(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate37.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.class !== void 0) {
      if (typeof data.class !== "string") {
        const err0 = { instancePath: instancePath + "/class", schemaPath: "#/properties/class/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err0];
        } else {
          vErrors.push(err0);
        }
        errors++;
      }
    }
    if (data.designator !== void 0) {
      const _errs5 = errors;
      let valid2 = false;
      var _valid0 = true;
      valid2 = valid2 || _valid0;
      if (!valid2) {
        const err1 = { instancePath: instancePath + "/designator", schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err1];
        } else {
          vErrors.push(err1);
        }
        errors++;
      } else {
        errors = _errs5;
        if (vErrors !== null) {
          if (_errs5) {
            vErrors.length = _errs5;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.name !== void 0) {
      const _errs8 = errors;
      let valid4 = false;
      var _valid1 = true;
      valid4 = valid4 || _valid1;
      if (!valid4) {
        const err2 = { instancePath: instancePath + "/name", schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
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
    if (data.text_content !== void 0) {
      const _errs11 = errors;
      let valid6 = false;
      var _valid2 = true;
      valid6 = valid6 || _valid2;
      if (!valid6) {
        const err3 = { instancePath: instancePath + "/text_content", schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
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
    if (data.footprint !== void 0) {
      const _errs14 = errors;
      let valid8 = false;
      var _valid3 = true;
      valid8 = valid8 || _valid3;
      if (!valid8) {
        const err4 = { instancePath: instancePath + "/footprint", schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      } else {
        errors = _errs14;
        if (vErrors !== null) {
          if (_errs14) {
            vErrors.length = _errs14;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.comment !== void 0) {
      const _errs17 = errors;
      let valid10 = false;
      var _valid4 = true;
      valid10 = valid10 || _valid4;
      if (!valid10) {
        const err5 = { instancePath: instancePath + "/comment", schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      } else {
        errors = _errs17;
        if (vErrors !== null) {
          if (_errs17) {
            vErrors.length = _errs17;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.x_mils !== void 0) {
      const _errs20 = errors;
      let valid12 = false;
      var _valid5 = true;
      valid12 = valid12 || _valid5;
      if (!valid12) {
        const err6 = { instancePath: instancePath + "/x_mils", schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      } else {
        errors = _errs20;
        if (vErrors !== null) {
          if (_errs20) {
            vErrors.length = _errs20;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.y_mils !== void 0) {
      const _errs23 = errors;
      let valid14 = false;
      var _valid6 = true;
      valid14 = valid14 || _valid6;
      if (!valid14) {
        const err7 = { instancePath: instancePath + "/y_mils", schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
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
    }
    if (data.start_x_mils !== void 0) {
      const _errs26 = errors;
      let valid16 = false;
      var _valid7 = true;
      valid16 = valid16 || _valid7;
      if (!valid16) {
        const err8 = { instancePath: instancePath + "/start_x_mils", schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
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
    if (data.start_y_mils !== void 0) {
      const _errs29 = errors;
      let valid18 = false;
      var _valid8 = true;
      valid18 = valid18 || _valid8;
      if (!valid18) {
        const err9 = { instancePath: instancePath + "/start_y_mils", schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      } else {
        errors = _errs29;
        if (vErrors !== null) {
          if (_errs29) {
            vErrors.length = _errs29;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.end_x_mils !== void 0) {
      const _errs32 = errors;
      let valid20 = false;
      var _valid9 = true;
      valid20 = valid20 || _valid9;
      if (!valid20) {
        const err10 = { instancePath: instancePath + "/end_x_mils", schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      } else {
        errors = _errs32;
        if (vErrors !== null) {
          if (_errs32) {
            vErrors.length = _errs32;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.end_y_mils !== void 0) {
      const _errs35 = errors;
      let valid22 = false;
      var _valid10 = true;
      valid22 = valid22 || _valid10;
      if (!valid22) {
        const err11 = { instancePath: instancePath + "/end_y_mils", schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      } else {
        errors = _errs35;
        if (vErrors !== null) {
          if (_errs35) {
            vErrors.length = _errs35;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.center_x_mils !== void 0) {
      const _errs38 = errors;
      let valid24 = false;
      var _valid11 = true;
      valid24 = valid24 || _valid11;
      if (!valid24) {
        const err12 = { instancePath: instancePath + "/center_x_mils", schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
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
    if (data.center_y_mils !== void 0) {
      const _errs41 = errors;
      let valid26 = false;
      var _valid12 = true;
      valid26 = valid26 || _valid12;
      if (!valid26) {
        const err13 = { instancePath: instancePath + "/center_y_mils", schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      } else {
        errors = _errs41;
        if (vErrors !== null) {
          if (_errs41) {
            vErrors.length = _errs41;
          } else {
            vErrors = null;
          }
        }
      }
    }
    for (const key0 in data) {
      if (key0 !== "class" && key0 !== "designator" && key0 !== "name" && key0 !== "text_content" && key0 !== "footprint" && key0 !== "comment" && key0 !== "x_mils" && key0 !== "y_mils" && key0 !== "start_x_mils" && key0 !== "start_y_mils" && key0 !== "end_x_mils" && key0 !== "end_y_mils" && key0 !== "center_x_mils" && key0 !== "center_y_mils") {
        const err14 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
    }
  } else {
    const err15 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err15];
    } else {
      vErrors.push(err15);
    }
    errors++;
  }
  validate37.errors = vErrors;
  return errors === 0;
}
validate37.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate36(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate36.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.collection === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "collection" }, message: "must have required property 'collection'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.object_index === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "object_index" }, message: "must have required property 'object_index'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.union_index === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "union_index" }, message: "must have required property 'union_index'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.object_summary === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "object_summary" }, message: "must have required property 'object_summary'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.collection !== void 0) {
      if (typeof data.collection !== "string") {
        const err4 = { instancePath: instancePath + "/collection", schemaPath: "#/properties/collection/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.object_index !== void 0) {
      let data1 = data.object_index;
      if (!(typeof data1 == "number" && (!(data1 % 1) && !isNaN(data1)))) {
        const err5 = { instancePath: instancePath + "/object_index", schemaPath: "#/properties/object_index/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.union_index !== void 0) {
      let data2 = data.union_index;
      if (!(typeof data2 == "number" && (!(data2 % 1) && !isNaN(data2)))) {
        const err6 = { instancePath: instancePath + "/union_index", schemaPath: "#/properties/union_index/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.object_summary !== void 0) {
      if (!validate37(data.object_summary, { instancePath: instancePath + "/object_summary", parentData: data, parentDataProperty: "object_summary", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate37.errors : vErrors.concat(validate37.errors);
        errors = vErrors.length;
      }
    }
    for (const key0 in data) {
      if (key0 !== "collection" && key0 !== "object_index" && key0 !== "union_index" && key0 !== "object_summary") {
        const err7 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
  } else {
    const err8 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err8];
    } else {
      vErrors.push(err8);
    }
    errors++;
  }
  validate36.errors = vErrors;
  return errors === 0;
}
validate36.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate35(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate35.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.union_index === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "union_index" }, message: "must have required property 'union_index'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.name === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.member_count === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "member_count" }, message: "must have required property 'member_count'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.members === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "members" }, message: "must have required property 'members'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.union_index !== void 0) {
      let data0 = data.union_index;
      if (!(typeof data0 == "number" && (!(data0 % 1) && !isNaN(data0)))) {
        const err4 = { instancePath: instancePath + "/union_index", schemaPath: "#/properties/union_index/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.name !== void 0) {
      if (typeof data.name !== "string") {
        const err5 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.member_count !== void 0) {
      let data2 = data.member_count;
      if (!(typeof data2 == "number" && (!(data2 % 1) && !isNaN(data2)))) {
        const err6 = { instancePath: instancePath + "/member_count", schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
      if (typeof data2 == "number") {
        if (data2 < 0 || isNaN(data2)) {
          const err7 = { instancePath: instancePath + "/member_count", schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err7];
          } else {
            vErrors.push(err7);
          }
          errors++;
        }
      }
    }
    if (data.members !== void 0) {
      let data3 = data.members;
      if (Array.isArray(data3)) {
        const len0 = data3.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!validate36(data3[i0], { instancePath: instancePath + "/members/" + i0, parentData: data3, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate36.errors : vErrors.concat(validate36.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err8 = { instancePath: instancePath + "/members", schemaPath: "#/properties/members/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
    for (const key0 in data) {
      if (key0 !== "union_index" && key0 !== "name" && key0 !== "member_count" && key0 !== "members") {
        const err9 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
  } else {
    const err10 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err10];
    } else {
      vErrors.push(err10);
    }
    errors++;
  }
  validate35.errors = vErrors;
  return errors === 0;
}
validate35.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate30(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate30.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.pads === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "pads" }, message: "must have required property 'pads'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.vias === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "vias" }, message: "must have required property 'vias'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.tracks === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "tracks" }, message: "must have required property 'tracks'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.arcs === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "arcs" }, message: "must have required property 'arcs'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.texts === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "texts" }, message: "must have required property 'texts'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.fills === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "fills" }, message: "must have required property 'fills'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.regions === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "regions" }, message: "must have required property 'regions'" };
      if (vErrors === null) {
        vErrors = [err6];
      } else {
        vErrors.push(err6);
      }
      errors++;
    }
    if (data.shapebased_regions === void 0) {
      const err7 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "shapebased_regions" }, message: "must have required property 'shapebased_regions'" };
      if (vErrors === null) {
        vErrors = [err7];
      } else {
        vErrors.push(err7);
      }
      errors++;
    }
    if (data.component_bodies === void 0) {
      const err8 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "component_bodies" }, message: "must have required property 'component_bodies'" };
      if (vErrors === null) {
        vErrors = [err8];
      } else {
        vErrors.push(err8);
      }
      errors++;
    }
    if (data.models === void 0) {
      const err9 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "models" }, message: "must have required property 'models'" };
      if (vErrors === null) {
        vErrors = [err9];
      } else {
        vErrors.push(err9);
      }
      errors++;
    }
    if (data.format === void 0) {
      const err10 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "format" }, message: "must have required property 'format'" };
      if (vErrors === null) {
        vErrors = [err10];
      } else {
        vErrors.push(err10);
      }
      errors++;
    }
    if (data.counts === void 0) {
      const err11 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "counts" }, message: "must have required property 'counts'" };
      if (vErrors === null) {
        vErrors = [err11];
      } else {
        vErrors.push(err11);
      }
      errors++;
    }
    if (data.raw_streams === void 0) {
      const err12 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "raw_streams" }, message: "must have required property 'raw_streams'" };
      if (vErrors === null) {
        vErrors = [err12];
      } else {
        vErrors.push(err12);
      }
      errors++;
    }
    if (data.board === void 0) {
      const err13 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "board" }, message: "must have required property 'board'" };
      if (vErrors === null) {
        vErrors = [err13];
      } else {
        vErrors.push(err13);
      }
      errors++;
    }
    if (data.union_name_records === void 0) {
      const err14 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "union_name_records" }, message: "must have required property 'union_name_records'" };
      if (vErrors === null) {
        vErrors = [err14];
      } else {
        vErrors.push(err14);
      }
      errors++;
    }
    if (data.smart_unions === void 0) {
      const err15 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "smart_unions" }, message: "must have required property 'smart_unions'" };
      if (vErrors === null) {
        vErrors = [err15];
      } else {
        vErrors.push(err15);
      }
      errors++;
    }
    if (data.user_unions === void 0) {
      const err16 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "user_unions" }, message: "must have required property 'user_unions'" };
      if (vErrors === null) {
        vErrors = [err16];
      } else {
        vErrors.push(err16);
      }
      errors++;
    }
    if (data.components === void 0) {
      const err17 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "components" }, message: "must have required property 'components'" };
      if (vErrors === null) {
        vErrors = [err17];
      } else {
        vErrors.push(err17);
      }
      errors++;
    }
    if (data.nets === void 0) {
      const err18 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "nets" }, message: "must have required property 'nets'" };
      if (vErrors === null) {
        vErrors = [err18];
      } else {
        vErrors.push(err18);
      }
      errors++;
    }
    if (data.net_classes === void 0) {
      const err19 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "net_classes" }, message: "must have required property 'net_classes'" };
      if (vErrors === null) {
        vErrors = [err19];
      } else {
        vErrors.push(err19);
      }
      errors++;
    }
    if (data.differential_pairs === void 0) {
      const err20 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "differential_pairs" }, message: "must have required property 'differential_pairs'" };
      if (vErrors === null) {
        vErrors = [err20];
      } else {
        vErrors.push(err20);
      }
      errors++;
    }
    if (data.polygons === void 0) {
      const err21 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "polygons" }, message: "must have required property 'polygons'" };
      if (vErrors === null) {
        vErrors = [err21];
      } else {
        vErrors.push(err21);
      }
      errors++;
    }
    if (data.rules === void 0) {
      const err22 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "rules" }, message: "must have required property 'rules'" };
      if (vErrors === null) {
        vErrors = [err22];
      } else {
        vErrors.push(err22);
      }
      errors++;
    }
    if (data.dimensions === void 0) {
      const err23 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "dimensions" }, message: "must have required property 'dimensions'" };
      if (vErrors === null) {
        vErrors = [err23];
      } else {
        vErrors.push(err23);
      }
      errors++;
    }
    if (data.extended_primitive_information === void 0) {
      const err24 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "extended_primitive_information" }, message: "must have required property 'extended_primitive_information'" };
      if (vErrors === null) {
        vErrors = [err24];
      } else {
        vErrors.push(err24);
      }
      errors++;
    }
    if (data.custom_shapes === void 0) {
      const err25 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "custom_shapes" }, message: "must have required property 'custom_shapes'" };
      if (vErrors === null) {
        vErrors = [err25];
      } else {
        vErrors.push(err25);
      }
      errors++;
    }
    if (data.via_structures === void 0) {
      const err26 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "via_structures" }, message: "must have required property 'via_structures'" };
      if (vErrors === null) {
        vErrors = [err26];
      } else {
        vErrors.push(err26);
      }
      errors++;
    }
    if (data.via_structure_links === void 0) {
      const err27 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "via_structure_links" }, message: "must have required property 'via_structure_links'" };
      if (vErrors === null) {
        vErrors = [err27];
      } else {
        vErrors.push(err27);
      }
      errors++;
    }
    if (data.board_regions === void 0) {
      const err28 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "board_regions" }, message: "must have required property 'board_regions'" };
      if (vErrors === null) {
        vErrors = [err28];
      } else {
        vErrors.push(err28);
      }
      errors++;
    }
    if (data.shapebased_component_bodies === void 0) {
      const err29 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "shapebased_component_bodies" }, message: "must have required property 'shapebased_component_bodies'" };
      if (vErrors === null) {
        vErrors = [err29];
      } else {
        vErrors.push(err29);
      }
      errors++;
    }
    if (data.embedded_fonts === void 0) {
      const err30 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "embedded_fonts" }, message: "must have required property 'embedded_fonts'" };
      if (vErrors === null) {
        vErrors = [err30];
      } else {
        vErrors.push(err30);
      }
      errors++;
    }
    if (data.embedded_models === void 0) {
      const err31 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "embedded_models" }, message: "must have required property 'embedded_models'" };
      if (vErrors === null) {
        vErrors = [err31];
      } else {
        vErrors.push(err31);
      }
      errors++;
    }
    if (data.pads !== void 0) {
      let data0 = data.pads;
      if (Array.isArray(data0)) {
        const len0 = data0.length;
        for (let i0 = 0; i0 < len0; i0++) {
          const _errs5 = errors;
          let valid4 = false;
          var _valid0 = true;
          valid4 = valid4 || _valid0;
          if (!valid4) {
            const err32 = { instancePath: instancePath + "/pads/" + i0, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err32];
            } else {
              vErrors.push(err32);
            }
            errors++;
          } else {
            errors = _errs5;
            if (vErrors !== null) {
              if (_errs5) {
                vErrors.length = _errs5;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err33 = { instancePath: instancePath + "/pads", schemaPath: "#/properties/pads/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
    }
    if (data.vias !== void 0) {
      let data2 = data.vias;
      if (Array.isArray(data2)) {
        const len1 = data2.length;
        for (let i1 = 0; i1 < len1; i1++) {
          const _errs10 = errors;
          let valid8 = false;
          var _valid1 = true;
          valid8 = valid8 || _valid1;
          if (!valid8) {
            const err34 = { instancePath: instancePath + "/vias/" + i1, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err34];
            } else {
              vErrors.push(err34);
            }
            errors++;
          } else {
            errors = _errs10;
            if (vErrors !== null) {
              if (_errs10) {
                vErrors.length = _errs10;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err35 = { instancePath: instancePath + "/vias", schemaPath: "#/properties/vias/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err35];
        } else {
          vErrors.push(err35);
        }
        errors++;
      }
    }
    if (data.tracks !== void 0) {
      let data4 = data.tracks;
      if (Array.isArray(data4)) {
        const len2 = data4.length;
        for (let i2 = 0; i2 < len2; i2++) {
          const _errs15 = errors;
          let valid12 = false;
          var _valid2 = true;
          valid12 = valid12 || _valid2;
          if (!valid12) {
            const err36 = { instancePath: instancePath + "/tracks/" + i2, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err36];
            } else {
              vErrors.push(err36);
            }
            errors++;
          } else {
            errors = _errs15;
            if (vErrors !== null) {
              if (_errs15) {
                vErrors.length = _errs15;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err37 = { instancePath: instancePath + "/tracks", schemaPath: "#/properties/tracks/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err37];
        } else {
          vErrors.push(err37);
        }
        errors++;
      }
    }
    if (data.arcs !== void 0) {
      let data6 = data.arcs;
      if (Array.isArray(data6)) {
        const len3 = data6.length;
        for (let i3 = 0; i3 < len3; i3++) {
          const _errs20 = errors;
          let valid16 = false;
          var _valid3 = true;
          valid16 = valid16 || _valid3;
          if (!valid16) {
            const err38 = { instancePath: instancePath + "/arcs/" + i3, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err38];
            } else {
              vErrors.push(err38);
            }
            errors++;
          } else {
            errors = _errs20;
            if (vErrors !== null) {
              if (_errs20) {
                vErrors.length = _errs20;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err39 = { instancePath: instancePath + "/arcs", schemaPath: "#/properties/arcs/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err39];
        } else {
          vErrors.push(err39);
        }
        errors++;
      }
    }
    if (data.texts !== void 0) {
      let data8 = data.texts;
      if (Array.isArray(data8)) {
        const len4 = data8.length;
        for (let i4 = 0; i4 < len4; i4++) {
          const _errs25 = errors;
          let valid20 = false;
          var _valid4 = true;
          valid20 = valid20 || _valid4;
          if (!valid20) {
            const err40 = { instancePath: instancePath + "/texts/" + i4, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err40];
            } else {
              vErrors.push(err40);
            }
            errors++;
          } else {
            errors = _errs25;
            if (vErrors !== null) {
              if (_errs25) {
                vErrors.length = _errs25;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err41 = { instancePath: instancePath + "/texts", schemaPath: "#/properties/texts/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err41];
        } else {
          vErrors.push(err41);
        }
        errors++;
      }
    }
    if (data.fills !== void 0) {
      let data10 = data.fills;
      if (Array.isArray(data10)) {
        const len5 = data10.length;
        for (let i5 = 0; i5 < len5; i5++) {
          const _errs30 = errors;
          let valid24 = false;
          var _valid5 = true;
          valid24 = valid24 || _valid5;
          if (!valid24) {
            const err42 = { instancePath: instancePath + "/fills/" + i5, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err42];
            } else {
              vErrors.push(err42);
            }
            errors++;
          } else {
            errors = _errs30;
            if (vErrors !== null) {
              if (_errs30) {
                vErrors.length = _errs30;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err43 = { instancePath: instancePath + "/fills", schemaPath: "#/properties/fills/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err43];
        } else {
          vErrors.push(err43);
        }
        errors++;
      }
    }
    if (data.regions !== void 0) {
      let data12 = data.regions;
      if (Array.isArray(data12)) {
        const len6 = data12.length;
        for (let i6 = 0; i6 < len6; i6++) {
          const _errs35 = errors;
          let valid28 = false;
          var _valid6 = true;
          valid28 = valid28 || _valid6;
          if (!valid28) {
            const err44 = { instancePath: instancePath + "/regions/" + i6, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err44];
            } else {
              vErrors.push(err44);
            }
            errors++;
          } else {
            errors = _errs35;
            if (vErrors !== null) {
              if (_errs35) {
                vErrors.length = _errs35;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err45 = { instancePath: instancePath + "/regions", schemaPath: "#/properties/regions/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err45];
        } else {
          vErrors.push(err45);
        }
        errors++;
      }
    }
    if (data.shapebased_regions !== void 0) {
      let data14 = data.shapebased_regions;
      if (Array.isArray(data14)) {
        const len7 = data14.length;
        for (let i7 = 0; i7 < len7; i7++) {
          const _errs40 = errors;
          let valid32 = false;
          var _valid7 = true;
          valid32 = valid32 || _valid7;
          if (!valid32) {
            const err46 = { instancePath: instancePath + "/shapebased_regions/" + i7, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err46];
            } else {
              vErrors.push(err46);
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
      } else {
        const err47 = { instancePath: instancePath + "/shapebased_regions", schemaPath: "#/properties/shapebased_regions/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err47];
        } else {
          vErrors.push(err47);
        }
        errors++;
      }
    }
    if (data.component_bodies !== void 0) {
      let data16 = data.component_bodies;
      if (Array.isArray(data16)) {
        const len8 = data16.length;
        for (let i8 = 0; i8 < len8; i8++) {
          const _errs45 = errors;
          let valid36 = false;
          var _valid8 = true;
          valid36 = valid36 || _valid8;
          if (!valid36) {
            const err48 = { instancePath: instancePath + "/component_bodies/" + i8, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err48];
            } else {
              vErrors.push(err48);
            }
            errors++;
          } else {
            errors = _errs45;
            if (vErrors !== null) {
              if (_errs45) {
                vErrors.length = _errs45;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err49 = { instancePath: instancePath + "/component_bodies", schemaPath: "#/properties/component_bodies/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err49];
        } else {
          vErrors.push(err49);
        }
        errors++;
      }
    }
    if (data.models !== void 0) {
      let data18 = data.models;
      if (Array.isArray(data18)) {
        const len9 = data18.length;
        for (let i9 = 0; i9 < len9; i9++) {
          const _errs50 = errors;
          let valid40 = false;
          var _valid9 = true;
          valid40 = valid40 || _valid9;
          if (!valid40) {
            const err50 = { instancePath: instancePath + "/models/" + i9, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err50];
            } else {
              vErrors.push(err50);
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
      } else {
        const err51 = { instancePath: instancePath + "/models", schemaPath: "#/properties/models/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err51];
        } else {
          vErrors.push(err51);
        }
        errors++;
      }
    }
    if (data.format !== void 0) {
      let data20 = data.format;
      if (typeof data20 !== "string") {
        const err52 = { instancePath: instancePath + "/format", schemaPath: "#/properties/format/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err52];
        } else {
          vErrors.push(err52);
        }
        errors++;
      }
      if ("altium_monkey.pcbdoc.structural.a0" !== data20) {
        const err53 = { instancePath: instancePath + "/format", schemaPath: "#/properties/format/const", keyword: "const", params: { allowedValue: "altium_monkey.pcbdoc.structural.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err53];
        } else {
          vErrors.push(err53);
        }
        errors++;
      }
    }
    if (data.counts !== void 0) {
      if (!validate31(data.counts, { instancePath: instancePath + "/counts", parentData: data, parentDataProperty: "counts", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate31.errors : vErrors.concat(validate31.errors);
        errors = vErrors.length;
      }
    }
    if (data.raw_streams !== void 0) {
      let data22 = data.raw_streams;
      if (Array.isArray(data22)) {
        const len10 = data22.length;
        for (let i10 = 0; i10 < len10; i10++) {
          if (!validate33(data22[i10], { instancePath: instancePath + "/raw_streams/" + i10, parentData: data22, parentDataProperty: i10, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate33.errors : vErrors.concat(validate33.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err54 = { instancePath: instancePath + "/raw_streams", schemaPath: "#/properties/raw_streams/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err54];
        } else {
          vErrors.push(err54);
        }
        errors++;
      }
    }
    if (data.board !== void 0) {
      const _errs59 = errors;
      let valid44 = false;
      var _valid10 = true;
      valid44 = valid44 || _valid10;
      if (!valid44) {
        const err55 = { instancePath: instancePath + "/board", schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err55];
        } else {
          vErrors.push(err55);
        }
        errors++;
      } else {
        errors = _errs59;
        if (vErrors !== null) {
          if (_errs59) {
            vErrors.length = _errs59;
          } else {
            vErrors = null;
          }
        }
      }
    }
    if (data.union_name_records !== void 0) {
      let data25 = data.union_name_records;
      if (Array.isArray(data25)) {
        const len11 = data25.length;
        for (let i11 = 0; i11 < len11; i11++) {
          const _errs64 = errors;
          let valid48 = false;
          var _valid11 = true;
          valid48 = valid48 || _valid11;
          if (!valid48) {
            const err56 = { instancePath: instancePath + "/union_name_records/" + i11, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err56];
            } else {
              vErrors.push(err56);
            }
            errors++;
          } else {
            errors = _errs64;
            if (vErrors !== null) {
              if (_errs64) {
                vErrors.length = _errs64;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err57 = { instancePath: instancePath + "/union_name_records", schemaPath: "#/properties/union_name_records/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err57];
        } else {
          vErrors.push(err57);
        }
        errors++;
      }
    }
    if (data.smart_unions !== void 0) {
      let data27 = data.smart_unions;
      if (Array.isArray(data27)) {
        const len12 = data27.length;
        for (let i12 = 0; i12 < len12; i12++) {
          const _errs69 = errors;
          let valid52 = false;
          var _valid12 = true;
          valid52 = valid52 || _valid12;
          if (!valid52) {
            const err58 = { instancePath: instancePath + "/smart_unions/" + i12, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err58];
            } else {
              vErrors.push(err58);
            }
            errors++;
          } else {
            errors = _errs69;
            if (vErrors !== null) {
              if (_errs69) {
                vErrors.length = _errs69;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err59 = { instancePath: instancePath + "/smart_unions", schemaPath: "#/properties/smart_unions/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err59];
        } else {
          vErrors.push(err59);
        }
        errors++;
      }
    }
    if (data.user_unions !== void 0) {
      let data29 = data.user_unions;
      if (Array.isArray(data29)) {
        const len13 = data29.length;
        for (let i13 = 0; i13 < len13; i13++) {
          let data30 = data29[i13];
          const _errs73 = errors;
          let valid55 = false;
          const _errs74 = errors;
          if (!validate35(data30, { instancePath: instancePath + "/user_unions/" + i13, parentData: data29, parentDataProperty: i13, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate35.errors : vErrors.concat(validate35.errors);
            errors = vErrors.length;
          }
          var _valid13 = _errs74 === errors;
          valid55 = valid55 || _valid13;
          if (_valid13) {
            var props0 = true;
          }
          const _errs75 = errors;
          if (data30 && typeof data30 == "object" && !Array.isArray(data30)) {
            if (data30.error === void 0) {
              const err60 = { instancePath: instancePath + "/user_unions/" + i13, schemaPath: "#/$defs/UnionError/required", keyword: "required", params: { missingProperty: "error" }, message: "must have required property 'error'" };
              if (vErrors === null) {
                vErrors = [err60];
              } else {
                vErrors.push(err60);
              }
              errors++;
            }
            if (data30.error !== void 0) {
              if (typeof data30.error !== "string") {
                const err61 = { instancePath: instancePath + "/user_unions/" + i13 + "/error", schemaPath: "#/$defs/UnionError/properties/error/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err61];
                } else {
                  vErrors.push(err61);
                }
                errors++;
              }
            }
            for (const key0 in data30) {
              if (key0 !== "error") {
                const err62 = { instancePath: instancePath + "/user_unions/" + i13 + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/UnionError/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err62];
                } else {
                  vErrors.push(err62);
                }
                errors++;
              }
            }
          } else {
            const err63 = { instancePath: instancePath + "/user_unions/" + i13, schemaPath: "#/$defs/UnionError/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err63];
            } else {
              vErrors.push(err63);
            }
            errors++;
          }
          var _valid13 = _errs75 === errors;
          valid55 = valid55 || _valid13;
          if (_valid13) {
            if (props0 !== true) {
              props0 = true;
            }
          }
          if (!valid55) {
            const err64 = { instancePath: instancePath + "/user_unions/" + i13, schemaPath: "#/properties/user_unions/items/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err64];
            } else {
              vErrors.push(err64);
            }
            errors++;
          } else {
            errors = _errs73;
            if (vErrors !== null) {
              if (_errs73) {
                vErrors.length = _errs73;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err65 = { instancePath: instancePath + "/user_unions", schemaPath: "#/properties/user_unions/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err65];
        } else {
          vErrors.push(err65);
        }
        errors++;
      }
    }
    if (data.components !== void 0) {
      let data33 = data.components;
      if (Array.isArray(data33)) {
        const len14 = data33.length;
        for (let i14 = 0; i14 < len14; i14++) {
          const _errs87 = errors;
          let valid62 = false;
          var _valid14 = true;
          valid62 = valid62 || _valid14;
          if (!valid62) {
            const err66 = { instancePath: instancePath + "/components/" + i14, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err66];
            } else {
              vErrors.push(err66);
            }
            errors++;
          } else {
            errors = _errs87;
            if (vErrors !== null) {
              if (_errs87) {
                vErrors.length = _errs87;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err67 = { instancePath: instancePath + "/components", schemaPath: "#/properties/components/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err67];
        } else {
          vErrors.push(err67);
        }
        errors++;
      }
    }
    if (data.nets !== void 0) {
      let data35 = data.nets;
      if (Array.isArray(data35)) {
        const len15 = data35.length;
        for (let i15 = 0; i15 < len15; i15++) {
          const _errs92 = errors;
          let valid66 = false;
          var _valid15 = true;
          valid66 = valid66 || _valid15;
          if (!valid66) {
            const err68 = { instancePath: instancePath + "/nets/" + i15, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err68];
            } else {
              vErrors.push(err68);
            }
            errors++;
          } else {
            errors = _errs92;
            if (vErrors !== null) {
              if (_errs92) {
                vErrors.length = _errs92;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err69 = { instancePath: instancePath + "/nets", schemaPath: "#/properties/nets/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err69];
        } else {
          vErrors.push(err69);
        }
        errors++;
      }
    }
    if (data.net_classes !== void 0) {
      let data37 = data.net_classes;
      if (Array.isArray(data37)) {
        const len16 = data37.length;
        for (let i16 = 0; i16 < len16; i16++) {
          const _errs97 = errors;
          let valid70 = false;
          var _valid16 = true;
          valid70 = valid70 || _valid16;
          if (!valid70) {
            const err70 = { instancePath: instancePath + "/net_classes/" + i16, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err70];
            } else {
              vErrors.push(err70);
            }
            errors++;
          } else {
            errors = _errs97;
            if (vErrors !== null) {
              if (_errs97) {
                vErrors.length = _errs97;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err71 = { instancePath: instancePath + "/net_classes", schemaPath: "#/properties/net_classes/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err71];
        } else {
          vErrors.push(err71);
        }
        errors++;
      }
    }
    if (data.differential_pairs !== void 0) {
      let data39 = data.differential_pairs;
      if (Array.isArray(data39)) {
        const len17 = data39.length;
        for (let i17 = 0; i17 < len17; i17++) {
          const _errs102 = errors;
          let valid74 = false;
          var _valid17 = true;
          valid74 = valid74 || _valid17;
          if (!valid74) {
            const err72 = { instancePath: instancePath + "/differential_pairs/" + i17, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err72];
            } else {
              vErrors.push(err72);
            }
            errors++;
          } else {
            errors = _errs102;
            if (vErrors !== null) {
              if (_errs102) {
                vErrors.length = _errs102;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err73 = { instancePath: instancePath + "/differential_pairs", schemaPath: "#/properties/differential_pairs/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err73];
        } else {
          vErrors.push(err73);
        }
        errors++;
      }
    }
    if (data.polygons !== void 0) {
      let data41 = data.polygons;
      if (Array.isArray(data41)) {
        const len18 = data41.length;
        for (let i18 = 0; i18 < len18; i18++) {
          const _errs107 = errors;
          let valid78 = false;
          var _valid18 = true;
          valid78 = valid78 || _valid18;
          if (!valid78) {
            const err74 = { instancePath: instancePath + "/polygons/" + i18, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err74];
            } else {
              vErrors.push(err74);
            }
            errors++;
          } else {
            errors = _errs107;
            if (vErrors !== null) {
              if (_errs107) {
                vErrors.length = _errs107;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err75 = { instancePath: instancePath + "/polygons", schemaPath: "#/properties/polygons/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err75];
        } else {
          vErrors.push(err75);
        }
        errors++;
      }
    }
    if (data.rules !== void 0) {
      let data43 = data.rules;
      if (Array.isArray(data43)) {
        const len19 = data43.length;
        for (let i19 = 0; i19 < len19; i19++) {
          const _errs112 = errors;
          let valid82 = false;
          var _valid19 = true;
          valid82 = valid82 || _valid19;
          if (!valid82) {
            const err76 = { instancePath: instancePath + "/rules/" + i19, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err76];
            } else {
              vErrors.push(err76);
            }
            errors++;
          } else {
            errors = _errs112;
            if (vErrors !== null) {
              if (_errs112) {
                vErrors.length = _errs112;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err77 = { instancePath: instancePath + "/rules", schemaPath: "#/properties/rules/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err77];
        } else {
          vErrors.push(err77);
        }
        errors++;
      }
    }
    if (data.dimensions !== void 0) {
      let data45 = data.dimensions;
      if (Array.isArray(data45)) {
        const len20 = data45.length;
        for (let i20 = 0; i20 < len20; i20++) {
          const _errs117 = errors;
          let valid86 = false;
          var _valid20 = true;
          valid86 = valid86 || _valid20;
          if (!valid86) {
            const err78 = { instancePath: instancePath + "/dimensions/" + i20, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err78];
            } else {
              vErrors.push(err78);
            }
            errors++;
          } else {
            errors = _errs117;
            if (vErrors !== null) {
              if (_errs117) {
                vErrors.length = _errs117;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err79 = { instancePath: instancePath + "/dimensions", schemaPath: "#/properties/dimensions/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err79];
        } else {
          vErrors.push(err79);
        }
        errors++;
      }
    }
    if (data.extended_primitive_information !== void 0) {
      let data47 = data.extended_primitive_information;
      if (Array.isArray(data47)) {
        const len21 = data47.length;
        for (let i21 = 0; i21 < len21; i21++) {
          const _errs122 = errors;
          let valid90 = false;
          var _valid21 = true;
          valid90 = valid90 || _valid21;
          if (!valid90) {
            const err80 = { instancePath: instancePath + "/extended_primitive_information/" + i21, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err80];
            } else {
              vErrors.push(err80);
            }
            errors++;
          } else {
            errors = _errs122;
            if (vErrors !== null) {
              if (_errs122) {
                vErrors.length = _errs122;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err81 = { instancePath: instancePath + "/extended_primitive_information", schemaPath: "#/properties/extended_primitive_information/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err81];
        } else {
          vErrors.push(err81);
        }
        errors++;
      }
    }
    if (data.custom_shapes !== void 0) {
      let data49 = data.custom_shapes;
      if (Array.isArray(data49)) {
        const len22 = data49.length;
        for (let i22 = 0; i22 < len22; i22++) {
          const _errs127 = errors;
          let valid94 = false;
          var _valid22 = true;
          valid94 = valid94 || _valid22;
          if (!valid94) {
            const err82 = { instancePath: instancePath + "/custom_shapes/" + i22, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err82];
            } else {
              vErrors.push(err82);
            }
            errors++;
          } else {
            errors = _errs127;
            if (vErrors !== null) {
              if (_errs127) {
                vErrors.length = _errs127;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err83 = { instancePath: instancePath + "/custom_shapes", schemaPath: "#/properties/custom_shapes/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err83];
        } else {
          vErrors.push(err83);
        }
        errors++;
      }
    }
    if (data.via_structures !== void 0) {
      let data51 = data.via_structures;
      if (Array.isArray(data51)) {
        const len23 = data51.length;
        for (let i23 = 0; i23 < len23; i23++) {
          const _errs132 = errors;
          let valid98 = false;
          var _valid23 = true;
          valid98 = valid98 || _valid23;
          if (!valid98) {
            const err84 = { instancePath: instancePath + "/via_structures/" + i23, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err84];
            } else {
              vErrors.push(err84);
            }
            errors++;
          } else {
            errors = _errs132;
            if (vErrors !== null) {
              if (_errs132) {
                vErrors.length = _errs132;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err85 = { instancePath: instancePath + "/via_structures", schemaPath: "#/properties/via_structures/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err85];
        } else {
          vErrors.push(err85);
        }
        errors++;
      }
    }
    if (data.via_structure_links !== void 0) {
      let data53 = data.via_structure_links;
      if (Array.isArray(data53)) {
        const len24 = data53.length;
        for (let i24 = 0; i24 < len24; i24++) {
          const _errs137 = errors;
          let valid102 = false;
          var _valid24 = true;
          valid102 = valid102 || _valid24;
          if (!valid102) {
            const err86 = { instancePath: instancePath + "/via_structure_links/" + i24, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err86];
            } else {
              vErrors.push(err86);
            }
            errors++;
          } else {
            errors = _errs137;
            if (vErrors !== null) {
              if (_errs137) {
                vErrors.length = _errs137;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err87 = { instancePath: instancePath + "/via_structure_links", schemaPath: "#/properties/via_structure_links/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err87];
        } else {
          vErrors.push(err87);
        }
        errors++;
      }
    }
    if (data.board_regions !== void 0) {
      let data55 = data.board_regions;
      if (Array.isArray(data55)) {
        const len25 = data55.length;
        for (let i25 = 0; i25 < len25; i25++) {
          const _errs142 = errors;
          let valid106 = false;
          var _valid25 = true;
          valid106 = valid106 || _valid25;
          if (!valid106) {
            const err88 = { instancePath: instancePath + "/board_regions/" + i25, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err88];
            } else {
              vErrors.push(err88);
            }
            errors++;
          } else {
            errors = _errs142;
            if (vErrors !== null) {
              if (_errs142) {
                vErrors.length = _errs142;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err89 = { instancePath: instancePath + "/board_regions", schemaPath: "#/properties/board_regions/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err89];
        } else {
          vErrors.push(err89);
        }
        errors++;
      }
    }
    if (data.shapebased_component_bodies !== void 0) {
      let data57 = data.shapebased_component_bodies;
      if (Array.isArray(data57)) {
        const len26 = data57.length;
        for (let i26 = 0; i26 < len26; i26++) {
          const _errs147 = errors;
          let valid110 = false;
          var _valid26 = true;
          valid110 = valid110 || _valid26;
          if (!valid110) {
            const err90 = { instancePath: instancePath + "/shapebased_component_bodies/" + i26, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err90];
            } else {
              vErrors.push(err90);
            }
            errors++;
          } else {
            errors = _errs147;
            if (vErrors !== null) {
              if (_errs147) {
                vErrors.length = _errs147;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err91 = { instancePath: instancePath + "/shapebased_component_bodies", schemaPath: "#/properties/shapebased_component_bodies/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err91];
        } else {
          vErrors.push(err91);
        }
        errors++;
      }
    }
    if (data.embedded_fonts !== void 0) {
      let data59 = data.embedded_fonts;
      if (Array.isArray(data59)) {
        const len27 = data59.length;
        for (let i27 = 0; i27 < len27; i27++) {
          const _errs152 = errors;
          let valid114 = false;
          var _valid27 = true;
          valid114 = valid114 || _valid27;
          if (!valid114) {
            const err92 = { instancePath: instancePath + "/embedded_fonts/" + i27, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err92];
            } else {
              vErrors.push(err92);
            }
            errors++;
          } else {
            errors = _errs152;
            if (vErrors !== null) {
              if (_errs152) {
                vErrors.length = _errs152;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err93 = { instancePath: instancePath + "/embedded_fonts", schemaPath: "#/properties/embedded_fonts/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err93];
        } else {
          vErrors.push(err93);
        }
        errors++;
      }
    }
    if (data.embedded_models !== void 0) {
      let data61 = data.embedded_models;
      if (Array.isArray(data61)) {
        const len28 = data61.length;
        for (let i28 = 0; i28 < len28; i28++) {
          const _errs157 = errors;
          let valid118 = false;
          var _valid28 = true;
          valid118 = valid118 || _valid28;
          if (!valid118) {
            const err94 = { instancePath: instancePath + "/embedded_models/" + i28, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err94];
            } else {
              vErrors.push(err94);
            }
            errors++;
          } else {
            errors = _errs157;
            if (vErrors !== null) {
              if (_errs157) {
                vErrors.length = _errs157;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err95 = { instancePath: instancePath + "/embedded_models", schemaPath: "#/properties/embedded_models/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err95];
        } else {
          vErrors.push(err95);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "pads" && key1 !== "vias" && key1 !== "tracks" && key1 !== "arcs" && key1 !== "texts" && key1 !== "fills" && key1 !== "regions" && key1 !== "shapebased_regions" && key1 !== "component_bodies" && key1 !== "models" && key1 !== "format" && key1 !== "counts" && key1 !== "raw_streams" && key1 !== "board" && key1 !== "union_name_records" && key1 !== "smart_unions" && key1 !== "user_unions" && key1 !== "components" && key1 !== "nets" && key1 !== "net_classes" && key1 !== "differential_pairs" && key1 !== "polygons" && key1 !== "rules" && key1 !== "dimensions" && key1 !== "extended_primitive_information" && key1 !== "custom_shapes" && key1 !== "via_structures" && key1 !== "via_structure_links" && key1 !== "board_regions" && key1 !== "shapebased_component_bodies" && key1 !== "embedded_fonts" && key1 !== "embedded_models") {
        const err96 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err96];
        } else {
          vErrors.push(err96);
        }
        errors++;
      }
    }
  } else {
    const err97 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err97];
    } else {
      vErrors.push(err97);
    }
    errors++;
  }
  validate30.errors = vErrors;
  return errors === 0;
}
validate30.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate29(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate29.evaluated;
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
    if (data.kind === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "kind" }, message: "must have required property 'kind'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.document === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "document" }, message: "must have required property 'document'" };
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
      if ("altium_cruncher.json_dump.a0" !== data0) {
        const err4 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.json_dump.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.kind !== void 0) {
      let data1 = data.kind;
      if (typeof data1 !== "string") {
        const err5 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      if ("PcbDoc" !== data1) {
        const err6 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/const", keyword: "const", params: { allowedValue: "PcbDoc" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.document !== void 0) {
      if (!validate30(data.document, { instancePath: instancePath + "/document", parentData: data, parentDataProperty: "document", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate30.errors : vErrors.concat(validate30.errors);
        errors = vErrors.length;
      }
    }
    for (const key0 in data) {
      if (key0 !== "schema" && key0 !== "kind" && key0 !== "document") {
        const err7 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
  } else {
    const err8 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err8];
    } else {
      vErrors.push(err8);
    }
    errors++;
  }
  validate29.errors = vErrors;
  return errors === 0;
}
validate29.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate45(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate45.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.pads === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "pads" }, message: "must have required property 'pads'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.vias === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "vias" }, message: "must have required property 'vias'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.tracks === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "tracks" }, message: "must have required property 'tracks'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.arcs === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "arcs" }, message: "must have required property 'arcs'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.texts === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "texts" }, message: "must have required property 'texts'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.fills === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "fills" }, message: "must have required property 'fills'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.regions === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "regions" }, message: "must have required property 'regions'" };
      if (vErrors === null) {
        vErrors = [err6];
      } else {
        vErrors.push(err6);
      }
      errors++;
    }
    if (data.shapebased_regions === void 0) {
      const err7 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "shapebased_regions" }, message: "must have required property 'shapebased_regions'" };
      if (vErrors === null) {
        vErrors = [err7];
      } else {
        vErrors.push(err7);
      }
      errors++;
    }
    if (data.component_bodies === void 0) {
      const err8 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "component_bodies" }, message: "must have required property 'component_bodies'" };
      if (vErrors === null) {
        vErrors = [err8];
      } else {
        vErrors.push(err8);
      }
      errors++;
    }
    if (data.models === void 0) {
      const err9 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "models" }, message: "must have required property 'models'" };
      if (vErrors === null) {
        vErrors = [err9];
      } else {
        vErrors.push(err9);
      }
      errors++;
    }
    if (data.name === void 0) {
      const err10 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
      if (vErrors === null) {
        vErrors = [err10];
      } else {
        vErrors.push(err10);
      }
      errors++;
    }
    if (data.counts === void 0) {
      const err11 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "counts" }, message: "must have required property 'counts'" };
      if (vErrors === null) {
        vErrors = [err11];
      } else {
        vErrors.push(err11);
      }
      errors++;
    }
    if (data.pads !== void 0) {
      let data0 = data.pads;
      if (Array.isArray(data0)) {
        const len0 = data0.length;
        for (let i0 = 0; i0 < len0; i0++) {
          const _errs5 = errors;
          let valid4 = false;
          var _valid0 = true;
          valid4 = valid4 || _valid0;
          if (!valid4) {
            const err12 = { instancePath: instancePath + "/pads/" + i0, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err12];
            } else {
              vErrors.push(err12);
            }
            errors++;
          } else {
            errors = _errs5;
            if (vErrors !== null) {
              if (_errs5) {
                vErrors.length = _errs5;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err13 = { instancePath: instancePath + "/pads", schemaPath: "#/properties/pads/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.vias !== void 0) {
      let data2 = data.vias;
      if (Array.isArray(data2)) {
        const len1 = data2.length;
        for (let i1 = 0; i1 < len1; i1++) {
          const _errs10 = errors;
          let valid8 = false;
          var _valid1 = true;
          valid8 = valid8 || _valid1;
          if (!valid8) {
            const err14 = { instancePath: instancePath + "/vias/" + i1, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err14];
            } else {
              vErrors.push(err14);
            }
            errors++;
          } else {
            errors = _errs10;
            if (vErrors !== null) {
              if (_errs10) {
                vErrors.length = _errs10;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err15 = { instancePath: instancePath + "/vias", schemaPath: "#/properties/vias/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
    }
    if (data.tracks !== void 0) {
      let data4 = data.tracks;
      if (Array.isArray(data4)) {
        const len2 = data4.length;
        for (let i2 = 0; i2 < len2; i2++) {
          const _errs15 = errors;
          let valid12 = false;
          var _valid2 = true;
          valid12 = valid12 || _valid2;
          if (!valid12) {
            const err16 = { instancePath: instancePath + "/tracks/" + i2, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err16];
            } else {
              vErrors.push(err16);
            }
            errors++;
          } else {
            errors = _errs15;
            if (vErrors !== null) {
              if (_errs15) {
                vErrors.length = _errs15;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err17 = { instancePath: instancePath + "/tracks", schemaPath: "#/properties/tracks/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
    }
    if (data.arcs !== void 0) {
      let data6 = data.arcs;
      if (Array.isArray(data6)) {
        const len3 = data6.length;
        for (let i3 = 0; i3 < len3; i3++) {
          const _errs20 = errors;
          let valid16 = false;
          var _valid3 = true;
          valid16 = valid16 || _valid3;
          if (!valid16) {
            const err18 = { instancePath: instancePath + "/arcs/" + i3, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err18];
            } else {
              vErrors.push(err18);
            }
            errors++;
          } else {
            errors = _errs20;
            if (vErrors !== null) {
              if (_errs20) {
                vErrors.length = _errs20;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err19 = { instancePath: instancePath + "/arcs", schemaPath: "#/properties/arcs/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
    }
    if (data.texts !== void 0) {
      let data8 = data.texts;
      if (Array.isArray(data8)) {
        const len4 = data8.length;
        for (let i4 = 0; i4 < len4; i4++) {
          const _errs25 = errors;
          let valid20 = false;
          var _valid4 = true;
          valid20 = valid20 || _valid4;
          if (!valid20) {
            const err20 = { instancePath: instancePath + "/texts/" + i4, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err20];
            } else {
              vErrors.push(err20);
            }
            errors++;
          } else {
            errors = _errs25;
            if (vErrors !== null) {
              if (_errs25) {
                vErrors.length = _errs25;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err21 = { instancePath: instancePath + "/texts", schemaPath: "#/properties/texts/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err21];
        } else {
          vErrors.push(err21);
        }
        errors++;
      }
    }
    if (data.fills !== void 0) {
      let data10 = data.fills;
      if (Array.isArray(data10)) {
        const len5 = data10.length;
        for (let i5 = 0; i5 < len5; i5++) {
          const _errs30 = errors;
          let valid24 = false;
          var _valid5 = true;
          valid24 = valid24 || _valid5;
          if (!valid24) {
            const err22 = { instancePath: instancePath + "/fills/" + i5, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err22];
            } else {
              vErrors.push(err22);
            }
            errors++;
          } else {
            errors = _errs30;
            if (vErrors !== null) {
              if (_errs30) {
                vErrors.length = _errs30;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err23 = { instancePath: instancePath + "/fills", schemaPath: "#/properties/fills/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
    }
    if (data.regions !== void 0) {
      let data12 = data.regions;
      if (Array.isArray(data12)) {
        const len6 = data12.length;
        for (let i6 = 0; i6 < len6; i6++) {
          const _errs35 = errors;
          let valid28 = false;
          var _valid6 = true;
          valid28 = valid28 || _valid6;
          if (!valid28) {
            const err24 = { instancePath: instancePath + "/regions/" + i6, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err24];
            } else {
              vErrors.push(err24);
            }
            errors++;
          } else {
            errors = _errs35;
            if (vErrors !== null) {
              if (_errs35) {
                vErrors.length = _errs35;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err25 = { instancePath: instancePath + "/regions", schemaPath: "#/properties/regions/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err25];
        } else {
          vErrors.push(err25);
        }
        errors++;
      }
    }
    if (data.shapebased_regions !== void 0) {
      let data14 = data.shapebased_regions;
      if (Array.isArray(data14)) {
        const len7 = data14.length;
        for (let i7 = 0; i7 < len7; i7++) {
          const _errs40 = errors;
          let valid32 = false;
          var _valid7 = true;
          valid32 = valid32 || _valid7;
          if (!valid32) {
            const err26 = { instancePath: instancePath + "/shapebased_regions/" + i7, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err26];
            } else {
              vErrors.push(err26);
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
      } else {
        const err27 = { instancePath: instancePath + "/shapebased_regions", schemaPath: "#/properties/shapebased_regions/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err27];
        } else {
          vErrors.push(err27);
        }
        errors++;
      }
    }
    if (data.component_bodies !== void 0) {
      let data16 = data.component_bodies;
      if (Array.isArray(data16)) {
        const len8 = data16.length;
        for (let i8 = 0; i8 < len8; i8++) {
          const _errs45 = errors;
          let valid36 = false;
          var _valid8 = true;
          valid36 = valid36 || _valid8;
          if (!valid36) {
            const err28 = { instancePath: instancePath + "/component_bodies/" + i8, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err28];
            } else {
              vErrors.push(err28);
            }
            errors++;
          } else {
            errors = _errs45;
            if (vErrors !== null) {
              if (_errs45) {
                vErrors.length = _errs45;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err29 = { instancePath: instancePath + "/component_bodies", schemaPath: "#/properties/component_bodies/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      }
    }
    if (data.models !== void 0) {
      let data18 = data.models;
      if (Array.isArray(data18)) {
        const len9 = data18.length;
        for (let i9 = 0; i9 < len9; i9++) {
          const _errs50 = errors;
          let valid40 = false;
          var _valid9 = true;
          valid40 = valid40 || _valid9;
          if (!valid40) {
            const err30 = { instancePath: instancePath + "/models/" + i9, schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err30];
            } else {
              vErrors.push(err30);
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
      } else {
        const err31 = { instancePath: instancePath + "/models", schemaPath: "#/properties/models/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err31];
        } else {
          vErrors.push(err31);
        }
        errors++;
      }
    }
    if (data.name !== void 0) {
      if (typeof data.name !== "string") {
        const err32 = { instancePath: instancePath + "/name", schemaPath: "#/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
        }
        errors++;
      }
    }
    if (data.counts !== void 0) {
      if (!validate31(data.counts, { instancePath: instancePath + "/counts", parentData: data, parentDataProperty: "counts", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate31.errors : vErrors.concat(validate31.errors);
        errors = vErrors.length;
      }
    }
    for (const key0 in data) {
      if (key0 !== "pads" && key0 !== "vias" && key0 !== "tracks" && key0 !== "arcs" && key0 !== "texts" && key0 !== "fills" && key0 !== "regions" && key0 !== "shapebased_regions" && key0 !== "component_bodies" && key0 !== "models" && key0 !== "name" && key0 !== "counts") {
        const err33 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err33];
        } else {
          vErrors.push(err33);
        }
        errors++;
      }
    }
  } else {
    const err34 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err34];
    } else {
      vErrors.push(err34);
    }
    errors++;
  }
  validate45.errors = vErrors;
  return errors === 0;
}
validate45.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate44(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate44.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.format === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "format" }, message: "must have required property 'format'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.footprint_count === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "footprint_count" }, message: "must have required property 'footprint_count'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.footprints === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "footprints" }, message: "must have required property 'footprints'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.models_3d === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "models_3d" }, message: "must have required property 'models_3d'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.raw_streams === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "raw_streams" }, message: "must have required property 'raw_streams'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.format !== void 0) {
      let data0 = data.format;
      if (typeof data0 !== "string") {
        const err5 = { instancePath: instancePath + "/format", schemaPath: "#/properties/format/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      if ("altium_monkey.pcblib.structural.a0" !== data0) {
        const err6 = { instancePath: instancePath + "/format", schemaPath: "#/properties/format/const", keyword: "const", params: { allowedValue: "altium_monkey.pcblib.structural.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.footprint_count !== void 0) {
      let data1 = data.footprint_count;
      if (!(typeof data1 == "number" && (!(data1 % 1) && !isNaN(data1)))) {
        const err7 = { instancePath: instancePath + "/footprint_count", schemaPath: "#/$defs/Count/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
      if (typeof data1 == "number") {
        if (data1 < 0 || isNaN(data1)) {
          const err8 = { instancePath: instancePath + "/footprint_count", schemaPath: "#/$defs/Count/minimum", keyword: "minimum", params: { comparison: ">=", limit: 0 }, message: "must be >= 0" };
          if (vErrors === null) {
            vErrors = [err8];
          } else {
            vErrors.push(err8);
          }
          errors++;
        }
      }
    }
    if (data.footprints !== void 0) {
      let data2 = data.footprints;
      if (Array.isArray(data2)) {
        const len0 = data2.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!validate45(data2[i0], { instancePath: instancePath + "/footprints/" + i0, parentData: data2, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate45.errors : vErrors.concat(validate45.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err9 = { instancePath: instancePath + "/footprints", schemaPath: "#/properties/footprints/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    if (data.models_3d !== void 0) {
      const _errs11 = errors;
      let valid5 = false;
      var _valid0 = true;
      valid5 = valid5 || _valid0;
      if (!valid5) {
        const err10 = { instancePath: instancePath + "/models_3d", schemaPath: "#/$defs/NativeValue/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
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
    if (data.raw_streams !== void 0) {
      let data5 = data.raw_streams;
      if (Array.isArray(data5)) {
        const len1 = data5.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (!validate33(data5[i1], { instancePath: instancePath + "/raw_streams/" + i1, parentData: data5, parentDataProperty: i1, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate33.errors : vErrors.concat(validate33.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err11 = { instancePath: instancePath + "/raw_streams", schemaPath: "#/properties/raw_streams/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
    }
    for (const key0 in data) {
      if (key0 !== "format" && key0 !== "footprint_count" && key0 !== "footprints" && key0 !== "models_3d" && key0 !== "raw_streams") {
        const err12 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
    }
  } else {
    const err13 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err13];
    } else {
      vErrors.push(err13);
    }
    errors++;
  }
  validate44.errors = vErrors;
  return errors === 0;
}
validate44.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate43(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate43.evaluated;
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
    if (data.kind === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "kind" }, message: "must have required property 'kind'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.document === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "document" }, message: "must have required property 'document'" };
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
      if ("altium_cruncher.json_dump.a0" !== data0) {
        const err4 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.json_dump.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.kind !== void 0) {
      let data1 = data.kind;
      if (typeof data1 !== "string") {
        const err5 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      if ("PcbLib" !== data1) {
        const err6 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/const", keyword: "const", params: { allowedValue: "PcbLib" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.document !== void 0) {
      if (!validate44(data.document, { instancePath: instancePath + "/document", parentData: data, parentDataProperty: "document", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate44.errors : vErrors.concat(validate44.errors);
        errors = vErrors.length;
      }
    }
    for (const key0 in data) {
      if (key0 !== "schema" && key0 !== "kind" && key0 !== "document") {
        const err7 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
  } else {
    const err8 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err8];
    } else {
      vErrors.push(err8);
    }
    errors++;
  }
  validate43.errors = vErrors;
  return errors === 0;
}
validate43.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
  if (!validate21(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs2 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    var props0 = true;
  }
  const _errs3 = errors;
  if (!validate25(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate25.errors : vErrors.concat(validate25.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs3 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs4 = errors;
  if (!validate29(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate29.errors : vErrors.concat(validate29.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs4 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  const _errs5 = errors;
  if (!validate43(data, { instancePath, parentData, parentDataProperty, rootData, dynamicAnchors })) {
    vErrors = vErrors === null ? validate43.errors : vErrors.concat(validate43.errors);
    errors = vErrors.length;
  }
  var _valid0 = _errs5 === errors;
  valid0 = valid0 || _valid0;
  if (_valid0) {
    if (props0 !== true) {
      props0 = true;
    }
  }
  if (!valid0) {
    const err0 = { instancePath, schemaPath: "#/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
    if (vErrors === null) {
      vErrors = [err0];
    } else {
      vErrors.push(err0);
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
