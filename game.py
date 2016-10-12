class Player:
    playerid = 0

    def __init__(self, playerid=0):
        self.playerid = playerid


class STATE:
    WAIT_TOPIC = 0
    ALL_PICK = 1
    ALL_CHOOSE_TARGET = 2


class Game:

    started = False
    state = STATE.WAIT_TOPIC
    players = []
    current_target_player = None
    topic = None

    def __init__(self, num_players=1, starting_player_num=0):
        for i in xrange(num_players):
            new_player = Player(i)
            self.players.append(new_player)

            # Sets the starting player
            self.current_target_player = starting_player_num

        self.state = STATE.WAIT_TOPIC

    def set_topic(self, topic):
        self.topic = topic

    def begin(self):
        if not self.started:
            self.started = True
            return True
        else:
            return False



