"""
This file contains function that will deal with the "Find a criminal in your livestream" feature.
It turns the webcam on and generates a response for each frame using webcam() and webcam1().
It captures the video and carries out face recognition operations on each frame from the live video
and produces an output using gen_frames()
"""


import os

from flask import render_template, Response
from werkzeug.utils import secure_filename, redirect

from flask import current_app

from . import app

import cv2 as cv

import face_recognition

import numpy as np

from src import constants

from src import generic

# To open the webcam
@app.route('/Webcam/')
def webcam():
    return render_template("Webcam.html")

# To generate a response
@app.route('/Webcam1')
def webcam1():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen_frames():

    # Capturing the video using webcam
    capture_device = cv.VideoCapture(0, cv.CAP_DSHOW)

    # A loop to go through all the frames of the video until the camera is on
    while True:

        # Read a frame, i.e., one image of the video
        success, frame = capture_device.read()

        # If the frame has not been successfully read
        if not success:
            break

        else:
            img = cv.resize(frame, (0, 0), None, 0.25, 0.25)

            # Get the face location of the frame
            face = face_recognition.face_locations(img)

            # Get the face encodings of the frame
            encode_face = face_recognition.face_encodings(img, face)

            # Get the criminal names and face encodings from our criminal records
            criminal_names = generic.get_criminal_names()
            encodings = generic.find_encodings()

            # For the fac encodings found for the frame
            for encode, faceLoc in zip(encode_face, face):

                # Compare it with the face encodings of the criminals
                matches = face_recognition.compare_faces(encodings, encode, tolerance=0.5555)
                facsdis = face_recognition.face_distance(encodings, encode)

                # Get the index of the criminal with minimum Euclidean distance
                match_index = np.argmin(facsdis)

                # If there is a match
                if matches[match_index]:

                    # Get the name of the criminal
                    name = criminal_names[match_index]

                    # Get the face locations
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

                    # Print a red rectangle along with the name of the criminal around the face
                    cv.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), thickness=2)
                    cv.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv.FILLED)
                    cv.putText(frame, name, (x1 + 12, y2), cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    cv.putText(frame, "Criminal detected", (0, 0), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))

                else:
                    # Get the face location
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 5, x2 * 5, y2 * 5, x1 * 5

                    # Print a green rectangle around the frame and say "Not a criminal"
                    cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), thickness=2)
                    cv.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv.FILLED)
                    cv.putText(frame, constants.NOT_A_CRIMINAL, (x1 + 12, y2), cv.FONT_HERSHEY_COMPLEX, 1,
                               (255, 255, 255), 2)

            # yielding the frame
            success, buffer = cv.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
