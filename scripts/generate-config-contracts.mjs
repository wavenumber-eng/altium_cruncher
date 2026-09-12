// TypeSpec is the authored input. Every generated projection comes from its schema.
import { spawnSync } from "node:child_process";
import { mkdtempSync, mkdirSync, readFileSync, writeFileSync, rmSync, existsSync, readdirSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, resolve, join, posix } from "node:path";
import { fileURLToPath } from "node:url";
import { compile } from "json-schema-to-typescript";
import Ajv2020 from "ajv/dist/2020.js";
import standaloneCode from "ajv/dist/standalone/index.js";
import { _ } from "ajv/dist/compile/codegen/index.js";
import { build } from "esbuild";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const check = process.argv.includes("--check");
const tempBase = resolve(tmpdir());
const temp = mkdtempSync(join(tempBase, "acr-contracts-"));
const outputs = new Map();
const families = [
  {stem: "pcb_svg_config", slug: "pcb-svg", model: "PcbSvgConfigInput", source: "pcb-svg", title: "PCB SVG / Toon", validator: "validate"},
  {stem: "schdoc_create_config", slug: "schdoc-create", model: "SchdocCreateConfigInput", source: "creation", title: "SchDoc creation"},
  {stem: "pcbdoc_create_config", slug: "pcbdoc-create", model: "PcbdocCreateConfigInput", source: "creation", title: "PcbDoc creation"},
  {stem: "project_skeleton_config", slug: "project-skeleton", model: "ProjectSkeletonConfigInput", source: "creation", title: "Project skeleton"},
  {stem: "mco_input", slug: "mco", model: "McoInput", source: "../mco/main", title: "MCO operations"},
  {stem: "mco_envelope", slug: "mco-envelope", model: "McoEnvelopeInput", source: "../mco/main", title: "MCO execution envelope"},
  {stem: "bom_pnp_config", slug: "bom-pnp", model: "BomPnpConfigInput", source: "bom-pnp-config", title: "BOM / PnP"},
  {stem: "clean_config", slug: "clean", model: "CleanConfigInput", source: "clean-config", title: "Clean"},
  {stem: "mate_config", slug: "mate", model: "MateConfigInput", source: "mate-config", title: "Mate"},
  {stem: "pcb_layer_step_config", slug: "pcb-layer-step", model: "PcbLayerStepConfigInput", source: "pcb-layer-step-config", title: "PCB layer STEP"},
  ...[
    ["design_review_manifest", "b0", "DesignReviewManifest"],
    ["megamaid_manifest", "b0", "MegamaidManifest"],
    ["schematic_svg_enrichment", "b0", "SchematicSvgEnrichment"],
    ["schematic_svg_manifest", "b0", "SchematicSvgManifest"],
    ["pcb_svg_component_layers", "a0", "PcbSvgComponentLayers"],
    ["pcb_svg_timings", "a0", "PcbSvgTimings"],
  ].map(([stem, version, model]) => ({stem, version, model, slug: stem.replaceAll("_", "-"),
    source: `../outputs/${stem.replaceAll("_", "-")}`, title: model, output: true})),
];
const json = (value) => JSON.stringify(value, null, 2) + "\n";
try {
  const result = spawnSync(process.execPath, [join(root, "node_modules/@typespec/compiler/cmd/tsp.js"),
    "compile", "src/tsp/altium_cruncher/config/main.tsp", "--config", "tspconfig.yaml",
    "--output-dir", temp, "--pretty=false"], {cwd: root, encoding: "utf8"});
  if (result.error) throw result.error;
  if (result.status !== 0) throw new Error(result.stdout + result.stderr);
  const emittedSchemas = new Map();
  for (const filename of readdirSync(join(temp, "schema")).sort()) {
    const emitted = JSON.parse(readFileSync(join(temp, "schema", filename), "utf8"));
    emittedSchemas.set(emitted.$id, {model: filename.slice(0, -5), schema: emitted});
    const declaration = emitted["x-acr-contract"];
    if (declaration) families.push({...declaration, model: filename.slice(0, -5),
      slug: declaration.slug || declaration.stem.replaceAll("_", "-"), output: declaration.kind === "output"});
  }
  if (new Set(families.map((family) => family.stem)).size !== families.length) throw new Error("Duplicate contract stem");
  if (new Set(families.map((family) => family.slug)).size !== families.length) throw new Error("Duplicate contract projection slug");
  for (const family of families) {
  const {stem, slug, model, source, title} = family;
  const banner = `Generated from ${posix.normalize(`src/tsp/altium_cruncher/config/${source}.tsp`)}. Do not edit.`;
  const validator = family.validator || `validate-${slug}`;
  const schema = JSON.parse(readFileSync(join(temp, `schema/${model}.json`), "utf8"));
  bundleReferences(schema, emittedSchemas);
  const metadata = {};
  for (const key of Object.keys(schema).filter((key) => key.startsWith("x-acr-"))) {
    metadata[key.slice(6)] = schema[key];
    delete schema[key];
  }
  annotateDefaults(schema, metadata["resolved-defaults"], schema);
  if (slug === "pcb-svg") {
    annotateDefaults(schema.$defs.ViewOptions, metadata["resolved-defaults"].view, schema);
    annotateDefaults(schema.$defs.ComponentOverride, metadata["resolved-defaults"].component, schema);
    metadata["schema"] = schema.properties.schema.anyOf.find((item) => item.const).const;
    metadata["special-layers"] = literals(schema.$defs.LayerOutputOptions.properties.include_special_layers.items);
    if (!metadata["special-layers"].length) throw new Error("Synthetic layer declaration is empty");
  } else {
    metadata["schema"] ??= schema.properties?.schema?.const;
    for (const definition of Object.values(schema.$defs || {})) annotateDefaults(definition, metadata["resolved-defaults"], schema);
  }
  lowerInputAnnotations(schema);
  if (slug === "mco") {
    const operations = [];
    for (const [name, definition] of Object.entries(schema.$defs || {})) {
      const info = definition["x-acr-operation"];
      if (!info) continue;
      const tags = literals(definition.properties.op);
      const argsRef = definition.properties.args.$ref;
      const args = schema.$defs[argsRef.split("/").at(-1)];
      const required = args.required || [];
      operations.push({...info, model: name, args_ref: argsRef,
        required_args: Object.keys(args.properties || {}).filter((key) => required.includes(key)),
        optional_args: Object.keys(args.properties || {}).filter((key) => !required.includes(key)),
        aliases: tags.filter((tag) => tag !== info.name)});
    }
    if (operations.length === 0) throw new Error("MCO operation catalog is empty");
    operations.sort((a, b) => a.group.localeCompare(b.group) || a.name.localeCompare(b.name));
    metadata.operations = operations;
    const names = operations.flatMap((operation) => [operation.name, ...operation.aliases]);
    for (const definition of Object.values(schema.$defs)) {
      if (definition.properties?.op?.["x-acr-custom-op"]) definition.properties.op.not = {enum: names};
    }
  }
  schema.$comment = banner;
  outputs.set(`docs/contracts/${stem}.${family.version || "a0"}.schema.json`, json(schema));
  outputs.set(`src/py/altium_cruncher/contracts/generated/${stem}.schema.json`, json(schema));
  outputs.set(`src/py/altium_cruncher/contracts/generated/${stem}.metadata.json`, json(metadata));
  outputs.set(`src/py/altium_cruncher/contracts/generated/${stem}.py`, pythonTypes(schema, model, banner));
  outputs.set(`src/ts/altium_cruncher_config/generated/${slug}.schema.json`, json(schema));
  outputs.set(`src/ts/altium_cruncher_config/generated/${slug}.metadata.json`, json(metadata));
  const typescriptSchema = structuredClone(schema);
  normalizeRecords(typescriptSchema);
  outputs.set(`src/ts/altium_cruncher_config/generated/${slug}.d.ts`, await compile({...typescriptSchema, title: model}, model, {
    bannerComment: `/** ${banner} */`, additionalProperties: false,
    declareExternallyReferenced: true, unknownAny: true,
  }));
  const ajv = new Ajv2020({strict: false, allErrors: true, code: {source: true, esm: true},
    useDefaults: false, coerceTypes: false, removeAdditional: false});
  ajv.addKeyword({keyword: "x-acr-input", schemaType: "string", code(cxt) {
    if (cxt.schema !== "number") return;
    const {data} = cxt;
    const numeric = cxt.parentSchema.anyOf[0];
    cxt.gen.if(_`typeof ${data} === "string" || typeof ${data} === "boolean"`, () => {
      cxt.fail(_`!Number.isFinite(Number(${data}))`);
      for (const [key, operator] of [["minimum", "<"], ["maximum", ">"], ["exclusiveMinimum", "<="], ["exclusiveMaximum", ">="]]) {
        if (numeric[key] === undefined) continue;
        const bound = numeric[key];
        const failure = {"<": _`Number(${data}) < ${bound}`, ">": _`Number(${data}) > ${bound}`,
          "<=": _`Number(${data}) <= ${bound}`, ">=": _`Number(${data}) >= ${bound}`}[operator];
        cxt.fail(failure);
      }
    });
  }});
  const validate = ajv.compile(schema);
  const validatorCode = standaloneCode(ajv, validate);
  const bundled = await build({stdin: {contents: validatorCode, resolveDir: root, sourcefile: "validate.js"},
    bundle: true, write: false, platform: "browser", format: "esm", legalComments: "inline"});
  outputs.set(`src/ts/altium_cruncher_config/generated/${validator}.js`, `// ${banner}\n${bundled.outputFiles[0].text}`);
  outputs.set(`src/ts/altium_cruncher_config/generated/${validator}.d.ts`, `/** ${banner} */
import type { ${model} } from './${slug}.js';
export interface ConfigError { instancePath: string; keyword: string; message?: string; }
export declare const validate: {
  (value: unknown): value is ${model};
  errors: ConfigError[] | null;
};
export default validate;
`);
  const lines = [`# ${title} ${family.output ? "output" : "configuration"} fields`, "", banner, "",
    family.output ? "Wire fields emitted by Cruncher. Validation preserves the payload without inserting defaults."
    : slug === "pcb-svg"
      ? "Authored overrides stay partial. Defaults are annotations, not values inserted when reading a file."
      : slug.startsWith("mco") ? "Authored MCO codecs preserve input fields and defaults; the execution envelope defers argument checks until a built-in operation is reached."
      : "Required paths/sections are checked at loading. Defaults describe generated templates or adapter fallbacks; codecs do not insert them.", "",
    family.output ? "See the contract authority inventory for producer locations and delegated upstream data boundaries."
    : slug === "pcb-svg"
      ? "The CLI applies presets, config overrides and explicit command choices afterward."
      : slug.startsWith("mco") ? "Execution, failure branches, custom registry behavior, dry-run checks and native CAD semantics remain Python behavior."
      : "Path resolution, normalization and native CAD semantics remain Python adapter behavior.", ""];
  for (const [name, model] of Object.entries({[family.model]: schema, ...schema.$defs})) {
    if (!model.properties) continue;
    lines.push(`## ${name}`, "", "| Field | Required | Default annotation | Description |", "| --- | --- | --- | --- |");
    for (const [key, value] of Object.entries(model.properties)) {
      const defaultText = value.default === undefined ? "—" : `\`${JSON.stringify(value.default)}\``;
      lines.push(`| \`${key}\` | ${(model.required || []).includes(key) ? "Yes" : "No"} | ${defaultText} | ${(value.description || "").replaceAll("|", "\\|").replaceAll("\n", " ")} |`);
    }
    lines.push("");
  }
  outputs.set(`docs/design/${slug}-config-fields.md`, lines.join("\n"));
  }
  const catalog = families.map((family) => ({stem: family.stem, model: family.model,
    kind: family.output ? "output" : "config", source: posix.normalize(`src/tsp/altium_cruncher/config/${family.source}.tsp`),
    schema: `docs/contracts/${family.stem}.${family.version || "a0"}.schema.json`,
    validator: family.validator || `validate-${family.slug}`, slug: family.slug}));
  outputs.set("src/py/altium_cruncher/contracts/generated/catalog.json", json(catalog));
  outputs.set("src/ts/altium_cruncher_config/generated/catalog.json", json(catalog));
  const pyApi = ['"""Generated contract transport entry points. Do not edit."""',
    'from typing import Literal, overload', 'from .._runtime import decode_config'];
  const tsApi = ['/** Generated contract transport entry points. Do not edit. */',
    'import { decodeConfig } from "../_runtime.js";'];
  for (const family of catalog) {
    pyApi.push(`from .${family.stem} import ${family.model}`);
    tsApi.push(`import type { ${family.model} } from "./${family.slug}.js";`,
      `import ${family.model}Validator from "./${family.validator}.js";`);
  }
  pyApi.push("");
  for (const family of catalog) pyApi.push('@overload',
    `def decode_contract(name: Literal["${family.stem}"], value: object) -> ${family.model}: ...`, "");
  pyApi.push('def decode_contract(name: str, value: object) -> object:',
    '    """Validate and copy authored JSON without applying defaults."""',
    `    if name not in ${JSON.stringify(catalog.map((family) => family.stem))}:`,
    '        raise ValueError(f"Unknown contract: {name}")',
    '    return decode_config(value, name, name)', '');
  tsApi.push('export interface ContractTypes {', ...catalog.map((family) => `  "${family.stem}": ${family.model};`), '}',
    'const validators = {', ...catalog.map((family) => `  "${family.stem}": ${family.model}Validator,`), '};',
    'export function decodeContract<K extends keyof ContractTypes>(name: K, value: unknown): ContractTypes[K] {',
    '  if (!Object.hasOwn(validators, name)) throw new Error(`Unknown contract: ${name}`);',
    '  return decodeConfig<unknown>(value, validators[name], name) as ContractTypes[K];', '}',
    'export function encodeContract<K extends keyof ContractTypes>(name: K, value: ContractTypes[K]): string {',
    '  return JSON.stringify(decodeContract(name, value), null, 2) + "\\n";', '}', '');
  outputs.set("src/py/altium_cruncher/contracts/generated/public.py", pyApi.join("\n"));
  outputs.set("src/ts/altium_cruncher_config/generated/public.ts", tsApi.join("\n"));
  for (const filename of readdirSync(join(root, "docs/contracts"))) {
    if (filename.endsWith(".schema.json") && !outputs.has(`docs/contracts/${filename}`)) {
      throw new Error(`Public schema lacks TypeSpec authority: ${filename}`);
    }
  }
  for (const [relative, content] of outputs) {
    const path = join(root, relative);
    if (check) {
      if (!existsSync(path) || readFileSync(path, "utf8") !== content) throw new Error(`Stale generated contract: ${relative}`);
    } else {
      mkdirSync(dirname(path), {recursive: true});
      writeFileSync(path, content, "utf8");
    }
  }
  console.log(`${check ? "Checked" : "Generated"} ${outputs.size} artifacts for ${families.length} contracts.`);
} finally {
  if (dirname(resolve(temp)) !== tempBase) throw new Error("Refusing cleanup outside the created temp directory");
  rmSync(temp, {recursive: true, force: true});
}

