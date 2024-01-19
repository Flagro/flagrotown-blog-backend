from flask import Blueprint, request, abort, current_app
from ..blog_repository import blog_repository
from ..object_storage import object_storage
from ..db import db
from ..models.post import Post
from ..models.image import Image
import hmac
import hashlib


blog_repo_bp = Blueprint('blog_repo_bp', __name__)


@blog_repo_bp.route('/blog-repo-update', methods=['POST'])
def blog_repo_update():
    # Validate the webhook
    signature = request.headers.get('X-Hub-Signature')
    if not is_valid_signature(request.data, signature, current_app.config['GITHUB_WEBHOOK_SECRET']):
        abort(403)

    deleted_files, added_files = blog_repository.get_diff()
    # Delete all the deleted/updated files
    for file_path in deleted_files:
        try:
            if file_path.endswith('.md'):
                # Assuming the file name maps directly to Post ID or some unique identifier
                post = Post.query.filter_by(id=file_path.strip('.md')).first()
                if post:
                    db.session.delete(post)
                    db.session.commit()
            else:
                image = Image.query.filter_by(filename=file_path).first()
                if image:
                    image.delete_from_s3()
                    db.session.delete(image)
                    db.session.commit()
        except Exception as e:
            # Log the exception
            print(f"Error deleting file {file_path}: {e}")

    # Add all the new/updated files
    for file_path, file_contents in added_files:
        try:
            if file_path.endswith('.md'):
                file_contents = file_contents.decode('utf-8')
                # Update or create new Post
                post = Post.query.filter_by(id=file_path.strip('.md')).first()
                if not post:
                    post = Post(id=file_path.strip('.md'), text=file_contents)
                    db.session.add(post)
                else:
                    post.text = file_contents
                post.update_image_links(object_storage)
                db.session.commit()
            else:
                # Create a new Image and upload to S3
                new_image = Image(filename=file_path)
                db.session.add(new_image)
                db.session.commit()
                new_image.upload_to_s3(file_contents)
        except Exception as e:
            # Log the exception
            print(f"Error adding/updating file {file_path}: {e}")

    return 'Update processed', 200


def is_valid_signature(payload, header_signature, secret):
    sha_name, signature = header_signature.split('=')
    if sha_name != 'sha1':
        return False

    mac = hmac.new(secret.encode(), msg=payload, digestmod=hashlib.sha1)
    return hmac.compare_digest(mac.hexdigest(), signature)
