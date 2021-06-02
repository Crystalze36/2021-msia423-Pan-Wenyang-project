import logging
import argparse

import yaml
import pandas as pd

from src.preprocess import scale_df, save_df
from src.model import get_a_mod_list_and_dict, cluster_selection_plot, save_model

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s',
                    level=logging.INFO)
logger = logging.getLogger('model-pipeline')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="pipeline for running cloud classification model")

    parser.add_argument('step',
                        default='test',
                        help='Which step to run',
                        choices=['preprocess', 'train'])

    parser.add_argument('--input',
                        '-i',
                        default=None,
                        help='Path to input data')

    parser.add_argument('--config',
                        default='config/config.yaml',
                        help='Path to configuration file')

    args = parser.parse_args()

    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    logger.info("Configuration file loaded from %s" % args.config)

    if args.step == 'preprocess':
        df_raw = pd.read_csv(args.input)
        df_scale = scale_df(df_raw, **config['preprocess']['scale_df'])
        save_df(df_scale, **config['preprocess']['save_df'])


    elif args.step == 'train':
        df_prepared = pd.read_csv(args.input)
        mod_dict, mod_list =  get_a_mod_list_and_dict(df_prepared, **config['model']['get_a_mod_list_and_dict'])
        cluster_selection_plot(df_prepared, mod_list, **config['model']['cluster_selection_plot'])
        save_model(mod_dict, **config['model']['save_model'])
