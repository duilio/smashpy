from smash.base import BaseBoard, SquareHelper, START_POSITION

# workarounds for pyflakes
SquareHelper
START_POSITION


class Board(BaseBoard):
    def set_check_status(self):
        return False
