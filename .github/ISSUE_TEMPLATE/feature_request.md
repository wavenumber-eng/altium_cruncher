---
name: Feature request
about: Propose a public command, config, output, or workflow improvement
title: ""
labels: enhancement
assignees: ""
---

## Summary

What should change?

## User Story

As a ..., I want ..., so that ...

Describe the PCB/library workflow this supports and why the current behavior is
not enough.

## Commands

List the command or commands this affects.

```powershell
altium-cruncher <command> ...
```

## Proposed Options Or Config

List the CLI arguments, config fields, defaults, and allowed values you expect.

```jsonc
{
  // example config option
}
```

## Expected Outputs

Describe expected files, stdout/stderr behavior, exit codes, generated JSON,
SVG, STEP, library artifacts, or other outputs.

## Acceptance Criteria

- [ ] Command help documents the new behavior
- [ ] Config comments document all new options, if config-driven
- [ ] Design docs cover usage, arguments, outputs, and tests
- [ ] Contract docs and tests cover stable JSON/config/API behavior, if changed

## Public Contract Impact

- [ ] New or changed CLI argument
- [ ] New or changed config option
- [ ] New or changed JSON/API output
- [ ] New or changed generated file/artifact
- [ ] New dependency
- [ ] Documentation only

## Alternatives

Mention any workaround or existing command you considered.

## Files Or Examples

Attach only files that can be shared publicly. Small synthetic examples are
preferred for tests.
