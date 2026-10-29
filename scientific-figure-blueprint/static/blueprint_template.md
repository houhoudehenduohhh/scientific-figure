# Scientific Figure & Statistical Blueprint Template (科研图表与统计分析蓝图规范)

> **铁律**：本文件由 `scientific-figure-blueprint` 自动生成，归档于 `markdown/<step>/<fig_name>_blueprint.md`。必须经人工审查签署通过后，方可交付 `scientific-figure` 编写绘图代码。  
> **语言约束**：本蓝图文件的**所有论述、解读、推断方案与文字描述必须 100% 使用中文输出**；仅保留英文代码标识符、数据表字段名与标准统计术语。

---

# [图件编号与主题] 顶刊科研图件综合规划蓝图

- **目标图件代号**：`Fig_X_<brief_name>`
- **目标期刊规格**：单栏 (88 mm) / 1.5 栏 (120 mm) / 双栏 (180 mm)
- **输入原始数据**：`Dataset/<step>/<raw_data_file>.parquet` (或 `.csv`)
- **中间统计契约表**：`Dataset/<step>/stats_results_<brief_name>.parquet`
- **生成代码目标**：`scripts/<step>/plot_<brief_name>.py`
- **审查签署状态**：`[ ] 待确认 / [x] 已确认通过`

---

## 第一部分：范文/参考图深度解构 (Reference Deconstruction)

### 1. 核心科学论断 (Scientific Claims)
- **主图传递的核心结论**：[一句话明确该图向审稿人证明的科学发现]
- **各子图证据链推进逻辑**：
  - **Panel a**：[基线/宏观暴露分布/现象确立]
  - **Panel b**：[核心干预/剂量反应曲线/主效应回归]
  - **Panel c/d**：[异质性/敏感性/机制验证]

### 2. 绘图形式与视觉编码 (Visual Encodings)
| 子图编号 | 图表类型 (Archetype) | X 轴物理意义 (Scale) | Y 轴物理意义 (Scale) | 分组/颜色映射 (Color Hue) | 误差/离散度表达 (Uncertainty) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **a** | 散点/限制性样条等 | 连续变量 (线性/对数) | 风险比 HR (Log scale) | 暴露组/情景 | 95% 置信带 (Shaded band) |
| **b** | 分组柱状/森林图等 | 效应值 Estimate | 亚组分类 Category | 显著性分类 | 95% 置信区间 (Error bar) |

### 3. 排版网格与空间结构 (Layout Topology)
- **多子图排列矩阵**：[例如 $2 \times 2$ 等宽排列、或非对称 Hero Layout]
- **空间比例分配**：[各 Panel 宽高比、留白规划]
- **图例共享方案**：[独立图例轴 (Legend-only axis) 或内嵌于 Panel 顶部空白区]

---

## 第二部分：数据结构探查、缺失值与异常值质量评估 (Data Structure & Quality Audit)

> **探查执行方式**：必须在编写蓝图时调用 `python .agents/skills/scientific-figure-blueprint/scripts/stat_check.py --data <数据路径> --audit-data`，将真实扫描结果结构化填入以下各小节。

### 1. 数据集基础结构与规模探查 (Data Dimensions & Types)
- **数据集宏观规模**：总行数 $N = [______]$，总特征列数 $K = [______]$，内存占用约 $[______]\text{ MB}$。
- **记录唯一性检查**：重复记录数 $[______]$ 行（若有主键/唯一标识，明确声明主键冲突情况）。
- **字段级结构概况**：
| 关键分析字段 | 数据类型 (dtype) | 非空计数值 | 唯一取值数 (nunique) | 是否为常量/近零方差 (NZV) |
| :--- | :--- | :--- | :--- | :--- |
| `[exposure_col]` | float64 / int64 | [______] | [______] | 否 (连续分布) |
| `[outcome_col]` | int32 / float64 | [______] | [______] | 否 |
| `[covariate_col]` | category / float64 | [______] | [______] | [是 / 否] |

