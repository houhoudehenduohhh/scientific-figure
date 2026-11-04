# Render & QA stage

## Preconditions

Confirm that the current Figure Spec and Figure Code Spec are approved, the audit is accepted, the code matches the audited draft, the runtime and output paths are resolved, and the user authorized rendering.

## Render

Run the declared backend and entry command. Record input identity, runtime and dependencies, configuration, random seeds when relevant, output paths, exit status, warnings, and generated artifacts.

## Quality assurance

Verify:

- output files open and are non-empty;
- dimensions, font family, ordinary text size, and raster resolution follow the selected profile;
- axes, units, legends, labels, uncertainty, and panel order match the Figure Spec;
- no unintended data filtering, refitting, or population change occurred;
- visual inspection catches clipping, overlap, missing fonts, blank panels, unreadable labels, and distorted geometry;
- captions or source-data notes match the selected audience and output format.

The default publication profile is 88/120/180 mm, Arial, 5–7 pt, and 300 DPI. Use these values unless the current Code Spec records an explicit override.

## Completion

Deliver figure files, source or plotting data when required, caption or explanatory text, QA evidence, deviations, and unresolved limitations. Do not infer scientific findings beyond the approved Figure Spec.
