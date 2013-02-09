"""Move generator"""

from itertools import chain

import numpy as np

from smash.move import Move
from smash.base import pair2square, rank, col, get_side
from smash.movetables import knight_table, bishop_table, rook_table, king_table


movefunc = {}


def gen_moves(board):
    """Generate all moves for a board

    NOTE: this includes also invalid moves

    """
    stm = board.stm
    b = board.raw

    if stm == 'w':
        cond = np.char.isupper
    else:
        cond = np.char.islower

    for sq in np.where(cond(b))[0]:
        p = b[sq]
        for m in movefunc[p.lower()](board, sq):
            yield m


def gen_pawn_moves(board, src):
    """Generate pawn moves"""

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


def _gen_ray_moves(board, src, rays):
    """Generate table based ray moves (i.e. bishop/rook moves)"""

    b = board.raw
    stm = board.stm

    for ray in rays:
        for dst in ray:
            if b[dst] != ' ':
                if get_side(b[dst]) != stm:
                    yield Move(src, dst, capture=b[dst])
                break
            else:
                yield Move(src, dst)


def gen_bishop_moves(board, src):
    """Generate bishop moves"""

    return _gen_ray_moves(board, src, bishop_table[src])


def gen_rook_moves(board, src):
    """Generate rook moves"""

    return _gen_ray_moves(board, src, rook_table[src])


def gen_queen_moves(board, src):
    """Generate queen moves"""

    return _gen_ray_moves(board, src, chain(bishop_table[src], rook_table[src]))


def _gen_simple_moves(board, src, dsts):
    """Generate simple table base moves (i.e. king/knight)"""

    b = board.raw
    stm = board.stm

    for dst in dsts:
        if b[dst] != ' ':
            if get_side(b[dst]) != stm:
                yield Move(src, dst, capture=b[dst])
        else:
            yield Move(src, dst)
        

def gen_knight_moves(board, src):
    """Generate knight moves"""

    return _gen_simple_moves(board, src, knight_table[src])


def gen_king_moves(board, src):
    """Generate king moves"""

    return _gen_simple_moves(board, src, king_table[src])
    

movefunc['p'] = gen_pawn_moves
movefunc['n'] = gen_knight_moves
movefunc['b'] = gen_bishop_moves
movefunc['r'] = gen_rook_moves
movefunc['q'] = gen_queen_moves
movefunc['k'] = gen_king_moves
