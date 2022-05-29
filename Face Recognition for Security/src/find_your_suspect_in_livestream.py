"""
This file contains function that will deal with the "Find suspect in your livestream" feature.
It turns the webcam on and generates a response for each frame using webcam2().
It captures the video and carries out face recognition operations on each frame from the live video
and produces an output using frames()
"""

import os

from flask import request, render_template, url_for,Response

from werkzeug.utils import secure_filename, redirect

from flask import current_app

from . import app

import cv2 as cv

import face_recognition

import numpy as np

from src import constants

from src import generic


@app.route('/Suspect2/',methods=['GET','POST'])
def Suspect2():

    # Checking whether the image has been posted or not
    if request.method=='POST':

        # Getting the image input and saving it
        photo=request.files['photo']
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config[constants.SUSPECT_RECORDS_PATH], "xyz.jpeg"))

        return render_template('Example3.html')

    return render_template('Suspect2.html')

def frames():

    # Taking the image input and converting it into required Color channel
    img=face_recognition.load_image_file(os.path.join(app.config[constants.SUSPECT_RECORDS_PATH], "xyz.jpeg"))
    img=cv.cvtColor(img,cv.COLOR_BGR2RGB)

    # Getting the face location and encodings
    face=face_recognition.face_locations(img)[0]
    encode_face1=face_recognition.face_encodings(img)[0] 

    # Capturing the video from web cam 
    captureDevice = cv.VideoCapture(0, cv.CAP_DSHOW)

    # Loop goes on until the camera is on
    while True:

        # Read a frame
        success,frame=captureDevice.read()

        # If not successfull
        if not success:
            break

        # If successful
        else:

            # Getting the face location and encodings of the frame
            imgS=cv.resize(frame,(0,0),None,0.25,0.25)
            face=face_recognition.face_locations(imgS)
            encode_face=face_recognition.face_encodings(imgS,face)

            for encode,faceLoc in zip(encode_face,face):

                # Matching and Comparing faces
                matches=face_recognition.compare_faces([encode_face1],encode,tolerance=0.5555)
                facsdis=face_recognition.face_distance([encode_face1],encode)
                matchIndex=np.argmin(facsdis)
                
                # If a match is found print a red rectangle around the suspect's face in the frame
                if matches[matchIndex]:
                    y1,x2,y2,x1=faceLoc
                    y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
                    cv.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),thickness=2)
                    cv.rectangle(frame,(x1,y2-35),(x2,y2),(0,0,255),cv.FILLED)
                    cv.putText(frame,"Suspect",(x1+12,y2),cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                
                # Else print a green rectangle around the face
                else:
                    y1,x2,y2,x1=faceLoc
                    y1,x2,y2,x1=y1*5,x2*5,y2*5,x1*5
                    cv.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),thickness=2)
                    cv.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv.FILLED)
                    cv.putText(frame,"Suspect not found",(x1+12,y2),cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

            
            # Converting the encoding to jpg and then to bytes 
            success, buffer = cv.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yielding the frames
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/Webcam2')
def Webcam2():

    return Response(frames(), mimetype='multipart/x-mixed-replace; boundary=frame')