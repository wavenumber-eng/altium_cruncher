# Local Inputs

Place local Altium source projects here before running the cricket-node
example. These files are ignored by Git.

Expected layout:

```text
input/
  cricket-node/
    11-10028__cricket-node-hw__B.PrjPcb
    cricket-node-hw__B.PcbDoc
    ...
  node-test-array/
    11-10077__node-test-array__B4.PrjPcb
    ...
```

With `WN_TEST_CORPUS` set, the local corpus copies can be staged with:

```powershell
New-Item -ItemType Directory -Force input\cricket-node, input\node-test-array
Copy-Item "$env:WN_TEST_CORPUS\altium\common\real_world_pcbdoc\cricket-node\input\*" input\cricket-node\ -Recurse -Force
Copy-Item "$env:WN_TEST_CORPUS\altium\common\real_world_pcbdoc\node_test_array\input\*" input\node-test-array\ -Recurse -Force
```
