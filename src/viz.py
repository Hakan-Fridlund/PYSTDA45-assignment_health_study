"""
Visualization settings for the Health Study project.
Defines shared color palettes and global plotting parameters
to ensure consistent visualizations across the project.

No custom plotting functions are defined in Part 1.
"""
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


# custom order for my okabe_ito palette (for white background) optimized order for greyscale
okabe_ito = ['#0072B2','#E69F00','#009E73','#56B4E9','#D55E00','#CC79A7','#F0E442','#000000']

# another order of okabe_ito I optimized for tritanopi, 
# best order overall, but not my favourite first 2 color pair
okabe_ito_tritanopi = ['#009E73','#E69F00','#0072B2','#CC79A7'
                       ,'#56B4E9','#D55E00','#F0E442','#000000']

# custom ordered glasbey for 20 colors. optimized for white background, greyscale and color blindness
glasbey_20 = ['#CC0036','#0994D4','#28540C','#6660FC','#600C84','#A20C60',
    '#905038','#049084','#D86C3C','#0000EA','#9678C0','#593500','#F6548A',
    '#08008A','#978700','#006A9C','#843C84','#D08404','#781E36','#0A8640']

PALETTES: dict[str, list[str]] = {'okabe_ito': okabe_ito,
    'okabe_ito_tritanopi': okabe_ito_tritanopi, 
    'glasbey_20': glasbey_20,}

# To set histogram figsizes, recommended on histplots
HIST_FIGSIZE = (6.5, 5.5)

sns.set_theme(
    style='whitegrid',
    palette=okabe_ito,
    font='DejaVu Sans'
)
# SEABORN - For these diagram types saturation needs to be manually set to 1 (since standard=0.75)
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


def plot_dodged_distribution(df: pd.DataFrame, palette: list[str]) -> plt.Axes:
    """
    Plot the age distribution by sex as side-by-side histograms with a KDE.
    Args:
        df: DataFrame containing the columns 'age' and 'sex' (coded 0/1).
        palette: Colours for the two groups (first colour for women,
            second for men).

    Returns:
        The Axes containing the histogram.
    """
    data = df.assign(Kön=df['sex'].map({0: 'Kvinna', 1: 'Man'}))
    sex_labels = {0: 'Kvinna', 1: 'Man'}

    _, ax = plt.subplots(figsize=(HIST_FIGSIZE))
    sns.histplot(data=data, x='age', hue='Kön', multiple='dodge', shrink=1.0,
                kde=True, palette=palette[:2], ax=ax, alpha = 0.8, bins = 15)

    # old legend needed to build new combined legend
    handles = ax.get_legend().legend_handles

    mean_age = df['age'].mean()
    mean_line = ax.axvline(mean_age, color='black', linestyle='--',
                           linewidth=3, label=f'Total (medel: {mean_age:.1f} år)')

    ax.legend(handles + [mean_line], [*sex_labels.values(), mean_line.get_label()],
              title='Kön')

    ax.set_title('Åldersfördelning efter kön')
    ax.set_xlabel('Ålder')
    ax.set_ylabel('Antal')
    plt.tight_layout()
    plt.show()
    return ax

def plot_bp_hist(df: pd.DataFrame, palette: list[str]) -> plt.Axes:
    """
    Plot the systolic bloodpressure distribution as histogram with a KDE.
    Args:
        df: DataFrame containing the column 'systolic_bp'
        palette: used for selecting the first color in palette list
    Returns:
        The Axes containing the histogram.
    """

    _, ax = plt.subplots(figsize=(HIST_FIGSIZE))
    sns.histplot(data=df, x='systolic_bp', kde=True, color=palette[0], ax=ax, alpha = 0.8, bins = 15)

    ax.set_title('Fördelning av systoliskt blodtryck')
    ax.set_xlabel('Systoliskt blodtryck (mmHg)')
    ax.set_ylabel('Antal')
    plt.tight_layout()
    plt.show()
    return ax


