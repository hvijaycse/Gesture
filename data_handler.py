# Importing modules created by me
from ctypes import ArgumentError
from mediapipeSolution.hand import handSolution
from config import get_config

# Importing all the other modules requried.
import sys
import os

import pandas as pd

import csv
import cv2
import numpy as np


def main():

    # Getting the config dictionary
    config = get_config()

    if config is None:
        print("Error in loading config")
        exit(1)

    
    # Setting the variables
    data_filename = config['data_filename']
    total_landmarks = config['total_landmarks']
    arguments = sys.argv[1:]

    # Checking if the file for data points exists or not.
    if not os.path.isfile(f'./{data_filename}'):
        # data point file does not exist
        # Creating the file
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
    
    

    if not arguments :
        # No argument is passed to the program
        arguments.append("Help")


    if arguments[0].lower() == 'add':
        # add argument is passed to the program 

        if len(arguments) == 1:
            print("Please pass the name of the class to be added to datapoints file.")
            exit(1)

        
        # Getting the class name
        class_name = arguments[1]

        # Declaring variables 
        data_points_to_be_collected = 600
        collected = 0
        multiply_row = []
        video_Source = config["video_Source"]

        # Setting VideoCapture to get input from camera .
        cap = cv2.VideoCapture(video_Source)

        # Opeining the datapoints file
        file = open(data_filename, mode='a', newline='')
        # csv writer to write data to the datapoint file 
        csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL) 

        for _ in range(total_landmarks):
            multiply_row.append(1)
            multiply_row.append(1)
            multiply_row.append(0.2)

        # setting max_num_hands=1, so input from only one hand is taken not all.
        handSolution_obj = handSolution(
            cap,
            max_num_hands=1
        )

        # Setting variable for working area in input frame.
        cap_w = handSolution_obj.frame_Width
        cap_h = handSolution_obj.frame_Height

        frame_Xs = int((cap_w * config['FrameXS'][0]) / config['FrameXS'][1])
        frame_Xe = int((cap_w * config['FrameXE'][0]) / config['FrameXE'][1])

        frame_Ys = int((cap_h * config['FrameYS'][0]) / config['FrameYS'][1])
        frame_Ye = int((cap_h * config['FrameYE'][0]) / config['FrameYE'][1])

        # Loop to get data
        while collected < data_points_to_be_collected:
            
            success, img = cap.read()
            handSolution_obj.process(img)

            # Cheking if any hand is detected.
            if handSolution_obj.results_Landmarks:
                # Hand is detected.

                # Putting the name of class and data points collected to the image.
                handSolution_obj.put_text_on_landmark(f"{class_name}, {collected}: Data points collected ", "WRIST")

                # Plottig all the landmarks on the image, so user can verify that 
                # the hand detected by media pipe is stable and not shaking, shaking hand
                # wil add lots of noise in the dataset.
                handSolution_obj.plot_all_Landmarks()

                # Creating row of data points
                row = handSolution_obj.get_all_coordinates()
                row_procced = list(
                    np.multiply(
                        row,
                        multiply_row
                        )
                    )

                # Adding class name in the row.
                row_procced.insert(0, class_name)

                # Writing the row to the file
                csv_writer.writerow(row_procced)

                # Increasing the counter.
                collected += 1
            
            # Plotting the working area in the input frame.
            handSolution_obj.plot_rectangle(
                (frame_Xs, frame_Ys),
                (frame_Xe, frame_Ye)
            )

            # Showing the image
            handSolution_obj.imshow()
            cv2.waitKey(1)

        
        print(f"{class_name} added to dataset")
        file.close()


    
    elif arguments[0].lower() == 'remove':
        # remove command is given 

        if len(arguments) == 1:
            print("Please provide name of the class to be removed from datapoints file")
            exit(1)

        # Name of the class to be removed
        removeClass = arguments[1]

        # Creating a dataframe of the datapoints file
        df = pd.read_csv(data_filename)

        # getting name of all the class in the datapoints file 
        all_class = df['Class'].unique()

        # Checking if the class that needed to be removed is even
        # there or not.
        if removeClass not in all_class:
            print(f"{removeClass} not in dataset")
            print("List of all the class: ", all_class)
            exit()

        # Removing the class from the dataset.
        df.drop(df[df['Class']==removeClass].index, axis=0, inplace=True)
        df.to_csv(data_filename, index=False)

        print(f'{removeClass} removed from data set')
    
    elif arguments[0].lower() == 'delete_all':
        # argument to delete all the data in the datapoints class.
        print("#"*40)
        print("WARNING: YOU ARE GOING TO DELETE COMPLETE DATASET!!!")
        print("#"*40)
        print()
        # verifying is used really intent to delete the data.
        ans = input("PLEASE ENTER 'Y' TO CONFIRM THE ACTION: ")

        if ans.lower() == 'y':
            # Deletting all the data form the datapoint file.
            df = pd.read_csv(data_filename)
            df.drop(df.index, axis=0, inplace=True)
            df.to_csv(data_filename, index=False)
            print("COMPLETE DATASET DELETED")
        else:
            print("DATASET NOT DELETED")
    
    elif arguments[0].lower() == "list":
        # List argument is recived

        # creating a dataframe for the datapoints file.
        df = pd.read_csv(data_filename)    

        # Getting name of all the uniqe class in the datapoint file
        all_class = df['Class'].unique()
        # Printing all the class name
        print("All class: ", all_class)
    
    elif arguments[0].lower() == 'help':
        # Help argument is passed printing the help message.
        print('''

Hi there, this program is used to create and remove data for hand gesture.

If you want to change the configuration of this program you can do it via, 
config.json file.

If you want to check the gestues in action you can use the main.py program.
To train a model for new gesture use model_trainer.ipynb notebook. 
You can also visualize the datasets using data_visualizer.ipynb notebook.  

______________________________________________________________________

This program require arguments to be passed to it while executing

    Eg: python data_handler.py args class
___________________
List of arguments: |
___________________|
___________________________________________________________________

add: 

This argument is used to add datapoint for new gestue in the datapoints
file, name of gestue class is needed to be passed after add.

Eg: python data_handler.py add Cursor
___________________________________________________________________

remove:

This argument is used to remove datapoints of a certain class from the
datapoints file, name of gestue class is needed to be passed after add.

Eg: python data_handler.py remove Cursor
___________________________________________________________________

delete_all:

This argument is used to remove all data from the datapoints class,
A confirmation to delete all the data if asked from the user is taken 
in this.
___________________________________________________________________

help:

Show this help Screen.
___________________________________________________________________
            ''')


if __name__ == "__main__":
    # Calling the main fucntion
    main()


