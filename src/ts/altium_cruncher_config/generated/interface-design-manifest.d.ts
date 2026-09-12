/** Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit. */

export type NamedInterface = RecordUnknown & {
  name: string;
};

/**
 * Cruncher-owned interface inventory consumed by documentation signoff; command_manifest remains wn-dev-std-owned.
 */
export interface InterfaceDesignManifest {
  schema: "altium_cruncher.interface_design_manifest.a0";
  major_interfaces: (string | NamedInterface)[];
}
export interface RecordUnknown {
  [k: string]: unknown;
}
