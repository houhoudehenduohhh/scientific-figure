---
name: nature-figure-blueprint
description: >-
  顶刊科研绘图与数据分析规划蓝图引擎（两步走之第 1 步）。在编写任何绘图代码前触发。负责接收用户原始数据与范文参考图，解构范文科学论断与视觉语法，制定数据分析与统计假设检验方案（含 Tidy 数据契约），规划绘图大纲与物理尺寸，并通过 OpenSpec 理念完成代码工程规格说明（数理公式、反向红线、原子任务与可验证断言），自动生成双 Markdown 文档（blueprint.md + code_spec.md）供人机对齐与审查门禁签署。
---

# Nature 科研图件与代码规格蓝图引擎 (Step 1 Blueprint Engine)

本技能为 **「Nature 顶刊科研出图流水线」的第一步 (Step 1: Planning & Dual-Contract Gate)**。  
核心宗旨：**科学与工程物理分离、规范先行、契约锁定、双重门禁对齐后再写代码**。杜绝直接编写绘图代码导致的统计口径脱节、版式反复返工和 AI 幻觉代码。

```
[输入: 用户原始数据 + 范文参考图]
               ↓
    【nature-figure-blueprint】(Step 1 规划与规格引擎)
       ├── 1. 范文深度解构 (科学论断 + 视觉通道 + 排版拓扑)
       ├── 2. 数据分析方案 (假设检验 + 效应量 + Tidy 契约表 Schema)
       ├── 3. 目标绘图大纲 (本地字段映射 + 88/180mm 尺寸 + 色彩体系)
       └── 4. OpenSpec 代码工程规格推演 (数理不变性 + 反向红线 + 原子 Tasks)
               ↓
       ┌───────┴───────┐ (物理拆分生成，保证各自拥有 100% 充沛 Token)
       ▼               ▼
【文稿 1: blueprint.md】       【文稿 2: code_spec.md】
 (面向科研科学与视觉审查)        (面向代码工程与反向红线审查)
 ├── 范文深度解构               ├── Proposal (工程目标与边界)
 ├── 本地数据映射与预期结论     ├── Invariants (前置条件/数理公式/反向红线/后置断言)
 ├── 统计推断与中间表 Schema    ├── Design (列投影防OOM/异常熔断)
 └── 期刊物理尺寸与图例格式     └── Tasks (带验收断言的原子开发清单)
       │                               │
       └───────────────┬───────────────┘
                       ▼
【★ 强制双契约人机审查门禁 (Dual-Contract Review Gate)】
          (科学结论 + 代码约束双确认通过)
                       │
                       ▼
【nature-figure】(Step 2: 严格依照 code_spec.md 的 Tasks 逐项落代码出图)
```

---

## 蓝图与代码规范生成标准执行协议 (Execution Protocol)

当用户发起科研绘图规划或提供样本参考图时，必须依次执行以下环节：

### 1. 范文/参考图视觉与逻辑解构 (Reference Deconstruction)
利用原生多模态视觉能力深度解析参考图：
1. **科学论断**：提炼参考图向审稿人证明的核心论点，厘清 Panel a, b, c... 的递进证据链；
2. **图表语法**：识别图表原型（散点/样条/小提琴/森林图/热图）、坐标系刻度（线性/对数）、分组色块及离散度表达形式（误差棒/阴影置信带）；
3. **空间拓扑**：分析多面板网格排布比例（例如 $2 \times 2$ 均分、或非对称 Hero Layout）。

### 2. 数据分析方案与统计契约制定 (Statistical Plan)
参考 `references/nature-statistics-contract.md` 制定严格推断统计方案：
1. **假设前提探查**：若数据已就绪，可调用 `scripts/stat_check.py` 探查正态性 (Shapiro-Wilk) 与方差齐性 (Levene)；
2. **统计检验选型**：锁定检验方法（如 Welch's t-test、Kruskal-Wallis、Cox 比例风险回归）；
3. **锁定 Tidy 中间数据契约**：明确要求后续分析脚本必须导出标准中间表（包含 `estimate, se, ci_lower, ci_upper, p_val, n, test_name`），严禁绘图脚本临时重算统计模型。

### 3. 目标图件排版设计与本地数据映射 (Target Plotting Design)
参考 `references/journal-specifications.md` 确定物理规格：
1. **本地科学论点**：根据范文逻辑，预判本地数据应得出的科学结论；
2. **字段-视觉通道映射**：明确定义本地数据表具体哪个列绑定至 X 轴、Y 轴、颜色分组与子面板；
3. **期刊物理尺寸**：锁定单栏 88 mm、1.5 栏 120 mm 或双栏 180 mm；确定 Arial 5–7 pt、0.5 pt 线宽与默认导出 300 DPI PNG。

### 4. 数据物理探查与 OpenSpec 代码工程规格推演 (Code Specs Derivation)
在编写 `code_spec.md` 前，必须执行真实的元数据与工程边界探查：
1. **元数据物理探查**：检查输入表实际 Schema、确切列名、行数规模及缺失率；
2. **确立数理不变性 (Invariants)**：写出加权或聚合数学公式；锁定异常值截断算法（如 P99 上界截断时机与范围）；
3. **确立反向红线 (Negative Constraints)**：
   - 严禁原位篡改输入数据；
   - 严禁静默过滤 NaN（必须输出丢弃计数日志）；
   - 绘图脚本严禁调用 `scipy` 重算 P 值；
   - 空间矢量轴强制锁定 `ax.set_aspect('equal')`；
   - 代码标识符与控制台日志必须 100% 英文。
4. **技术架构防御**：大数据量下强制采用列投影下推（`columns=[...]`），限制内存峰值；
5. **编译原子任务清单 (Tasks)**：拆解为 3~4 个原子任务，每个任务配备明确的程序化断言条件（`assert ...`）。

### 5. 双文件物理拆分输出与双门禁审查 (Dual-Contract Review Gate)
为彻底杜绝 Output Token 挤压，必须物理分离输出两个 Markdown 文件：

1. **生成科学蓝本**：依据 `static/blueprint_template.md` 渲染生成：
   `markdown/<step_dir>/<fig_name>_blueprint.md`
2. **生成代码规范**：依据 `static/code_spec_template.md` 渲染生成：
   `markdown/<step_dir>/<fig_name>_code_spec.md`
3. **【语言约束】**：两个文档的**所有分析论述、算法说明、边界描述与审查清单必须 100% 使用中文书写**，仅保留英文代码标识符、数据表字段名与标准统计术语。
4. **强制门禁中断**：向用户结构化呈现科学结论与代码红线摘要，提示用户审查。
5. **严禁越权**：在获得用户显式确认通过前，**严禁**自动触发第二步（`nature-figure`）编写绘图代码！
