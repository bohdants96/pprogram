from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)

from app.views import user
from app.views import tag
from app.views import film
from app.views import room
from app.views import session
from app.views import schedule
from app.views import ticket

app.register_blueprint(tag.tag_blueprint)
app.register_blueprint(user.user_blueprint)
app.register_blueprint(film.film_blueprint)
app.register_blueprint(room.room_blueprint)
app.register_blueprint(session.session_blueprint)
app.register_blueprint(schedule.schedule_blueprint)
app.register_blueprint(ticket.ticket_blueprint)

app.config["JWT_SECRET_KEY"] = "secret-key"
jwt = JWTManager(app)
