import "../common.tsp";
using TypeSpec.JsonSchema;
namespace Wavenumber.AltiumCruncher.Mco;

model PcbdocCreateUserUnionArgs extends Record<unknown> {
  ...MutationArgs;
  name: McoString;
  members?: "all" | null = "all";
}

@extension(
  "x-acr-operation",
  #{
    name: "pcbdoc.create_user_union",
    group: "pcbdoc",
    summary: "Create a user union over generated PCB objects.",
  }
)
model PcbdocCreateUserUnionOperation extends Record<unknown> {
  ...OperationFields;
  `op`: "pcbdoc.create_user_union";
  args: PcbdocCreateUserUnionArgs;
}
