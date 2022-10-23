from models import *

session = Session()

user_1 = Users(userName='m2', firstName='Ivan', lastName='Dvylyuk', email='123@gmail.com', password='12345', phone='3809709993', userStatus=1)
user_2 = Users(userName='softserve', firstName='Bohdan', lastName='Tsisinskyi', email='456@gmail.com', password='55555', phone='3809319194', userStatus=1)
room_1 = Rooms(name='Room1', numOfSeats=100)
room_2 = Rooms(name='Room2', numOfSeats=150)
tag_1 = Tags(name='Crime')
tag_2 = Tags(name='Humor')
tag_3 = Tags(name='Drama')
film_1 = Films(name='The Godfather', duration=175, status='incoming', tags=[tag_1, tag_2])
film_2 = Films(name='he Wolf of Wall Street', duration=180, status='incoming', tags=[tag_2, tag_3])
session_2 = Sessions(startTime='2022-11-11 13:00:00', filmId=1, roomId=1, pricePerTicket=50)
session_1 = Sessions(startTime='2022-10-24 16:00:00', filmId=2, roomId=2, pricePerTicket=75)
schedule_1 = Schedules(date='2022-11-11', sessionsWatch=[session_2])
schedule_2 = Schedules(date='2022-10-24', sessionsWatch=[session_1])
ticket_1 = Tickets(userId=1, sessionId=2, seatNum=10, date='2022-11-11 13:00:00')
ticket_2 = Tickets(userId=2, sessionId=1, seatNum=12, date='2022-10-24 16:00:00')
#
session.add_all([user_1, user_2, room_1, room_2, tag_1, tag_2, tag_3, film_1, film_2,
                 session_1, session_2, ticket_1, ticket_2, schedule_1, schedule_2])

session.commit()