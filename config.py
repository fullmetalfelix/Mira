from pymongo import MongoClient
import os


class Config(object):

	WTF_CSRF_ENABLED = True
	SECRET_KEY = os.environ.get('MIRA_SECRET', "use some secure secret key here!")
	
	DEBUG = True

	MONGO_HOST = os.environ.get('MONGO_HOST')
	MONGO_USER = os.environ.get('MONGO_USER')
	MONGO_PWD = os.environ.get('MONGO_PWD')
	MONGO_DB = os.environ.get('MONGO_DB')
	DATABASE = MongoClient('mongodb://{}:{}@{}'.format(MONGO_USER, MONGO_PWD,MONGO_HOST))[MONGO_DB]

	PUBLIC_URL =	os.environ.get('PUBLIC_URL')
	PUBLIC_NAME =	"Mira"
	

	CELERY_BROKER_URL 		= "redis://:{}@{}:6379/0".format(os.environ['REDIS_PASSWORD'], os.environ['REDIS_HOST'])
	CELERY_RESULT_BACKEND 	= "redis://:{}@{}:6379/0".format(os.environ['REDIS_PASSWORD'], os.environ['REDIS_HOST'])



	UPLOAD_FOLDER = './archive/'
	DOCS_LOC = 'docs/'
	
	MEGA_MODEL = None
	