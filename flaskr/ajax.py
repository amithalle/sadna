import functools
import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from flask_api import status

import get_song
import create_song

bp = Blueprint('ajax', __name__, url_prefix='/ajax')


@bp.route('/songs', methods=('GET',))
def get_songs():
    if "author" in request.args:
        data = get_song.get_songs_by_author(request.args["author"])
    elif "name" in request.args:
        data = get_song.get_songs_by_name(request.args["name"])
    elif "start_date" in request.args and "end_date" in request.args:
        start, end = (request.args["start_date"], request.args["end_date"])
        start, end = (datetime.datetime.strptime(start,"%d/%m/%Y"), 
            datetime.datetime.strptime(end,"%d/%m/%Y"))
        data = get_song.get_songs_by_date_range(start , end)
    else:
        print ("getting all")
        data = get_song.get_all_songs()
    return render_template("ajax/songs.html", songs=data)