from flask import Blueprint, request, jsonify
from models.db import db
from models.reviews import Reviews
from flask_jwt_extended import jwt_required, get_jwt_identity

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/', methods=['GET'])
@jwt_required()
def get_reviews():
    user_id = get_jwt_identity()  # Get the logged-in user ID
    reviews = Reviews.query.filter_by(userID=user_id).all()  # Fetch user-specific reviews
    return jsonify([review.to_dict() for review in reviews]), 200

@reviews_bp.route('/', methods=['POST'])
@jwt_required()
def add_review():
    user_id = get_jwt_identity()  # Get the logged-in user ID
    data = request.json

    # Validate inputs
    if not data.get('description') or not data.get('rating') or not data.get('location'):
        return jsonify({"error": "All fields are required"}), 400

    # Add review to the database
    new_review = Reviews(
        userID=user_id,
        description=data['description'],
        rating=data['rating'],
        location=data['location']
    )
    db.session.add(new_review)
    db.session.commit()

    return jsonify({"message": "Review added successfully!"}), 201
