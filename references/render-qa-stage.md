# Render & QA stage

## Preconditions

Confirm that the current Figure Spec and Figure Code Spec are approved, the exact current audit report has `audit_report_status: complete` and `audit_user_decision: accepted`, `accepted_audit_id` equals the current `audit_id`, the code matches the audited draft, the runtime and output paths are resolved, and the user explicitly authorized rendering after seeing that audit report.

The rendering gate is a blocking assertion, not an inference:

`assert audit_report_status == "complete"`

`assert audit_user_decision == "accepted"`

`assert accepted_audit_id == audit_id`

`assert render_authorized_by_user == "yes"`

The acceptance must arrive in a later user turn than the turn that produced the audit report. Do not run a repair, re-audit, production render, or presentation command in the same turn that creates the audit report or repairs an audit finding. After repair, create a new audit report and stop again for a new user decision.

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
