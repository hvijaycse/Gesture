# Importing my modules to use media pipe and mouse actions 
from mediapipeSolution.hand import handSolution
from gestureHandler.mouse import mouseActions


# Importing configuration
from config import get_config

import cv2

# To laod ml Model
import pickle
import numpy as np

import pyautogui

from threading import Thread

import sys
import traceback


def main():

    # Getting config dictionary
    config = get_config()

    if config is None:
        # Error in loading config
        print("Error loading config")
        exit(1)

    # Setting varaibles 
    total_landmarks = config["total_landmarks"]
    video_Source = config["video_Source"]
    model_filename = config["model_filename"]

    stop_threads = False # This is used to stop thread when exiting the program

    thread_stop_func = lambda: stop_threads # This method stop the thread.

    arguments = sys.argv[1:] # Getting arguments passed to the program.
    
    if not arguments :
        # No argumet passed.
        arguments.append("Help")

    # Getting video input
    cap = cv2.VideoCapture(video_Source)

    # Loading the model
    with open(model_filename, 'rb') as file:
        model = pickle.load(file)
    

    # Creating multiple row to change the data from handSolution
    # to our requirements.
    multiply_row = []

    for _ in range(total_landmarks):
        multiply_row.append(1)
        multiply_row.append(1)
        multiply_row.append(0.2)

    
    # Setting max_num_hands = 1, otherwise it will 
    # perform gesture based upon the 2 hands in the
    # video input
    handSolution_obj = handSolution(
        cap,
        max_num_hands = 1
        )

    pyautogui.FAILSAFE=False

    # Setting the variable to get the coordinate of working area in the 
    # input frame .
    screenW, screenH  = pyautogui.size()

    cap_w = handSolution_obj.frame_Width
    cap_h = handSolution_obj.frame_Height

    frame_Xs = int((cap_w * config['FrameXS'][0]) / config['FrameXS'][1])
    frame_Xe = int((cap_w * config['FrameXE'][0]) / config['FrameXE'][1])

    frame_Ys = int((cap_h * config['FrameYS'][0]) / config['FrameYS'][1])
    frame_Ye = int((cap_h * config['FrameYE'][0]) / config['FrameYE'][1])

    # Using thread to perform mouse action, as directly using pyautogui slows the process.
    MouseAction_Queue = [] # This list is used to communicate with the thread.
    mouse_thread = Thread(target = mouseActions, args = ( MouseAction_Queue, thread_stop_func,))
    mouse_thread.start()


    try:

        if arguments[0].lower() == 'test':
            # Test argument is passed only classification
            # of hand gesture will be done. 

            # Loop to get image from the video input.
            while cap.isOpened():

                success, image = cap.read()

                handSolution_obj.process(image)

                # Checking if hand is detected in the frame or not.
                if handSolution_obj.results_Landmarks:
                    # hand is detected.
                    row = handSolution_obj.get_all_coordinates()
                    row = list(
                        np.multiply(
                            row,
                            multiply_row
                            )
                        )
                    
                    # classifying the hand gesture.
                    predection = model.predict([row])[0]
                    gesture_name = config["Gesture"].get(predection, "IDLE")
                    Landmark_name = config["Landmarks"].get(gesture_name, "THUMB_TIP")

                    # Plotting the landmark which will be used 
                    # for the gesture action. 
                    handSolution_obj.plot_this_Landmark_smooth(
                        Landmark_name,
                        color=(89, 52, 249)
                        )

                    # Plotting the gesture detected on the WRIST of the hand
                    handSolution_obj.put_text_on_landmark(
                        text=predection,
                        landmark_name="WRIST"
                    )
                
                # plotting the working area in frame
                handSolution_obj.plot_rectangle(
                    (frame_Xs, frame_Ys),
                    (frame_Xe, frame_Ye)
                )

                # Plotting all the landmarks.
                handSolution_obj.plot_all_Landmarks()

                # Showing the final image
                handSolution_obj.imshow()

                # Checking if 'ESC' key is pressed
                if cv2.waitKey(1) & 0xFF == 27:
                    # Exiting the program.
                    stop_threads = True
                    mouse_thread.join()
                    break
        
        elif arguments[0].lower() == "run":
            # run argument is passed classification
            # of hand gesture and action based on that 
            # gesture will be performed. 

            # Loop to get image from the video input.
            while cap.isOpened():
        
                success, image = cap.read()


                handSolution_obj.process(image)

                predection = ""

                # Checking if hand is detected in the frame or not.
                if handSolution_obj.results_Landmarks:
                    # hand is detected.
                    row = handSolution_obj.get_all_coordinates()
                    row = list(
                        np.multiply(
                            row,
                            multiply_row
                            )
                        )
                    # classifying the hand gesture.
                    predection = model.predict([row])[0]

                    handSolution_obj.put_text_on_landmark(
                        text=predection,
                        landmark_name="WRIST"
                    )

                # Mapping the gesture to mouse module input.
                predection_mapping = config["Gesture"].get(predection, "IDLE")

                # Clearing the MouseAction_Queue
                # If this is not performed, a ghosting effect 
                # will take place 
                MouseAction_Queue.clear()

                # Getting the name of the landmark to be used for this gesture.
                landmark_name = config["Landmarks"].get(predection_mapping, "IDLE")

                # Zoom is not implemented properly skipping that for now.
                if predection_mapping != "ZOOM":

                    # getting the coordinate of the landmark
                    landmark_cords = handSolution_obj.get_coordinate_smooth(landmark_name)

                    if landmark_cords != None:
                        X, Y, _ = landmark_cords

                        # Cheking if coordinate of this gestue needed to be scalled for 
                        # working area,
                        if config["Landmark_Scalling"].get(predection_mapping, 0):

                            X = np.interp(X, [frame_Xs, frame_Xe], [0, screenW])

                            Y = np.interp(Y, [frame_Ys, frame_Ye], [0, screenH])

                        
                        # Adding the gesture to be performed to the 
                        # Mouseaction queue.
                        MouseAction_Queue.append(
                            [
                                predection_mapping,
                                [X, Y]
                            ]
                        )

                    # Plotting the landmark used for the gesture.
                    handSolution_obj.plot_this_Landmark_smooth(landmark_name)

                # plotting the working area in the frame
                handSolution_obj.plot_rectangle(
                    (frame_Xs, frame_Ys),
                    (frame_Xe, frame_Ye),
                )
                # Showing the final image
                handSolution_obj.imshow()

                # Checking if 'ESC' key is pressed
                if cv2.waitKey(1) & 0xFF == 27:
                    # Exiting the program.
                    stop_threads = True
                    mouse_thread.join()
                    print("BYE BYE")
                    break

        elif arguments[0] == "Help":
            # Help argument is passed

            # Stopping the threads. 
            stop_threads = True
            mouse_thread.join()
            # printing the help message.
            print('''

Hi there, this program perform mouse action such as controlling cursor, drag and drop
based upon hand gesture that it recive from the camera input.

If you want to change the configuration of this program you can do it via, 
config.json file.

If you want to change the default gesture for certain action you can do it via
data_handler.py program, and model_trainer.ipynb notebook. You can also visualize the 
datasets using data_visualizer.ipynb notebook.  

______________________________________________________________________

This program require arguments to be passed to it while executing

    Eg: python main.py args
___________________
List of arguments: |
___________________|
___________________________________________________________________

run: 

This argument make the program classify the gesture given to the 
program via camera input and, perform action according to them.
___________________________________________________________________

test:

This argument make the program classify the gesture given to the 
program via camera input and display them, no action are performed 
in this based upon the classification.
___________________________________________________________________

help:

Show this help Screen.
___________________________________________________________________
            ''')

        else:
            stop_threads = True
            mouse_thread.join()
    
    except KeyboardInterrupt:
        # This program can be stopped with 'ctrl + c' 
        # to stop the thread proprly this except block is created

        stop_threads = True
        mouse_thread.join()
        print("BYE BYE")
        exit()
    
    except Exception as  err:
        # If any error arise while the execution 
        # this except block is used to stop the thread
        # and properly exit the program
        traceback.print_exc()
        stop_threads = True
        mouse_thread.join()
        exit(1)


        
        


if __name__ == "__main__":
    # calling the main function
    main()