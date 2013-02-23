from base import squares, squares_inv, rank, col, pair2square


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
