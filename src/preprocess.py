import logging
from typing import List

import pandas as pd
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


def scale_df(df: pd.DataFrame, features: List) -> pd.DataFrame:
    """Generate a standardized dataframe with selected features

    Args:
        df (pd.DataFrame): the raw input data
        features (List): selected features that will be used to train the model

    Returns:
        df_scale (pd.DataFrame): a standardized dataframe with selected features
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Provided argument df need to be pd.Dataframe, but now it is {type(df)}")

    std_scale = StandardScaler()
    df_scale = pd.DataFrame(std_scale.fit_transform(df[features]), columns=features)
    logger.info(f'The shape of the standardized data is {df_scale.shape}')
    return df_scale


def save_df(df: pd.DataFrame, output_path: str) -> None:
    """Save the dataframe to a specific path"""
    df.to_csv(output_path, index=False)
    logger.info('The standardized data is saved to %s', output_path)
