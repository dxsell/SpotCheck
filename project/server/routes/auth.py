from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user import User
from models.db import db

bcrypt = Bcrypt()
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json

    # Validate input fields
    if not data.get('username') or not data.get('password') or not data.get('email'):
        return jsonify({"error": "All fields are required"}), 400

    # Check if the username or email already exists
    if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Username or email already exists"}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    # Create a new user
    new_user = User(username=data['username'], password=hashed_password, email=data['email'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    # Validate inputs
    if not data.get('username') or not data.get('password'):
        return jsonify({"error": "Username and password are required"}), 400

    # Query user from the database
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        # Generate a JWT token
        token = create_access_token(identity=user.id)
        return jsonify({"token": token, "username": user.username}), 200

    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route('/account', methods=['GET'])
@jwt_required()
def get_account():
    user_id = get_jwt_identity()  # Get the logged-in user ID
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "username": user.username,
        "email": user.email,
        "member_since": user.created_at.strftime("%B %Y")
    }), 200
