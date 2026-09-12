/** Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit. */

export interface Profiles {
  schema: "altium_cruncher.profiles.a0";
  profiles: Profile[];
}
export interface Profile {
  name: string;
  guid: string;
  path: string;
  extensions_root: string;
  registry_path: string;
  registry_exists: boolean;
  module_name: string;
  module_dir: string;
  module_dir_exists: boolean;
  registered: boolean;
  registry_version: string | null;
  dll_path: string;
  dll_exists: boolean;
  last_write_time_utc: string | null;
}
