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
