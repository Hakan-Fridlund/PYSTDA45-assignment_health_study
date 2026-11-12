"""
Module providing the HealthAnalyzer wrapper class for health study analysis.

Integrates data loading, preprocessing, statistical calculations,
and visualizations through modular components as a wrapper class.
"""
from pathlib import Path
import data

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / 'data' / 'health_study_dataset.csv'



class HealthAnalyzer():
    """
    Interface class for health study data analysis.

    Coordinates data loading, preprocessing, statistical analysis,
    and visualization by integrating the project's modular components.
    """

    def __init__(self, path: str = DATA_PATH, palette: str = 'okabe_ito') -> None:
        self.df = data.load_data(path)
        self.palette = palette
        self.df = data.clean_data(self.df)
        self.df = data.transform_data(self.df)
        data.validate_data(self.df)




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
