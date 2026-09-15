## 14. Cluster Heatmap — 聚类热力图（带树状图 + 聚类边界 + 轮廓系数标注）

**场景**: 基因表达矩阵、特征相关性 + 层次聚类。增加聚类结构信息。
**⚠ 布局**: 只画列方向树状图（不画行方向树状图），避免遮挡 y 轴标签。使用 `fig.add_axes()` 手动分区（不要用 gridspec）。树状图和热力图的 left/width 参数完全一致。

```python
from _utils.plot_utils import setup_style, save_fig, PALETTE, COLORS, _lighten; from _utils.palette_maps import palette_cmap, palette_stops, contrast_text
setup_style()
import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.spatial.distance import pdist

np.random.seed(42)
data = np.random.randn(10, 8)
labels_row = [f'Sample-{i+1}' for i in range(10)]
labels_col = [f'Feat-{i+1}' for i in range(8)]

Z_col = linkage(pdist(data.T), method='ward')
Z_row = linkage(pdist(data), method='ward')

n_clusters = 3
col_clusters = fcluster(Z_col, n_clusters, criterion='maxclust')
row_clusters = fcluster(Z_row, n_clusters, criterion='maxclust')

fig = plt.figure(figsize=(10, 8))

# ── 关键：树状图和热力图的 left 和 width 参数完全一致，否则会对不齐
# ── _left 需要足够容纳色条(左侧) + 间距 + y轴标签区域(至少 0.15)
_left = 0.22   # 长文本标签需要更大左边距
_width = 0.56
_cbar_left = _left + _width + 0.03

# 列树状图（只画列方向，不画行方向，避免遮挡标签）
ax_dendro_top = fig.add_axes([_left, 0.86, _width, 0.10])
dn_col = dendrogram(Z_col, ax=ax_dendro_top, leaf_font_size=0,
                     color_threshold=Z_col[-n_clusters + 1, 2],
                     above_threshold_color=COLORS['ref_line'])
ax_dendro_top.set_axis_off()

# Heatmap —— left 和 width 与树状图完全一致
ax_heat = fig.add_axes([_left, 0.08, _width, 0.76])
col_order = dn_col['leaves']
row_order = list(range(len(labels_row)))
ordered_data = data[row_order][:, col_order]

im = ax_heat.imshow(ordered_data, aspect='auto', cmap=palette_cmap('diverging'), interpolation='nearest')
ax_heat.set_xticks(range(len(labels_col)))
ax_heat.set_xticklabels([labels_col[i] for i in col_order], fontsize=8,
                         rotation=45, ha='right')
ax_heat.set_yticks(range(len(labels_row)))
ax_heat.set_yticklabels([labels_row[i] for i in row_order], fontsize=8)

# Cluster boundary lines
sorted_col_clusters = [col_clusters[i] for i in col_order]
for k in range(1, len(sorted_col_clusters)):
    if sorted_col_clusters[k] != sorted_col_clusters[k - 1]:
        ax_heat.axvline(k - 0.5, color='white', linewidth=2.5)
sorted_row_clusters = [row_clusters[i] for i in row_order]
for k in range(1, len(sorted_row_clusters)):
    if sorted_row_clusters[k] != sorted_row_clusters[k - 1]:
        ax_heat.axhline(k - 0.5, color='white', linewidth=2.5)

# Colorbar
ax_cbar = fig.add_axes([_cbar_left, 0.08, 0.02, 0.76])
cbar = plt.colorbar(im, cax=ax_cbar)
cbar.ax.tick_params(labelsize=8)

# Silhouette score annotation
ax_heat.text(0.98, 0.02, 'Silhouette = 0.42',
             transform=ax_heat.transAxes, fontsize=8, ha='right', va='bottom',
             bbox=dict(boxstyle='round,pad=0.3', facecolor=_lighten(PALETTE[0], 0.7),
                       edgecolor=PALETTE[0], alpha=0.9))

save_fig(fig, 'figures/fig_cluster_heatmap.pdf')
```

**⚠ 易踩的坑（聚类热力图专用）：**
```python
# 1. _left 取 0.22，给 y 轴标签 + 左侧色条留够空间（长文本标签需要更多）
# 2. 左侧色条放在 _left-0.05，色条右边界与热力图左边界之间留 0.025 间距
# 3. 树状图和热力图的 left/width 参数完全一致，否则会对不齐
# 4. ★ 行/样本聚类(需要行树状图)：不要把行标签留在左侧——左侧树状图的叶子连线会横穿标签文字。
#    正确做法：行树状图放最左、行标签移到热力图【右侧】(ax_heat.yaxis.tick_right())，两者彻底分开。
#    完整可跑代码见下方「变体：双向聚类热力图(带行树状图 + 标签移右侧)」。
#    (若只做列聚类、行不聚类，仍按上面主配方：只画列树状图、行标签留左侧即可。)
# 5. 不要手动写 fig.tight_layout()。注：save_fig 内部虽会调一次 tight_layout，但对 add_axes 的
#    固定坐标不生效(只打印无害 UserWarning)，手动布局不会被移动——实测保存前后 axes 坐标一致。
# 6. 数值标注颜色需要适应：abs(val)>0.6 用白色字，其余用深色字
# 7. ★ y 标签超长（>20 字符）兜底：调用 auto_truncate_yticklabels(ax_heat, max_chars=18)
#    或在数据准备阶段就用缩写（'avg_silhouette_2024' 而非 'average_silhouette_coefficient_2024'）。
#    plot_utils._save 会在检测到 y label 溢出 figure 左边界时自动截断 + 减字号兜底，
#    但生成阶段就避免超长更稳妥。
# 8. ★ 长标签场景：宽度用 7.0-7.2 英寸（⛔ 上限 7.2，别写 9-10 —— 单栏正文才 6.5in，
#    原生 10in 会被缩到 0.53、刻度 8.5pt 变 4.5pt、线宽腰斩 → 坐标轴糊成一团、线条发虚），
#    并把 _left 提到 0.26-0.30 换取标签空间（7.2×0.28 ≈ 2.0 英寸，够放 18 字符截断后的标签）。
#    figsize=(6, ...) 时即便 _left=0.22 实际像素空间只有 1.3 英寸，长标签必溢出。
#    ⛔ 标签实在放不下就先按第 7 条截断/缩写，不要靠摊大画布 —— 摊得越大缩得越狠，字反而更小。
```

