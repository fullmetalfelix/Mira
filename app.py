from flask_wtf import CSRFProtect
from flask import Flask, send_from_directory, redirect, request
from flask_login import LoginManager
from flask_login import current_user
from flask_mail import Mail
import jinja2

from config import Config

from pymongo import MongoClient
import gridfs
from momentjs import momentjs
import glob


app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)


app.jinja_env.globals['momentjs'] = momentjs
app.jinja_env.line_statement_prefix = '%'


# the main templates
template_folders = ["./templates"]

jinjaloader = jinja2.ChoiceLoader([	app.jinja_loader, jinja2.FileSystemLoader(template_folders), ])
app.jinja_loader = jinjaloader


mail = Mail()
mail.init_app(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


db = Config.DATABASE
fs = gridfs.GridFS(db)



# import all routes
import routes
import routes_search
import routes_upload
import routes_show


@app.context_processor
def utility_processor():
	return dict(db=db, current_user=current_user)


@app.route('/ping')
def ping():
	return "pong"

