# scientific-figure

> **顶刊级科研数据分析、蓝图规划与出版级绘图一体化智能套件**  
> *A Publication-Grade Scientific Data Analysis, Blueprint Planning & Plotting Suite for AI Coding Agents*

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Journal Standard](https://img.shields.io/badge/Standard-Nature%2FLancet%2FCell-red.svg)](https://www.nature.com/)
[![Specification](https://img.shields.io/badge/Specs-OpenSpec--Driven-success.svg)](https://github.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 一、 项目背景与核心理念

在利用大语言模型（AI Coding Agents）进行科研数据分析与绘图时，传统工作流常面临四大痛点：
1. **暗箱与幻觉**：AI 未彻底理解范文逻辑便直接生成几百行绘图代码，出现坐标轴错位、图表类型误判；
2. **统计口径割裂**：绘图脚本在画图时临时重算模型、P值或置信区间，导致正文数据与图表数据口径脱节；
3. **输出 Token 挤压**：将科学结论、排版大纲与代码规范挤压在单次回答中，导致大模型在代码边界处严重缩水；
4. **形式化规范缺失**：缺少对大数据量内存防护（防 OOM）、空值静默丢弃、底线字号（<5 pt）的物理审查机制。

**`scientific-figure` 彻底重构了科研可视化范式**。将全流程拆解为**「两步走、双文解耦、双重审查门禁」**的闭环 Stack：

```
                    【顶刊科研出图一体化 Stack (scientific-figure)】
                                          │
       ┌──────────────────────────────────┴──────────────────────────────────┐
       ▼                                                                     ▼
【第 1 步: nature-figure-blueprint】                      【第 2 步: nature-figure】
 (规划蓝图与代码工程规格引擎)                               (依规出图与物理字号质检引擎)
       │                                                                     ▲
       ├───────► 文档 1: 【figX_blueprint.md】                               │
       │         (科学论断 + 视觉通道 + 统计推断方案 + 88/180mm)               │
       │                                                                     │
       ├───────► 文档 2: 【figX_code_spec.md】                               │
       │         (OpenSpec 4 级契约: Proposal / Specs / Design / Tasks)      │
       │                                                                     │
       ▼                                                                     │
【★ 强制双契约人机审查门禁 (Dual-Contract Gate)】 ─────────────────────────────┘
 (用户同时审查：科学结论一致性 + 代码反向红线与断言)
```

---

## 二、 双 Skill 核心职能分工

### 1. `nature-figure-blueprint` (Step 1: 规划蓝图与代码规格引擎)
- **触发时机**：用户提供「范文参考图 + 原始数据」时率先触发；
- **核心成果物**：物理生成两份独立的 Markdown 文档，彻底释放模型 Token 算力：
  - **`figX_blueprint.md`**：面向科研人员。深入解构范文证据链（Panel a, b, c...），制定严格的统计推断方案（检验方法、效应量、95% CI、异常值截断口径），规划图件在 Nature 尺寸（单栏 88mm、双栏 180mm）下的视觉拓扑；
  - **`figX_code_spec.md`**：面向代码工程师与审查者。基于 OpenSpec 理念，确立**数理不变性公式**、**反向红线（禁止项）**、**大数据列投影防 OOM 设计**，以及**带可执行断言（`assert`）的原子 Tasks 清单**。
- **人机门禁 (Blocking Gate)**：暂停流程，向用户汇报关键规划摘要，必须经人工审查签署后，方可进入编码阶段。

### 2. `nature-figure` (Step 2: 出版级出图与物理质检引擎)
- **触发时机**：用户在第一步中确认通过双门禁后触发；
- **核心执行闭环**：
  - **只读中间契约表**：严格消费统计步骤输出的标准化 Tidy Stats 数据表，**严禁在绘图脚本中临时重算统计模型或 P 值**；
  - **严格对标 Code Spec**：对照 `code_spec.md` 中的 Tasks 清单逐项编写生产级 Python 代码；
  - **环境隔离运行**：显式调用项目虚拟环境解释器（`.\.venv\Scripts\python.exe`）；
  - **默认 300 DPI PNG 导出**：边缘保留 12mm 留白，供快速审阅；仅在用户显式要求时追加矢量 PDF/SVG；
  - **物理字号底层审计**：内置 `audit_pdf_text.py` 探针，逐流解析 PDF `Tf` 操作符，确保任何角标、文字均 $\ge 5$ pt，杜绝版面跌破底线；
  - **标准图例文本生成**：自动生成符合 Nature 标准的 Caption（`Fig. X | Title.`、样本量 $n$、效应量与精确 P 值）。

---

## 三、 仓库目录架构

```text
scientific-figure/
├── README.md                          # 中文主文档
├── README_EN.md                       # English Documentation
├── LICENSE                            # MIT License
├── .gitignore                         # 规范 Git 忽略规则
├── nature-figure-blueprint/           # [Skill 1] 规划蓝图与代码规格引擎
│   ├── SKILL.md                       # 调度协议与执行路由
│   ├── static/                        # 静态模板契约
│   │   ├── blueprint_template.md      # 科学视觉蓝本模板 (5 部分)
│   │   └── code_spec_template.md      # OpenSpec 代码工程规格模板 (5 部分)
│   ├── references/                    # 统计与排版规约
│   │   ├── nature-statistics-contract.md # 顶刊统计规范与 Tidy 数据契约
│   │   └── journal-specifications.md  # 期刊排版几何与物理尺寸规范 (88/180mm)
│   └── scripts/
│       └── stat_check.py              # 正态性与方差齐性快速审计工具
└── nature-figure/                     # [Skill 2] 出版级出图与物理质检引擎
    ├── SKILL.md                       # 出图调度协议与门禁校验
    ├── manifest.yaml                  # 动态条件路由总清单
    ├── README.md                      # 子技能中英文文档
    ├── static/                        # 核心立场与 Python rcParams 主题配置
    ├── references/                    # 顶刊专业配方与算法库
    │   ├── journal-specifications.md  # 统一物理尺寸与默认 PNG 导出定义
    │   ├── figure-legend-conventions.md # Nature 图例文本写作规范
    │   ├── chart-types.md             # 复杂图表（雷达/3D/流形/填充等）配方
    │   ├── common-patterns.md         # 复合多面板编排（Hero Panel/独立图例轴）
    │   ├── template-catalog.md        # 5 大经典生物医学图表目录
    │   └── design-theory.md           # 科学可视化色彩与字体理论
    ├── scripts/                       # 生产级工具链与物理探针
    │   ├── audit_pdf_text.py          # PDF 矢量文字物理字号审计器 (硬检 >= 5pt)
    │   ├── validate_figure.py         # 绘图脚本静态代码合规预检器
    │   ├── figure_safety.py           # 单调网格安全插值计算器
    │   └── plot_templates.py          # 标准图表快速生成器
    └── assets/                        # 顶刊复现案例库与视觉图谱 (figures4papers)
```

---

## 四、 核心设计红线与质量保证

1. **绝对拒绝“裸 P 值”**：严禁孤立报告 $P$ 值或星号；必须同时报告效应量（Cohen's $d$, HR, OR, $r$）及 95% 置信区间；
2. **数据契约单向流动**：数据清洗与推断统计先行，固化输出标准中间表；绘图代码严禁擅自重新拟合模型；
3. **空间真实几何投影**：空间地理矢量图强制声明 `ax.set_aspect('equal')`，防止地图纬度向拉伸变形；
4. **反向红线零妥协**：严禁原位篡改原始数据、严禁静默过滤空值样本（必须打印过滤统计日志）、控制台日志 100% 全英文。

---

## 五、 快速上手

### 1. 安装与环境依赖
推荐在独立的 Python 虚拟环境（`.venv`）中安装基础科学计算与绘图依赖：
```bash
python -m venv .venv
.\.venv\Scripts\pip install numpy pandas scipy matplotlib seaborn pyarrow geopandas
```

### 2. 作为 Agent Skill 使用
将本仓库克隆至你的 Agent 工作区技能目录（如 `.agents/skills/` 或配置到 Antigravity / Claude Code / Cline 等智能体框架）：
```bash
git clone https://github.com/houhoudehenduohhh/scientific-figure.git .agents/skills/scientific-figure
```
在与 AI 结对编程时，直接提示：
> “请参考【范文图片路径】以及【数据文件路径】，调用 `nature-figure-blueprint` 生成规划蓝图与代码工程规范。”

---

## 六、 开源协议

本项目采用 [MIT License](LICENSE) 授权开源。欢迎引用、贡献图表配方与提出改进建议！
