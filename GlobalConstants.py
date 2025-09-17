from dataclasses import dataclass


@dataclass(frozen=True)
class Constants:
    CAR_AI_MODEL_FILE = "ai_models/car_ai.pt"
    CAR_WIDTH_IMAGE = 640
    CAR_HEIGHT_IMAGE = 360
    WIN_WIDTH = 2500
    WIN_HEIGHT = 1400
    WHITE = (255, 255, 255)
    RED = (200, 0, 0)
    BRIGHT_RED = (255, 50, 50)
    GREEN = (0, 200, 0)
    X1 = 1762 
    Y1 = 841
    X2 = 1850
    Y2 = 1059
    FERRARI_XMIN = 251
    FERRARI_YMIN = 108
    FERRARI_XMAX = 626
    FERRARI_YMAX = 357
    VELOCITY = 10
    ANGLE = 180  