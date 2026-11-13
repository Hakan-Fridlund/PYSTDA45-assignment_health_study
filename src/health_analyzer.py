"""
Module providing the HealthAnalyzer wrapper class for health study analysis.

Integrates data loading, preprocessing, statistical calculations,
and visualizations through modular components as a wrapper class.
"""
from pathlib import Path
import pandas as pd
import matplotlib as plt
import seaborn as sns
from . import data_utils, metrics, viz


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / 'data' / 'health_study_dataset.csv'



class HealthAnalyzer():
    """
    Interface class for health study data analysis.

    Coordinates data loading, preprocessing, statistical analysis,
    and visualization by integrating the project's modular components.
    """

    def __init__(self, path: str = DATA_PATH, palette: str = 'okabe_ito') -> None:
        self.df = data_utils.load_data(path)
        self.palette = palette
        self.df = data_utils.clean_data(self.df)
        self.df = data_utils.transform_data(self.df)
        data_utils.validate_data(self.df)

    def summary_statistics(self) -> pd.DataFrame:
        """
        Calculate mean, median, minimum and maximum for the study measurements.
        Returns:
            DataFrame with one row per measurement and the columns
            'Mean', 'Median', 'Min' and 'Max'. Values are rounded to 2 decimals.
        """
        return metrics.summary_statistics(self.df)

    def correlation_matrix(self, method: str = 'pearson') -> pd.DataFrame:
        """
        Calculate the correlation matrix for the numeric columns.
        Args:
            method: Correlation method: 'pearson', 'spearman' or 'kendall'.
        Returns:
            Square DataFrame with correlation coefficients between all
            numeric columns.
        """
        return metrics.correlation_matrix(self.df, method=method)

    def disease_share(self) -> pd.Series:
        """
        Calculate the share of disease prevalence.
        Returns:
            Series with the percentage of participants per group, indexed by
            'Ingen sjukdom' and 'Sjukdom'. Values are rounded.
        """
        return metrics.disease_share(self.df)

    def age_by_sex(self) -> pd.DataFrame:
        """
        Calculate descriptive statistics for age, grouped by sex.
        Returns:
            DataFrame with one row per sex. Values are rounded to one decimal.
        """
        return metrics.age_by_sex(self.df)

    def smoker_share(self) -> pd.DataFrame:
        """
        Calculate descriptive smoker share grouped by sex.
        Returns:
            DataFrame of 2x2 rows, show percentages of smoker status.
        """
        return metrics.smoker_share(self.df)

    def chol_bp_corr(self) -> pd.DataFrame:
        """
        Calculate correlation of systolic_bp and cholesterol.
        Returns:
            DataFrame of systolic_bp and cholesterol corr, per sex
        """
        return metrics.chol_bp_corr(self.df)

    def smoker_disease_distribution(self) -> pd.DataFrame:
        """Calculate disease distribution among smokers and non-smokers."""
        return metrics.smoker_disease_distribution(self.df)

    def disease_probability(self, population_size: int = 1000) -> pd.Dataframe:
        """Calculate share of disease in population (default to: 1000)"""
        return metrics.disease_probability(self.df, population_size)

    def simulate_disease_prevalence(self, population_size: int = 1000, seed: int = 0) -> pd.DataFrame:
        """Simulate disease prevalence and compare it with observed prevalence."""
        return metrics.simulate_disease_prevalence(self.df, population_size, seed)

    def blood_pressure_summary(self) -> pd.DataFrame:
        """Return summary statistics for systolic blood pressure."""
        return metrics.blood_pressure_summary(self.df)

    def blood_pressure_confidence_interval(self, confidence_level: float = 0.95) -> pd.DataFrame:
        """Return confidence interval for mean systolic blood pressure."""
        return metrics.blood_pressure_confidence_interval(self.df, confidence_level)

    def blood_pressure_bootstrap_ci(self, confidence_level: float = 0.95, n_bootstrap: int = 10_000, seed: int = 0) -> pd.DataFrame:
        """Return bootstrap confidence interval for mean systolic blood pressure."""
        return metrics.blood_pressure_bootstrap_ci(self.df, confidence_level, n_bootstrap, seed)



    def plot_dodged_distribution(self) -> plt.Axes:
        """Plot the age distribution by sex with kde (see viz)."""
        return viz.plot_dodged_distribution(self.df, viz.PALETTES[self.palette])

    def plot_bp_hist(self) -> plt.Axes:
        """Plot the systolic bloodpressure histogram plot with kde (see viz)."""
        return viz.plot_bp_hist(self.df, viz.PALETTES[self.palette])

    def plot_smokers_by_sex(self) -> plt.Axes:
        """Plot smokers divided by sex as countplot (see viz)."""
        return viz.plot_smokers_by_sex(self.df, viz.PALETTES[self.palette])

    def plot_chol_bp_corr(self) -> sns.FacetGrid:
        """Plot the scatterplot with correlation between cholesterol and systolic bloodpressure,
        by sex with separate regressionlines."""
        return viz.plot_chol_bp_corr(self.df, viz.PALETTES[self.palette])

    def plot_bp_by_disease(self) -> plt.Axes:
        """Plot systolic blood pressure distribution by disease status, combined box/swarmplot"""
        return viz.plot_bp_by_disease(self.df, viz.PALETTES[self.palette])

    def plot_chol_by_disease(self) -> plt.Axes:
        """Plot cholesterol distribution by disease status, combined box/swarmplot"""
        return viz.plot_chol_by_disease(self.df, viz.PALETTES[self.palette])

    def plot_age_by_disease(self) -> plt.Axes:
        """Plot age distribution by disease status, combined box/swarmplot"""
        return viz.plot_age_by_disease(self.df, viz.PALETTES[self.palette])

    def plot_smoking_by_disease(self) -> plt.Axes:
        """Plot smoking proportions by disease status, stacked boxplot"""
        return viz.plot_smoking_by_disease(self.df, viz.PALETTES[self.palette])
