import pytest
from app import app
from app import db
from models import *
from flask import url_for
from flask_bcrypt import generate_password_hash


client = app.test_client()


    

class TestGetObjects:
    def test_get_user(self, get_user, get_token_customer):
        get_user = session.query(Users).filter(Users.userName == get_user[1]["userName"]).first()
        res = client.get(f'/user/{get_user.id}', headers={'Authorization': 'Bearer ' + str(get_token_customer)})
        assert res.status_code == 200

    def test_get_tag(self, get_tag, get_token_admin):
        tag = session.query(Tags).filter(Tags.name == get_tag[0]["name"]).first()
        res = client.get(f'/tag/{tag.id}', headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert res.status_code == 200

    def test_tag_get_unauth(self, get_tag, get_token_customer):
        tag = session.query(Tags).filter(Tags.name == get_tag[0]["name"]).first()
        res = client.get(f'/tag/{tag.id}', headers={'Authorization': 'Bearer ' + str(get_token_customer)})
        assert res.status_code == 403
        assert res.json == {'error': 'Access is denied'}

    def test_tag_get_id_not_found(self, get_tag, get_token_admin):
        response = client.get(f'/tag/8', headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert response.status_code == 404
        assert response.data == b'{"error":"Tag not found"}\n'


    def test_get_film_findByStatus(self, get_tag, get_token_admin):
        res = client.get(f'/film/findByStatus/in rent', headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert res.status_code == 200

    def test_get_film_findByTag(self, get_tag, get_token_admin):
        res = client.get(f'/film/findByTag/action', headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert res.status_code == 200

    def test_film_get_unauth(self,  get_token_customer):
        response = client.get('/film/1', headers={'Authorization': 'Bearer ' + str(get_token_customer)})
        assert response.status_code == 403
        assert response.json == {'error': 'Access is denied'}

    def test_filmfindByTag_get_unauth(self,  get_token_customer):
        response = client.get('/film/findByTag/action', headers={'Authorization': 'Bearer ' + str(get_token_customer)})
        assert response.status_code == 403
        assert response.json == {'error': 'Access is denied'}

    def test_filmfindByStatus_get_unauth(self,  get_token_customer):
        response = client.get('/film/findByStatus/in rent', headers={'Authorization': 'Bearer ' + str(get_token_customer)})
        assert response.status_code == 403
        assert response.json == {'error': 'Access is denied'}

    def test_room_get_unauth(self, get_token_customer):
        res = client.get(f'/room/1', headers={'Authorization': 'Bearer ' + str(get_token_customer)})
        assert res.status_code == 403
        assert res.json == {'error': 'Access is denied'}

    @pytest.mark.slow
    def test_get_schedule_by_date(self):
        res = client.get(f'schedule/2022-11-11')
        assert res.status_code == 200

    @pytest.mark.slow
    def test_schedule_update(self, get_schedule, get_token_admin):
        response = app.test_client().put(f'/schedule/2022-11-11', json=get_schedule[1], headers={"Authorization": f"Bearer {get_token_admin}"})
        assert response.status_code == 200
    ###sell###
    


class TestUpdateObjects:
    def test_user_update(self, get_user, get_token_customer):
        new_user = session.query(Users).filter(Users.userName == get_user[1]["userName"]).first()
        response = app.test_client().put(f'/user/{new_user.id}', json=get_user[3], headers={"Authorization": f"Bearer {get_token_customer}"})
        assert response.status_code == 200
        assert response.json == {"message":"User was updated"}

    
    def test_tag_update(self, get_tag, get_token_admin):
        tag = session.query(Tags).filter(Tags.name == get_tag[0]["name"]).first()
        response = app.test_client().put(f'/tag/{tag.id}', json=get_tag[2], headers={"Authorization": f"Bearer {get_token_admin}"})
        assert response.status_code == 200

    def test_film_update(self, get_film, get_token_admin):
        response = app.test_client().put(f'/film/1', json=get_film[3], headers={"Authorization": f"Bearer {get_token_admin}"})
        assert response.status_code == 200

    
    def test_room_update(self, get_room, get_token_admin):
        room = session.query(Rooms).filter(Rooms.name == get_room[1]["name"]).first()
        response = app.test_client().put(f'/room/{room.id}', json=get_room[2], headers={"Authorization": f"Bearer {get_token_admin}"})
        assert response.status_code == 200

    def test_tag_put_id_not_found(self, get_tag, get_token_admin):
        response = client.put(f'/tag/8', json=get_tag[2], headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert response.status_code == 404
        assert response.data == b'{"error":"Tag does not exist"}\n'

    def test_put_film_error(self, get_film, get_token_admin):
        res = app.test_client().put(f'/film/1', json=get_film[2], headers={"Authorization": f"Bearer {get_token_admin}"})
        assert res.status_code == 400

    def test_put_room_error(self, get_room, get_token_customer):
        res = app.test_client().put(f'/room/1', json=get_room[2], headers={"Authorization": f"Bearer {get_token_customer}"})
        assert res.status_code == 403
        assert res.json == {'error': 'Access is denied'}

class TestError:
    def test_user_validation_error(self, get_user):
        response = client.post('/user', json=get_user[2])
        assert response.status_code == 400
        assert response.json == {"userNam": ["Unknown field."],"userName": ["Missing data for required field."]}
    
    @pytest.mark.slow
    def test_get_token_customer_error(self, get_user):
        user_to_get = session.query(Users).filter(Users.userName == get_user[0]["userName"]).first()
        resp = client.post('/user/login', json={"usernam": user_to_get.userName, "password": "11111111"})
        assert resp.status_code == 400
        assert resp.json == {"usernam": ["Unknown field."],"username": ["Missing data for required field."]}
        
    def test_user_create_username_used(self, get_user):
        get_user[0]["password"] = "XXX"
        get_user[0]["userName"] = "user"
        response = client.post('/user', json=get_user[0])
        assert response.status_code == 400
        assert response.json == {"message": "Password is too short"}

    
    ########################PUT#############################
    def test_put_tag_error(self, get_tag, get_token_admin):
        res = app.test_client().put(f'/tag/1', json=get_tag[3], headers={"Authorization": f"Bearer {get_token_admin}"})
        assert res.status_code == 400
        assert res.json == {'nam': ['Unknown field.']}

    def test_put_room_validation_error(self, get_room, get_token_admin):
        res = app.test_client().put(f'/room/1', json=get_room[3], headers={"Authorization": f"Bearer {get_token_admin}"})
        assert res.status_code == 400
        assert res.json == {'nam': ['Unknown field.']}

    def test_put_room_error(self, get_room, get_token_admin):
        res = app.test_client().put(f'/room/1', json=get_room[4], headers={"Authorization": f"Bearer {get_token_admin}"})
        assert res.status_code == 400
        assert res.json == {"message": "numOfSeats < 0"}
    
    def test_put_user_validation_error(self, get_user, get_token_admin):
        res = app.test_client().put(f'/user/1', json=get_user[4], headers={"Authorization": f"Bearer {get_token_admin}"})
        assert res.status_code == 400
        assert res.json == {'userNam': ['Unknown field.']}
    ###########################GET#############################
    def test_validation_error_get_findByStatus(self, get_token_admin):
        response = client.get('/film/findByStatus/incom', headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert response.status_code == 400
        assert response.json == ["Must be one of: incoming, in rent, out of date."]
    
    ########################POST#############################
    def test_post_room_validation_error(self, get_room, get_token_admin):
        res = client.post('/room', json=get_room[3], headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert res.status_code == 400
        assert res.json == {"nam": ["Unknown field."],"name": ["Missing data for required field."]}

    def test_post_tag_error(self, get_tag, get_token_admin):
        res = client.post('/tag', json=get_tag[3], headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert res.status_code == 400
        assert res.json == {"nam": ["Unknown field."],"name": ["Missing data for required field."]}

    def test_post_film_error(self, get_film, get_token_admin):
        res = client.post('/film', json=get_film[2], headers={'Authorization': 'Bearer ' + str(get_token_admin)})
        assert res.status_code == 400
        assert res.json == {"nam": ["Unknown field."],"name": ["Missing data for required field."]}
        

    def test_post_room_error(self, get_room, get_token_admin):
        res = app.test_client().post(f'/room', json=get_room[4], headers={"Authorization": f"Bearer {get_token_admin}"})
        assert res.status_code == 400
        assert res.json == {"message": "numOfSeats < 0"}
    
    def test_post_sell_validation_error(self, get_user, get_token_admin):
        res = app.test_client().put(f'/user/1', json=get_user[4], headers={"Authorization": f"Bearer {get_token_admin}"})
        assert res.status_code == 400
        assert res.json == {'userNam': ['Unknown field.']}

    def test_sell_error_create(self, get_ticket, get_token_admin):
        response = client.post('/user/sell', json=get_ticket[1], headers={'Authorization': 'Bearer ' + str(get_token_admin)})

        assert response.status_code == 400
        assert response.json == {"dat": ["Unknown field."],"date": ["Missing data for required field."]}

    

   
    
    

    

    # def test_sell_create(self):
    #     seller = session.query(Users).filter(Users.userName == user_admin["userName"]).first()
    #     resp = client.post('/user/login', json={"username": seller.userName, "password": "11111111"})
    #     token = resp.json['token']
    #     response = client.post('/user/sell', json=sell_ticket, headers={'Authorization': 'Bearer ' + str(token)})
    #     assert response.status_code == 200
    #     assert response.json == {"message": "ticket create"}

    

    
    



# def test_create_user():
#     responce = client.post('/user', json=user_customer)
#     assert responce.status_code == 200

# def test_validation_erorr():
#     responce = client.post('/user', json=user_customer_er)
#     assert responce.status_code == 400

