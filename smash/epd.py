import logging

from smash.board import Board
from smash.move import Move


log = logging.getLogger(__name__)


class EPDSuite(object):
    def __init__(self, fin):
        self._suite = suite = []

        for i, line in enumerate(fin, 1):
            try:
                fen, moves = self.parse_line(line)
            except ValueError:
                log.error('Cannot parse line %d', i)
                continue
            suite.append((fen, moves))

    def parse_line(self, line):
        line = [x.strip() for x in line.split(';')]
        line = line[0].split()
        bmidx = line.index('bm')
        fen = line[:bmidx]
        fen.extend(['0', '1'])
        fen = ' '.join(fen)

        board = Board(fen)
        moves = []
        for san in line[bmidx+1:]:
            san = san.rstrip(',')
            moves.append(Move.from_san(board, san))
        return fen, moves

    def test_engine(self, engine):
        success = 0
        fail = 0

        for i, (fen, moves) in enumerate(self._suite, 1):
            print 'Test n.%d:' % i,
            board = Board(fen)
            result, score = engine.bestmove(board)
            if result not in moves:
                fail += 1
                moves = ' or '.join(m.str_simple() for m in moves)
                print 'FAIL with score %s (%s instead of %s)' % (score,
                                                                 result.str_simple(),
                                                                 moves)
            else:
                success += 1
                print 'OK with score: %s' % score

        print 'Results: %s/%s' % (success, success + fail)
