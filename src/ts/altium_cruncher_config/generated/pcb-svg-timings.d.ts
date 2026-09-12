/** Generated from src/tsp/altium_cruncher/outputs/pcb-svg-timings.tsp. Do not edit. */

export interface PcbSvgTimings {
  schema: "pcb.svg.timings.a0";
  clock: "wall";
  workers?: number;
  notes: string;
  model_cache?: PcbSvgTimingsModelCacheObject | null;
  events: PcbSvgTimingsEventsItem[];
}
export interface PcbSvgTimingsModelCacheObject {
  directory: string;
  counts: PcbSvgTimingsModelCacheObjectCounts;
  read_seconds: number;
  write_seconds: number;
}
export interface PcbSvgTimingsModelCacheObjectCounts {
  hits: number;
  misses: number;
  writes: number;
  invalid: number;
  evictions: number;
}
export interface PcbSvgTimingsEventsItem {
  id: number;
  parent_id: number | null;
  stage: string;
  command?: string;
  board?: string;
  variant?: string;
  view?: string;
  side?: "top" | "bottom" | "both" | "board";
  layer?: string;
  part?: string;
  cache: "none" | "built" | "hit" | "assembled" | "disabled";
  failed: boolean;
  seconds: number;
  exclusive_seconds: number;
}
