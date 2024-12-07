from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models.db import db
from config import Config
from routes.auth import auth_bp
from routes.reviews import reviews_bp

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize JWT and Database
JWTManager(app)
db.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(reviews_bp, url_prefix='/api/reviews')

@app.route('/')
def home():
    return {"message": "Welcome to the Flask Backend!"}

@app.route('/test_db')
def test_db():
    try:
        connection = db.engine.raw_connection()
        connection.cursor().execute('select 1')
        connection.close()
        return {"message": "Database connection successful"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
