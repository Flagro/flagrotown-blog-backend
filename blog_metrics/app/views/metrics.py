import requests
from flask import Blueprint, jsonify, abort
from ..models.metrics import PostAnalytics
from ..db import db


metrics_bp = Blueprint('metrics_bp', __name__)


def check_post_exists(post_id):
    response = requests.get(f'https://blog-api.flagrotown.com/posts/{post_id}')
    return response.status_code == 200


@metrics_bp.route('/<int:post_id>', methods=['GET'])
def get_metrics(post_id):
    if not check_post_exists(post_id):
        abort(404, description=f"Post {post_id} doesn't exist")

    metrics = PostAnalytics.query.get(post_id)
    if not metrics:
        metrics = PostAnalytics(post_id=post_id)
        db.session.add(metrics)
        db.session.commit()

    return jsonify({
        'views': metrics.views,
    })
