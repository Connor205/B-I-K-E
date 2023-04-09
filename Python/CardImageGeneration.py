import cv2
import numpy as np
from Shuffler import Shuffler
import pathlib
import time

# Start video capture
cap = cv2.VideoCapture(0)

# Lets create the folder to hold the unlabled images
pathlib.Path('unlabled_images').mkdir(parents=True, exist_ok=True)

# Get the serial port from the user
port = input("Enter the port for the shuffler: ")

# Now lets make a shuffler
shuffler = Shuffler(port)
shuffler.waitForReady()

# Now we can do it in batches of 52 (ie whole deck)

while True:
    # Get a confirmation from the user
    input("Press enter to start the next batch")

    # Now we can dispense 52 cards
    for i in range(52):
        print("Taking image {}".format(i))
        # Wait for the shuffler to be ready
        shuffler.waitForReady()
        # Now we want to take a photo and identify the card
        # Read the image from the camera
        ret, frame = cap.read()
        # Convert the image to grayscale
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

        cropped_suit = result[450:725, 750:1050]

        # resize to 100 by 100
        cropped_suit = cv2.resize(cropped_suit, (100, 100))

        cv2.imwrite(
            "unlabled_images/{}_suit_{}.png".format(i, str(time.time())),
            cropped_suit)
        cv2.imwrite(
            "unlabled_images/{}_number_{}.png".format(i, str(time.time())),
            cropped_number)
        cv2.imwrite(
            "unlabled_images/{}_full_{}.png".format(i, str(time.time())),
            result)

        cv2.imshow('cropped_number', cropped_number)
        cv2.imshow('cropped_suit', cropped_suit)
        cv2.imshow('frame', result)
        cv2.waitKey(1)

        # Then we drop the card
        shuffler.dispense()
        time.sleep(0.5)
