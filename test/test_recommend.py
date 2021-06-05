import numpy as np
import pandas as pd
import pytest

from src.recommend import swap_to_right, filter_by_cluster, get_mapping_to_df


def test_filter_by_cluster():
    df_in = pd.DataFrame(
        [['ha', 'haha', 2], ['hello', 'world', 2], ['ha', 'docker', 1]],
        columns=['var1', 'var2', 'cluster_label'])
    df_true = pd.DataFrame([['ha', 'haha', 2], ['hello', 'world', 2]],
                           columns=['var1', 'var2', 'cluster_label'])
    df_test = filter_by_cluster(df_in, 2)
    pd.testing.assert_frame_equal(df_true, df_test)


def test_filter_by_cluster_non_df():
    df_in = 'I am not a data frame'

    with pytest.raises(AttributeError):
        filter_by_cluster(df_in, 1)


def test_swap_to_right():
    arr_in = np.array([3, 2, 4, 1, 5])
    arr_test = swap_to_right(arr_in, 1)
    arr_true = np.array([1, 2, 4, 3, 5])
    assert np.allclose(arr_test, arr_true)


def test_swap_to_right_non_np():
    np_in = 'I am not a numpy array'
    with pytest.raises(TypeError):
        swap_to_right(np_in, 1)


def test_get_mapping_to_df():
    df_in = pd.DataFrame([['yes', 10], ['ha', 0], ['hello', 7]],
                         columns=['name', 'random_num'])
    closest_info_in = np.array([[1, 2, 0], [2, 1, 1]])
    k_in = 2

    df_true = pd.DataFrame([['ha', 'hello', 'yes'], ['hello', 'ha', 'ha']],
                           columns=['input', 'rec1', 'rec2'])
    df_test = get_mapping_to_df(df_in, closest_info_in, k_in)
    pd.testing.assert_frame_equal(df_test, df_true)

def test_get_mapping_to_df_non_df():
    df_in = 'ha'
    closest_info_in = np.array([[1, 2, 0], [2, 1, 1]])
    k_in = 2
    with pytest.raises(TypeError):
        get_mapping_to_df(df_in, closest_info_in, k_in)