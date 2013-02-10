import numpy as np
from collections import namedtuple


pieces = ' PNBRQK pnbrqk'
squares = [''.join([c, r]) for r in '12345678' for c in 'abcdefgh']
squares = {label: idx for idx, label in enumerate(squares)}
squares_inv = {idx: label for label, idx in squares.iteritems()}
sides = 'wb'


def is_black(x):
    return x.islower()


def is_white(x):
    return x.isupper()


def get_side(x):
    if is_white(x):
        return 'w'
    else:
        return 'b'


def swap_side(x):
    return 'w' if x == 'b' else 'b'


def rank(sq):
    return int(sq / 8)


def col(sq):
    return int(sq % 8)


def pair2square(r, c):
    return r * 8 + c


START_POSITION = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
EN_PASSANT_CAPTURES = {pair2square(5, c): pair2square(4, c) for c in range(8)}
EN_PASSANT_CAPTURES.update({pair2square(2, c): pair2square(3, c) for c in range(8)})


class BaseBoard(object):
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
        if castling != '-':
            for c in castling:
                assert c in 'KQkq'
                self._castling[c] = 1

        self._en_passant = squares.get(en_passant, None)
        self._rule50 = int(rule50)
        self._movecnt = int(movecnt)
        self._checked = self._is_checked()
        self._set_hashkey()

        self._history = [TransitionStatus(None, self.castling.copy(),
                                          self._en_passant, self._rule50,
                                          self._checked, self._hashkey, True)]

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
        if any(self.castling.values()):
            out.append(''.join(p for p in 'KQkq' if self.castling[p]))
        else:
            out.append('-')

        inv_squares = {v: k for k, v in squares.items()}
        out.append(inv_squares.get(self.en_passant, '-'))

        out.append(str(self._rule50))
        out.append(str(self._movecnt))

        return ' '.join(out)

    def move(self, m):
        irreversible = False
        b = self.raw
        p = b[m.dst] = b[m.src]
        b[m.src] = ' '

        old_en_passant = self._en_passant
        self._en_passant = None
        
        if m.promote:
            b[m.dst] = m.promote

        # check if rook or king moved and set castling values
        if p in 'Rr':
            castling_side = {(0, 'w'): 'Q',
                             (56, 'b'): 'q',
                             (7, 'w'): 'K',
                             (63, 'b'): 'k'}.get((m.src, self.stm), None)
            if castling_side and self._castling[castling_side]:
                self._castling[castling_side] = 0
                irreversible = True
        elif p in 'Kk':
            if self.stm == 'w':
                castling_sides = 'KQ'
            else:
                castling_sides = 'kq'
            
            if self._castling[castling_sides[0]] or self._castling[castling_sides[1]]:
                self._castling[castling_sides[0]] = 0
                self._castling[castling_sides[1]] = 0
                irreversible = True

        if p in 'Pp':
            self._rule50 = 0
            irreversible = True

            if m.dst == old_en_passant:
                b[EN_PASSANT_CAPTURES[m.dst]] = ' '
            
            # set the en passant square if it is a double push
            if abs(rank(m.src) - rank(m.dst)) == 2:
                self._en_passant = pair2square((rank(m.src) + rank(m.dst)) / 2,
                                               col(m.src))

        elif m.capture:
            self._rule50 = 0
            irreversible = True

            # if a rook is captures, check if castling flags should be changed
            if m.capture in 'Rr':
                castling_side = {(0, 'b'): 'Q',
                                 (56, 'w'): 'q',
                                 (7, 'b'): 'K',
                                 (63, 'w'): 'k'}.get((m.dst, self.stm), None)
                if castling_side and self._castling[castling_side]:
                    self._castling[castling_side] = 0
                    irreversible = True
            
        elif p in 'Kk' and abs(col(m.src) - col(m.dst)) == 2:
            # if it is a castling move then move also the rook
            r = rank(m.dst)
            c = col(m.dst)
            if c == 2:
                r_src = pair2square(r, 0)
                r_dst = pair2square(r, c+1)
            else:
                r_src = pair2square(r, 7)
                r_dst = pair2square(r, c-1)
            b[r_dst] = b[r_src]
            b[r_src] = ' '
            irreversible = True
        else:
            self._rule50 += 1

        self._movecnt += 1
        self._stm = swap_side(self.stm)
        self._set_hashkey()

        self._checked = self._is_checked()
        
        self._history.append(TransitionStatus(m, self.castling.copy(),
                                              self._en_passant, self._rule50,
                                              self._checked, self._hashkey, irreversible))

    def undo(self):
        assert len(self._history) > 1

        b = self.raw
        m = self._history.pop().move
        status = self._history[-1]

        stm = swap_side(self._stm)

        if m.promote:
            b[m.src] = {'w': 'P', 'b': 'p'}[stm]
        else:
            b[m.src] = b[m.dst]

        b[m.dst] = ' '
        if b[m.src] in 'Pp' and m.dst == status.en_passant:
            b[EN_PASSANT_CAPTURES[m.dst]] = {'w': 'p', 'b': 'P'}[stm]
        elif m.capture:
            b[m.dst] = m.capture

        if b[m.src] in 'Kk' and abs(col(m.dst) - col(m.src)) == 2:
            r = rank(m.dst)
            c = col(m.dst)

            if c == 2:
                r_src = pair2square(r, 0)
                r_dst = pair2square(r, c+1)
            else:
                r_src = pair2square(r, 7)
                r_dst = pair2square(r, c-1)

            b[r_src] = b[r_dst]
            b[r_dst] = ' '

        self._stm = stm
        self._movecnt -= 1
        self._castling.update(status.castling)
        self._en_passant = status.en_passant
        self._rule50 = status.rule50
        self._checked = status.checked
        self._hashkey = status.hashkey

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

    @property
    def checked(self):
        return self._checked

    def can_attack(self, stm, sq):
        raise NotImplemented()

    def is_legal(self):
        xking = {'w': 'k', 'b': 'K'}[self.stm]
        sq = np.where(self.raw == xking)[0][0]
        return not self.can_attack(self.stm, sq)

    def _is_checked(self):
        king = {'w': 'K', 'b': 'k'}[self.stm]
        sq = np.where(self.raw == king)[0][0]
        return self.can_attack(swap_side(self.stm), sq)

    def _set_hashkey(self):
        self._hashkey = hash((self.stm, tuple(self.raw), self.en_passant,
                              tuple(self.castling.iteritems())))
                             
TransitionStatus = namedtuple('TransitionStatus',
                              'move castling en_passant rule50 checked hashkey irreversible')


class SquareHelper(object):
    def __init__(self):
        self.__dict__ = squares
