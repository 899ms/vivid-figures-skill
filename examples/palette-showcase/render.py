"""Render the README's five color variants of recipe:advanced.ridgeline.

Input: synthetic_samples.csv (demonstration only). All variants share the
same data, density estimates, axes, fonts and layout. Native width 6 inches;
display at 6 inches gives scale 1, so 8pt labels remain 8pt.
The original template's overlapping ridges, outlines and median markers are
retained. Fill uses a clipped continuous gradient. KDE medians use the same
normalization as their curves. No original Skill resource is modified.
"""
from pathlib import Path
import argparse
import csv
import json
import os
import re
import sys
import tempfile

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.font_manager import fontManager
from matplotlib.path import Path as MplPath
from matplotlib.patches import PathPatch
import numpy as np
from scipy.stats import gaussian_kde

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'original/resources/assets/shared-scripts'))
import plot_utils as pu
from plot_utils import setup_style

OPTIONS = [('coral', '珊瑚青绿'), ('ocean', '海洋暖橙'), ('iris', '鸢尾杏桃'),
           ('forest', '森林日光'), ('berry', '浆果冰蓝')]


def render(output):
    output.mkdir(parents=True, exist_ok=True)
    with (Path(__file__).parent / 'synthetic_samples.csv').open(encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    names = sorted({row['group'] for row in rows})
    data = [np.array([float(row['score']) for row in rows if row['group'] == name])
            for name in names]
    x_grid = np.linspace(min(d.min() for d in data)-5, max(d.max() for d in data)+5, 700)
    stats = []
    for d in data:
        kde = gaussian_kde(d, bw_method=.3)
        raw = kde(x_grid)
        peak = raw.max()
        median = np.median(d)
        stats.append((raw/peak*.92, median, float(kde(median)[0]/peak*.92)))
    palette_doc = (REPO / 'color-selection.md').read_text(encoding='utf-8')
    fonts = {f.name for f in fontManager.ttflist}
    cjk = next((f for f in ['Microsoft YaHei', 'Noto Sans CJK SC', 'PingFang SC', 'SimHei']
                if f in fonts), 'DejaVu Sans')
    initial_cwd = Path.cwd()
    audit = []
    with tempfile.TemporaryDirectory(prefix='vivid-showcase-') as work:
        try:
            os.chdir(work)
            for slug, label in OPTIONS:
                line = next(line for line in palette_doc.splitlines() if line.startswith('| '+label))
                colors = re.findall(r'#[0-9A-Fa-f]{6}', line)
                assert len(colors) == 7
                Path('CLAUDE.md').write_text(
                    '<!-- MH_DATA_FIG_PALETTE=custom -->\n'
                    '<!-- MH_DATA_FIG_COLORS='+','.join(colors)+' -->\n'
                    '<!-- MH_DATA_FIG_STYLE=clean_open -->\n', encoding='utf-8')
                setup_style()
                assert pu.PALETTE == colors
                # Fixed typography makes palette comparison independent of folder seeds.
                plt.rcParams.update({'font.sans-serif':[cjk,'DejaVu Sans'],
                                     'font.size':8, 'axes.linewidth':.65})
                fig, ax = plt.subplots(figsize=(6, 3.9))
                fig.subplots_adjust(left=.125, right=.89, bottom=.17, top=.83)
                n = len(names)
                for i in range(n-1, -1, -1):
                    density, median, med_height = stats[i]
                    baseline = i*.64
                    color = pu.PALETTE[i]
                    z = n-i
                    # Template layering: pale fill below a full-color outline.
                    ax.fill_between(x_grid, baseline, baseline+density,
                                    color=pu._lighten(color,.5), alpha=.85, zorder=z)
                    verts = np.column_stack((np.r_[x_grid,x_grid[::-1]],
                                             np.r_[baseline+density,np.full(len(x_grid),baseline)]))
                    clip = PathPatch(MplPath(verts, closed=True), transform=ax.transData)
                    cmap = LinearSegmentedColormap.from_list(slug+str(i),
                            [pu._lighten(color,.91),pu._lighten(color,.06)])
                    im = ax.imshow(np.linspace(0,1,256).reshape(-1,1),
                            extent=(x_grid[0],x_grid[-1],baseline,baseline+.92),
                            origin='lower', aspect='auto', cmap=cmap, zorder=z+.1)
                    im.set_clip_path(clip)
                    ax.plot(x_grid, baseline+density, color=color, lw=1.3, zorder=z+.5)
                    ax.plot([median,median],[baseline,baseline+med_height],
                            color=color, lw=1.0, ls=(0,(2.5,2)), zorder=z+.8)
                    ax.scatter([median],[baseline+med_height],s=13,color=color,
                               edgecolor='white',lw=.5,zorder=n+2)
                    ax.text(1.025, baseline+.17, f'{median:.1f}',
                            transform=ax.get_yaxis_transform(), va='center',
                            color=color, fontsize=8, fontweight='bold', clip_on=False)
                ax.set_yticks(np.arange(n)*.64+.17, names, fontsize=8)
                for tick, color in zip(ax.get_yticklabels(),pu.PALETTE):
                    tick.set_color(color)
                    tick.set_fontweight('bold')
                ax.tick_params(axis='y',length=0,pad=8)
                ax.tick_params(axis='x',length=3,labelsize=8)
                ax.set_xlim(x_grid[0],x_grid[-1])
                ax.set_ylim(-.08,(n-1)*.64+1.04)
                ax.set_xticks([20,40,60,80,100])
                ax.set_xlabel('综合得分（分）',fontsize=8.5,labelpad=7)
                ax.spines[['left','right','top']].set_visible(False)
                ax.spines['bottom'].set_color(pu.COLORS['ref_line'])
                ax.grid(False)
                # These are gallery captions outside the data axes, not paper titles.
                fig.text(.07,.945,'VIVID FIGURES',fontsize=9,fontweight='bold',color=pu.COLORS['text'])
                fig.text(.07,.892,label+'  /  渐变山脊图',fontsize=13,fontweight='bold',color=pu.COLORS['text'])
                ax.text(1.025,1.025,'中位数',transform=ax.transAxes,fontsize=7,color=pu.COLORS['text'])
                for i,color in enumerate(pu.PALETTE):
                    fig.add_artist(plt.Rectangle((.71+i*.031,.94),.024,.018,
                                   transform=fig.transFigure,facecolor=color,edgecolor='none'))
                fig.text(.07,.035,'模拟数据 · 每组 240 个样本 · 曲线等高归一化 · 虚线标记中位数',
                         fontsize=6.6,color=pu.COLORS['text'])
                fig.savefig(output/(slug+'.png'),dpi=300,facecolor='white')
                plt.close(fig)
                audit.append({'palette':slug,'colors':colors,'samples_per_group':[len(d) for d in data],
                              'medians':[round(float(s[1]),4) for s in stats]})
                print('Rendered',slug)
        finally:
            os.chdir(initial_cwd)
    (output/'render-info.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=REPO/'docs/images')
    args=parser.parse_args()
    render(args.output.resolve())
