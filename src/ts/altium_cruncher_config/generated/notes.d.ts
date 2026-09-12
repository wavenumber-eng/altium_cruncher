/** Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit. */

export type Count = number;

export interface Notes {
  schema: "altium_cruncher.notes.a0";
  input: string;
  source_kind: "schdoc" | "prjpcb";
  path_base: "input_directory";
  schdoc_count: Count;
  filters: NoteFilters;
  schdocs: NotesPage[];
}
export interface NoteFilters {
  include_sheet_template_text: boolean;
  default_suppression: string;
}
export interface NotesPage {
  file: string;
  notes?: Note[];
  text_frames?: Note[];
  free_text?: Note[];
}
export interface Note {
  text: string;
  position_mils: Point | null;
  unique_id?: string;
  bounds_mils?: Bounds;
  author?: string | number | boolean;
}
export interface Point {
  x: number;
  y: number;
}
export interface Bounds {
  x_min: number;
  y_min: number;
  x_max: number;
  y_max: number;
}
