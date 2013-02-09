"""Move generator"""

from smash.move import Move
from smash.board import \
    pair2square, rank, col, get_side
from smash.movetables import knight_table


movefunc = {}


def gen_moves(board):
    """Generate all moves for a board

    NOTE: this includes also invalid moves

    """
    stm = board.stm
    b = board.raw
    for sq in xrange(64):
        p = b[sq]
        if get_side(p) == stm:
            for m in movefunc[p.lower()](board, sq):
                yield m


def gen_empty_moves(*args):
    if False:
        yield


def gen_pawn_moves(board, src):
    r = rank(src)
    c = col(src)
    b = board.raw
    stm = board.stm

    assert 0 < r < 7
    assert 0 <= c <= 7
    
    promotes = [None]
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

    nextsq = pair2square(r + dir, c)

    if b[nextsq] == ' ':
        for p in promotes:
            yield Move(src, nextsq, promote=p)

        if first_rank == r:
            doublesq = pair2square(r + dir*2, c)
            if b[doublesq] == ' ':
                yield Move(src, doublesq, en_passant=nextsq)

    # gen captures
    nextsqs = []
    if c != 0:
        nextsqs.append(pair2square(r + dir, c - 1))
    if c != 7:
        nextsqs.append(pair2square(r + dir, c + 1))

    for nextsq in nextsqs:
        if b[nextsq] != ' ' and get_side(b[nextsq]) != stm:
            for p in promotes:
                yield Move(src, nextsq, capture=b[nextsq], promote=p)
        elif nextsq == board.en_passant:
            yield Move(src, nextsq, capture=b[src].swapcase())


def gen_knight_moves(board, src):
    b = board.raw
    stm = board.stm

    for dst in knight_table[src]:
        if b[dst] != ' ':
            if get_side(b[dst]) != stm:
                yield Move(src, dst, capture=b[dst])
        else:
            yield Move(src, dst)


movefunc[' '] = gen_empty_moves
movefunc['p'] = gen_pawn_moves
movefunc['n'] = gen_knight_moves
movefunc['b'] = gen_empty_moves
movefunc['r'] = gen_empty_moves
movefunc['q'] = gen_empty_moves
movefunc['k'] = gen_empty_moves
