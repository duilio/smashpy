import unittest
from smash.board import Board, SquareHelper
from smash.move import Move
from smash.movegen import gen_moves, gen_pawn_moves, gen_knight_moves


class PawnMoveTest(unittest.TestCase):
    def test_initial_row(self):
        b = Board()
        sq = SquareHelper()
        self.assertItemsEqual(gen_pawn_moves(b, sq.a2),
                              [Move(sq.a2, sq.a3),
                               Move(sq.a2, sq.a4, en_passant=sq.a3)])

        b = Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1')
        self.assertItemsEqual(gen_pawn_moves(b, sq.a7),
                              [Move(sq.a7, sq.a6),
                               Move(sq.a7, sq.a5, en_passant=sq.a6)])

    def test_captures(self):
        b = Board('k7/p1p/1P6/8/8/8/8/K7 w - - 0 1')
        sq = SquareHelper()
        self.assertItemsEqual(gen_pawn_moves(b, sq.b6),
                              [Move(sq.b6, sq.a7, capture='p'),
                               Move(sq.b6, sq.c7, capture='p'),
                               Move(sq.b6, sq.b7)])

    def test_promotes(self):
        b = Board('k7/7P/8/8/8/8/8/K7 w - - 0 1')
        sq = SquareHelper()
        self.assertItemsEqual(gen_pawn_moves(b, sq.h7),
                              [Move(sq.h7, sq.h8, promote='Q'),
                               Move(sq.h7, sq.h8, promote='N'),
                               Move(sq.h7, sq.h8, promote='R'),
                               Move(sq.h7, sq.h8, promote='B')])

    def test_captures_and_promotes(self):
        b = Board('k5n1/7P/8/8/8/8/8/K7 w - - 0 1')
        sq = SquareHelper()
        self.assertItemsEqual(gen_pawn_moves(b, sq.h7),
                              [Move(sq.h7, sq.h8, promote='Q'),
                               Move(sq.h7, sq.h8, promote='N'),
                               Move(sq.h7, sq.h8, promote='R'),
                               Move(sq.h7, sq.h8, promote='B'),
                               Move(sq.h7, sq.g8, capture='n', promote='Q'),
                               Move(sq.h7, sq.g8, capture='n', promote='N'),
                               Move(sq.h7, sq.g8, capture='n', promote='R'),
                               Move(sq.h7, sq.g8, capture='n', promote='B')])

    def test_en_passant(self):
        b = Board('k7/8/8/pP6/8/8/8/K7 w - a6 0 1')
        sq = SquareHelper()
        self.assertItemsEqual(gen_pawn_moves(b, sq.b5),
                              [Move(sq.b5, sq.a6, capture='p'),
                               Move(sq.b5, sq.b6)])


class KnightMoveTest(unittest.TestCase):
    def test_lower_edge(self):
        b = Board()
        sq = SquareHelper()
        self.assertItemsEqual(gen_knight_moves(b, sq.b1),
                              [Move(sq.b1, sq.a3),
                               Move(sq.b1, sq.c3)])

    def test_higher_edge(self):
        b = Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1')
        sq = SquareHelper()
        self.assertItemsEqual(gen_knight_moves(b, sq.b8),
                              [Move(sq.b8, sq.a6),
                               Move(sq.b8, sq.c6)])

    def test_all_moves(self):
        b = Board('k7/8/8/8/4N3/8/8/K7 w - - 0 1')
        sq = SquareHelper()
        self.assertItemsEqual(gen_knight_moves(b, sq.e4),
                              [Move(sq.e4, sq.d6),
                               Move(sq.e4, sq.f6),
                               Move(sq.e4, sq.g5),
                               Move(sq.e4, sq.g3),
                               Move(sq.e4, sq.f2),
                               Move(sq.e4, sq.d2),
                               Move(sq.e4, sq.c3),
                               Move(sq.e4, sq.c5)])

    def test_captures(self):
        b = Board('k7/8/1p6/2p5/N7/2p5/1p6/K7 w - - 0 1')
        sq = SquareHelper()
        self.assertItemsEqual(gen_knight_moves(b, sq.a4),
                              [Move(sq.a4, sq.b6, capture='p'),
                               Move(sq.a4, sq.c5, capture='p'),
                               Move(sq.a4, sq.c3, capture='p'),
                               Move(sq.a4, sq.b2, capture='p')])


class MoveGenTest(unittest.TestCase):
    def test_start_position(self):
        b = Board()
        sq = SquareHelper()
        
        self.assertItemsEqual(gen_moves(b),
                              [Move(sq.a2, sq.a3),
                               Move(sq.a2, sq.a4, en_passant=sq.a3),
                               Move(sq.b2, sq.b3),
                               Move(sq.b2, sq.b4, en_passant=sq.b3),
                               Move(sq.c2, sq.c3),
                               Move(sq.c2, sq.c4, en_passant=sq.c3),
                               Move(sq.d2, sq.d3),
                               Move(sq.d2, sq.d4, en_passant=sq.d3),
                               Move(sq.e2, sq.e3),
                               Move(sq.e2, sq.e4, en_passant=sq.e3),
                               Move(sq.f2, sq.f3),
                               Move(sq.f2, sq.f4, en_passant=sq.f3),
                               Move(sq.g2, sq.g3),
                               Move(sq.g2, sq.g4, en_passant=sq.g3),
                               Move(sq.h2, sq.h3),
                               Move(sq.h2, sq.h4, en_passant=sq.h3),
                               Move(sq.b1, sq.a3),
                               Move(sq.b1, sq.c3),
                               Move(sq.g1, sq.h3),
                               Move(sq.g1, sq.f3),
                               ])
