from flask import Flask
from flask_cors import CORS
from routes.user_routes import user_blueprint

app = Flask(__name__)

CORS(app)


app.register_blueprint(user_blueprint)
