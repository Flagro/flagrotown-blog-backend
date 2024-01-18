from flask import Blueprint, request, abort, current_app
from ..blog_repository import blog_repository
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
    # Add all the new/updated files

    return 'Update processed', 200


def is_valid_signature(payload, header_signature, secret):
    sha_name, signature = header_signature.split('=')
    if sha_name != 'sha1':
        return False

    mac = hmac.new(secret.encode(), msg=payload, digestmod=hashlib.sha1)
    return hmac.compare_digest(mac.hexdigest(), signature)
