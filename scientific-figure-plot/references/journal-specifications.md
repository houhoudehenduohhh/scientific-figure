# 期刊与课题组排版尺寸与技术规范 (Journal & Lab Specifications)

> **核心原则**：统一课题组科研绘图标准（以 88 mm / 180 mm 规范为主基准）与 Nature 系列期刊技术规范，作为全流程排版尺寸的**唯一定量参考事实来源 (Single Source of Truth)**。

---

## 一、 画布物理尺寸与版心规范 (Layout & Dimensions)

| 版式类型 | 课题组基准宽度 | 顶刊兼容宽度范围 | 推荐高度上限 | 适用场景 |
| :--- | :---: | :---: | :---: | :--- |
| **单栏图 (Single Column)** | **88 mm** | 88 – 89 mm (~3.46 in) | $\le 170$ mm | 单一指标、单对变量关系、独立折线/柱状/散点图 |
| **1.5 栏图 (Intermediate)** | **120 mm** | 120 – 136 mm (~4.72 in) | $\le 170$ mm | 中型横向比较图、带侧边小图例的复合面板 |
| **双栏通栏 (Double Column)**| **180 mm** | 180 – 183 mm (~7.09 in) | $\le 225$ mm | 多面板组图（Panel a–f）、全景矩阵图、机制流程复合图 |

> **换算公式**：`figsize=(width_mm / 25.4, height_mm / 25.4)`。  
> **留白约束**：图表边缘外边距留白设为 **12 mm** (`pad_inches=12/25.4`)。

---

## 二、 字体规范与字号层级 (Typography Hierarchy)

- **字体族 (Font Family)**：全图严格统一使用无衬线字体 **Arial**（备用：`Helvetica`、`DejaVu Sans`）。
- **可编辑文本保留**：禁止在导出时对文字进行描边栅格化，设置 `pdf.fonttype = 42`（保留 TrueType 文本）。

| 文本层级 | 物理字号 (pt) | 字体粗细 (Weight) | 规则与位置 |
| :--- | :---: | :---: | :--- |
| **子图编号 (Panel Label)** | **8 – 9 pt** | **加粗 (Bold)** | 位于子图左上方（如 `a`, `b`, `c`），严禁在正上方硬塞长英文大标题 |
| **坐标轴标题 (Axis Label)** | **6.5 – 7 pt** | 常规 (Normal) | 首字母大写，包含物理量与单位（例如 `PM2.5 concentration (μg/m³)`） |
| **刻度标签 (Tick Label)** | **6 pt** | 常规 (Normal) | 允许范围 5–6 pt，数字清晰对齐，无科学计数法截断 |
| **图例与图内标注 (Legend/Text)** | **5.5 – 6 pt** | 常规 (Normal) | 允许范围 5–7 pt；**严禁出现 < 5 pt 的文字**（含上下标） |

---

## 三、 线条粗细与刻度几何规范 (Spines & Ticks)

| 图元对象 | 规范参数 | 对应 Matplotlib 参数 |
| :--- | :---: | :--- |
| **边框与坐标轴 (Spines)** | **0.5 pt** | `axes.linewidth = 0.5` |
| **网格线与参考基准线** | **0.5 pt** (虚线/浅灰) | `grid.linewidth = 0.5, linestyle = '--'` |
| **拟合曲线 / 核心趋势线** | **0.8 pt** (次要 0.5 pt) | `lines.linewidth = 0.8` |
| **刻度朝向 (Direction)** | **向内 (in)** | `xtick.direction = 'in', ytick.direction = 'in'` |
| **主刻度长度 (Major Ticks)** | **3.0 mm** (~8.5 pt) | `xtick.major.size = 8.5, ytick.major.size = 8.5` |
| **次刻度长度 (Minor Ticks)** | **1.5 mm** (~4.25 pt)| `xtick.minor.size = 4.25, ytick.minor.size = 4.25` |
| **刻度线宽度 (Tick Width)** | **0.5 pt** | `xtick.major.width = 0.5, ytick.major.width = 0.5` |
| **框式对称 (Mirror Ticks)** | 上与右开启刻度线 | `xtick.top = True, ytick.right = True` |

