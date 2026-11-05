# Figure Audit stage

## Preconditions

Auditors receive the current Figure Spec, Figure Code Spec, complete draft code, relevant result or input schemas, runtime constraints, and any reference images used by the design.

## Independent lenses

Use three isolated auditors when the environment supports them. They must submit findings independently before reconciliation. If independent auditors are unavailable, report that limitation instead of claiming the gate passed.

### Auditor 1: scientific evidence and data mapping

Review the claim, panel evidence, source data, analysis unit, field-to-channel mapping, transformations, uncertainty, labels, hard-coded values, selection, and claim boundary. Do not require P values, confidence intervals, a Tidy schema, or model output when the Figure Spec does not call for them.

### Auditor 2: visual encoding and layout

Review chart or image grammar, axes and units, legends and direct labels, color accessibility, panel hierarchy, collision risks, spatial geometry when applicable, and the selected output profile. Use the default 88/120/180 mm, Arial, 5–7 pt, and 300 DPI profile unless the current spec explicitly overrides it.

### Auditor 3: implementation, rendering, and reproducibility

Review the Spec to code mapping, backend consistency, deterministic behavior, input and output contracts, file validity, error handling, resource release, dependency capture, and visual render checks. Do not assume Python, matplotlib, PNG, or a particular assertion unless the Code Spec selects them.

## Findings

Each finding includes:

- `finding_type`;
- `severity`;
- `spec_reference`;
- code or render evidence;
- risk and affected output;
- recommended action;
- `return_stage`.

Use these finding types:

- `SPEC_DEFECT`;
- `CONTRACT_VIOLATION`;
- `IMPLEMENTATION_DEFECT`;
- `VISUAL_RENDER_DEFECT`;
- `REPRODUCIBILITY_RISK`;
- `ADVISORY`.

Use `blocker`, `major`, or `minor` severity. A faithful implementation of a defective Figure Spec is still a `SPEC_DEFECT`.

## Reconciliation

The coordinator deduplicates evidence and resolves conflicts without majority voting.

- `BLOCKED`: unresolved blocker or `SPEC_DEFECT`;
- `CHANGES_REQUIRED`: major code, contract, or render finding;
- `PASS_WITH_NOTES`: only accepted minor or advisory findings;
- `PASS`: no unresolved findings.

Return specification defects to Figure Spec and implementation or rendering defects to Build. Re-audit repaired current artifacts before Render & QA.

## Mandatory user decision stop

Write the audit report with these explicit states:

- `audit_report_status: complete`;
- `audit_overall_status: BLOCKED | CHANGES_REQUIRED | PASS_WITH_NOTES | PASS`;
- `audit_user_decision: pending`;
- `render_authorized_by_user: no`.

The audit gate is still closed when the overall status is `PASS` or `PASS_WITH_NOTES`. Stop after presenting the report. The next turn must contain an explicit user decision for this exact report, for example `accept audit & render`, before rendering can be routed. A repair request or a new spec decision routes back to Figure Spec or Build and invalidates this report.
