import pytest
from app import app
from app import db
from models import *
from flask import url_for
from flask_bcrypt import generate_password_hash
from b_test import client

class TestExceptionAdmin:

    def test_post_session_error(self, get_sess, get_token_customer):
        res = app.test_client().post(f'/session', json=get_sess[0], headers={"Authorization": f"Bearer {get_token_customer}"})
        assert res.status_code == 403
        assert res.json == {'error': 'Access is denied'}

    def test_post_session_validation_error(self, get_sess, get_token_admin):
        res = client.post('/session', json=get_sess[2], headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert res.status_code == 400
        assert res.json == {"startTim": ["Unknown field."],"startTime": ["Missing data for required field."]}

    def test_post_session_price_error(self, get_sess, get_token_admin):
        res = app.test_client().post(f'/session', json=get_sess[1], headers={"Authorization": f"Bearer {get_token_admin}"})
        assert res.status_code == 400
        assert res.json == {"message": "Price is < 0"}

    def test_session_post_film_not_found(self, get_sess, get_token_admin):
        response = client.post(f'/session', json=get_sess[3], headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert response.status_code == 404
        assert response.data ==  b'{"error":"Film not found"}\n'

    def test_session_post_room_not_found(self, get_sess, get_token_admin):
        response = client.post(f'/session', json=get_sess[4], headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert response.status_code == 404
        assert response.data == b'{"error":"Room not found"}\n'




class TestSchedule:
    def test_schedule_create_error_not_exist(self, get_schedule, get_token_admin):
        response = client.post('/schedule/2023-01-11', json=get_schedule[4], headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert response.status_code == 404
        assert response.data == b'{"error":"sessions not found"}\n'

    def test_schedule_create_error_validation(self, get_schedule, get_token_admin):
        response = client.post('/schedule', json=get_schedule[2], headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert response.status_code == 400
        assert response.data == b'{"dat":["Unknown field."],"date":["Missing data for required field."]}\n'

    def test_schedule_create_date_error_validation(self, get_schedule, get_token_admin):
        response = client.post('/schedule/2023-01-11', json=get_schedule[2], headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert response.status_code == 400
        assert response.data == b'{"dat":["Unknown field."]}\n'

    


    @pytest.mark.slow
    def test_get_schedule_by_date_ticket(self, get_token_admin):
        res = client.get(f'/schedule/2022-11-11/tickets', headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert res.status_code == 200

class TestTickets:
    def test_get_user_tickets(self, get_user, get_token_customer, get_ticket):
        get_user = session.query(Users).filter(Users.id == get_ticket[0]["userId"]).first()
        res = client.get(f'/user/{get_user.id}/tickets', headers={'Authorization': 'Bearer ' + str(get_token_customer)})
        assert res.status_code == 200

    def test_get_session_tickets(self, get_user, get_token_admin):
        res = client.get(f'/session/tickets/1', headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert res.status_code == 200

    def test_delete_ticket_error(self, get_token_customer):
        res = client.delete(f'/ticket/1', headers={'Authorization': 'Bearer ' + str(get_token_customer)})
        assert res.status_code == 403
        assert res.json == {'error': 'Access is denied'}

    def test_ticket_delete_id_not_found(self, get_sess, get_token_admin):
        response = client.delete(f'/ticket/100', headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert response.status_code == 404
        assert response.data == b'{"error":"Ticket not found"}\n'

class TestPutSession:
    def test_session_update(self, get_sess, get_token_admin):
        response = app.test_client().put(f'/session/1', json=get_sess[5], headers={"Authorization": f"Bearer {get_token_admin}"})
        assert response.status_code == 200
    def test_session_put_id_not_found(self, get_sess, get_token_admin):
        response = client.put(f'/session/8', json=get_sess[5], headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert response.status_code == 404
        assert response.data == b'{"error":"Session does not exist"}\n'

    def test_session_put_film_not_found(self, get_sess, get_token_admin):
        response = client.put(f'/session/1', json=get_sess[3], headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert response.status_code == 404
        assert response.data ==  b'{"error":"Film not found"}\n'
    def test_session_put_room_not_found(self, get_sess, get_token_admin):
        response = client.put(f'/session/1', json=get_sess[4], headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert response.status_code == 404
        assert response.data == b'{"error":"Room not found"}\n'

    
    
