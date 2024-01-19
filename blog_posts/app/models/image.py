from sqlalchemy import ForeignKey
from ..db import db
from ..object_storage import object_storage


class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    post_id = db.Column(db.Integer, ForeignKey('posts.id'), nullable=False)

    def __repr__(self):
        return f'<Image {self.id}>'

    def upload_to_s3(self, file_content):
        return object_storage.upload_file(file_content, self.filename)

    def delete_from_s3(self):
        return object_storage.delete_file(self.filename)

    @property
    def url(self):
        return object_storage.generate_file_url(self.filename)
