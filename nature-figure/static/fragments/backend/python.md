# 绘图后端：Python (matplotlib / seaborn)

**Python 专属执行铁律**：当选定 Python 后端后，所有的图件绘制、预览图生成、高分辨率导出与视觉质检必须 100% 在 Python 中完成。严禁调用 R/ggplot2、patchwork 或任何 R 图形设备来生成临时预览或替代码。若缺少依赖包，直接在 Python 虚拟环境中安装，严禁跨语言混合绘制。

## Python 快速启动配置 (Quick-Start)

```python
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "svg.fonttype": "none",     # editable text in SVG
    "pdf.fonttype": 42,         # editable TrueType text in PDF
    "font.size": 7,             # use 15-24 only for large slide-sized panels
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
})

def save_pub_py(fig, filename, dpi=300, export_vector=False):
    """默认导出高分辨率 PNG；仅在用户显式要求时导出矢量图 (PDF/SVG)"""
    fig.savefig(f"{filename}.png", dpi=dpi, bbox_inches="tight")
    if export_vector:
        fig.savefig(f"{filename}.svg", bbox_inches="tight")
        fig.savefig(f"{filename}.pdf", bbox_inches="tight")
```

Use `text.usetex = True` only when LaTeX is installed and math-rich labels are required.

## 课题组科研绘图统一规范 (Lab Style Guide - 默认优先执行)

当在当前课题组项目环境下绘图时，优先采用以下统一规范（来自《科研绘图规范与配色参考手册》）：

```python
import matplotlib as mpl
import matplotlib.pyplot as plt

# 课题组 5 色标准调色板
LAB_PALETTE = {
    "deep_blue":    "#1F67AC",  # 深蓝 (主基准/扩张型/全国均值)
    "orange_flesh": "#F4A682",  # 橙/肉色 (更新型/提质情景)
    "red":          "#B21F2C",  # 红色 (收缩型/关键警示)
    "dark_red":     "#660721",  # 深红/暗红 (重度收缩/极端特征)
    "light_purple": "#7F73AD",  # 浅紫 (辅助分类/外生变量)
}
LAB_COLOR_CYCLE = ["#1F67AC", "#F4A682", "#B21F2C", "#7F73AD", "#660721"]

def setup_lab_style():
    """配置课题组标准科研绘图样式"""
    # 刻度长度换算: 3mm ≈ 8.5pt, 1.5mm ≈ 4.25pt
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "DejaVu Sans", "sans-serif"],
        "font.size": 6.0,                # 正文 5-7 pt，一律不加粗
        "font.weight": "normal",
        "axes.titlesize": 7.0,
        "axes.labelsize": 6.5,
        "xtick.labelsize": 6.0,
        "ytick.labelsize": 6.0,
        "legend.fontsize": 6.0,
        
        # 边框与线条：统一 0.5 pt
        "axes.linewidth": 0.5,
        "lines.linewidth": 0.5,
        "patch.linewidth": 0.5,
        "grid.linewidth": 0.5,
        
        # 刻度线细节：向内 (in)，主刻度 3mm，次刻度 1.5mm，粗细 0.5 pt
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.major.size": 8.5,        # 3 mm
        "ytick.major.size": 8.5,
        "xtick.minor.size": 4.25,       # 1.5 mm
        "ytick.minor.size": 4.25,
        "xtick.major.width": 0.5,
        "ytick.major.width": 0.5,
        "xtick.minor.width": 0.5,
        "ytick.minor.width": 0.5,
        "xtick.top": True,
        "ytick.right": True,
        
        "legend.frameon": False,
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
    })

# 尺寸要求：双栏宽度严格 18 cm，单栏 8.8 cm
# fig, ax = plt.subplots(figsize=(18/2.54, 12/2.54))  # 双栏示例
# 标号要求：图号 (a, b) 约 9 pt，且必须加粗
# ax.text(-0.12, 1.05, 'a', transform=ax.transAxes, fontsize=9, fontweight='bold')
# 导出边缘要求：坐标轴与边框边缘距离 12 mm
# fig.savefig('output.pdf', bbox_inches='tight', pad_inches=12/25.4)
```

## Going deeper

- `references/journal-specifications.md` — 期刊与课题组排版尺寸与技术规范 (88/180mm、Arial 5-7pt、默认 PNG 导出)
- `references/api.md` — Python PALETTE, helper function signatures, validation rules.
- `references/template-catalog.md` — validated CSV-driven volcano, ROC, dot-plot, marginal, and paired templates backed by `scripts/plot_templates.py`.
- `references/common-patterns.md` — hero panels, legend-only axes, dark image plates, asymmetric layouts.
- `references/chart-types.md` — radar, 3D sphere, fill_between, scatter patterns.
- `references/tutorials.md` — end-to-end walkthroughs for bars, trends, heatmaps.
- `references/demos.md` — third-party figures4papers demo map, copyright boundary, and original Python reimplementation guidance.
- `scripts/validate_figure.py` — dependency-free source preflight before rendering and visual QA.
- `scripts/audit_pdf_text.py` — dependency-free `Tf` scan of exported PDF text runs; use it to enforce the 5 pt glyph floor after rendering.
- `scripts/figure_safety.py` — strict monotone interpolation and annotation placement above uncertainty extents.
