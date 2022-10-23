CREATE TABLE users(
   id SERIAL NOT NULL PRIMARY KEY,
   username VARCHAR (50) NOT NULL,
   firstName VARCHAR (50) NOT NULL,
   lastName VARCHAR (20) NOT NULL,
   email VARCHAR(100) NOT NULL,
   password VARCHAR (255) NOT NULL,
   phone VARCHAR(100) NOT NULL,
   userStatus INT NOT NULL
);

CREATE TABLE rooms(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    numOfSeats INT NOT NULL
);


CREATE TABLE schedules(
    id        SERIAL PRIMARY KEY,
    date    date       NOT NULL
);

CREATE TABLE films (
    id SERIAL NOT NULL PRIMARY KEY,
    name    VARCHAR(100)       NOT NULL,
    duration INT not null,
    status varchar(100) not null,
    constraint check_status CHECK(status IN ('incoming','in rent', 'out of date'))
);

CREATE TABLE tags(
    id serial PRIMARY KEY,
    name varchar(100) NOT NULL
);

CREATE TABLE film_tag(
    filmId int NOT NUll,
    tagId  int NOT NULL,
    CONSTRAINT fk_filmId FOREIGN KEY (filmId) REFERENCES films (id),
    CONSTRAINT fk_tagId FOREIGN KEY (tagId) REFERENCES tags (id)
);

CREATE TABLE sessions(
    id        SERIAL PRIMARY KEY,
    startTime    TIMESTAMP       NOT NULL,
    filmId INT       NOT NULL,
    roomId   INT       NOT NULL,
    pricePerTicket      DECIMAL(5,2) not null,
    CONSTRAINT fk_filmId FOREIGN KEY (filmId) REFERENCES films (id),
    CONSTRAINT fk_roomId FOREIGN KEY (roomId) REFERENCES rooms (id)
);

CREATE TABLE tickets(
    id        SERIAL NOT NULL PRIMARY KEY,
    userId    INT       NOT NULL,
    sessionId INT       NOT NULL,
    seatNum   INT       NOT NULL,
    date      TIMESTAMP not null,
    CONSTRAINT fk_userId FOREIGN KEY (userId) REFERENCES users (id),
    CONSTRAINT fk_sessionId FOREIGN KEY (sessionId) REFERENCES sessions (id)
);

CREATE TABLE schedule_session(
    scheduleId int NOT NULL,
    sessionId  int NOT NULL,
    CONSTRAINT fk_scheduleId FOREIGN KEY (scheduleId) REFERENCES schedules (id),
    CONSTRAINT fk_sessionId FOREIGN KEY (sessionId) REFERENCES sessions (id)
);