def plot_smokers_by_sex(df: pd.DataFrame, palette: list[str]) -> plt.Axes:
    """
    Plot the number of smokers by sex countplot.
        Args:
            df: DataFrame containing the column 'smoker' and 'sex'
            palette: Colours for the two groups.
        Returns:
            The Axes containing the histogram.
    """

    _, ax = plt.subplots()
    sns.countplot(data=df, x='smoker', hue='sex', palette=palette[:2], saturation=1, edgecolor='black')

    ax.set_title('Antal rökare fördelat på kön')
    ax.set_xlabel('Rökare')
    ax.set_ylabel('Antal')

    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Nej', 'Ja'])

    ax.legend_.set_title('Sex')
    ax.legend_.texts[0].set_text('Kvinna')
    ax.legend_.texts[1].set_text('Man')
    plt.tight_layout()
    plt.show()
    return ax

def plot_chol_bp_corr(df: pd.DataFrame, palette: list[str]) -> sns.FacetGrid:
    """
    Plot the relationship between cholesterol and systolic blood pressure,
    with separate regression lines for each sex.
    Args:
        df: DataFrame containing cholesterol, systolic_bp and sex columns.
        Sex is encoded as 0 (Female) and 1 (Male).
        palette : Color palette containing at least two colors.
    Returns:
        Seaborn FacetGrid containing the scatter plot and regression lines.
    """

    g = sns.lmplot(data=df, x='cholesterol', y='systolic_bp', hue='sex', palette=palette[:2],
        markers=['o', 'h'], height=6, aspect=1.5, scatter_kws={'alpha': 0.6}, ci=95, n_boot=5000, seed=42)

    g.set_axis_labels('Kolesterol (mmol/L)', 'Systoliskt blodtryck (mmHg)')
    g.figure.suptitle('Kolesterol i förhållande till systoliskt blodtryck', y=1.02)

    g.legend.set_title('Kön')
    g.legend.texts[0].set_text('Kvinna')
    g.legend.texts[1].set_text('Man')

    g.ax.grid(alpha=0.3)
    g.figure.tight_layout()
    plt.show()

    return g

def plot_bp_by_disease(df: pd.DataFrame, palette: list[str]) -> plt.Axes:
    """
    Plot the distribution of systolic blood pressure by disease status
    using a boxplot and overlaid swarmplot.
    The number of observations in each disease group is included in the x-axis labels.
    Args:
        df: DataFrame containing 'disease' and 'systolic_bp' columns.
        Disease status is encoded as 0 (No disease) and 1 (Disease).
        palette : Color palette containing at least two colors.
    Returns: Matplotlib Axes containing the boxplot and swarmplot.
    """
    disease_counts = df['disease'].value_counts()
    labels = {0: f'Ingen sjukdom (antal: {disease_counts.get(0, 0)})',
                1: f'Sjukdom (antal: {disease_counts.get(1, 0)})'}

    fig, ax = plt.subplots()
    sns.boxplot(data=df, x='disease', y='systolic_bp', hue='disease', palette=palette[:2],
                legend=False, order=[0, 1], width=0.6, saturation=1, ax=ax)

    sns.swarmplot(data=df, x='disease', y='systolic_bp', color='black', alpha=0.3, size=4,
        order=[0, 1], ax=ax)

    ax.set_title('Systoliskt blodtrycksfördelning efter sjukdomsstatus')
    ax.set_xlabel('Sjukdomsstatus')
    ax.set_ylabel('Systoliskt blodtryck (mmHg)')
    ax.set_xticks([0, 1], labels=[labels[0], labels[1]])

    fig.tight_layout()
    plt.show()
    return ax

