from flask import Flask
from flask_mysqldb import MySQL
from config import Config
from controllers.serie_controller import series_controller

app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)

app.register_blueprint(series_controller)

@app.route("/")
def home():
    return "Hello, Flask!"
