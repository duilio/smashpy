import unittest
from smash.board import Board, START_POSITION


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
