import unittest
from smash.board import Board, SquareHelper, START_POSITION
from smash.move import Move


class FenTest(unittest.TestCase):
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

    def test_move_pawn(self):
        b = Board()
        sq = SquareHelper()
        b.move(Move(sq.e2, sq.e3))
        self.assertEquals(b.fen(), 'rnbqkbnr/pppppppp/8/8/8/4P3/PPPP1PPP/RNBQKBNR b KQkq - 0 2')

    def test_move_double_push_pawn(self):
        b = Board()
        sq = SquareHelper()
        b.move(Move(sq.e2, sq.e4, en_passant=sq.e3))
        self.assertEquals(b.fen(), 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 2')

    def test_move_pawn_capture(self):
        b = Board('rnbqkbnr/pppppppp/4P3/8/8/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1')
        sq = SquareHelper()
        b.move(Move(sq.e6, sq.f7, capture='p'))
        self.assertEquals(b.fen(), 'rnbqkbnr/pppppPpp/8/8/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 2')

    def test_move_pawn_promote(self):
        b = Board('k7/7P/8/8/8/8/8/K7 w - - 0 1')
        sq = SquareHelper()
        b.move(Move(sq.h7, sq.h8, promote='Q'))
        self.assertEquals(b.fen(), 'k6Q/8/8/8/8/8/8/K7 b - - 0 2')

    def test_move_pawn_promote_and_capture(self):
        b = Board('k5n1/7P/8/8/8/8/8/K7 w - - 0 1')
        sq = SquareHelper()
        b.move(Move(sq.h7, sq.g8, capture='n', promote='Q'))
        self.assertEquals(b.fen(), 'k5Q1/8/8/8/8/8/8/K7 b - - 0 2')

    def test_move_pawn_en_passant(self):
        b = Board('k7/8/8/pP6/8/8/8/K7 w - a6 0 1')
        sq = SquareHelper()
        b.move(Move(sq.b5, sq.a6, capture='p'))
        self.assertEqual(b.fen(), 'k7/8/P7/8/8/8/8/K7 b - - 0 2')
