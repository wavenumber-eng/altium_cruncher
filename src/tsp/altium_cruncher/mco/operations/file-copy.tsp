import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model FileCopyArgs extends Record<unknown> {
  source: McoString;
  destination: McoString;
  overwrite?: boolean | null = false;
}

@extension(
  "x-acr-operation",
  #{
    name: "file.copy",
    group: "file",
    summary: "Copy one file into the workflow output tree.",
  }
)
model FileCopyOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "file.copy";
  args: FileCopyArgs;
}