---

## 四、 官方标准配色库 (Color Palettes)

### 1. 课题组 5 色标准调色板 (Lab Palette)
```python
LAB_PALETTE = {
    "deep_blue":    "#1F67AC",  # 深蓝 (主基准/扩张型/全国均值/对照组)
    "orange_flesh": "#F4A682",  # 橙/肉色 (更新型/提质情景/次级序列)
    "red":          "#B21F2C",  # 红色 (收缩型/关键警示/高暴露)
    "dark_red":     "#660721",  # 深红/暗红 (重度收缩/极端高危特征)
    "light_purple": "#7F73AD",  # 浅紫 (辅助分类/外生变量/气候环境)
}
LAB_COLOR_CYCLE = ["#1F67AC", "#F4A682", "#B21F2C", "#7F73AD", "#660721"]
```

### 2. Okabe-Ito 色盲友好通用调色板 (Nature Standard)
```python
OKABE_ITO = {
    "black":        "#000000",
    "orange":       "#E69F00",
    "sky_blue":     "#56B4E9",
    "bluish_green": "#009E73",
    "yellow":       "#F0E442",
    "blue":         "#0072B2",
    "vermilion":    "#D55E00",
    "reddish_purple":"#CC79A7",
    "grey":         "#999999",
}
```

---

## 五、 Python 绘图环境初始化与导出函数 (开箱即用)

```python
import matplotlib as mpl
import matplotlib.pyplot as plt

def setup_pub_style():
    """初始化顶刊与课题组标准 rcParams 配置"""
    mpl.rcParams.update({
        # 字体规范：Arial，正文 6pt
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "DejaVu Sans", "sans-serif"],
        "font.size": 6.0,
        "font.weight": "normal",
        "axes.titlesize": 7.0,
        "axes.titleweight": "normal",
        "axes.labelsize": 6.5,
        "axes.labelweight": "normal",
        "xtick.labelsize": 6.0,
        "ytick.labelsize": 6.0,
        "legend.fontsize": 6.0,
        "figure.titlesize": 8.0,

        # 线条与边框：0.5 pt
        "axes.linewidth": 0.5,
        "lines.linewidth": 0.5,
        "patch.linewidth": 0.5,
        "grid.linewidth": 0.5,

        # 刻度细节：向内，主刻度 3mm，次刻度 1.5mm，宽度 0.5pt
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.major.size": 8.5,
        "ytick.major.size": 8.5,
        "xtick.minor.size": 4.25,
        "ytick.minor.size": 4.25,
        "xtick.major.width": 0.5,
        "ytick.major.width": 0.5,
        "xtick.minor.width": 0.5,
        "ytick.minor.width": 0.5,
        "xtick.top": True,
        "ytick.right": True,

        # 图例与可编辑矢量文本
        "legend.frameon": False,
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
    })

def add_panel_label(ax, label="a", x=-0.12, y=1.05):
    """添加标准子图标号 (9 pt 加粗)"""
    ax.text(x, y, label, transform=ax.transAxes,
            fontsize=9.0, fontweight="bold", va="bottom", ha="left")

def save_pub_figure(fig, out_prefix, dpi=300, export_vector=False):
    """保存符合尺寸规范的科研图件
    
    默认仅导出 300 DPI PNG 供快速审查；
    仅在 export_vector=True (用户显式要求) 时才增量导出矢量 PDF/SVG。
    """
    pad_in_inches = 12.0 / 25.4  # 12mm 边缘留白
    # 默认导出 PNG
    fig.savefig(f"{out_prefix}.png", dpi=dpi, bbox_inches="tight", pad_inches=pad_in_inches)
    
    # 显式要求时才导出矢量图
    if export_vector:
        fig.savefig(f"{out_prefix}.pdf", bbox_inches="tight", pad_inches=pad_in_inches)
        fig.savefig(f"{out_prefix}.svg", bbox_inches="tight", pad_inches=pad_in_inches)
```
