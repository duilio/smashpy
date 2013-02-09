"""Move generator"""

from smash.move import Move
from smash.board import \
    pair2square, rank, col, get_side


movefunc = {}


def gen_moves(board):
    """Generate all moves for a board

    NOTE: this includes also invalid moves

    """
    stm = board.stm
    b = board.raw
    for sq in xrange(64):
        r, c = rank(sq), col(sq)
        e = b[sq]
        if get_side(e) == stm:
            for m in _gen_moves(b, stm, e, r, c):
                yield m


def _gen_moves(b, stm, p, r, c):
    return movefunc[p.lower()](b, stm, r, c)


def gen_empty_moves(*args):
    if False:
        yield


def gen_pawn_moves(b, stm, r, c):
    assert 0 < r < 7
    assert 0 <= c <= 7
    
    promotes = []
    if stm == 'w':
        dir = 1
        if r == 6:
            promotes = 'NBRQ'
        first_rank = 1
    else:
        dir = -1
        if r == 1:
            promotes = 'nbrq'
        first_rank = 6

    currsq = pair2square(r, c)
    nextsq = pair2square(r + dir, c)

    if b[nextsq] == ' ':
        for p in promotes:
            yield Move(currsq, nextsq, promote=p)
        else:
            yield Move(currsq, nextsq)

        if first_rank == r:
            doublesq = pair2square(r + dir*2, c)
            if b[doublesq] == ' ':
                yield Move(currsq, doublesq, en_passant=nextsq)

    # gen captures
    leftsq = pair2square(r + dir, c - 1)
    rightsq = pair2square(r + dir, c + 1)

    for nextsq in (leftsq, rightsq):
        if c != 0 and b[nextsq] != ' ' and get_side(b[nextsq]) != stm:
            for p in promotes:
                yield Move(currsq, nextsq, capture=b[nextsq], promote=p)
            else:
                yield Move(currsq, nextsq, capture=b[nextsq])


movefunc['p'] = gen_pawn_moves
movefunc['n'] = gen_empty_moves
movefunc['b'] = gen_empty_moves
movefunc['r'] = gen_empty_moves
movefunc['q'] = gen_empty_moves
movefunc['k'] = gen_empty_moves
