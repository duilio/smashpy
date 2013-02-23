from contextlib import contextmanager

from smash.evaluate import INF, evaluate
from smash.movegen import gen_moves


@contextmanager
def moving(board, move):
    """Context manager to make a move and undo it at the end"""

    try:
        board.move(move)
        yield board
    finally:
        board.undo()


def mate_score(ply):
    """Mate score is relative to the number of plies followed"""

    return -(INF - ply)


class Engine(object):
    DEFAULT_CONFIG = {
        'depth': 4,
        }

    name = 'Smash'
    author = 'Maurizio Sambati'

    def __init__(self, **config):
        self.config = self.DEFAULT_CONFIG.copy()
        self.config.update(config)

    def check_end(self, board, ply):
        """Check the end of a game

        Only check for checkmates and stale draw.

        NOTE: This function doesn't check draw by move repetitions or rule 50.

        """
        for move in gen_moves(board):
            with moving(board, move):
                if board.is_legal():
                    return None

        if board.checked:
            return -mate_score(ply)
        else:
            return 0

    def bestmove(self, board):
        """Returns the best move and its score"""

        score, move = self._search(board, self.config['depth'])
        return (move, score)

    def stop(self):
        self._stop = True

    def _search(self, board, depth, ply=1):
        """Search recursively for the best move"""

        assert depth >= 0
        assert ply >= 1
        assert board.is_legal()

        # the search terminates at depth = 0
        # just check for a mate/draw or returns an heuristic score
        if depth == 0:
            score = self.check_end(board, ply)
            if score is not None:
                return score, None

            return evaluate(board), None

        alpha = -INF
        bestmove = None

        for move in gen_moves(board):
            with moving(board, move):
                if not board.is_legal():
                    continue

                score, _ = self._search(board, depth-1, ply+1)
                score = -score

                if bestmove is None or score > alpha:
                    alpha = score
                    bestmove = move

        # if no move was found, then we must be in an game over
        if bestmove is None:
            if board.checked:
                return -INF, None
            else:
                return 0, None

        return alpha, bestmove