function bundleReferences(schema, catalog) {
  // Published contracts are self-contained: browser/Python validation never
  // performs network resolution, even when TypeSpec roots reference each other.
  const imported = new Map();
  const definitions = schema.$defs ||= {};
  const visit = (node, localPrefix = "") => {
    if (!node || typeof node !== "object") return;
    if (node.$ref?.startsWith("#/$defs/") && localPrefix) {
      node.$ref = `#/$defs/${localPrefix}${node.$ref.slice(8)}`;
    } else if (node.$ref && !node.$ref.startsWith("#")) {
      const target = catalog.get(node.$ref);
      if (!target) throw new Error(`Unresolved external contract reference: ${node.$ref}`);
      const key = `Imported${target.model}`;
      if (!imported.has(node.$ref)) {
        imported.set(node.$ref, key);
        const copy = structuredClone(target.schema);
        const children = copy.$defs || {};
        delete copy.$id; delete copy.$schema; delete copy.$defs;
        for (const name of Object.keys(copy).filter((name) => name.startsWith("x-acr-"))) delete copy[name];
        definitions[key] = copy;
        visit(copy, `${key}_`);
        for (const [name, child] of Object.entries(children)) {
          definitions[`${key}_${name}`] = child;
          visit(child, `${key}_`);
        }
      }
      node.$ref = `#/$defs/${key}`;
    }
    for (const [key, child] of Object.entries(node)) {
      if (key !== "$defs") visit(child, localPrefix);
    }
  };
  visit(schema);
  // Only the original definitions need the empty-prefix traversal.
  for (const [name, definition] of Object.entries(definitions)) {
    if (!name.startsWith("Imported")) visit(definition);
  }
}

