"""
Module for calculating health study data.
"""

from functools import partial
import pandas as pd
import numpy as np
from scipy.stats import norm, ttest_ind
from scipy import stats
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from statsmodels.stats.outliers_influence import variance_inflation_factor



def summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate mean, median, minimum and maximum for the study measurements.
    Args:
        df: DataFrame containing the health study data.
    Returns:
        DataFrame with one row per measurement (age, weight, height, BMI
        systolic_bp, cholesterol) and the columns 'Mean', 'Median',
        'Min' and 'Max'. rounded to 2 decimals.
    """
    columns = {'age': 'Ålder:',
               'weight': 'Vikt (kg):',
                'height': 'Längd (cm):',
                'bmi': 'BMI:',
                'systolic_bp': 'Systoliskt blodtryck (mmHg):',
                'cholesterol': 'Kolesterol (mmol/L):'}

    return (df[list(columns)].agg(['mean', 'median', 'min', 'max', 'std']).T
                .rename(index=columns,
                columns={'mean': 'Medelvärde',
                         'median': 'Median',
                         'min': 'Min',
                         'max': 'Max',
                         'std': 'Std',},).round(2))


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
    return df.select_dtypes(include='number').corr(method=method).rename(
        index=swedish, columns=swedish)


def disease_share(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the share of disease prevalence.
    Args:
        df: DataFrame containing the health study data.
    Returns:
        DataFrame with the percentage of participants per group, indexed by
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
        DataFrame: containing the health study data (columns 'sex' and 'smoker').
    Returns:
        DataFrame of 2x2, show percentages of smoker status.
      
    """
    smoker_sh = pd.crosstab(df['sex'], df['smoker'], normalize='index') * 100

    smoker_sh = smoker_sh.rename(
    index={0: 'Kvinna', 1: 'Man'},
    columns={0: 'Nej', 1: 'Ja'}).rename_axis(
        index='Kön', columns='Rökare')
    return smoker_sh.round(1)

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

