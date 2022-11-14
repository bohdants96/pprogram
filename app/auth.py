import app.db as db
from models import *
from flask_jwt_extended import get_jwt_identity
from flask import jsonify


def check_admin_auth():
    current_identity_username = get_jwt_identity()
    userA = db.session.query(Users).filter_by(userName=current_identity_username).first()

    if userA.userStatus != 2:
        return jsonify({'error': 'Access is denied'}), 403


def check_manager_or_admin_auth():
    current_identity_username = get_jwt_identity()
    userA = db.session.query(Users).filter_by(userName=current_identity_username).first()

    if userA.userStatus == 0:
        return jsonify({'error': 'Access is denied'}), 403


def user_check_auth(user_id):
    current_identity_username = get_jwt_identity()
    userA = db.session.query(Users).filter_by(userName=current_identity_username).first()

    user = db.session.query(Users).filter_by(id=user_id).first()

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    if user.userName != userA.userName:
        return jsonify({'error': 'Access is denied'}), 403


def user_manager_admin_check_auth(user_id):
    current_identity_username = get_jwt_identity()
    userA = db.session.query(Users).filter_by(userName=current_identity_username).first()

    user = db.session.query(Users).filter_by(id=user_id).first()

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    if user.userName != userA.userName and userA.userStatus == 0:
        return jsonify({'error': 'Access is denied'}), 403