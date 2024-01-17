from ..db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)

    @classmethod
    def find_or_create(cls, email, name):
        user = cls.query.filter_by(email=email).first()
        if not user:
            user = cls(email=email, name=name)
            db.session.add(user)
            db.session.commit()
        return user    

    def __repr__(self):
        return f"<User id={self.id}, email='{self.email}'>"
