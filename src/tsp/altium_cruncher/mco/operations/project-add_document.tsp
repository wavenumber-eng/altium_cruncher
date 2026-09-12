import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model ProjectAddDocumentArgs extends Record<unknown> {
  file: McoString;
  document: McoString;
  unique_id?: string | null = null;
}

@extension(
  "x-acr-operation",
  #{
    name: "project.add_document",
    group: "project",
    summary: "Append a document entry to a .PrjPcb file.",
  }
)
model ProjectAddDocumentOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "project.add_document";
  args: ProjectAddDocumentArgs;
}
