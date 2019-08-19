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

from megadetector import *


## Image visualisation page
#
@app.route('/show/<imageID>', methods=['GET'])
def image(imageID):

	
	imginfo = db.images.find_one({'_id': ObjectId(imageID)})
	if not imginfo:
		return '<span class="error">Image not found!</span>'


	return render_template('page-image.html', imgID=str(imageID))



## ajax backend
@app.route('/show/<imageID>/refresh', methods=['GET'])
def image_get(imageID):

	answer = {}
	imginfo = db.images.find_one({'_id': ObjectId(imageID)})
	if not imginfo:
		answer['type'] = 'error'
		answer['message'] = 'image not found'
		return dumps(answer)


	# TODO: check permissions

	imginfo['crops'] = list(db.crops.find({'src': ObjectId(imageID)}))

	answer['type'] = 'success'
	answer['message'] = 'image loaded'
	answer['image'] = imginfo
	return dumps(answer)



## Delete an image from the database
#
@app.route('/show/delete/<imageID>', methods=['GET'])
def image_delete(imageID):

	imgID = ObjectId(imageID)

	db.crops.remove({'src': imgID})
	db.images.remove({'_id': imgID})

	return redirect('/')



@app.route('/show/<imageID>/megascan', methods=['GET'])
def image_test(imageID):

	answer = {}

	imgID = ObjectId(imageID)
	img = db.images.find_one({'_id': imgID})
	if not img:
		answer['type'] = 'error'
		answer['message'] = 'image not found'
		return 'error'


	# delete all crops previously found for this image
	db.crops.remove({'src': imgID})

	# rescan with MS megascanner 3
	crops = MegaScan(img)
	db.crops.insert_many(crops)


	answer['type'] = 'success'
	answer['message'] = 'scan completed'
	answer['crops'] = list(db.crops.find({'src': imgID}))

	return dumps(answer)