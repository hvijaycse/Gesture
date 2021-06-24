from .MP_base import MP_base


import cv2
from mediapipe.python.solutions import face_mesh
from mediapipe.python.solutions.drawing_utils import DrawingSpec


class facemeshSolution(MP_base):

    def __init__(
        self, 
        video_Capture: cv2.VideoCapture, 
        min_detection_confidence=0.75, 
        min_tracking_confidence=0.75, 
        **kwargs
        ) -> None:

        super().__init__(video_Capture, min_detection_confidence=min_detection_confidence, min_tracking_confidence=min_tracking_confidence)

        self._set_MP_Solution(
            solution_Name='Face Mesh',
            MP_Solution=face_mesh,
            MP_Solution_Detector=face_mesh.FaceMesh,
            MP_Solution_CONNECTIONS= face_mesh.FACE_CONNECTIONS,
            MP_Landmarks = None
        )
    

    def _set_result_Landmarks(self):
        self.results_Landmarks = self.results.multi_face_landmarks


if __name__ == "__main__":

    videoSource = 0
    videoSource = "http://192.168.43.1:8080/video"

    cap = cv2.VideoCapture(videoSource)

    faceMesh_object = facemeshSolution(cap)

    faceMesh_object.run_test()

    # while cap.isOpened():

    #     success, image = cap.read()

    #     if not success:
    #         print("Skipping the empty frame")
    #         break

    #     faceMesh_object.process(image)

    #     faceMesh_object.plot_all_Landmarks(
    #         landmarks_Specs= DrawingSpec(color=(121, 22, 76), thickness=1, circle_radius=1)
    #     )

    #     faceMesh_object.imshow()

    #     print(faceMesh_object.get_all_coordinates())



    #     if cv2.waitKey(1) & 0xFF == 21:
    #         print("Exiting the program.")
    #         break
         