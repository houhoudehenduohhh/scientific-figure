---
name: nature-figure
description: >-
  顶刊科研绘图与成果导出引擎（两步走之第 2 步）。在已获得用户审查确认的 Figure Blueprint 蓝图指导下触发。负责依据 approved blueprint.md 与 Tidy Stats 中间表，编写并执行生产级 Python (matplotlib/seaborn) 绘图脚本，严格落实 88/180mm、Arial 5–7pt、0.5pt 轴线向内刻度与默认 300 DPI PNG 导出，并执行底线字号物理审计与 Nature 级图例文本生成。
---

# Nature 顶刊科研出图与质检引擎 (Step 2 Production Plotter)

本技能为 **「Nature 顶刊科研出图流水线」的第二步 (Step 2: Production Plotting & QA)」**。  
**前置硬约束**：本技能必须以 **第 1 步 (`nature-figure-blueprint`) 生成并经用户双门禁确认的 Blueprint MD 与 Code Spec MD** 为唯一输入！严禁脱离规划蓝图与代码规范随意编写绘图代码。

```
[输入 1: 经确认的 markdown/<step>/<fig_name>_blueprint.md (科学与视觉蓝本)]
[输入 2: 经确认的 markdown/<step>/<fig_name>_code_spec.md (OpenSpec代码工程规范与Tasks)]
[输入 3: 中间数据契约表 Dataset/<step>/stats_results_<name>.parquet]
               ↓
    【nature-figure】(Step 2 执行出图)
       ├── 1. 读取 blueprint.md 中的「视觉映射」与「物理尺寸」
       ├── 2. 对照 code_spec.md 的 Tasks 清单逐项编写并断言自测
       ├── 3. 严格遵循反向红线 (严禁临时重算统计，全英文日志)
       ├── 4. 显式调用 .venv 执行出图，默认导出 300+ DPI PNG
       ├── 5. 运行 audit_pdf_text.py 执行底层矢量字号物理探查 (>= 5pt)
       └── 6. 按照顶刊句式自动生成配套图例 (Caption) 与 Source Data 说明
               ↓
[输出成果: models/<step>/<fig_name>.png (+ 可选 PDF/SVG) + Caption]
```

---

## 出图执行标准协议 (Plotting Protocol)

### 1. 前置双门禁校验 (Pre-requisite Gate)
- 检查是否存在当前图件的规划文件 `markdown/<step>/<fig_name>_blueprint.md` 与代码规范文件 `markdown/<step>/<fig_name>_code_spec.md`；
- **若不存在或未确认**：立即提示用户先调用 `nature-figure-blueprint` 完成双文生成与人机对齐门禁；
- **若已确认**：读取 `blueprint.md` 中的科学论断与视觉映射，读取 `code_spec.md` 中的数理公式、反向红线与 Tasks 任务清单。

### 2. 确认绘图后端与环境配置
- 强制使用项目虚拟环境解释器：优先检测 `.\.venv\Scripts\python.exe`；
- 采用 `matplotlib` / `seaborn`；加载 `static/fragments/backend/python.md` 与 [journal-specifications.md](references/journal-specifications.md)；
- 注入标准主题配置：`Arial` 字体、Panel 标号 9pt 加粗、正文/刻度 5–7pt、轴线 0.5pt、向内刻度（主刻度 3mm / 次刻度 1.5mm）。

### 3. 依据 Code Spec 实施分步代码编写 (Task-Driven Implementation)
依据 `code_spec.md` 中的 Task 清单编写脚本，保存至 `scripts/<对应业务步骤>/plot_<fig_name>.py`：
1. **逐项落实 Task 与验证断言**：按照 Task 1 至 Task 4 的顺序编写代码，确保每个 Task 配备的 `assert` 逻辑完整有效；
2. **死守反向红线 (Negative Constraints)**：
   - 直接从 `Dataset/` 中读取标准中间表，**严禁在绘图脚本中临时调用 `scipy` 重算 P 值或重构回归模型**；
   - 严禁静默过滤数据，因空值或异常被过滤的样本必须打印丢弃统计日志；
   - 地理空间矢量图强制声明 `ax.set_aspect('equal')`；
   - 代码标识符与控制台日志 100% 使用英文；
3. **图元防碰撞**：散点、线形、误差棒与文字标签预留安全留白。

### 4. 渲染与成果导出 (Rendering & Export)
显式在项目终端中执行脚本：
```powershell
& ".\.venv\Scripts\python.exe" scripts/<step>/plot_<fig_name>.py
```
- **默认导出**：300+ DPI PNG（归档至 `models/<对应业务步骤>/`，边缘留白 12mm），供快速预览与审阅；
- **增量矢量导出**：仅当用户显式要求导出矢量图时，才增量保存 `.pdf` 与 `.svg`。

### 5. 交付前质检审计与图例生成 (QA Preflight & Caption)
1. **物理字号探查**：若导出了 PDF，调用 `scripts/audit_pdf_text.py` 扫描底层 `Tf` 操作符，确保无任何文字或角标跌破 5 pt；
2. **对齐自查表**：对照 `static/core/contract.md` 终审质检清单排查截断、刻度翻转等隐患；
3. **图例自动生成**：按照 `references/figure-legend-conventions.md` 规范，输出标准 Nature 图例文本：
   - `Fig. X | Title.` 句式；
   - 明确声明独立样本量 $n$；
   - 明确定义误差棒（Mean $\pm$ SD、Mean $\pm$ SEM 或 Median + IQR）；
   - 标注两阶段假设检验方法与精确 P 值；
   - 附带 `Source data are provided as a Source Data file.`。

### 6. 成果交付报告与语言规范 (Delivery Report & Language Protocol)
1. **面向用户的交付说明与质检报告 100% 使用中文**：
   - 所有生成的用户交付说明、质检审计报告、复盘文档（如 `markdown/<step>/<fig_name>_report.md`、Artifact 汇报总结、数据诊断报告等），**必须强制统一使用中文撰写**，以便课题组快速审阅、技术交底与成果汇报；
   - 报告需清晰梳理修改前后对比、空间与数理机制解释、数据诊断结论与生产脚本指引；
2. **全英文红线的严格适用边界**：
   - 全局规则中的“全英文”红线，严格限定于：底层代码标识符（变量名/函数名/类名）、脚本文件与数据表命名、控制台运行日志（`print` / `logging`）以及随图导出的学术投稿英文图例（Caption）；
   - **严禁**将全英文规则泛化到面向用户的技术说明、中文 Markdown 汇报报告及人机交互交底文档中！
