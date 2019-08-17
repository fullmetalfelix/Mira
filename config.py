from pymongo import MongoClient


class Config(object):

	WTF_CSRF_ENABLED = True
	SECRET_KEY = "use some secure secret key here!"
	
	DEBUG = True

	DATABASE = MongoClient('mongodb://user:pwd@host')['db']

	PUBLIC_URL =	"http://localhost:5000/"
	PUBLIC_NAME =	"Mira"
	
	DOCS_LOC = 'docs/'
	
	