def plot_chol_by_disease(df: pd.DataFrame, palette: list[str]) -> plt.Axes:
    """
    Plot the distribution of cholesterol by disease status
    using a boxplot and overlaid swarmplot.
    The number of observations in each disease group is included in the x-axis labels.
    Args:
        df: DataFrame containing 'disease' and 'cholesterol' columns.
        Disease status is encoded as 0 (No disease) and 1 (Disease).
        palette : Color palette containing at least two colors.
    Returns: Matplotlib Axes containing the boxplot and swarmplot.
    """
    disease_counts = df['disease'].value_counts()
    labels = {0: f'Ingen sjukdom (antal: {disease_counts.get(0, 0)})',
                1: f'Sjukdom (antal: {disease_counts.get(1, 0)})'}

    fig, ax = plt.subplots()
    sns.boxplot(data=df, x='disease', y='cholesterol', hue='disease', palette=palette[:2], 
                legend=False, order=[0, 1], width=0.6, saturation=1, ax=ax)

    sns.swarmplot(data=df, x='disease', y='cholesterol', color='black', alpha=0.3, size=4,
        order=[0, 1], ax=ax)

    ax.set_title('Fördelning av kolesterol efter sjukdomsstatus')
    ax.set_xlabel('Sjukdomsstatus')
    ax.set_ylabel('Kolesterol (mmol/L)')
    ax.set_xticks([0, 1], labels=[labels[0], labels[1]])

    fig.tight_layout()
    plt.show()
    return ax


def plot_age_by_disease(df: pd.DataFrame, palette: list[str]) -> plt.Axes:
    """
    Plot the distribution of age by disease status
    using a boxplot and overlaid swarmplot.
    The number of observations in each disease group is included in the x-axis labels.
    Args:
        df: DataFrame containing 'disease' and 'age' columns.
        Disease status is encoded as 0 (No disease) and 1 (Disease).
        palette : Color palette containing at least two colors.
    Returns: Matplotlib Axes containing the boxplot and swarmplot.
    """
    disease_counts = df['disease'].value_counts()
    labels = {0: f'Ingen sjukdom (antal: {disease_counts.get(0, 0)})',
                1: f'Sjukdom (antal: {disease_counts.get(1, 0)})'}

    fig, ax = plt.subplots()
    sns.boxplot(data=df, x='disease', y='age', hue='disease', palette=palette[:2], 
                legend=False, order=[0, 1], width=0.6, saturation=1, ax=ax)

    sns.swarmplot(data=df, x='disease', y='age', color='black', alpha=0.3, size=4,
        order=[0, 1], ax=ax)

    ax.set_title('Åldersfördelning efter sjukdomsstatus')
    ax.set_xlabel('Sjukdomsstatus')
    ax.set_ylabel('Ålder (år)')
    ax.set_xticks([0, 1], labels=[labels[0], labels[1]])

    fig.tight_layout()
    plt.show()
    return ax


def plot_smoking_by_disease(df: pd.DataFrame, palette: Sequence[str]) -> Axes:
    """
    Plot the proportion of smokers and non-smokers by disease status
    using a stacked bar chart.
    The number of observations in each disease group is included in the x-axis labels.
    ARgs: 
        DataFrame: containing 'disease' and 'smoker' columns.
        (Disease and smoking status are encoded as 0 and 1.)
        palette: Color palette containing at least two colors.
    Returns:
        Matplotlib Axes containing the stacked bar chart.
    """
    smoker_proportion = (pd.crosstab(df['disease'], df['smoker'], normalize='index')
        .reindex(index=[0, 1], columns=[0, 1], fill_value=0) * 100)

    disease_counts = df['disease'].value_counts()

    labels = [f'Ingen sjukdom (n={disease_counts.get(0, 0)})', f'Sjukdom (n={disease_counts.get(1, 0)})']
    smoker_proportion.index = labels

    ax = smoker_proportion.plot(kind='bar', stacked=True, color=[palette[0], palette[1]], edgecolor='black', alpha=1)

    ax.set_title('Rökstatus efter sjukdomsförekomst')
    ax.set_xlabel('Sjukdomsstatus')
    ax.set_ylabel('Andel deltagare (%)')
    ax.set_ylim(0, 110)
    ax.legend(['Icke-rökare', 'Rökare'], title='Rökstatus')

    ax.tick_params(axis='x', rotation=0)
    ax.figure.tight_layout()
    plt.show()

    return ax