from numbers import Number
from typing import Tuple

import pandas as pd


def normalize(x: Number, x_min: Number, x_max: Number) -> Number:
    x -= x_min
    x /= x_max - x_min
    return x


def normalize_field(df: pd.DataFrame, field: str) -> pd.DataFrame:
    min_x, max_x = min(df[field]), max(df[field])
    df.loc[:, field] = df[field].transform(lambda x: normalize(x, min_x, max_x))
    return df


def normalize_field_and_yield_min_max(
    df: pd.DataFrame, field: str
) -> Tuple[pd.DataFrame, Number, Number]:
    df = df.copy()
    min_x, max_x = min(df[field]), max(df[field])
    df.loc[:, field] = df[field].transform(lambda x: normalize(x, min_x, max_x))
    return df, min_x, max_x

def min_max_scale(_df: pd.DataFrame, scaled_fields: pd.Series):
    scaled_df = _df.copy()

    for feature in scaled_fields:
        feature_min = scaled_df[feature].min()
        feature_max = scaled_df[feature].max()
        feature_delta = feature_max - feature_min

        scaled_df[feature] = (
            scaled_df[feature].subtract(feature_min).divide(feature_delta)
        )

    return scaled_df