def disease_probability(df: pd.DataFrame, population_size: int = 1000) -> pd.DataFrame:
    """ 
    Calculates the mean for disease, the mean represent the share in %, 
    and other keyvalues for disease probability.
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
    disease_prob = df['disease'].mean()

    rng = np.random.default_rng(seed)
    simulated_population = rng.choice([0, 1], size=population_size, p=[1 - disease_prob, disease_prob])

    simulated_prevalence = simulated_population.mean()
    difference = abs(disease_prob - simulated_prevalence)

    summary = pd.DataFrame({'Värde': [
            f'{simulated_prevalence:.2%}',
            f'{disease_prob:.2%}',
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
        DataFrame Table containing the lower, upper confidence limits and the confidence interval.
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



def welch_ttest_smoking_blood_pressure(df: pd.DataFrame, alternative: str = 'two-sided') -> pd.DataFrame:
    """
    Perform Welch's t-test to compare mean systolic blood pressure
    between smokers and non-smokers.
    Args:
        DataFrame: containing 'smoker' and 'systolic_bp' columns.
            Smoker is coded as 0 (non-smoker) and 1 (smoker).
        alternative: Alternative hypothesis. Options are 'two-sided',
            'greater' or 'less'. Default is 'two-sided'.
    Returns:
        DataFrame: containing the t-statistic and p-value.
    """
    if alternative not in ['two-sided', 'less', 'greater']:
        raise ValueError("alternative must be 'two-sided', 'less' or 'greater'.")

    smokers = df.loc[df['smoker'] == 1, 'systolic_bp'].dropna()

    non_smokers = df.loc[df['smoker'] == 0, 'systolic_bp'].dropna()

    t_stat, p_value = ttest_ind(smokers, non_smokers, equal_var=False, alternative=alternative)

    summary = pd.DataFrame({'Värde': [round(t_stat, 4),f'{p_value:.6g}',alternative]},
                           index=['t-värde:', 'p-värde:', 'Testalternativ:'])

    return summary



def power_simulation(df: pd.DataFrame, n_simulations: int = 5000, alpha: float = 0.05, seed: int = 0) -> pd.DataFrame:
    """
    Simulate statistical power for Welch's t-test at different sample sizes, 
    comparing systolic blood pressure between smokers and non-smokers.
    The observed group means and standard deviations are used
    as assumed population parameters for the simulation.
    Args:
        DataFrame: containing 'smoker' and 'systolic_bp'.
        n_simulations: Number of simulations per sample size.
        alpha: Significance level. Defaults to 0.05.
        seed: Random seed for reproducibility. Defaults to 0.
    Returns:
        DataFrame: containing sample sizes and estimated power.
    """
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1.")

    smokers = df.loc[df['smoker'] == 1, 'systolic_bp'].dropna()

    non_smokers = df.loc[df['smoker'] == 0, 'systolic_bp'].dropna()

    mean_smokers = smokers.mean()
    mean_non_smokers = non_smokers.mean()
    std_smokers = smokers.std(ddof=1)
    std_non_smokers = non_smokers.std(ddof=1)

    sample_sizes = np.array([100, 250, 500, 1000, 2000, 3000, 5000, 7500,
                              10000, 15000, 20000, 25000, 30000, 35000])

    smoker_ratio = len(smokers) / (len(smokers)+len(non_smokers))
    sample_sizes_smokers = np.rint(sample_sizes * smoker_ratio).astype(int)
    sample_sizes_non_smokers = sample_sizes - sample_sizes_smokers
    rng = np.random.default_rng(seed)

# Lambda function since small function I prefer this inside another function over a nested funct
    welch_test = lambda x, y: ttest_ind(x, y, equal_var=False, alternative='two-sided').pvalue

    generate_smokers = partial(rng.normal, loc=mean_smokers, scale=std_smokers)
    generate_non_smokers = partial(rng.normal, loc=mean_non_smokers, scale=std_non_smokers)

    power_result = stats.power(test=welch_test, rvs=(generate_non_smokers, generate_smokers),
        n_observations=(sample_sizes_non_smokers, sample_sizes_smokers),
        significance=alpha,
        n_resamples=n_simulations,
        vectorized=False)

    results = pd.DataFrame({
        'Totalt stickprov': sample_sizes,
        'Rökare': sample_sizes_smokers,
        'Icke-rökare': sample_sizes_non_smokers,
        'Statistisk power (%)': power_result.power * 100})

    return results




def multiple_linear_regression(df: pd.DataFrame) -> dict[str, object]:
    """
    Perform multiple linear regression to investigate factors
    associated with systolic blood pressure.
    Uses scikit-learn for model training and statsmodels for statistical inference.

    Args:
        DataFrame: containing the regression variables.
    Returns:
        dict: Regression results.
    """
    features = ["age", "cholesterol", "bmi", "smoker", "sex"]
    target = "systolic_bp"
    data = df[features + [target]].dropna()

    X = data[features]
    y = data[target]

    model = LinearRegression()
    model.fit(X, y)

    X_ols = sm.add_constant(X)
    ols_result = sm.OLS(y, X_ols).fit()

    confidence_intervals = ols_result.conf_int()

    coefficients = pd.DataFrame({"coefficient": ols_result.params,
                    "std_error": ols_result.bse,
                    "p_value": ols_result.pvalues,
                    "ci_lower": confidence_intervals[0],
                    "ci_upper": confidence_intervals[1],})

    y_pred = pd.Series(model.predict(X), index=y.index)
    residuals = y - y_pred

    return {"coefficients": coefficients,
        "r_squared": model.score(X, y),
        "adjusted_r_squared": ols_result.rsquared_adj,
        "model": model,
        "ols_result": ols_result,
        "X": X,
        "y": y,
        "y_pred": y_pred,
        "residuals": residuals,
        "n_observations": len(data),
        "n_dropped": len(df) - len(data),}


def format_regression_results(results: dict[str, object]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Format multiple linear regression results into Swedish tables.
    Args : 
        dict: Results returned by multiple_linear_regression()
    Returns:
    tuple[pd.DataFrame, pd.DataFrame] Coefficient table and model summary in Swedish.
    """
    variable_names = {"const": "Konstant",
            "age": "Ålder",
            "cholesterol": "Kolesterol",
            "bmi": "BMI",
            "smoker": "Rökning",
            "sex": "Kön",}

    column_names = {"coefficient": "Koefficient",
        "std_error": "Standardfel",
        "p_value": "p-värde",
        "ci_lower": "95 % KI (nedre)",
        "ci_upper": "95 % KI (övre)",}

    coefficient_table = results["coefficients"].copy()

    coefficient_table = coefficient_table.rename(index=variable_names)
    coefficient_table = (coefficient_table
        .rename(columns=column_names)
        .rename_axis("Variabel"))

    coefficient_table = coefficient_table.round({"Koefficient": 3, "Standardfel": 3,
                        "p-värde": 4, "95 % KI (nedre)": 3, "95 % KI (övre)": 3,}) 

    model_summary = pd.DataFrame({"Modellmått": ["R²",
                    "Justerat R²",
                    "Antal observationer",
                    "Bortfallna observationer",],
        "Värde": [round(results["r_squared"], 4),
            round(results["adjusted_r_squared"], 4),
            results["n_observations"],
            results["n_dropped"],],}, dtype=object)

    return coefficient_table, model_summary


def calculate_vif(results: dict[str, object]) -> pd.DataFrame:
    """
    Calculate variance inflation factors for regression predictors.

    Args:
        results: Dictionary returned by multiple_linear_regression().

    Returns:
        DataFrame containing VIF values for each predictor.
    """
    X = results["X"]

    vif_data = pd.DataFrame({"variable": X.columns,
        "VIF": [variance_inflation_factor(X.values, i)for i in range(X.shape[1])]})

    vif_data = vif_data.replace({"variable": {"age": "Ålder",
                            "cholesterol": "Kolesterol",
                            "bmi": "BMI",
                            "smoker": "Rökning",
                            "sex": "Kön"}}).rename(columns={"variable": "Variabel"})

    return vif_data


def logistic_regression(df: pd.DataFrame,) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    """
    Perform logistic regression to investigate factors associatedwith disease.
    Args:
        DataFrame: containing disease and explanatory variables.
    Returns:
        Tuple containing regression results, actual disease values and predicted probabilities.
    """
    predictors = ['age', 'smoker', 'cholesterol', 'systolic_bp','bmi','sex']

    X = df[predictors]
    y = df['disease']

    X = sm.add_constant(X)
    model = sm.Logit(y, X).fit(disp=False)

    odds_ratios = np.exp(model.params)
    conf_int = np.exp(model.conf_int())

    results = pd.DataFrame({'Oddskvot': odds_ratios,
        '95 % KI nedre': conf_int[0],
        '95 % KI övre': conf_int[1],
        'p-värde': model.pvalues})

    results = results.drop('const')

    results = results.rename(index={'age': 'Ålder',
                            'smoker': 'Rökning',
                            'cholesterol': 'Kolesterol',
                            'systolic_bp': 'Systoliskt blodtryck',
                            'bmi': 'BMI',
                            'sex': 'Kön'})

    y_true = y.copy()
    y_prob = model.predict(X)

    return results, y_true, y_prob