function pythonTypes(schema, rootModel, banner) {
  const local = structuredClone(schema);
  const models = {[rootModel]: local, ...local.$defs};
  // TypeSpec emits inline objects for generic instantiations and anonymous
  // sections. Give them names instead of losing their fields to dict[str, object].
  const promote = (node, path, top = false) => {
    if (!node || typeof node !== "object") return;
    if (!top && node.type === "object" && Object.keys(node.properties || {}).length) {
      let name = path.replace(/[^a-zA-Z0-9_]/g, "_");
      while (Object.hasOwn(models, name)) name += "_";
      const model = structuredClone(node);
      models[name] = model;
      for (const key of Object.keys(node)) delete node[key];
      node.$ref = `#/$defs/${name}`;
      promote(model, name, true);
      return;
    }
    for (const [key, child] of Object.entries(node)) {
      if (["$defs", "default", "examples"].includes(key) || key.startsWith("x-")) continue;
      if (Array.isArray(child)) child.forEach((item, i) => promote(item, `${path}_${key}_${i}`));
      else if (key === "properties") for (const [field, value] of Object.entries(child)) promote(value, `${path}_${field}`);
      else promote(child, `${path}_${key}`);
    }
  };
  for (const [name, model] of Object.entries(models)) promote(model, name, true);
  const hasFields = (model) => Object.keys(model.properties || {}).length > 0;
  const type = (node) => {
    if (node.not && !Object.keys(node.not).length) return "Never";
    if (node.$ref) return node.$ref.split("/").at(-1);
    const literal = (value) => value === null ? "None" : value === true ? "True" : value === false ? "False" : JSON.stringify(value);
    if (node.const !== undefined) return `Literal[${literal(node.const)}]`;
    if (node.enum) return `Literal[${node.enum.map(literal).join(", ")}]`;
    if (node.anyOf) return [...new Set(node.anyOf.map(type))].join(" | ");
    if (node.oneOf) return [...new Set(node.oneOf.map(type))].join(" | ");
    if (node.type === "array") return `list[${type(node.items)}]`;
    if (node.type === "object") {
      const extra = node.additionalProperties ?? node.unevaluatedProperties;
      return `dict[str, ${extra === false || extra?.not ? "Never" : extra && typeof extra === "object" ? type(extra) : "object"}]`;
    }
    const result = {string: "str", boolean: "bool", number: "float", integer: "int", null: "None"}[node.type];
    if (result) return result;
    const structural = Object.keys(node).filter((key) => !key.startsWith("x-") && !["description", "default", "title"].includes(key));
    if (structural.length) throw new Error(`Unsupported Python contract shape: ${JSON.stringify(node)}`);
    return "object";
  };
  const lines = [`"""${banner}"""`, "", "from __future__ import annotations", "", "from typing import Literal, Never, NotRequired", "from typing_extensions import TypedDict", ""];
  // Functional TypedDict syntax preserves wire keys such as 'global'. Forward refs
  // also allow model declaration order to follow the schema's deterministic order.
  for (const [name, model] of Object.entries(models)) {
    if (!hasFields(model)) continue;
    for (const parent of model.allOf || []) {
      // Conditional constraints narrow values, without adding transport fields.
      if (parent.if && parent.then) continue;
      const inherited = models[parent.$ref?.split("/").at(-1)];
      if (!inherited || hasFields(inherited)) throw new Error(`Unsupported non-record inheritance in ${name}`);
    }
    lines.push(`${name} = TypedDict(${JSON.stringify(name)}, {`);
    for (const [key, field] of Object.entries(model.properties)) {
      const value = type(field);
      lines.push(`    ${JSON.stringify(key)}: ${(model.required || []).includes(key) ? JSON.stringify(value) : `NotRequired[${JSON.stringify(value)}]`},`);
    }
    let extra = model.additionalProperties;
    if (extra === undefined && model.allOf?.some((item) => item.$ref)) {
      const parent = models[model.allOf.find((item) => item.$ref).$ref.split("/").at(-1)];
      extra = parent.additionalProperties ?? parent.unevaluatedProperties;
    }
    // PEP 728 preserves typed extra items instead of silently closing an open
    // TypeSpec Record when producing Python's known-field view.
    lines.push(extra !== undefined && extra !== false && !extra?.not
      ? `}, extra_items=${typeof extra === "object" ? JSON.stringify(type(extra)) : "object"})`
      : "}, closed=True)", "");
  }
  const emitted = new Set(Object.keys(models).filter((name) => hasFields(models[name])));
  const emitAlias = (name, pending = new Set()) => {
    if (emitted.has(name)) return;
    if (pending.has(name)) throw new Error(`Recursive alias unsupported: ${name}`);
    pending.add(name);
    const expression = type(models[name]);
    for (const dependency of Object.keys(models)) {
      if (dependency !== name && new RegExp(`\\b${dependency}\\b`).test(expression)) emitAlias(dependency, pending);
    }
    lines.push(`${name} = ${expression}`);
    emitted.add(name);
    pending.delete(name);
  };
  for (const name of Object.keys(models)) emitAlias(name);
  return lines.join("\n").trimEnd() + "\n";
}

