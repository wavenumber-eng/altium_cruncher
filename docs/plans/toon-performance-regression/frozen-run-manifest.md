+++
type = "plan_log"
id = "toon-performance-frozen-run-manifest"
plan_id = "toon-performance-regression"
step_id = "freeze-benchmark-environments"
created = "2026-09-20T22:00:00-04:00"
+++

# Frozen benchmark manifest

Status: environment freeze complete; diagnostic single-run census complete

## Host and launcher

- host: `WN2`;
- OS: Microsoft Windows 11 Pro 10.0.26200, build 26200;
- CPU: AMD Ryzen 9 9950X 16-Core Processor, 32 logical processors;
- physical memory: 66,125,668,352 bytes;
- `uv`: 0.9.15 (`5eafae332`, 2025-12-02);
- Python: CPython 3.14.1;
- Python executable SHA-256 (both environments):
  `5037B26DFAFA528A5E16F40302EBB3215A0F7CD201CC4F061C4A801A33F7FE72`.

## Detached environments

| Candidate | Commit | Worktree | `uv.lock` SHA-256 | Cruncher | Monkey | Geometer |
| --- | --- | --- | --- | --- | --- | --- |
| pre-clipping | `79bb81e88108c1c79a0a7d5caf2973203187d32c` | `C:\eli\agent-worktrees\altium-cruncher-performance\pre-2026.9.18` | `A41DE1F50D66F6F64DDF6BE77D5F7D3690625D176D5207112FECF5C1BD2EBE83` | 2026.9.18 | 2026.9.18 | 2026.9.13 |
| corrected | `bb76253d95c2c38a6dc764a9ac036e2dc27c4cbf` | `C:\eli\agent-worktrees\altium-cruncher-performance\corrected-bb76253` | `AC1C078041F05F0E3C4CECE56D288608D2CD8248402951D999A52EF95940CD37` | 2026.9.20 | 2026.9.19 | 2026.9.19 |

Both worktrees were created detached and synchronized with
`uv sync --frozen --all-extras`. Their complete `uv pip freeze` sets are
identical except for the editable Cruncher candidate, `altium-monkey`, and
`wn-geometer`. The common resolved packages are:

`attrs==26.1.0`, `build==1.5.0`, `certifi==2026.5.20`,
`charset-normalizer==3.4.7`, `colorama==0.4.6`, `docutils==0.22.4`,
`easyeda-monkey==2026.9.11`, `et-xmlfile==2.0.0`, `freetype-py==2.5.1`,
`id==1.6.1`, `idna==3.16`, `iniconfig==2.3.0`, `jaraco-classes==3.4.0`,
`jaraco-context==6.1.2`, `jaraco-functools==4.5.0`,
`json-with-comments==1.2.10`, `jsonschema==4.26.0`,
`jsonschema-rs==0.48.5`, `jsonschema-specifications==2025.9.1`,
`keyring==25.7.0`, `lxml==6.0.2`, `lz4==4.4.5`,
`markdown-it-py==4.2.0`, `mdurl==0.1.2`, `more-itertools==11.1.0`,
`msgspec==0.21.1`, `nh3==0.3.5`, `nodeenv==1.10.0`, `numpy==2.5.3`,
`openpyxl==3.1.5`, `packaging==26.2`, `pillow==12.3.0`,
`pluggy==1.6.0`, `pygments==2.20.0`, `pyproject-hooks==1.2.0`,
`pyright==1.1.409`, `pytest==9.0.3`, `pytest-json-report==1.5.0`,
`pytest-metadata==3.1.1`, `pywin32-ctypes==0.2.3`,
`readme-renderer==44.0`, `referencing==0.37.0`, `requests==2.34.2`,
`requests-toolbelt==1.0.0`, `resvg-py==0.5.0`, `rfc3986==2.0.0`,
`rich==15.0.0`, `rpds-py==2026.5.1`, `ruff==0.15.14`,
`shapely==2.1.2`, `tomli-w==1.2.0`, `twine==6.2.0`,
`typing-extensions==4.15.0`, `uharfbuzz==0.54.1`, `urllib3==2.7.0`, and
`wn-rack==1.1.0`.

Geometer launcher/native SHA-256 values are:

