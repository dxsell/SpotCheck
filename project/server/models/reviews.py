from .db import db

class Reviews(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.String(50))
    rating = db.Column(db.String(100))
    location = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email}
