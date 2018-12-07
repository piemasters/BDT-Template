import glob
import logging
import os

from tests.features.project1 import project1_config as project1_config
from tests.features.project2 import project2_config as project2_config


def before_all(context):
    context.config.setup_logging()


def before_feature(context, feature):
    dirs_to_clear = []

    if 'PROJECT1' in feature.name:
        set_logger('logs_PROJECT1.log')
        dirs_to_clear = [
            project1_config.XML_INGEST,
            project1_config.JSON_OUTPUT,
            project1_config.FAILURE_OUTPUT,
            project1_config.ERROR_OUTPUT,
        ]
    elif 'PROJECT2' in feature.name:
        set_logger('logs_PROJECT2.log')
        dirs_to_clear = [
            project2_config.XML_INGEST,
            project2_config.JSON_OUTPUT,
            project2_config.FAILURE_OUTPUT,
            project2_config.ERROR_OUTPUT,
        ]

    for d in dirs_to_clear:
        delete_directory_contents(d)

    logging.info('All directories cleared successfully')
    logging.info('Running feature ' + feature.name + ' <' + str(len(feature.scenarios)) + ' scenario(s)>')


def set_logger(filename):
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(
        filename=filename,
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def delete_directory_contents(directory):
    files = glob.glob(directory + '*')
    for file in files:
        if not os.path.isdir(file):
            os.remove(file)
