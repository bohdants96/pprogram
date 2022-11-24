from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, ValidationError, validate
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash
from models import Users, Tickets, Sessions
from flask_jwt import current_identity
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, get_jti
import app.db as db
from app.auth import check_admin_auth, check_manager_or_admin_auth, user_manager_admin_check_auth, user_check_auth

from datetime import timedelta
import redis

user_blueprint = Blueprint('user', __name__, url_prefix='/user')
bcrypt = Bcrypt()

ACCESS_EXPIRES = timedelta(hours=1)

jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=5000, db=0, decode_responses=True
)


@user_blueprint.route('', methods=['POST'])
def create_user():
    try:
        class UserToCreate(Schema):
            userName = fields.String(required=True)
            firstName = fields.String(required=True)
            lastName = fields.String(required=True)
            email = fields.Email(required=True)
            password = fields.String(required=True)
            phone = fields.Integer(required=True)
            userStatus = fields.Integer(required=True)

        UserToCreate().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    users = db.session.query(Users).filter_by(userName=request.json['userName']).all()
    if len(users) > 0:
        return jsonify({"message": "Username is used"}), 400
    if len(request.json['password']) < 8:
        return jsonify({"message": "Password is too short"}), 400
    user = Users(userName=request.json['userName'], firstName=request.json['firstName'],
                 lastName=request.json['lastName'], email=request.json['email'],
                 password=bcrypt.generate_password_hash(request.json['password']).decode('utf-8'),
                 phone=request.json['phone'], userStatus=request.json['userStatus'])
    #try:
    db.session.add(user)
    # except:
    #     db.session.rollback()
    #     return jsonify({"message": "Error user create"}), 500
    db.session.commit()

    user = db.session.query(Users).filter_by(id=user.id).first()
    res_json = {'id': user.id,
                'email': user.email,
                'username': user.userName,
                'firstName': user.firstName,
                'lastName': user.lastName}

    return jsonify(res_json), 200


@user_blueprint.route('/<int:user_id>', methods=['GET'])
@jwt_required
def get_user(user_id):
    res = user_manager_admin_check_auth(user_id)
    if res is not None:
        return res

    user = db.session.query(Users).filter_by(id=user_id).first()
    res_json = {'id': user.id,
                'email': user.email,
                'username': user.userName,
                'firstName': user.firstName,
                'lastName': user.lastName}

    return jsonify(res_json), 200


@user_blueprint.route('/<int:user_id>', methods=['PUT'])
@jwt_required
def update_user(user_id):
    res = user_check_auth(user_id)
    if res is not None:
        return res

    try:
        class UserToUpdate(Schema):
            userName = fields.String()
            firstName = fields.String()
            lastName = fields.String()
            email = fields.Email()
            password = fields.String()
            phone = fields.Integer()

        # if not request.json:
        #     raise ValidationError('No input data provided')
        UserToUpdate().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    user1 = db.session.query(Users).filter_by(id=user_id).all()

    username = None
    username = request.json['userName']
    if username is not None:
        users = db.session.query(Users).filter_by(userName=username).all()
        if len(users)> 0 and users[0].id != user_id:
            return jsonify({"message": "Username is used"}), 400

    user = db.session.query(Users).filter(Users.id == user_id).first()

    if user is None:
        return jsonify({'error': 'User does not exist'}), 404

    # try:
    if 'userName' in request.json:
        user.userName = request.json['userName']
    if 'firstName' in request.json:
        user.firstName = request.json['firstName']
    if 'lastName' in request.json:
        user.lastName = request.json['lastName']
    if 'email' in request.json:
        user.email = request.json['email']
    if 'password' in request.json:
        user.password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
    if 'phone' in request.json:
            user.phone = request.json['phone']
    # except:
    #     db.session.rollback()
    #     return jsonify({"User Data is not valid"}), 400

    db.session.commit()

    #return get_user(user_id)
    return jsonify({"message":"User was updated"}), 200


@user_blueprint.route('/<int:user_id>', methods=['DELETE'])
@jwt_required
def delete_user(user_id):
    res = user_check_auth(user_id)
    if res is not None:
        return res

    user = db.session.query(Users).filter_by(id=user_id).first()
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    # try:
    db.session.delete(user)
    # except:
    #     db.session.rollback()
    #     return jsonify({"User data is not valid"}), 400

    db.session.commit()

    return jsonify({"message":"User was deleted"}), 200


@user_blueprint.route('/login', methods=['POST'])
def login():
    try:
        class UserToLogin(Schema):
            username = fields.String(required=True)
            password = fields.String(required=True)
        user = UserToLogin().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    user_db = db.session.query(Users).filter(Users.userName == user['username']).first()

    if user_db is None:
        return jsonify({'error': 'User not found'}), 401

    if user is not None and check_password_hash(user_db.password, user['password']):
        access_token = create_access_token(identity=user_db.userName, expires_delta=timedelta(days=2))
        return jsonify({'token': access_token}), 200

    return jsonify({'error': 'Could not verify user'}), 401


@user_blueprint.route('/logout', methods=['GET'])
@jwt_required
def logout():
    jti = get_jti(request.headers.get('Authorization', None).split()[1])
    #jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    return jsonify(msg="Access token revoked")


@user_blueprint.route('/sell', methods=['POST'])
@jwt_required
def sell():
    res = check_manager_or_admin_auth()
    if res is not None:
        return res
    try:
        class TicketToCreate(Schema):
            userId = fields.Integer(required=True)
            sessionId = fields.Integer(required=True)
            seatNum = fields.Integer(required=True)
            date = fields.Date(required=True)

        TicketToCreate().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    user = db.session.query(Users).filter_by(id=request.json['userId']).first()
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    session = db.session.query(Sessions).filter_by(id=request.json['sessionId']).first()
    if session is None:
        return jsonify({'error': 'Session not found'}), 404
    ticket = Tickets(userId=request.json['userId'], sessionId=request.json['sessionId'],
                     seatNum=request.json['seatNum'], date=request.json['date'])
    #try:
    db.session.add(ticket)
    # except:
    #     db.session.rollback()
    #     return jsonify({"message": "Error ticket create"}), 500
    db.session.commit()

    ticket = db.session.query(Tickets).filter_by(id=ticket.id).first()
    res = {'id': ticket.id,
           'userId': ticket.userId,
           'sessionId': ticket.sessionId,
           'seatNum': ticket.seatNum,
           'date': ticket.date}

    return jsonify(res), 200



@user_blueprint.route('/<int:user_id>/tickets', methods=['GET'])
@jwt_required
def get_tickets(user_id):
    res = user_manager_admin_check_auth(user_id)
    if res is not None:
        return res

    user = db.session.query(Users).filter_by(id=user_id).first()
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    tickets = db.session.query(Tickets).filter_by(userId=user_id).all()
    if tickets is None:
        return jsonify({'error': 'User not found'}), 404
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
