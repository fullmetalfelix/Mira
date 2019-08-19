from pymongo import MongoClient


class Config(object):

	WTF_CSRF_ENABLED = True
	SECRET_KEY = "use some secure secret key here!"
	
	DEBUG = True

	DATABASE = MongoClient('mongodb://mira:mira@nanolayers.dyndns.org')['mira']

	PUBLIC_URL =	"http://localhost:5000/"
	PUBLIC_NAME =	"Mira"
	

	UPLOAD_FOLDER = './archive/'
	DOCS_LOC = 'docs/'
	
	MEGA_MODEL = None