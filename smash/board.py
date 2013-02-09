from smash.base import \
    BaseBoard, SquareHelper, START_POSITION, rank, col, pair2square, swap_side
from movegen import \
    gen_knight_moves, gen_bishop_moves, gen_rook_moves, gen_king_moves


# workarounds for pyflakes
SquareHelper
START_POSITION


class Board(BaseBoard):
    def can_attack(self, stm, sq):
        """Returns true if the player attacks the square"""

        xside = swap_side(stm)
        p = {'w': 'N', 'b': 'n'}[stm]
        for m in gen_knight_moves(self, sq, xside):
            if m.capture == p:
                return True

        p = {'w': 'BQ', 'b': 'bq'}[stm]
        for m in gen_bishop_moves(self, sq, xside):
            if m.capture and m.capture in p:
                return True

        p = {'w': 'RQ', 'b': 'rq'}[stm]
        for m in gen_rook_moves(self, sq, xside):
            if m.capture and m.capture in p:
                return True

        p = {'w': 'K', 'b': 'k'}[stm]
        for m in gen_king_moves(self, sq, xside, do_castling=False):
            if m.capture and m.capture == p:
                return True

        r = rank(sq)
        c = col(sq)

        if stm == 'w':
            r -= 1
        else:
            r += 1

        other = {'w': 'P', 'b': 'p'}[stm]
        if 0 <= r <= 7:
            if c > 0 and self.raw[pair2square(r, c - 1)] == other:
                return True
            if c < 7 and self.raw[pair2square(r, c + 1)] == other:
                return True

        return False
