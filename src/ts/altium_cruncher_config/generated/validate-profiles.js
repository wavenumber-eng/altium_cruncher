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
    if (data.profiles === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "profiles" }, message: "must have required property 'profiles'" };
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
      if ("altium_cruncher.profiles.a0" !== data0) {
        const err3 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.profiles.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.profiles !== void 0) {
      let data1 = data.profiles;
      if (Array.isArray(data1)) {
        const len0 = data1.length;
        for (let i0 = 0; i0 < len0; i0++) {
          let data2 = data1[i0];
          if (data2 && typeof data2 == "object" && !Array.isArray(data2)) {
            if (data2.name === void 0) {
              const err4 = { instancePath: instancePath + "/profiles/" + i0, schemaPath: "#/$defs/Profile/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
              if (vErrors === null) {
                vErrors = [err4];
              } else {
                vErrors.push(err4);
              }
              errors++;
            }
            if (data2.guid === void 0) {
              const err5 = { instancePath: instancePath + "/profiles/" + i0, schemaPath: "#/$defs/Profile/required", keyword: "required", params: { missingProperty: "guid" }, message: "must have required property 'guid'" };
              if (vErrors === null) {
                vErrors = [err5];
              } else {
                vErrors.push(err5);
              }
              errors++;
            }
            if (data2.path === void 0) {
              const err6 = { instancePath: instancePath + "/profiles/" + i0, schemaPath: "#/$defs/Profile/required", keyword: "required", params: { missingProperty: "path" }, message: "must have required property 'path'" };
              if (vErrors === null) {
                vErrors = [err6];
              } else {
                vErrors.push(err6);
              }
              errors++;
            }
            if (data2.extensions_root === void 0) {
              const err7 = { instancePath: instancePath + "/profiles/" + i0, schemaPath: "#/$defs/Profile/required", keyword: "required", params: { missingProperty: "extensions_root" }, message: "must have required property 'extensions_root'" };
              if (vErrors === null) {
                vErrors = [err7];
              } else {
                vErrors.push(err7);
              }
              errors++;
            }
            if (data2.registry_path === void 0) {
              const err8 = { instancePath: instancePath + "/profiles/" + i0, schemaPath: "#/$defs/Profile/required", keyword: "required", params: { missingProperty: "registry_path" }, message: "must have required property 'registry_path'" };
              if (vErrors === null) {
                vErrors = [err8];
              } else {
                vErrors.push(err8);
              }
              errors++;
            }
            if (data2.registry_exists === void 0) {
              const err9 = { instancePath: instancePath + "/profiles/" + i0, schemaPath: "#/$defs/Profile/required", keyword: "required", params: { missingProperty: "registry_exists" }, message: "must have required property 'registry_exists'" };
              if (vErrors === null) {
                vErrors = [err9];
              } else {
                vErrors.push(err9);
              }
              errors++;
            }
            if (data2.module_name === void 0) {
              const err10 = { instancePath: instancePath + "/profiles/" + i0, schemaPath: "#/$defs/Profile/required", keyword: "required", params: { missingProperty: "module_name" }, message: "must have required property 'module_name'" };
              if (vErrors === null) {
                vErrors = [err10];
              } else {
                vErrors.push(err10);
              }
              errors++;
            }
            if (data2.module_dir === void 0) {
              const err11 = { instancePath: instancePath + "/profiles/" + i0, schemaPath: "#/$defs/Profile/required", keyword: "required", params: { missingProperty: "module_dir" }, message: "must have required property 'module_dir'" };
              if (vErrors === null) {
                vErrors = [err11];
              } else {
                vErrors.push(err11);
              }
              errors++;
            }
            if (data2.module_dir_exists === void 0) {
              const err12 = { instancePath: instancePath + "/profiles/" + i0, schemaPath: "#/$defs/Profile/required", keyword: "required", params: { missingProperty: "module_dir_exists" }, message: "must have required property 'module_dir_exists'" };
              if (vErrors === null) {
                vErrors = [err12];
              } else {
                vErrors.push(err12);
              }
              errors++;
            }
            if (data2.registered === void 0) {
              const err13 = { instancePath: instancePath + "/profiles/" + i0, schemaPath: "#/$defs/Profile/required", keyword: "required", params: { missingProperty: "registered" }, message: "must have required property 'registered'" };
              if (vErrors === null) {
                vErrors = [err13];
              } else {
                vErrors.push(err13);
              }
              errors++;
            }
            if (data2.registry_version === void 0) {
              const err14 = { instancePath: instancePath + "/profiles/" + i0, schemaPath: "#/$defs/Profile/required", keyword: "required", params: { missingProperty: "registry_version" }, message: "must have required property 'registry_version'" };
              if (vErrors === null) {
                vErrors = [err14];
              } else {
                vErrors.push(err14);
              }
              errors++;
            }
            if (data2.dll_path === void 0) {
              const err15 = { instancePath: instancePath + "/profiles/" + i0, schemaPath: "#/$defs/Profile/required", keyword: "required", params: { missingProperty: "dll_path" }, message: "must have required property 'dll_path'" };
              if (vErrors === null) {
                vErrors = [err15];
              } else {
                vErrors.push(err15);
              }
              errors++;
            }
            if (data2.dll_exists === void 0) {
              const err16 = { instancePath: instancePath + "/profiles/" + i0, schemaPath: "#/$defs/Profile/required", keyword: "required", params: { missingProperty: "dll_exists" }, message: "must have required property 'dll_exists'" };
              if (vErrors === null) {
                vErrors = [err16];
              } else {
                vErrors.push(err16);
              }
              errors++;
            }
            if (data2.last_write_time_utc === void 0) {
              const err17 = { instancePath: instancePath + "/profiles/" + i0, schemaPath: "#/$defs/Profile/required", keyword: "required", params: { missingProperty: "last_write_time_utc" }, message: "must have required property 'last_write_time_utc'" };
              if (vErrors === null) {
                vErrors = [err17];
              } else {
                vErrors.push(err17);
              }
              errors++;
            }
            if (data2.name !== void 0) {
              if (typeof data2.name !== "string") {
                const err18 = { instancePath: instancePath + "/profiles/" + i0 + "/name", schemaPath: "#/$defs/Profile/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err18];
                } else {
                  vErrors.push(err18);
                }
                errors++;
              }
            }
            if (data2.guid !== void 0) {
              if (typeof data2.guid !== "string") {
                const err19 = { instancePath: instancePath + "/profiles/" + i0 + "/guid", schemaPath: "#/$defs/Profile/properties/guid/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err19];
                } else {
                  vErrors.push(err19);
                }
                errors++;
              }
            }
            if (data2.path !== void 0) {
              if (typeof data2.path !== "string") {
                const err20 = { instancePath: instancePath + "/profiles/" + i0 + "/path", schemaPath: "#/$defs/Profile/properties/path/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err20];
                } else {
                  vErrors.push(err20);
                }
                errors++;
              }
            }
            if (data2.extensions_root !== void 0) {
              if (typeof data2.extensions_root !== "string") {
                const err21 = { instancePath: instancePath + "/profiles/" + i0 + "/extensions_root", schemaPath: "#/$defs/Profile/properties/extensions_root/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err21];
                } else {
                  vErrors.push(err21);
                }
                errors++;
              }
            }
            if (data2.registry_path !== void 0) {
              if (typeof data2.registry_path !== "string") {
                const err22 = { instancePath: instancePath + "/profiles/" + i0 + "/registry_path", schemaPath: "#/$defs/Profile/properties/registry_path/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err22];
                } else {
                  vErrors.push(err22);
                }
                errors++;
              }
            }
            if (data2.registry_exists !== void 0) {
              if (typeof data2.registry_exists !== "boolean") {
                const err23 = { instancePath: instancePath + "/profiles/" + i0 + "/registry_exists", schemaPath: "#/$defs/Profile/properties/registry_exists/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
                if (vErrors === null) {
                  vErrors = [err23];
                } else {
                  vErrors.push(err23);
                }
                errors++;
              }
            }
            if (data2.module_name !== void 0) {
              if (typeof data2.module_name !== "string") {
                const err24 = { instancePath: instancePath + "/profiles/" + i0 + "/module_name", schemaPath: "#/$defs/Profile/properties/module_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err24];
                } else {
                  vErrors.push(err24);
                }
                errors++;
              }
            }
            if (data2.module_dir !== void 0) {
              if (typeof data2.module_dir !== "string") {
                const err25 = { instancePath: instancePath + "/profiles/" + i0 + "/module_dir", schemaPath: "#/$defs/Profile/properties/module_dir/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err25];
                } else {
                  vErrors.push(err25);
                }
                errors++;
              }
            }
            if (data2.module_dir_exists !== void 0) {
              if (typeof data2.module_dir_exists !== "boolean") {
                const err26 = { instancePath: instancePath + "/profiles/" + i0 + "/module_dir_exists", schemaPath: "#/$defs/Profile/properties/module_dir_exists/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
                if (vErrors === null) {
                  vErrors = [err26];
                } else {
                  vErrors.push(err26);
                }
                errors++;
              }
            }
            if (data2.registered !== void 0) {
              if (typeof data2.registered !== "boolean") {
                const err27 = { instancePath: instancePath + "/profiles/" + i0 + "/registered", schemaPath: "#/$defs/Profile/properties/registered/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
                if (vErrors === null) {
                  vErrors = [err27];
                } else {
                  vErrors.push(err27);
                }
                errors++;
              }
            }
            if (data2.registry_version !== void 0) {
              let data13 = data2.registry_version;
              const _errs30 = errors;
              let valid5 = false;
              const _errs31 = errors;
              if (typeof data13 !== "string") {
                const err28 = { instancePath: instancePath + "/profiles/" + i0 + "/registry_version", schemaPath: "#/$defs/Profile/properties/registry_version/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err28];
                } else {
                  vErrors.push(err28);
                }
                errors++;
              }
              var _valid0 = _errs31 === errors;
              valid5 = valid5 || _valid0;
              const _errs33 = errors;
              if (data13 !== null) {
                const err29 = { instancePath: instancePath + "/profiles/" + i0 + "/registry_version", schemaPath: "#/$defs/Profile/properties/registry_version/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
                if (vErrors === null) {
                  vErrors = [err29];
                } else {
                  vErrors.push(err29);
                }
                errors++;
              }
              var _valid0 = _errs33 === errors;
              valid5 = valid5 || _valid0;
              if (!valid5) {
                const err30 = { instancePath: instancePath + "/profiles/" + i0 + "/registry_version", schemaPath: "#/$defs/Profile/properties/registry_version/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
                if (vErrors === null) {
                  vErrors = [err30];
                } else {
                  vErrors.push(err30);
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
            if (data2.dll_path !== void 0) {
              if (typeof data2.dll_path !== "string") {
                const err31 = { instancePath: instancePath + "/profiles/" + i0 + "/dll_path", schemaPath: "#/$defs/Profile/properties/dll_path/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err31];
                } else {
                  vErrors.push(err31);
                }
                errors++;
              }
            }
            if (data2.dll_exists !== void 0) {
              if (typeof data2.dll_exists !== "boolean") {
                const err32 = { instancePath: instancePath + "/profiles/" + i0 + "/dll_exists", schemaPath: "#/$defs/Profile/properties/dll_exists/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
                if (vErrors === null) {
                  vErrors = [err32];
                } else {
                  vErrors.push(err32);
                }
                errors++;
              }
            }
            if (data2.last_write_time_utc !== void 0) {
              let data16 = data2.last_write_time_utc;
              const _errs40 = errors;
              let valid6 = false;
              const _errs41 = errors;
              if (typeof data16 !== "string") {
                const err33 = { instancePath: instancePath + "/profiles/" + i0 + "/last_write_time_utc", schemaPath: "#/$defs/Profile/properties/last_write_time_utc/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err33];
                } else {
                  vErrors.push(err33);
                }
                errors++;
              }
              var _valid1 = _errs41 === errors;
              valid6 = valid6 || _valid1;
              const _errs43 = errors;
              if (data16 !== null) {
                const err34 = { instancePath: instancePath + "/profiles/" + i0 + "/last_write_time_utc", schemaPath: "#/$defs/Profile/properties/last_write_time_utc/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
                if (vErrors === null) {
                  vErrors = [err34];
                } else {
                  vErrors.push(err34);
                }
                errors++;
              }
              var _valid1 = _errs43 === errors;
              valid6 = valid6 || _valid1;
              if (!valid6) {
                const err35 = { instancePath: instancePath + "/profiles/" + i0 + "/last_write_time_utc", schemaPath: "#/$defs/Profile/properties/last_write_time_utc/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
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
            for (const key0 in data2) {
              if (key0 !== "name" && key0 !== "guid" && key0 !== "path" && key0 !== "extensions_root" && key0 !== "registry_path" && key0 !== "registry_exists" && key0 !== "module_name" && key0 !== "module_dir" && key0 !== "module_dir_exists" && key0 !== "registered" && key0 !== "registry_version" && key0 !== "dll_path" && key0 !== "dll_exists" && key0 !== "last_write_time_utc") {
                const err36 = { instancePath: instancePath + "/profiles/" + i0 + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/Profile/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err36];
                } else {
                  vErrors.push(err36);
                }
                errors++;
              }
            }
          } else {
            const err37 = { instancePath: instancePath + "/profiles/" + i0, schemaPath: "#/$defs/Profile/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err37];
            } else {
              vErrors.push(err37);
            }
            errors++;
          }
        }
      } else {
        const err38 = { instancePath: instancePath + "/profiles", schemaPath: "#/properties/profiles/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err38];
        } else {
          vErrors.push(err38);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "schema" && key1 !== "profiles") {
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
  validate20.errors = vErrors;
  return errors === 0;
}
validate20.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
export {
  validate_default as default,
  validate
};
