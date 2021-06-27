from .MP_base import MP_base

import cv2

from mediapipe.python.solutions import pose


class poseSolution(MP_base):

    def __init__(self, video_Capture: cv2.VideoCapture, min_detection_confidence=0.75, min_tracking_confidence=0.75, **kwargs) -> None:
        super().__init__(video_Capture, min_detection_confidence=min_detection_confidence, min_tracking_confidence=min_tracking_confidence,)

        self._set_MP_Solution(
            solution_Name="Body Pose",
            MP_Solution=pose,
            MP_Solution_Detector=pose.Pose,
            MP_Solution_CONNECTIONS= pose.POSE_CONNECTIONS,
            MP_Landmarks= pose.PoseLandmark
        )
    
    def _set_result_Landmarks(self):
        self.results_Landmarks = [self.results.pose_landmarks]
    

if __name__ == "__main__":

    videoSource = 0
    # videoSource = "http://192.168.43.1:8080/video"

    cap = cv2.VideoCapture(videoSource)

    pose_object = poseSolution(cap)

    pose_object.run_test()
