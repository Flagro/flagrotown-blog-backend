from flask import Blueprint, redirect, url_for, session
from auth_service.app import oauth, db
from auth_service.models.user import User, db


auth = Blueprint('auth', __name__)


def find_or_create_user(email, name):
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, name=name)
        db.session.add(user)
        db.session.commit()
    return user


@auth.route('/login')
def login():
    redirect_uri = url_for('auth.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@auth.route('/authorize')
def authorize():
    token = oauth.google.authorize_access_token()
    resp = oauth.google.get('userinfo')
    user_info = resp.json()
    user = find_or_create_user(user_info['email'], user_info['name'])

    session['user_id'] = user.id
    return 'Logged in as: ' + user_info['email']

@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))
