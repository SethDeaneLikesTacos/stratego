
class Piece(object):
    def __init__(self, rep=None, player=None):
        self.rep = rep
        self.player = player

    def updaterep(self, rep):
        self.rep = rep

    def updateplayer(self, player):
        self.player = player
