import cv2
import numpy as np
import time
import random
import os
import pathlib

UNLABELED_DIRECTORY = "unlabeled_images"

# Get a list of all of the files in the directory using pathlib
path = pathlib.Path(UNLABELED_DIRECTORY)

# Get a list of all of the files in the directory
files = list(path.glob("*.png"))

# Now lets filter the list to only include the suit images
suit_files = [x for x in files if "suit" in x.name]

# Now lets filter the list to only include the number images
number_files = [x for x in files if "number" in x.name]

# Now lets sort the files by the time they were created
suit_files.sort(key=lambda x: x.stat().st_ctime)
number_files.sort(key=lambda x: x.stat().st_ctime)

# Lets print out some information about the files
print("There are {} suit files and {} number files".format(
    len(suit_files), len(number_files)))

# Now lets create the folder to hold the labeled images

pathlib.Path('labeled_images').mkdir(parents=True, exist_ok=True)

# Now lets create a list of all of the suits
suits = ["clubs", "diamonds", "hearts", "spades"]

# Now lets create a list of all of the numbers
numbers = [
    "ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen",
    "king"
]

# So we have all of the classes
# We can create a dictionary to map the classes to keys
class_to_key = {
    "clubs": "c",
    "diamonds": "d",
    "hearts": "h",
    "spades": "s",
    "ace": "a",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "10": "1",
    "jack": "j",
    "queen": "q",
    "king": "k"
}

# Make sure that there are no duplicate keys
assert len(class_to_key) == len(set(class_to_key.values()))

# Now we can create a dictionary to map the keys to classes
key_to_class = {ord(v): k for k, v in class_to_key.items()}

# Then we can create a directory for each class inside of the labled images
# directory
for key in class_to_key.keys():
    pathlib.Path('labeled_images/{}'.format(key)).mkdir(parents=True,
                                                        exist_ok=True)

# Now we can loop through the files and move them to the correct directory
# We can do the suits first

for suit_file in suit_files:
    # Get the name of the file
    file_name = suit_file.name

    # Display the file to the user using cv2
    image = cv2.imread(str(suit_file))
    cv2.imshow("Suit Image", image)

    # Wait for the user to press a key
    key = cv2.waitKey(0)

    # get the class from the key
    class_name = key_to_class[key]

    # Get the new file name
    new_file_name = "{}_{}".format(class_name, file_name)

    # Move the file
    os.rename(suit_file, "labeled_images/{}/{}".format(class_name,
                                                       new_file_name))

# Now we can do the numbers
for number_file in number_files:
    # Get the name of the file
    file_name = number_file.name

    # Display the file to the user using cv2
    image = cv2.imread(str(number_file))
    cv2.imshow("Number Image", image)

    # Wait for the user to press a key
    key = cv2.waitKey(0)

    # get the class from the key
    class_name = key_to_class[key]

    # Get the new file name
    new_file_name = "{}_{}".format(class_name, file_name)

    # Move the file
    os.rename(number_file,
              "labeled_images/{}/{}".format(class_name, new_file_name))
