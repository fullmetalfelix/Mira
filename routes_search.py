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



## Image search page
#
@app.route('/search', methods=['GET'])
@login_required
def search():

	return render_template('page-search.html')





## Image search page
#
@app.route('/search/request', methods=['POST'])
@login_required
def search_request():

	answer = {}
	data = request.json

	tags = [t.strip() for t in data['tags'].split(',')]
	tags = [t for t in tags if len(t) > 0]

	query = {}
	if len(tags) > 0:
		query['tags'] = {'$in': tags}

	if data['loc'] != "":
		query['loc'] = {'$regex' : loc, '$options' : 'i'}

	if data['status'] != 'any':
		query['phase'] = int(data['status'])

	results = list(db.images.find(query, {'file': 0, 'hash': 0}))

	answer['type'] = 'success'
	answer['message'] = 'found {} images'.format(len(results))
	answer['results'] = results
	return dumps(answer)


