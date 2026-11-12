"""
Module for loading, cleaning, and transforming health study data.
Missing values are preserved during cleaning to avoid unintended
data loss. Their handling is delegated to individual analysis
methods and functions.
"""
import warnings
import pandas as pd


def load_data(path: str ='../data/health_study_dataset.csv') -> pd.DataFrame:
    """ Load a csv file into a pandas dataset"""
    return pd.read_csv(path)


def clean_data(df:pd.DataFrame  ) -> pd.DataFrame:
    """
    Clean the input DataFrame by handling missing values,
    duplicates, and data types.
    Args:
        df: DataFrame containing the raw health study data.
    Returns:
        A cleaned DataFrame.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")
    df = df.copy()
    df = df.drop_duplicates()
    return df


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """ 
    Transform the dataframe by setting the ID as index, 
    encoding categorical variables to binary and calculating bmi"""

    if 'id' not in df.columns:
        raise ValueError("Required column 'id' is missing.")

    df = df.copy()

    if not df['id'].is_unique:
        warnings.warn(
        "Duplicate ID detected (with different values). All rows will be retained as is.",
        UserWarning)

    df = df.set_index('id')
    df['bmi'] = df['weight'] / (df['height'] / 100) ** 2

    df['sex'] = df['sex'].replace({'F': 0, 'M': 1})
    df['smoker'] = df['smoker'].replace({'No': 0, 'Yes': 1})
    df['sex'] = df['sex'].astype('int64')
    df['smoker'] = df['smoker'].astype('int64')

    return df



def validate_data(df: pd.DataFrame) -> None:
    """
    Validate the transformed health study DataFrame.
    Raises AssertionError for invalid data. 
    Issues warnings for values outside the defined plausibility ranges.
    """

    assert 'age' in df.columns, 'Missing column: age.'
    assert 'sex' in df.columns, 'Missing column: sex.'
    assert 'height' in df.columns, 'Missing column: height.'
    assert 'weight' in df.columns , 'Missing column: weight.'
    assert 'systolic_bp' in df.columns, 'Missing column: systolic_bp.'
    assert 'cholesterol' in df.columns, 'Missing column: cholesterol.'
    assert 'smoker' in df.columns, 'Missing column: smoker.'
    assert 'disease' in df.columns, 'Missing column: disease.'
    assert 'bmi' in df.columns, 'Missing column: bmi.'

    assert df['sex'].dropna().isin([0, 1]).all(), 'Invalid sex value (must be 1 or 0)'
    assert df['smoker'].dropna().isin([0, 1]).all(), 'Invalid smoker value (must be 1 or 0)'
    assert df['disease'].dropna().isin([0, 1]).all(), 'Invalid disease value (must be 1 or 0)'

    assert (df['age'].dropna() >= 0).all(), 'Invalid age, cannot be negative'
    assert (df['height'].dropna() > 0).all(), 'Invalid height, must be greater than 0'
    assert (df['weight'].dropna() > 0).all(), 'Invalid weight, must be greater than 0'
    assert (df['systolic_bp'].dropna() > 0).all(), 'Invalid systolic_bp, must be greater than 0'
    assert (df['cholesterol'].dropna() > 0).all(), 'Invalid cholesterol, must be greater than 0'

    if ((df['age'] > 120)).any():
        warnings.warn("Age values above 120 detected.")

    if ((df['bmi'] < 12) | (df['bmi'] > 50)).any():
        warnings.warn("BMI values outside the range 12-50 detected.")

    if ((df['systolic_bp'] < 50) | (df['systolic_bp'] > 250)).any():
        warnings.warn("Systolic blood pressure values outside the range 50-250 detected.")

    if ((df['cholesterol'] < 1.0) | (df['cholesterol'] > 10.0)).any():
        warnings.warn("Cholesterol values outside the range 1.0-10.0 detected.")
