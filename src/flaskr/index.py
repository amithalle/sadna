import functools
import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from flask_api import status

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    return render_template("base.html")
