# Scientific Figure

一个面向不同研究项目的科研绘图 Skill。它把绘图工作拆成四个可回溯的阶段：

`Figure Spec → Build → Independent Audit → Render & QA`

核心目标是让图件的科学论断、数据映射、视觉编码和代码实现彼此对得上，同时不把某一个项目、期刊、语言或图表类型的习惯写成普遍规则。

## 使用方式

1. **Figure Spec**：根据研究目标、数据/结果产物和可选参考图，形成或迭代 `Figure Spec` 与 `Figure Code Spec`。这一阶段只规定需要考虑的事项，不替用户强行选择统计方法、异常值规则或绘图库。
2. **Build**：在两个 Spec 获得明确批准后，生成可审计的绘图实现、配置和测试；不直接渲染最终交付图。
3. **Independent Audit**：由三个相互独立的审计视角检查科学证据与映射、视觉编码与版式、实现与可复现性。审计可以指出 Spec 本身的问题。
4. **Render & QA**：在审计通过且用户授权后执行绘图，并检查文件、尺寸、字体、字号、分辨率、布局和数据映射。

每次实质性修改都覆盖当前 Spec，并使下游批准、审计和出图许可失效，避免旧报告继续约束新版本。

## 稳定的出版默认值

项目保留以下通用默认值，除非当前 Spec 明确记录了用户或目标媒介的覆盖：

- 图宽：88 mm、120 mm 或 180 mm；
- 字体：Arial；
- 普通图中文字：5–7 pt；
- 栅格导出：300 DPI。

这些是可覆盖的默认配置，不代表所有图件都必须使用同一刊物模板。

## 有意不写死的内容

核心 Skill 不强制 P99 截断、某一种统计检验、Tidy 数据表、Python/matplotlib、固定图表类型、必需参考图、Nature 标题或固定存储路径。它只要求在 Spec 中说明与当前图件有关的来源、单位、变换、不确定性、视觉通道、输出介质、可访问性、复现条件和 QA 标准。

`assets/` 与 `references/optional/` 中的素材是可选参考资源，不会被默认加载，也不改变项目的通用路由。

## 文件入口

- [SKILL.md](SKILL.md)：总路由与门禁；
- [references/spec-stage.md](references/spec-stage.md)：Spec 阶段；
- [references/build-stage.md](references/build-stage.md)：Build 阶段；
- [references/audit-stage.md](references/audit-stage.md)：三视角独立审计；
- [references/render-qa-stage.md](references/render-qa-stage.md)：渲染与 QA；
- [templates/figure-spec.md](templates/figure-spec.md)：图件设计模板；
- [templates/figure-code-spec.md](templates/figure-code-spec.md)：代码规格模板；
- [templates/figure-audit-report.md](templates/figure-audit-report.md)：审计报告模板。

## 边界

本 Skill 负责图件规划、实现门禁、审计和交付检查；不替代研究者对科学问题、数据质量、统计识别或最终论断的判断。任何无法由当前数据和 Spec 支持的结论，都必须在审计中降级或退回修改。
