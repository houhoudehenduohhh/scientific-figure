# Scientific Figure Code Audit Report (科研绘图代码多智能体独立审计报告)

> **审计性质**：本文件由 `figure-code-audit` 调度 3 个独立纯净 Subagent 并行审计生成，归档于 `markdown/<step>/<fig_name>_code_audit.md`。  
> **流转规则**：代码在未经本审计门禁签署前**严禁执行出图**。用户审查本报告中的缺陷清单与代码补丁建议后，确认修改方向再交付 `scientific-figure-plot` 固化与渲染。

---

# [图件代号] 绘图代码工程规格与多智能体审计报告

- **目标图件代号**：`Fig_X_<brief_name>`
- **关联代码工程规范**：`markdown/<step>/<fig_name>_code_spec.md`
- **被审计草稿脚本**：`scripts/<step>/plot_<brief_name>.py`
- **审计综合判定**：`[PASS 通过 / WARN 建议优化 / FAIL 阻断修改]`

---

## 一、三方智能体独立审计综合裁决 (Executive Summary)

| 审计维度 | 负责智能体角色 | 判定结果 (Status) | 发现缺陷项数 | 核心阻断级问题概述 |
| :--- | :--- | :---: | :---: | :--- |
| **维度 1: 统计契约与红线** | 统计契约审计员 (Subagent 1) | `PASS / WARN / FAIL` | [___] 项 | [如：现场调用 scipy 重算 P 值 / 静默丢弃缺失值] |
| **维度 2: 期刊版式与排版** | 版式排版审计员 (Subagent 2) | `PASS / WARN / FAIL` | [___] 项 | [如：字号跌破 5pt / 刻度未向内 / 尺寸非 88mm] |
| **维度 3: 任务断言与鲁棒性** | 代码鲁棒性审计员 (Subagent 3) | `PASS / WARN / FAIL` | [___] 项 | [如：缺少 output 大小断言 / 内存未释放] |

---

## 二、逐维度详细审计发现 (Detailed Findings)

### 1. 契约消费与反向红线审计 (Subagent 1)
- **Tidy 契约表 Schema 对齐**：
  - [通过 / 存在偏差]：[详细陈述]
- **反向红线排查**：
  - [x] 现场统计重算检查：[是否存在 scipy/statsmodels 违规计算]
  - [x] 静默数据过滤检查：[是否存在无日志 dropna]
  - [x] 日志语言检查：[是否 100% 纯英文输出]
- **数理与坐标轴映射**：
  - [评估基准参考线、对数尺度转换与误差棒正确性]

### 2. 期刊物理尺寸与文字排版审计 (Subagent 2)
- **图幅物理尺寸**：[核验单栏 88mm / 双栏 180mm 计算与 dpi 参数]
- **字号阶梯合规性**：
  - Panel 标号：[是否为 9pt Bold]
  - 坐标轴/图例：[是否为 7pt]
  - 刻度/正文：[是否为 5–6pt]
  - 底线探查：[是否存在 < 5pt 风险]
- **坐标轴向内刻度与线宽**：[0.5pt 轴线、向内刻度检验]
- **图元防碰撞与几何不变性**：[空间地图是否 equal aspect，文本有无重叠]

### 3. OpenSpec 任务落地与防御性断言审计 (Subagent 3)
- **原子 Tasks 覆盖度**：
  - [Task 1 至 Task 4 的完整映射评估]
- **程序化断言 (assert) 落地情况**：
  - 前置断言：[是否断言输入存在与必需字段]
  - 过程断言：[是否断言数据非空与范围]
  - 产出断言：[是否断言输出图片存在且体积有效]
- **防御性退出与资源释放**：[plt.close()、try-except 与 sys.exit(1) 审查]

---

## 三、代码精准修复建议与 Patch 补丁 (Actionable Code Patches)

针对上述审计检出的缺陷，提供针对性的修正代码块（Diff / Replacement）：

### 缺陷 1：[缺陷简述]
```python
# 修改前 (Original Problematic Code)
...

# 修改后 (Recommended Compliant Patch)
...
```

### 缺陷 2：[缺陷简述]
```python
# 修改前 (Original Problematic Code)
...

# 修改后 (Recommended Compliant Patch)
...
```

---

## 四、人工审计放行门禁 (Human Sign-off Gate)

- [ ] Subagent 1 发现的契约与红线问题已评估，无阻断项。
- [ ] Subagent 2 发现的版式字号问题已修正，满足 Nature 物理规格。
- [ ] Subagent 3 确认原子断言完整，具备防御性退出机制。
- **最终处置决定**：`[ ] 采纳建议直接执行修改 / [ ] 调整部分代码后出图 / [ ] 重新生成代码`
