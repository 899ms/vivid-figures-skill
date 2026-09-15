# 通用宿主适配（仅迁移接口）

`<SKILL>` 为本 skill 的绝对目录，`<CAP>` 为 `<SKILL>/original`，`<RES>` 为 `<CAP>/resources`，`<WORKSPACE>` 为当前任务目录。原文 `{capabilityRoot}` 对应 `<CAP>`。历史来源路径仅用于溯源，不是运行依赖。

`original/` 是逐字保留的来源资源。执行其中历史兼容说明时，Claude、Codex 或 agent 均指当前宿主中的智能体；任何“Claude means Codex”字样由本适配覆盖。原文列出的 Codex 专用 MCP 名称不构成依赖，改用宿主已有的等价能力。

## 执行路径与环境

使用宿主可运行的 Python（原脚本需要 Python 3.10+），按所选工作流安装 [Python 依赖](requirements.txt)。现有依赖可直接使用，不切换到原应用托管运行时。原文 Bash 片段由宿主 Bash 执行，并让 `python` 指向同一个环境。

```text
python "<RES>/scripts/resolve_runtime.py"
python "<RES>/scripts/bootstrap.py" --workspace "<WORKSPACE>" --profile modeling-competition --capability all
```

使用 bootstrap 生成的 `<WORKSPACE>/.codex-plot-runtime.json` 解析工具路径。该名称仅为原脚本兼容文件名，不要求 Codex。执行脚本时工作目录为 `<WORKSPACE>`；原文中的 `$MH_PYTHON` 设为已选择的 Python，`$MH_TOOLS_DIR` 设为 `<WORKSPACE>/tools`。独立使用不设置 `HAJIMI_CAPTURE_ELECTRON`；HTML 使用本机 Chrome。浏览器/Draw.io 可用 `CHROME_PATH`/`DRAWIO_PATH` 指定，TikZ 使用 XeLaTeX，Mermaid 使用 mmdc，PDF 预览按原文使用 PyMuPDF 或 Poppler。它们仅在对应绘图路径使用。

原版 `CAPABILITY.md`、`manifest.json`、`PACKAGE_MANIFEST.md` 与 `PROMPT_PROVENANCE.json` 为来源记录；其中应用激活阶段、托管路径、Codex 标识及旧版本说明不作为当前 Skill 的运行入口。

## 原宿主接口对应

| 原接口或上下文 | 当前宿主中的对应执行 |
|---|---|
| read/ls/find/grep、Bash、Write/Edit、Claude/Codex工具名 | 使用宿主的 Read、Glob、Grep、Bash、Write、Edit 或等价文件与终端工具；保留命令含义与绘图原文 |
| 读取生成图、视觉检查工具 | 用宿主的图像读取或视觉能力实际打开生成图；按原版检查项目及当前修复轮次执行。旧外部视觉API脚本由宿主视觉能力承接，不以静态检查代替看图 |
| `hajimi_validate_figure_plan(action="begin", minimum=…)` | `node --experimental-strip-types "<SKILL>/scripts/figure-plan-cli.mjs" begin --workspace "<WORKSPACE>"`；仅用户明确提高整题下限时追加 `--minimum N` |
| `hajimi_validate_figure_plan(action="validate", planPath=…)` | `node --experimental-strip-types "<SKILL>/scripts/figure-plan-cli.mjs" validate --workspace "<WORKSPACE>" --plan FIGURE_PLAN.json`；使用原版校验函数，需 Node.js 22.6+ |
| `hajimi_stage8_phase` | 在当前计划记录 figures/writing/review/ready；不调用应用状态API。只出图时按原策略在 figures 完成后停止 |
| frozen Claim/Evidence、前七阶段材料 | 本任务已提供或已确认的数据、模型结果及证据文件；在计划保留来源对应，不为独立绘图启动原应用的完整论文状态机 |
| `hajimi_bind_publication` / `hajimi_validate_delivery` | 以原 FIGURE_MANIFEST、源文件、实际输出和适用的原版检查脚本执行对账；独立skill不声称建立应用发布绑定、自动证据冻结或人工验收状态 |
| “规划通过后才能运行shell” | 原应用当前 `requireFigurePlan` 已为空操作，shell可用；保留先规划后绘图顺序，不增加宿主执行拦截 |

当前 `stage8-policy` 保留全部绘图、修复与适用的页面复核要求。其正文写作部分只在用户确实要求写论文时适用，相关论文写作skill不属于本绘图包；本迁移不扩展论文写作能力。

科学插图工作流保持原有规划、构图、风格、评分与迭代提示词。渲染时将原文的 Codex ImageGen 调用映射到当前宿主实际提供的图像生成工具或已配置的 MCP 图像生成能力；视觉复查使用宿主视觉能力。若宿主没有图像生成工具，只报告该渲染依赖缺失，不改写提示词或改用未经授权的外部服务。数据图、HTML、Draw.io、TikZ 与 Mermaid 路径不依赖图像生成工具。

## 绘图项目标记

统一沿用 expressive 绘图指导。设置标记前执行 [配色选择](color-selection.md) 的询问与选择规则；仅询问配色，不按项目名抽选风格。

在工作区 `CLAUDE.md` 中保留已有内容，设置原工具读取的标记（文件名为兼容接口）：用户选择默认或珊瑚青绿时，使用 `MH_DATA_FIG_PALETTE=custom`、`MH_DATA_FIG_COLORS=#4ECDC4,#FF6B6B,#45B7D1,#F7A072,#A06CD5,#F79256,#7DCFB6`、`MH_DATA_FIG_STYLE=clean_open`。其他配色按配色选择文件替换颜色标记。用户已有版式设置不因换色改变。

标记使用原格式 `<!-- KEY=VALUE -->`；尊重用户已有自定义颜色或其他已选配置。生成代码在 `setup_style()` 后读取 `pu.PALETTE`/`pu.COLORS`，与原路由指导一致。
