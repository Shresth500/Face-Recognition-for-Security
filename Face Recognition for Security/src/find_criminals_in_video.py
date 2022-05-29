"""
This file contains function that deals with the "Find criminals in your video" feature.
It takes the input video and processes it frame by frame and performs face recognition 
operations to identify criminals using find_criminals_in_video()
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


@app.route('/videos/', methods=['POST', 'GET'])
def find_criminals_in_video():

    # After the video submission
    if request.method == 'POST':

        # Take the video as input and save it
        video = request.files['video']
        filename = secure_filename(video.filename)
        video.save(os.path.join(app.config[constants.SUSPECT_RECORDS_PATH], filename))

        # Create a new file name for the processed video
        new_filename = constants.NEW + filename

        encodelist=generic.find_encodings()
        criminal_names = generic.get_criminal_names()

        # Take the input video in the desired format 
        cap = cv.VideoCapture(os.path.join(app.config[constants.SUSPECT_RECORDS_PATH], filename))

        # Getting the features of video capture
        frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        fps=int(cap.get(cv.CAP_PROP_FPS))
        fourcc=cv.VideoWriter_fourcc(*'h264')
        
        # Create a video writer object to save the processed video
        result=cv.VideoWriter(os.path.join(app.config[constants.SUSPECT_RECORDS_PATH], new_filename),fourcc,fps,(frame_width,frame_height))
        
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
                    matches=face_recognition.compare_faces(encodelist,encode,tolerance=0.555)
                    facsdis=face_recognition.face_distance(encodelist,encode)
                    matchIndex=np.argmin(facsdis)

                    # If we get a match
                    if matches[matchIndex]:

                        # Getting the name of the Criminal
                        name=criminal_names[matchIndex]
                        
                        # Get the location of the face
                        y1,x2,y2,x1=faceLoc

                        # Printing the red rectangle along with the name of the Criminal
                        frame=cv.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),thickness=2)
                        frame=cv.rectangle(frame,(x1,y2-35),(x2,y2),(0,0,255),cv.FILLED)
                        frame=cv.putText(frame,name,(x1+12,y2),cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                        frame=cv.putText(frame,"Criminal detected",(0,0),cv.FONT_HERSHEY_COMPLEX,1,(0,255,0))
                    else:

                        # Printing the green rectangle along with the text Criminal not founded
                        y1,x2,y2,x1=faceLoc
                        frame=cv.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),thickness=2)
                        frame=cv.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv.FILLED)
                        frame=cv.putText(frame,"Criminal not determined",(x1+12,y2),cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                
                # Saving the frame
                result.write(frame)

        cap.release()
        result.release()

        return render_template('Example2.html',message="VIDEO SUCCESSFULLY UPLOADED",filename=new_filename)
    
    return render_template('videos.html')

# Function helps to show the processed video
@app.route('/display_video/<filename>')
def display_video(filename):

    return redirect(url_for('static', filename=constants.SUSPECT_RECORDS + filename), code=301)