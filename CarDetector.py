from typing import List, Tuple, Dict
from ultralytics import YOLO
import cv2
from GlobalConstants import Constants

class CarDetector():

    def __init__(self, model_path):
        self.__model = YOLO(model_path)

    def detect_car(self, frame, constants: Constants) -> List[Tuple[int, int]]:
        """
        params:
            frame: capture of a video frame.
        This method obtains the center of each car that are in the image
        return:
            A list of elements, each element contains their center: (x,y)
        """
        data: List[Tuple[int, int]] = []
        frame_resized = cv2.resize(frame, (constants.CAR_WIDTH_IMAGE, constants.CAR_HEIGHT_IMAGE))  # Resizing for better precition
        results = self.__model(frame_resized, device="cpu",verbose=False, conf=0.5) # Execute the model

        for result in results:
        
            if result.boxes:
                boxes = result.boxes
        
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    x1 = int((x1 * constants.WIN_WIDTH) / constants.CAR_WIDTH_IMAGE)
                    y1 = int((y1 * constants.WIN_HEIGHT) / constants.CAR_HEIGHT_IMAGE)
                    x2 = int((x2 * constants.WIN_WIDTH) / constants.CAR_WIDTH_IMAGE)
                    y2 = int((y2 * constants.WIN_HEIGHT) / constants.CAR_HEIGHT_IMAGE)
                    centerx = (x1+x2)//2
                    centery = (y1+y2)//2
                    data.append((centerx,centery))

        return data
    

