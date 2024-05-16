from flask import Flask
from flask_cors import CORS
from __init__ import db
from Model.Login import user_login
from Model.EventCreate import EventCreate
from Model.EventManage import get_events

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)
# username: root, password: root
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/emsdb?charset=utf8'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.route("/login", methods=["POST"])(user_login)
app.route("/eventCreate", methods=["POST"])(EventCreate)
app.route("/events", methods=["GET"])(get_events)

if __name__ == "__main__":
    app.run(debug=True)