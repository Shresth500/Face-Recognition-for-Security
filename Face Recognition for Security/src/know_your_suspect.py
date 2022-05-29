"""
This file contains function that will deal with the "Know your suspect" feature.
After you give an input on the website,
know_your_suspect() is called which performs the face recognition operation and
saves a processed image with a green box around the face,
if the suspect is not present in the criminal records
else a red box with the criminal's name.
This processed image is then shown using display_image()
"""


import os

from flask import request, render_template, url_for

from werkzeug.utils import secure_filename, redirect

from flask import current_app

from . import app

import cv2 as cv

import face_recognition

import numpy as np

from src import constants

from src import generic



@app.route('/Images/', methods=['POST', 'GET'])
def know_your_suspect():

    # After the photo submission
    if request.method == 'POST':

        # Take the photo as input and save it
        photo = request.files['photo']
        filename = secure_filename(photo.filename)
        photo.save(constants.SUSPECT_RECORDS_PATH + filename)

        # Create a new file name for the processed image
        new_filename = constants.NEW + filename

        # Take the input image in the desired format and convert to the correct color channel
        img = face_recognition.load_image_file(constants.SUSPECT_RECORDS_PATH + filename)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        # Get the face location and encodings for our input image
        face = face_recognition.face_locations(img)[0]
        encode_face = face_recognition.face_encodings(img)[0]

        # Get the criminal names and face encodings from our criminal records
        criminal_names = generic.get_criminal_names()
        encodings = generic.find_encodings()

        # Compare the face encodings of our criminals with the input image
        matches = face_recognition.compare_faces(encodings, encode_face, tolerance=0.5555)
        face_dis = face_recognition.face_distance(encodings, encode_face)

        # Take the index of the criminal with te minimum face distance
        # This is because the face with the minimum Euclidean distance will have the highest chance of matching
        # So we don't have to check for all the criminals
        match_index = np.argmin(face_dis)

        # If the criminal matches with the suspect
        if matches[match_index]:

            # Get the criminal name
            name = criminal_names[match_index]

            # Get the face location of the suspect
            y1, x2, y2, x1 = face

            # Create a red rectangle around the suspects name and print the criminal name with it
            img = cv.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), thickness=2)
            img = cv.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv.FILLED)
            img = cv.putText(img, name, (x1 + 12, y2), cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        # If the criminal doesn't match the suspect
        else:

            # Get the face location of the suspect
            y1, x2, y2, x1 = face

            # Make a green rectangle around the suspects face
            # And write "Criminal not found"
            img = cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), thickness=2)
            img = cv.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv.FILLED)
            img = cv.putText(img, constants.NOT_A_CRIMINAL, (x1 + 12, y2), cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255),
                             2)

        # Save the processed image
        cv.imwrite(constants.SUSPECT_RECORDS_PATH + new_filename ,img)
        print(os.getcwd())
        print()

        return render_template('ShowImage.html', message="IMAGE SUCCESSFULLY UPLOADED", filename=new_filename)

    return render_template('Images.html')

# Function helps to show the processed image
@app.route('/display_image/<filename>')
def display_image(filename):
    print("function called")
    return redirect(url_for('static', filename=constants.SUSPECT_RECORDS + filename), code=301)
