# Modeling paper-figure workflow

执行下列工作流；公共配置与检查规则由入口统一加载。

1. Run `python scripts/bootstrap.py --workspace <active-project-root> --profile modeling-competition --capability paper-figure`.
2. Read `references/paper-figure.md` completely and follow it as the authoritative prompt for visual design, chart/diagram construction, templates, export quality, review, and iteration. 适配实际数据时，尽量保留原模板的视觉结构、配色层次和关键图形元素，仅按数据语义与可读性需要作必要调整。 修图时优先调整位置、间距和尺寸，尽量保留色条、图例、关键标记等信息元素；确需删减时，说明原因及替代的表达方式。 渐变保真强要求：模板中的渐变填充、透明度层次和连续渐变配色属于关键样式，初次绘制和后续修图均须默认保留，尽可能复现原版视觉效果；不得仅为减少代码、方便实现或认为不影响数据表达而改成单层纯色、离散配色或仅留轮廓线。适配时优先调整渐变范围、层数、透明度和配色，在保持数据真实的前提下保留可辨识的渐变层次；只有数据语义不支持或调整后仍明显妨碍阅读时才作必要简化，并说明具体原因。
生成前先根据样本量、重复值和分布形态判断图形是否适合数据，再保真适配模板；小样本或大量相同值时可保留原始散点与简洁箱线，不必叠加密度层。采用雨云图时保留散点、箱体与半小提琴的错位布局，避免为凑齐元素而重叠堆放。

3. Use the executable paths in `<active-project-root>/.vivid/runtime.json`.

规划、对账与绘图要求从所选工作流加载；检查规则只维护在 review-policy.md。


保留绘图方法、模板与配方。检查范围和修复次数见 `../review-policy.md` （相对于 resources）。
