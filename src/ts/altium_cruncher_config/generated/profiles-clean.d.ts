/** Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit. */

export interface ProfilesClean {
  schema: "altium_cruncher.profiles.clean.a0";
  actions: ProfileCleanAction[];
}
export interface ProfileCleanAction {
  profile_guid: string;
  profile_name: string;
  profile_path: string;
  module_name: string;
  module_dir: string;
  removed_module_dir: boolean;
  removed_registry_item: boolean;
  dry_run: boolean;
}
