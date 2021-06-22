from MP_base import MP_base

import cv2

from mediapipe.python.solutions import holistic
from mediapipe.python.solutions.drawing_utils import DrawingSpec

import numpy as np

from typing import List

class holisticSolution(MP_base):
    # Class for MP_base Solution

    '''
    Will be Utilizing a dicitonary for this solution
    as its result contains multiple landmarks and detection, 
    such as face, left hand, right hand, etc.
    '''

    def __init__(
        self, 
        video_Capture: cv2.VideoCapture, 
        detection_list = ['face', 'pose', 'right_hand', 'left_hand'],
        min_detection_confidence = 0.75, 
        min_tracking_confidence = 0.75, 
        **kwargs) -> None:

        self.to_be_detected = {
            "FACE": False,
            "POSE": False,
            "LEFT_HAND": False,
            "RIGHT_HAND": False,
        }

        for detection in detection_list:

            if detection.upper() in self.to_be_detected:
                self.to_be_detected[detection.upper()] = True
         

        super().__init__(video_Capture, min_detection_confidence=min_detection_confidence, min_tracking_confidence=min_tracking_confidence, **kwargs)

        connection_dict = {
            'FACE': holistic.FACE_CONNECTIONS,
            'POSE': holistic.POSE_CONNECTIONS,
            'LEFT_HAND': holistic.HAND_CONNECTIONS,
            'RIGHT_HAND': holistic.HAND_CONNECTIONS
        }


        landmarks_dict = {
            'FACE': None,
            'POSE': holistic.PoseLandmark,
            'LEFT_HAND': holistic.HandLandmark,
            'RIGHT_HAND': holistic.HandLandmark,
        }

        self._set_MP_Solution(
            'Holistic',
            MP_Solution= holistic,
            MP_Solution_Detector= holistic.Holistic,
            MP_Solution_CONNECTIONS= connection_dict,
            MP_Landmarks = landmarks_dict,
            **kwargs,
        )
    
    def _set_result_Landmarks(self):

        self.results_Landmarks = [
            {
                'FACE': self.results.face_landmarks,
                'POSE': self.results.pose_landmarks,
                'LEFT_HAND': self.results.left_hand_landmarks,
                'RIGHT_HAND': self.results.right_hand_landmarks
            }
        ]
    
    def get_all_coordinates(self, landmark_name_list: List[str] = None, result_index = 0):

        if self.results_Landmarks:
            if not landmark_name_list: 

                row = []

                for landmark_name in self.to_be_detected.keys():
                    if self.to_be_detected[landmark_name] and self.results_Landmarks[result_index][landmark_name] is not None:
                        for point in self.results_Landmarks[result_index][landmark_name].landmark:
                            row.append([point.x, point.y, point.y])
                
                row = list(
                    np.array(
                        row
                    ).flatten()
                )

                if not row:
                    row = None
                
            else:
                row = list(
                    np.array(
                        [self._get_coordinate_by_Landmark(landmark_name=landmark_name) for landmark_name in landmark_name_list]
                    ).flatten()
                )
            
            return row
            # pass
        return None
     
    def print_landmarks_list(self,) -> None:
        # This method will print the list of 
        # name of all the landmarks in the mediapipe solution 
        if self.MP_landmarks:
            print(f"List of all the landmarks for {self.solution_Name}")
            
            for landmark_name, landmarks in self.MP_landmarks.items():

                if self.MP_landmarks[landmark_name] is not None and self.to_be_detected[landmark_name] is not None:

                    print('')
                    print(f'{landmark_name.title()} landmark list')
                    print()
                    for landmark in landmarks:
                        print(landmark.name)
        else:
            print(f"Landmarks for {self.solution_Name} is not set")
    

    def _get_coordinate_by_Landmark(self, landmark_name: str, result_index: int=0) -> None or List:
        try:
            if self.results_Landmarks and self.MP_landmarks:

                for result_landmark_name, landmark_obj in self.MP_landmarks.items():

                    try:

                        if not self.to_be_detected[result_landmark_name]:
                            continue

                        landmark_key = landmark_obj.__getitem__(landmark_name)

                        if self.results_Landmarks[result_index][result_landmark_name]:

                            result_Landmark = self.results_Landmarks[result_index][result_landmark_name]

                            Point = result_Landmark.landmark[landmark_key]

                            return [ Point.x, Point.y, Point.z ]
                        else:
                            return None
                    
                    except:
                        continue
            
            else:
                return None
        except:
            return None
    

    
    def plot_all_Landmarks(
        self, 
        landmarks_Specs: DrawingSpec = DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4), 
        connection_Specs:  DrawingSpec = DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2)
        ) -> None:

        if self.results_Landmarks:

            for result_landmark in self.results_Landmarks:

                for result_landmark_name, res_landmark in result_landmark.items():

                    if not self.to_be_detected[result_landmark_name]:
                        continue

                    self.MP_drawing_utils.draw_landmarks(

                        image = self.image, landmark_list = res_landmark, connections = self.MP_Solution_CONNECTIONS[result_landmark_name],
                        landmark_drawing_spec = landmarks_Specs, connection_drawing_spec = connection_Specs
                    )
        


if __name__ == "__main__":

    videoSource = 0

    cap = cv2.VideoCapture(videoSource)

    to_be_detected = ['left_hand']
    
    holisticSolution_obj = holisticSolution(cap,)
    
    holisticSolution_obj.run_test()