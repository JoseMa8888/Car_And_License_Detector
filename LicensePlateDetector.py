import cv2
import easyocr
import mysql.connector 
from datetime import timedelta
import datetime


class LicensePlateDetector():
    def __init__(self):
        self.__host: str = "localhost"
        self.__port: int = 3306
        self.__db: str = "parking_lot"
        self.__parking_id = 1
        self.__conn = None
        self.__ocr_reader = easyocr.Reader(['es'])
        self.__enter = True 

    def openConnection(self, user, passw):
        try:
            if self.__conn is not None and self.__conn.is_connected():
                return False
            self.__conn = mysql.connector.connect(
                host=self.__host,
                port=self.__port,
                database=self.__db,
                user=user,
                password=passw
            )
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")


    def get_license_plate(self, frame, enter=True):
        """
        params:
            frame: capture of a video frame.
        This method gets the text from a frame. The frame must be a slice of the image which 
        contais the license plate
        return:
            The result is the license plate text and the image of it 
        """
        if enter:
            license_frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        else:
            license_frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        results = self.__ocr_reader.readtext(license_frame)
        license_text = ""
        for (bbox, text, prob) in results:
            license_text += text
        if len(license_text)==7:
            return license_text, license_frame
        return None, None


    def car_in(self, data):
        """
        params:
            data: must like [[x1,x2,y1,y2,license,text.strip()]]
        This method stores the data gotten from detect_text into a mysql database.
        return:
            True if nothing bad happens, otherwise it's False
        """
        try:
            if data:
                for dt in data:
                    query = """
                    SELECT COUNT(*) AS total
                    FROM car
                    WHERE license=%s
                    """
                    cursor = self.__conn.cursor()
                    foto,lic = dt[4], dt[5]
                    foto = foto.tobytes()
                    cursor.execute(query, (lic,))
                    results = cursor.fetchall()
                    if results[0][0] == 0:
                        print("The license is not in the database")
                        cursor = self.__conn.cursor()
                        query1 = """
                        INSERT INTO car (license, foto) VALUES (%s, %s)
                        """ 
                        cursor.execute(query1, (lic, foto))
                        self.__conn.commit()
                    else:
                        print("The car is in the database")

                    query2 = """
                    UPDATE parking SET n_empty_spots=n_empty_spots-1 WHERE id = %s
                    """
                    cursor.execute(query2, (self.__parking_id,))
                    self.__conn.commit()

                    query3 = """
                    INSERT INTO enter (car_license, parking_id, time_in, time_out) VALUES (%s, %s, %s, %s)
                    """
                    now = datetime.datetime.now()
                    cursor.execute(query3, (lic, self.__parking_id, now, now+timedelta(minutes=5)))
                    self.__conn.commit()
                return True
            return False
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
            

    def car_out(self, data):
        """
        params:
            data: must like [[x1,x2,y1,y2,license,text.strip()]]
        This method updates parking to remove the existing car.
        return:
            True if nothing bad happens, otherwise it's False
        """
        try:
            if data:
                for dt in data:
                    query = """
                    SELECT COUNT(*) AS total
                    FROM car
                    WHERE license=%s
                    """
                    cursor = self.__conn.cursor()
                    lic = dt[4]
                    cursor.execute(query, (lic,))
                    results = cursor.fetchall()
                    if len(results) == 0:
                        print("The system does not have your license")
                        return False
                    
                    query2 = """
                    SELECT time_out FROM enter WHERE car_license=%s
                    """
                    cursor.execute(query2, (lic,))
                    results = cursor.fetchall()
                    maximum_datetime = max(results)
                    now = datetime.datetime.now()
                    print(maximum_datetime[0], now)
                    if maximum_datetime[0] > now:
                        query3 = """
                        UPDATE parking SET n_empty_spots=n_empty_spots+1 WHERE id = %s
                        """
                        cursor.execute(query3, (self.__parking_id,))
                        self.__conn.commit()
                        return True
                    else:
                        print("You have to pay for your extra time")
                        return False
            return False
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False


    def in_or_out(self, activation=True):
        """
        params:
            activation: boolean
        This method activates or deactivates the enter mode.
        return:
            True if nothing bad happens, otherwise it's False
        """
        self.__enter = activation


    def execute_system(self, frame):
        """
        params:
            activation: boolean
        This method activates or deactivates the enter mode.
        return:
            True if nothing bad happens, otherwise it's False
        """
        data = self.detect_text(frame)
        if self.__enter:
            self.car_in(data)
        else:
            self.car_out(data)


    def closeConnection(self):
        try:
            if self.__conn and self.__conn.is_connected():
                self.__conn.close()
                print("Connection closed success")
                return True
            else:
                return False
        except mysql.connector.Error as e:
            print(e)
            return False
        
        

