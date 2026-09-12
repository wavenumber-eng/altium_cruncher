/** Generated from src/tsp/altium_cruncher/config/creation.tsp. Do not edit. */

export type SchdocCreateConfigInput = RecordUnknown & {
  /**
   * SchDoc create config contract id.
   */
  schema: "altium_cruncher.schdoc.create.config.a0";
  /**
   * SchDoc file to create, relative to this config file unless absolute.
   */
  file: string;
  /**
   * Altium SheetStyle enum name or native integer id. Falsy input uses D.
   */
  sheet_style?: string | number | boolean | null;
  /**
   * Optional SchDot template file to copy settings from.
   */
  template?: NonemptyString | null;
  /**
   * Whether to copy visual sheet settings from the template; legacy JSON truthiness is preserved. Prefer true or false.
   */
  apply_template_visual_sheet_settings?: boolean | string | number | null | unknown[] | RecordUnknown;
  /**
   * Optional explicit sheet size in mils.
   */
  custom_sheet_mils?: CustomSheetMils | null;
};
export type NonemptyString = string;
export type CustomSheetMils = RecordUnknown & {
  /**
   * Custom sheet width in mils.
   */
  width: number | boolean;
  /**
   * Custom sheet height in mils.
   */
  height: number | boolean;
};

export interface RecordUnknown {
  [k: string]: unknown;
}
