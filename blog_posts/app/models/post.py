from sqlalchemy.orm import relationship
from ..db import db


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    images = relationship('Image', backref='post', lazy=True)

    def __repr__(self):
        return f'<Post {self.id}>'
