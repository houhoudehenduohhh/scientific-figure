---
name: scientific-figure
description: Plan, build, independently audit, render, and quality-check scientific figures through explicit Figure Spec gates. Use for project figure work that produces files or code; do not use for a one-off plotting explanation.
---

# Scientific Figure

Use one current Figure Spec and one current Figure Code Spec to drive a four-stage workflow. The project decides the scientific claim, data mapping, plotting backend, runtime, output path, and presentation profile.

## Route by state

| State | Stage | Read |
|---|---|---|
| No approved figure specs or the user is revising the design | Figure Spec | [references/spec-stage.md](references/spec-stage.md) |
| Both specs are approved and draft plotting code is requested or missing | Build | [references/build-stage.md](references/build-stage.md) |
| Draft plotting code exists and the current audit has not received a user decision | Audit | [references/audit-stage.md](references/audit-stage.md) |
| Audit is accepted by the user and rendering is explicitly authorized | Render & QA | [references/render-qa-stage.md](references/render-qa-stage.md) |

Complete only the earliest stage whose gate is incomplete. A request that combines planning and rendering stops at the current Spec gate.

## Resolve the current project state

Inspect the user request, project files, current specs, source data or approved result artifacts, draft code, audit report, and output state. Resolve paths, runtime, backend, and output format from:

1. explicit user instructions;
2. existing project configuration and approved specs;
3. reliable read-only discovery;
4. a focused question when a material choice remains unresolved.

Reference images are optional. If supplied, analyze them; if absent, design from the scientific or communication objective and the Figure Spec.

## Current spec and approval rules

- Keep one current Figure Spec and one current Figure Code Spec. Overwrite them during revision.
- A substantive edit resets `status: draft`, clears `approved_at`, and invalidates downstream audit and render clearance.
- Build requires explicit approval of both current specs.
- Audit reviews the exact current specs and the exact draft code.
- Audit completion and audit acceptance are separate states. A generated `PASS` or `PASS_WITH_NOTES` report is not user acceptance.
- After producing or revising an audit report, stop and present the independent findings, reconciliation, overall status, and required return stage. Do not repair code, revise specs, re-audit, or render in the same turn unless the user gives a new decision.
- Render & QA requires `audit_user_decision: accepted` for the exact current audit, plus explicit authorization to render. Phrases such as “continue”, “fix it”, or a bundled planning and rendering request do not satisfy this condition.
- `SPEC_DEFECT` returns to Figure Spec; code or render defects return to Build.

## Stable publication defaults

The default publication profile is:

- figure widths: 88 mm, 120 mm, or 180 mm;
- font family: Arial;
- ordinary figure text: 5–7 pt;
- raster export: 300 DPI.

These defaults remain available and visible in the Code Spec. A project may override them when the user or target medium requires another profile. Do not turn them into assumptions about a particular journal or figure type.

## General boundaries

The core skill does not impose P99 processing, a statistical test, a Tidy schema, a plotting language, a fixed chart type, a mandatory reference image, a Nature caption, a fixed directory, or a universal map rule. Put such decisions and their rationale in the current specs.

Use the templates as consideration frameworks:

- [templates/figure-spec.md](templates/figure-spec.md)
- [templates/figure-code-spec.md](templates/figure-code-spec.md)
- [templates/figure-audit-report.md](templates/figure-audit-report.md)

At each gate, report produced artifacts, unresolved decisions, and the next approval or action required, then stop.
