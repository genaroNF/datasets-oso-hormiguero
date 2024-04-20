import os
from consts import DATASETS_PATH
from processors.yolo import process_selected_datasets


def is_directory(file):
    return os.path.isdir(os.path.join('./datasets', file))


def get_dataset_indexes(dataset_dirs, datasets_options, exit_option):
    datasets_options = datasets_options.replace(' ', '')
    dataset_dirs_index = datasets_options.split(',')
    if exit_option in dataset_dirs_index:
        return []

    selected_datasets = []
    for dir_index in dataset_dirs_index:
        if dir_index.isnumeric():
            selected_datasets.append(dataset_dirs[int(dir_index) - 1])

    return selected_datasets


def get_dataset_selection():
    print('Please select the dataset or datasets you want to process:')
    dataset_dirs = list(
        filter(is_directory, os.listdir(DATASETS_PATH))
    )
    dataset_dirs.sort()
    for index, dataset in enumerate(dataset_dirs):
        print(f'{index + 1}. {dataset}')

    exit_option = len(dataset_dirs) + 1
    print(f'{exit_option}. Exit.')
    print('Input the number of the selected dataset. If you want to process')
    print('multiple datasets, please input the numbers separated by a colon.')
    datasets_options = input('Leave empty to process all (E.g. 1,2,10): ')
    print('-' * 70)

    # If options is empty process all
    if (not datasets_options):
        return dataset_dirs

    return get_dataset_indexes(dataset_dirs, datasets_options, exit_option)


def process_datasets():

    selected_datasets = get_dataset_selection()
    # If list is empty exit
    if (not selected_datasets):
        return False

    print('The following datasets will be proceded: ')
    for dataset in selected_datasets:
        print(f'- {dataset}')
    confirm = input(
        'The following datasets will be proceded. Confirm (y/n): '
    )
    print('-' * 70)
    print('-' * 70)

    if confirm.lower() == 'y':
        # Proccess the selected datasets
        process_selected_datasets('./results/datasets', selected_datasets)

    return True
