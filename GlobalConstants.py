from typing import List, Dict, Tuple
class Constants():

    def __init__(self, win_width=2500, win_height=1400):
        self.CAR_AI_MODEL_FILE = "ai_models/car_ai.pt"
        self.WHITE = (255, 255, 255)
        self.RED = (200, 0, 0)
        self.BRIGHT_RED = (255, 50, 50)
        self.GREEN = (0, 200, 0)
        self.WIN_WIDTH = win_width 
        self.WIN_HEIGHT = win_height
        self.FONTSIZE = int(60*(self.WIN_WIDTH/2500))
        self.bottonX = int(20*(self.WIN_WIDTH/2500))
        self.tenY = int(10*(self.WIN_HEIGHT/1400))
        self.bottonY = int(15*(self.WIN_HEIGHT/1400))
        self.original_carX = int(750*(self.WIN_WIDTH/2500))
        self.original_carY = int(450*(self.WIN_HEIGHT/1400))
        self.CAR_WIDTH_IMAGE = int(640*(self.WIN_WIDTH/2500))
        self.CAR_HEIGHT_IMAGE = int(360*(self.WIN_HEIGHT/1400))
        self.X1 = int(1762*(self.WIN_WIDTH/2500))
        self.Y1 = int(841*(self.WIN_HEIGHT/1400))
        self.X2 = int(1850*(self.WIN_WIDTH/2500))
        self.Y2 = int(1059*(self.WIN_HEIGHT/1400))
        self.Z1 = int(1341*(self.WIN_WIDTH/2500))
        self.W1 = int(1101*(self.WIN_HEIGHT/1400))
        self.Z2 = int(1429*(self.WIN_WIDTH/2500))
        self.W2 = int(1319*(self.WIN_HEIGHT/1400))
        self.SX1 = int(1750*(self.WIN_WIDTH/2500))
        self.SY1 = int(1108*(self.WIN_HEIGHT/1400))
        self.SX2 = int(1852*(self.WIN_WIDTH/2500))
        self.SY2 = int(1217*(self.WIN_HEIGHT/1400))
        self.SSX1 = int(1341*(self.WIN_WIDTH/2500))
        self.SSY1 = int(925*(self.WIN_HEIGHT/1400))
        self.SSX2 = int(1443*(self.WIN_WIDTH/2500))
        self.SSY2 = int(1034*(self.WIN_HEIGHT/1400))
        self.x = int(200*(self.WIN_WIDTH/2500))
        self.y = int(1280*(self.WIN_HEIGHT/1400))
        self.VELOCITY = int((self.WIN_HEIGHT+self.WIN_WIDTH)/390)
        self.ANGLE = 180
        self.CAR_COORDINATES = (int(936*(self.WIN_WIDTH/2500)),int(49*(self.WIN_HEIGHT/1400)),int(487*(self.WIN_WIDTH/2500)),int(124*(self.WIN_HEIGHT/1400)))
        self.LICENSE1_COORDINATES = (int(2038*(self.WIN_WIDTH/2500)),int(1227*(self.WIN_HEIGHT/1400)),int(399*(self.WIN_WIDTH/2500)),int(120*(self.WIN_HEIGHT/1400)))
        self.LICENSE2_COORDINATES = (int(2040*(self.WIN_WIDTH/2500)),int(1090*(self.WIN_HEIGHT/1400)),int(398*(self.WIN_WIDTH/2500)),int(119*(self.WIN_HEIGHT/1400)))
        self.exit_botton_coordinates = (int(2300*(self.WIN_WIDTH/2500)), int(40*(self.WIN_HEIGHT/1400)), int(150*(self.WIN_WIDTH/2500)), int(70*(self.WIN_HEIGHT/1400)))
        self.parking: Dict[str, List[int]] = {
            'A8': [37, 30, 463, 200, 1, 426, 170],
            'A3': [36, 200, 465, 368, 1, 429, 168],
            'B2': [33, 369, 466, 544, 1, 433, 175],
            'C2': [35, 545, 468, 713, 1, 433, 168],
            'D2': [36, 713, 471, 883, 1, 435, 170],
            'E1': [35, 882, 475, 1063, 1, 440, 181],
            'A1': [798, 192, 1218, 362, 1, 420, 170],
            'A5': [800, 362, 1220, 544, 1, 420, 182],
            'B3': [801, 543, 1220, 707, 1, 419, 164],
            'C3': [802, 706, 1220, 880, 1, 418, 174],
            'A2': [1220, 192, 1633, 363, 1, 413, 171],
            'A6': [1218, 362, 1635, 543, 1, 417, 181],
            'B4': [1221, 544, 1636, 711, 1, 415, 167],
            'C4': [1218, 708, 1636, 882, 1, 418, 174],
            'A7': [2007, 30, 2465, 194, 1, 458, 164],
            'A4': [2007, 192, 2465, 360, 1, 458, 168],
            'B1': [2008, 359, 2466, 539, 1, 458, 180],
            'C1': [2007, 538, 2466, 707, 1, 459, 169],
            'D1': [2008, 707, 2465, 882, 1, 457, 175],
            'E2': [2007, 882, 2466, 1056, 1, 459, 174]
        }

    def activate_parking(self):
        for key in self.parking:
            for i in range(7):
                if i == 0 or i == 2 or i == 5:
                    self.parking[key][i] = int(self.parking[key][i]*(self.WIN_WIDTH/2500))
                elif i == 1 or i == 3 or i == 6: 
                    self.parking[key][i] = int(self.parking[key][i]*(self.WIN_HEIGHT/1400))