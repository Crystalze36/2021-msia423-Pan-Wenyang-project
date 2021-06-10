import pytest
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from src.model import get_a_mod_list_and_dict

features = ['sp_attack', 'sp_defense', 'hp', 'attack', 'defense', 'speed']

df_in = pd.DataFrame([[-0.75181913, -0.45913113, -0.804014, -0.90028389, -0.63304444,
                       -1.59200589],
                      [-0.06417968, 0.16695677, 0.25389916, -0.18664422, -0.14608718,
                       -0.45485883],
                      [1.86121078, 1.83652452, 1.66445004, 1.89937943, 1.9408725,
                       1.06133726],
                      [-0.98103229, -1.08521903, -1.22717927, -0.73559782, -0.8417404,
                       -0.0758098]], columns=features)


def test_get_a_mod_list_and_dict():
    cluster_range = [2, 3]
    seed = 10

    mod_dict_test, mod_list_test = get_a_mod_list_and_dict(df_in, cluster_range, seed)
    mod_2 = KMeans(n_clusters=2, random_state=seed).fit(df_in)
    mod_3 = KMeans(n_clusters=3, random_state=seed).fit(df_in)

    assert np.allclose(mod_2.labels_, mod_list_test[0].labels_)
    assert mod_3.inertia_ == mod_dict_test['3'].inertia_


def test_get_a_mod_list_and_dict_non_iter():

    cluster_range = 100

    with pytest.raises(TypeError):
        get_a_mod_list_and_dict(df_in, cluster_range)
