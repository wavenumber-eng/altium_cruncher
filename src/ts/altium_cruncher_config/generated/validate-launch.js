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
    if (data.install === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "install" }, message: "must have required property 'install'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.file === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "file" }, message: "must have required property 'file'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.command === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "command" }, message: "must have required property 'command'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.dry_run === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "dry_run" }, message: "must have required property 'dry_run'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.schema !== void 0) {
      let data0 = data.schema;
      if (typeof data0 !== "string") {
        const err5 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
      if ("altium_cruncher.launch.a0" !== data0) {
        const err6 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.launch.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.install !== void 0) {
      let data1 = data.install;
      if (data1 && typeof data1 == "object" && !Array.isArray(data1)) {
        if (data1.name === void 0) {
          const err7 = { instancePath: instancePath + "/install", schemaPath: "#/$defs/Install/required", keyword: "required", params: { missingProperty: "name" }, message: "must have required property 'name'" };
          if (vErrors === null) {
            vErrors = [err7];
          } else {
            vErrors.push(err7);
          }
          errors++;
        }
        if (data1.label === void 0) {
          const err8 = { instancePath: instancePath + "/install", schemaPath: "#/$defs/Install/required", keyword: "required", params: { missingProperty: "label" }, message: "must have required property 'label'" };
          if (vErrors === null) {
            vErrors = [err8];
          } else {
            vErrors.push(err8);
          }
          errors++;
        }
        if (data1.major === void 0) {
          const err9 = { instancePath: instancePath + "/install", schemaPath: "#/$defs/Install/required", keyword: "required", params: { missingProperty: "major" }, message: "must have required property 'major'" };
          if (vErrors === null) {
            vErrors = [err9];
          } else {
            vErrors.push(err9);
          }
          errors++;
        }
        if (data1.root === void 0) {
          const err10 = { instancePath: instancePath + "/install", schemaPath: "#/$defs/Install/required", keyword: "required", params: { missingProperty: "root" }, message: "must have required property 'root'" };
          if (vErrors === null) {
            vErrors = [err10];
          } else {
            vErrors.push(err10);
          }
          errors++;
        }
        if (data1.x2_path === void 0) {
          const err11 = { instancePath: instancePath + "/install", schemaPath: "#/$defs/Install/required", keyword: "required", params: { missingProperty: "x2_path" }, message: "must have required property 'x2_path'" };
          if (vErrors === null) {
            vErrors = [err11];
          } else {
            vErrors.push(err11);
          }
          errors++;
        }
        if (data1.runtime_tfm === void 0) {
          const err12 = { instancePath: instancePath + "/install", schemaPath: "#/$defs/Install/required", keyword: "required", params: { missingProperty: "runtime_tfm" }, message: "must have required property 'runtime_tfm'" };
          if (vErrors === null) {
            vErrors = [err12];
          } else {
            vErrors.push(err12);
          }
          errors++;
        }
        if (data1.registry_version === void 0) {
          const err13 = { instancePath: instancePath + "/install", schemaPath: "#/$defs/Install/required", keyword: "required", params: { missingProperty: "registry_version" }, message: "must have required property 'registry_version'" };
          if (vErrors === null) {
            vErrors = [err13];
          } else {
            vErrors.push(err13);
          }
          errors++;
        }
        if (data1.unique_id === void 0) {
          const err14 = { instancePath: instancePath + "/install", schemaPath: "#/$defs/Install/required", keyword: "required", params: { missingProperty: "unique_id" }, message: "must have required property 'unique_id'" };
          if (vErrors === null) {
            vErrors = [err14];
          } else {
            vErrors.push(err14);
          }
          errors++;
        }
        if (data1.source === void 0) {
          const err15 = { instancePath: instancePath + "/install", schemaPath: "#/$defs/Install/required", keyword: "required", params: { missingProperty: "source" }, message: "must have required property 'source'" };
          if (vErrors === null) {
            vErrors = [err15];
          } else {
            vErrors.push(err15);
          }
          errors++;
        }
        if (data1.name !== void 0) {
          if (typeof data1.name !== "string") {
            const err16 = { instancePath: instancePath + "/install/name", schemaPath: "#/$defs/Install/properties/name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err16];
            } else {
              vErrors.push(err16);
            }
            errors++;
          }
        }
        if (data1.label !== void 0) {
          if (typeof data1.label !== "string") {
            const err17 = { instancePath: instancePath + "/install/label", schemaPath: "#/$defs/Install/properties/label/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err17];
            } else {
              vErrors.push(err17);
            }
            errors++;
          }
        }
        if (data1.major !== void 0) {
          let data4 = data1.major;
          const _errs12 = errors;
          let valid3 = false;
          const _errs13 = errors;
          if (!(typeof data4 == "number" && (!(data4 % 1) && !isNaN(data4)))) {
            const err18 = { instancePath: instancePath + "/install/major", schemaPath: "#/$defs/Install/properties/major/anyOf/0/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
            if (vErrors === null) {
              vErrors = [err18];
            } else {
              vErrors.push(err18);
            }
            errors++;
          }
          var _valid0 = _errs13 === errors;
          valid3 = valid3 || _valid0;
          const _errs15 = errors;
          if (data4 !== null) {
            const err19 = { instancePath: instancePath + "/install/major", schemaPath: "#/$defs/Install/properties/major/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err19];
            } else {
              vErrors.push(err19);
            }
            errors++;
          }
          var _valid0 = _errs15 === errors;
          valid3 = valid3 || _valid0;
          if (!valid3) {
            const err20 = { instancePath: instancePath + "/install/major", schemaPath: "#/$defs/Install/properties/major/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err20];
            } else {
              vErrors.push(err20);
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
        if (data1.root !== void 0) {
          if (typeof data1.root !== "string") {
            const err21 = { instancePath: instancePath + "/install/root", schemaPath: "#/$defs/Install/properties/root/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err21];
            } else {
              vErrors.push(err21);
            }
            errors++;
          }
        }
        if (data1.x2_path !== void 0) {
          if (typeof data1.x2_path !== "string") {
            const err22 = { instancePath: instancePath + "/install/x2_path", schemaPath: "#/$defs/Install/properties/x2_path/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err22];
            } else {
              vErrors.push(err22);
            }
            errors++;
          }
        }
        if (data1.runtime_tfm !== void 0) {
          let data7 = data1.runtime_tfm;
          const _errs22 = errors;
          let valid4 = false;
          const _errs23 = errors;
          if (typeof data7 !== "string") {
            const err23 = { instancePath: instancePath + "/install/runtime_tfm", schemaPath: "#/$defs/Install/properties/runtime_tfm/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err23];
            } else {
              vErrors.push(err23);
            }
            errors++;
          }
          var _valid1 = _errs23 === errors;
          valid4 = valid4 || _valid1;
          const _errs25 = errors;
          if (data7 !== null) {
            const err24 = { instancePath: instancePath + "/install/runtime_tfm", schemaPath: "#/$defs/Install/properties/runtime_tfm/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err24];
            } else {
              vErrors.push(err24);
            }
            errors++;
          }
          var _valid1 = _errs25 === errors;
          valid4 = valid4 || _valid1;
          if (!valid4) {
            const err25 = { instancePath: instancePath + "/install/runtime_tfm", schemaPath: "#/$defs/Install/properties/runtime_tfm/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err25];
            } else {
              vErrors.push(err25);
            }
            errors++;
          } else {
            errors = _errs22;
            if (vErrors !== null) {
              if (_errs22) {
                vErrors.length = _errs22;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data1.registry_version !== void 0) {
          let data8 = data1.registry_version;
          const _errs28 = errors;
          let valid5 = false;
          const _errs29 = errors;
          if (typeof data8 !== "string") {
            const err26 = { instancePath: instancePath + "/install/registry_version", schemaPath: "#/$defs/Install/properties/registry_version/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err26];
            } else {
              vErrors.push(err26);
            }
            errors++;
          }
          var _valid2 = _errs29 === errors;
          valid5 = valid5 || _valid2;
          const _errs31 = errors;
          if (data8 !== null) {
            const err27 = { instancePath: instancePath + "/install/registry_version", schemaPath: "#/$defs/Install/properties/registry_version/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err27];
            } else {
              vErrors.push(err27);
            }
            errors++;
          }
          var _valid2 = _errs31 === errors;
          valid5 = valid5 || _valid2;
          if (!valid5) {
            const err28 = { instancePath: instancePath + "/install/registry_version", schemaPath: "#/$defs/Install/properties/registry_version/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err28];
            } else {
              vErrors.push(err28);
            }
            errors++;
          } else {
            errors = _errs28;
            if (vErrors !== null) {
              if (_errs28) {
                vErrors.length = _errs28;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data1.unique_id !== void 0) {
          let data9 = data1.unique_id;
          const _errs34 = errors;
          let valid6 = false;
          const _errs35 = errors;
          if (typeof data9 !== "string") {
            const err29 = { instancePath: instancePath + "/install/unique_id", schemaPath: "#/$defs/Install/properties/unique_id/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err29];
            } else {
              vErrors.push(err29);
            }
            errors++;
          }
          var _valid3 = _errs35 === errors;
          valid6 = valid6 || _valid3;
          const _errs37 = errors;
          if (data9 !== null) {
            const err30 = { instancePath: instancePath + "/install/unique_id", schemaPath: "#/$defs/Install/properties/unique_id/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
            if (vErrors === null) {
              vErrors = [err30];
            } else {
              vErrors.push(err30);
            }
            errors++;
          }
          var _valid3 = _errs37 === errors;
          valid6 = valid6 || _valid3;
          if (!valid6) {
            const err31 = { instancePath: instancePath + "/install/unique_id", schemaPath: "#/$defs/Install/properties/unique_id/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err31];
            } else {
              vErrors.push(err31);
            }
            errors++;
          } else {
            errors = _errs34;
            if (vErrors !== null) {
              if (_errs34) {
                vErrors.length = _errs34;
              } else {
                vErrors = null;
              }
            }
          }
        }
        if (data1.source !== void 0) {
          if (typeof data1.source !== "string") {
            const err32 = { instancePath: instancePath + "/install/source", schemaPath: "#/$defs/Install/properties/source/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err32];
            } else {
              vErrors.push(err32);
            }
            errors++;
          }
        }
        for (const key0 in data1) {
          if (key0 !== "name" && key0 !== "label" && key0 !== "major" && key0 !== "root" && key0 !== "x2_path" && key0 !== "runtime_tfm" && key0 !== "registry_version" && key0 !== "unique_id" && key0 !== "source") {
            const err33 = { instancePath: instancePath + "/install/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/Install/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err33];
            } else {
              vErrors.push(err33);
            }
            errors++;
          }
        }
      } else {
        const err34 = { instancePath: instancePath + "/install", schemaPath: "#/$defs/Install/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err34];
        } else {
          vErrors.push(err34);
        }
        errors++;
      }
    }
    if (data.file !== void 0) {
      let data12 = data.file;
      const _errs45 = errors;
      let valid8 = false;
      const _errs46 = errors;
      if (typeof data12 !== "string") {
        const err35 = { instancePath: instancePath + "/file", schemaPath: "#/properties/file/anyOf/0/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err35];
        } else {
          vErrors.push(err35);
        }
        errors++;
      }
      var _valid4 = _errs46 === errors;
      valid8 = valid8 || _valid4;
      const _errs48 = errors;
      if (data12 !== null) {
        const err36 = { instancePath: instancePath + "/file", schemaPath: "#/properties/file/anyOf/1/type", keyword: "type", params: { type: "null" }, message: "must be null" };
        if (vErrors === null) {
          vErrors = [err36];
        } else {
          vErrors.push(err36);
        }
        errors++;
      }
      var _valid4 = _errs48 === errors;
      valid8 = valid8 || _valid4;
      if (!valid8) {
        const err37 = { instancePath: instancePath + "/file", schemaPath: "#/properties/file/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
        if (vErrors === null) {
          vErrors = [err37];
        } else {
          vErrors.push(err37);
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
    if (data.command !== void 0) {
      let data13 = data.command;
      if (Array.isArray(data13)) {
        const len0 = data13.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (typeof data13[i0] !== "string") {
            const err38 = { instancePath: instancePath + "/command/" + i0, schemaPath: "#/properties/command/items/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err38];
            } else {
              vErrors.push(err38);
            }
            errors++;
          }
        }
      } else {
        const err39 = { instancePath: instancePath + "/command", schemaPath: "#/properties/command/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err39];
        } else {
          vErrors.push(err39);
        }
        errors++;
      }
    }
    if (data.dry_run !== void 0) {
      if (typeof data.dry_run !== "boolean") {
        const err40 = { instancePath: instancePath + "/dry_run", schemaPath: "#/properties/dry_run/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err40];
        } else {
          vErrors.push(err40);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "schema" && key1 !== "install" && key1 !== "file" && key1 !== "command" && key1 !== "dry_run") {
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
