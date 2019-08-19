# -*- coding: utf-8 -*-

from Mira.app import app, lm, db
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime

import flask
from flask import session, request, redirect, render_template, url_for
from flask_login import login_user, logout_user, login_required, current_user

from datetime import datetime

import pymongo, bson, json
from bson.objectid import ObjectId
from bson.json_util import dumps, CANONICAL_JSON_OPTIONS



### BASIC BAGES ###

## Simple index page
#
# this shows basic functionalities to upload images and analyse them
@app.route('/', methods=['GET'])
def index():





	return render_template('page-index.html')



# ------------------------------------------------------------------------------






@app.route('/ping', methods=['GET'])
def ping():
	return "pong"







