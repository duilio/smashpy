from itertools import izip_longest

from smash.move import Move
from smash.movegen import gen_moves
from smash.base import squares
from smash.perft import perft


class ShellHelper(object):
    def __init__(self, board, engine):
        self.board = board
        self.engine = engine
        self._objects = {
            'b': board,
            'engine': engine,
            'fen': board.fen,
            'auto': self.auto,
            'move': self.move,
            'undo': self.undo,
            'show': self.show,
            'perft': self.perft,
            'movelist': self.movelist,
            }
        self._objects.update(squares)

    @property
    def objects(self):
        return self._objects.copy()

    def auto(self):
        move, score = self.engine.bestmove(self.board)
        print 'Best move: %s (%s)' % (move.str_simple(), score)

    def move(self, *args, **kwargs):
        if len(args) + len(kwargs) == 1:
            self.board.move(*args, **kwargs)
        else:
            m = Move(*args, **kwargs)
            self.board.move(m)
        self.show()

    def undo(self):
        self.board.undo()
        self.show()

    def show(self):
        print self.board
        print self.board.fen()

    def perft(self, depth):
        print perft(self.board, depth, 0)

    def movelist(self):
        r = []
        for m in gen_moves(self.board):
            self.board.move(m)
            if self.board.is_legal():
                r.append(m.str_simple())
            self.board.undo()
        r = iter(r)
        for row in izip_longest(*[r]*4, fillvalue=''):
            print ' '.join(row)
