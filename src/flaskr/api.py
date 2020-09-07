import functools
import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from flask_api import status

from server import get_song
from server import create_song

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/songs', methods=('POST',))
def post_songs():
    error = ""
    required = ["author", "date","name","filename"]
    for x in required:
        if x not in request.values:
            error += "{} is required. ".format(x)
    
    if error != "":
        return error, status.HTTP_400_BAD_REQUEST

    try:
        create_song.insert_song(request.values["name"],request.values["filename"], 
            request.values["author"],
            datetime.datetime.strptime(request.values["date"],"%Y-%m-%d") )
        return "ok"
    except Exception as e:
        return "error: {}".format(str(e)), status.HTTP_500_INTERNAL_SERVER_ERROR