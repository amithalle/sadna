import functools
import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from flask_api import status

from server import get_song, word_groups, word_relations

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

@bp.route("/words", methods=["GET"])
def get_words():
    if "song_id" in request.values:
        data = get_song.get_song_words(request.values["song_id"])
    else:
        data = get_song.get_all_words()

    return render_template("ajax/words_table.html", words=data)

@bp.route("/words_in_song", methods=["GET"])
def get_words_in_song_form():
    return render_template("ajax/words_search.html",songs=get_song.get_all_songs())

@bp.route("/words_index_form", methods=["GET"])
def get_word_index_form():
    return render_template("ajax/word_index_form.html",songs=get_song.get_all_songs())

@bp.route("/words_index", methods=["GET"])
def get_word_index():
    if "song_id" in request.values:
        return render_template("ajax/word_index.html",words=get_song.get_words_for_song(request.values["song_id"]))
    else:
        return "song_id is needed", status.HTTP_400_BAD_REQUEST

@bp.route("/word_occurences", methods=["GET"])
def get_occurrences():
    if "word" not in request.values:
        return "word is needed", status.HTTP_400_BAD_REQUEST
    song_id = request.values["song_id"] if  "song_id" in request.values else None
    song_id = song_id if song_id != "" else None # make emapty string become none
    data = get_song.get_word_context(request.values["word"], song_id)
    return render_template("ajax/word_occurences.html", occurences=data, word=request.values["word"])

@bp.route("/word_by_index", methods=["GET"])
def word_by_index():
    return render_template("ajax/word_by_index.html", songs=get_song.get_all_songs())


@bp.route("/get_word_groups", methods=["GET"])
def get_word_groups():
    return render_template("ajax/word_groups.html", groups=word_groups.get_groups())

@bp.route("/words_in_group", methods=["GET"])
def get_word_group():
    if "group_id" not in request.values:
        return "group_id is required", status.HTTP_400_BAD_REQUEST
    else:

        group_id = request.values["group_id"]
        words = word_groups.get_words_in_group(group_id)
        return render_template("ajax/word_group_details.html", 
            group_words=words, 
            group_id=group_id, 
            group_name=word_groups.get_group_name(group_id)[0][0], 
            words=[w[0] for w in get_song.get_all_words()])


@bp.route("/group_occurences", methods=["GET"])
def group_occurences():
    if "group_id" not in request.values:
        return "group_id is required", status.HTTP_400_BAD_REQUEST
    else:
        group_id = request.values["group_id"]

        words = word_groups.get_words_in_group(group_id)
        occurences = get_song.get_word_context(words)
        return render_template("ajax/word_occurences.html", occurences=occurences)


@bp.route("/get_word_relations", methods=["GET"])
def get_word_relations():
    relation_list = word_relations.get_word_relations()
    return render_template("ajax/word_relations.html", relation_list=relation_list)