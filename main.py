from mediapipeSolution.hand import handSolution

from config import get_config

import cv2

import pickle
import numpy as np


import sys


def main():

    config = get_config()

    if config is None:
        print("Error loading config")
        exit(1)

    total_landmarks = config["total_landmarks"]
    video_Source = config["video_Source"]
    model_filename = config["model_filename"]


    arguments = sys.argv[1:]

    cap = cv2.VideoCapture(video_Source)


    with open(model_filename, 'rb') as file:
        model = pickle.load(file)

    multiply_row = []

    for _ in range(total_landmarks):
        multiply_row.append(1)
        multiply_row.append(1)
        multiply_row.append(0.2)
    
    handSolution_obj = handSolution(
        cap,
        max_num_hands = 1
        )

    if arguments[0] == 'check':

        while cap.isOpened():

            success, image = cap.read()

            handSolution_obj.process(image)

            if handSolution_obj.results_Landmarks:
                row = handSolution_obj.get_all_coordinates()
                row = list(
                    np.multiply(
                        row,
                        multiply_row
                        )
                    )
                
                predection = model.predict([row])[0]

                handSolution_obj.put_text_on_landmark(
                    text=predection,
                    landmark_name="WRIST"
                )
            
            # handSolution_obj.plot_all_Landmarks()

            handSolution_obj.plot_this_Landmark_smooth("THUMB_TIP")
            
            cv2.imshow('Hand gesture', handSolution_obj.image)

            if cv2.waitKey(1) & 0xFF == 27:
                break
    



        
        


if __name__ == "__main__":
    main()