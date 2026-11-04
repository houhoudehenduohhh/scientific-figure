# Scientific Figure Skill v2 Implementation Plan

> **For agentic workers:** Use this plan to implement the approved generalized figure workflow.

**Goal:** Replace the project-specific multi-entry figure suite with one portable Figure Spec driven workflow while retaining the requested publication defaults: 88/120/180 mm, Arial, 5–7 pt, and 300 DPI.

**Architecture:** A root `SKILL.md` routes four stages: Figure Spec, Build, Independent Audit, and Render & QA. Current Figure Spec and Figure Code Spec files are overwriteable and carry project-specific methods, backend, paths, and outputs. Existing chart assets and advanced references remain optional resources.

**Spec:** User-approved design direction in the conversation and prior scientific-figure audit.

## Global Constraints

- Keep 88/120/180 mm, Arial, 5–7 pt, and 300 DPI as the default publication profile.
- Do not make P99, a statistical test, a data schema, a plotting backend, a journal caption, or a fixed directory universal.
- Reference images are optional.
- Build creates a draft and tests but does not render production figures.
- Audit distinguishes `SPEC_DEFECT` from implementation and rendering defects.
- Render & QA requires approved current specs, accepted audit, matching code, and explicit execution authorization.

## Tasks

### Task 1: Create the root four-stage contract

Create `SKILL.md`, `agents/openai.yaml`, four stage references, and three templates: `figure-spec.md`, `figure-code-spec.md`, `figure-audit-report.md`.

The root must route by state, preserve overwrite semantics, discover paths and runtimes, and retain the four publication defaults as an explicit optional-to-override profile.

### Task 2: Reframe the audit protocol

Create a generic audit reference covering three independent lenses:

1. scientific evidence and data mapping;
2. visual encoding and layout;
3. implementation, rendering, and reproducibility.

Use the finding types `SPEC_DEFECT`, `CONTRACT_VIOLATION`, `IMPLEMENTATION_DEFECT`, `VISUAL_RENDER_DEFECT`, `REPRODUCIBILITY_RISK`, and `ADVISORY`.

### Task 3: Migrate documentation, resources, and entrypoints

Rewrite bilingual READMEs around the four stages. Move the old untracked `figure-code-audit` into `legacy/figure-code-audit`. Remove the old Blueprint and Plot active entrypoints. Preserve the existing plot assets and optional references under the root `assets/` and `references/optional/` areas.

### Task 4: Add behavioral checks and verify

Add tests or forward-test records for:

- a no-reference-image exploratory figure;
- an approved map or publication figure using the default profile;
- an ML performance figure with no P value or regression requirement;
- a faithful implementation of a bad visual spec returning `SPEC_DEFECT`.

Run the Skill validator, existing figure safety tests, Python compile checks, and diff checks.
