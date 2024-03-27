"""
This code creates the mix for train40 for example

Combination
  Training
    - Cao, Xiaoyan: Outdoor 1-4, Indoor 1-5
    - Djay de Gier: Train
  Validation
    - Cao, Xiaoyan: Outdoor 5
    - Djay de Gier: valid
  Test (we don't use `Cao, Xiaoyan` because the images are similar)
    - Djay de Gier: Test 
"""
import os
import glob
import shutil
from pathlib import Path

from processors.ANTS.yolo import process_ANTS
from processors.roboflow.yolo import process_roboflow

def mix_all_datasets():
  path = input("specify a path to save the mix (default ./result/mixes/roboflow_ANTS): ") or "./results/mixes/roboflow_ANTS"
  Path(f"{path}/training").mkdir(parents=True, exist_ok=True)
  Path(f"{path}/test").mkdir(parents=True, exist_ok=True)
  Path(f"{path}/validation").mkdir(parents=True, exist_ok=True)

  should_process = input("Should we process the data(Y|N): ") 
  should_process = should_process == "Y"
  dataset_path = input(
    "Where should we store the process data(./results/datasets): "
    if should_process else
    "Where are the processed datasets(./results/datasets): "
  ) or "./results/datasets"

  if should_process:
    process_ANTS(dataset_path)
    process_roboflow(dataset_path)

  for root, dirs, files in os.walk(f"{dataset_path}/roboflow/train" ):
    for name in files:
      shutil.copy(f"{root}/{name}", f"{path}/training/{name}")
  
  for root, dirs, files in os.walk(f"{dataset_path}/roboflow/test" ):
    for name in files:
      shutil.copy(f"{root}/{name}", f"{path}/test/{name}")
  
  for root, dirs, files in os.walk(f"{dataset_path}/roboflow/valid" ):
    for name in files:
      shutil.copy(f"{root}/{name}", f"{path}/validation/{name}")

  for root, dirs, files in os.walk(f"{dataset_path}/ANTS/IndoorDataset" ):
    for name in files:
      shutil.copy(f"{root}/{name}", f"{path}/training/{name}")

  for root, dirs, files in os.walk(f"{dataset_path}/ANTS/OutdoorDataset" ):
    for name in files:
      shutil.copy(f"{root}/{name}", f"{path}/validation/{name}" if "Seq0010Object30Image64" in name else f"{path}/training/{name}")
