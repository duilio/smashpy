import unittest
from smash.board import Board, SquareHelper, START_POSITION
from smash.move import Move


class BoardFenTest(unittest.TestCase):
    def test_start_position(self):
        b = Board()
        t = 'RNBQKBNR' + 'P'*8 + ' '*8*4 + 'p'*8 + 'rnbqkbnr'
        self.assertEqual(''.join(b.raw), t)
        self.assertEqual(b.stm, 'w')
        self.assertIsNone(b.en_passant)
        self.assertItemsEqual(b.castling.items(),
                              zip('kKqQ', [1, 1, 1, 1]))

    def test_fen_start_position(self):
        b = Board()
        self.assertEqual(b.fen(), START_POSITION)

sq = SquareHelper()
move_fixtures = [
    # pawn move
    (START_POSITION, Move(sq.e2, sq.e3),
     'rnbqkbnr/pppppppp/8/8/8/4P3/PPPP1PPP/RNBQKBNR b KQkq - 0 2'),
    # pawn double push
    (START_POSITION, Move(sq.e2, sq.e4, en_passant=sq.e3),
     'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 2'),
    # pawn capture
    ('rnbqkbnr/pppppppp/4P3/8/8/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1',
     Move(sq.e6, sq.f7, capture='p'),
     'rnbqkbnr/pppppPpp/8/8/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 2'),
    # pawn promotion
    ('k7/7P/8/8/8/8/8/K7 w - - 0 1',
     Move(sq.h7, sq.h8, promote='Q'),
     'k6Q/8/8/8/8/8/8/K7 b - - 0 2'),
    # pawn promotion with capture
    ('k5n1/7P/8/8/8/8/8/K7 w - - 0 1',
     Move(sq.h7, sq.g8, capture='n', promote='Q'),
     'k5Q1/8/8/8/8/8/8/K7 b - - 0 2'),
    # en passant capture
    ('k7/8/8/pP6/8/8/8/K7 w - a6 0 1',
     Move(sq.b5, sq.a6, capture='p'),
     'k7/8/P7/8/8/8/8/K7 b - - 0 2'),
    ('4k3/8/8/8/8/8/8/R3K2R w KQ - 0 1',
     Move(sq.e1, sq.c1),
     '4k3/8/8/8/8/8/8/2KR3R b - - 0 2'),
    ('4k3/8/8/8/8/8/8/R3K2R w KQ - 0 1',
     Move(sq.e1, sq.g1),
     '4k3/8/8/8/8/8/8/R4RK1 b - - 0 2'),
    ]

check_fixtures = [
    ('k7/8/8/8/8/8/p7/K7 w - - 0 1', False),
    ('k7/8/8/8/8/8/1p6/K7 w - - 0 1', True),
    ('k7/8/8/8/8/8/1p6/1K6 w - - 0 1', False),
    ('k7/8/8/8/8/8/2p5/1K6 w - - 0 1', True),
    ('k7/8/8/8/8/8/2P5/1K6 w - - 0 1', False),
    ('k7/8/8/8/8/8/1b6/K7 w - - 0 1', True),
    ('k7/8/8/8/8/2b5/8/K7 w - - 0 1', True),
    ('k7/8/8/8/8/2Q5/8/K7 w - - 0 1', False),
    ('k7/8/8/8/8/2q5/8/K7 w - - 0 1', True),
    ('k7/8/8/8/8/2r5/8/K7 w - - 0 1', False),
    ('k7/8/8/8/8/r7/8/K7 w - - 0 1', True),
    ('k7/8/8/8/8/q7/8/K7 w - - 0 1', True),
    ('k7/8/8/8/8/R7/8/K7 w - - 0 1', False),
    ]


class BoardMoveTest(unittest.TestCase):
    def test_move(self):
        for i, (start_fen, move, end_fen) in enumerate(move_fixtures, 1):
            b = Board(start_fen)
            b.move(move)
            self.assertEquals(b.fen(), end_fen,
                              msg='Failed at n. %s:\n%r != %r' % (i, b.fen(), end_fen))

    def test_undo(self):
        for i, (start_fen, move, _) in enumerate(move_fixtures, 1):
            b = Board(start_fen)
            b.move(move)
            b.undo()
            self.assertEquals(b.fen(), start_fen,
                              msg='Failed at n. %s:\n%r != %r' % (i, b.fen(), start_fen))


class BoardCheckTest(unittest.TestCase):
    def test_check_status(self):
        for i, (fen, checked) in enumerate(check_fixtures, 1):
            b = Board(fen)
            self.assertEquals(b.checked, checked, msg='Failed at n. %s' % i)
