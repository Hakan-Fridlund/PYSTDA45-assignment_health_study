"""
Module providing the HealthAnalyzer wrapper class for health study analysis.

Integrates data loading, preprocessing, statistical calculations,
and visualizations through modular components as a wrapper class.
"""
from pathlib import Path
import pandas as pd
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
            df: DataFrame containing the health study data.
            method: Correlation method: 'pearson', 'spearman' or 'kendall'.
        Returns:
            Square DataFrame with correlation coefficients between all
            numeric columns.
        """

        return metrics.correlation_matrix(self.df, method=method)

    def disease_share(self) -> pd.Series:
        """
        Calculate the share of disease prevalence.
        Args:
            df: DataFrame containing the health study data.
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


    def plot_dodged_distribution(self):
        """Plot the age distribution by sex (see plots)."""
        return viz.plot_dodged_distribution(self.df, viz.PALETTES[self.palette])

if __name__ == "__main__":

    analyzer = HealthAnalyzer(path=DATA_PATH)

    print("\n--- DataFrame head ---")
    print(analyzer.df.head())

    print("\n--- Descriptive statistics ---")
    print(analyzer.df.describe())

    analyzer.df.info()
    print('\nMissing Values:\n', analyzer.df.isna().sum())
    print('\nduplicates:', analyzer.df.duplicated().sum())

    print(analyzer.df['sex'].unique())
    print(analyzer.df['smoker'].unique())
