from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models.db import db
from config import Config
from routes.auth import auth_bp

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
JWTManager(app)
db.init_app(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')

@app.route('/')
def home():
    return {"message": "Welcome to the Flask Backend!"}

if __name__ == '__main__':
    app.run(debug=True)
