"""
This file contains function that deals with "Find suspect in your video" feature. 
It takes the input video and processes it frame by frame and performs face recognition
operations to identify the suspect using Suspect1()
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


@app.route('/Suspect1/',methods=['GET','POST'])
def Suspect1():

    # Checking whether the video and photo is being posted or not
    if request.method=='POST':
        photo=request.files['photo']
        print(photo)

        # Saving the Suspect image
        filename1 = secure_filename(photo.filename)
        photo.save(constants.SUSPECT_RECORDS_PATH + filename1)

        # Getting the image of the Suspect
        img=face_recognition.load_image_file(constants.SUSPECT_RECORDS_PATH + filename1)
        img=cv.cvtColor(img,cv.COLOR_BGR2RGB)

        # Getting the face encodings of the Suspect
        face1=face_recognition.face_locations(img)[0]
        encode_face1=face_recognition.face_encodings(img)[0]

        # Getting the video in which suspect will be searched 
        video=request.files['video']
        
        # Saving the Video in which suspect will be searched
        filename = secure_filename(video.filename)
        new_filename="new"+filename
        video.save(constants.SUSPECT_RECORDS_PATH + filename)

        # Capture the video in the required format
        cap = cv.VideoCapture(constants.SUSPECT_RECORDS_PATH + filename)
        frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        fps=int(cap.get(cv.CAP_PROP_FPS))
        fourcc=cv.VideoWriter_fourcc(*'h264')

        # Create a video writer object to save the processed video
        result=cv.VideoWriter(constants.SUSPECT_RECORDS_PATH + new_filename,fourcc,fps,(frame_width,frame_height))

        # This loop goes on for all the frames of the video
        while True:

            # Read a frame 
            success,frame=cap.read()

            # If it was not successful
            if not success:
                break

            # If we could read a frame successfully
            else:

                # Get the face location and encodings
                face=face_recognition.face_locations(frame)
                encode_face=face_recognition.face_encodings(frame,face)
    
                for encode,faceLoc in zip(encode_face,face):

                    # Comparing the face with Criminals
                    matches=face_recognition.compare_faces([encode_face1],encode,tolerance=0.555)
                    facsdis=face_recognition.face_distance([encode_face1],encode)
                    matchIndex=np.argmin(facsdis)

                    # If we get a match
                    if matches[matchIndex]:

                        # Printing the red rectangle along with text "Suspect"
                        y1,x2,y2,x1=faceLoc
                        frame=cv.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),thickness=2)
                        frame=cv.rectangle(frame,(x1,y2-35),(x2,y2),(0,0,255),cv.FILLED)
                        frame=cv.putText(frame,"Suspect detected",(x1+12,y2),cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                    else:

                        # Printing the green rectangle along with the text Suspect not founded
                        y1,x2,y2,x1=faceLoc
                        frame=cv.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),thickness=2)
                        frame=cv.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv.FILLED)
                        frame=cv.putText(frame,"Suspect not found",(x1+12,y2),cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),2) 
                
                # Saving the frame
                result.write(frame)

        cap.release()
        result.release()
        return render_template('Example2.html',message="VIDEO SUCCESSFULLY UPLOADED",filename=new_filename)

    return render_template('Suspect1.html')