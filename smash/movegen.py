"""Move generator"""

from itertools import chain

import numpy as np

from smash.move import Move
from smash.base import pair2square, rank, col, get_side, swap_side
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


def _gen_ray_moves(board, src, rays, stm):
    """Generate table based ray moves (i.e. bishop/rook moves)"""

    b = board.raw

    for ray in rays:
        for dst in ray:
            if b[dst] != ' ':
                if get_side(b[dst]) != stm:
                    yield Move(src, dst, capture=b[dst])
                break
            else:
                yield Move(src, dst)


def gen_bishop_moves(board, src, stm=None):
    """Generate bishop moves"""

    if stm is None:
        stm = board.stm
    return _gen_ray_moves(board, src, bishop_table[src], stm)


def gen_rook_moves(board, src, stm=None):
    """Generate rook moves"""

    if stm is None:
        stm = board.stm
    return _gen_ray_moves(board, src, rook_table[src], stm)


def gen_queen_moves(board, src, stm=None):
    """Generate queen moves"""

    if stm is None:
        stm = board.stm
    return _gen_ray_moves(board, src, chain(bishop_table[src], rook_table[src]), stm)


def _gen_simple_moves(board, src, dsts, stm):
    """Generate simple table base moves (i.e. king/knight)"""

    b = board.raw

    for dst in dsts:
        if b[dst] != ' ':
            if get_side(b[dst]) != stm:
                yield Move(src, dst, capture=b[dst])
        else:
            yield Move(src, dst)
        

def gen_knight_moves(board, src, stm=None):
    """Generate knight moves"""

    if stm is None:
        stm = board.stm

    return _gen_simple_moves(board, src, knight_table[src], stm)


def gen_king_moves(board, src, stm=None, do_castling=True):
    """Generate king moves"""

    if stm is None:
        stm = board.stm

    for m in _gen_simple_moves(board, src, king_table[src], stm):
        yield m

    if do_castling and not board.checked:
        for m in _gen_castling_moves(board, src, stm):
            yield m


def _gen_castling_moves(board, src, stm):
    b = board.raw
    ks_dst = src + 2
    ks_transit = src + 1
    qs_dst = src - 2
    qs_transit = src - 1
    qs_transit_rook = src - 3
    if stm == 'w':
        ks = 'K'
        qs = 'Q'
    else:
        ks = 'k'
        qs = 'q'

    xside = swap_side(stm)
    if board.castling[ks] and b[ks_transit] == ' ' and b[ks_dst] == ' ' \
            and not board.can_attack(xside, ks_transit):
        yield Move(src, ks_dst)
    if board.castling[qs] and b[qs_transit] == ' ' and b[qs_transit_rook] == ' ' \
            and b[qs_dst] == ' ' and not board.can_attack(xside, qs_transit):
        yield Move(src, qs_dst)
    

def _gen_ray_captures(board, src, rays, stm):
    b = board.raw
    for ray in rays:
        for dst in ray:
            if b[dst] != ' ':
                if get_side(b[dst]) != stm:
                    yield b[dst]
                break


def _gen_simple_captures(board, src, dsts, stm):
    b = board.raw
    for dst in dsts:
        if b[dst] != ' ':
            if get_side(b[dst]) != stm:
                yield b[dst]


def gen_knight_captures(board, src, stm=None):
    stm = stm or board.stm
    for m in _gen_simple_captures(board, src, knight_table[src], stm):
        yield m


def gen_king_captures(board, src, stm=None):
    stm = stm or board.stm
    for m in _gen_simple_captures(board, src, king_table[src], stm):
        yield m


def gen_bishop_captures(board, src, stm=None):
    stm = stm or board.stm
    for m in _gen_ray_captures(board, src, bishop_table[src], stm):
        yield m


def gen_rook_captures(board, src, stm=None):
    stm = stm or board.stm
    for m in _gen_ray_captures(board, src, rook_table[src], stm):
        yield m


movefunc['p'] = gen_pawn_moves
movefunc['n'] = gen_knight_moves
movefunc['b'] = gen_bishop_moves
movefunc['r'] = gen_rook_moves
movefunc['q'] = gen_queen_moves
movefunc['k'] = gen_king_moves
