---
name: vivid-figures-skill
description: 使用完整的生动数据图指导、140个完整配方（含32个新增截图恢复模板）和辅助脚本，规划、生成、修改及检查数学建模与科研图表；涵盖数据图、Draw.io/TikZ技术图、HTML/Mermaid和科学场景插图。
---

# Vivid Figures Skill — 生动数据图

使用开放 Agent Skills 格式。一套绘图指导、统一项目配置及按需加载的完整配方，支持数据图和多种技术图。

## 完整组合模板

需要问卷残差分布与相关关系组合图，或用户指定原版“小提琴＋Pearson 组合图”时，读取 [完整模板调用说明](templates/sem-violin-pearson/TEMPLATE.md)，直接运行随附原版代码；该模板默认保留自身样式，按专用说明执行。

## 数值图模板检索

首次选择数值图模板时读取 [数据与模板选择](figure-selection.md)，结合数据与目的跨库查卡片、看候选实图，再加载完整配方；这一步落实原有候选检索，不重复规划，修图和换色沿用已选模板。适用于下述上游规划及绘图工作流中的选图步骤。

选定或沿用模板后，按 [源码底稿与保真要点](template-fidelity.md) 复制完整代码并局部适配，绘制前读取所选卡片的源码保留重点；修图和换色也沿用这些要点。

## 加载与执行

1. 首次使用读取 [执行环境与配置](host-adapter.md)、[绘图指导](original/drawing-guide.md)、[检查与修复](original/review-policy.md) 及 [绘图入口](original/resources/ENTRYPOINT.md)。按入口选择工作流，完整读取其关联参考文档；未变化的指导可复用。只读本次涉及的图型，不加载所有工作流。
2. 数据图读取 [尺寸预计算](original/fragments/original-size-preflight.md)、[配方用色](original/fragments/original-color-usage.md) 和 [配色选择](color-selection.md)。按任务再读 [数值](original/fragments/data-figures.md)、[统计/机器学习](original/fragments/statistics-figures.md)、[优化](original/fragments/optimization-figures.md)、[图网络](original/fragments/graph-network-figures.md) 或 [技术图](original/fragments/technical-diagrams.md)。
3. 新建完整论文或整题图集时，执行 [上游规划](original/upstream-planning.md)。明确单图、已有图修复或用户限定的小批图，不重启整题规划。保留 FIGURE_MANIFEST 分类、执行顺序及恢复对账。
4. 执行 bootstrap、配置配色、检索完整配方、保真适配、绘制、实际看图和修复。修图和换色沿用已选模板，按保真要点保留渐变、透明度、描边和信息元素。

参考文档中的 `references/`、`workflows/`、`scripts/`、`assets/` 相对于 `original/resources/`；`_utils/`、`figures/`、`skills/shared-scripts/` 相对于任务工作区。优先使用本包维护的资源。
