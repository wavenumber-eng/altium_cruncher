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
    if (data.actions === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "actions" }, message: "must have required property 'actions'" };
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
      if ("altium_cruncher.profiles.clean.a0" !== data0) {
        const err3 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.profiles.clean.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err3];
        } else {
          vErrors.push(err3);
        }
        errors++;
      }
    }
    if (data.actions !== void 0) {
      let data1 = data.actions;
      if (Array.isArray(data1)) {
        const len0 = data1.length;
        for (let i0 = 0; i0 < len0; i0++) {
          let data2 = data1[i0];
          if (data2 && typeof data2 == "object" && !Array.isArray(data2)) {
            if (data2.profile_guid === void 0) {
              const err4 = { instancePath: instancePath + "/actions/" + i0, schemaPath: "#/$defs/ProfileCleanAction/required", keyword: "required", params: { missingProperty: "profile_guid" }, message: "must have required property 'profile_guid'" };
              if (vErrors === null) {
                vErrors = [err4];
              } else {
                vErrors.push(err4);
              }
              errors++;
            }
            if (data2.profile_name === void 0) {
              const err5 = { instancePath: instancePath + "/actions/" + i0, schemaPath: "#/$defs/ProfileCleanAction/required", keyword: "required", params: { missingProperty: "profile_name" }, message: "must have required property 'profile_name'" };
              if (vErrors === null) {
                vErrors = [err5];
              } else {
                vErrors.push(err5);
              }
              errors++;
            }
            if (data2.profile_path === void 0) {
              const err6 = { instancePath: instancePath + "/actions/" + i0, schemaPath: "#/$defs/ProfileCleanAction/required", keyword: "required", params: { missingProperty: "profile_path" }, message: "must have required property 'profile_path'" };
              if (vErrors === null) {
                vErrors = [err6];
              } else {
                vErrors.push(err6);
              }
              errors++;
            }
            if (data2.module_name === void 0) {
              const err7 = { instancePath: instancePath + "/actions/" + i0, schemaPath: "#/$defs/ProfileCleanAction/required", keyword: "required", params: { missingProperty: "module_name" }, message: "must have required property 'module_name'" };
              if (vErrors === null) {
                vErrors = [err7];
              } else {
                vErrors.push(err7);
              }
              errors++;
            }
            if (data2.module_dir === void 0) {
              const err8 = { instancePath: instancePath + "/actions/" + i0, schemaPath: "#/$defs/ProfileCleanAction/required", keyword: "required", params: { missingProperty: "module_dir" }, message: "must have required property 'module_dir'" };
              if (vErrors === null) {
                vErrors = [err8];
              } else {
                vErrors.push(err8);
              }
              errors++;
            }
            if (data2.removed_module_dir === void 0) {
              const err9 = { instancePath: instancePath + "/actions/" + i0, schemaPath: "#/$defs/ProfileCleanAction/required", keyword: "required", params: { missingProperty: "removed_module_dir" }, message: "must have required property 'removed_module_dir'" };
              if (vErrors === null) {
                vErrors = [err9];
              } else {
                vErrors.push(err9);
              }
              errors++;
            }
            if (data2.removed_registry_item === void 0) {
              const err10 = { instancePath: instancePath + "/actions/" + i0, schemaPath: "#/$defs/ProfileCleanAction/required", keyword: "required", params: { missingProperty: "removed_registry_item" }, message: "must have required property 'removed_registry_item'" };
              if (vErrors === null) {
                vErrors = [err10];
              } else {
                vErrors.push(err10);
              }
              errors++;
            }
            if (data2.dry_run === void 0) {
              const err11 = { instancePath: instancePath + "/actions/" + i0, schemaPath: "#/$defs/ProfileCleanAction/required", keyword: "required", params: { missingProperty: "dry_run" }, message: "must have required property 'dry_run'" };
              if (vErrors === null) {
                vErrors = [err11];
              } else {
                vErrors.push(err11);
              }
              errors++;
            }
            if (data2.profile_guid !== void 0) {
              if (typeof data2.profile_guid !== "string") {
                const err12 = { instancePath: instancePath + "/actions/" + i0 + "/profile_guid", schemaPath: "#/$defs/ProfileCleanAction/properties/profile_guid/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err12];
                } else {
                  vErrors.push(err12);
                }
                errors++;
              }
            }
            if (data2.profile_name !== void 0) {
              if (typeof data2.profile_name !== "string") {
                const err13 = { instancePath: instancePath + "/actions/" + i0 + "/profile_name", schemaPath: "#/$defs/ProfileCleanAction/properties/profile_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err13];
                } else {
                  vErrors.push(err13);
                }
                errors++;
              }
            }
            if (data2.profile_path !== void 0) {
              if (typeof data2.profile_path !== "string") {
                const err14 = { instancePath: instancePath + "/actions/" + i0 + "/profile_path", schemaPath: "#/$defs/ProfileCleanAction/properties/profile_path/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err14];
                } else {
                  vErrors.push(err14);
                }
                errors++;
              }
            }
            if (data2.module_name !== void 0) {
              if (typeof data2.module_name !== "string") {
                const err15 = { instancePath: instancePath + "/actions/" + i0 + "/module_name", schemaPath: "#/$defs/ProfileCleanAction/properties/module_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err15];
                } else {
                  vErrors.push(err15);
                }
                errors++;
              }
            }
            if (data2.module_dir !== void 0) {
              if (typeof data2.module_dir !== "string") {
                const err16 = { instancePath: instancePath + "/actions/" + i0 + "/module_dir", schemaPath: "#/$defs/ProfileCleanAction/properties/module_dir/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err16];
                } else {
                  vErrors.push(err16);
                }
                errors++;
              }
            }
            if (data2.removed_module_dir !== void 0) {
              if (typeof data2.removed_module_dir !== "boolean") {
                const err17 = { instancePath: instancePath + "/actions/" + i0 + "/removed_module_dir", schemaPath: "#/$defs/ProfileCleanAction/properties/removed_module_dir/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
                if (vErrors === null) {
                  vErrors = [err17];
                } else {
                  vErrors.push(err17);
                }
                errors++;
              }
            }
            if (data2.removed_registry_item !== void 0) {
              if (typeof data2.removed_registry_item !== "boolean") {
                const err18 = { instancePath: instancePath + "/actions/" + i0 + "/removed_registry_item", schemaPath: "#/$defs/ProfileCleanAction/properties/removed_registry_item/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
                if (vErrors === null) {
                  vErrors = [err18];
                } else {
                  vErrors.push(err18);
                }
                errors++;
              }
            }
            if (data2.dry_run !== void 0) {
              if (typeof data2.dry_run !== "boolean") {
                const err19 = { instancePath: instancePath + "/actions/" + i0 + "/dry_run", schemaPath: "#/$defs/ProfileCleanAction/properties/dry_run/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
                if (vErrors === null) {
                  vErrors = [err19];
                } else {
                  vErrors.push(err19);
                }
                errors++;
              }
            }
            for (const key0 in data2) {
              if (key0 !== "profile_guid" && key0 !== "profile_name" && key0 !== "profile_path" && key0 !== "module_name" && key0 !== "module_dir" && key0 !== "removed_module_dir" && key0 !== "removed_registry_item" && key0 !== "dry_run") {
                const err20 = { instancePath: instancePath + "/actions/" + i0 + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/ProfileCleanAction/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err20];
                } else {
                  vErrors.push(err20);
                }
                errors++;
              }
            }
          } else {
            const err21 = { instancePath: instancePath + "/actions/" + i0, schemaPath: "#/$defs/ProfileCleanAction/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err21];
            } else {
              vErrors.push(err21);
            }
            errors++;
          }
        }
      } else {
        const err22 = { instancePath: instancePath + "/actions", schemaPath: "#/properties/actions/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err22];
        } else {
          vErrors.push(err22);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "schema" && key1 !== "actions") {
        const err23 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
    }
  } else {
    const err24 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err24];
    } else {
      vErrors.push(err24);
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
