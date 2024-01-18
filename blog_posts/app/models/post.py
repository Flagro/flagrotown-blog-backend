import re
from sqlalchemy.orm import relationship
from ..db import db


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    images = relationship('Image', backref='post', lazy=True)

    def __repr__(self):
        return f'<Post {self.id}>'

    def update_image_links(self, object_storage):
        """
        Update Markdown image references in the post text with Object Storage URLs, 
        while preserving the alt text.
        """
        pattern = r'(!\[.*?\])\(\.\./images/(.*?)\)'

        def replace_with_url(match):
            alt_text = match.group(1)
            filename = match.group(2)
            image = next((img for img in self.images if img.filename == filename), None)
            if image:
                return f'{alt_text}({object_storage.generate_file_url(image.filename)})'
            return match.group(0)  # No replacement if no corresponding image

        self.text = re.sub(pattern, replace_with_url, self.text)
