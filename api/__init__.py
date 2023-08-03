from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from api.utils.config import DATABASE_CONNECTION_URI

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route('/')
def hello():
    return 'My First API !!'