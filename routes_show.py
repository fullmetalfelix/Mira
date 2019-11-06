# -*- coding: utf-8 -*-

from Mira.app import app, lm, db, celery
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import celery.states as states

from datetime import datetime

import flask
from flask import session, request, redirect, render_template, url_for
from flask_login import login_user, logout_user, login_required, current_user

from datetime import datetime

import pymongo, bson, json
from bson.objectid import ObjectId
from bson.json_util import dumps, CANONICAL_JSON_OPTIONS

#from megadetector import MegaScanner



## Image visualisation page
#
@app.route('/show/<imageID>', methods=['GET'])
@login_required
def image(imageID):

	
	imginfo = db.images.find_one({'_id': ObjectId(imageID)})
	if not imginfo:
		return '<span class="error">Image not found!</span>'

	return render_template('page-image.html', imgID=str(imageID))



## ajax backend
@app.route('/show/<imageID>/refresh', methods=['GET'])
@login_required
def image_get(imageID):

	imgID = ObjectId(imageID)

	answer = {}
	imginfo = db.images.find_one({'_id': imgID}, {'thumb': 0, 'hash': 0})
	if not imginfo:
		answer['type'] = 'error'
		answer['message'] = 'image not found'
		return dumps(answer)


	# check if there is a scan task active
	task = db.tasks.find_one({'imgID': imgID})
	if task:
		# if there is a task, check if it is done
		taskID = task['ctask']
		res = celery.AsyncResult(taskID)
		needsDelete = (res.state == states.PENDING and res.result == None) or (res.state == states.SUCCESS)

		if needsDelete:
			celery.AsyncResult(taskID).forget()
			db.tasks.delete_one({'ctask': taskID})
			task = None


	answer['type'] = 'success'
	answer['message'] = 'image loaded'
	answer['image'] = imginfo
	answer['task'] = task
	return dumps(answer)



@app.route('/show/<imageID>/override', methods=['POST'])
@login_required
def image_override(imageID):

	answer = {}
	data = request.json
	imgID = ObjectId(imageID)

	imginfo = db.images.find_one({'_id': imgID}, {'thumb': 0, 'hash': 0})
	if not imginfo:
		answer['type'] = 'error'
		answer['message'] = 'image not found'
		return dumps(answer)

	task = db.tasks.find_one({'imgID': imgID})
	if task:
		answer['type'] = 'error'
		answer['message'] = 'detection in progress'
		return dumps(answer)

	if imginfo['phase'] != 10:
		answer['type'] = 'error'
		answer['message'] = 'unknown error'
		return dumps(answer)

	crops = imginfo.get('crops', [])
	if data['cropID'] >= len(crops):
		answer['type'] = 'error'
		answer['message'] = 'invalid crop'
		return dumps(answer)
	crop = crops[data['cropID']]
	

	result = {}
	result[data['cls']] = 1.0

	newcrops = []
	for i in range(len(crops)):

		if i == data['cropID']:
			# this is the crop to edit
			newanal = [a for a in crops[i]['analysis'] if a['name'] != 'user']
			analysis = {
				'name': 'user',
				'fullname': current_user.record['fullname'],
				'result': result,
			}
			newanal.append(analysis)
			crops[i]['analysis'] = newanal

		newcrops.append(crops[i])


	db.images.find_one_and_update(
		{'_id': imgID},
		{'$set': { 'crops': newcrops }}
	)


	answer['type'] = 'success'
	answer['message'] = 'done'
	return dumps(answer)



## Delete an image from the database
#
@app.route('/show/delete/<imageID>', methods=['GET'])
@login_required
def image_delete(imageID):

	imgID = ObjectId(imageID)

	db.images.remove({'_id': imgID})
	db.tasks.remove({'imgID': imgID})

	return redirect('/')





@app.route('/check/<string:taskID>', methods=['GET'])
@login_required
def check_detector(taskID):  

	res = celery.AsyncResult(taskID)

	answer = {}
	answer['type'] = res.state	
	answer['result'] = res.result


	if res.state == states.PENDING and res.result == None:
		answer['type'] = 'NOTFOUND'


	return dumps(answer)


