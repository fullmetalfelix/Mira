from pymongo import MongoClient


class Config(object):

	WTF_CSRF_ENABLED = True
	SECRET_KEY = "use some secure secret key here!"
	
	DEBUG = True

	DATABASE = MongoClient('mongodb://flasktester:flasker00@nanolayers.dyndns.org')['flasktest']

	PUBLIC_URL =	"http://localhost:5000/"
	PUBLIC_NAME =	"Mira"
	
	DOCS_LOC = 'docs/'
	
	