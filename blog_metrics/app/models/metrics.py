from ..db import db


class PostAnalytics(db.Model):
    __tablename__ = 'post_analytics'

    post_id = db.Column(db.Integer, primary_key=True)
    views = db.Column(db.Integer, default=0, nullable=False)
    # Future fields for comments, upvotes, etc.

    def __repr__(self):
        return f'<PostAnalytics {self.post_id}>'
