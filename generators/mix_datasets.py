import os
import shutil
import yaml
from consts import PROCESS_PATH, MIX_PATH, DATASETS_PATH
from pathlib import Path
from processors.yolo import process_selected_datasets


def is_directory(file):
    return os.path.isdir(os.path.join('./datasets', file))


def process_datasets():
    datasets_dirs = list(
            filter(is_directory, os.listdir(DATASETS_PATH))
        )
    process_selected_datasets(PROCESS_PATH, datasets_dirs)


def copy_file_to_destination(store_path, dir_path, file, slope, file_index):
    module = 2 * slope if slope else 0
    add_file = (
        (file_index % module) == 0 or (file_index % module) == (module - 1)
    ) if slope else False

    if not slope or add_file:
        shutil.copy(f'{dir_path}/{file}', f'{store_path}/{file}')


def copy_files_to_destination(dataset, sub_dataset, slope=None):
    store_path = f"{MIX_PATH}/{sub_dataset['type']}"

    if (not os.path.exists(store_path)):
        Path(f'{store_path}').mkdir(parents=True, exist_ok=True)

    for dir_path, _, filenames in os.walk(
        f"{PROCESS_PATH}/{dataset}/{sub_dataset['name']}"
    ):
        file_index = 1
        if slope:
            filenames.sort()
        for file in filenames:
            copy_file_to_destination(
                store_path, dir_path, file, slope, file_index
            )
            file_index += 1


def mix_datasets(datasets=[], slope=None):

    if not datasets:
        print('Please select one of the following options:')
        print('1. Normalize all data sets.')
        print('2. Use normalized datasets.')
        print('3. Exit.')
        option = input('Input the number of the selected option: ')
        print('-' * 70)

    if (datasets or option == '1'):
        process_datasets()

    if datasets or option == '1' or option == '2':

        if (os.path.exists(PROCESS_PATH) or datasets):
            # Get list of processed datasets
            datasets_dirs = datasets if datasets else list(
                filter(is_directory, os.listdir(PROCESS_PATH))
            )

            for dataset in datasets_dirs:
                # Open config file
                with open(f'{PROCESS_PATH}/{dataset}/config.yml') as config:
                    params = yaml.full_load(config)

                for sub_dataset in params['set_of_datasets']:
                    copy_files_to_destination(dataset, sub_dataset, slope)

            print('-' * 70)
            print('-' * 70)
            print('Mix created successfully.')
            print('-' * 70)
        else:
            print('-' * 70)
            print('Provided path was not found.')

    else:
        return False

    return True
