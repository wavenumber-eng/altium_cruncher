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
    if (data.installs === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "installs" }, message: "must have required property 'installs'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.schema !== void 0) {
      let data0 = data.schema;
      if (typeof data0 !== "string") {
        const err2 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err2];
        } else {
          vErrors.push(err2);
        }
        errors++;
      }
      if ("altium_cruncher.installs.a0" !== data0) {
        const err3 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.installs.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.installs !== void 0) {
      let data1 = data.installs;
      if (Array.isArray(data1)) {
        const len0 = data1.length;
        for (let i0 = 0; i0 < len0; i0++) {
          let data2 = data1[i0];
          if (data2 && typeof data2 == "object" && !Array.isArray(data2)) {
            if (data2.name === void 0) {
              const err4 = { instancePath: instancePath + "/installs/" + i0, schemaPath: "#/$defs/Install/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
              if (vErrors === null) {
                vErrors = [err4];
              } else {
                vErrors.push(err4);
              }
              errors++;
            }
            if (data2.label === void 0) {
              const err5 = { instancePath: instancePath + "/installs/" + i0, schemaPath: "#/$defs/Install/required", keyword: "required", params: { missingProperty: "label" }, message: "must have required property 'label'" };
              if (vErrors === null) {
                vErrors = [err5];
              } else {
                vErrors.push(err5);
              }
              errors++;
            }
            if (data2.major === void 0) {
              const err6 = { instancePath: instancePath + "/installs/" + i0, schemaPath: "#/$defs/Install/required", keyword: "required", params: { missingProperty: "major" }, message: "must have required property 'major'" };
              if (vErrors === null) {
                vErrors = [err6];
              } else {
                vErrors.push(err6);
              }
              errors++;
            }
            if (data2.root === void 0) {
              const err7 = { instancePath: instancePath + "/installs/" + i0, schemaPath: "#/$defs/Install/required", keyword: "required", params: { missingProperty: "root" }, message: "must have required property 'root'" };
              if (vErrors === null) {
                vErrors = [err7];
              } else {
                vErrors.push(err7);
              }
              errors++;
            }
            if (data2.x2_path === void 0) {
              const err8 = { instancePath: instancePath + "/installs/" + i0, schemaPath: "#/$defs/Install/required", keyword: "required", params: { missingProperty: "x2_path" }, message: "must have required property 'x2_path'" };
              if (vErrors === null) {
                vErrors = [err8];
              } else {
                vErrors.push(err8);
              }
              errors++;
            }
            if (data2.runtime_tfm === void 0) {
              const err9 = { instancePath: instancePath + "/installs/" + i0, schemaPath: "#/$defs/Install/required", keyword: "required", params: { missingProperty: "runtime_tfm" }, message: "must have required property 'runtime_tfm'" };
              if (vErrors === null) {
                vErrors = [err9];
              } else {
                vErrors.push(err9);
              }
              errors++;
            }
            if (data2.registry_version === void 0) {
              const err10 = { instancePath: instancePath + "/installs/" + i0, schemaPath: "#/$defs/Install/required", keyword: "required", params: { missingProperty: "registry_version" }, message: "must have required property 'registry_version'" };
              if (vErrors === null) {
                vErrors = [err10];
              } else {
                vErrors.push(err10);
              }
              errors++;
            }
            if (data2.unique_id === void 0) {
              const err11 = { instancePath: instancePath + "/installs/" + i0, schemaPath: "#/$defs/Install/required", keyword: "required", params: { missingProperty: "unique_id" }, message: "must have required property 'unique_id'" };
              if (vErrors === null) {
                vErrors = [err11];
              } else {
                vErrors.push(err11);
              }
              errors++;
            }
            if (data2.source === void 0) {
              const err12 = { instancePath: instancePath + "/installs/" + i0, schemaPath: "#/$defs/Install/required", keyword: "required", params: { missingProperty: "source" }, message: "must have required property 'source'" };
              if (vErrors === null) {
                vErrors = [err12];
              } else {
                vErrors.push(err12);
              }
              errors++;
            }
            if (data2.name !== void 0) {
              if (typeof data2.name !== "string") {
                const err13 = { instancePath: instancePath + "/installs/" + i0 + "/name", schemaPath: "#/$defs/Install/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err13];
                } else {
                  vErrors.push(err13);
                }
                errors++;
              }
            }
            if (data2.label !== void 0) {
              if (typeof data2.label !== "string") {
                const err14 = { instancePath: instancePath + "/installs/" + i0 + "/label", schemaPath: "#/$defs/Install/properties/label/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err14];
                } else {
                  vErrors.push(err14);
                }
                errors++;
              }
            }
            if (data2.major !== void 0) {
              let data5 = data2.major;
              const _errs14 = errors;
              let valid5 = false;
              const _errs15 = errors;
              if (!(typeof data5 == "number" && (!(data5 % 1) && !isNaN(data5)))) {
                const err15 = { instancePath: instancePath + "/installs/" + i0 + "/major", schemaPath: "#/$defs/Install/properties/major/anyOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
                if (vErrors === null) {
                  vErrors = [err15];
                } else {
                  vErrors.push(err15);
                }
                errors++;
              }
              var _valid0 = _errs15 === errors;
              valid5 = valid5 || _valid0;
              const _errs17 = errors;
              if (data5 !== null) {
                const err16 = { instancePath: instancePath + "/installs/" + i0 + "/major", schemaPath: "#/$defs/Install/properties/major/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
                if (vErrors === null) {
                  vErrors = [err16];
                } else {
                  vErrors.push(err16);
                }
                errors++;
              }
              var _valid0 = _errs17 === errors;
              valid5 = valid5 || _valid0;
              if (!valid5) {
                const err17 = { instancePath: instancePath + "/installs/" + i0 + "/major", schemaPath: "#/$defs/Install/properties/major/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err17];
                } else {
                  vErrors.push(err17);
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
            if (data2.root !== void 0) {
              if (typeof data2.root !== "string") {
                const err18 = { instancePath: instancePath + "/installs/" + i0 + "/root", schemaPath: "#/$defs/Install/properties/root/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err18];
                } else {
                  vErrors.push(err18);
                }
                errors++;
              }
            }
            if (data2.x2_path !== void 0) {
              if (typeof data2.x2_path !== "string") {
                const err19 = { instancePath: instancePath + "/installs/" + i0 + "/x2_path", schemaPath: "#/$defs/Install/properties/x2_path/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err19];
                } else {
                  vErrors.push(err19);
                }
                errors++;
              }
            }
            if (data2.runtime_tfm !== void 0) {
              let data8 = data2.runtime_tfm;
              const _errs24 = errors;
              let valid6 = false;
              const _errs25 = errors;
              if (typeof data8 !== "string") {
                const err20 = { instancePath: instancePath + "/installs/" + i0 + "/runtime_tfm", schemaPath: "#/$defs/Install/properties/runtime_tfm/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err20];
                } else {
                  vErrors.push(err20);
                }
                errors++;
              }
              var _valid1 = _errs25 === errors;
              valid6 = valid6 || _valid1;
              const _errs27 = errors;
              if (data8 !== null) {
                const err21 = { instancePath: instancePath + "/installs/" + i0 + "/runtime_tfm", schemaPath: "#/$defs/Install/properties/runtime_tfm/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
                if (vErrors === null) {
                  vErrors = [err21];
                } else {
                  vErrors.push(err21);
                }
                errors++;
              }
              var _valid1 = _errs27 === errors;
              valid6 = valid6 || _valid1;
              if (!valid6) {
                const err22 = { instancePath: instancePath + "/installs/" + i0 + "/runtime_tfm", schemaPath: "#/$defs/Install/properties/runtime_tfm/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err22];
                } else {
                  vErrors.push(err22);
                }
                errors++;
              } else {
                errors = _errs24;
                if (vErrors !== null) {
                  if (_errs24) {
                    vErrors.length = _errs24;
                  } else {
                    vErrors = null;
                  }
                }
              }
            }
            if (data2.registry_version !== void 0) {
              let data9 = data2.registry_version;
              const _errs30 = errors;
              let valid7 = false;
              const _errs31 = errors;
              if (typeof data9 !== "string") {
                const err23 = { instancePath: instancePath + "/installs/" + i0 + "/registry_version", schemaPath: "#/$defs/Install/properties/registry_version/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err23];
                } else {
                  vErrors.push(err23);
                }
                errors++;
              }
              var _valid2 = _errs31 === errors;
              valid7 = valid7 || _valid2;
              const _errs33 = errors;
              if (data9 !== null) {
                const err24 = { instancePath: instancePath + "/installs/" + i0 + "/registry_version", schemaPath: "#/$defs/Install/properties/registry_version/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
                if (vErrors === null) {
                  vErrors = [err24];
                } else {
                  vErrors.push(err24);
                }
                errors++;
              }
              var _valid2 = _errs33 === errors;
              valid7 = valid7 || _valid2;
              if (!valid7) {
                const err25 = { instancePath: instancePath + "/installs/" + i0 + "/registry_version", schemaPath: "#/$defs/Install/properties/registry_version/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err25];
                } else {
                  vErrors.push(err25);
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
            if (data2.unique_id !== void 0) {
              let data10 = data2.unique_id;
              const _errs36 = errors;
              let valid8 = false;
              const _errs37 = errors;
              if (typeof data10 !== "string") {
                const err26 = { instancePath: instancePath + "/installs/" + i0 + "/unique_id", schemaPath: "#/$defs/Install/properties/unique_id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err26];
                } else {
                  vErrors.push(err26);
                }
                errors++;
              }
              var _valid3 = _errs37 === errors;
              valid8 = valid8 || _valid3;
              const _errs39 = errors;
              if (data10 !== null) {
                const err27 = { instancePath: instancePath + "/installs/" + i0 + "/unique_id", schemaPath: "#/$defs/Install/properties/unique_id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
                if (vErrors === null) {
                  vErrors = [err27];
                } else {
                  vErrors.push(err27);
                }
                errors++;
              }
              var _valid3 = _errs39 === errors;
              valid8 = valid8 || _valid3;
              if (!valid8) {
                const err28 = { instancePath: instancePath + "/installs/" + i0 + "/unique_id", schemaPath: "#/$defs/Install/properties/unique_id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err28];
                } else {
                  vErrors.push(err28);
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
            if (data2.source !== void 0) {
              if (typeof data2.source !== "string") {
                const err29 = { instancePath: instancePath + "/installs/" + i0 + "/source", schemaPath: "#/$defs/Install/properties/source/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err29];
                } else {
                  vErrors.push(err29);
                }
                errors++;
              }
            }
            for (const key0 in data2) {
              if (key0 !== "name" && key0 !== "label" && key0 !== "major" && key0 !== "root" && key0 !== "x2_path" && key0 !== "runtime_tfm" && key0 !== "registry_version" && key0 !== "unique_id" && key0 !== "source") {
                const err30 = { instancePath: instancePath + "/installs/" + i0 + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/Install/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err30];
                } else {
                  vErrors.push(err30);
                }
                errors++;
              }
            }
          } else {
            const err31 = { instancePath: instancePath + "/installs/" + i0, schemaPath: "#/$defs/Install/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err31];
            } else {
              vErrors.push(err31);
            }
            errors++;
          }
        }
      } else {
        const err32 = { instancePath: instancePath + "/installs", schemaPath: "#/properties/installs/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err32];
        } else {
          vErrors.push(err32);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "schema" && key1 !== "installs") {
        const err33 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
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
  validate20.errors = vErrors;
  return errors === 0;
}
validate20.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
export {
  validate_default as default,
  validate
};
