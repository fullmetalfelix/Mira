# -*- coding: utf-8 -*-

from Mira.app import app, lm, db
from werkzeug.security import generate_password_hash
from datetime import datetime

import flask
from flask import session, request, redirect, render_template, url_for, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user



## Simple index page
#
# this shows basic functionalities to upload images and analyse them
@app.route('/')
def index:


	return render_template('index.html')


@app.route('/upload')
def index:


	return ""


@app.route('/uploadbatch')
def index:


	return ""