### 2. 缺失值诊断与样本留存评估 (Missing Value Audit & Complete-Case Assessment)
- **分析所需变量完整案例 (Complete-case) 样本留存率**：
  - 核心分析字段全非空样本量：$N_{\text{complete}} = [______]$ 行（占全集 $[______]\%$）。
  - 因缺失待剔除/处理的样本损耗量：$\Delta N = [______]$ 行（占全集 $[______]\%$）。
- **字段级缺失率明细与严重度评估**：
| 变量字段名 | 缺失行数 | 缺失百分比 (%) | 缺失严重度评级 | 推荐处置策略 |
| :--- | :--- | :--- | :--- | :--- |
| `[col_name]` | [___] | [___]% | 无 (0%) / 低 (<1%) / 中 (1-5%) / 高 (5-20%) / 严重 (>20%) | [完整案例剔除并打印日志 / 中位数插补 / 多重插补 MICE / 排除变量] |

### 3. 异常值检验与截断策略 (Outlier Inspection & Truncation Strategy)
- **连续型核心变量分位数与偏度诊断**：
| 变量字段名 | 最小值 (Min) | P1 | P5 | 中位数 (Median) | 均值 (Mean) | P95 | P99 | P99.5 | 最大值 (Max) | 偏度 (Skewness) | 偏斜度评估 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `[exposure_col]` | [___] | [___] | [___] | [___] | [___] | [___] | [___] | [___] | [___] | [___] | [近似对称 / 重度右偏 / 重度左偏] |

- **异常值检出准则与具体数据表现**：
  - **Tukey IQR 规则越界检出**：下界 $[Q1 - 1.5 \times IQR] = [______]$，上界 $[Q3 + 1.5 \times IQR] = [______]$，越界离群样本共 $[______]$ 例。
  - **极端上尾分位数表现**：P99 上界数值为 $[______]$，最大观测值达 $[______]$（最大值约为 P99 的 $[______]$ 倍）。
  - **物理合法域排查**：是否包含非物理负值、超出理论上限或不可能出现的测量极端值：`[无 / 发现 xxx]`。
- **推荐异常值处理策略**：
  - **截断时机与口径**：[明确是否执行 P99 / P99.5 上界 Winsorization 缩尾截断；明确替换为阈值还是丢弃]
  - **分布规整转换**：[若严重右偏，评估是否需要 $\ln(x+1)$ 或对数尺度映射]

### 4. 数据预处理落地指引与清洗清单 (Data Preprocessing Actionable Directives)
依据上述探查结果，明确代码工程在数据清洗阶段必须履行的指令：
1. **强制类型转换**：[明确哪些字段需强转为 category、int 或 float]
2. **缺失值清洗执行指令**：[严格禁止静默过滤，必须在代码中显式打印丢弃/插补样本数]
3. **异常值截断执行指令**：[计算全局/分国别的 P99 上界，执行 `df[col] = df[col].clip(upper=p99_val)`，断言 `assert df[col].max() <= p99_val` 并输出截断影响行数]
4. **有效样本量断言**：[清洗后进入统计模型的样本量必须断言 $N \ge [______]$]

---

## 第三部分：数据分析方案与统计契约 (Statistical Analysis Plan)

