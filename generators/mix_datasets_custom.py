import os
from consts import PROCESS_PATH, DATASETS_PATH
from processors.yolo import process_selected_datasets
from process_datasets import get_dataset_selection
from generators.mix_datasets import mix_datasets


def is_directory(file):
    return os.path.isdir(os.path.join('./datasets', file))


def mix_datasets_selected(datasets=[], slope=None):

    datasets_dirs = list(
        filter(is_directory, os.listdir(PROCESS_PATH))
    ) if os.path.exists(PROCESS_PATH) else datasets

    if not datasets_dirs:
        print('No directories found in the processed datasets path.')
        option = input('Do you want toprocess all the data (y/n): ')
        print('-' * 70)

        if (option == 'y'):
            datasets_dirs = list(
                filter(is_directory, os.listdir(DATASETS_PATH))
            )
            process_selected_datasets(PROCESS_PATH, datasets_dirs)
        else:
            return True

    if datasets_dirs:

        selected_datasets = get_dataset_selection()
        if (not selected_datasets):
            return False
        return mix_datasets(selected_datasets, slope)

    return True
