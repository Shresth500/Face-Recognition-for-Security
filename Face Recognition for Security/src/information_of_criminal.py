"""
This file contains function that will deal with the "Information of a Criminal" feature.
After you fill the form on the website,
information_of_criminal() is called which writes a text file containing all the information of the criminal
and saves the picture of the criminal with <the name of the criminal>.jpg file name
"""

import os

from flask import request, render_template

from flask import current_app

from . import app

from src import constants

from werkzeug.utils import secure_filename


@app.route('/Information/', methods=['POST', 'GET'])
def information_of_criminal():

    # After the form has been submitted
    if request.method == 'POST':

        # Take the input given in the form
        name = request.form.get('Name')
        country = request.form.get('Country')
        height = request.form.get('Height')
        weight = request.form.get('Weight')
        age = request.form.get('Age')
        crime = request.form.get('Crime')
        photo = request.files['Photo']

        # Make the photo name
        #photo.filename = name + ".jpg"

        # Open the file in which you want to save the criminal's details
        file = open('src/static/'+name+".txt", "w")

        # Write in the file
        file.write(
            'f name - {name} \n Country - {Country} \n height - {height} \n weight - {weight} \n age - {age} \n Crime '
            '- {Crime}'.format(
                name=name, Country=country, height=height, weight=weight, age=age, Crime=crime))

        # Close te file
        file.close()

        # Save the picture
        photo.filename=name+".jpg"
        photoname=secure_filename(photo.filename)
        photo.save(constants.CRIMINAL_RECORDS_PATH+photoname)

        return render_template("Index.html", message="FILE UPLOADED SUCCESSFULLY", photo=photo)

    return render_template('Information.html')
