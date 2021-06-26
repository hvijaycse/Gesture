from mediapipeSolution import hand
from mediapipeSolution.hand import handSolution
from gestureHandler.mouse import mouseActions

from config import get_config

import cv2

import pickle

import numpy as np

import pyautogui

from threading import Thread

import sys
import traceback


def main():



    config = get_config()

    if config is None:
        print("Error loading config")
        exit(1)

    total_landmarks = config["total_landmarks"]
    video_Source = config["video_Source"]
    model_filename = config["model_filename"]

    screenW, screenH  = pyautogui.size()

    stop_threads = False

    thread_stop_func = lambda: stop_threads

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

    try:

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
                
                # cv2.imshow('Hand gesture', handSolution_obj.image)

                handSolution_obj.imshow()

                if cv2.waitKey(1) & 0xFF == 27:
                    break
        
        elif arguments[0] == "run":

            pyautogui.FAILSAFE=False

            cap_w = handSolution_obj.frame_Width
            cap_h = handSolution_obj.frame_Height

            frame_Xs = int((cap_w * config['FrameXS'][0]) / config['FrameXS'][1])
            frame_Xe = int((cap_w * config['FrameXE'][0]) / config['FrameXE'][1])

            frame_Ys = int((cap_h * config['FrameYS'][0]) / config['FrameYS'][1])
            frame_Ye = int((cap_h * config['FrameYE'][0]) / config['FrameYE'][1])

            print(frame_Xs, frame_Ys)
            print(frame_Xe, frame_Ye)
            MouseAction_Queue = []

            mouse_thread = Thread(target = mouseActions, args = ( MouseAction_Queue, thread_stop_func,))

            mouse_thread.start()

            while cap.isOpened():
        
                success, image = cap.read()


                handSolution_obj.process(image)

                predection = ""

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
                



                predection_mapping = config["Gesture"].get(predection, "IDLE")

                MouseAction_Queue.clear()

                landmark_name = config["Landmarks"].get(predection_mapping, "IDLE")

                if predection_mapping != "ZOOM":

                    landmark_cords = handSolution_obj.get_coordinate_smooth(landmark_name)

                    if landmark_cords != None:

                        X, Y, _ = landmark_cords

                        if config["Landmark_Scalling"].get(predection_mapping, 0):

                            X = np.interp(X, [frame_Xs, frame_Xe], [0, screenW])

                            Y = np.interp(Y, [frame_Ys, frame_Ye], [0, screenH])

                        MouseAction_Queue.append(
                            [
                                predection_mapping,
                                [X, Y]
                            ]
                        )
                    

                    handSolution_obj.plot_this_Landmark_smooth(landmark_name)

                    
                handSolution_obj.image = cv2.rectangle(
                    handSolution_obj.image, 
                    (frame_Xe, frame_Ye),
                    (frame_Xs, frame_Ys),
                    (255, 0, 0),
                    2,
                )
                
                handSolution_obj.imshow()

                if cv2.waitKey(1) & 0xFF == 27:
                    stop_threads = True
                    mouse_thread.join()
                    print("BYE BYE")
                    break
    
    except KeyboardInterrupt:
        stop_threads = True
        mouse_thread.join()
        print("BYE BYE")
        exit()
    
    except Exception as  err:
        # print(e.with_traceback())
        traceback.print_exc()
        stop_threads = True
        mouse_thread.join()
        exit(1)


        
        


if __name__ == "__main__":
    main()