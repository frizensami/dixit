#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, send_file
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
from flask_socketio import SocketIO, send, join_room, leave_room, emit
from game import Game

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
socketio = SocketIO(app)
current_game = Game(num_players=3)


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#




@socketio.on('start_command')
def start(data):
    current_game = Game(num_players=3)
    if current_game.begin():
        emit('start', {'starting_player': current_game.current_target_player}, broadcast=True)
        print "Game started!"

@socketio.on('card_clicked')
def start(data):
    player_id = data["playerid"]
    card_id = data["cardid"]
    print "card id: %s clicked by %s" % (str(card_id), str(player_id))


@socketio.on('join')
def on_join(data):
    print "Player joined: " + str(data['playerid'])


@socketio.on('disconnect')
def on_leave():
    print "Client left!"



# === APP ROUTES ===

@app.route('/<int:playerid>')
def player(playerid):
    return render_template('pages/player.html', playerid=str(playerid))


@app.route('/<int:playerid>/play/<int:cardnum>')
def play(playerid, cardnum):
    return cardnum


@app.route('/<int:playerid>/choose/<int:cardnum>')
def choose(playerid, cardnum):
    return cardnum


@app.route('/')
def home():
    return render_template('pages/home.html')


@app.route('/img/<int:img_num>')
def get_image(img_num):
    filename = "static/img/" + str(img_num) + ".jpg"
    return send_file(filename, mimetype='image/jpg')

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    socketio.run(app)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
