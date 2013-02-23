import os
import struct

from smash.base import pair2square, rank, col


def check_pair2square(r, c):
    if r < 0 or r > 7 or c < 0 or c > 7:
        return None
    return pair2square(r, c)


def gen_ray_table(dirs):
    """Generate rays-like table

    For each square follow all directions until an edge is reached.
    
    """
    table = []
    for src in range(64):
        r, c = rank(src), col(src)
        table.append([])

        for dr, dc in dirs:
            dtable = []
            for d in range(1, 8):
                dst = check_pair2square(dr * d + r, dc * d + c)
                if dst is None:
                    break
                dtable.append(dst)
            if dtable:
                table[src].append(dtable)
    return table


def gen_simple_table(dirs):
    """Generate simple tables

    For each square try all directions without extensions.
    
    """
    table = []
    for src in range(64):
        r, c = rank(src), col(src)
        table.append([])
        for dr, dc in dirs:
            dst = check_pair2square(r + dr, c + dc)
            if dst is not None:
                table[src].append(dst)
    return table


def gen_bishop_table():
    return gen_ray_table([(1, 1), (1, -1), (-1, -1), (-1, 1)])


def gen_rook_table():
    return gen_ray_table([(1, 0), (0, 1), (-1, 0), (0, -1)])


def gen_king_table():
    return gen_simple_table([(1, 0), (0, 1), (-1, 0), (0, -1),
                             (1, 1), (1, -1), (-1, -1), (-1, 1)])


def gen_knight_table():
    return gen_simple_table([(2, -1), (2, 1), (1, 2), (-1, 2),
                             (-2, 1), (-2, -1), (-1, -2), (1, -2)])


def nextrand64():
    return struct.unpack('l', os.urandom(8))[0]


def gen_zobrist_keys():
    piece_keys = {}
    for p in 'PNBRQKpnbrqk':
        piece_keys[p] = [nextrand64() for sq in range(64)]

    en_passant_keys = [nextrand64() for c in range(8)]

    castling_keys = {}
    for p in 'KkQq':
        castling_keys[p] = nextrand64()

    stm_key = nextrand64()
    return piece_keys, en_passant_keys, castling_keys, stm_key


def gen_tables():
    import re
    from pprint import PrettyPrinter

    pp = PrettyPrinter(indent=4, width=76)

    def indent(s):
        return re.sub('^', ' '*4, s, flags=re.M)

    output = {
        'knight_table': gen_knight_table(),
        'bishop_table': gen_bishop_table(),
        'rook_table': gen_rook_table(),
        'king_table': gen_king_table(),
        }

    return '\n'.join('%s = \\\n%s\n' % (k, indent(pp.pformat(v)))
                     for k, v in output.iteritems()).rstrip()
