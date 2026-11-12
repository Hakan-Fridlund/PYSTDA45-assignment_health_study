"""
Module for calculating health study data.
"""

import pandas as pd


def summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate mean, median, minimum and maximum for the study measurements.
    Args:
        df: DataFrame containing the health study data.
    Returns:
        DataFrame with one row per measurement (age, weight, height,
        systolic_bp, cholesterol) and the columns 'Mean', 'Median',
        'Min' and 'Max'. rounded to 2 decimals.
    """
    columns = {'age': 'Ålder', 
               'weight': 'Vikt (kg)',
                'height': 'Längd (cm)',
                'systolic_bp': 'Systoliskt blodtryck (mmHg)',
                'cholesterol': 'Kolesterol (mmol/L)'}

    return (df[list(columns)].agg(['mean', 'median', 'min', 'max']).T
                .rename(index=columns,
                columns={'mean': 'Medelvärde',
                         'median': 'Median',
                         'min': 'Min',
                         'max': 'Max'}).round(2))
                    

def correlation_matrix(df: pd.DataFrame, method: str = 'pearson') -> pd.DataFrame:
    """
    Calculate the correlation matrix for the numeric columns.
    Args:
        df: DataFrame containing the health study data.
        method: Correlation method: 'pearson', 'spearman' or 'kendall'.
    Returns:
        Square DataFrame with correlation coefficients between all
        numeric columns.
    """
    return df.select_dtypes(include='number').corr(method=method)