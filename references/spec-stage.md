# Figure Spec stage

## Outcome

Create or revise the current Figure Spec and Figure Code Spec, then stop for explicit user approval.

## Procedure

1. Inspect the research or communication objective, available data or approved result artifacts, existing project conventions, optional reference images, and current specs.
2. Separate confirmed facts, user decisions, proposals, assumptions, and open questions.
3. Decide whether the figure is inferential, descriptive, predictive, mechanistic, spatial, image based, or mixed. Do not assume a statistical result is needed for every figure.
4. Map each panel and visual channel to a scientific or communication purpose.
5. Record data source, analysis unit, transformations, uncertainty expression, accessibility needs, audience, output format, and the default or overridden publication profile.
6. Translate the design into a Figure Code Spec with input contracts, backend, transformations, visual mappings, geometry, artifacts, reproducibility, and QA tasks.
7. Overwrite the current specs with `status: draft`, summarize decisions and open questions, and stop.

## Data and reference inspection

Read-only inspection is allowed for data schemas, result tables, existing figures, and reference images. It produces evidence for the Spec. It does not automatically choose a model, outlier rule, test, or visual encoding.

## Gate

Do not write production plotting code, render a final figure, or alter the analysis population in this stage.
