import functools
import datetime
import io
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, current_app, send_file
)
from flask_api import status
import os
from werkzeug.utils import secure_filename
from server import get_song
from server import create_song, word_groups, word_relations, phrases, xml_handler

ALLOWED_EXTENSIONS = {'txt', 'xml'}

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
        if (not file_path):
            return "error reading file", status.HTTP_400_BAD_REQUEST
            
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


@bp.route("/word_by_index", methods=["GET"])
def word_by_index():
    word = []
    for val in ["word_index", "line_index","song_id","index_by"]:
        if val not in request.values or request.values[val] is None or request.values[val] == "":
            return val + " is needed", status.HTTP_400_BAD_REQUEST
    
    if request.values["index_by"] == "stanza":
        if "stanza_index" not in request.values:
            return "stanza_index is needed", status.HTTP_400_BAD_REQUEST
        else:
            word = get_song.get_word_by_stanza_index(request.values["song_id"],
                                                     request.values["stanza_index"],
                                                     request.values["line_index"],
                                                     request.values["word_index"])
            
    elif request.values["index_by"] == "global":
            word = get_song.get_word_by_global_index(request.values["song_id"],
                                                request.values["line_index"],
                                                request.values["word_index"])

    else:
        return "unknown index_by option: " + request.values["index_by"], status.HTTP_400_BAD_REQUEST

    if len(word) > 0:
        return jsonify(word[0][0])
    else:
        return "word not found", status.HTTP_400_BAD_REQUEST


@bp.route("/create_group", methods=["POST"])
def create_group():
    if "group_name" not in request.values:
        return "group_name is required", status.HTTP_400_BAD_REQUEST
    elif request.values["group_name"] == "": 
        return "group_name cannot be empty", status.HTTP_400_BAD_REQUEST
    else:
        id = word_groups.create_word_group(request.values["group_name"],[])

        return jsonify(id)

@bp.route("/add_words_to_group", methods=["POST"])
def add_word_to_group():
    if "group_id" not in request.values:
        return "group_id is required", status.HTTP_400_BAD_REQUEST
    
    if "word" not in request.values:
        return "word is required", status.HTTP_400_BAD_REQUEST
    
    if request.values["word"] == "" and len(request.values["words"]) == 0: 
        return "word cannot be empty", status.HTTP_400_BAD_REQUEST
    words_to_add = [request.values["word"]]
    words_to_add.append(request.values["words"])
    words_to_add.remove("")
    word_groups.add_words_to_group(request.values["group_id"], words_to_add )

    return "OK"

@bp.route("/add_word_to_word_relation", methods=["POST"])
def add_word_to_word_relation():
    if "words" not in request.values:
        return "words is required", status.HTTP_400_BAD_REQUEST
    elif len(request.values["words"]) != 2:
        return "words must be an array of 2 words", status.HTTP_400_BAD_REQUEST
    
    if "relation_id" not in request.values:
        return "relation_id is required", status.HTTP_400_BAD_REQUEST
    
@bp.route("/add_word_relation", methods=["POST"])
def add_word_relation():
    if "relation_name" not in request.values:
        return "relation_name is required", status.HTTP_400_BAD_REQUEST

    return word_relations.create_relation(request.values["relation_name"]), status.HTTP_201_CREATED


@bp.route("/add_phrase", methods=["POST"])
def add_phrase():
    if "phrase" not in request.values or request.values["phrase"] is None or request.values["phrase"] == "":
        return "phrase is required", status.HTTP_400_BAD_REQUEST

    return jsonify(phrases.create_phrase(request.values["phrase"])), status.HTTP_201_CREATED


@bp.route("/export", methods=["GET"])
def export():
    if "entity_type" not in request.values or request.values["entity_type"] is None or request.values["entity_type"] == "":
        return "entity_type is required", status.HTTP_400_BAD_REQUEST

    entity_type = request.values["entity_type"]
    ALL = "all"
    SONG = "song"
    PHRASE = "phrase"
    GROUP = "group"
    if entity_type not in [ALL, SONG, PHRASE, GROUP]:
        return "unknown entity_type", status.HTTP_400_BAD_REQUEST
    tree = xml_handler.get_base_xml()
    if entity_type == ALL or entity_type == SONG:
        songs = get_song.get_all_songs()
        for song in songs:
            tree.append(xml_handler.dump_song(song))

    if entity_type == ALL or entity_type == PHRASE:
        all_phrases = phrases.get_all_phrases()
        for p in all_phrases:
            tree.append(xml_handler.dump_phrase(p))
    if entity_type == ALL or entity_type == GROUP:
        all_groups = word_groups.get_groups()
        for group in all_groups:
            tree.append(xml_handler.dump_word_group(group))
    

    
    buffer = io.StringIO(xml_handler.to_string(tree))
    mem = io.BytesIO()
    mem.write(buffer.getvalue().encode())
    mem.seek(0)
    buffer.close()

    return send_file (
        mem,
        as_attachment=True,
        attachment_filename ='export.xml',
        mimetype='text/xml',
        cache_timeout = 0
    )

