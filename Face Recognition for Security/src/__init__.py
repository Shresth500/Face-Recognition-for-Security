from flask import Flask

from . import constants

app = Flask(__name__, template_folder='template',static_folder='static')
app.config[constants.CRIMINAL_RECORDS_PATH] = constants.CRIMINAL_RECORDS_PATH
app.config[constants.SUSPECT_RECORDS_PATH] = constants.SUSPECT_RECORDS_PATH


from . import home

from . import know_your_suspect

from . import information_of_criminal

from . import find_criminals_in_video

from . import find_criminals_in_livestream

from . import find_your_suspect_in_video

from . import find_your_suspect_in_livestream