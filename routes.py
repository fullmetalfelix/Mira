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


## Image search page
#
@app.route('/search', methods=['GET'])
def search():




	return render_template('page-search.html')





## Image visualisation page
#
@app.route('/show/<imageID>', methods=['GET'])
def image():

	
	#imginfo = db.images.find_one({'_id': ObjectID(imageID)})



	return render_template('image.html')

## ajax backend
@app.route('/show/<imageID>/refresh', methods=['GET'])
def image_get():

	answer = {}
	imginfo = db.images.find_one({'_id': ObjectID(imageID)})
	if not imginfo:
		answer['type'] = 'error'
		answer['message'] = 'image not found'
		return dumps(answer)


	# TODO: check permissions


	answer['type'] = 'success'
	answer['message'] = 'image loaded'
	answer['image'] = imginfo
	return dumps(answer)




## Image upload page
#
@app.route('/upload', methods=['GET'])
def upload():


	return render_template('page-upload.html')



## Upload ajax backends
@app.route('/upload/img', methods=['POST'])
def upload_post():

	data = request.json

	entry = {
		'filename': data['filename'],
		'tags': [t.strip() for t in data['tags'].split(',')],
		'loc': data['loc'],
		'file': data['dataURL'] # the image is stores as its base64 dataURL - might take a bit more space!
	}

	# place the entry in the database and retrieve the ID for no reason
	imgID = db.images.insert_one(entry).inserted_id

	# give an answer to the client so it can move on with its life
	answer = {}
	answer['type'] = 'success'
	answer['message'] = 'image uploaded'
	return dumps(answer)



@app.route('/upload/batch', methods=['POST'])
def upload_batch():


	return ""



@app.route('/ping', methods=['GET'])
def ping():
	return "pong"







