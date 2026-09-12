// Build a browser-targeted consumer and run the same authored vectors as Python.
import { build } from "esbuild";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { pathToFileURL, fileURLToPath } from "node:url";
import assert from "node:assert/strict";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const tempBase = resolve(tmpdir());
const temp = mkdtempSync(join(tempBase, "acr-browser-contract-"));
try {
  const outfile = join(temp, "config.mjs");
  const built = await build({entryPoints: [join(root, "src/ts/altium_cruncher_config/index.ts")],
    bundle: true, platform: "browser", format: "esm", outfile, metafile: true});
  assert.equal(Object.values(built.metafile.outputs).flatMap((output) => output.imports).length, 0);
  const api = await import(pathToFileURL(outfile));
  const {decodePcbSvgConfig, encodePcbSvgConfig} = api;
  const vectors = JSON.parse(readFileSync(join(root, "tests/fixtures/pcb-svg-config-vectors.json"), "utf8"));
  for (const vector of vectors) {
    const value = structuredClone(vector.value);
    if (!vector.valid) { assert.throws(() => decodePcbSvgConfig(value), undefined, vector.name); continue; }
    const decoded = decodePcbSvgConfig(value);
    assert.deepEqual(decoded, vector.value, vector.name);
    assert.deepEqual(value, vector.value, vector.name);
    assert.deepEqual(JSON.parse(encodePcbSvgConfig(decoded)), vector.value, vector.name);
  }
  for (const value of [NaN, Infinity, undefined, 1n, new Date()]) {
    assert.throws(() => decodePcbSvgConfig({global: {styles: {custom: {value}}}}));
  }
  const creation = JSON.parse(readFileSync(join(root, "tests/fixtures/creation-config-vectors.json"), "utf8"));
  const names = {schdoc: "SchdocCreate", pcbdoc: "PcbdocCreate", project: "ProjectSkeleton"};
  for (const vector of creation) {
    const decode = api[`decode${names[vector.family]}Config`];
    const encode = api[`encode${names[vector.family]}Config`];
    const value = structuredClone(vector.value);
    if (!vector.valid) { assert.throws(() => decode(value), undefined, vector.name); continue; }
    assert.deepEqual(decode(value), vector.value, vector.name);
    assert.deepEqual(JSON.parse(encode(decode(value))), vector.value, vector.name);
    assert.deepEqual(value, vector.value, vector.name);
  }
  const mco = JSON.parse(readFileSync(join(root, "tests/fixtures/mco-contract-vectors.json"), "utf8"));
  for (const vector of mco) {
    const value = structuredClone(vector.value);
    if (!vector.valid) { assert.throws(() => api.decodeMco(value), undefined, vector.name); continue; }
    assert.deepEqual(api.decodeMco(value), vector.value, vector.name);
    assert.deepEqual(JSON.parse(api.encodeMco(api.decodeMco(value))), vector.value, vector.name);
    assert.deepEqual(value, vector.value, vector.name);
  }
  const workflows = JSON.parse(readFileSync(join(root, "tests/fixtures/workflow-contract-vectors.json"), "utf8"));
  for (const vector of workflows) {
    const value = structuredClone(vector.value);
    if (!vector.valid) { assert.throws(() => api.decodeContract(vector.contract, value), undefined, vector.name); continue; }
    const decoded = api.decodeContract(vector.contract, value);
    assert.deepEqual(decoded, vector.value, vector.name);
    assert.deepEqual(JSON.parse(api.encodeContract(vector.contract, decoded)), vector.value, vector.name);
    assert.deepEqual(value, vector.value, vector.name);
  }
  console.log(`${vectors.length + creation.length + mco.length + workflows.length} shared browser vectors passed; bundle has no external imports.`);
} finally {
  if (dirname(resolve(temp)) !== tempBase) throw new Error("Refusing cleanup outside the created temp directory");
  rmSync(temp, {recursive: true, force: true});
}
