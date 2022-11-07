from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, ValidationError, validate
from flask_bcrypt import Bcrypt
from pprogram.models import Tickets
import pprogram.app.db as db

ticket_blueprint = Blueprint('ticket', __name__, url_prefix='/ticket')
bcrypt = Bcrypt()


@ticket_blueprint.route('/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    ticket = db.session.query(Tickets).filter_by(id=ticket_id).first()
    if ticket is None:
        return jsonify({'error': 'Ticket not found'}), 404

    try:
        db.session.delete(ticket)
    except:
        db.session.rollback()
        return jsonify({"Ticket data is not valid"}), 400

    db.session.commit()

    return "", 204
