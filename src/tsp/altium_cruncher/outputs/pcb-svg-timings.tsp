import "@typespec/json-schema";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.PcbSvgTimingsContract;

model PcbSvgTimingsModelCacheObjectCounts {
  @extension("minimum", 0)
  hits: integer;

  @extension("minimum", 0)
  misses: integer;

  @extension("minimum", 0)
  writes: integer;

  @extension("minimum", 0)
  invalid: integer;

  @extension("minimum", 0)
  evictions: integer;
}

model PcbSvgTimingsModelCacheObject {
  directory: string;
  counts: PcbSvgTimingsModelCacheObjectCounts;

  @extension("minimum", 0)
  read_seconds: float64;

  @extension("minimum", 0)
  write_seconds: float64;
}

model PcbSvgTimingsEventsItem {
  @extension("minimum", 0)
  id: integer;

  @extension("minimum", 0)
  parent_id: integer | null;

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

  @extension("minimum", 0)
  seconds: float64;

  @extension("minimum", 0)
  exclusive_seconds: float64;
}

@jsonSchema
@id("pcb.svg.timings.a0")
@extension("title", "PCB SVG job wall timings")
model PcbSvgTimings {
  schema: "pcb.svg.timings.a0";
  clock: "wall";

  @extension("minimum", 1)
  workers?: integer;

  notes: string;
  model_cache?: PcbSvgTimingsModelCacheObject | null;
  events: PcbSvgTimingsEventsItem[];
}
