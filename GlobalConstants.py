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
    Z1 = 1341
    W1 = 1101
    Z2 = 1429
    W2 = 1319

    SX1 = 1750
    SY1 = 1108
    SX2 = 1852
    SY2 = 1217

    SSX1 = 1341
    SSY1 = 905
    SSX2 = 1443
    SSY2 = 1014

    FERRARI_XMIN = 251
    FERRARI_YMIN = 108
    FERRARI_XMAX = 626
    FERRARI_YMAX = 357
    VELOCITY = 10
    ANGLE = 180  
    CAR_COORDINATES = (936,49,487,124)
    LICENSE1_COORDINATES = (2038,1227,399,120)
    LICENSE2_COORDINATES = (2040,1090,398,119)