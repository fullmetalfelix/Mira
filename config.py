from pymongo import MongoClient


class Config(object):

	WTF_CSRF_ENABLED = True
	SECRET_KEY = "use some secure secret key here!"
	
	DEBUG = True

	DATABASE = MongoClient('mongodb://mira:mira@host')['db']

	PUBLIC_URL =	"http://mira.rahtiapp.fi/"
	PUBLIC_NAME =	"Mira"
	

	UPLOAD_FOLDER = './archive/'
	DOCS_LOC = 'docs/'
	
	