from pymongo import MongoClient


class Config(object):

	WTF_CSRF_ENABLED = True
	SECRET_KEY = "use some secure secret key here!"
	
	DEBUG = True

	DATABASE = MongoClient('mongodb://mira:mira@mongo-mira')['mira']

	#PUBLIC_URL =	"https://mira.rahtiapp.fi/"
	PUBLIC_URL =	"http://localhost:5000/"
	PUBLIC_NAME =	"Mira"
	

	UPLOAD_FOLDER = './archive/'
	DOCS_LOC = 'docs/'
	
	