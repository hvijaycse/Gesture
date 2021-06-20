from typing import List

import mediapipe as mp
from mediapipe.python.solutions.drawing_utils import DrawingSpec


import numpy as np

import cv2

from abc import ABC, abstractmethod


class MediapipeBase(ABC):
    # Base class for mediapipe solution detection


    def __init__(
        self, video_Capture: cv2.VideoCapture, 
        min_detection_confidence=0.75, min_tracking_confidence=0.75,
        **kwargs
        ) -> None:

        # this is initializer for MediapipeBase class


        super().__init__

        self.solution_Name: str = "Base Class"
        self.video_capture: cv2.VideoCapture = video_Capture

        self.MP_Solution = None
        self.MP_Solution_Detector = None
        self.MP_Solution_CONNECTIONS = None
        self.MP_drawing_utils = mp.solutions.drawing_utils
        self.MP_landmarks = None

        self.min_detection_confidence: float = min_detection_confidence
        self.min_tracking_confidence: float = min_tracking_confidence

        self.landmark_LastDict: dict = {}
        self.landmark_Smoothenss: int = 7
        self.results_Landmarks: list = []

        self.image: np.array = None
        self.results: list = None

        # Setting the frame width and height of the video_Capture input
        self._set_Frame_Width_and_Height(video_Capture)
    
    def _set_Frame_Width_and_Height(self, video_Capture: cv2.VideoCapture ) -> None:
        # This method set frame width and height, 
        # This is used to calculate the exact location of
        # landmark on the with respect to input image.

        self.frame_Width = int(video_Capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_Height = int(video_Capture.get(cv2.CAP_PROP_FRAME_HEIGHT))


    
    def _set_MP_Solution(
        self, solution_Name, MP_Solution, 
        MP_Solution_Detector, MP_Solution_CONNECTIONS, MP_Landmarks=None ,
        **kwargs) -> None:

        # This method is used to set the Mediapipe solution method and 
        #  must be called in the child class to use mediapipe detections.

        if not solution_Name:
            self.solution_Name = MP_Solution.__doc__
        else:
            self.solution_Name = solution_Name
        # Updating the values
        self.MP_Solution = MP_Solution
        self.MP_Solution_Detector = MP_Solution_Detector
        self.MP_Solution_CONNECTIONS = MP_Solution_CONNECTIONS
        self.MP_landmarks = MP_Landmarks

        # calling _set_detector methods
        self._set_detector(**kwargs)
    
    def _set_detector(self, **kwargs, ):
        # This method is used to set the MP_soltion_dectector
        # This object is used to detect and tracks the objects.

        # Checking if MP_Solution_Detector is set
        if self.MP_Solution_Detector:

            # Creating a mediapipe detector object 
            self.MP_Solution_Detector = self.MP_Solution_Detector(
                min_detection_confidence= self.min_detection_confidence,
                min_tracking_confidence= self.min_tracking_confidence,
                **kwargs
                )
        else:
            print("Set MP_Solution first. ")
            exit()
    
    def print_landmarks_list(self,) -> None:
        # This method will print the list of 
        # name of all the landmarks in the mediapipe solution 
        if self.MP_landmarks:
            print(f"List of all the landmarks for {self.solution_Name}")
            
            for idx, landmark in enumerate(self.MP_landmarks):
                print(f"{idx}: {landmark.name}")
        else:
            print(f"Landmarks for {self.solution_Name} is not set")

    def process(self, image, flip = True) -> None:

        # process method to process the input image and
        # update the result based upon the result. 

        if flip:
            # flipping the image horizintally
            image = cv2.flip(image, 1)

        self.image = image

        # Checking if MP_Solution_Detector is set or not.
        if self.MP_Solution_Detector:

            # Processing the input image.
            image_RGB = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

            # Updating the results.
            self.results = self.MP_Solution_Detector.process(image_RGB)

            # Setting the results lanmarks to a list
            self._set_result_Landmarks()
        else:
            print("SET MP_Solution with _set_MP_Solution method fist")
            exit()
    

    '''
    Methods to plot landmarks and put text on landmarks
    '''

    def plot_all_Landmarks(
        self,
        landmarks_Specs: DrawingSpec = DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
        connection_Specs: DrawingSpec = DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
        ) -> None:

        # Method to plot all landmarks

        if self.results_Landmarks:

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

    '''
    Methods to deals with the data of landmarks
    '''
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

    
    def _get_coordinate_by_Landmark(self, landmark_name: str, result_index: int) -> None or List:

        try:
            if self.results_Landmarks and self.MP_landmarks:
                landmark_key = self.MP_landmarks.__getitem__(landmark_name)

                result_Landmark = self.results_Landmarks[result_index]

                Point = result_Landmark.landmark[landmark_key]

                return [ Point.x, Point.y, Point.z ]
            
            else:
                return None
        except:
            return None


    '''
    Using abstractmethod decorator to create 
    method to create an abstract class

    Base class specific for media pipe solutions are required to  
    created to utilize this class.
    
    '''

    @abstractmethod
    def _set_result_Landmarks(self):
        '''
        This method will wil be used to update self.landmarks list
        This needs to be done specific to mediapipe solutions method
        '''
        pass



    '''
    Method to show show the image
    '''
    def imshow(self,):
        cv2.imshow(self.solution_Name, self.image, )
    

    def run_test(self, ):

        while self.video_capture.isOpened():

            suceess, image = self.video_capture.read()

            if not suceess:
                print("Error")
                break

            self.process(image)

            self.plot_all_Landmarks()

            self.imshow()

            if cv2.waitKey(1) & 0xFF == 27:
                print("BYE! BYE!")
                break
