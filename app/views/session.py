from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, ValidationError, validate
from flask_bcrypt import Bcrypt
from pprogram.models import Sessions, Tickets, Films, Rooms
import pprogram.app.db as db

session_blueprint = Blueprint('session', __name__, url_prefix='/session')
bcrypt = Bcrypt()


@session_blueprint.route('', methods=['POST'])
def create_session():
    try:
        class SessionToCreate(Schema):
            startTime = fields.DateTime(required=True)
            filmId = fields.Integer(required=True)
            roomId = fields.Integer(required=True)
            pricePerTicket = fields.Integer(required=True)

        SessionToCreate().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    if request.json['pricePerTicket'] < 0:
        return jsonify({"message": "Price is < 0"}), 400
    film = db.session.query(Films).filter_by(id=request.json['filmId']).first()
    if film is None:
        return jsonify({'error': 'Film not found'}), 404
    room = db.session.query(Rooms).filter_by(id=request.json['roomId']).first()
    if room is None:
        return jsonify({'error': 'Room not found'}), 404
    session = Sessions(startTime=request.json['startTime'], filmId=request.json['filmId'],
                       roomId=request.json['roomId'], pricePerTicket=request.json['pricePerTicket'])
    try:
        db.session.add(session)
    except:
        db.session.rollback()
        return jsonify({"message": "Error session create"}), 500
    db.session.commit()
    return get_session(session.id)


@session_blueprint.route('/<int:session_id>', methods=['GET'])
def get_session(session_id):
    session = db.session.query(Sessions).filter_by(id=session_id).first()
    if session is None:
        return jsonify({'error': 'Session not found'}), 404

    res_json = {'id': session.id,
                'startTime': session.startTime,
                'filmId': session.filmId,
                'roomId': session.roomId,
                'pricePerTicket': session.pricePerTicket
                }

    return jsonify(res_json), 200


@session_blueprint.route('/<int:session_id>', methods=['PUT'])
def update_session(session_id):
    try:
        class SessionToUpdate(Schema):
            startTime = fields.DateTime()
            filmId = fields.Integer()
            roomId = fields.Integer()
            pricePerTicket = fields.Integer()

        if not request.json:
            raise ValidationError('No input data provided')
        SessionToUpdate().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    session = db.session.query(Sessions).filter(Sessions.id == session_id).first()

    if session is None:
        return jsonify({'error': 'Session does not exist'}), 404
    film = db.session.query(Films).filter_by(id=request.json['filmId']).first()
    if film is None:
        return jsonify({'error': 'Film not found'}), 404
    room = db.session.query(Rooms).filter_by(id=request.json['roomId']).first()
    if room is None:
        return jsonify({'error': 'Room not found'}), 404
    try:
        if 'startTime' in request.json:
            session.startTime = request.json['startTime']
        if 'filmId' in request.json:
            session.filmId = request.json['filmId']
        if 'roomId' in request.json:
            session.roomId = request.json['roomId']
        if 'pricePerTicket' in request.json:
            session.pricePerTicket = request.json['pricePerTicket']

    except:
        db.session.rollback()
        return jsonify({"Session Data is not valid"}), 400

    db.session.commit()

    return get_session(session_id)


@session_blueprint.route('/<int:session_id>', methods=['DELETE'])
def delete_session(session_id):
    session = db.session.query(Sessions).filter_by(id=session_id).first()
    if session is None:
        return jsonify({'error': 'Session not found'}), 404

    try:
        db.session.delete(session)
    except:
        db.session.rollback()
        return jsonify({"Session data is not valid"}), 400

    db.session.commit()

    return "", 204


@session_blueprint.route('/tickets/<int:session_id>', methods=['GET'])
def get_tickets_session(session_id):
    tickets = db.session.query(Tickets).filter_by(sessionId=session_id).all()
    if tickets is None:
        return jsonify({'error': 'Session not found'}), 404
    res = []
    for ticket in tickets:
        res_json = {'id': ticket.id,
                    'userId': ticket.userId,
                    'sessionId': ticket.sessionId,
                    'seatNum': ticket.seatNum,
                    'date': ticket.date
                    }
        res.append(res_json)

    return jsonify(res), 200