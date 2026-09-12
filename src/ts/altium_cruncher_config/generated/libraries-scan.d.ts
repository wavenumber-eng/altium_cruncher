/** Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit. */

export interface LibrariesScan {
  schema: "altium_cruncher.libraries.scan.a0";
  roots: string[];
  recursive: boolean;
  symbols: LibraryEntry[];
  footprints: LibraryEntry[];
  warnings: string[];
}
export interface LibraryEntry {
  name: string;
  library: string;
}
