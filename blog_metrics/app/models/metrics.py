from sqlalchemy.orm import relationship
from ..db import db


class Metrics(db.Model):
    __tablename__ = 'metrics'

    id = db.Column(db.Integer, primary_key=True)
    metrics = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Metrics for Post {self.id}>'
