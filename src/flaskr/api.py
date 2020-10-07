import functools
import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, current_app
)
from flask_api import status
import os
from werkzeug.utils import secure_filename
from server import get_song
from server import create_song

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/songs', methods=('POST',))
def post_songs():
    error = ""
    required = ["author", "date", "name"]
    for x in required:
        if x not in request.values:
            error += "{} is required. ".format(x)
    
    if error != "":
        return error, status.HTTP_400_BAD_REQUEST


    try:
        file_path = upload_file(request)
        create_song.insert_song(request.values["name"], file_path, 
            request.values["author"],
            datetime.datetime.strptime(request.values["date"],"%Y-%m-%d") )
        os.unlink(file_path)
        return redirect("/")
    except Exception as e:
        return "error: {}".format(str(e)), status.HTTP_500_INTERNAL_SERVER_ERROR

def upload_file(request):
    # check if the post request has the file part
    if 'filename' not in request.files:
        flash("no file")
        return False
    else:
        file = request.files['filename']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return False
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            full_path= os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(full_path)
            return full_path

@bp.route("/get_song", methods=["GET"])
def get_song_by_field():
    data = None

    if "field" not in request.values:
        return "field is required", status.HTTP_400_BAD_REQUEST
    elif request.values["field"] == 'author':
        if "author"  in request.values:
            data = get_song.get_songs_by_author(request.values["author"])
        else:
            return "author is required", status.HTTP_400_BAD_REQUEST
    elif request.values["field"] == 'name':
        if 'name'  in request.values.keys():
            data = get_song.get_songs_by_name(request.values["name"])
        else:
            return "name is required", status.HTTP_400_BAD_REQUEST
    elif request.values["field"] == 'date':
        if "date_start"  in request.values and "date_end"  in request.values:
            data = get_song.get_songs_by_date_range(request.values["date_start"], request.values["date_end"])
        else:
            return "dates are required", status.HTTP_400_BAD_REQUEST
    elif request.values["field"] == 'word':
        if "word" in request.values.keys():
            sond_ids = get_song.get_song_ids_by_words([request.values["word"]])
            data = get_song.get_songs_by_id(sond_ids)
        else:
            return "word is required", status.HTTP_400_BAD_REQUEST

    else:
        return "{} is invalid for 'field'".format(request.values["field"]), status.HTTP_400_BAD_REQUEST

    if data is not None:
        return render_template("ajax/songs.html", songs=data)
    else:
        return "there was an error somewhere", status.HTTP_500_INTERNAL_SERVER_ERROR

@bp.route("/all_songs", methods=["GET"])
def get_all_songs():
    return jsonify(get_song.get_all_songs())
