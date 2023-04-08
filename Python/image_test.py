import cv2
import numpy as np
import time
import random


# print out all clicks
def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Left button clicked")
        print("x: ", x, "y: ", y)


# Start video capture
cap = cv2.VideoCapture(0)
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Crop the image
    cropped_number = gray[10:480, 775:1415]
    # Rotate cropped 90 degrees
    cropped_number = cv2.rotate(cropped_number, cv2.ROTATE_90_COUNTERCLOCKWISE)

    cropped_shape = gray[10:480, 350:850]
    # Rotate cropped_shape 90 degrees
    cropped_shape = cv2.rotate(cropped_shape, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # Display the resulting frame
    cv2.imshow('frame', gray)
    cv2.imshow('cropped_number', cropped_number)
    cv2.imshow('cropped_shape', cropped_shape)
    cv2.setMouseCallback("frame", click_event)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break