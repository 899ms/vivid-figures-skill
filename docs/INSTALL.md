# 安装 Vivid Figures

[返回首页](../README.md)

安装分两步：先把 Skill 放到 AI 助手能找到的位置，再给它准备可用的 Python 环境。以下以 **Claude Code 的个人级安装**为例，装好后可在多个项目中使用。

## 1. 准备基础软件

| 软件 | 用途 | 要求 |
|---|---|---|
| Claude Code，或能加载 Agent Skills 的其他助手 | 读数据、执行绘图代码、看图与修图 | 需要文件、终端执行和图像读取能力 |
| Python | 运行数据分析和绘图代码 | 3.10+ |
| Git | 下载与更新本仓库 | 使用下方克隆和更新命令时需要 |
| Bash | 运行随附的图表检查脚本 | Windows 推荐 Git for Windows 的 Git Bash；macOS/Linux 通常已有 |
| Node.js | 运行完整图集的规划校验工具 | 建议 22.6+；普通 Matplotlib 绘图不依赖它 |

安装 Python 后，先在终端确认 `python --version`（macOS/Linux 可用 `python3 --version`）能正常显示版本。

## 2. 下载并安装 Python 依赖

下面使用独立虚拟环境，避免与其他项目的 Python 依赖混在一起。命令中的安装目录有空格也可以使用。

### Windows：PowerShell

```powershell
git clone https://github.com/yjz211/vivid-figures-skill.git "$env:USERPROFILE/.claude/skills/vivid-figures-skill"
python -m venv "$env:USERPROFILE/.claude/skills/vivid-figures-skill/.venv"
& "$env:USERPROFILE/.claude/skills/vivid-figures-skill/.venv/Scripts/python.exe" -m pip install --upgrade pip
& "$env:USERPROFILE/.claude/skills/vivid-figures-skill/.venv/Scripts/python.exe" -m pip install -r "$env:USERPROFILE/.claude/skills/vivid-figures-skill/requirements.txt"
```

这些命令直接调用虚拟环境中的 Python，不需要运行激活脚本。

### macOS / Linux：终端

```bash
git clone https://github.com/yjz211/vivid-figures-skill.git "$HOME/.claude/skills/vivid-figures-skill"
python3 -m venv "$HOME/.claude/skills/vivid-figures-skill/.venv"
"$HOME/.claude/skills/vivid-figures-skill/.venv/bin/python" -m pip install --upgrade pip
"$HOME/.claude/skills/vivid-figures-skill/.venv/bin/python" -m pip install -r "$HOME/.claude/skills/vivid-figures-skill/requirements.txt"
```

部分 Linux 发行版需要先通过系统包管理器安装 `python3-venv`，才能创建虚拟环境。中文图表需要本机有中文字体；Linux 可安装 Noto Sans CJK，Windows 和 macOS 通常已有可用字体。

`requirements.txt` 包含数据分析、绘图、PDF 预览和空间图表所用的依赖，包括 NumPy、pandas、SciPy、Matplotlib、Seaborn、scikit-learn、Pillow、PyMuPDF 和 GeoPandas 等。第一次完整安装可能需要一些时间。

### 只给一个项目安装

也可以在目标项目目录执行：

```bash
git clone https://github.com/yjz211/vivid-figures-skill.git .claude/skills/vivid-figures-skill
```

然后把上面的虚拟环境和依赖安装命令中的路径改为该项目里的 Skill 路径。个人级和项目级选择一种即可。

## 3. 让 AI 使用正确的 Python

重新打开 Claude Code，在放有数据的项目里输入：

```text
使用 vivid-figures-skill 绘图。
Python 请使用这个 Skill 安装目录下的 .venv 环境。
先检查环境，然后读取我的数据文件。
```

这样可以避免“依赖装好了，AI 却调用另一个 Python”的问题。你也可以提供完整解释器路径。

如果没有识别到 Skill，确认安装文件夹内直接有 `SKILL.md`，而不是多套了一层同名文件夹。支持斜杠调用时可输入 `/vivid-figures-skill`。

## 4. 按要画的图安装可选工具

| 要画什么 | 额外需要什么 | 备注 |
|---|---|---|
| 流程图、技术路线图、可编辑框图 | draw.io Desktop | 导出 Draw.io 图件时使用 |
| 带公式的精确几何图、TikZ 技术图 | TeX Live 或 MiKTeX，含 XeLaTeX 及中文支持 | 终端需能运行 `xelatex` |
| HTML 图和网页截图 | Chrome 或 Chromium | 未找到时可指定 `CHROME_PATH` 或 `PUPPETEER_EXECUTABLE_PATH` |
| Mermaid 图 | Node.js 与 Mermaid CLI | 安装命令见下方 |
| PDF 转图片的备用方式 | Poppler | 已有 PyMuPDF 时通常不需要 |
| AI 生成的科学场景插图 | 助手提供的图像生成工具，或已配置的图像生成 MCP | 本 Skill 不附送图像生成服务；普通数据图不依赖它 |

Mermaid CLI 安装：

```bash
npm install -g @mermaid-js/mermaid-cli
```

draw.io 路径无法自动找到时，可设置 `DRAWIO_PATH`。Mac 上的应用也可能需要手动指定可执行文件路径。

## 检查与常见问题

让 AI 使用上述虚拟环境，在 Skill 安装目录运行：

```bash
python original/resources/scripts/resolve_runtime.py
```

这里的 `python` 指已选定的虚拟环境解释器。脚本会列出 Python 和可选工具路径，**不会验证所有 Python 包是否已安装**；暂时不用的可选工具显示空值无需处理。

| 遇到的问题 | 处理方法 |
|---|---|
| `ModuleNotFoundError` | 确认 AI 的 Python 与安装依赖的 Python 是同一个 |
| 中文显示成方框 | 安装中文字体后重新启动绘图进程 |
| 找不到 `bash` | Windows 安装 Git for Windows，并让 AI 使用 Git Bash 的可执行文件 |
| 找不到 `xelatex`、draw.io 或 Chrome | 安装当前图型需要的工具，或提供实际路径 |
| 没有图像生成能力 | 仅影响 AI 场景插图；数据图可继续用 Python 绘制 |

## 更新到最新版本

进入 Skill 安装目录后执行：

```bash
git pull --ff-only
```

如果更新记录提到依赖有变化，再使用同一个虚拟环境执行 `python -m pip install -r requirements.txt`。重新打开 AI 会话，以加载新的 Skill 指导。
