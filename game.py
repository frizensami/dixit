class Player:
    playerid = 0

    def __init__(self, playerid=0):
        self.playerid = playerid


class STATE:
    WAIT_TOPIC = 0
    ALL_PICK = 1
    ALL_CHOOSE_TARGET = 2


class Game:

    state = STATE.WAIT_TOPIC
    players = []

    def __init__(self, num_players):
        for i in xrange(num_players):
            self.players.append(Player(i))

        self.state = STATE.WAIT_TOPIC

