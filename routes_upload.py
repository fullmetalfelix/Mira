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





## Image upload page
#
@app.route('/upload', methods=['GET'])
def upload():

	# not much to do here... just return the template
	return render_template('page-upload.html')





## Upload ajax backends
#
# this is called by the client when uploading an image
#
@app.route('/upload/img', methods=['POST'])
def upload_post():

	data = request.json

	# create the mongo document to store
	entry = {
		'original': data['original'],
		'tags': [t.strip() for t in data['tags'].split(',')],
		'loc': data['loc'],
		'file': data['dataURL'], # the image is stores as its base64 dataURL - might take a bit more space!
		'uptime': datetime.utcnow() # upload timestamp
	}

	# place the entry in the database and retrieve its ID for no reason
	imgID = db.images.insert_one(entry).inserted_id


	# give an answer to the client so it can move on with its life
	answer = {}
	answer['type'] = 'success'
	answer['message'] = 'image uploaded'
	return dumps(answer)






## Upload ajax responder - for batches of images
#
# TODO
#
@app.route('/upload/batch', methods=['POST'])
def upload_batch():


	return ""


