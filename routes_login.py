# -*- coding: utf-8 -*-

from Mira.user import User
from Mira.app import app, lm, db, mail, csrf

from werkzeug.security import generate_password_hash
import flask
from flask import session, request, redirect, render_template, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message

from bson.objectid import ObjectId
from datetime import datetime
import random, string
import time





# *** LOGIN SYSTEM *** ********************************************************



from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Email, Length, EqualTo

from Mira.widgets import *



## Class for a login form
#
class LoginForm(FlaskForm):
	
	"""Login form to access writing and settings pages"""

	name = StringField('Name', widget=Widget_textinput, validators=[InputRequired(), Length(max=30)], render_kw={"placeholder":"your username here"})
	password = PasswordField('Password', widget=Widget_textinput, validators=[InputRequired()], render_kw={"placeholder":"your password here", 'type':'password'})
	
	#reminder = SubmitField(label='Reminder')
	loginbutton= SubmitField()






## Main login URL
#
# POST is called when the client submits the login form.
#
@app.route('/login', methods=['GET', 'POST'])
def login():

	# create a login form
	form = LoginForm()

	if request.method == 'POST' and form.validate_on_submit():

		# fetch a user record with same name
		userRecord = db.userinfo.find_one({"name": form.name.data})

		if not userRecord:
			flask.flash("Wrong username or password!", category='error')
			return render_template('login.html', title='MIRA Login', form=form)

		# code here means the record exists


		# check the password
		pwOK = User.Login_validate(userRecord, form.password.data)
		if pwOK:

			# the password/user combo was ok

			# check if the email is verified
			if not userRecord['validated']:
				flask.flash("Email address not verified.", category='error')
				return render_template('login.html', title='MIRA Login', form=form)


			# LOGIN SUCCESFUL --- continue
			# create a user object
			user_obj = User(userRecord['name'])
			# login the user with the system
			login_user(user_obj)

			# get this time as the lastlogin and update it in the database
			lastlogin = datetime.utcnow()
			lastlogin = { "$set": { "lastlogin": lastlogin }, "$unset": {"oldpassword":"", "requestedreset":""} }
			db.userinfo.update_one({"name": userRecord['name']}, lastlogin)
			# when login is successful, the old password and reset request are removed from the database

			# what is this? redirect to main page with login details
			return redirect(request.args.get("next") or app.config['PUBLIC_URL'])

		else:
			time.sleep(5)
			flask.flash("Wrong username or password.", category='error')
			return render_template('login.html', title='MIRA Login', form=form)


	return render_template('login.html', title='MIRA Login', form=form)




## Logout function
#
@app.route('/logout', methods=['GET'])
@login_required
def logout():

	current_user.UserTick()

	logout_user()

	return render_template("logout.html")



## Internal function to login users and create the User object
#
@lm.user_loader
def load_user(name):

	u = db.userinfo.find_one({"name": name})

	if not u:
		return None

	user_obj = User(u['name'])
	user_obj.Load(u)

	return user_obj

# *****************************************************************************
