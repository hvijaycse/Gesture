import sys
import os

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

    if arguments[0].lower() == 'add':

        

        class_name = arguments[1]
        data_points_to_be_collected = 400
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

            handSolution_obj.imshow()
            cv2.waitKey(1)

            collected += 1
        
        file.close()
        




    
    elif arguments[0].lower() == 'remove':
        removeClass = arguments[1]

        df = pd.read_csv(data_filename)
        df.drop(df[df['Class']==removeClass].index, axis=0, inplace=True)
        df.to_csv(data_filename, index=False)
    
    elif arguments[0].lower() == 'delete_all':

        df = pd.read_csv(data_filename)
        df.drop(df.index, axis=0, inplace=True)
        df.to_csv(data_filename, index=False)

    
if __name__ == "__main__":
    
    main()


