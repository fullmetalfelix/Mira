from pymongo import MongoClient


class Config(object):

	WTF_CSRF_ENABLED = True
	SECRET_KEY = "use some secure secret key here!"
	
	DEBUG = True

	DATABASE = MongoClient('mongodb://mira:mira@mongo-mira', authSource='mira')['mira']

	PUBLIC_URL =	"https://mira.rahtiapp.fi/"
	PUBLIC_NAME =	"Mira"
	

	UPLOAD_FOLDER = './archive/'
	DOCS_LOC = 'docs/'
	
	