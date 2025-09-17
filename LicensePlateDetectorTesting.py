from LicensePlateDetector import LicensePlateDetector
import numpy as np
import cv2
import pytesseract
import mysql.connector
import cvzone
from ultralytics import YOLO
import matplotlib.pyplot as plt


model_file = "ai_models/license_ai.pt"
license_plate = "source/car_license_plate.png"

def setup():
    try:
        instance = LicensePlateDetector(model_file)
        print("Test 1 success")
    except Exception as e:
        print(f"Fail: \n {e}")


def TestOpenConnection():
    instance = LicensePlateDetector(model_file)
    try:
        result = instance.openConnection(user="parking_user", passw="parking_user")
        if result:
            print("Test 2 success")
        else:
            print("Fail")
            print(result)
    except Exception as e:
        print(f"Fail: \n {e}")


def TestDetectPlate():
    instance = LicensePlateDetector(model_file)
    image = cv2.imread(license_plate)
    image = cv2.resize(image, (640, 640))
    try:
        result = instance.detect_plate(image)
        print("Test 3 success")
        print(result)
    except Exception as e:
        print(f"Fail: \n {e}")


def TestDetectText():
    instance = LicensePlateDetector(model_file)
    image = cv2.imread(license_plate)
    image = cv2.resize(image, (640, 640))
    try:
        result = instance.detect_text(image)
        print("Test 4 success")
        print(result)
    except Exception as e:
        print(f"Fail: \n {e}")


def TestDetectText():
    instance = LicensePlateDetector(model_file)
    image = cv2.imread(license_plate)
    image = cv2.resize(image, (640, 640))
    try:
        result = instance.detect_text(image)
        print("Test 4 success")
        print(result)
    except Exception as e:
        print(f"Fail: \n {e}")


def TestCarIn():
    instance = LicensePlateDetector(model_file)
    image = cv2.imread(license_plate)
    image = cv2.resize(image, (640, 640))
    try:
        instance.openConnection(user="parking_user", passw="parking_user")
        result = instance.detect_text(image)
        entered = instance.car_in(result)
        if entered:
            print("Test 5 success")
        else:
            print("Fail")
        instance.closeConnection()
    except Exception as e:
        print(f"Fail: \n {e}")


def TestCarOut():
    instance = LicensePlateDetector(model_file)
    image = cv2.imread(license_plate)
    image = cv2.resize(image, (640, 640))
    try:
        instance.openConnection(user="parking_user", passw="parking_user")
        result = instance.detect_text(image)
        entered = instance.car_out(result)
        if entered:
            print("Test 6 success")
        else:
            print("Fail")
        instance.closeConnection()
    except Exception as e:
        print(f"Fail: \n {e}")

def main():
    # setup()
    # TestOpenConnection()
    # TestDetectPlate()
    # TestDetectText()
    # TestCarIn()
    # TestCarOut()
    cap = cv2.VideoCapture(0)
    instance = LicensePlateDetector(model_file)

    while True:
        success, frame = cap.read()
        frame = cv2.resize(frame, (1366, 768)) 
        if success:
            results = instance.detect_text(frame)
            if results:
                x1,x2,y1,y2,license,text = results[0]
                cvzone.cornerRect(frame, (x1,y1,x2-x1,y2-y1))
                cvzone.putTextRect(frame, text, (x1,y1-20))
        cv2.imshow("Image", frame)
        
        cv2.waitKey(1)

if __name__ == "__main__":
    main()