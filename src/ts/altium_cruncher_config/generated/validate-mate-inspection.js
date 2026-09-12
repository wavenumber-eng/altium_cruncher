// Generated from src/tsp/altium_cruncher/outputs/mate.tsp. Do not edit.
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
    if (data.designator === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "designator" }, message: "must have required property 'designator'" };
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
    if (data.layer === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "layer" }, message: "must have required property 'layer'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.footprint === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "footprint" }, message: "must have required property 'footprint'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.x_mils === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "x_mils" }, message: "must have required property 'x_mils'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.y_mils === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "y_mils" }, message: "must have required property 'y_mils'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.designator !== void 0) {
      if (typeof data.designator !== "string") {
        const err6 = { instancePath: instancePath + "/designator", schemaPath: "#/properties/designator/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.kind !== void 0) {
      if (typeof data.kind !== "string") {
        const err7 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.layer !== void 0) {
      if (typeof data.layer !== "string") {
        const err8 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
    if (data.footprint !== void 0) {
      if (typeof data.footprint !== "string") {
        const err9 = { instancePath: instancePath + "/footprint", schemaPath: "#/properties/footprint/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
    }
    if (data.x_mils !== void 0) {
      if (!(typeof data.x_mils == "number")) {
        const err10 = { instancePath: instancePath + "/x_mils", schemaPath: "#/properties/x_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
    }
    if (data.y_mils !== void 0) {
      if (!(typeof data.y_mils == "number")) {
        const err11 = { instancePath: instancePath + "/y_mils", schemaPath: "#/properties/y_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
    }
    if (data.net_name !== void 0) {
      if (typeof data.net_name !== "string") {
        const err12 = { instancePath: instancePath + "/net_name", schemaPath: "#/properties/net_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
    }
    if (data.source_power_port !== void 0) {
      let data7 = data.source_power_port;
      if (data7 && typeof data7 == "object" && !Array.isArray(data7)) {
        if (data7.text === void 0) {
          const err13 = { instancePath: instancePath + "/source_power_port", schemaPath: "#/$defs/PowerPort/required", keyword: "required", params: { missingProperty: "text" }, message: "must have required property 'text'" };
          if (vErrors === null) {
            vErrors = [err13];
          } else {
            vErrors.push(err13);
          }
          errors++;
        }
        if (data7.style === void 0) {
          const err14 = { instancePath: instancePath + "/source_power_port", schemaPath: "#/$defs/PowerPort/required", keyword: "required", params: { missingProperty: "style" }, message: "must have required property 'style'" };
          if (vErrors === null) {
            vErrors = [err14];
          } else {
            vErrors.push(err14);
          }
          errors++;
        }
        if (data7.show_net_name === void 0) {
          const err15 = { instancePath: instancePath + "/source_power_port", schemaPath: "#/$defs/PowerPort/required", keyword: "required", params: { missingProperty: "show_net_name" }, message: "must have required property 'show_net_name'" };
          if (vErrors === null) {
            vErrors = [err15];
          } else {
            vErrors.push(err15);
          }
          errors++;
        }
        if (data7.text !== void 0) {
          if (typeof data7.text !== "string") {
            const err16 = { instancePath: instancePath + "/source_power_port/text", schemaPath: "#/$defs/PowerPort/properties/text/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err16];
            } else {
              vErrors.push(err16);
            }
            errors++;
          }
        }
        if (data7.style !== void 0) {
          if (typeof data7.style !== "string") {
            const err17 = { instancePath: instancePath + "/source_power_port/style", schemaPath: "#/$defs/PowerPort/properties/style/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err17];
            } else {
              vErrors.push(err17);
            }
            errors++;
          }
        }
        if (data7.show_net_name !== void 0) {
          if (typeof data7.show_net_name !== "boolean") {
            const err18 = { instancePath: instancePath + "/source_power_port/show_net_name", schemaPath: "#/$defs/PowerPort/properties/show_net_name/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err18];
            } else {
              vErrors.push(err18);
            }
            errors++;
          }
        }
        for (const key0 in data7) {
          if (key0 !== "text" && key0 !== "style" && key0 !== "show_net_name") {
            const err19 = { instancePath: instancePath + "/source_power_port/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/PowerPort/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err19];
            } else {
              vErrors.push(err19);
            }
            errors++;
          }
        }
      } else {
        const err20 = { instancePath: instancePath + "/source_power_port", schemaPath: "#/$defs/PowerPort/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
    }
    if (data.source_pad_geometries !== void 0) {
      let data12 = data.source_pad_geometries;
      if (Array.isArray(data12)) {
        const len0 = data12.length;
        for (let i0 = 0; i0 < len0; i0++) {
          let data13 = data12[i0];
          if (data13 && typeof data13 == "object" && !Array.isArray(data13)) {
            if (data13.x_mils === void 0) {
              const err21 = { instancePath: instancePath + "/source_pad_geometries/" + i0, schemaPath: "#/$defs/PadGeometry/required", keyword: "required", params: { missingProperty: "x_mils" }, message: "must have required property 'x_mils'" };
              if (vErrors === null) {
                vErrors = [err21];
              } else {
                vErrors.push(err21);
              }
              errors++;
            }
            if (data13.y_mils === void 0) {
              const err22 = { instancePath: instancePath + "/source_pad_geometries/" + i0, schemaPath: "#/$defs/PadGeometry/required", keyword: "required", params: { missingProperty: "y_mils" }, message: "must have required property 'y_mils'" };
              if (vErrors === null) {
                vErrors = [err22];
              } else {
                vErrors.push(err22);
              }
              errors++;
            }
            if (data13.width_mils === void 0) {
              const err23 = { instancePath: instancePath + "/source_pad_geometries/" + i0, schemaPath: "#/$defs/PadGeometry/required", keyword: "required", params: { missingProperty: "width_mils" }, message: "must have required property 'width_mils'" };
              if (vErrors === null) {
                vErrors = [err23];
              } else {
                vErrors.push(err23);
              }
              errors++;
            }
            if (data13.height_mils === void 0) {
              const err24 = { instancePath: instancePath + "/source_pad_geometries/" + i0, schemaPath: "#/$defs/PadGeometry/required", keyword: "required", params: { missingProperty: "height_mils" }, message: "must have required property 'height_mils'" };
              if (vErrors === null) {
                vErrors = [err24];
              } else {
                vErrors.push(err24);
              }
              errors++;
            }
            if (data13.shape === void 0) {
              const err25 = { instancePath: instancePath + "/source_pad_geometries/" + i0, schemaPath: "#/$defs/PadGeometry/required", keyword: "required", params: { missingProperty: "shape" }, message: "must have required property 'shape'" };
              if (vErrors === null) {
                vErrors = [err25];
              } else {
                vErrors.push(err25);
              }
              errors++;
            }
            if (data13.layer === void 0) {
              const err26 = { instancePath: instancePath + "/source_pad_geometries/" + i0, schemaPath: "#/$defs/PadGeometry/required", keyword: "required", params: { missingProperty: "layer" }, message: "must have required property 'layer'" };
              if (vErrors === null) {
                vErrors = [err26];
              } else {
                vErrors.push(err26);
              }
              errors++;
            }
            if (data13.rotation_degrees === void 0) {
              const err27 = { instancePath: instancePath + "/source_pad_geometries/" + i0, schemaPath: "#/$defs/PadGeometry/required", keyword: "required", params: { missingProperty: "rotation_degrees" }, message: "must have required property 'rotation_degrees'" };
              if (vErrors === null) {
                vErrors = [err27];
              } else {
                vErrors.push(err27);
              }
              errors++;
            }
            if (data13.x_mils !== void 0) {
              if (!(typeof data13.x_mils == "number")) {
                const err28 = { instancePath: instancePath + "/source_pad_geometries/" + i0 + "/x_mils", schemaPath: "#/$defs/PadGeometry/properties/x_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
                if (vErrors === null) {
                  vErrors = [err28];
                } else {
                  vErrors.push(err28);
                }
                errors++;
              }
            }
            if (data13.y_mils !== void 0) {
              if (!(typeof data13.y_mils == "number")) {
                const err29 = { instancePath: instancePath + "/source_pad_geometries/" + i0 + "/y_mils", schemaPath: "#/$defs/PadGeometry/properties/y_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
                if (vErrors === null) {
                  vErrors = [err29];
                } else {
                  vErrors.push(err29);
                }
                errors++;
              }
            }
            if (data13.width_mils !== void 0) {
              if (!(typeof data13.width_mils == "number")) {
                const err30 = { instancePath: instancePath + "/source_pad_geometries/" + i0 + "/width_mils", schemaPath: "#/$defs/PadGeometry/properties/width_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
                if (vErrors === null) {
                  vErrors = [err30];
                } else {
                  vErrors.push(err30);
                }
                errors++;
              }
            }
            if (data13.height_mils !== void 0) {
              if (!(typeof data13.height_mils == "number")) {
                const err31 = { instancePath: instancePath + "/source_pad_geometries/" + i0 + "/height_mils", schemaPath: "#/$defs/PadGeometry/properties/height_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
                if (vErrors === null) {
                  vErrors = [err31];
                } else {
                  vErrors.push(err31);
                }
                errors++;
              }
            }
            if (data13.shape !== void 0) {
              let data18 = data13.shape;
              if (!(typeof data18 == "number" && (!(data18 % 1) && !isNaN(data18)))) {
                const err32 = { instancePath: instancePath + "/source_pad_geometries/" + i0 + "/shape", schemaPath: "#/$defs/PadGeometry/properties/shape/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
                if (vErrors === null) {
                  vErrors = [err32];
                } else {
                  vErrors.push(err32);
                }
                errors++;
              }
            }
            if (data13.layer !== void 0) {
              let data19 = data13.layer;
              if (!(typeof data19 == "number" && (!(data19 % 1) && !isNaN(data19)))) {
                const err33 = { instancePath: instancePath + "/source_pad_geometries/" + i0 + "/layer", schemaPath: "#/$defs/PadGeometry/properties/layer/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
                if (vErrors === null) {
                  vErrors = [err33];
                } else {
                  vErrors.push(err33);
                }
                errors++;
              }
            }
            if (data13.rotation_degrees !== void 0) {
              if (!(typeof data13.rotation_degrees == "number")) {
                const err34 = { instancePath: instancePath + "/source_pad_geometries/" + i0 + "/rotation_degrees", schemaPath: "#/$defs/PadGeometry/properties/rotation_degrees/type", keyword: "type", params: { type: "number" }, message: "must be number" };
                if (vErrors === null) {
                  vErrors = [err34];
                } else {
                  vErrors.push(err34);
                }
                errors++;
              }
            }
            if (data13.corner_radius_mils !== void 0) {
              if (!(typeof data13.corner_radius_mils == "number")) {
                const err35 = { instancePath: instancePath + "/source_pad_geometries/" + i0 + "/corner_radius_mils", schemaPath: "#/$defs/PadGeometry/properties/corner_radius_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
                if (vErrors === null) {
                  vErrors = [err35];
                } else {
                  vErrors.push(err35);
                }
                errors++;
              }
            }
            for (const key1 in data13) {
              if (key1 !== "x_mils" && key1 !== "y_mils" && key1 !== "width_mils" && key1 !== "height_mils" && key1 !== "shape" && key1 !== "layer" && key1 !== "rotation_degrees" && key1 !== "corner_radius_mils") {
                const err36 = { instancePath: instancePath + "/source_pad_geometries/" + i0 + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/PadGeometry/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err36];
                } else {
                  vErrors.push(err36);
                }
                errors++;
              }
            }
          } else {
            const err37 = { instancePath: instancePath + "/source_pad_geometries/" + i0, schemaPath: "#/$defs/PadGeometry/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err37];
            } else {
              vErrors.push(err37);
            }
            errors++;
          }
        }
      } else {
        const err38 = { instancePath: instancePath + "/source_pad_geometries", schemaPath: "#/properties/source_pad_geometries/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err38];
        } else {
          vErrors.push(err38);
        }
        errors++;
      }
    }
    for (const key2 in data) {
      if (key2 !== "designator" && key2 !== "kind" && key2 !== "layer" && key2 !== "footprint" && key2 !== "x_mils" && key2 !== "y_mils" && key2 !== "net_name" && key2 !== "source_power_port" && key2 !== "source_pad_geometries") {
        const err39 = { instancePath: instancePath + "/" + key2.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
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
  validate22.errors = vErrors;
  return errors === 0;
}
validate22.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.designator === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "designator" }, message: "must have required property 'designator'" };
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
    if (data.layer === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "layer" }, message: "must have required property 'layer'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.x_mils === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "x_mils" }, message: "must have required property 'x_mils'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.y_mils === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "y_mils" }, message: "must have required property 'y_mils'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.width_mils === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "width_mils" }, message: "must have required property 'width_mils'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.height_mils === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "height_mils" }, message: "must have required property 'height_mils'" };
      if (vErrors === null) {
        vErrors = [err6];
      } else {
        vErrors.push(err6);
      }
      errors++;
    }
    if (data.hole_size_mils === void 0) {
      const err7 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "hole_size_mils" }, message: "must have required property 'hole_size_mils'" };
      if (vErrors === null) {
        vErrors = [err7];
      } else {
        vErrors.push(err7);
      }
      errors++;
    }
    if (data.plated === void 0) {
      const err8 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "plated" }, message: "must have required property 'plated'" };
      if (vErrors === null) {
        vErrors = [err8];
      } else {
        vErrors.push(err8);
      }
      errors++;
    }
    if (data.shape === void 0) {
      const err9 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "shape" }, message: "must have required property 'shape'" };
      if (vErrors === null) {
        vErrors = [err9];
      } else {
        vErrors.push(err9);
      }
      errors++;
    }
    if (data.designator !== void 0) {
      if (typeof data.designator !== "string") {
        const err10 = { instancePath: instancePath + "/designator", schemaPath: "#/properties/designator/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
    }
    if (data.kind !== void 0) {
      if (typeof data.kind !== "string") {
        const err11 = { instancePath: instancePath + "/kind", schemaPath: "#/properties/kind/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err11];
        } else {
          vErrors.push(err11);
        }
        errors++;
      }
    }
    if (data.layer !== void 0) {
      let data2 = data.layer;
      if (!(typeof data2 == "number" && (!(data2 % 1) && !isNaN(data2)))) {
        const err12 = { instancePath: instancePath + "/layer", schemaPath: "#/properties/layer/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
    }
    if (data.x_mils !== void 0) {
      if (!(typeof data.x_mils == "number")) {
        const err13 = { instancePath: instancePath + "/x_mils", schemaPath: "#/properties/x_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.y_mils !== void 0) {
      if (!(typeof data.y_mils == "number")) {
        const err14 = { instancePath: instancePath + "/y_mils", schemaPath: "#/properties/y_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
    }
    if (data.width_mils !== void 0) {
      if (!(typeof data.width_mils == "number")) {
        const err15 = { instancePath: instancePath + "/width_mils", schemaPath: "#/properties/width_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
    }
    if (data.height_mils !== void 0) {
      if (!(typeof data.height_mils == "number")) {
        const err16 = { instancePath: instancePath + "/height_mils", schemaPath: "#/properties/height_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
    }
    if (data.hole_size_mils !== void 0) {
      if (!(typeof data.hole_size_mils == "number")) {
        const err17 = { instancePath: instancePath + "/hole_size_mils", schemaPath: "#/properties/hole_size_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
    }
    if (data.plated !== void 0) {
      if (typeof data.plated !== "boolean") {
        const err18 = { instancePath: instancePath + "/plated", schemaPath: "#/properties/plated/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
    }
    if (data.shape !== void 0) {
      let data9 = data.shape;
      if (!(typeof data9 == "number" && (!(data9 % 1) && !isNaN(data9)))) {
        const err19 = { instancePath: instancePath + "/shape", schemaPath: "#/properties/shape/type", keyword: "type", params: { type: "integer" }, message: "must be integer" };
        if (vErrors === null) {
          vErrors = [err19];
        } else {
          vErrors.push(err19);
        }
        errors++;
      }
    }
    if (data.net_name !== void 0) {
      if (typeof data.net_name !== "string") {
        const err20 = { instancePath: instancePath + "/net_name", schemaPath: "#/properties/net_name/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err20];
        } else {
          vErrors.push(err20);
        }
        errors++;
      }
    }
    if (data.source_power_port !== void 0) {
      let data11 = data.source_power_port;
      if (data11 && typeof data11 == "object" && !Array.isArray(data11)) {
        if (data11.text === void 0) {
          const err21 = { instancePath: instancePath + "/source_power_port", schemaPath: "#/$defs/PowerPort/required", keyword: "required", params: { missingProperty: "text" }, message: "must have required property 'text'" };
          if (vErrors === null) {
            vErrors = [err21];
          } else {
            vErrors.push(err21);
          }
          errors++;
        }
        if (data11.style === void 0) {
          const err22 = { instancePath: instancePath + "/source_power_port", schemaPath: "#/$defs/PowerPort/required", keyword: "required", params: { missingProperty: "style" }, message: "must have required property 'style'" };
          if (vErrors === null) {
            vErrors = [err22];
          } else {
            vErrors.push(err22);
          }
          errors++;
        }
        if (data11.show_net_name === void 0) {
          const err23 = { instancePath: instancePath + "/source_power_port", schemaPath: "#/$defs/PowerPort/required", keyword: "required", params: { missingProperty: "show_net_name" }, message: "must have required property 'show_net_name'" };
          if (vErrors === null) {
            vErrors = [err23];
          } else {
            vErrors.push(err23);
          }
          errors++;
        }
        if (data11.text !== void 0) {
          if (typeof data11.text !== "string") {
            const err24 = { instancePath: instancePath + "/source_power_port/text", schemaPath: "#/$defs/PowerPort/properties/text/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err24];
            } else {
              vErrors.push(err24);
            }
            errors++;
          }
        }
        if (data11.style !== void 0) {
          if (typeof data11.style !== "string") {
            const err25 = { instancePath: instancePath + "/source_power_port/style", schemaPath: "#/$defs/PowerPort/properties/style/type", keyword: "type", params: { type: "string" }, message: "must be string" };
            if (vErrors === null) {
              vErrors = [err25];
            } else {
              vErrors.push(err25);
            }
            errors++;
          }
        }
        if (data11.show_net_name !== void 0) {
          if (typeof data11.show_net_name !== "boolean") {
            const err26 = { instancePath: instancePath + "/source_power_port/show_net_name", schemaPath: "#/$defs/PowerPort/properties/show_net_name/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
            if (vErrors === null) {
              vErrors = [err26];
            } else {
              vErrors.push(err26);
            }
            errors++;
          }
        }
        for (const key0 in data11) {
          if (key0 !== "text" && key0 !== "style" && key0 !== "show_net_name") {
            const err27 = { instancePath: instancePath + "/source_power_port/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/PowerPort/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err27];
            } else {
              vErrors.push(err27);
            }
            errors++;
          }
        }
      } else {
        const err28 = { instancePath: instancePath + "/source_power_port", schemaPath: "#/$defs/PowerPort/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err28];
        } else {
          vErrors.push(err28);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "designator" && key1 !== "kind" && key1 !== "layer" && key1 !== "x_mils" && key1 !== "y_mils" && key1 !== "width_mils" && key1 !== "height_mils" && key1 !== "hole_size_mils" && key1 !== "plated" && key1 !== "shape" && key1 !== "net_name" && key1 !== "source_power_port") {
        const err29 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err29];
        } else {
          vErrors.push(err29);
        }
        errors++;
      }
    }
  } else {
    const err30 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err30];
    } else {
      vErrors.push(err30);
    }
    errors++;
  }
  validate24.errors = vErrors;
  return errors === 0;
}
validate24.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
function validate27(data, { instancePath = "", parentData, parentDataProperty, rootData = data, dynamicAnchors = {} } = {}) {
  let vErrors = null;
  let errors = 0;
  const evaluated0 = validate27.evaluated;
  if (evaluated0.dynamicProps) {
    evaluated0.props = void 0;
  }
  if (evaluated0.dynamicItems) {
    evaluated0.items = void 0;
  }
  if (data && typeof data == "object" && !Array.isArray(data)) {
    if (data.x_mils === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "x_mils" }, message: "must have required property 'x_mils'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.y_mils === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "y_mils" }, message: "must have required property 'y_mils'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.segment === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "segment" }, message: "must have required property 'segment'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.center_mils === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "center_mils" }, message: "must have required property 'center_mils'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.radius_mils === void 0) {
      const err4 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "radius_mils" }, message: "must have required property 'radius_mils'" };
      if (vErrors === null) {
        vErrors = [err4];
      } else {
        vErrors.push(err4);
      }
      errors++;
    }
    if (data.start_angle_degrees === void 0) {
      const err5 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "start_angle_degrees" }, message: "must have required property 'start_angle_degrees'" };
      if (vErrors === null) {
        vErrors = [err5];
      } else {
        vErrors.push(err5);
      }
      errors++;
    }
    if (data.end_angle_degrees === void 0) {
      const err6 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "end_angle_degrees" }, message: "must have required property 'end_angle_degrees'" };
      if (vErrors === null) {
        vErrors = [err6];
      } else {
        vErrors.push(err6);
      }
      errors++;
    }
    if (data.x_mils !== void 0) {
      if (!(typeof data.x_mils == "number")) {
        const err7 = { instancePath: instancePath + "/x_mils", schemaPath: "#/properties/x_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.y_mils !== void 0) {
      if (!(typeof data.y_mils == "number")) {
        const err8 = { instancePath: instancePath + "/y_mils", schemaPath: "#/properties/y_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
    if (data.segment !== void 0) {
      let data2 = data.segment;
      if (typeof data2 !== "string") {
        const err9 = { instancePath: instancePath + "/segment", schemaPath: "#/properties/segment/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err9];
        } else {
          vErrors.push(err9);
        }
        errors++;
      }
      if ("arc" !== data2) {
        const err10 = { instancePath: instancePath + "/segment", schemaPath: "#/properties/segment/const", keyword: "const", params: { allowedValue: "arc" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err10];
        } else {
          vErrors.push(err10);
        }
        errors++;
      }
    }
    if (data.center_mils !== void 0) {
      let data3 = data.center_mils;
      if (Array.isArray(data3)) {
        if (data3.length > 2) {
          const err11 = { instancePath: instancePath + "/center_mils", schemaPath: "#/$defs/Pair/maxItems", keyword: "maxItems", params: { limit: 2 }, message: "must NOT have more than 2 items" };
          if (vErrors === null) {
            vErrors = [err11];
          } else {
            vErrors.push(err11);
          }
          errors++;
        }
        if (data3.length < 2) {
          const err12 = { instancePath: instancePath + "/center_mils", schemaPath: "#/$defs/Pair/minItems", keyword: "minItems", params: { limit: 2 }, message: "must NOT have fewer than 2 items" };
          if (vErrors === null) {
            vErrors = [err12];
          } else {
            vErrors.push(err12);
          }
          errors++;
        }
        const len0 = data3.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!(typeof data3[i0] == "number")) {
            const err13 = { instancePath: instancePath + "/center_mils/" + i0, schemaPath: "#/$defs/Pair/items/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err13];
            } else {
              vErrors.push(err13);
            }
            errors++;
          }
        }
      } else {
        const err14 = { instancePath: instancePath + "/center_mils", schemaPath: "#/$defs/Pair/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
    }
    if (data.radius_mils !== void 0) {
      if (!(typeof data.radius_mils == "number")) {
        const err15 = { instancePath: instancePath + "/radius_mils", schemaPath: "#/properties/radius_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
    }
    if (data.start_angle_degrees !== void 0) {
      if (!(typeof data.start_angle_degrees == "number")) {
        const err16 = { instancePath: instancePath + "/start_angle_degrees", schemaPath: "#/properties/start_angle_degrees/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err16];
        } else {
          vErrors.push(err16);
        }
        errors++;
      }
    }
    if (data.end_angle_degrees !== void 0) {
      if (!(typeof data.end_angle_degrees == "number")) {
        const err17 = { instancePath: instancePath + "/end_angle_degrees", schemaPath: "#/properties/end_angle_degrees/type", keyword: "type", params: { type: "number" }, message: "must be number" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
    }
    for (const key0 in data) {
      if (key0 !== "x_mils" && key0 !== "y_mils" && key0 !== "segment" && key0 !== "center_mils" && key0 !== "radius_mils" && key0 !== "start_angle_degrees" && key0 !== "end_angle_degrees") {
        const err18 = { instancePath: instancePath + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err18];
        } else {
          vErrors.push(err18);
        }
        errors++;
      }
    }
  } else {
    const err19 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err19];
    } else {
      vErrors.push(err19);
    }
    errors++;
  }
  validate27.errors = vErrors;
  return errors === 0;
}
validate27.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
var wrapper0 = { validate: validate26 };
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
    if (data.vertices === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "vertices" }, message: "must have required property 'vertices'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.closed === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "closed" }, message: "must have required property 'closed'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.vertices !== void 0) {
      let data0 = data.vertices;
      if (Array.isArray(data0)) {
        const len0 = data0.length;
        for (let i0 = 0; i0 < len0; i0++) {
          let data1 = data0[i0];
          const _errs4 = errors;
          let valid3 = false;
          const _errs5 = errors;
          if (data1 && typeof data1 == "object" && !Array.isArray(data1)) {
            if (data1.x_mils === void 0) {
              const err2 = { instancePath: instancePath + "/vertices/" + i0, schemaPath: "#/$defs/LineVertex/required", keyword: "required", params: { missingProperty: "x_mils" }, message: "must have required property 'x_mils'" };
              if (vErrors === null) {
                vErrors = [err2];
              } else {
                vErrors.push(err2);
              }
              errors++;
            }
            if (data1.y_mils === void 0) {
              const err3 = { instancePath: instancePath + "/vertices/" + i0, schemaPath: "#/$defs/LineVertex/required", keyword: "required", params: { missingProperty: "y_mils" }, message: "must have required property 'y_mils'" };
              if (vErrors === null) {
                vErrors = [err3];
              } else {
                vErrors.push(err3);
              }
              errors++;
            }
            if (data1.segment === void 0) {
              const err4 = { instancePath: instancePath + "/vertices/" + i0, schemaPath: "#/$defs/LineVertex/required", keyword: "required", params: { missingProperty: "segment" }, message: "must have required property 'segment'" };
              if (vErrors === null) {
                vErrors = [err4];
              } else {
                vErrors.push(err4);
              }
              errors++;
            }
            if (data1.x_mils !== void 0) {
              if (!(typeof data1.x_mils == "number")) {
                const err5 = { instancePath: instancePath + "/vertices/" + i0 + "/x_mils", schemaPath: "#/$defs/LineVertex/properties/x_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
                if (vErrors === null) {
                  vErrors = [err5];
                } else {
                  vErrors.push(err5);
                }
                errors++;
              }
            }
            if (data1.y_mils !== void 0) {
              if (!(typeof data1.y_mils == "number")) {
                const err6 = { instancePath: instancePath + "/vertices/" + i0 + "/y_mils", schemaPath: "#/$defs/LineVertex/properties/y_mils/type", keyword: "type", params: { type: "number" }, message: "must be number" };
                if (vErrors === null) {
                  vErrors = [err6];
                } else {
                  vErrors.push(err6);
                }
                errors++;
              }
            }
            if (data1.segment !== void 0) {
              let data4 = data1.segment;
              if (typeof data4 !== "string") {
                const err7 = { instancePath: instancePath + "/vertices/" + i0 + "/segment", schemaPath: "#/$defs/LineVertex/properties/segment/type", keyword: "type", params: { type: "string" }, message: "must be string" };
                if (vErrors === null) {
                  vErrors = [err7];
                } else {
                  vErrors.push(err7);
                }
                errors++;
              }
              if ("line" !== data4) {
                const err8 = { instancePath: instancePath + "/vertices/" + i0 + "/segment", schemaPath: "#/$defs/LineVertex/properties/segment/const", keyword: "const", params: { allowedValue: "line" }, message: "must be equal to constant" };
                if (vErrors === null) {
                  vErrors = [err8];
                } else {
                  vErrors.push(err8);
                }
                errors++;
              }
            }
            for (const key0 in data1) {
              if (key0 !== "x_mils" && key0 !== "y_mils" && key0 !== "segment") {
                const err9 = { instancePath: instancePath + "/vertices/" + i0 + "/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/LineVertex/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
                if (vErrors === null) {
                  vErrors = [err9];
                } else {
                  vErrors.push(err9);
                }
                errors++;
              }
            }
          } else {
            const err10 = { instancePath: instancePath + "/vertices/" + i0, schemaPath: "#/$defs/LineVertex/type", keyword: "type", params: { type: "object" }, message: "must be object" };
            if (vErrors === null) {
              vErrors = [err10];
            } else {
              vErrors.push(err10);
            }
            errors++;
          }
          var _valid0 = _errs5 === errors;
          valid3 = valid3 || _valid0;
          if (_valid0) {
            var props0 = true;
          }
          const _errs17 = errors;
          if (!validate27(data1, { instancePath: instancePath + "/vertices/" + i0, parentData: data0, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate27.errors : vErrors.concat(validate27.errors);
            errors = vErrors.length;
          }
          var _valid0 = _errs17 === errors;
          valid3 = valid3 || _valid0;
          if (_valid0) {
            if (props0 !== true) {
              props0 = true;
            }
          }
          if (!valid3) {
            const err11 = { instancePath: instancePath + "/vertices/" + i0, schemaPath: "#/properties/vertices/items/anyOf", keyword: "anyOf", params: {}, message: "must match a schema in anyOf" };
            if (vErrors === null) {
              vErrors = [err11];
            } else {
              vErrors.push(err11);
            }
            errors++;
          } else {
            errors = _errs4;
            if (vErrors !== null) {
              if (_errs4) {
                vErrors.length = _errs4;
              } else {
                vErrors = null;
              }
            }
          }
        }
      } else {
        const err12 = { instancePath: instancePath + "/vertices", schemaPath: "#/properties/vertices/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err12];
        } else {
          vErrors.push(err12);
        }
        errors++;
      }
    }
    if (data.closed !== void 0) {
      if (typeof data.closed !== "boolean") {
        const err13 = { instancePath: instancePath + "/closed", schemaPath: "#/properties/closed/type", keyword: "type", params: { type: "boolean" }, message: "must be boolean" };
        if (vErrors === null) {
          vErrors = [err13];
        } else {
          vErrors.push(err13);
        }
        errors++;
      }
    }
    if (data.cutouts !== void 0) {
      let data7 = data.cutouts;
      if (Array.isArray(data7)) {
        const len1 = data7.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (!wrapper0.validate(data7[i1], { instancePath: instancePath + "/cutouts/" + i1, parentData: data7, parentDataProperty: i1, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? wrapper0.validate.errors : vErrors.concat(wrapper0.validate.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err14 = { instancePath: instancePath + "/cutouts", schemaPath: "#/properties/cutouts/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err14];
        } else {
          vErrors.push(err14);
        }
        errors++;
      }
    }
    for (const key1 in data) {
      if (key1 !== "vertices" && key1 !== "closed" && key1 !== "cutouts") {
        const err15 = { instancePath: instancePath + "/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err15];
        } else {
          vErrors.push(err15);
        }
        errors++;
      }
    }
  } else {
    const err16 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err16];
    } else {
      vErrors.push(err16);
    }
    errors++;
  }
  validate26.errors = vErrors;
  return errors === 0;
}
validate26.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
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
    if (data.board_key === void 0) {
      const err0 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "board_key" }, message: "must have required property 'board_key'" };
      if (vErrors === null) {
        vErrors = [err0];
      } else {
        vErrors.push(err0);
      }
      errors++;
    }
    if (data.pcb_path === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "pcb_path" }, message: "must have required property 'pcb_path'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.components === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "components" }, message: "must have required property 'components'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.free_pads === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "free_pads" }, message: "must have required property 'free_pads'" };
      if (vErrors === null) {
        vErrors = [err3];
      } else {
        vErrors.push(err3);
      }
      errors++;
    }
    if (data.board_key !== void 0) {
      if (typeof data.board_key !== "string") {
        const err4 = { instancePath: instancePath + "/board_key", schemaPath: "#/properties/board_key/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err4];
        } else {
          vErrors.push(err4);
        }
        errors++;
      }
    }
    if (data.pcb_path !== void 0) {
      if (typeof data.pcb_path !== "string") {
        const err5 = { instancePath: instancePath + "/pcb_path", schemaPath: "#/properties/pcb_path/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.components !== void 0) {
      let data2 = data.components;
      if (Array.isArray(data2)) {
        const len0 = data2.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!validate22(data2[i0], { instancePath: instancePath + "/components/" + i0, parentData: data2, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate22.errors : vErrors.concat(validate22.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err6 = { instancePath: instancePath + "/components", schemaPath: "#/properties/components/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.free_pads !== void 0) {
      let data4 = data.free_pads;
      if (Array.isArray(data4)) {
        const len1 = data4.length;
        for (let i1 = 0; i1 < len1; i1++) {
          if (!validate24(data4[i1], { instancePath: instancePath + "/free_pads/" + i1, parentData: data4, parentDataProperty: i1, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate24.errors : vErrors.concat(validate24.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err7 = { instancePath: instancePath + "/free_pads", schemaPath: "#/properties/free_pads/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.board_outline_mils !== void 0) {
      let data6 = data.board_outline_mils;
      if (data6 && typeof data6 == "object" && !Array.isArray(data6)) {
        if (data6.left === void 0) {
          const err8 = { instancePath: instancePath + "/board_outline_mils", schemaPath: "#/$defs/Bounds/required", keyword: "required", params: { missingProperty: "left" }, message: "must have required property 'left'" };
          if (vErrors === null) {
            vErrors = [err8];
          } else {
            vErrors.push(err8);
          }
          errors++;
        }
        if (data6.bottom === void 0) {
          const err9 = { instancePath: instancePath + "/board_outline_mils", schemaPath: "#/$defs/Bounds/required", keyword: "required", params: { missingProperty: "bottom" }, message: "must have required property 'bottom'" };
          if (vErrors === null) {
            vErrors = [err9];
          } else {
            vErrors.push(err9);
          }
          errors++;
        }
        if (data6.right === void 0) {
          const err10 = { instancePath: instancePath + "/board_outline_mils", schemaPath: "#/$defs/Bounds/required", keyword: "required", params: { missingProperty: "right" }, message: "must have required property 'right'" };
          if (vErrors === null) {
            vErrors = [err10];
          } else {
            vErrors.push(err10);
          }
          errors++;
        }
        if (data6.top === void 0) {
          const err11 = { instancePath: instancePath + "/board_outline_mils", schemaPath: "#/$defs/Bounds/required", keyword: "required", params: { missingProperty: "top" }, message: "must have required property 'top'" };
          if (vErrors === null) {
            vErrors = [err11];
          } else {
            vErrors.push(err11);
          }
          errors++;
        }
        if (data6.left !== void 0) {
          if (!(typeof data6.left == "number")) {
            const err12 = { instancePath: instancePath + "/board_outline_mils/left", schemaPath: "#/$defs/Bounds/properties/left/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err12];
            } else {
              vErrors.push(err12);
            }
            errors++;
          }
        }
        if (data6.bottom !== void 0) {
          if (!(typeof data6.bottom == "number")) {
            const err13 = { instancePath: instancePath + "/board_outline_mils/bottom", schemaPath: "#/$defs/Bounds/properties/bottom/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err13];
            } else {
              vErrors.push(err13);
            }
            errors++;
          }
        }
        if (data6.right !== void 0) {
          if (!(typeof data6.right == "number")) {
            const err14 = { instancePath: instancePath + "/board_outline_mils/right", schemaPath: "#/$defs/Bounds/properties/right/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err14];
            } else {
              vErrors.push(err14);
            }
            errors++;
          }
        }
        if (data6.top !== void 0) {
          if (!(typeof data6.top == "number")) {
            const err15 = { instancePath: instancePath + "/board_outline_mils/top", schemaPath: "#/$defs/Bounds/properties/top/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err15];
            } else {
              vErrors.push(err15);
            }
            errors++;
          }
        }
        for (const key0 in data6) {
          if (key0 !== "left" && key0 !== "bottom" && key0 !== "right" && key0 !== "top") {
            const err16 = { instancePath: instancePath + "/board_outline_mils/" + key0.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/Bounds/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err16];
            } else {
              vErrors.push(err16);
            }
            errors++;
          }
        }
      } else {
        const err17 = { instancePath: instancePath + "/board_outline_mils", schemaPath: "#/$defs/Bounds/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err17];
        } else {
          vErrors.push(err17);
        }
        errors++;
      }
    }
    if (data.board_outline !== void 0) {
      if (!validate26(data.board_outline, { instancePath: instancePath + "/board_outline", parentData: data, parentDataProperty: "board_outline", rootData, dynamicAnchors })) {
        vErrors = vErrors === null ? validate26.errors : vErrors.concat(validate26.errors);
        errors = vErrors.length;
      }
    }
    if (data.board_origin_mils !== void 0) {
      let data13 = data.board_origin_mils;
      if (data13 && typeof data13 == "object" && !Array.isArray(data13)) {
        if (data13.x === void 0) {
          const err18 = { instancePath: instancePath + "/board_origin_mils", schemaPath: "#/$defs/Point/required", keyword: "required", params: { missingProperty: "x" }, message: "must have required property 'x'" };
          if (vErrors === null) {
            vErrors = [err18];
          } else {
            vErrors.push(err18);
          }
          errors++;
        }
        if (data13.y === void 0) {
          const err19 = { instancePath: instancePath + "/board_origin_mils", schemaPath: "#/$defs/Point/required", keyword: "required", params: { missingProperty: "y" }, message: "must have required property 'y'" };
          if (vErrors === null) {
            vErrors = [err19];
          } else {
            vErrors.push(err19);
          }
          errors++;
        }
        if (data13.x !== void 0) {
          if (!(typeof data13.x == "number")) {
            const err20 = { instancePath: instancePath + "/board_origin_mils/x", schemaPath: "#/$defs/Point/properties/x/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err20];
            } else {
              vErrors.push(err20);
            }
            errors++;
          }
        }
        if (data13.y !== void 0) {
          if (!(typeof data13.y == "number")) {
            const err21 = { instancePath: instancePath + "/board_origin_mils/y", schemaPath: "#/$defs/Point/properties/y/type", keyword: "type", params: { type: "number" }, message: "must be number" };
            if (vErrors === null) {
              vErrors = [err21];
            } else {
              vErrors.push(err21);
            }
            errors++;
          }
        }
        for (const key1 in data13) {
          if (key1 !== "x" && key1 !== "y") {
            const err22 = { instancePath: instancePath + "/board_origin_mils/" + key1.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/$defs/Point/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
            if (vErrors === null) {
              vErrors = [err22];
            } else {
              vErrors.push(err22);
            }
            errors++;
          }
        }
      } else {
        const err23 = { instancePath: instancePath + "/board_origin_mils", schemaPath: "#/$defs/Point/type", keyword: "type", params: { type: "object" }, message: "must be object" };
        if (vErrors === null) {
          vErrors = [err23];
        } else {
          vErrors.push(err23);
        }
        errors++;
      }
    }
    for (const key2 in data) {
      if (key2 !== "board_key" && key2 !== "pcb_path" && key2 !== "components" && key2 !== "free_pads" && key2 !== "board_outline_mils" && key2 !== "board_outline" && key2 !== "board_origin_mils") {
        const err24 = { instancePath: instancePath + "/" + key2.replace(/~/g, "~0").replace(/\//g, "~1"), schemaPath: "#/unevaluatedProperties/not", keyword: "not", params: {}, message: "must NOT be valid" };
        if (vErrors === null) {
          vErrors = [err24];
        } else {
          vErrors.push(err24);
        }
        errors++;
      }
    }
  } else {
    const err25 = { instancePath, schemaPath: "#/type", keyword: "type", params: { type: "object" }, message: "must be object" };
    if (vErrors === null) {
      vErrors = [err25];
    } else {
      vErrors.push(err25);
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
    if (data.source === void 0) {
      const err1 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "source" }, message: "must have required property 'source'" };
      if (vErrors === null) {
        vErrors = [err1];
      } else {
        vErrors.push(err1);
      }
      errors++;
    }
    if (data.source_tag === void 0) {
      const err2 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "source_tag" }, message: "must have required property 'source_tag'" };
      if (vErrors === null) {
        vErrors = [err2];
      } else {
        vErrors.push(err2);
      }
      errors++;
    }
    if (data.boards === void 0) {
      const err3 = { instancePath, schemaPath: "#/required", keyword: "required", params: { missingProperty: "boards" }, message: "must have required property 'boards'" };
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
      if ("altium_cruncher.mate.inspect.a0" !== data0) {
        const err5 = { instancePath: instancePath + "/schema", schemaPath: "#/properties/schema/const", keyword: "const", params: { allowedValue: "altium_cruncher.mate.inspect.a0" }, message: "must be equal to constant" };
        if (vErrors === null) {
          vErrors = [err5];
        } else {
          vErrors.push(err5);
        }
        errors++;
      }
    }
    if (data.source !== void 0) {
      if (typeof data.source !== "string") {
        const err6 = { instancePath: instancePath + "/source", schemaPath: "#/properties/source/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err6];
        } else {
          vErrors.push(err6);
        }
        errors++;
      }
    }
    if (data.source_tag !== void 0) {
      if (typeof data.source_tag !== "string") {
        const err7 = { instancePath: instancePath + "/source_tag", schemaPath: "#/properties/source_tag/type", keyword: "type", params: { type: "string" }, message: "must be string" };
        if (vErrors === null) {
          vErrors = [err7];
        } else {
          vErrors.push(err7);
        }
        errors++;
      }
    }
    if (data.boards !== void 0) {
      let data3 = data.boards;
      if (Array.isArray(data3)) {
        const len0 = data3.length;
        for (let i0 = 0; i0 < len0; i0++) {
          if (!validate21(data3[i0], { instancePath: instancePath + "/boards/" + i0, parentData: data3, parentDataProperty: i0, rootData, dynamicAnchors })) {
            vErrors = vErrors === null ? validate21.errors : vErrors.concat(validate21.errors);
            errors = vErrors.length;
          }
        }
      } else {
        const err8 = { instancePath: instancePath + "/boards", schemaPath: "#/properties/boards/type", keyword: "type", params: { type: "array" }, message: "must be array" };
        if (vErrors === null) {
          vErrors = [err8];
        } else {
          vErrors.push(err8);
        }
        errors++;
      }
    }
    for (const key0 in data) {
      if (key0 !== "schema" && key0 !== "source" && key0 !== "source_tag" && key0 !== "boards") {
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
  validate20.errors = vErrors;
  return errors === 0;
}
validate20.evaluated = { "props": true, "dynamicProps": false, "dynamicItems": false };
export {
  validate_default as default,
  validate
};