function normalizeRecords(node) {
  if (!node || typeof node !== "object") return;
  // For leaf record declarations only, these keywords are equivalent. Do not
  // rewrite closure on composed objects where evaluated-property tracking matters.
  if (node.type === "object" && !Object.keys(node.properties || {}).length && !node.allOf && !node.anyOf &&
      node.unevaluatedProperties && !node.unevaluatedProperties.not) {
    node.additionalProperties ??= node.unevaluatedProperties;
    delete node.unevaluatedProperties;
  }
  for (const [key, value] of Object.entries(node)) {
    // The type emitter understands boolean false as never, but not not:{}.
    if (value && typeof value === "object" && value.not && !Object.keys(value.not).length) {
      node[key] = false;
      continue;
    }
    if (Array.isArray(value)) value.forEach(normalizeRecords);
    else normalizeRecords(value);
  }
}

function literals(node) {
  return [...new Set([...(node.enum || []), ...(typeof node.const === "string" ? [node.const] : []),
    ...(node.anyOf || []).flatMap(literals)])];
}

function annotateDefaults(node, value, rootSchema) {
  if (node.$ref) node = rootSchema.$defs[node.$ref.split("/").at(-1)];
  if (node.anyOf) {
    const objectBranch = node.anyOf.find((branch) => branch.$ref || branch.type === "object");
    if (objectBranch) return annotateDefaults(objectBranch, value, rootSchema);
  }
  if (!node.properties || !value || typeof value !== "object" || Array.isArray(value)) return;
  for (const [key, field] of Object.entries(node.properties)) {
    if (!(key in value)) continue;
    if (value[key] === null || typeof value[key] !== "object") field.default = value[key];
    annotateDefaults(field, value[key], rootSchema);
  }
}