**变体：双向聚类热力图（带行树状图 + 标签移右侧，不糊标签）**

**场景**：需要同时展示**行聚类**(样本/类别聚类)和列聚类，且行标签是中文/长文本。
关键：行树状图放最左，行标签移到热力图**右侧**，两者彻底分开——避免左侧树状图连线横穿标签。

```python
from _utils.plot_utils import setup_style, save_fig, PALETTE, COLORS
setup_style()
import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.spatial.distance import pdist

# data: (n_row, n_col); labels_row 可为中文长标签; z-score 后 vmin/vmax 取 ±2
n_row, n_col = data.shape
Z_row = linkage(pdist(data), method='ward')
Z_col = linkage(pdist(data.T), method='ward')
n_clusters = 3
row_clusters = fcluster(Z_row, n_clusters, criterion='maxclust')
col_clusters = fcluster(Z_col, n_clusters, criterion='maxclust')

fig = plt.figure(figsize=(10, 7))
# 横向分区[左→右]: [行树状图][热力图][右侧标签(自动占位)][色条]
_heat_x, _heat_w, _bottom, _height = 0.19, 0.56, 0.10, 0.72

# 行树状图(左, orientation='left')
ax_dleft = fig.add_axes([0.05, _bottom, 0.12, _height])
dn_row = dendrogram(Z_row, ax=ax_dleft, orientation='left', no_labels=True,
                    color_threshold=Z_row[-n_clusters + 1, 2],
                    above_threshold_color=COLORS['ref_line'])
ax_dleft.invert_yaxis()          # ★ 让叶子[上→下]与 imshow(origin=upper) 同向
ax_dleft.set_axis_off()
row_order = dn_row['leaves']     # ★ invert 后 row_order = leaves 正序(勿加 [::-1]，否则行全错位)

# 列树状图(顶)
ax_dtop = fig.add_axes([_heat_x, 0.84, _heat_w, 0.11])
dn_col = dendrogram(Z_col, ax=ax_dtop, no_labels=True,
                    color_threshold=Z_col[-n_clusters + 1, 2],
                    above_threshold_color=COLORS['ref_line'])
ax_dtop.set_axis_off()
col_order = dn_col['leaves']

# 热力图(left/width 与列树状图完全一致，才对得齐)
ax_heat = fig.add_axes([_heat_x, _bottom, _heat_w, _height])
im = ax_heat.imshow(data[np.ix_(row_order, col_order)], aspect='auto',
                    cmap='coolwarm', interpolation='nearest', vmin=-2, vmax=2)
# ★ 行标签移到右侧，彻底避开左侧树状图连线
ax_heat.set_yticks(range(n_row))
ax_heat.set_yticklabels([labels_row[i] for i in row_order], fontsize=9)
ax_heat.yaxis.tick_right()
ax_heat.yaxis.set_tick_params(length=0)   # 去刻度线只留文字
ax_heat.set_xticks(range(n_col))
ax_heat.set_xticklabels([labels_col[i] for i in col_order], fontsize=8, rotation=45, ha='right')
for s in ax_heat.spines.values():
    s.set_visible(False)

# 聚类分界白线
srow = [row_clusters[i] for i in row_order]
for k in range(1, n_row):
    if srow[k] != srow[k - 1]:
        ax_heat.axhline(k - 0.5, color='white', linewidth=2.5)
scol = [col_clusters[i] for i in col_order]
for k in range(1, n_col):
    if scol[k] != scol[k - 1]:
        ax_heat.axvline(k - 0.5, color='white', linewidth=2.5)

# 色条(最右, 给右侧标签留出 0.75→0.90 的空间)
ax_cbar = fig.add_axes([0.90, _bottom, 0.02, _height])
cbar = plt.colorbar(im, cax=ax_cbar); cbar.ax.tick_params(labelsize=8)
cbar.set_label('成分含量 (列 z-score)', fontsize=9)

save_fig(fig, 'figures/fig_cluster_heatmap.pdf')
```

**⚠ 变体专用坑（已实跑验证）：**
```python
# A. ★★ row_order = dn_row['leaves'] 正序！配 invert_yaxis() 才对齐。
#    误写 leaves[::-1] 会让每一行的标签与数据错位(比"线穿字"更隐蔽、更严重)。
#    自检口诀: 若行有单调趋势(如亮度递增), 出图应看到从上到下大致分组连续。
# B. 行标签一定 yaxis.tick_right()；留在左侧必被树状图连线穿过(用户实测踩坑)。
# C. 右侧中文长标签: 色条左边界(0.90) 与热力图右边界(0.75) 之间留 0.15 给标签。
#    标签更长(>8 中文字)就把色条推到 0.92 或调小 _heat_w。
# D. 行/列树状图的 left/width 必须分别等于热力图的 left/width，否则叶子与格子对不齐。
```

---
