# 配色选择

本 Skill 使用一套绘图指导，配色只决定颜色搭配。七套配色及颜色顺序唯一维护于 [palettes.json](original/resources/assets/shared-scripts/palettes.json)，文档和示例不另存一份颜色表。

可选：**橄榄杏棕（默认）**、珊瑚青绿、蓝粉浅彩、蓝天绿地、柔绿森林、粉彩少女、海洋清风，以及自定义颜色。「橄榄行踪」按现有橄榄杏棕识别。

已有选择时沿用，补图或修图不重复询问。用户未指定配色时使用默认；明确要求由助手决定时可选择并简短告知。用户自己的颜色优先，不按目录名抽选主题。

在初始化工作区后，用所选 Python 执行：

```bash
python _utils/vivid_config.py palettes
python _utils/vivid_config.py set palette olive-apricot
```

命令可加 `--workspace <任务目录>`，也可在其子目录运行。配置保存在 `.vivid/config.json`。预设只保存 ID，读取时从色板文件取得颜色；自定义使用 `palette: "custom"` 与至少两个 HEX 字符串构成的 `colors` 数组。一次写入自定义设置：

```python
from _utils.vivid_config import write_config
write_config(workspace, palette="custom", colors=user_colors)
```

生成代码在 `setup_style()` 后读取 `pu.PALETTE` / `pu.COLORS`。换色不改变已选模板、用户已有版式、字体尺寸、渐变、透明度或审图要求。分类色随项目选择，连续量沿用对应配方的连续色图。流程/框图统一主色，工程图保留原配色，批注白底，具体执行见 [绘图指导](original/drawing-guide.md)。
