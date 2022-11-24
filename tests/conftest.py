import pytest
from models import *
from b_test import client

@pytest.fixture
def get_user():
    user_admin_1 = {
        "userName":"admin",
        "firstName":"adm",
        "lastName":"in",
        "email":"admin@gmail.com",
        "password":"11111111",
        "phone":"380671234567",
        "userStatus":2
    }
    user_customer = {
        "userName":"ubah",
        "firstName":"dsfsdf",
        "lastName":"asdsadsad",
        "email":"sfdsdfs@gmail.com",
        "password":"11111111",
        "phone":"380671234567",
        "userStatus":0
    }
    userInfoP = {
        "userNam":"Ivan",
        "firstName":"dsfsdf",
        "lastName":"asdsadsad",
        "email":"ubah@gmail.com",
        "password":"11111111",
        "phone":"380671234567",
        "userStatus":0
    }
    user_update = {
        "userName":"ubah",
        "firstName":"dsfsdf",
        "lastName":"asdsadsad",
        "email":"sdsds@gmail.com",
        "password":"11111111",
        "phone":"380671234567"
    }
    user_update_er = {
        "userNam":"ubah",
        "firstName":"dsfsdf",
        "lastName":"asdsadsad",
        "email":"sdsds@gmail.com",
        "password":"11111111",
        "phone":"380671234567"
    }
    user_list = [user_admin_1, user_customer, userInfoP, user_update, user_update_er]
    return user_list  

# @pytest.fixture():
# def check_admin:
@pytest.fixture
def get_schedule():
    schedule = {
        "date": "2022-11-11",
        "sessions": [1]
    }
    schedule_update = {
        "sessions": [1]
    }
    schedule_er = {
        "dat": "2022-11-11",
        "sessions": [1]
    }
    schedule_error = {
        "sessions": [3]
    }
    schedule_date = {
        "sessions": [1]
    }
    list = [schedule, schedule_update, schedule_er,schedule_date, schedule_error]
    return list

@pytest.fixture
def get_ticket():
    sell_ticket = {
        "date": "2022-11-13",
        "userId": 2,
        "seatNum": 19,
        "sessionId":1
    }
    sell_ticket_er = {
        "dat": "2022-11-13",
        "userId": 2,
        "seatNum": 19,
        "sessionId":1
    }
    list = [sell_ticket, sell_ticket_er]
    return list

@pytest.fixture
def get_sess():
    session_1 = {
        "startTime": "18:30:00",
        "filmId": 1,
        "roomId": 2,
        "pricePerTicket":100
    }
    session_2 = {
        "startTime": "18:30:00",
        "filmId": 1,
        "roomId": 2,
        "pricePerTicket":-5
    }
    session_3 = {
        "startTim": "18:30:00",
        "filmId": 1,
        "roomId": 2,
        "pricePerTicket":100
    }
    session_4 = {
        "startTime": "18:30:00",
        "filmId": 10,
        "roomId": 2,
        "pricePerTicket":100
    }
    session_5 = {
        "startTime": "18:30:00",
        "filmId": 1,
        "roomId": 20,
        "pricePerTicket":100
    }
    session_6 = {
        "startTime": "18:30:00",
        "filmId": 1,
        "roomId": 2,
        "pricePerTicket":100
    }
    session_7 = {
        "startTime": "19:30:00",
        "filmId": 1,
        "roomId": 1,
        "pricePerTicket":100
    }
    list = [session_1, session_2, session_3, session_4, session_5, session_6, session_7]
    return list

@pytest.fixture
def get_room():
    room1 = {
    "name": "Room5",
    "numOfSeats": 200
    }
    room2 = {
    "name": "Room2",
    "numOfSeats": 100
    }
    room_update = {
    "name": "roooom",
    "numOfSeats": 50
    }
    room_er = {
    "nam": "roooom",
    "numOfSeats": 50
    }
    room_seat = {
    "name": "rooom",
    "numOfSeats": -3 
    }
    room = [room1,room2, room_update, room_er, room_seat]
    return room

@pytest.fixture
def get_tag():
    tag1 = {
    "name":"action"
    }
    tag_2 = {
    "name":"active"
    }
    tag_update = {
    "name":"horror"
    }
    tag_er = {
    "nam":"action"
    }
    tags = [tag1,tag_2, tag_update, tag_er]
    return tags

@pytest.fixture
def get_film():
    film_one = {
        "name": "Home Alone",
        "duration": 110,
        "status": "in rent",
        "tags": [1]
    }
    film_sec = {
        "name": "Scream",
        "duration": 110,
        "status": "incoming",
        "tags": [1,2]
    }
    film_val = {
        "nam": "Home Alone",
        "duration": 110,
        "status": "in rent",
        "tags": [1,2]
    }
    film_update = {
        "name": "LOLO",
        "duration": 110,
        "status": "incoming"
    }
    film_list = [film_one, film_sec, film_val,film_update]
    return film_list


@pytest.fixture(scope='function')
def wrapper():
    Session().close()
    BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)

@pytest.fixture
def get_token_admin(get_user):
    get_user = session.query(Users).filter(Users.userName == get_user[0]["userName"]).first()
    resp = client.post('/user/login', json={"username": get_user.userName, "password": "11111111"})
    return resp.json['token']


@pytest.fixture
def get_token_customer(get_user):
    user_to_get = session.query(Users).filter(Users.userName == get_user[1]["userName"]).first()
    resp = client.post('/user/login', json={"username": user_to_get.userName, "password": "11111111"})
    return resp.json['token']