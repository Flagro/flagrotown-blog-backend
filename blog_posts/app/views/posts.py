from flask import Blueprint, jsonify, abort
from ..models.post import Post


posts_bp = Blueprint('posts_bp', __name__)

@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404, description=f"Post with ID {post_id} not found")

    return jsonify({
        'id': post.id,
        'text': post.text
    })
