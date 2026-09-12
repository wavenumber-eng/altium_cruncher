import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model ProjectCreateArgs extends Record<unknown> {
  file: McoString;
  name?: string | null = null;
  project_name?: string | null = null;
  overwrite?: boolean | null = false;
}

@extension(
  "x-acr-operation",
  #{
    name: "project.create",
    group: "project",
    summary: "Create an empty .PrjPcb file.",
  }
)
model ProjectCreateOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "project.create";
  args: ProjectCreateArgs;
}
