import logging
from typing import List

import pandas as pd
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)

def scale_df(df: pd.DataFrame, features: List) -> pd.DataFrame:
    std_scale = StandardScaler()
    df_scale =  pd.DataFrame(std_scale.fit_transform(df[features]), columns=features)
    logger.info(f'The shape of the standardized data is {df_scale.shape}')
    return df_scale

def save_df(df: pd.DataFrame, output_path: str) -> pd.DataFrame:
    df.to_csv(output_path, index=False)
    logger.info('The standardized data is saved to %s', output_path)


