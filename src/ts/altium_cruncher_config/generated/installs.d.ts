/** Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit. */

export interface Installs {
  schema: "altium_cruncher.installs.a0";
  installs: Install[];
}
export interface Install {
  name: string;
  label: string;
  major: number | null;
  root: string;
  x2_path: string;
  runtime_tfm: string | null;
  registry_version: string | null;
  unique_id: string | null;
  source: string;
}
