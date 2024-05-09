import cv2
import os
# import math
import shutil
import numpy as np
from PIL import Image

from consts import MIX_PATH, AUGMENT_PATH

# Ruta imagen base
image_path = './test/test2.jpg'
annotations_path = './test/test2.txt'


def get_image_size(image_path):
    sample_image = Image.open(image_path)
    return sample_image.size


def flip_horizontal(annotation, image_width, image_height):
    x_center_flipped = 1 - annotation['x_center']
    return {
        'class_index': annotation['class_index'],
        'x_center': x_center_flipped,
        'y_center': annotation['y_center'],
        'width': annotation['width'],
        'height': annotation['height']
    }


def flip_vertical(annotation, image_width, image_height):
    y_center_flipped = 1 - annotation['y_center']
    return {
        'class_index': annotation['class_index'],
        'x_center': annotation['x_center'],
        'y_center': y_center_flipped,
        'width': annotation['width'],
        'height': annotation['height']
    }

# WIP
# def rotate_45(annotation, image_width, image_height):
#     corners = get_box_corners(annotation, image_width, image_height)

#     return {
#         'class_index': annotation['class_index'],
#         'x_center': new_x_center / image_width,
#         'y_center': new_y_center / image_height,
#         'width': new_width / image_width,
#         'height': new_height / image_height
#     }


def get_box_corners(annotation, image_width, image_height):
    x_center = annotation['x_center'] * image_width
    y_center = annotation['y_center'] * image_height
    width = annotation['width'] * image_width
    height = annotation['height'] * image_height

    # Esquina superior izquierda
    x1 = x_center - (width / 2)
    y1 = y_center - (height / 2)

    # Esquina superior derecha
    x2 = x1 + width
    y2 = y1

    # Esquina inferior izquierda
    x3 = x1
    y3 = y1 + height

    # Esquina inferior derecha
    x4 = x2
    y4 = y3

    # Guardar las coordenadas en un array
    corners = [x1, y1, x2, y2, x3, y3, x4, y4]

    return np.array(corners)


def rotate_90_clockwise(annotation, image_width, image_height):
    x_center_rotated = 1 - annotation['y_center']
    y_center_rotated = annotation['x_center']
    return {
        'class_index': annotation['class_index'],
        'x_center': x_center_rotated,
        'y_center': y_center_rotated,
        'width': annotation['height'],
        'height': annotation['width']
    }


def rotate_90_counterclockwise(annotation, image_width, image_height):
    x_center_rotated = annotation['y_center']
    y_center_rotated = 1 - annotation['x_center']
    return {
        'class_index': annotation['class_index'],
        'x_center': x_center_rotated,
        'y_center': y_center_rotated,
        'width': annotation['height'],
        'height': annotation['width']
    }

# WIP
# def rotate_135(annotation, image_width, image_height):
#

#     return {
#         'class_index': annotation['class_index'],
#         'x_center': max(0, min(1, new_x_center)),
#         'y_center': max(0, min(1, new_y_center)),
#         'width': max(0, min(1, new_width / image_width)),
#         'height': max(0, min(1, new_height / image_height))
#     }


def identity(annotation, image_width, image_height):
    return annotation


def transform_image(image):

    # Aplicar transformaciones comunes
    return [
        ("flip_horizontal", cv2.flip(image, 1)),
        ("flip_vertical", cv2.flip(image, 0)),
        # ("rotate_45", cv2.warpAffine(
        #     image,
        #     cv2.getRotationMatrix2D(
        #         (image.shape[1]/2, image.shape[0]/2),
        #         45,
        #         1.0
        #     ),
        #     (image.shape[1], image.shape[0])
        # )),
        ("rotate_90_clockwise", cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)),
        # ("rotate_135", cv2.warpAffine(
        #     image,
        #     cv2.getRotationMatrix2D(
        #         (image.shape[1]/2, image.shape[0]/2),
        #         135,
        #         1.0
        #     ),
        #     (image.shape[1], image.shape[0])
        # )),
        ("rotate_90_counterclockwise", cv2.rotate(
            image, cv2.ROTATE_90_COUNTERCLOCKWISE
        )),
        ("blur", cv2.GaussianBlur(image, (5, 5), 0)),
        ("brightness_increase", cv2.add(image, 50)),
        ("brightness_decrease", cv2.subtract(image, 50)),
        ("contrast_increase", cv2.addWeighted(image, 1.5, image, 0, 0)),
        ("contrast_decrease", cv2.addWeighted(image, 0.5, image, 0, 0)),
    ]


