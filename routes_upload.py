# -*- coding: utf-8 -*-

from Mira.app import app, lm, db
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime

import flask
from flask import session, request, redirect, render_template, url_for
from flask_login import login_user, logout_user, login_required, current_user

from datetime import datetime

import pymongo, bson, json
from bson.objectid import ObjectId
from bson.json_util import dumps, CANONICAL_JSON_OPTIONS


from PIL import Image
from io import BytesIO
import base64
import hashlib


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

	answer = {}
	data = request.json

	# create the mongo document to store
	tags = [t.strip() for t in data['tags'].split(',')]
	tags = [t for t in tags if len(t) > 0]
	
	entry = {
		'filename': data['filename'],
		'file': data['dataURL'], # the image is stored as its base64 dataURL - might take a bit more space!
		'tags': tags,
		'loc': data['loc'],
		'uptime': datetime.utcnow(), # upload timestamp
		'phase': 0,
	}

	entry['hash'] = hashlib.sha512()
	entry['hash'].update(entry['filename'].encode())
	entry['hash'].update(entry['file'].encode())
	entry['hash'] = entry['hash'].digest()


	# check if there is already an image in the database with the same hash
	others = list(db.images.find({'filename': entry['filename'], 'hash': entry['hash']}))
	if len(others) > 0:
		answer['type'] = 'error'
		answer['message'] = 'image already in the database'
		return dumps(answer)

	# make a lowres thumbnail
	size = 128, 128
	img = entry['file'].split(';base64,',1)[1]
	img = base64.b64decode(img)
	img = Image.open(BytesIO(img))
	img.thumbnail(size, Image.ANTIALIAS)
	buffer = BytesIO()
	img.save(buffer, format="PNG")
	entry['thumb'] = 'data:image/png;base64,'.encode()+base64.b64encode(buffer.getvalue())

	# place the entry in the database and retrieve its ID for no reason
	imgID = db.images.insert_one(entry).inserted_id


	# give an answer to the client so it can move on with its life
	answer['type'] = 'success'
	answer['message'] = 'image uploaded'
	return dumps(answer)






## Upload ajax responder - for batches of images
#
# TODO
#
@app.route('/upload/batch', methods=['POST'])
def upload_batch():


	return "NOT IMPLEMENTED YET"


