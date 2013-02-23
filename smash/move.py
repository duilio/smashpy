import re
from base import squares, squares_inv, rank, col, pair2square


SAN_EXP = re.compile(r'^(?P<piece>[PNRBQK])?(?P<src>[a-h][1-8]?)?(?P<capture>[x:])?-?(?P<dst>[a-h]?[1-8]?)(?:e\.p)?(?P<promote>(?:=)?[NBRQ]|(?:\()[NBRQ](?:\)))?(?:\+)?$')


class Move(object):
    __slot__ = ['src', 'dst', 'en_passant', 'capture', 'promote']

    def __init__(self, src, dst, capture=None, en_passant=None, promote=None):
        self.src = src
        self.dst = dst
        self.en_passant = en_passant
        self.capture = capture
        self.promote = promote

    def __eq__(self, other):
        return self._tuple() == other._tuple()

    def __str__(self):
        return str(self._tuple())

    def __repr__(self):
        return 'Move' + str(self)

    def __hash__(self):
        return hash(self._tuple())

    def __lt__(self, other):
        return self._tuple() < other._tuple()

    def _tuple(self):
        return (self.src, self.dst, self.en_passant, self.capture, self.promote)

    def str_simple(self):
        """Returns a string representing the Move object

        The string is compatible to UCI move format and can be read by humans too.

        The format is {src}{dst}{promote}, where promote is optional and the piece
        is always lowercase.

        Examples:

        >>> from base import SquareHelper
        >>> sq = SquareHelper()

        >>> Move(sq.e2, sq.e4, en_passant=sq.e3).str_simple()
        'e2e4'

        >>> Move(sq.e4, sq.d5, capture='p').str_simple()
        'e4e5'

        >>> Move(sq.e7, sq.e8, promote='Q').str_simple()
        'e7e8q'

        """
        if self.promote:
            promote = self.promote.lower()
        else:
            promote = ''
        return squares_inv[self.src] + squares_inv[self.dst] + promote

    @classmethod
    def from_string(cls, board, s):
        """Parses a string and returns a Move object

        Strings format is the same produced by `str_simple` method.

        NOTE: This method doesn't check for the move legality.
        It could actually move nothing or capture piece of the same side or
        promote a white queen to a black bishop in g6.

        """
        src, dst, promote = s[:2], s[2:4], s[4:]
        capture = None
        en_passant = None

        # check for promote
        if not promote:
            promote = None
        else:
            if board.stm == 'w':
                promote = promote.upper()

        src = squares[src]
        dst = squares[dst]

        # check for capture
        b = board.raw
        if b[dst] != ' ':
            capture = b[dst]
        elif dst == board.en_passant:
            capture = 'p' if board.stm == 'w' else 'P'

        # check for pawn double push (and set en passant square)
        if b[src] in 'pP':
            rsrc, rdst = rank(src), rank(dst)
            if abs(rsrc - rdst) == 2:
                rep = (rsrc + rdst) / 2
                en_passant = pair2square(rep, col(src))

        return cls(src, dst, capture=capture, en_passant=en_passant,
                   promote=promote)

    @classmethod
    def from_san(cls, board, s):
        """Parses a SAN move

        """
        CASTLING = {
            'w': {
                'src': squares['e1'],
                'k_dst': squares['g1'],
                'q_dst': squares['c1'],
                },
            'b': {
                'src': squares['e8'],
                'k_dst': squares['g8'],
                'q_dst': squares['c8'],
                }
            }

        # special case: castling
        if s in ('0-0', 'O-O'):
            sq = CASTLING[board.stm]
            return Move(sq['src'], sq['k_dst'])
        elif s in ('0-0-0', 'O-O-O'):
            sq = CASTLING[board.stm]
            return Move(sq['src'], sq['q_dst'])

        p, src, capture, dst, promote = SAN_EXP.match(s).groups()

        #
        # fill missing information
        #

        if not p:
            p = 'P'

        if not dst:
            dst = src
            src = None

        # convert piece name to a side-aware name
        if board.stm == 'b':
            p = p.lower()
            if promote:
                promote = promote.lower()

        b = board.raw
        moves = [m for m in board.legal_moves() if b[m.src] == p]
        assert moves

        def parse_square(square):
            """Returns the square coordinates

            NOTE: either column or rank might miss... in this case we return None

            """
            columns = dict(zip('abcdefgh', range(8)))
            ranks = dict(zip('12345678', range(8)))

            if square[0] in columns:
                c = columns[square[0]]
                square = square[1:]
            else:
                c = None

            if square and square[0] in ranks:
                r = ranks[square[0]]
            else:
                r = None

            return r, c

        # filter by source square (if any...)
        if src:
            src_r, src_c = parse_square(src)
            if src_r is not None:
                moves = [m for m in moves if rank(m.src) == src_r]

            if src_c is not None:
                moves = [m for m in moves if col(m.src) == src_c]

        # filter by dst square (required!)
        dst_r, dst_c = parse_square(dst)
        if dst_r is not None:
            moves = [m for m in moves if rank(m.dst) == dst_r]

        if dst_c is not None:
            moves = [m for m in moves if col(m.dst) == dst_c]

        assert moves

        # if it is required the move to be a capture, filter non captures
        if capture:
            moves = [m for m in moves if m.capture]

        # filter by promoted piece
        if promote:
            moves = [m for m in moves if m.promote == promote]

        assert len(moves) == 1
        return moves[0]
