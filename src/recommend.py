import logging
from typing import List

import numpy as np
import pandas as pd
import joblib
from sklearn.metrics import pairwise_distances

logger = logging.getLogger(__name__)


def append_cluster_and_name(df_raw: pd.DataFrame, scale_path: str,
                            model_path: str) -> pd.DataFrame:
    """Add Pokemon name and assigned cluster to the preprocessed dataframe

    Args:
        df_raw (pd.DataFrame): the raw input dataframe
        scale_path (str): the path that stores the preprocess dataframe
        model_path (str): the path that saves the fitted model

    Returns:
        df_prepared (pd.DataFrame): preproessed dataframe with name and cluster attached
    """
    df_scale = pd.read_csv(scale_path)
    mod = joblib.load(model_path)

    logger.debug(f'The shpae of df_scale is {df_scale.shape}')
    logger.debug(f'The shpae of df_raw is {df_raw.shape}')

    df_prepared = df_scale.copy(deep=True)
    df_prepared = df_prepared.assign(cluster_label=mod.predict(df_scale),
                                     name=df_raw['name'])

    return df_prepared


def filter_by_cluster(df: pd.DataFrame, cluster_idx: int) -> pd.DataFrame:
    """Return a filtered dataframe only with observations associated with a specific cluster"""
    df_one_cluster = df.query('cluster_label == @cluster_idx').reset_index(
        drop=True)
    logger.debug('Cluster %d has %d observations', cluster_idx,
                 df_one_cluster.shape[0])
    return df_one_cluster


def swap_to_right(input_arr: np.ndarray, i: int) -> np.ndarray:
    """"Swap the first element that equals to i with the element index 0"""
    if not isinstance(input_arr, np.ndarray):
        raise TypeError(f'input_arr should be np.ndarray but now it is {type(input_arr)}')
    right_idx = np.where(input_arr == i)[0].item()
    input_arr[[0, right_idx]] = input_arr[[right_idx, 0]]
    return input_arr


def closest_k_in_cluster(df_one_cluster: pd.DataFrame,
                         features: List,
                         k: int = 10) -> np.ndarray:
    """Find the k closest elements for each observation in the dataframe

    Args:
        df_one_cluster (pd.DataFrame): a filtered dataframe with one specific cluster
        features (List): features that are used to calculate pairwise distances 
        k (int, optional): how many closest observations to find. Defaults to 10.

    Returns:
        closest_k(np.ndarray): 1st element in each row is the target 
            and the rest of k elements are the index of closest elements
    """
    dist_mtx = pairwise_distances(df_one_cluster[features])
    closest_k = np.argsort(dist_mtx)[:, :(k + 1)]
    # Get rid of the case where two pokemons have exact same feature and thus mess up the ordering
    for i in range(closest_k.shape[0]):
        if closest_k[i][0] != i:
            closest_k[i] = swap_to_right(closest_k[i], i)
    return closest_k


def get_mapping_to_df(df_one_cluster: pd.DataFrame,
                      closest_info: np.ndarray,
                      k: int = 10) -> pd.DataFrame:
    """Map each element (an integer) in the closest info array to its corresponding Pokemon name
       and return the mapping result as a pandas Dataframe

    Args:
        df_one_cluster (pd.DataFrame): a filtered dataframe with one specific cluster
        closest_info (np.ndarray): the array that describes the closest element for each row 
        k (int, optional): how many recommendations to make. Defaults to 10.

    Returns:
        pd.DataFrame: records the k recommendations for each Pokemon
    """
    int2str = df_one_cluster['name'].to_dict()

    # Adapted from: https://stackoverflow.com/questions/16992713/translate-every-element-in-numpy-array-according-to-key
    map_closest_info = np.vectorize(int2str.get)(closest_info)

    df_info = pd.DataFrame(map_closest_info,
                           columns=['input'] +
                                   [f'rec{i}' for i in range(1, (k + 1))])
    return df_info


def get_url(name: str) -> str:
    """Generate a url for a given Pokemon str"""
    return f'https://pokemondb.net/pokedex/{name}'


def to_long(df_result: pd.DataFrame) -> pd.DataFrame:
    """Change the dataframe from wide to long format and sort by input and the_rank column"""
    df_long = df_result.melt(id_vars=['input'],
                             var_name='the_rank',
                             value_name='recommendation')
    df_long['the_rank'] = df_long.the_rank.str.replace('rec', '').astype(int)
    df_long = df_long.sort_values(['input', 'the_rank'], ignore_index=True)
    logger.debug(f'The shape of the long format is {df_long.shape}')
    return df_long


def merge_display(df_long: pd.DataFrame, df_raw: pd.DataFrame,
                  display_features: List) -> pd.DataFrame:
    """Merge display features into the recommendation dataframe
       from the raw data

    Args:
        df_long (pd.DataFrame): the recommendation information
        df_raw (pd.DataFrame): the raw input with display features for each Pokemon
        display_features (List): the features that will be added into the recommendation table

    Returns:
        df_final (pd.DataFrame): recommendation information with additional features attached
    """
    df_final = pd.merge(df_long,
                        df_raw[display_features],
                        left_on='recommendation',
                        right_on='name',
                        how='inner')
    logger.debug(f'The shape after merging is {df_final.shape}')
    df_final = df_final.drop('name', axis=1) \
        .sort_values(['input', 'the_rank'], ignore_index=True)
    return df_final


def format_clean(df: pd.DataFrame) -> pd.DataFrame:
    """Add a column with url for each Pokemon and clean the format for some columns"""
    df['learn_more'] = df['recommendation'].apply(get_url)
    df.abilities = df.abilities.str.replace('[^a-zA-Z0-9, -]', '', regex=True)
    df.input = df.input.str.lower()
    df.type2 = df.type2.fillna('None')
    return df


def generate_recommendation(df: pd.DataFrame, df_raw: pd.DataFrame,
                            num_clusters: int, features: List, k: int,
                            display_features: List, output_path: str) -> None:
    """Orchestration function to generate and store recommendations

    Args:
        df (pd.DataFrame): preproessed dataframe with Pokemon name and cluster attached
        df_raw (pd.DataFrame): the raw input dataframe
        num_clusters (int): total number of clusters
        features (List): features that are used to calculate pairwise distances 
        k (int): how many recommendations to make
        display_features (List): the features that will be added into the recommendation table
        output_path (str): the path to store the recommendation result
    """
    result = []
    for i in range(0, num_clusters):
        df_one_clus = filter_by_cluster(df, i)
        closet_info = closest_k_in_cluster(df_one_clus, features, k)
        df_info = get_mapping_to_df(df_one_clus, closet_info, k)
        result.append(df_info)
    df_result = pd.concat(result, axis=0)
    df_result_long = to_long(df_result)
    df_result_merge = merge_display(df_result_long, df_raw, display_features)
    df_final = format_clean(df_result_merge)
    df_final.to_csv(output_path, index=False)
    logger.info('The recommendation result is saved to %s', output_path)
