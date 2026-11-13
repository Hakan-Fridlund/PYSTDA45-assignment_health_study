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

    swedish = {'age': 'Ålder',
            'sex': 'Kön',
            'weight': 'Vikt',
            'height': 'Längd',
            'systolic_bp': 'Blodtryck',
            'cholesterol': 'Kolesterol',
            'smoker': 'Rökare',
            'disease': 'Sjukdom',
            'bmi': 'BMI'}
    return df.select_dtypes(include='number').corr(method=method).rename(index=swedish, columns=swedish)


def disease_share(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the share of disease prevalence.
    Args:
        df: DataFrame containing the health study data.
    Returns:
        Series with the percentage of participants per group, indexed by
        'Ingen sjukdom' and 'Sjukdom'. Values are rounded.
    """
    return ((df['disease'].map({0: 'Ingen sjukdom', 1: 'Sjukdom'})
         .value_counts(normalize=True)* 100)
        .round(2)
        .rename('Andel (%)')
        .rename_axis('Sjukdomsstatus')
        .to_frame())

def age_by_sex(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate descriptive statistics for age, grouped by sex.
    Args:
        df: DataFrame containing the health study data (columns 'sex' and 'age').
    Returns:
        DataFrame with one row per sex and the columns 'Medelvärde',
        'Median', 'Standardavvikelse' and 'Antal'. 
        Values are rounded to one decimal.
    """
    return (df.groupby('sex')['age']
        .agg(['mean', 'median', 'std', 'count'])
        .rename(columns={'mean': 'Medelvärde',
            'median': 'Median',
            'std': 'Standardavvikelse',
            'count': 'Antal',},
            index={0: 'Kvinna', 1: 'Man'})
        .rename_axis('Kön')
        .round(1))

def smoker_share(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate descriptive smoker share grouped by sex.
    Args:
        df: DataFrame containing the health study data (columns 'sex' and 'smoker').
    Returns:
        DataFrame of 2x2 rows, show percentages of smoker status.
      
    """
    smoker_share = pd.crosstab(df['sex'], df['smoker'], normalize='index') * 100

    smoker_share = smoker_share.rename(
    index={0: 'Kvinna', 1: 'Man'},
    columns={0: 'Nej', 1: 'Ja'}).rename_axis(
        index='Kön', columns='Rökare')
    return smoker_share.round(1)

def chol_bp_corr(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the correlation between cholesterol and systolic blood pressure
    separately for women and men.
    Args:
        df: DataFrame containing 'sex', 'systolic_bp' and 'cholesterol'.
    Returns:
        DataFrame containing the correlation coefficient for each sex.
    """
    corr = (
        df.groupby('sex')[['cholesterol', 'systolic_bp']]
        .corr()
        .iloc[[1, 3], 0]
        .droplevel(1)
        .rename(index={0: 'Kvinna', 1: 'Man'})
        .rename('Korrelation (r)'))
    
    corr.index.name = 'Kön'

    return corr.to_frame().round(3)

def smoker_disease_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the percentage distribution of disease status
    among smokers and non-smokers.
    Args:
        DataFrame: containing the 'smoker' and 'disease' columns
        Both variables are binary encoded as 0 and 1.
    Returns:
        DataFrame with Percentage distribution of disease status by smoking status.
        Rows represent smoking status and columns represent disease status.
    """
    smoker_risk = pd.crosstab(df['smoker'], df['disease'], normalize='index') * 100

    smoker_risk = smoker_risk.reindex(index=[0, 1], columns=[0, 1], fill_value=0)

    smoker_risk = smoker_risk.rename(
        index={0: 'Icke-rökare', 1: 'Rökare'},
        columns={0: 'Ingen sjukdom', 1: 'Sjukdom'}).rename_axis(
            index='Rökstatus', columns='Sjukdomsstatus')

    return smoker_risk.round(1)

def disease_probability(df: pd.Dataframe, population_size: int = 1000) -> pd.DataFrame:
    """ 
    Calculates the mean disease, since encoded as 0 and 1,
    the mean represent the share in % and other keyvalues for disease probability.
    Args:
        DataFrame: containing 'disease' column.
    Returns:
        Dataframe with keyvalues for disease probability.
    """
    probability = df['disease'].mean()
    no_disease_probability = 1 - probability
    expected_cases = probability * population_size

    summary = pd.DataFrame({
        'Värde': [
            f'{probability:.2%}',
            f'{probability:.4f}',
            f'{no_disease_probability:.4f}',
            population_size,
            round(expected_cases)
        ]
    }, index=[
        'Observerad sjukdomsförekomst:',
        'Sannolikhet för sjukdom:',
        'Sannolikhet för ingen sjukdom:',
        'Simulerad population (antal individer):',
        'Förväntat antal individer med sjukdom:'])

    return summary