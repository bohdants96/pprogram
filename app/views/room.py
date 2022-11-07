from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, ValidationError, validate
from flask_bcrypt import Bcrypt
from pprogram.models import Rooms
import pprogram.app.db as db
import pprogram.app.views.tag as tg

room_blueprint = Blueprint('room', __name__, url_prefix='/room')
bcrypt = Bcrypt()


@room_blueprint.route('',methods=['POST'])
def create_room():
    try:
        class RoomToCreate(Schema):
            name = fields.String(required=True)
            numOfSeats = fields.Integer(required=True)
        RoomToCreate().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    if request.json['numOfSeats']<0:
        return ({"message": "numOfSeats < 0"}), 400
    room = Rooms(name=request.json['name'], numOfSeats=request.json['numOfSeats'])

    try:
        db.session.add(room)
    except:
        db.session.rollback()
        return jsonify({"message": "Error room create"}), 500
    db.session.commit()
    return get_room(room.id)


@room_blueprint.route('/<int:room_id>', methods=['GET'])
def get_room(room_id):
    room = db.session.query(Rooms).filter_by(id=room_id).first()
    if room is None:
        return jsonify({'error': 'User not found'}), 404

    res_json = {'id': room.id,
                'name': room.name,
                'numOfSeats': room.numOfSeats
                }

    return jsonify(res_json), 200


@room_blueprint.route('/<int:room_id>',methods=['DELETE'])
def delete_room(room_id):
    room = db.session.query(Rooms).filter_by(id=room_id).first()
    if room is None:
        return jsonify({'error': 'Room not found'}), 404
    try:
        db.session.delete(room)
    except:
        db.session.rollback()
        return jsonify({"Film data is not valid"}), 400

    db.session.commit()

    return "", 204


@room_blueprint.route('/<int:room_id>',methods=['PUT'])
def update_room(room_id):
    try:
        class RoomToUpdate(Schema):
            name = fields.String()
            numOfSeats = fields.Integer()

        if not request.json:
            raise ValidationError('No input data provided')
        RoomToUpdate().load(request.json)

    except ValidationError as err:
        return jsonify(err.messages), 400
    if request.json['numOfSeats']<0:
        return ({"message": "numOfSeats < 0"}), 400
    room = db.session.query(Rooms).filter(Rooms.id == room_id).first()

    if room is None:
        return jsonify({'error': 'Room does not exist'}), 404

    try:
        if 'name' in request.json:
            room.name = request.json['name']
        if 'numOfSeats' in request.json:
            room.numOfSeats = request.json['numOfSeats']
    except:
        db.session.rollback()
        return jsonify({"User Data is not valid"}), 400

    db.session.commit()

    return get_room(room_id)