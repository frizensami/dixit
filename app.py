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
current_game = None


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

def topic_callback(topic):
    socketio.emit('topic', {'topic': topic}, broadcast=True)
    print "Emitted topic: " + str(topic)


def pick_target_callback(other_cards_for_players):
    socketio.emit('pick_target', other_cards_for_players, broadcast=True)
    print "Emitted pick_target: " + str(other_cards_for_players)


def after_guess_callback(target_card):
    socketio.emit('after_guess', target_card, broadcast=True)
    print "Emitted after_guess: " + str(target_card)


@socketio.on('start_command')
def start(data):
    global current_game
    current_game = Game(num_players=3, send_topic_callback=topic_callback,
                        send_pick_target_callback=pick_target_callback,
                        send_after_guess_callback=after_guess_callback)
    if current_game.begin():

        to_send = {'starting_player': current_game.current_target_player}
        for index, player in enumerate(current_game.players):
            print "Index: " + str(index)
            to_send[index] = player.deck[0:6]

        emit('start', to_send, broadcast=True)
        print "Game started!"
        print "Game start status %s" % current_game.started


@socketio.on('next_round')
def on_nr(data):
    print "Trying to start next round!"
    if current_game.start_next_round():
        to_send = {'starting_player': current_game.current_target_player}
        for index, player in enumerate(current_game.players):
            print "Index: " + str(index)
            to_send[index] = player.deck[0:6]

        emit('start', to_send, broadcast=True)
        print "next round started!"


@socketio.on('deck_card_clicked')
def deck_clicked(data):
    player_id = data["playerid"]
    card_id = data["cardid"]
    print "card id: %s clicked by %s" % (str(card_id), str(player_id))
    current_game.notify_deck_card_clicked(player_id, card_id)


@socketio.on('other_card_clicked')
def other_clicked(data):
    player_id = data["playerid"]
    card_id = data["cardid"]
    print "card id: %s clicked by %s" % (str(card_id), str(player_id))
    current_game.notify_other_card_clicked(player_id, card_id)


@socketio.on('new_topic')
def newtopic(data):
    player_id = data["playerid"]
    topic_text = data["topictext"]
    print "Topic: %s submitted by %s" % (str(topic_text), str(player_id))
    current_game.notify_new_topic(player_id, topic_text)



@socketio.on('join')
def on_join(data):
    print "Player joined: " + str(data['playerid'])

    # We need to send the player his stuff if the game has started
    global current_game
    if current_game is not None:
        # Step 1: Send them their cards
        player_id = data["playerid"]
        cards = current_game.players[player_id].deck[0:6]
        out_dict = {'starting_player': current_game.current_target_player, player_id: cards}
        emit('start', out_dict)
        print "Emitted starting info on rejoining player: %s" % str(out_dict)



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
    socketio.run(app, host="0.0.0.0")

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
