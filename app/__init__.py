from flask import Flask

app = Flask(__name__)

from pprogram.app.views import user
from pprogram.app.views import tag
from pprogram.app.views import film
from pprogram.app.views import room
from pprogram.app.views import session
from pprogram.app.views import schedule
from pprogram.app.views import ticket

app.register_blueprint(tag.tag_blueprint)
app.register_blueprint(user.user_blueprint)
app.register_blueprint(film.film_blueprint)
app.register_blueprint(room.room_blueprint)
app.register_blueprint(session.session_blueprint)
app.register_blueprint(schedule.schedule_blueprint)
app.register_blueprint(ticket.ticket_blueprint)
