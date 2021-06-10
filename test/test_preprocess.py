import pytest
import pandas as pd

from src.preprocess import scale_df


def test_scale_df():
    features = ['sp_attack', 'sp_defense', 'hp', 'attack', 'defense', 'speed']
    df_in = pd.DataFrame([[65, 65, 45, 49, 49, 45],
                          [80, 80, 60, 62, 63, 60],
                          [122, 120, 80, 100, 123, 80],
                          [60, 50, 39, 52, 43, 65],
                          [80, 65, 58, 64, 58, 80]],
                         columns=features)
    df_true = pd.DataFrame([[-0.75181913, -0.45913113, -0.804014, -0.90028389, -0.63304444,
                             -1.59200589],
                            [-0.06417968, 0.16695677, 0.25389916, -0.18664422, -0.14608718,
                             -0.45485883],
                            [1.86121078, 1.83652452, 1.66445004, 1.89937943, 1.9408725,
                             1.06133726],
                            [-0.98103229, -1.08521903, -1.22717927, -0.73559782, -0.8417404,
                             -0.0758098],
                            [-0.06417968, -0.45913113, 0.11284407, -0.0768535, -0.32000048,
                             1.06133726]], columns=features)
    df_test = scale_df(df_in, features)
    pd.testing.assert_frame_equal(df_true, df_test)


def test_scale_df_non_df():
    df_in = 100

    with pytest.raises(TypeError):
        scale_df(df_in, ['hi'])
