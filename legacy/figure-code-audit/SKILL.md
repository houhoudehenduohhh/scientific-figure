---
name: figure-code-audit
description: >-
  顶刊科研绘图代码多智能体独立审计引擎（流水线中间门禁）。在绘图草稿代码生成后、实际执行出图前触发。严禁未经审计直接执行代码！负责调用 3 个独立纯净 Subagent，分别从【统计契约与反向红线】、【期刊版式与字号刻度】、【原子任务覆盖与程序化断言】三个严苛维度实施独立交叉审计，汇编结构化审计报告（markdown/<step>/<fig_name>_code_audit.md）并给出具体修复 Patch，供人工决策与代码完善后放行出图。
---

# 顶刊科研绘图代码多智能体独立审计引擎 (Figure Code Audit Gate)

> [!IMPORTANT]
> **代码执行前置审计门禁 (Pre-Execution Audit Gate & Zero Blind-Run)**:
> 严禁在生成绘图草稿代码后立即盲目执行（Blind Run）！
> 1. **强制审计前置**：绘图脚本生成后，必须由本技能调度 **3 个独立纯净的 Subagent** 进行单向隔离交叉审查。
> 2. **独立多视角裁决**：
>    - Subagent 1 审查【统计契约与反向红线】；
>    - Subagent 2 审查【期刊版式与排版字号】；
>    - Subagent 3 审查【原子任务覆盖与程序化断言】。
> 3. **汇编报告与强制停机**：将三方审计结果汇编为 `markdown/<step>/<fig_name>_code_audit.md`，提供具体的代码修复 Patch。输出完成后**无条件停机**，将裁决权交还用户。用户决策确认后再进入 `scientific-figure-plot` 固化并渲染出图。

```
[输入 1: 经确认的 markdown/<step>/<fig_name>_code_spec.md (OpenSpec工程规格)]
[输入 2: 待审计草稿代码 scripts/<step>/plot_<fig_name>.py]
               ↓
    【figure-code-audit】(多智能体独立审查引擎)
       ├── 并行调度 Subagent 1: 契约与统计规范审计 (Tidy消费/禁止重算/纯英文日志)
       ├── 并行调度 Subagent 2: 期刊版式与排版审计 (88mm宽度/Arial 5-7pt/向内刻度/防碰撞)
       └── 并行调度 Subagent 3: 代码鲁棒性审计 (Task覆盖/前中后断言assert/防御性退出)
               ↓
       【汇编综合审计报告】(markdown/<step>/<fig_name>_code_audit.md)
       ├── 三方综合裁决矩阵 (PASS / WARN / FAIL)
       ├── 逐维度缺陷清单
       └── 针对性修复建议与精准代码 Patch
               ↓
       【★ 强制人机交互停机等待决策】
          (用户审阅审计报告 -> 决定采纳 Patch 或调整)
               ↓
       【scientific-figure-plot】(固化修正脚本，最终执行 300 DPI 渲染与质检)
```

---

## 审计执行标准协议 (Execution Protocol)

### 1. 审计前置就绪检查 (Pre-Audit Verification)
- 验证代码工程规范 `markdown/<step>/<fig_name>_code_spec.md` 是否已签署通过；
- 验证待审计的草稿代码 `scripts/<step>/plot_<fig_name>.py` 是否已写入本地磁盘；
- 若文件缺失，立即提示阻断并返回前置步骤。

### 2. 调度 3 个独立纯净 Subagent 实施专项审计 (Three-Agent Parallel Audit)
主代理通过 `invoke_subagent` 分别唤起 3 个互相隔离的 Subagent，注入对应的代码与审计清单：

#### ① Subagent 1: 契约与统计规范审计员
- **Role**: `Figure Contract Auditor`
- **审计重点**：参考 `references/figure-audit-checklists.md` 第一节：
  - 是否严格从 `Dataset/` 中消费 Tidy 结果契约表；
  - **红线排查**：严禁调用 `scipy.stats` 或 `statsmodels` 临时重算 P 值或拟合统计模型；
  - **红线排查**：严禁隐式 `dropna()`，过滤必须有丢弃计数英文日志；
  - **红线排查**：控制台输出是否 100% 英文。
- **输出**：该维度的判定状态 (`PASS/WARN/FAIL`)、缺陷清单及对应代码修复片段。

#### ② Subagent 2: 期刊版式与排版拓扑审计员
- **Role**: `Journal Layout Auditor`
- **审计重点**：参考 `references/figure-audit-checklists.md` 第二节：
  - 图幅宽度是否精确匹配单栏 88 mm、1.5 栏 120 mm 或双栏 180 mm；
  - 字体是否为 Arial，Panel 标号是否 9 pt Bold，轴标题是否 7 pt，刻度/注释是否 5–6 pt；
  - 底线字号排查：是否存在 $< 5\text{ pt}$ 的隐患；
  - 轴线宽是否为 0.5 pt，刻度线是否强制向内；
  - 空间地图是否锁死 `ax.set_aspect('equal')`，图元是否存在重叠碰撞。
- **输出**：该维度的判定状态 (`PASS/WARN/FAIL`)、缺陷清单及对应代码修复片段。

#### ③ Subagent 3: 代码鲁棒性与任务断言审计员
- **Role**: `Code Robustness Auditor`
- **审计重点**：参考 `references/figure-audit-checklists.md` 第三节：
  - 是否完整映射了 `code_spec.md` 中声明的 Task 1 至 Task 4 清单；
  - 是否落实了必需的程序化断言（前置文件存在断言、过程数据有效断言、后置文件输出体积断言 `assert fig_path.stat().st_size > 10000`）；
  - 是否显式执行 `plt.close()` 释放内存；
  - 致命异常是否调用 `sys.exit(1)` 退出。
- **输出**：该维度的判定状态 (`PASS/WARN/FAIL`)、缺陷清单及对应代码修复片段。

### 3. 汇编输出结构化审计报告 (Aggregate Audit Report)
主代理汇总 3 个 Subagent 的独立反馈，依据 `static/figure_audit_template.md` 渲染并生成：
`markdown/<step>/<fig_name>_code_audit.md`
- 包含三方综合裁决矩阵（PASS / WARN / FAIL）；
- 归纳逐项缺陷与危害等级；
- 提供精准的「修改前 vs 修改后」代码补丁 (Patch)。

### 4. 强制停机与人机决策交互 (Mandatory Stop & Human Decision)
- 向用户简洁呈报审计综合结论（如：2 项 WARN，1 项 FAIL）；
- 结构化列出核心代码修复建议；
- **无条件停止调用任何工具**，等待用户人工审查：
  - 用户确认采纳 Patch `->` 触发 `scientific-figure-plot` 打补丁并执行渲染出图；
  - 用户提出调整需求 `->` 结合用户指令修正代码。
