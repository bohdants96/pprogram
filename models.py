import os
from sqlalchemy import *
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

#DB_URI = os.getenv("DB_URI")
engine = create_engine("postgresql://postgres:postgres22@localhost:5432/cinema")

Session = sessionmaker(bind=engine)
BaseModel = declarative_base()

FilmTag = Table('FilmsTags',
    BaseModel.metadata,
    Column('filmId', Integer, ForeignKey('films.id')),
    Column('tagId', Integer, ForeignKey('tags.id'))
)

schedule_session = Table('ScheduleSession',
    BaseModel.metadata,
    Column('scheduleId', Integer, ForeignKey('schedules.id'), primary_key=True),
    Column('sessionId', Integer, ForeignKey('sessions.id'), primary_key=True)
)

class Users(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True)
    userName = Column(String)
    firstName = Column(String)
    lastName = Column(String)
    email = Column(String)
    password = Column(String)
    phone = Column(String)
    userStatus = Column(Integer)

class Rooms(BaseModel):
    __tablename__ = "rooms"

    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True)
    name = Column(String)
    numOfSeats = Column(Integer)


class Tags(BaseModel):
    __tablename__ = "tags"

    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True)
    name = Column(String)

class Films(BaseModel):
    __tablename__ = "films"

    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True)
    name = Column(String)
    duration = Column(Integer)
    status = Column(String)
    CheckConstraint(status.in_(['incoming', 'in rent', 'out of date']))
    tags = relationship(Tags, secondary=FilmTag, backref='movies')

class Sessions(BaseModel):
    __tablename__ = "sessions"

    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True)
    startTime = Column(DateTime, server_default=func.now())
    filmId = Column(Integer, ForeignKey('films.id'))
    roomId = Column(Integer, ForeignKey('rooms.id'))
    pricePerTicket = Column(Float)
    filmToWatch = relationship(Films, foreign_keys=[filmId], backref="id_film", lazy="joined")
    FilmRoom = relationship(Rooms, foreign_keys=[roomId], backref="id_room", lazy="joined")

class Schedules(BaseModel):
    __tablename__ = "schedules"

    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True)
    date = Column(Date)
    sessionsWatch = relationship(Sessions, secondary=schedule_session, backref="schedule")

class Tickets(BaseModel):
    __tablename__ = "tickets"

    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True)
    userId = Column(Integer, ForeignKey('users.id'))
    sessionId = Column(Integer, ForeignKey('sessions.id'))
    seatNum = Column(Integer)
    date = Column(DateTime, server_default=func.now())
    UserToWatch = relationship(Users, foreign_keys=[userId], backref="userWatch", lazy="joined")
    SessionTicket = relationship(Sessions, foreign_keys=[sessionId], backref="sessionT", lazy="joined")
BaseModel.metadata.create_all(engine)