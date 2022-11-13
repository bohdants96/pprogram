from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, ValidationError, validate
from flask_bcrypt import Bcrypt
from models import Films, FilmTag, Tags
import app.db as db
import app.views.tag as tg
from flask_jwt_extended import *
from app.auth import check_admin_auth, check_manager_or_admin_auth

film_blueprint = Blueprint('film', __name__, url_prefix='/film')
bcrypt = Bcrypt()


@film_blueprint.route('', methods=['POST'])
@jwt_required
def create_film():
    res = check_admin_auth()
    if res is not None:
        return res
    try:
        class FilmToCreate(Schema):
            name = fields.String(required=True)
            duration = fields.Integer(required=True)
            status = fields.Str(validate=validate.OneOf(["incoming", "in rent", "out of date"]))
            tags = fields.List(fields.Integer())

        FilmToCreate().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    film = Films(name=request.json['name'], duration=request.json['duration'],
                 status=request.json['status'])

    tagsId = []
    for i in range(len(request.json['tags'])):
        tagsId.append(request.json['tags'][i])
    for i in range(len(request.json['tags'])):
        tag = db.session.query(Tags).filter_by(id=tagsId[i]).first()
        if tag is None:
            return jsonify({'error': 'Tag not found'}), 404

    try:
        db.session.add(film)
    except:
        db.session.rollback()
        return jsonify({"message": "Error film create"}),500
    db.session.commit()

    for i in range(len(request.json['tags'])):
        tagsId.append(request.json['tags'][i])
    for i in range(len(request.json['tags'])):
        tag = db.session.query(Tags).filter_by(id=tagsId[i]).first()
        filmTag = FilmTag(filmId=film.id, tagId=tagsId[i])

        try:
            db.session.add(filmTag)
        except:
            db.session.rollback()
            return jsonify({"message": "Error filmTag create"}),500
    db.session.commit()
    return get_film(film.id)
    # return jsonify(len(request.json['tags']))


@film_blueprint.route('/<int:film_id>', methods=['GET'])
@jwt_required
def get_film(film_id):
    res = check_manager_or_admin_auth()
    if res is not None:
        return res
    film = db.session.query(Films).filter_by(id=film_id).first()
    if film is None:
        return jsonify({'error': 'Film not found'}), 404

    res_json = {
        'id': film.id,
        'name': film.name,
        'duration': film.duration,
        'status': film.status
    }
    return jsonify(res_json), 200


@film_blueprint.route('/<int:film_id>', methods=['DELETE'])
@jwt_required
def delete_film(film_id):
    res = check_admin_auth()
    if res is not None:
        return res
    film = db.session.query(Films).filter_by(id=film_id).first()
    if film is None:
        return jsonify({'error': 'Film not found'}), 404
    filmTags = db.session.query(FilmTag).filter_by(filmId=film_id).all()
    if filmTags is None:
        return jsonify({'error': 'Film`s tags not found'}), 404
    try:
        for filmTag in filmTags:
            db.session.delete(filmTag)
        db.session.delete(film)
    except:
        db.session.rollback()
        return jsonify({"Film data is not valid"}), 400

    db.session.commit()

    return "", 204


@film_blueprint.route('/findByStatus/<string:film_status>', methods=['GET'])
@jwt_required
def get_film_by_status(film_status):
    res = check_manager_or_admin_auth()
    if res is not None:
        return res
    res = []
    films = db.session.query(Films).filter_by(status=film_status).all()
    if films is None:
        return jsonify({'error': 'Films not found'}), 404

    for film in films:
        res_json = {
            'id': film.id,
            'name': film.name,
            'duration': film.duration,
            'status': film.status
        }
        res.append(res_json)
    return jsonify(res), 200


@film_blueprint.route('/findByTag/<string:film_tag>', methods=['GET'])
@jwt_required
def get_film_by_tag(film_tag):
    res = check_manager_or_admin_auth()
    if res is not None:
        return res
    res = []
    tagIds = db.session.query(Tags).filter_by(name=film_tag).first()
    if tagIds is None:
        return jsonify({'error': 'Tag not found'}), 404

    resFilmId = db.session.query(FilmTag).filter_by(tagId=tagIds.id).all()
    if resFilmId is None:
        return jsonify({'error': 'Films not found'}), 404
    for j in range(len(resFilmId)):
        films = db.session.query(Films).filter_by(id=resFilmId[j].filmId).first()
        res_json = {
            'id': films.id,
            'name': films.name,
            'duration': films.duration,
            'status': films.status
        }
        res.append(res_json)
    return jsonify(res), 200


@film_blueprint.route('/<int:film_id>', methods=['PUT'])
@jwt_required
def update_film(film_id):
    res = check_admin_auth()
    if res is not None:
        return res
    try:
        class FilmToUpdate(Schema):
            name = fields.String()
            duration = fields.Integer()
            status = fields.Str(validate=validate.OneOf(["incoming", "in rent", "out of date"]))

        if not request.json:
            raise ValidationError('No input data provided')
        FilmToUpdate().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    film = db.session.query(Films).filter(Films.id == film_id).first()

    if film is None:
        return jsonify({'error': 'User does not exist'}), 404

    try:
        if 'name' in request.json:
            film.name = request.json['name']
        if 'duration' in request.json:
            film.duration = request.json['duration']
        if 'status' in request.json:
            film.status = request.json['status']
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"Film Data is not valid"}), 400

    db.session.commit()

    return get_film(film_id)
