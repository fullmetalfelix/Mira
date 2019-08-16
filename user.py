
from werkzeug.security import check_password_hash, generate_password_hash

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from Mira.app import db

import pymongo
from datetime import datetime


class User():

	def __init__(self, name):
		
		self.ID = 0
		self.name = name
		
		self.isAuth = False
		self.isAnonym = True
		self.record = {'_id': None}


	def Load(self, userRecord):

		self.isAuth = True
		self.isAnonym = False

		self.record = userRecord
		self.name = userRecord['name']
		

	def get_screen_name(self):
		if self.record['fullname'] == "":
			return self.record['name']
		else:
			return self.record['fullname']

	def get_name(self):
		return self.record['name'];

	def is_authenticated(self):
		return self.isAuth

	def is_active(self):
		return self.record['validated']

	def is_anonymous(self):
		return self.isAnonym

	def get_id(self):
		return self.name

	
	@staticmethod
	def Save(form, validated=True):
		
		# create the record for mongo
		record = {}
		record['email'] = form.email.data
		record['name'] = form.name.data
		record['fullname'] = ""
		record['tel1'] = ""
		record['tel2'] = ""
		record['password'] = generate_password_hash(form.password.data, salt_length=16, method='sha256')

		record['validated'] = validated
		record['created'] = datetime.utcnow()

		record['hiddenmsg'] = []

		# ...

		
		mongoID = db.userinfo.insert_one(record).inserted_id
		
		return mongoID

	

	@staticmethod
	def Save_ajax(data):
		
		# create the record for mongo
		record = {}
		record['email'] = data['email']
		record['name'] = data['name']
		record['fullname'] = ""
		record['tel1'] = ""
		record['tel2'] = ""
		record['password'] = generate_password_hash(data['password'], salt_length=16, method='sha256')

		record['validated'] = True
		record['created'] = datetime.utcnow()

		record['hiddenmsg'] = []
		

		# ...

		
		mongoID = db.userinfo.insert_one(record).inserted_id
		
		return mongoID

	@staticmethod
	def Login_validate(userRecord, pw):
		# pw is the password written in the login form
		# userRecord is the mongoDB userinfo document corresponding to the email in the form
		
		goodpw = check_password_hash(userRecord['password'], pw)
		
		return goodpw



	## Updates the lastlogin property of a user in the database
	#
	def UserTick(self):

		self.record = db.userinfo.find_one_and_update({'_id': self.record['_id']}, 
			{'$set': {'lastlogin': datetime.utcnow()}}, return_document=pymongo.ReturnDocument.AFTER)



def User_screenName(userRecord):
	
	if userRecord.get('fullname', "") != "": 
		return userRecord['fullname']
	else: 
		return userRecord['name']

