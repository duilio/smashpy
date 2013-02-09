import numpy as np

from smash.base import BaseBoard, SquareHelper, START_POSITION, rank, col, pair2square
from movegen import gen_knight_moves, gen_bishop_moves, gen_rook_moves


# workarounds for pyflakes
SquareHelper
START_POSITION


class Board(BaseBoard):
    def set_check_status(self):
        king = {'w': 'K', 'b': 'k'}[self.stm]
        sq = np.where(self.raw == king)[0][0]

        other_knight = {'w': 'n', 'b': 'N'}[self.stm]
        for m in gen_knight_moves(self, sq):
            if m.capture == other_knight:
                return True

        other = {'w': 'bq', 'b': 'BQ'}[self.stm]
        for m in gen_bishop_moves(self, sq):
            if m.capture and m.capture in other:
                return True

        other = {'w': 'rq', 'b': 'RQ'}[self.stm]
        for m in gen_rook_moves(self, sq):
            if m.capture and m.capture in other:
                return True

        r = rank(sq)
        c = col(sq)

        if self.stm == 'w':
            r += 1
        else:
            r -= 1

        other = {'w': 'p', 'b': 'P'}[self.stm]
        if 0 <= r <= 7:
            if c > 0 and self.raw[pair2square(r, c - 1)] == other:
                return True
            if c < 7 and self.raw[pair2square(r, c + 1)] == other:
                return True

        return False
