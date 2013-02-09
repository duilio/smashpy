import unittest
from smash.board import Board, squares
from smash.move import Move
from smash.movegen import gen_pawn_moves


class PawnTest(unittest.TestCase):
    def test_initial_row(self):
        b = Board()

        a2, a3, a4 = [squares[k] for k in ('a2', 'a3', 'a4')]
        self.assertItemsEqual(list(gen_pawn_moves(b.raw, 'w', 1, 0)),
                              [Move(a2, a3),
                               Move(a2, a4, en_passant=a3)])

        a7, a6, a5 = [squares[k] for k in ('a7', 'a6', 'a5')]
        self.assertItemsEqual(list(gen_pawn_moves(b.raw, 'b', 6, 0)),
                              [Move(a7, a6),
                               Move(a7, a5, en_passant=a6)])
