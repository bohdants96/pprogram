import pytest
from app import app
from app import db
from models import *
from flask import url_for
from flask_bcrypt import generate_password_hash
from b_test import client


class TestDeleteObjects:
    @pytest.mark.slow
    def test_schedule_ticket(self, get_token_admin):
        res = client.delete(f'/schedule/2022-11-11', headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert res.status_code == 204

    def test_tag_delete(self, get_token_admin, get_tag):
        tag = session.query(Tags).filter(Tags.name == get_tag[1]["name"]).first()
        response = client.delete(f'/tag/{tag.id}', headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert response.status_code == 204

    def test_film_delete(self, get_token_admin):
        response = client.delete(f'/film/1', headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert response.status_code == 204

    def test_room_delete(self, get_token_admin, get_room):
        delete_room = session.query(Rooms).filter(Rooms.name == get_room[0]["name"]).first()
        response = client.delete(f'/room/{delete_room.id}', headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert response.status_code == 204
    
    @pytest.mark.slow
    def test_session_delete(self, get_token_admin, get_room):
        response = client.delete(f'/session/1', headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert response.status_code == 204
    @pytest.mark.slow
    def test_delete_ticket(self, get_token_admin):
        res = client.delete(f'/ticket/1', headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert res.status_code == 204

    @pytest.mark.slow
    def test_logout(self, get_user, get_token_admin):
        res = client.get(f'/user/logout', headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert res.json == {"msg": "Access token revoked"}

    @pytest.mark.slow
    def test_user_delete(self, get_token_admin, get_user):
        delete_user = session.query(Users).filter(Users.userName == get_user[0]["userName"]).first()
        response = client.delete(f'/user/{delete_user.id}', headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert response.status_code == 200
        assert response.json == {'message': 'User was deleted'}

    
