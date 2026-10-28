# scientific-figure

> **A Publication-Grade Scientific Data Analysis, Blueprint Planning & Plotting Suite for AI Coding Agents**

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Journal Standard](https://img.shields.io/badge/Standard-Nature%2FLancet%2FCell-red.svg)](https://www.nature.com/)
[![Specification](https://img.shields.io/badge/Specs-OpenSpec--Driven-success.svg)](https://github.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Overview

When using AI coding assistants for scientific data visualization, research teams often face critical issues:
1. **Hallucination & Misalignment**: Models generate complex plotting code without truly deconstructing reference figures, resulting in mismatched evidence hierarchies and incorrect chart archetypes.
2. **Statistical Discrepancy**: Plotting scripts on-the-fly recalculate models, P-values, or confidence intervals, causing discrepancies between the manuscript text and figures.
3. **Output Token Exhaustion**: Cramming scientific rationale, aesthetic mapping, and code specifications into a single turn forces the model to heavily compress code engineering constraints.
4. **Lack of Preflight Quality Assurance**: No automated mechanism checks for out-of-memory risks on large datasets, silent NaN drops, or text falling below the journal font size limit (<5 pt).

`scientific-figure` fundamentally redesigns scientific visualization with a **two-step, dual-contract, human-in-the-loop pipeline**:

- **Step 1 (`scientific-figure-blueprint`)**: Deconstructs reference claims, establishes statistical inference plans, defines aesthetics, and derives OpenSpec-grade code specifications (`blueprint.md` + `code_spec.md`) before any code is written.
- **Step 2 (`scientific-figure`)**: Consumes the approved blueprint and tidy stats tables to execute production-grade Python (matplotlib/seaborn) plotting, strictly enforcing Nature specifications (88/180 mm, Arial 5–7 pt, 0.5 pt inward ticks, default 300 DPI PNG), verifying font sizes with physical stream probes (`audit_pdf_text.py`), and generating publication-ready captions.

---

## Repository Architecture

```text
scientific-figure/
├── README.md                          # Chinese Documentation
├── README_EN.md                       # English Documentation
├── LICENSE                            # MIT License
├── .gitignore                         # Git exclusion rules
├── scientific-figure-blueprint/           # [Step 1] Planning & Code Spec Engine
│   ├── SKILL.md                       # Execution protocol
│   ├── static/                        # Static contract templates
│   │   ├── blueprint_template.md      # Scientific blueprint template
│   │   └── code_spec_template.md      # OpenSpec code engineering template
│   ├── references/                    # Statistical & journal specifications
│   │   ├── nature-statistics-contract.md # Rigorous stats & data contract
│   │   └── journal-specifications.md  # 88/180 mm physical dimensions & specs
│   └── scripts/
│       └── stat_check.py              # Automated normality & homoscedasticity checks
└── scientific-figure/                     # [Step 2] Production Plotting & QA Engine
    ├── SKILL.md                       # Execution protocol & QA preflight
    ├── manifest.yaml                  # Dynamic condition router
    ├── README.md                      # Sub-skill guide
    ├── static/                        # Lab theme defaults & publication rcParams
    ├── references/                    # Chart recipe catalog & design patterns
    │   ├── journal-specifications.md  # Unified physical dimensions & default PNG export
    │   ├── figure-legend-conventions.md # Caption writing conventions
    │   ├── chart-types.md             # Advanced chart recipes
    │   ├── common-patterns.md         # Multi-panel composite layouts
    │   ├── template-catalog.md        # 5 validated biomedical templates
    │   └── design-theory.md           # Color theory & typography
    ├── scripts/                       # Automated preflight & auditing tools
    │   ├── audit_pdf_text.py          # PDF font size stream auditor (>= 5pt)
    │   ├── validate_figure.py         # Static code linter
    │   ├── figure_safety.py           # Safe numerical monotonic interpolation
    │   └── plot_templates.py          # Automated template generator
    └── assets/                        # Curated figures4papers reference gallery
```

---

## Core Invariants & Quality Gates

1. **No Naked P-Values**: P-values must be paired with effect sizes (Cohen's $d$, HR, OR, $r$) and 95% confidence intervals.
2. **Unidirectional Data Contract**: Statistical models and clean tables are generated first; plotting scripts strictly consume tidy intermediate tables without recalculating statistics.
3. **True Spatial Proportions**: Geographic vector maps strictly enforce `ax.set_aspect('equal')`.
4. **Defensive Engineering**: Big data requires projection pushdown (`columns=[...]`) to prevent OOM; silent drops of NaN samples are strictly prohibited.

---

## License

This project is licensed under the [MIT License](LICENSE).
