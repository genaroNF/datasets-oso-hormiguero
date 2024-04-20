
import os
import yaml
import glob
import pandas as pd
import shutil
from PIL import Image
from pathlib import Path
from consts import DATASETS_PATH, BASE_STORE_PATH

IMG = 'img_folder'
ANNOTATIONS = 'annotation_folder'
CSV_KEYS = 'csv_keys'
PURPOSE = 'TYPE'


def copy_images_to_destination(img_path, store_path, sub_dataset_name):
    for img_name in os.listdir(img_path):
        if os.path.isfile(f'{img_path}/{img_name}'):
            shutil.copy(
                f'{img_path}/{img_name}',
                f'{store_path}/{sub_dataset_name}_{img_name}'
            )


def copy_annotations_to_destination(
    store_path, sub_dataset_name, annotation_path, config
):
    # Move annotations and images into destination folder
    for annotated_file in glob.glob(f'{annotation_path}/*.txt'):
        fix_class_in_dataframe(
            store_path,
            sub_dataset_name,
            config,
            annotated_file
        )


def fix_class_in_dataframe(store_path, sub_dataset_name, config, file):
    data = pd.read_csv(file, names=config[CSV_KEYS], sep=' ')
    data['class'] = 0
    data.to_csv(
        f'{store_path}/{sub_dataset_name}_{os.path.basename(file)}',
        index=False,
        sep=' ',
        header=False
    )


def get_image_size(img_path):
    sample_image = Image.open(
        f'{img_path}/{os.listdir(img_path)[0]}'
    )
    return sample_image.size


def is_directory(file):
    return os.path.isdir(os.path.join('./datasets', file))


def normalize_csv_file_for_yolo(
    csv_keys, csv_file, width, height, store_path, sub_dataset_name
):
    csv_file['bbl'] = (
        (csv_file['bbl'] + csv_file['bbw'] / 2) / width
    )
    csv_file['bbt'] = (
        (csv_file['bbt'] + csv_file['bbh'] / 2) / height
    )
    csv_file['bbw'] = csv_file['bbw'] / width
    csv_file['bbh'] = csv_file['bbh'] / height

    if 'frame' in csv_keys:
        separate_data_by_frame(
            csv_file, store_path, sub_dataset_name
        )
    return csv_file


def create_config_file(store_path, dataset_type):
    data = {
        'type': dataset_type
    }
    with open(f'{store_path}/config.yml', 'w') as config:
        yaml.dump(data, config, sort_keys=False)


def separate_data_by_frame(normalized_csv, store_path, sub_dataset_name):
    for frame in normalized_csv['frame'].unique():
        frame_annotations = normalized_csv[
            normalized_csv['frame'] == frame
        ][
            ['bbl', 'bbt', 'bbw', 'bbh']
        ]

        # Add a class key to csv file with value 0
        # ( ant class value = 0 )
        frame_annotations.insert(0, 'class', 0)
        num = f'{frame}'.zfill(6)
        frame_annotations.to_csv(
            f'{store_path}/{sub_dataset_name}_{num}.txt',
            index=False,
            sep=' ',
            header=False
        )


def process_selected_datasets(input_store_path, datasets, slope=None):
    base_store_path = input_store_path if input_store_path else BASE_STORE_PATH

    for dataset in datasets:

        dataset_path = os.path.join(DATASETS_PATH, dataset)
        with open(f'{dataset_path}/config.yml') as config:
            params = yaml.full_load(config)

        store_path = f'{base_store_path}/{dataset}'

        Path(f'{store_path}').mkdir(
            parents=True,
            exist_ok=True
        )

        shutil.copy(f'{dataset_path}/config.yml', store_path)
        csv_keys = params[CSV_KEYS]

        for sub_dataset in params['set_of_datasets']:

            sub_dataset_name = sub_dataset['name']
            img_path = sub_dataset[IMG]
            annotation_path = sub_dataset[ANNOTATIONS]

            store_path = f'{base_store_path}/{dataset}/{sub_dataset_name}'

            Path(f'{store_path}').mkdir(parents=True, exist_ok=True)

            # Copy images to store path
            copy_images_to_destination(img_path, store_path, sub_dataset_name)

            # Normalize all files in directory
            if (is_directory(annotation_path) and not params['isNormalized']):
                # Get images size to normalize entries for yolo
                width, height = get_image_size(img_path)
                for annotated_file in glob.glob(f'{annotation_path}/*.txt'):
                    csv_file = pd.read_csv(
                        f'{annotation_path}/{annotated_file}', names=csv_keys
                    )
                    normalized_csv = csv_file[csv_keys]
                    normalized_csv = normalize_csv_file_for_yolo(
                        csv_keys, normalized_csv, width,
                        height, store_path, sub_dataset_name
                    )

            # Normalize file in directory
            elif not params['isNormalized']:
                # Get images size to normalize entries for yolo
                width, height = get_image_size(img_path)
                csv_file = pd.read_csv(annotation_path, names=csv_keys)
                normalized_csv = csv_file[csv_keys]
                normalized_csv = normalize_csv_file_for_yolo(
                    csv_keys, normalized_csv, width,
                    height, store_path, sub_dataset_name
                )

            else:
                copy_annotations_to_destination(
                    store_path, sub_dataset_name, annotation_path, params
                )

    print('-' * 70)
    print('-' * 70)
    print('Datasets were processed successfully.')
    print('-' * 70)
    print('-' * 70)
