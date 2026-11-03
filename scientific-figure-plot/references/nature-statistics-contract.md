# Nature 统计推断与数据契约规范 (Nature Statistics Contract)

本规范为 Nature 系列及高影响期刊的统计分析与科研绘图设定**硬性数据契约**。杜绝审稿人常见的“P值滥用”、“误差棒歧义”、“样本量缺失”与“数据口径前后脱节”问题。

---

## 一、 顶刊统计规范六大铁律 (The Six Rules of Nature Statistics)

1. **拒绝裸 P 值 (No Naked P-values)**：
   - 严禁仅报告 $P$ 值或星号（如 `* P < 0.05`）；
   - 必须同时报告**效应量 (Effect Size)** 与 **95% 置信区间 (95% CI)**（如 Cohen's $d$、$\eta^2$、Hazard Ratio、Odds Ratio、$r$、$R^2$）。
2. **精确报告 P 值 (Exact P-values)**：
   - 所有 $P \ge 0.001$ 必须报告精确数值，保留 2–3 位有效数字（例如 $P = 0.038$、$P = 0.004$）；
   - 仅当 $P < 0.001$ 时允许使用不等号（报告为 $P < 0.001$）；严禁写 $P = 0.000$ 或 $P = \text{NS}$。
3. **误差棒定义必须无歧义 (Explicit Error Bars)**：
   - 必须在图例（Caption）中明确声明误差棒代表什么：
     - 正态分布描述变异度：$\text{Mean} \pm \text{SD}$；
     - 估计总体均值精度：$\text{Mean} \pm \text{s.e.m.}$ 或 $\text{Mean with 95\% CI}$；
     - 偏态/非参数数据：$\text{Median with IQR}$（箱线图须标明须线定义，如 1.5 倍 IQR 或 5th–95th 百分位）。
   - 严禁在同一图表中混淆 SD 与 SEM。
4. **样本量标定 (Explicit Sample Size $N$)**：
   - 每一个子图、每一个散点或组别，必须标明明确的独立样本量 $n$（例如 $n = 12$ biologically independent samples）；
   - 区分“生物学独立重复”与“技术重复”。
5. **双侧检验原则 (Two-Sided Tests)**：
   - 所有假设检验默认采用双侧检验（Two-sided/Two-tailed）；若采用单侧检验，必须在 Blueprint 和正文中提供预先注册或强理论依据。
6. **多重重测矫正 (Multiple Testing Correction)**：
   - 对组间事后多重比较或基因组多重检验，必须明确说明校正方法（如 Tukey HSD、Bonferroni、Benjamini-Hochberg FDR），并报告校正后 $q$ 值或调整 $P$ 值。

---

## 二、 统计与绘图的核心数据契约 (Tidy Stats Data Contract)

为了防止绘图代码与统计分析割裂，流水线实行**「统计引擎先行，绘图引擎只读标准表」**原则。

统计分析脚本执行完成后，必须导出标准中间表（`.csv` 或 `.parquet`），供绘图脚本直接消费：

### 标准中间表 Schema 规范

| 字段名称 | 类型 | 含义与示例 |
| :--- | :--- | :--- |
| `panel` | str | 对应子图标号（例如 `'a'`, `'b'`） |
| `group` | str | 实验组/亚组名称（例如 `'Control'`, `'Exposure'`） |
| `x` | float/str | X 轴分类或连续自变量数值 |
| `estimate` | float | 点估计值（Mean, Median, Beta, HR, OR） |
| `se` | float | 标准误（若无则填 `None`） |
| `ci_lower` | float | 95% 置信区间下界 |
| `ci_upper` | float | 95% 置信区间上界 |
| `stat_val` | float | 检验统计量数值（$t$, $F$, $U$, $H$, $\chi^2$, $z$） |
| `df` | float/str | 自由度（如适用） |
| `p_val` | float | 精确 P 值（例如 `0.0028`） |
| `n` | int | 该点/组的样本量（例如 `45`） |
| `test_name` | str | 采用的假设检验名称（例如 `'Welch\'s t-test'`） |

> **红线约束**：绘图脚本 `scripts/plot_*.py` 中**严禁**临时调用 `scipy.stats` 计算 P 值或估计模型参数；绘图脚本只负责从标准契约表中读取数据、绘制图形、添加标注。

---

## 三、 假设检验选型与降级决策树 (Assumption-Driven Decision Tree)

运行 `scripts/stat_check.py` 自动探查数据并执行以下决策分支：

```
               [连续变量两组比较]
                      │
           正态性检验 (Shapiro-Wilk)
           ┌──────────┴──────────┐
      [两组均正态]           [任一组非正态]
           │                      │
     方差齐性 (Levene)       Mann-Whitney U 检验
     ┌─────┴─────┐           (报告 Median + IQR)
 [齐次]        [非齐]
   │             │
Student's   Welch's t-test
t-test      (报告 Mean ± SEM)
```

```
               [连续变量多组比较]
                      │
           正态性检验 (Shapiro-Wilk)
           ┌──────────┴──────────┐
      [全组均正态]           [任一组非正态]
           │                      │
     方差齐性 (Levene)       Kruskal-Wallis 检验
     ┌─────┴─────┐           + Dunn 事后校正
 [齐次]        [非齐]        (报告 Median + IQR)
   │             │
One-way     Welch's ANOVA
ANOVA       + Games-Howell
+ Tukey     (报告 Mean ± SEM)
```

---

## 四、 顶刊图例 (Caption) 统计规范写作模板

在生成最终图件时，伴随图件输出标准 Nature 句式图例：

> **Fig. 1 \| [核心结论短标题].**  
> **a**, [子图 a 实验与图形描述]. Data are presented as mean $\pm$ s.e.m. ($n = 30$ mice per group). Statistical significance was assessed by two-sided Welch's $t$-test ($t = 3.14$, d.f. = 54.2, $P = 0.0027$; Cohen's $d = 0.81$, 95% CI [0.28, 1.34]).  
> **b**, [子图 b 实验与图形描述]. Medians with interquartile ranges (IQR; 25th–75th percentiles) are shown ($n = 120$ observations). Two-sided Mann-Whitney $U$ test ($U = 1,420$, $P = 0.012$; rank-biserial correlation $r = 0.38$).  
> **c**, [子图 c 剂量反应曲线]. Solid curve indicates estimated hazard ratios (HR) derived from restricted cubic splines (3 knots), with shaded areas representing 95% confidence intervals ($N = 184,210$, events = 4,320).  
> Source data are provided as a Source Data file.
