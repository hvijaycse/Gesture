import sys
import os
from numpy.distutils.misc_util import all_strings

import pandas as pd

import csv
import cv2
import numpy as np
from mediapipeSolution.hand import handSolution

from config import get_config


def main():

    config = get_config()

    if config is None:
        print("Error in loading config")
        exit(1)

    data_filename = config['data_filename']
    total_landmarks =config['total_landmarks']

    if not os.path.isfile(f'./{data_filename}'):
        
        print("Gesture gesture data file does not exist.")
        print("Creating gesture data file. ")
        headers = ["Class"]

        for i in range(total_landmarks):
            headers.append(f'x{i}')
            headers.append(f'y{i}')
            headers.append(f'z{i}')
        
        with open(data_filename, 'w', newline='') as file:
            csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL )
            csv_writer.writerow(headers)
        
    arguments = sys.argv[1:]

    if not arguments :
        arguments.append("Help")


    if arguments[0].lower() == 'add':

        

        class_name = arguments[1]
        data_points_to_be_collected = 600
        collected = 0

        multiply_row = []

        video_Source = config["video_Source"]

        cap = cv2.VideoCapture(video_Source)

        file = open(data_filename, mode='a', newline='')
        csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL) 

        for _ in range(total_landmarks):
            multiply_row.append(1)
            multiply_row.append(1)
            multiply_row.append(0.2)
        

        handSolution_obj = handSolution(
            cap,
            max_num_hands=1
        )

        cap_w = handSolution_obj.frame_Width
        cap_h = handSolution_obj.frame_Height

        frame_Xs = int((cap_w * config['FrameXS'][0]) / config['FrameXS'][1])
        frame_Xe = int((cap_w * config['FrameXE'][0]) / config['FrameXE'][1])

        frame_Ys = int((cap_h * config['FrameYS'][0]) / config['FrameYS'][1])
        frame_Ye = int((cap_h * config['FrameYE'][0]) / config['FrameYE'][1])

        while collected < data_points_to_be_collected:
            
            success, img = cap.read()

            handSolution_obj.process(img)

            if handSolution_obj.results_Landmarks:

                handSolution_obj.put_text_on_landmark(class_name, "WRIST")

                handSolution_obj.plot_all_Landmarks()

                row = handSolution_obj.get_all_coordinates()
                row_procced = list(
                    np.multiply(
                        row,
                        multiply_row
                        )
                    )

                # print(row, row_procced, sep='\n')
                row_procced.insert(0, class_name)
                csv_writer.writerow(row_procced)
            
            handSolution_obj.plot_rectangle(
                (frame_Xs, frame_Ys),
                (frame_Xe, frame_Ye)
            )

            handSolution_obj.imshow()
            cv2.waitKey(1)

            collected += 1
        
        print(f"{class_name} added to dataset")
        file.close()


    
    elif arguments[0].lower() == 'remove':
        removeClass = arguments[1]

        df = pd.read_csv(data_filename)
        all_class = df['Class'].unique()

        if removeClass not in all_class:
            print(f"{removeClass} not in dataset")
            print("List of all the class: ", all_class)
            exit()

        df.drop(df[df['Class']==removeClass].index, axis=0, inplace=True)
        df.to_csv(data_filename, index=False)
        print(f'{removeClass} removed from data set')
    
    elif arguments[0].lower() == 'delete_all':
        print("#"*40)
        print("WARNING: YOU ARE GOING TO DELETE COMPLETE DATASET!!!")
        print("#"*40)
        print()
        ans = input("PLEASE ENTER 'Y' TO CONFIRM THE ACTION: ")

        if ans.lower() == 'y':
            df = pd.read_csv(data_filename)
            df.drop(df.index, axis=0, inplace=True)
            df.to_csv(data_filename, index=False)
            print("COMPLETE DATASET DELETED")
        else:
            print("DATASET NOT DELETED")
    
    elif arguments[0].lower() == "list":
        df = pd.read_csv(data_filename)    

        all_class = df['Class'].unique()
        print("All class: ", all_class)
if __name__ == "__main__":
    
    main()


