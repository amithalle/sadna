import functools
import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from flask_api import status

from server import get_song

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


@bp.route("/song_text", methods=("GET",))
def get_song_text():
    if "song_id" in request.args:
        data = get_song.get_song_text(request.args["song_id"])
        return render_template("ajax/song_text.html", text=data)


@bp.route("/song_form", methods=('GET',))
def get_song_form():
    return render_template("ajax/song_form.html")


@bp.route("/song_search", methods=('GET',))
def get_song_search():
    return render_template("ajax/song_search.html")