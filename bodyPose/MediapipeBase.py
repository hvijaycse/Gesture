from typing import List, Tuple
import mediapipe as mp
from mediapipe.python.solutions.hands import HandLandmark
import numpy as np

import cv2

from abc import ABC, abstractmethod

from mediapipe.python.solutions.drawing_utils import DrawingSpec
from numpy.lib.function_base import select


class MediapipeBase(ABC):
    # Base class for mediapipe solution detection


    def __init__(
        self, video_Capture: cv2.VideoCapture, 
        min_detection_confidence=0.75, min_tracking_confidence=0.75,
        ) -> None:


        super().__init__


        self.solution_Name = "Base Class"

        self.MP_Solution = None
        
        self.MP_Solution_Detector = None

        self.MP_Solution_CONNECTIONS = None

        self.MP_drawing_utils = mp.solutions.drawing_utils

        self.min_detection_confidence = min_detection_confidence

        self.min_tracking_confidence = min_tracking_confidence

        self.landmark_LastDict = {}

        self.landmark_Smoothenss = 7

        self.results_Landmarks = []

        self.image = None

        self.results = None

        self._setFrameWidthHeight(video_Capture)
    
    def _setFrameWidthHeight(self, video_Capture: cv2.VideoCapture ):

        self.frame_Width = int(video_Capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_Height = int(video_Capture.get(cv2.CAP_PROP_FRAME_HEIGHT))


    
    def _set_MP_Solution(self,solution_Name, MP_Solution, MP_Solution_Detector, MP_Solution_CONNECTIONS) -> None:
        self.solution_Name = solution_Name
        self.MP_Solution = MP_Solution
        self.MP_Solution_Detector = MP_Solution_Detector
        self.MP_Solution_CONNECTIONS = MP_Solution_CONNECTIONS
        self._set_detector()
    
    def _set_detector(self, **kwargs, ):

        if self.MP_Solution_Detector:
            self.MP_Solution_Detector = self.MP_Solution_Detector(
                min_detection_confidence= self.min_detection_confidence,
                min_tracking_confidence= self.min_tracking_confidence,
                **kwargs
                )
        else:
            print("Set MP_Solution first. ")
            exit()

    def process(self, image, flip = True) -> None:
        
        if flip:
            image = cv2.flip(image, 1)

        self.image = image

        if self.MP_Solution_Detector:

            image_RGB = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

            self.results = self.MP_Solution_Detector.process(image_RGB)

            self._set_result_Landmarks()
        else:
            print("SET MP_Solution with _set_MP_Solution method fist")
            exit()
            
    

    def plot_all_Landmarks(
        self,
        landmarks_Specs: DrawingSpec = DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
        connection_Specs: DrawingSpec = DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
        ) -> None:

        if self.results_Landmarks:

            # if self.MP_Solution_CONNECTIONS:
            for result_landmarks in self.results_Landmarks:

                self.MP_drawing_utils.draw_landmarks(
                    image = self.image, landmark_list = result_landmarks, connections = self.MP_Solution_CONNECTIONS,
                    landmark_drawing_spec = landmarks_Specs, connection_drawing_spec = connection_Specs
                )
    
    def plot_this_Landmark(
        self,  landmarks_Name: str,
        result_index = 0, radius:int=4, 
        color=(121, 22, 76), thickness=2
        ) -> None:

        if self.results_Landmarks:

            Cordinates  = self._get_coordinate_by_Landmark_scalled(landmark_name=landmarks_Name, result_index=result_index)
            if Cordinates:
                self.image = cv2.circle(
                    self.image, Cordinates[:2], radius=radius, 
                    color=color, thickness=thickness  
                )
            
    
    def put_text_on_landmark(
        self, text: str, landmark_name: str,
        result_index = 0, fontFace = cv2.FONT_HERSHEY_PLAIN, fontScale = 1, 
        color = (255, 255, 255), **kwargs
        ) -> None:

        coordinates = self._get_coordinate_by_Landmark_scalled(landmark_name=landmark_name, result_index=result_index)

        if coordinates:
            cv2.putText( 
                self.image, text=text, org=coordinates[:2],
                fontFace=fontFace, fontScale=fontScale, color=color, 
                **kwargs
                )
    

    def get_distance_btw_landmarks(self, landmark_name_1:str, landmark_name_2: str, result_index:int = 0) -> float:

        if self.results_Landmarks:
            l1_x, l1_y, _ = self._get_coordinate_by_Landmark_scalled(landmark_name=landmark_name_1, result_index=result_index)
            l2_x, l2_y, _ = self._get_coordinate_by_Landmark_scalled(landmark_name=landmark_name_2, result_index=result_index)

            base = l1_x - l2_x
            perpendicular = l1_y - l2_y

            return np.hypot(base, perpendicular)

        return 0
    
    def get_mid_by_landmarks(self, landmark_name_1:str, landmark_name_2: str, result_index:int = 0) -> np.array:

        if self.results_Landmarks:

            coordinate1 = self._get_coordinate_by_Landmark_scalled(landmark_name=landmark_name_1, result_index=result_index)
            coordinate2 = self._get_coordinate_by_Landmark_scalled(landmark_name=landmark_name_2, result_index=result_index)

            return (coordinate1 + coordinate2) / 2
    

    def get_all_coordinates(self, landmark_name_list: List[str] = None, result_index = 0):

        if self.results_Landmarks:
            if not landmark_name_list: 
                row = list(
                    np.array(
                        [[point.x, point.y, point.y] for point in self.results_Landmarks[result_index].landmark]
                    ).flatten()
                )
                
            else:
                row = list(
                    np.array(
                        [self._get_coordinate_by_Landmark(landmark_name=landmark_name) for landmark_name in landmark_name_list]
                    ).flatten()
                )
            
            return row
            # pass
        return None
    

    def _get_coordinate_by_Landmark_scalled(self, landmark_name:str, result_index : int = 0):

        coordinates = self._get_coordinate_by_Landmark(landmark_name=landmark_name, result_index=result_index)

        if coordinates:
            return list(
                np.multiply(
                    coordinates,
                    [self.frame_Width, self.frame_Height, self.frame_Width]
                ).astype(int)
            ) 
            
        else:
            return None

    


    

    @abstractmethod
    def _set_result_Landmarks(self):
        '''
        This method will wil be used to update self.landmarks list
        This needs to be done specific to mediapipe solutions method
        '''
        pass

    @abstractmethod
    def _get_coordinate_by_Landmark(
        self, 
        landmark_name: str, 
        result_index : int = 0
        ) -> None or Tuple:

        '''
        This method will return the coordinate of landmarks by name.
        '''
        pass


    def imshow(self,):
        cv2.imshow(self.solution_Name, self.image, )
        


class HandSolution(MediapipeBase):

    def __init__(self, video_Capture: cv2.VideoCapture, min_detection_confidence=0.75, min_tracking_confidence=0.75) -> None:

        super().__init__(video_Capture, min_detection_confidence=min_detection_confidence, min_tracking_confidence=min_tracking_confidence)

        self._set_MP_Solution("Hands", mp.solutions.hands ,mp.solutions.hands.Hands, mp.solutions.hands.HAND_CONNECTIONS)

    def _set_result_Landmarks(self):  
        self.results_Landmarks = self.results.multi_hand_landmarks
    
    def _get_coordinate_by_Landmark(self, landmark_name: str, result_index: int=0) -> None or Tuple:

        try:
            if self.results_Landmarks:
                landmark_key = self.MP_Solution.HandLandmark.__getitem__(landmark_name)
                result_Landmark = self.results_Landmarks[result_index]

                return [ result_Landmark.landmark[landmark_key].x, result_Landmark.landmark[landmark_key].y, result_Landmark.landmark[landmark_key].z]
        except:
            return None
    

if __name__ == "__main__":

    cap = cv2.VideoCapture(0)

    HandSolution_object = HandSolution(video_Capture=cap)

    while cap.isOpened():

        success, image = cap.read()

        HandSolution_object.process(image)

        # HandSolution_object.plot_all_Landmarks()

        # HandSolution_object.plot_this_Landmark("WRIST")

        # HandSolution_object.put_text_on_landmark("THIS IS WORKING", "INDEX_FINGER_TIP")

        # cords = HandSolution_object.get_all_coordinates(landmark_name_list=["WRIST", "INDEX_FINGER_TIP"])
        
        HandSolution_object.imshow()

        if cv2.waitKey(1) & 0XFF == 27:
            break
    
    cap.release()