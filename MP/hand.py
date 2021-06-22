from MP_base import MP_base

import cv2

from mediapipe.python.solutions import hands


class handSolution(MP_base):

    def __init__(self, video_Capture: cv2.VideoCapture, min_detection_confidence=0.75, min_tracking_confidence=0.75, **kwargs) -> None:

        super().__init__(video_Capture, min_detection_confidence=min_detection_confidence, min_tracking_confidence=min_tracking_confidence)

        self._set_MP_Solution(
            solution_Name = None,
            MP_Solution = hands, 
            MP_Solution_Detector = hands.Hands,
            MP_Solution_CONNECTIONS = hands.HAND_CONNECTIONS,
            MP_Landmarks=hands.HandLandmark,
            **kwargs
        )
    
    def _set_result_Landmarks(self):

        self.results_Landmarks = self.results.multi_hand_landmarks

    
    


if __name__ == "__main__":

    videoSource = 0
    # videoSource = "http://192.168.43.1:8080/video"

    cap = cv2.VideoCapture(videoSource)

    handPose_obj = handSolution(cap)


    handPose_obj.run_test()

