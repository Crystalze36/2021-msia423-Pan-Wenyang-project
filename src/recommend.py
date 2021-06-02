import logging
from typing import List

import numpy as np
import pandas as pd
import joblib
from sklearn.metrics import pairwise_distances

logger = logging.getLogger(__name__)


def append_cluster_and_name(raw_path: str, scale_path: str,
                            model_path: str) -> pd.DataFrame:
    df_raw = pd.read_csv(raw_path)
    df_scale = pd.read_csv(scale_path)
    mod = joblib.load(model_path)

    logger.debug(f'The shpae of df_scale is {df_scale.shape}')
    logger.debug(f'The shpae of df_raw is {df_raw.shape}')

    df_prepared = df_scale.copy(deep=True)
    df_prepared = df_prepared.assign(cluster_label=mod.predict(df_scale),
                                     name=df_raw['name'])
    
    return df_prepared


def filter_by_cluster(df: pd.DataFrame, cluster_idx: int) -> pd.DataFrame:
    df_one_cluster = df.query('cluster_label == @cluster_idx').reset_index(
        drop=True)
    logger.debug('Cluster %d has %d observations', cluster_idx,
                 df_one_cluster.shape[0])
    return df_one_cluster


def swap_to_right(input_arr: np.ndarray, i: int) -> np.ndarray:
    right_idx = np.where(input_arr == i)[0].item()
    input_arr[[0, right_idx]] = input_arr[[right_idx, 0]]
    return input_arr


def closest_k_in_cluster(df_one_cluster: pd.DataFrame,
                         features: List,
                         k: int = 11) -> np.ndarray:
    dist_mtx = pairwise_distances(df_one_cluster[features])
    closest_k = np.argsort(dist_mtx)[:, :11]
    # Get rid of the case where two pokemons have exact same feature and thus mess up the ordering
    for i in range(closest_k.shape[0]):
        if closest_k[i][0] != i:
            closest_k[i] = swap_to_right(closest_k[i], i)
    return closest_k


def get_mapping_to_df(df_one_cluster: pd.DataFrame,
                      closest_info: np.ndarray) -> pd.DataFrame:
    int2str = df_one_cluster['name'].to_dict()

    # Adapted from: https://stackoverflow.com/questions/16992713/translate-every-element-in-numpy-array-according-to-key
    map_cloest_info = np.vectorize(int2str.get)(closest_info)

    df_info = pd.DataFrame(map_cloest_info,
                           columns=['input'] +
                           [f'rec{i}' for i in range(1, 11)])
    return df_info


def generate_recommendation(df: pd.DataFrame, num_clusters: int,
                            features: List, k: int, output_path: str):
    result = []
    for i in range(0, num_clusters):
        df_one_clus = filter_by_cluster(df, i)
        cloest_info = closest_k_in_cluster(df_one_clus, features, k)
        df_info = get_mapping_to_df(df_one_clus, cloest_info)
        result.append(df_info)
    df_result = pd.concat(result, axis=0)
    df_result.to_csv(output_path, index=False)
    logger.info('The recommendation result is saved to %s', output_path)