def store_transformed_image(image_path, img_name, store_path):
    # Load image
    image = cv2.imread(image_path)

    # Store original image
    cv2.imwrite(os.path.join(store_path, img_name), image)

    image_transformations = transform_image(image)
    name, extension = os.path.splitext(img_name)
    for transfromation, transformed_image in image_transformations:
        cv2.imwrite(
            os.path.join(store_path, f'{name}_{transfromation}{extension}'),
            transformed_image
        )


def load_annotations_lines(annotation_path):
    annotations = []

    with open(annotation_path, 'r') as file:
        for line in file:
            line = line.strip().split(' ')
            class_index = int(line[0])
            x_center, y_center, width, height = map(float, line[1:])
            annotations.append({
                'class_index': class_index,
                'x_center': x_center,
                'y_center': y_center,
                'width': width,
                'height': height
            })

    return annotations


transformations = [
    {
        'name': 'flip_horizontal',
        'operation': flip_horizontal
    },
    {
        'name': 'flip_vertical',
        'operation': flip_vertical
    },
    # {
    #     'name': 'rotate_45',
    #     'operation': rotate_45
    # },
    {
        'name': 'rotate_90_clockwise',
        'operation': rotate_90_clockwise
    },
    # {
    #     'name': 'rotate_135',
    #     'operation': rotate_135
    # },
    {
        'name': 'rotate_90_counterclockwise',
        'operation': rotate_90_counterclockwise
    },
    {
        'name': 'blur',
        'operation': identity
    },
    {
        'name': 'brightness_increase',
        'operation': identity
    },
    {
        'name': 'brightness_decrease',
        'operation': identity
    },
    {
        'name': 'contrast_increase',
        'operation': identity
    },
    {
        'name': 'contrast_decrease',
        'operation': identity
    },
]


def transform_and_store_annotations(
    annotation_path, annotation_name, store_path, image_path
):
    # Store original annotation
    shutil.copy(
        annotation_path, f"{store_path}/{annotation_name}.txt"
    )

    annotations_lines = load_annotations_lines(annotation_path)
    image_width, image_height = get_image_size(image_path)

    for transformation in transformations:
        destination = (
            f"{store_path}/{annotation_name}_{transformation['name']}.txt"
        )
        with open(destination, 'w') as file:
            for annotation in annotations_lines:
                transformed_annotation = transformation['operation'](
                    annotation,
                    image_width,
                    image_height
                )
                line = f"{transformed_annotation['class_index']} "
                line += f"{transformed_annotation['x_center']} "
                line += f"{transformed_annotation['y_center']} "
                line += f"{transformed_annotation['width']} "
                line += f"{transformed_annotation['height']}\n"
                file.write(line)


def augment_datasets():

    # Get list of mixed datasets
    datasets_dirs = list(os.listdir(MIX_PATH))

    for dataset in datasets_dirs:
        # Augment each image
        dataset_path = f'{MIX_PATH}/{dataset}'
        store_path = f'{AUGMENT_PATH}/{dataset}'
        os.makedirs(store_path, exist_ok=True)
        for image_name in os.listdir(dataset_path):
            # check if the file is an image ends with png or jpg or jpeg
            if (image_name.endswith((".png", ".jpg", ".jpeg"))):
                image_path = f'{dataset_path}/{image_name}'
                store_transformed_image(
                    image_path,
                    image_name,
                    store_path
                )

                annotation_path = (
                    f'{dataset_path}/{os.path.splitext(image_name)[0]}.txt'
                )
                transform_and_store_annotations(
                    annotation_path,
                    os.path.splitext(image_name)[0],
                    store_path,
                    image_path
                )

    return True
