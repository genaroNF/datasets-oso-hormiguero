# datasets-oso-hormiguero
Dataset's compilations used in the [oso-hormiguero](https://github.com/genaroNF/oso-hormiguero) project, here we have the datasets along with scripts that process the data to get it ready for yolov8

- generators: generate different combinations of datasets, the ones mentioned in the training log
- processors: Process the data to get it ready for a model, `<dataset>_<model>.py`
- main.py: CLI client to process the datasets and generate the mixes

## Datasets references
- [Cao, xiaoyan (2021), “ANTS--ant detection and tracking”, Mendeley Data, V3, doi: 10.17632/9ws98g4npw.3, visited on 2024-03-24](https://data.mendeley.com/datasets/9ws98g4npw/3)
- [Djay de Gier, Ant object detection Dataset, Roboflow, visited on 2024-03-24](https://universe.roboflow.com/djay-de-gier-fopbf/ant-object-detection)