| Candidate | launcher | packaged native executable |
| --- | --- | --- |
| 2026.9.13 | `ADCE7568204DD3766EA2926D75224D9D7EE963DB7921EBFF53F4039E71A8A63A` | `A87E1A5ED0B0E9BAE5C35119CCDA0B31642D9CB28775B7F060EC4EA43B417A1A` |
| 2026.9.19 | `E255BF1336EF78398F7A0840614BDF7ACB0A1C49275CBF569044E6A37FDDD2F8` | `882BADC245D1611F72F6A87E7D2B3DE2039F46FB6EA470BCAD612788B52D5095` |

## Controlled input and exact argv

- RT Super input SHA-256:
  `BCF91A9B0A77AA9294BCD44B8148D1F4202A164BBAF6BBEF5E82F0BFD7834C94`;
- config SHA-256:
  `E2282C385990BBCD13F3A6E5716D836C93B20F5A8A14B1119E8E157A1DC51911`;
- cache: disabled;
- worker count: one.

Each candidate ran this argv from its frozen worktree, substituting only its
unique output and timings paths:

```text
uv run acr toon C:\eli\wn-hw\altium_cruncher\tests\assets\projects\rt_super_c1\input\RT_SUPER_C1.PrjPcb --output OUTPUT --config C:\eli\wn-hw\altium_cruncher\temp\toon-performance-ab\rt-super-c1\pre-clipping-2026.9.18.config.jsonc --no-cache --workers 1 --timings OUTPUT\timings.json
```

## Diagnostic result

These are single diagnostic runs, not release statistics.

| Candidate | wall, s | Geometer calls | model illustration calls | native request attachment bytes | SVG bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2026.9.18 | 5.413 uninstrumented / 2.673 call-probed | 40 | 36 A0 | 4,443,947 | 3,766,900 |
| corrected | 10.462 uninstrumented / 9.877 call-probed | 472 | 466 B0 | 26,437,243 | 12,550,726 |

The corrected call-probed run spends 6.160 seconds in 466 model illustration
operations. The pre-clipping run spends 0.641 seconds in 36 such operations.
This proves that request multiplication, not merely a slower native operation,
is a primary RT Super regression mechanism. It does not yet isolate the A0/B0
per-request native cost.

Ten immediate replays of the first top-side direct model use the same 38,950
byte STEP payload in both environments (SHA-256
`0B5AC1DE9B5728598A705CF1BDCE4BB4F94BF84EAAA981715E4C788127B891AB`).
The Geometer 2026.9.13 A0 request has a 7.939 ms median and the 2026.9.19 B0
uncut request has an 8.078 ms median. This matched-model evidence attributes
the material RT Super cost to request multiplication rather than per-request
native-kernel regression.

Structural census of the uninstrumented SVGs:

| Candidate/view | elements | uses | surface uses | aperture uses | path commands |
| --- | ---: | ---: | ---: | ---: | ---: |
| pre/top | 5,100 | 50 | 50 | 0 | 30,690 |
| pre/bottom | 3,241 | 107 | 107 | 0 | 35,608 |
| corrected/top | 25,162 | 235 | 126 | 109 | 61,571 |
| corrected/bottom | 32,005 | 233 | 107 | 126 | 91,685 |

Raw profiles and SVGs are ignored under
`C:\eli\wn-hw\altium_cruncher\temp\toon-performance-frozen`.

## Loz Old Man scale census

One cache-disabled, one-worker call-probed diagnostic run produces:

| Candidate | wall, s | Geometer calls | model illustration calls | model illustration time, s | model attachment bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2026.9.18 | 16.272 | 96 | 93 A0 | 11.864 | 34,163,690 |
| corrected | 45.896 | 552 | 547 B0 | 36.848 | 121,599,021 |

Loz therefore confirms the RT mechanism at scale: corrected model-illustration
count grows 5.88x while wall time grows 2.82x. This is consistent with the
current occurrence-specific clipping identity preventing the reusable
projection grouping present before clipping.

## Same-code RT controls

Instrumentation-only normal behavior takes 10.008 seconds, makes 466 model
illustration calls, and emits 12,550,726 SVG bytes. Two deliberately invalid
attribution controls show:

- omitting only aperture SVG definitions/instances retains all 466 calls and
  emits 7,687,821 bytes; its 11.227 second single run provides no evidence of a
  runtime win, while proving that aperture composition accounts for 38.7
  percent of output bytes and a large DOM fraction;
- returning only the uncut projection removes 154 clipped calls, takes 8.342
  seconds, and emits 9,929,656 bytes.

The remaining 312 uncut direct-model calls in the second control are the next
optimization target. The safe design must restore projection reuse without
reusing an occurrence's region decision, clipped plane, warnings, or aperture
eligibility on another occurrence.
