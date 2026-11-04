# Generalization forward tests

These scenarios are acceptance checks for future changes:

1. A descriptive exploratory figure with no reference image routes to Figure Spec without forcing P99, a significance test, a Tidy schema, or a specific backend.
2. An approved publication figure can use the retained defaults: 88/120/180 mm, Arial, 5–7 pt, and 300 DPI.
3. A machine-learning performance figure can specify metrics and uncertainty without being required to contain P values or regression diagnostics.
4. A faithful implementation of an unsafe or unsupported visual design is reported as `SPEC_DEFECT`, not silently accepted as a code pass.
5. A project may override a default width, font, size, or DPI when the current Code Spec records the target medium and reason.
6. A missing reference image is an open design input, not a blocking requirement unless the current Spec explicitly depends on it.
