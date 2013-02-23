from smash.base import \
    BaseBoard, SquareHelper, START_POSITION, rank, col, pair2square, swap_side
from movegen import \
    gen_knight_captures, gen_bishop_captures, gen_rook_captures, gen_king_captures, \
    gen_moves


# workarounds for pyflakes
SquareHelper
START_POSITION


class Board(BaseBoard):
    KNIGHTS = {'w': 'N', 'b': 'n'}
    BISHOPS = {'w': 'BQ', 'b': 'bq'}
    ROOKS = {'w': 'RQ', 'b': 'rq'}
    KINGS = {'w': 'K', 'b': 'k'}
    PAWNS = {'w': 'P', 'b': 'p'}

    def can_attack(self, stm, sq):
        """Returns true if the player attacks the square"""

        xside = swap_side(stm)
        p = Board.KNIGHTS[stm]
        for x in gen_knight_captures(self, sq, xside):
            if x == p:
                return True

        p = Board.BISHOPS[stm]
        for x in gen_bishop_captures(self, sq, xside):
            if x in p:
                return True

        p = Board.ROOKS[stm]
        for x in gen_rook_captures(self, sq, xside):
            if x in p:
                return True

        p = Board.KINGS[stm]
        for x in gen_king_captures(self, sq, xside):
            if x == p:
                return True

        r = rank(sq)
        c = col(sq)

        if stm == 'w':
            r -= 1
        else:
            r += 1

        p = Board.PAWNS[stm]
        if 0 <= r <= 7:
            if c > 0 and self.raw[pair2square(r, c - 1)] == p:
                return True
            if c < 7 and self.raw[pair2square(r, c + 1)] == p:
                return True

        return False

    def legal_moves(self):
        moves = []
        for m in gen_moves(self):
            with self.moving(m):
                if self.is_legal():
                    moves.append(m)
        return moves
