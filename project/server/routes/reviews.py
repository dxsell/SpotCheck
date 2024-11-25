from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.db import db
from sqlalchemy.exc import SQLAlchemyError

reviews_bp = Blueprint('reviews', __name__, url_prefix='/api/reviews')

@reviews_bp.route('/', methods=['POST'])
@jwt_required()
def add_review():
    user_id = get_jwt_identity()  # Get user ID from the JWT token
    data = request.json

    # Debugging: Print received data
    print(f"Received data: {data}")

    # Validate input data
    if not data.get('description') or not data.get('rating') or not data.get('location'):
        return jsonify({"error": "All fields are required"}), 400

    # Attempt to save to the database
    try:
        db.session.execute(
            """
            INSERT INTO reviews (userID, description, rating, location)
            VALUES (:userID, :description, :rating, :location)
            """,
            {
                "userID": user_id,
                "description": data["description"],
                "rating": data["rating"],
                "location": data["location"],
            }
        )
        db.session.commit()
        return jsonify({"message": "Review added successfully!"}), 201
    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500

@reviews_bp.route('/', methods=['GET'])
@jwt_required()
def get_reviews():
    user_id = get_jwt_identity()  # Get user ID from the JWT token
    results = db.session.execute(
        "SELECT * FROM reviews WHERE userID = :userID",
        {"userID": user_id}
    ).fetchall()

    reviews = [
        {"id": row.id, "description": row.description, "rating": row.rating, "location": row.location}
        for row in results
    ]

    return jsonify(reviews), 200

