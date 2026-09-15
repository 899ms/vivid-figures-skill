import numpy as np, matplotlib.pyplot as plt
import seaborn as sns
from _utils.plot_utils import setup_style, save_fig, PALETTE, COLORS
setup_style()
np.random.seed(42)

regions = ['北京', '上海', '广东', '浙江', '江苏', '四川', '湖北', '山东']
years = [str(y) for y in range(2015, 2024)]
data = np.random.uniform(3, 12, (len(regions), len(years)))
data = np.round(data, 1)

fig, ax = plt.subplots(figsize=(9, 5))
sns.heatmap(data, annot=True, fmt='.1f', cmap='YlOrRd',
            xticklabels=years, yticklabels=regions,
            linewidths=0.3, linecolor='white',
            cbar_kws={'label': 'GDP增长率 (%)', 'shrink': 0.8}, ax=ax)
ax.set_xlabel('年份', fontsize=11); ax.set_ylabel('地区', fontsize=11)
ax.set_yticklabels(regions, rotation=0, fontsize=9)
fig.tight_layout()
save_fig(fig, 'figures/fig_spatiotemporal.pdf')
