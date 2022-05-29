import face_recognition
import cv2 as cv

import os

from src import constants


# Function to return the criminal names
def get_criminal_names():
    criminal_names = []

    # Get the file names of the criminal pictures which contains the criminal names
    list_of_criminals = os.listdir(constants.CRIMINAL_RECORDS_PATH)
    list_of_criminals.sort()

    # Iterate through the list
    for criminal in list_of_criminals:

        # Extract the name and append it to the list
        criminal_names.append(os.path.splitext(criminal)[0])

    return criminal_names

# Function to return face encodings of criminals
def find_encodings():

    encodings = []
    images = []

    # Get a list of file names for criminal photos
    list_of_criminals = os.listdir(constants.CRIMINAL_RECORDS_PATH)
    list_of_criminals.sort()

    # Iterate through the list
    for criminal in list_of_criminals:

        # Take the input image and append it to the list
        images.append(cv.imread(f'{constants.CRIMINAL_RECORDS_PATH}/{criminal}'))

    # Iterate through the list of images
    for img in images:

        # Convert to the correct color channel
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        # Get the face encoding
        encode = face_recognition.face_encodings(img)[0]

        # Append it to the list
        encodings.append(encode)
    

    return encodings
