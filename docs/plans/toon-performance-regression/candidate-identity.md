+++
type = "plan_log"
id = "toon-performance-candidate-identity"
plan_id = "toon-performance-regression"
step_id = "release-requalification"
created = "2026-09-20T23:55:00-04:00"
+++

# Exact remediated candidate identity

Status: source, contract, development-standard, workflow, and visual-equivalence
checks pass; owner-authorized branch commit and CI processing are next

This records the qualified pre-commit candidate immediately before the
owner-authorized branch push. Its frozen Git content identity is:

- base HEAD: `9ddec7435640bb91eacab4fff71c38b3f0e2542e`;
- tracked binary-diff Git hash: `d578ae8ca93463a7c10fea63da11896e8596a61b`;
- nine-file untracked manifest Git hash:
  `9edd8233baf3c5999fa04043d92b9eed47ab18e7`;
- composite candidate Git hash:
  `4f45b0f439d5607a9d33f36d7d7fe1a4dd20fa04`.

The composite is the Git object hash of `HEAD`, the tracked-diff hash, and the
untracked-manifest hash separated by newlines. The tracked diff is
`git diff --binary HEAD`; the untracked manifest is the ordinally sorted output
of `git ls-files --others --exclude-standard` formatted as each file's
`git hash-object` plus path. This identity document alone is excluded to avoid
a self-referential digest. Ignored benchmark and gallery outputs are evidence,
not candidate source.

Qualification on this exact candidate:

- Rack: 95 passed, one expected skip, zero failures;
- focused audit regressions: 111 passed;
- independent follow-up audit suite: 124 passed;
- contract freshness: 465 generated artifacts across 46 contracts;
- TypeScript and browser checks: pass, including 126 browser vectors;
- Wavenumber development standard: all 20 checks pass;
- RT Super and Loz Old Man top/bottom SVGs: byte-identical to the previously
  qualified optimized outputs when using the frozen benchmark config;
- a fresh default RT Super render resolves its white mask to black physical
  silkscreen on both sides and passes the complete Rack/contract checks.
- the reusable review gallery uses a solid-white, vector-native pan/zoom canvas.

The exact final-audit gallery is
`C:\eli\wn-hw\altium_cruncher\temp\toon-performance-frozen\final-audit\review\index.html`.
The auto-contrast RT Super review is
`C:\eli\wn-hw\altium_cruncher\temp\silkscreen-auto-contrast\output\index.html`.
No package was built, published, or released; repository CI owns package-build
qualification after the candidate is committed and pushed on owner approval.
