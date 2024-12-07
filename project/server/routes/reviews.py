from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.db import db
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError

reviews_bp = Blueprint('reviews', __name__, url_prefix='/api/reviews')


@reviews_bp.route('/addreview', methods=['POST'])
@jwt_required()
def add_review():
    """
    Endpoint to add a new review to the database.
    Requires an authenticated user and valid input data.
    """
    user_id = get_jwt_identity()  
    data = request.json

    
    print(f"Received review data: {data}")

    
    if not data.get('description') or not data.get('rating') or not data.get('location'):
        return jsonify({"error": "All fields (description, rating, location) are required"}), 400

    try:
        # Insert the review into the database
        query = text("""
            INSERT INTO reviews (userID, description, rating, location)
            VALUES (:userID, :description, :rating, :location)
        """)
        db.session.execute(query, {
            "userID": user_id,
            "description": data["description"],
            "rating": data["rating"],
            "location": data["location"],
        })
        db.session.commit()
        return jsonify({"message": "Review added successfully!"}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error occurred: {e}")
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500


@reviews_bp.route('/getreview', methods=['GET'])
@jwt_required()
def get_reviews():
    print(f"Request Headers: {request.headers}")  
    """
    Endpoint to fetch all reviews for the authenticated user.
    """
    user_id = get_jwt_identity()  
    print(f"Authenticated user ID: {user_id}")  

    try:
        # Fetch reviews for the authenticated user
        query = text("SELECT * FROM reviews WHERE userID = :userID")
        results = db.session.execute(query, {"userID": user_id}).fetchall()

        # Format the results as a list of dictionaries
        reviews = [
            {
                "id": row.id,
                "description": row.description,
                "rating": row.rating,
                "location": row.location
            } for row in results
        ]

        return jsonify(reviews), 200
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500

@reviews_bp.route('/getallreview', methods=['GET'])
@jwt_required()
def get_allreviews():
    print(f"Request Headers: {request.headers}")  
    """
    Endpoint to fetch all reviews for the authenticated user.
    """
    user_id = get_jwt_identity()  
    print(f"Authenticated user ID: {user_id}")  

    try:
        # Fetch reviews for the authenticated user
        query = text("SELECT * FROM reviews")
        results = db.session.execute(query).fetchall()

        # Format the results as a list of dictionaries
        reviews = [
            {
                "id": row.id,
                "description": row.description,
                "rating": row.rating,
                "location": row.location
            } for row in results
        ]

        return jsonify(reviews), 200
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500


@reviews_bp.route('/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    """
    Endpoint to delete a specific review by its ID.
    Requires the user to be authenticated and the review to belong to the user.
    """
    user_id = get_jwt_identity()  
    print(f"Authenticated user ID: {user_id}, Deleting review ID: {review_id}")

    try:
        # Verify the review belongs to the authenticated user
        query = text("DELETE FROM reviews WHERE id = :review_id AND userID = :userID")
        result = db.session.execute(query, {"review_id": review_id, "userID": user_id})
        db.session.commit()

        if result.rowcount == 0:
            return jsonify({"error": "Review not found or not authorized"}), 404

        return jsonify({"message": "Review deleted successfully!"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error occurred: {e}")
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500
