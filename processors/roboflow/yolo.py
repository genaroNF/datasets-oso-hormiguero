"""
This script updates the data of the dataset in 

For this script to work you have to put specify the path to the foler where all the label files are stored
"""
import os
import glob
import shutil
from pathlib import Path
import pandas as pd



def process_roboflow(save_path):
    def fix_class_in_dataframe(subfolder, file):
        data = pd.read_csv(file, names=["class","1","2","3","4"], sep=" ")
        data["class"] = 0
        data.to_csv(f"{save_path}/roboflow/{subfolder}/{os.path.basename(file)}", index=False, sep=' ', header=False)

    path = f"./datasets/Djay de Gier, Ant object detection Dataset"
    subfolders = ["train", "test", "valid"]

    for subfolder in subfolders:
        # create path and save directory
        Path(f"{save_path}/roboflow/{subfolder}").mkdir(parents=True, exist_ok=True)
        for file in glob.glob(f"{path}/{subfolder}/labels/*.txt"):
            fix_class_in_dataframe(subfolder, file)

        for file_in_img in os.listdir(f"{path}/{subfolder}/images"):
            if os.path.isfile(f"{path}/{subfolder}/images/{file_in_img}"):
                shutil.copy(f"{path}/{subfolder}/images/{file_in_img}", f"{save_path}/roboflow/{subfolder}/{file_in_img}")
