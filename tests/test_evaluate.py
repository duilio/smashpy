import unittest
from smash.board import Board
from smash.evaluate import evaluate_material


class EvaluateMaterialTest(unittest.TestCase):
    fixtures = [
        ('rnbqkbnr/pppp1ppp/8/8/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1', (370, 370)),
        ('r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1', (100, 100)),
        ]

    def test_start(self):
        b = Board()
        self.assertEquals(evaluate_material(b.raw), (380, 380))

    def test_fixtures(self):
        for fen, expected in self.fixtures:
            b = Board(fen=fen)
            self.assertEquals(evaluate_material(b.raw), expected)
