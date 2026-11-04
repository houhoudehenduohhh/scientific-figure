# Scientific Figure

This skill provides a portable four-stage workflow for scientific figures:

`Figure Spec → Build → Independent Audit → Render & QA`

It preserves traceability between claims, data mappings, visual encodings, implementation, and delivered files without assuming one project, journal, language, backend, or chart type.

The default publication profile is retained: 88/120/180 mm figure widths, Arial, ordinary text at 5–7 pt, and 300 DPI raster export. These values can be overridden only when the current spec records the user or medium-specific reason.

The core workflow does not impose universal P99 processing, statistical tests, a Tidy schema, Python or matplotlib, a mandatory reference image, Nature-specific captions, or fixed paths. Optional assets and references are preserved under `assets/` and `references/optional/`.

See [SKILL.md](SKILL.md) and the four stage references for routing and gates.
