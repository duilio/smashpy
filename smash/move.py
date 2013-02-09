class Move(object):
    __slot__ = ['src', 'dst', 'en_passant', 'capture', 'promote']

    def __init__(self, src, dst, capture='', en_passant=None, promote=' '):
        self.src = src
        self.dst = dst
        self.en_passant = en_passant
        self.capture = capture
        self.promote = promote

    def __eq__(self, other):
        a = (self.src, self.dst, self.en_passant, self.capture, self.promote)
        b = (other.src, other.dst, other.en_passant, other.capture, other.promote)
        return a == b

    def __str__(self):
        return str((self.src, self.dst, self.en_passant, self.capture, self.promote))

    def __repr__(self):
        return 'Move' + str(self)
