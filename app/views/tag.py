from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, ValidationError
from flask_bcrypt import Bcrypt
from pprogram.models import Tags, FilmTag
import pprogram.app.db as db

tag_blueprint = Blueprint('tag', __name__, url_prefix='/tag')
bcrypt = Bcrypt()


@tag_blueprint.route('', methods=['POST'])
def create_tag():
    try:
        class TagToCreate(Schema):
            name = fields.String(required=True)
        TagToCreate().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    tag = Tags(name=request.json['name'])
    try:
        db.session.add(tag)
    except:
        db.session.rollback()
        return jsonify({"message": "Error tag create"}), 500
    db.session.commit()
    return get_tag(tag.id)


@tag_blueprint.route('/<int:tag_id>', methods=['GET'])
def get_tag(tag_id):
    tag = db.session.query(Tags).filter_by(id=tag_id).first()
    if tag is None:
        return jsonify({'error': 'Tag not found'}), 404

    res_json = {
        'id': tag.id,
        'name': tag.name
    }
    return jsonify(res_json), 200


@tag_blueprint.route('/<int:tag_id>', methods=['PUT'])
def update_tag(tag_id):
    try:
        class TagToUpdate(Schema):
            name = fields.String(required=False)

        if not request.json:
            raise ValidationError('No input data provided')
        TagToUpdate().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    tag = db.session.query(Tags).filter(Tags.id == tag_id).first()

    if tag is None:
        return jsonify({'error': 'Tag does not exist'}), 404

    try:
        if 'name' in request.json:
            tag.name = request.json['name']
    except:
        db.session.rollback()
        return jsonify({"Tag Data is not valid"}), 400

    db.session.commit()

    return get_tag(tag_id)


@tag_blueprint.route('/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    filmTags = db.session.query(FilmTag).filter_by(tagId=tag_id).all()
    tag = db.session.query(Tags).filter_by(id=tag_id).first()
    if tag is None:
        return jsonify({'error': 'Tag not found'}), 404

    try:
        for filmTag in filmTags:
            db.session.delete(filmTag)
        db.session.delete(tag)
    except:
        db.session.rollback()
        return jsonify({"Tag data is not valid"}), 400

    db.session.commit()

    return "", 204
