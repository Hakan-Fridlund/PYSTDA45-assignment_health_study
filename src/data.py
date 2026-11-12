"""
Module for loading, cleaning, and transforming health study data.
"""
import pandas as pd

def load_data(path: str ='../data/health_study_dataset.csv') -> pd.DataFrame:
    """ Load a csv file into a pandas dataset"""
    return pd.read_csv(path)

def clean_data():
    pass

def transform_data():
    pass

def encode_variables():
    pass


