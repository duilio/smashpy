import time

from smash.evaluate import INF, evaluate
from smash.movegen import gen_moves


def mate_score(ply):
    """Mate score is relative to the number of plies followed"""

    return -(INF - ply)


class Stat(object):
    __slots__ = ['nodes', 'leaves', 'mates', 'draws', 't_start']

    def __init__(self):
        self.reset()

    def reset(self):
        self.t_start = time.time()
        self.nodes = 0
        self.leaves = 0
        self.mates = 0
        self.draws = 0


class Engine(object):
    DEFAULT_CONFIG = {
        'depth': 4,
        }

    name = 'Smash'
    author = 'Maurizio Sambati'

    def __init__(self, **config):
        self.config = self.DEFAULT_CONFIG.copy()
        self.config.update(config)
        self.stat = Stat()

        def _cb_null(*args, **kwargs):
            pass

        self._cb_info = _cb_null

    def check_end(self, board, ply):
        """Check the end of a game

        Only check for checkmates and stale draw.

        NOTE: This function doesn't check draw by move repetitions or rule 50.

        """
        for move in gen_moves(board):
            with board.moving(move):
                if board.is_legal():
                    return None

        if board.checked:
            return -mate_score(ply)
        else:
            return 0

    def bestmove(self, board):
        """Returns the best move and its score"""

        self.stat.reset()
        score, move = self._search(board, self.config['depth'])
        self.send_info(depth=self.config['depth'], score=score, pv=[move])
        return (move, score)

    def stop(self):
        self._stop = True

    def _search(self, board, depth, ply=1):
        """Search recursively for the best move"""

        assert depth >= 0
        assert ply >= 1
        assert board.is_legal()

        stat = self.stat
        stat.nodes += 1

        # the search terminates at depth = 0
        # just check for a mate/draw or returns an heuristic score
        if depth == 0:
            stat.leaves += 1
            score = self.check_end(board, ply)
            if score is not None:
                if score == 0:
                    stat.draws += 1
                else:
                    stat.mates += 1
                return score, None

            return evaluate(board), None

        alpha = -INF
        bestmove = None

        for move in gen_moves(board):
            with board.moving(move):
                if not board.is_legal():
                    continue

                score, _ = self._search(board, depth-1, ply+1)
                score = -score

                if bestmove is None or score > alpha:
                    alpha = score
                    bestmove = move

        # if no move was found, then we must be in an game over
        if bestmove is None:
            stat.leaves += 1
            if board.checked:
                stat.mates += 1
                return -INF, None
            else:
                stat.draws += 1
                return 0, None

        return alpha, bestmove

    def set_cb_info(self, cb):
        self._cb_info = cb

    def send_info(self, depth, score, pv):
        self._cb_info(depth=depth, score=score, pv=pv, nodes=self.stat.nodes,
                      time=(time.time() - self.stat.t_start))
