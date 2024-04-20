# Ant Datasets for Oso-Hormiguero

This repository contains a collection of datasets related to ants used in the [Oso-Hormiguero](https://github.com/genaroNF/oso-hormiguero) project, along with scripts to process the data for use with the selected model.

## Contents

- **Generators:** Scripts to generate different combinations of datasets mentioned in the training log. Located under `generators` folder.
- **Processors:** Scripts to normalize the data for a specific model, named `<dataset>_<model>.py`. `Currently only works for yolo.`

## How to Use
1. Run `python main.py` to start the CLI client for processing datasets and/or generating mixes.
2. Select one of the options prompted in the console:
   - **Option 1:** Process a dataset for YOLO:
     - Normalizes the datasets for YOLOv8.
   - **Option 2:** Create a mix of data sets.
     - Combines all the project datasets into one.

### Option 1 - Process a Dataset for YOLO
- The console will display the available datasets. Select the datasets you want to mix, separating them by semicolons.

### Option 2 - Create Mixes
- Select one of the options prompted in the console:
   - **Mix all the datasets:** Uses the entire dataset mix.
   - **Mix all the datasets with less slope:** Reduces the number of similar images to decrease the slope.
   - **Custom mix:** Displays the available datasets. Select the datasets you want to mix, separating them by semicolons.

## Results
Under reults folder there are two directorys:

### datasets
Contains the processed datasets.

### mixes
Contains the mixed datasets.

## Datasets References
- [Cao, Xiaoyan (2021), “ANTS--Ant Detection and Tracking”, Mendeley Data, V3, doi: 10.17632/9ws98g4npw.3, visited on 2024-03-24](https://data.mendeley.com/datasets/9ws98g4npw/3)
- [Djay de Gier, Ant Object Detection Dataset, Roboflow, visited on 2024-03-24](https://universe.roboflow.com/djay-de-gier-fopbf/ant-object-detection)