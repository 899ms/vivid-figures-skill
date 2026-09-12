# Vivid Figures Skill（生动数据图 Skill）

面向 Anthropic Agent Skills 兼容宿主的科研与数学建模绘图 Skill。包内保留完整绘图指导、108个原版配方、expressive/restrained 两种模式、字体、检查器和渲染辅助脚本。

> **授权限制：本仓库仅允许个人、非商业使用。未经版权所有者事先书面许可，禁止修改、改编、二次开发、制作衍生作品、复制传播、转售、提供付费服务或以任何形式用于商业用途。**完整条款见 [LICENSE](LICENSE)。仓库内第三方组件及材料仍遵循各自的许可证和声明。

## 安装 Skill

Claude Code 个人级安装：

```bash
git clone https://github.com/yjz211/vivid-figures-skill.git ~/.claude/skills/vivid-figures-skill
```

仅对一个项目启用：

```bash
git clone https://github.com/yjz211/vivid-figures-skill.git .claude/skills/vivid-figures-skill
```

重新启动或重新打开 Anthropic 宿主后，让 Claude 自动选择本 Skill；支持斜杠技能调用的宿主也可使用 `/vivid-figures-skill`。

## 绘图模式与配色

鲜艳舒适型（expressive）和稳重科研型（restrained）都可选择：珊瑚青绿、海洋暖橙、鸢尾杏桃、森林日光、浆果冰蓝、科研原配色，也支持自定义颜色。模式原配色分别是珊瑚青绿和科研原配色。

使用时 Agent 会先询问尚未确定的模式/配色；已明确选择、要求沿用、使用默认或交给 Agent 决定时，不重复询问。例如：“用稳重版，海洋暖橙配色画图”。配色只改变颜色搭配，原有选图、模板、渐变层次、尺寸与修复流程不变。完整选项与标记格式见 [配色选择](color-selection.md)。

## 电脑需要安装什么

### 基础数据图：必须

- Python 3.10或更高版本。
- 能读取本地文件、运行 Python、写出 PNG/PDF 并读取图片的 Anthropic Agent Skills 宿主。
- Python依赖。完整安装命令：

```bash
python -m venv .venv
```

Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

macOS/Linux：

```bash
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

`requirements.txt` 是完整能力依赖，包含 NumPy、pandas、SciPy、Matplotlib、Seaborn、scikit-learn、statsmodels、SymPy、NetworkX、Pillow、PyMuPDF、GeoPandas、libpysal、esda 和 CairoSVG 等。普通数据图不一定逐项使用，但一次完整安装最省事。

### 规划校验：建议安装

- Node.js 22.6或更高版本。它用于运行原规划校验 CLI，不负责 Matplotlib 绘图。

检查版本：

```bash
node --version
python --version
```

### 按需安装

| 功能 | 需要的软件 | 说明 |
|---|---|---|
| HTML图与HTML转PNG/PDF | Google Chrome或Chromium | 可用 `CHROME_PATH` 或 `PUPPETEER_EXECUTABLE_PATH` 指定可执行文件 |
| Draw.io技术图导出 | draw.io Desktop | 可用 `DRAWIO_PATH` 指定可执行文件 |
| TikZ、精密几何与中文LaTeX | TeX Live或MiKTeX，必须包含XeLaTeX与中文支持 | 命令行应能运行 `xelatex` |
| Mermaid渲染 | Node.js及 `@mermaid-js/mermaid-cli` | 安装：`npm install -g @mermaid-js/mermaid-cli`，命令行应能运行 `mmdc` |
| PDF转图片备用路径 | Poppler | Skill优先使用 `PyMuPDF`；已有PyMuPDF时Poppler通常不是必需项 |
| Bash检查脚本 | Bash | macOS/Linux通常已有；Windows可安装Git for Windows并使用Git Bash，或使用WSL |
| AI科学场景插图 | 宿主提供的图像生成工具或已配置的MCP图像生成服务 | 数据图、HTML、Draw.io、TikZ和Mermaid不依赖此项；Skill不会自行调用未经配置的外部服务 |

基础数据图不要求 OpenAI API Key，也不要求安装 HaJiMi 应用。

## 检查本机环境

```bash
python original/resources/scripts/resolve_runtime.py
```

输出中的 `python` 应有路径。只检查当前要使用的可选能力即可；例如准备画 Mermaid 时确认 `mmdc` 有路径，准备画 TikZ 时确认 `xelatex` 有路径。

## 初始化一个绘图工作区

在目标项目中执行：

```bash
python /path/to/vivid-figures-skill/original/resources/scripts/bootstrap.py \
  --workspace /path/to/project \
  --profile modeling-competition \
  --capability paper-figure
```

常用 `--capability` 值包括 `paper-figure`、`paper-technical-diagram`、`paper-figure-html`、`mermaid-diagram`、`paper-illustration` 和 `all`。

## 兼容说明

- `SKILL.md` 是 Anthropic Agent Skills 入口。
- `anthropic-host-adapter.md` 只负责把原宿主工具映射到 Anthropic 宿主，不更改绘图标准。
- `original/` 是逐字保留的原始绘图资源。
- bootstrap 生成的 `.codex-plot-runtime.json` 只是兼容文件名，不需要安装 Codex。
