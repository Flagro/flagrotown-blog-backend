from flask import Blueprint, jsonify, abort
from ..models.metrics import Metrics


metrics_bp = Blueprint('metrics_bp', __name__)

@metrics_bp.route('/<int:post_id>', methods=['GET'])
def get_metrics(post_id):
    metrics = Metrics.query.get(post_id)
    if not metrics:
        abort(404, description=f"Metrics for post with ID {post_id} not found")

    return jsonify({
        'id': metrics.id,
        'metrics': metrics.metrics
    })