### 1. 统计假设检验与推断方案 (Hypothesis Testing)
- **正态性与方差齐性探查**：[运行 `scripts/stat_check.py` 结果汇报：Shapiro-Wilk / D'Agostino-Pearson 与 Levene 检验]
- **采用的检验方法**：[明确检验方法，如双侧 Welch's t-test、Cox 比例风险回归、Mann-Whitney U、Kruskal-Wallis]
- **效应量与不确定性**：[明确报告何种效应量（Cohen's d、Hazard Ratio、Odds Ratio）及 95% CI]
- **统计模型参数设置**：[明确自变量、结局变量、混杂协变量、聚类稳健标准误层级 (Cluster SE)]

### 2. 标准化中间数据契约 (Tidy Stats Data Contract Schema)
> 统计分析脚本必须输出符合以下 Schema 的中间表，严禁绘图脚本临时重算统计模型：

| 字段名 | 类型 | 含义与示例 |
| :--- | :--- | :--- |
| `panel` | str | 对应子图标号（`'a'`, `'b'`） |
| `group` | str | 分组名称（`'Control'`, `'Exposed'`） |
| `x` | float/str | X 轴自变量 |
| `estimate` | float | 估计值（HR, Beta, Mean, Median） |
| `se` | float | 标准误 |
| `ci_lower` | float | 95% CI 下界 |
| `ci_upper` | float | 95% CI 上界 |
| `stat_val` | float | 统计量数值（$t, F, \chi^2, z$） |
| `p_val` | float | 精确 P 值（保留 2-3 位有效数字） |
| `n` | int | 独立有效样本量 |
| `test_name` | str | 假设检验全称 |

---

## 第四部分：目标图件设计与本地数据映射 (Target Plotting Design)

### 1. 本地数据预期结论 (Target Claims)
- **本地数据的对应科学论点**：[按照范文逻辑，本地数据应该得出什么科学结论]
- **子面板结论分配**：
  - **Panel a (本地)**：[对应本地数据的变量与结论]
  - **Panel b (本地)**：[对应本地数据的变量与结论]

### 2. 字段-视觉通道映射表 (Data-to-Aesthetics Mapping)
| 子图编号 | 输入数据源文件 | X 轴绑定字段 | Y 轴绑定字段 | 颜色/形状映射字段 | 统计标注项 (P值 / N / CI) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **a** | `Dataset/...` | `exp_dose` | `hr_estimate` | `model_type` | $N = \text{xxxx}$, P-trend |
| **b** | `Dataset/...` | `subgroup` | `hazard_ratio` | `p_val < 0.05` | $P = 0.003$, 95% CI |

### 3. 物理排版与期刊技术规格 (Physical Journal Specs)
- **总画幅尺寸**：宽 [88 / 180] mm $\times$ 高 [___] mm (边缘留白 12 mm)
- **字体规范**：Arial 无衬线字体，Panel 标号 9 pt 加粗，正文/刻度 5–7 pt 不加粗
- **轴线与刻度**：轴线宽 0.5 pt，刻度向内 (主刻度 3 mm / 次刻度 1.5 mm，线宽 0.5 pt)
- **配色标准**：课题组标准 5 色调色板 (LAB_PALETTE) 或 Okabe-Ito 色盲友好色谱
- **导出格式**：默认 300 DPI PNG 供快速审查；用户显式要求时再导出矢量 PDF/SVG

---

## 第五部分：配套代码工程规范声明 (Code Spec Link)

> **物理隔离原则**：为确保大模型 Token 算力 100% 聚焦于代码严谨性与数理边界，本图件的技术实现规格与任务清单**不在此处挤压生成**，而是独立存放于同目录下的配套文件：
> - **配套代码工程规范**：`markdown/<step>/<fig_name>_code_spec.md`
> - **包含核心内容**：
>   1. 脚本架构与模块划分（统计脚本 `01_run_stats_*.py` + 绘图脚本 `02_plot_*.py`）；
>   2. 形式化规格与数理不变性（前置条件校验、精确公式、缺失值处理与异常值 P99 截断口径）；
>   3. 反向红线与禁止项（严禁静默过滤、严禁绘图脚本重算 P 值、全英文日志）；
>   4. OpenSpec 原子任务清单与带断言的验收标准（Tasks with Verification Assertions）。

---

## 第六部分：科学蓝本审查门禁签署 (Review Gate Sign-off)

- [ ] 范文科学逻辑与视觉编码已准确解构，无误读。
- [ ] 数据结构已完成真实探查，样本规模、字段类型与近零方差字段已核对。
- [ ] 缺失值诊断完整，缺失机制评估与完整案例样本留存损耗已确认。
- [ ] 异常值分布与偏度已明确，P99 缩尾截断/转换策略与物理边界处理已确认。
- [ ] 统计假设检验方法与 Tidy 数据契约已明确定义。
- [ ] 本地数据字段映射完整，无口径不一致。
- [ ] 物理期刊尺寸（88/180 mm、Arial 5–7 pt、向内刻度、默认 PNG 导出）符合规范。
- [ ] 配套的 `<fig_name>_code_spec.md` 代码工程规范已同步生成。
- **审查决定**：`[待确认 / 驳回修改 / 确认通过]` (仅在用户显式确认通过后，方可触发编写代码)
