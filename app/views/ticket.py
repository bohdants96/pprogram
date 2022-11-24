from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, ValidationError, validate
from flask_bcrypt import Bcrypt
from models import Tickets
import app.db as db
from app.auth import check_admin_auth
from flask_jwt_extended import jwt_required

ticket_blueprint = Blueprint('ticket', __name__, url_prefix='/ticket')
bcrypt = Bcrypt()


@ticket_blueprint.route('/<int:ticket_id>', methods=['DELETE'])
@jwt_required
def delete_ticket(ticket_id):
    res = check_admin_auth()
    if res is not None:
        return res
    ticket = db.session.query(Tickets).filter_by(id=ticket_id).first()
    if ticket is None:
        return jsonify({'error': 'Ticket not found'}), 404

    db.session.delete(ticket)
    db.session.commit()

    return "", 204
