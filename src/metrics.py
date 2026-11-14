"""
Module for calculating health study data.
"""

import pandas as pd
import numpy as np
from scipy.stats import norm


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

def simulate_disease_prevalence(df: pd.DataFrame, population_size: int = 1000, seed: int = 0) -> pd.DataFrame:
    """
    Simulate disease prevalence in a population based on observed prevalence.
    ARgs:
        DataFrame: containing the binary 'disease' column.
        population_size : int, default=1000
            Number of individuals in the simulated population.
        seed : int, default=0
            Random seed for reproducibility.
    Returns:
        DataFrame Table comparing simulated and observed disease prevalence,
        including the absolute difference.
    """
    disease_probability = df['disease'].mean()

    rng = np.random.default_rng(seed)
    simulated_population = rng.choice([0, 1], size=population_size, p=[1 - disease_probability, disease_probability])

    simulated_prevalence = simulated_population.mean()
    difference = abs(disease_probability - simulated_prevalence)

    summary = pd.DataFrame({'Värde': [
            f'{simulated_prevalence:.2%}',
            f'{disease_probability:.2%}',
            f'{difference:.2%}']}, 
            index=[
        'Simulerad sjukdomsförekomst:',
        'Observerad sjukdomsförekomst:',
        'Skillnad:'])

    return summary

def blood_pressure_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate mean and sample standard deviation of systolic blood pressure.
    Args:
        DataFrame containing the 'systolic_bp' column.
    Returns:
            Summary table with mean and standard deviation in mmHg.
    """
    systolic_mean = df['systolic_bp'].mean()
    systolic_std = df['systolic_bp'].std(ddof=1)

    summary = pd.DataFrame({'Värde': [round(systolic_mean, 2), round(systolic_std, 2)]}
                           , index=['Medelvärde för observerat systoliskt blodtryck (mmHg):', 
                                'Standardavvikelse för observerat systoliskt blodtryck (mmHg):'])

    return summary

def blood_pressure_confidence_interval(df: pd.DataFrame, confidence_level: float = 0.95) -> pd.DataFrame:
    """
    Calculate a confidence interval for the mean systolic blood pressure
    using the normal approximation.
    Args:
        DataFrame: containing the 'systolic_bp' column.
        confidence_level: float, default=0.95 for the interval.
    Returns:
        DataFrame Table containing the lower and upper confidence limits and the confidence interval.
    """
    systolic_mean = df['systolic_bp'].mean()
    systolic_std = df['systolic_bp'].std(ddof=1)
    n = df['systolic_bp'].count()

    if not 0 < confidence_level < 1:
        raise ValueError("confidence_level must be between 0 and 1.")
    if n < 2:
        raise ValueError("At least two valid observations are required.")

    z = norm.ppf(1 - (1 - confidence_level) / 2)

    standard_error = systolic_std / np.sqrt(n)
    margin_of_error = z * standard_error

    ci_lower = systolic_mean - margin_of_error
    ci_upper = systolic_mean + margin_of_error

    summary = pd.DataFrame({'Värde': [
            round(ci_lower, 2),
            round(ci_upper, 2),]},
            index=['Nedre gräns konfidensintervall (mmHg):',
                'Övre gräns konfidensintervall (mmHg):'])

    return summary

def blood_pressure_bootstrap_ci(df: pd.DataFrame, confidence_level: float = 0.95, n_bootstrap: int = 10_000, seed: int = 0) -> pd.DataFrame:
    """
    Calculate a bootstrap confidence interval for mean systolic blood pressure.
    Args:
        DataFrame: containing the 'systolic_bp' column.
        confidence_level: Confidence level, default=0.95.
        n_bootstrap: Number of bootstrap resamples, default=10,000.
        seed: Random seed for reproducibility, default=0.
    Returns:
        DataFrame containing the lower and upper confidence limits.
    """
    data = df['systolic_bp'].dropna()
    n = len(data)

    if not 0 < confidence_level < 1:
        raise ValueError("confidence_level must be between 0 and 1.")
    if n_bootstrap < 1:
        raise ValueError("n_bootstrap must be at least 1.")
    if n < 2:
        raise ValueError("At least two valid observations are required.")

    rng = np.random.default_rng(seed)
    bootstrap_means = []

    for _ in range(n_bootstrap):
        sample = rng.choice(data, size=n, replace=True)
        bootstrap_means.append(sample.mean())

    alpha = 1 - confidence_level
    ci_lower = np.percentile(bootstrap_means, alpha / 2 * 100)
    ci_upper = np.percentile(bootstrap_means, (1 - alpha / 2) * 100)

    summary = pd.DataFrame({'Värde': [round(ci_lower, 2), round(ci_upper, 2)]}, 
                           index=['Nedre gräns bootstrap-konfidensintervall (mmHg):',
                            'Övre gräns bootstrap-konfidensintervall (mmHg):'])

    return summary


def smoking_blood_pressure_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate descriptive statistics for systolic blood pressure
    grouped by smoking status.
    Args:
        DataFrame: containing 'smoker' and 'systolic_bp' columns.
            Smoker is coded as 0 (non-smoker) and 1 (smoker).
    Returns:
        DataFrame: containing count, mean and standard deviation
            of systolic blood pressure by smoking status.
    """
    smoking_stats = (df.groupby('smoker', observed=True)['systolic_bp']
                     .agg(['count', 'mean', 'std']).round(2))

    smoking_stats = smoking_stats.rename(
        index={0: 'Icke-rökare', 1: 'Rökare'},
        columns={'count': 'Antal',
            'mean': 'Medelvärde (mmHg)',
            'std': 'Standardavvikelse (mmHg)'}).rename_axis('Rökstatus')

    return smoking_stats