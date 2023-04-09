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

    # rotate the image 15 degrees counter clockwise
    image_center = tuple(np.array(frame.shape[1::-1]) / 2)

    rot_mat = cv2.getRotationMatrix2D(image_center, -15 - 90, 1.0)
    result = cv2.warpAffine(gray,
                            rot_mat,
                            frame.shape[1::-1],
                            flags=cv2.INTER_LINEAR)

    # Crop the image
    cropped_number = result[100:475, 750:1050]

    # resize to 100 by 100
    cropped_number = cv2.resize(cropped_number, (100, 100))

    print(cropped_number.shape)

    cropped_suit = result[450:725, 750:1050]

    # resize to 100 by 100
    cropped_suit = cv2.resize(cropped_suit, (100, 100))

    # cropped_shape = gray[10:480, 350:850]
    # # Rotate cropped_shape 90 degrees
    # cropped_shape = cv2.rotate(cropped_shape, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # Display the resulting frame
    cv2.imshow('frame', result)
    cv2.imshow('cropped_number', cropped_number)
    cv2.imshow('cropped_suit', cropped_suit)
    cv2.setMouseCallback("frame", click_event)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break