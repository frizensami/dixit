import time


class GameLogger:

    def __init__(self):
        print "Initializing logfile"
        self.logfile = open('log-' + str(int(time.time())) + '.log', 'w')

    def __enter__(self):
        return self

    def __exit__(self):
        self.logfile.close()

