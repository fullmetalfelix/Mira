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

from megadetector import MegaScanner



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

	imgID = ObjectId(imageID)

	answer = {}
	imginfo = db.images.find_one({'_id': imgID})
	if not imginfo:
		answer['type'] = 'error'
		answer['message'] = 'image not found'
		return dumps(answer)


	# TODO: check permissions


	# check if there is a scan task active
	task = db.analysis.find_one({'src': imgID})
	if task != None:
		answer['type'] = 'inprogress'
		answer['message'] = 'scan in progress...'
		imginfo['crops'] = []
		answer['image'] = imginfo
		return dumps(answer)


	imginfo['crops'] = list(db.crops.find({'src': imgID}))

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



## Requests a megascan of the image
#
@app.route('/show/<imageID>/megascan', methods=['GET'])
def image_megascan(imageID):

	answer = {}

	imgID = ObjectId(imageID)
	img = db.images.find_one({'_id': imgID})
	if not img:
		answer['type'] = 'error'
		answer['message'] = 'image not found'
		return dumps(answer)


	# check if there is already an analysis task running
	task = db.analysis.find_one({'src': imgID})
	if task != None:
		answer['type'] = 'inprogress'
		answer['message'] = 'scan in progress...'
		answer['crops'] = []
		return dumps(answer)


	# delete all crops previously found for this image
	db.crops.remove({'src': imgID})

	# mark down a task for this image
	db.analysis.insert_one({
		'src': imgID,
		'time': datetime.utcnow(),
	})

	# start a thread with the task - rescan with MS megascanner 3
	task = MegaScanner(img)

	# give a temporary answer to the client - please wait and refresh
	answer['type'] = 'inprogress'
	answer['message'] = 'scan in progress...'
	answer['crops'] = []

	return dumps(answer)





## Check the status of the megascan
@app.route('/show/<imageID>/megascan/check', methods=['GET'])
def image_megascan_check(imageID):

	answer = {}

	imgID = ObjectId(imageID)
	img = db.images.find_one({'_id': imgID})
	if not img:
		answer['type'] = 'error'
		answer['message'] = 'image not found'
		return dumps(answer)


	task = db.analysis.find_one({'src': imgID})
	if task != None:
		answer['type'] = 'inprogress'
		answer['message'] = 'scan in progress...'
		answer['crops'] = []
		return dumps(answer)


	answer['type'] = 'success'
	answer['message'] = 'scan completed'
	answer['crops'] = list(db.crops.find({'src': imgID}))

	return dumps(answer)







