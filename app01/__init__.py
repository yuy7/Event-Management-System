from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

def init_db():
    app = Flask(__name__)
    app.config.from_object(__name__)
    CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)
    # username: root, password: root
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/emsdb?charset=utf8'
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    return app, db