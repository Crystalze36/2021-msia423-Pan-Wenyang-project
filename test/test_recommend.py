import numpy as np

from src.recommend import swap_to_right


def test_swap_to_right():
    arr_in = np.array([3, 2, 4, 1, 5])
    arr_test = swap_to_right(arr_in, 1)
    arr_true = np.array([1, 2, 4, 3, 5])
    assert np.allclose(arr_test, arr_true)


def test_filter_by_cluster():
    pass