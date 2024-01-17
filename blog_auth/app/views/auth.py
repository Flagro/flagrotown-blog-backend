from flask import Blueprint, redirect, url_for, session
from ..auth import oauth
from ..models.user import User


auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/login')
def login():
    redirect_uri = url_for('auth.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@auth_bp.route('/authorize')
def authorize():
    token = oauth.google.authorize_access_token()
    resp = oauth.google.get('userinfo', token=token)
    user_info = resp.json()
    user = User.find_or_create(user_info['email'], user_info['name'])

    session['user_id'] = user.id
    return 'Logged in as: ' + user_info['email']


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))