function lowerInputAnnotations(node) {
  if (!node || typeof node !== "object") return;
  for (const child of Object.values(node)) {
    if (Array.isArray(child)) child.forEach(lowerInputAnnotations);
    else lowerInputAnnotations(child);
  }
  const kind = node["x-acr-input"];
  if (!kind && !node["x-acr-nullable"]) return;
  const annotations = {};
  for (const key of ["description", "default", "x-acr-input", "x-acr-nullable", "x-acr-trim"]) {
    if (key in node) { annotations[key] = node[key]; delete node[key]; }
  }
  const canonical = structuredClone(node);
  const branches = [canonical];
  if (annotations["x-acr-nullable"]) branches.push({type: "null"});
  if (kind === "boolean") {
    branches.push({type: "number"}, {type: "string", pattern: "^\\s*(?:1|0|[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]|[yY][eE][sS]|[nN][oO]|[oO][nN]|[oO][fF][fF])\\s*$"});
  } else if (kind === "number") {
    branches.push({type: "boolean"}, {type: "string", pattern: "^\\s*[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?\\s*$"});
  } else if (kind === "enum") {
    const values = [];
    const collect = (item) => {
      if (typeof item.const === "string") values.push(item.const);
      if (item.enum) values.push(...item.enum.filter((v) => typeof v === "string"));
      item.anyOf?.forEach(collect);
    };
    collect(canonical);
    if (!values.length) throw new Error("Input enum annotation has no literal values");
    const escaped = (value) => value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const pattern = values.map((value) => [...value].map((c) => /[a-z]/i.test(c) ? `[${c.toLowerCase()}${c.toUpperCase()}]` : escaped(c)).join("")).join("|");
    const space = annotations["x-acr-trim"] === false ? "" : "\\s*";
    branches.push({type: "string", pattern: `^${space}(?:${pattern})${space}$`});
  }
  for (const key of Object.keys(node)) delete node[key];
  Object.assign(node, {anyOf: branches}, annotations);
}
