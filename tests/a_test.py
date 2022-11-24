import pytest
from app import app
from app import db
from models import *
from flask import url_for
from flask_bcrypt import generate_password_hash
from b_test import client


class TestCreateObjects:
    @pytest.mark.slow
    def test_user_create(self, wrapper, get_user):
        response = client.post('/user', json=get_user[0])
        response = client.post('/user', json=get_user[1])
        assert response.status_code == 200
    @pytest.mark.slow
    def test_tag_create(self, get_tag, get_token_admin):
        response = client.post('/tag', json=get_tag[0], headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        response = client.post('/tag', json=get_tag[1], headers={'Authorization': 'Bearer ' + str(get_token_admin)})

        assert response.status_code == 200
    @pytest.mark.slow
    def test_film_create(self, get_film, get_token_admin):
        response = client.post('/film', json=get_film[0], headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        response = client.post('/film', json=get_film[1], headers={'Authorization': 'Bearer ' + str(get_token_admin)})

        assert response.status_code == 200
    

    def test_tag_create_unauth(self, get_tag, get_token_customer):
        response = client.post('/tag', json=get_tag[2], headers={'Authorization': 'Bearer ' + str(get_token_customer)})
        assert response.status_code == 403
        assert response.json == {'error': 'Access is denied'}

    def test_film_create_unauth(self, get_film, get_token_customer):
        response = client.post('/film', json=get_film[0], headers={'Authorization': 'Bearer ' + str(get_token_customer)})
        assert response.status_code == 403
        assert response.json == {'error': 'Access is denied'}

    @pytest.mark.slow
    def test_room_create(self, get_room, get_token_admin):
        response = client.post('/room', json=get_room[0], headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        response = client.post('/room', json=get_room[1], headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert response.status_code == 200

    @pytest.mark.slow
    def test_session_create(self, get_sess, get_token_admin):
        response = client.post('/session', json=get_sess[0], headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        response = client.post('/session', json=get_sess[6], headers={'Authorization': 'Bearer ' + str(get_token_admin)})

        assert response.status_code == 200

    @pytest.mark.slow
    def test_sell_create(self, get_ticket, get_token_admin):
        response = client.post('/user/sell', json=get_ticket[0], headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert response.status_code == 200

    @pytest.mark.slow
    def test_schedule_create(self, get_schedule, get_token_admin):
        response = client.post('/schedule', json=get_schedule[0], headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert response.status_code == 200

    @pytest.mark.slow
    def test_schedule_create_date(self, get_schedule, get_token_admin):
        response = client.post('/schedule/2023-01-11', json=get_schedule[3], headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert response.status_code == 200