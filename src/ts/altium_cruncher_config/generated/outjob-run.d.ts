/** Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit. */

export interface OutjobRun {
  schema: "altium_cruncher.outjob.run.a0";
  project: string;
  success: boolean;
  results: OutjobResult[];
}
export interface OutjobResult {
  project: string;
  outjob: string;
  success: boolean;
  launch_code: number;
  timed_out: boolean;
  error_count: number;
  marker_text: string;
  normalized_changed: boolean;
  rebound_document_paths: number;
  marker_path: string;
  log_path: string;
}
