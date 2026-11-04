# Figure Build stage

## Preconditions

- Current Figure Spec and Figure Code Spec exist.
- Both are explicitly approved.
- No substantive edit occurred after approval.

## Outcome

Generate a draft implementation and tests that can be independently audited without rendering the production deliverable.

## Procedure

1. Map each Code Spec task to code, configuration, or a test.
2. Read declared result artifacts or input data using the selected backend and schema.
3. Implement the visual mappings, geometry, labels, and export path from the current spec.
4. Add tests for data mapping, domain limits, transformations, deterministic behavior, and failure handling.
5. Run syntax, import, static, and synthetic or minimal fixture tests.
6. Produce a spec-to-code verification map and stop for Audit.

Do not render the production figure, fit an undeclared model, recompute an undeclared inferential result, or silently change the analysis population.
