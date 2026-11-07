"""
Visualization settings for the Health Study project.
Defines a shared color palette and global plotting parameters
to ensure consistent visualizations across the project.

No custom plotting functions are defined in Part 1.
"""
import seaborn as sns
import matplotlib.pyplot as plt


# custom order for my okabe_ito palette (for white background) optimized order for greyscale
okabe_ito = ['#0072B2','#E69F00','#009E73','#56B4E9','#D55E00','#CC79A7','#F0E442','#000000']


sns.set_theme(
    style='whitegrid',
    palette=okabe_ito,
    font='DejaVu Sans'
)
# SEABORN - For these diagram types saturation needs to be set to 1 (since standard=0.75)
# sns.barplot() /sns.countplot() / sns.boxplot() / sns.violinplot()	/ sns.boxenplot()

plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=okabe_ito)

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11

plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 11

plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

plt.rcParams['legend.fontsize'] = 10
plt.rcParams['legend.title_fontsize'] = 11
plt.rcParams['legend.frameon'] = False
plt.rcParams['legend.loc'] = 'best'
plt.rcParams['legend.borderaxespad'] = 0.8
# removes the top and right spines (frame) from axes
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

plt.rcParams['lines.linewidth'] = 1.8
plt.rcParams['lines.markersize'] = 6

plt.rcParams['xtick.major.width'] = 0.8
plt.rcParams['ytick.major.width'] = 0.8
plt.rcParams['xtick.major.size'] = 4
plt.rcParams['ytick.major.size'] = 4

plt.rcParams['axes.grid'] = True
plt.rcParams['axes.grid.axis'] = 'y'
plt.rcParams['axes.axisbelow'] = True

plt.rcParams['grid.color'] = '#D9D9D9'
plt.rcParams['grid.alpha'] = 0.6
plt.rcParams['grid.linewidth'] = 0.7
plt.rcParams['grid.linestyle'] = '-'

plt.rcParams['figure.figsize'] = (9, 5.5)
plt.rcParams['figure.dpi'] = 120

plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['savefig.facecolor'] = 'white'