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