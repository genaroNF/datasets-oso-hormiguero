"""
The pourpose of this file is to work over the files of the dataset of https://academic.oup.com/gigascience/article/doi/10.1093/gigascience/giac096/6776178#378261164
"""
import os
import pandas as pd
from PIL import Image
from pathlib import Path
import shutil

def process_ANTS(save_path):
    main_directory = "./datasets/Cao, xiaoyan (2021), ANTS--ant detection and tracking"
    for secondary_directory in os.listdir(main_directory):
        for x in os.listdir(f"{main_directory}/{secondary_directory}"):
            # create path and save directory
            Path(f"{save_path}/ANTS/{secondary_directory}/{x}").mkdir(parents=True, exist_ok=True)
            # open the ground truth file
            true_data = pd.read_csv(f'{main_directory}/{secondary_directory}/{x}/gt/gt.txt', names=["frame","id","bbl","bbt","bbw","bbh","confidence_score"])

            # get images size to normalize entries for yolo
            im = Image.open(f'{main_directory}/{secondary_directory}/{x}/img/000001.jpg')
            w, h = im.size

            for file_in_img in os.listdir(f'{main_directory}/{secondary_directory}/{x}/img'):
                if os.path.isfile(f'{main_directory}/{secondary_directory}/{x}/img/{file_in_img}'):
                    shutil.copy(f'{main_directory}/{secondary_directory}/{x}/img/{file_in_img}', f"{save_path}/ANTS/{secondary_directory}/{x}/{x}_{file_in_img}")

            # generate a new data frame with the processed data
            new_data = true_data[["frame", "bbl", "bbt", "bbw", "bbh"]]
            new_data["bbl"] = (new_data["bbl"] + new_data["bbw"] / 2) / w
            new_data["bbt"] = (new_data["bbt"] + new_data["bbh"] / 2) / h
            new_data["bbw"] = new_data["bbw"] / w
            new_data["bbh"] = new_data["bbh"] / h

            # separate the data by frame and create the txt files with the normalized data
            for frame in new_data["frame"].unique():
                new_df = new_data[new_data['frame']==frame][["bbl", "bbt", "bbw", "bbh"]]
                new_df.insert(0, "class", 0)
                num = f"{frame}".zfill(6)
                new_df.to_csv(f"{save_path}/ANTS/{secondary_directory}/{x}/{x}_{num}.txt", index=False, sep=' ', header=False)
