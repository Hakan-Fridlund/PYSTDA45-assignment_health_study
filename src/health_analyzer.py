"""
Module providing the HealthAnalyzer wrapper class for health study analysis.

Integrates data loading, preprocessing, statistical calculations,
and visualizations through modular components as a wrapper class.
"""

from . import data, metrics, viz


class HealthAnalyzer():
     """
    Interface class for health study data analysis.

    Coordinates data loading, preprocessing, statistical analysis,
    and visualization by integrating the project's modular components.
    """

    def __init__(self, path: str = '../data/health_study_dataset.csv', palette: str = 'okabe_ito') -> None:
        self.df = data.load_data(path)
        self.palette = palette

