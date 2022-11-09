from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, ValidationError, validate
from flask_bcrypt import Bcrypt
from pprogram.models import Schedules, schedule_session, Sessions, Tickets
import pprogram.app.db as db
import datetime

schedule_blueprint = Blueprint('schedule', __name__, url_prefix='/schedule')
bcrypt = Bcrypt()


@schedule_blueprint.route('', methods=['POST'])
def create_schedule():
    try:
        class ScheduleToCreate(Schema):
            date = fields.Date(required=True)
            sessions = fields.List(fields.Integer())

        ScheduleToCreate().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    schedule = Schedules(date=request.json['date'])
    try:
        db.session.add(schedule)
    except:
        db.session.rollback()
        return jsonify({"message": "Error schedule create"}), 500
    db.session.commit()
    sessionId = []
    for i in range(len(request.json['sessions'])):
        sessionId.append(request.json['sessions'][i])
    for i in range(len(request.json['sessions'])):
        sessions = db.session.query(Sessions).filter_by(id=sessionId[i]).first()
        if sessions is None:
            return jsonify({'error': 'sessions not found'}), 404
        scheduleSession = schedule_session(scheduleId=schedule.id, sessionId=sessionId[i])
        try:
            db.session.add(scheduleSession)
        except:
            db.session.rollback()
            return jsonify({"message": "Error scheduleSession create"}), 500
    db.session.commit()
    return get_schedule(schedule.id)


@schedule_blueprint.route('/<int:schedule_id>', methods=['GET'])
def get_schedule(schedule_id):
    schedule = db.session.query(Schedules).filter_by(id=schedule_id).first()
    if schedule is None:
        return jsonify({'error': 'Schedule not found'}), 404
    sessions = db.session.query(schedule_session).filter_by(scheduleId=schedule_id).all()
    res_ses = []
    for session in sessions:
        res_session = {
            'idSessionSchedule': session.id
        }
        res_ses.append(res_session)
    res_json = {
        'id': schedule.id,
        'date': schedule.date,
        'sessions': res_ses

    }
    return jsonify(res_json), 200


@schedule_blueprint.route('/<string:date>', methods=['POST'])
def create_schedule_date(date):
    try:
        class ScheduleToCreate(Schema):
            sessions = fields.List(fields.Integer())

        ScheduleToCreate().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    schedule = Schedules(date=date)
    try:
        db.session.add(schedule)
    except:
        db.session.rollback()
        return jsonify({"message": "Error schedule create"}), 500
    db.session.commit()
    sessionId = []
    for i in range(len(request.json['sessions'])):
        sessionId.append(request.json['sessions'][i])
    for i in range(len(request.json['sessions'])):
        sessions = db.session.query(Sessions).filter_by(id=sessionId[i]).first()
        if sessions is None:
            delete_schedule(date)
            return jsonify({'error': 'sessions not found'}), 404
        scheduleSession = schedule_session(scheduleId=schedule.id, sessionId=sessionId[i])
        try:
            db.session.add(scheduleSession)
        except:
            db.session.rollback()
            return jsonify({"message": "Error scheduleSession create"}), 500
    db.session.commit()
    return get_schedule(schedule.id)


@schedule_blueprint.route('/<string:date>', methods=['PUT'])
def update_schedule(date):
    try:
        class ScheduleToUpdate(Schema):
            sessions = fields.List(fields.Integer())

        if not request.json:
            raise ValidationError('No input data provided')
        ScheduleToUpdate().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    schedule = db.session.query(Schedules).filter(Schedules.date == date).first()

    if schedule is None:
        return jsonify({'error': 'Schedule does not exist'}), 404

    try:
        if 'sessions' in request.json:
            sessionId = []
            for i in range(len(request.json['sessions'])):
                sessionId.append(request.json['sessions'][i])
            for i in range(len(request.json['sessions'])):
                sessions = db.session.query(Sessions).filter_by(id=sessionId[i]).first()
                if sessions is None:
                    delete_schedule(date)
                    return jsonify({'error': 'sessions not found'}), 404
                scheduleSession = schedule_session(scheduleId=schedule.id, sessionId=sessionId[i])
                db.session.add(scheduleSession)
    except:
        db.session.rollback()
        return jsonify({"Schedule Data is not valid"}), 400

    db.session.commit()

    return get_schedule(schedule.id)


@schedule_blueprint.route('/<string:date>', methods=['DELETE'])
def delete_schedule(date):
    schedules = db.session.query(Schedules).filter(date == date).all()
    if schedules is None:
        return jsonify({'error': 'Session not found'}), 404
    for schedule in schedules:
        schedule_s = db.session.query(schedule_session).filter_by(scheduleId=schedule.id).all()
        if schedule_s is None:
            return jsonify({'error': 'Film`s tags not found'}), 404
        try:
            for schedule_ss in schedule_s:
                db.session.delete(schedule_ss)
            db.session.commit()
            db.session.delete(schedule)
        except:
            db.session.rollback()
            return jsonify({"Session data is not valid"}), 400

        db.session.commit()

    return "", 204


@schedule_blueprint.route('/<string:date>', methods=['GET'])
def get_schedule_date(date):
    schedule = db.session.query(Schedules).filter(Schedules.date==date).first()
    if schedule is None:
        return jsonify({'error': 'Schedule not found'}), 404
    sessions = db.session.query(schedule_session).filter_by(scheduleId=schedule.id).all()
    res_ses = []
    for session in sessions:
        res_session = {
            'idSessionSchedule': session.id
        }
        res_ses.append(res_session)
    res_json = {
        'id': schedule.id,
        'date': schedule.date,
        'sessions': res_ses

    }
    return jsonify(res_json), 200


# to rewrite
@schedule_blueprint.route('/tickets/<string:date>', methods=['GET'])
def get_tickets_session(date):
    schedule = db.session.query(Schedules).filter(Schedules.date==date).first()
    if schedule is None:
        return jsonify({'error': 'Schedule not found'}), 404
    res_j = []
    sessions = db.session.query(schedule_session).filter_by(scheduleId=schedule.id).all()
    if len(sessions) == 0:
        return jsonify({'error': 'Sessions not found'}), 404
    for session in sessions:
        tickets = db.session.query(Tickets).filter_by(sessionId=session.id).all()
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
            res.append(jsonify(res_json))
        res_i = {
            "tickets": jsonify(res)
        }
        res_j.append(res_i)

    return jsonify(res_j), 200
