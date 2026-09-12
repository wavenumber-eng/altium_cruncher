import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model ProjectAddParameterArgs extends Record<unknown> {
  file: McoString;
  name: McoString;
  value: McoString;
}

@extension(
  "x-acr-operation",
  #{
    name: "project.add_parameter",
    group: "project",
    summary: "Set one project parameter.",
  }
)
model ProjectAddParameterOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "project.add_parameter";
  args: ProjectAddParameterArgs;
}
