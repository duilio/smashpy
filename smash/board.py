import numpy as np

pieces = ' PNBRQK pnbrqk'
squares = [''.join([c, r]) for r in '12345678' for c in 'abcdefgh']
squares = {label: idx for idx, label in enumerate(squares)}
sides = 'wb'


def is_black(x):
    return x.lower()


def is_white(x):
    return x.upper()


def get_side(x):
    if is_white(x):
        return 'b'
    else:
        return 'w'


def rank(sq):
    return int(sq / 8)


def col(sq):
    return int(sq % 8)


def pair2square(r, c):
    return r * 8 + c


START_POSITION = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'


class Board(object):
    def __init__(self, fen=START_POSITION):
        self._board = board = np.empty(64, dtype='c')
        board[:] = ' '
        i = 0
        pieces, stm, castling, en_passant, rule50, movecnt = fen.split()
        for p in pieces:
            if p.isdigit():
                i += int(p)
                continue
            elif p == '/':
                continue
            r, c = rank(i), col(i)
            sq = pair2square(7-r, c)
            i += 1
            board[sq] = p

        self._stm = stm

        self._castling = {'K': 0, 'Q': 0, 'k': 0, 'q': 0}
        for c in castling:
            assert c in 'KQkq'
            self._castling[c] = 1

        self._en_passant = squares.get(en_passant, None)
        self._rule50 = int(rule50)
        self._movecnt = int(movecnt)

    def __str__(self):
        lines = []
        lines.append('   '.join(' ABCDEFGH'))
        for row_idx in range(8, 0, -1):
            row = self._board[(row_idx-1)*8:(row_idx)*8]
            lines.append(' | '.join([str(row_idx)] + map(str, row)) + ' | ' + str(row_idx))
        lines.append('   '.join(' ABCDEFGH'))
        return '\n'.join(lines)

    def fen(self):
        out = []

        spaces = [(' '*x, str(x)) for x in range(1, 9)]

        def collapse(row):
            row = ''.join(row)
            for s, n in reversed(spaces):
                row = row.replace(s, n)
            return row
        
        for row_idx in range(8, 0, -1):
            out.append(collapse(self._board[(row_idx-1)*8:(row_idx)*8]))

        out = ['/'.join(out)]

        out.append(self.stm)
        out.append(''.join(p for p in 'KQkq' if self.castling[p]))

        inv_squares = {v: k for k, v in squares.items()}
        out.append(inv_squares.get(self.en_passant, '-'))

        out.append(str(self._rule50))
        out.append(str(self._movecnt))

        return ' '.join(out)

    @property
    def stm(self):
        return self._stm

    @property
    def en_passant(self):
        return self._en_passant

    @property
    def raw(self):
        return self._board

    @property
    def castling(self):
        return self._castling
