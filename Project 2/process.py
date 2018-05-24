import pandas as pd
import os

from config import crime_types_original, variables, base_columns


def get_data():
    ''''''
    data_dir = os.path.relpath('data/')
    year_df = pd.read_csv(data_dir + '/Year_df.csv')

    df = year_df[base_columns + variables + crime_types_original]

    # Rename columns
    crime_types = [' '.join(cr.split('_')).title() for cr in
                   crime_types_original]

    df = df.rename(mapper=dict(zip(crime_types_original, crime_types)),
                   axis='columns')

    return df


def get_state(dfs):

    try:
        state_abbrev = dfs.State_Abbrev.unique()
    except KeyError:
        state_abbrev = 'USA'

    return dfs, state_abbrev


def get_state_dropdown(dfs, state_checks):

    return dfs[dfs.State_Abbrev.isin(state_checks)]


def drop_rows_with_zeros(dfs):

    # Omit all zeros and NANs
    dfs = dfs.loc[~(dfs == 0).any(axis=1)]

    return dfs.dropna()
