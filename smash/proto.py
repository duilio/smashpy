import sys
import logging

from smash.board import Board
from smash.move import Move


log = logging.getLogger(__name__)


class Protocol(object):
    def __init__(self, engine, board_class):
        self.engine = engine
        self.board_class = Board

    def loop(self):
        self._quit = False
        while not self._quit:
            cmd = self.read_command()
            self.exec_command(cmd)

    def read_command(self):
        raise NotImplemented()

    def exec_command(self):
        raise NotImplemented()

    def read_input(self):
        r = raw_input().strip()
        log.debug('>>> %s', r)
        return r

    def write(self, s):
        log.debug('<<< %s', s)
        sys.stdout.write(s + '\n')
        sys.stdout.flush()


class UCIProtocol(Protocol):
    def __init__(self, engine, board_class=Board):
        super(UCIProtocol, self).__init__(engine, board_class)

    def read_command(self):
        cmd = self.read_input()
        cmd = cmd.split()
        args = cmd[1:]
        cmdname = cmd[0]

        return cmdname, args

    def exec_command(self, cmd):
        cmdname, args = cmd
        if cmdname == 'uci':
            self.write('id name %s' % self.engine.name)
            self.write('id author %s' % self.engine.author)
            self.write('uciok')
        elif cmdname == 'debug':
            if args[0] == 'on':
                self.engine.debug = True
            else:
                self.engine.debug = False
        elif cmdname == 'isready':
            self.write('readyok')
        elif cmdname == 'setoption':
            # TODO: set engine options
            pass
        elif cmdname == 'ucinewgame':
            # TODO: reset the game engine
            pass
        elif cmdname == 'position':
            if args[0] == 'startpos':
                board = self.board_class()
                moves = args[1:]
            elif args[0] == 'fen':
                board = self.board_class(' '.join(args[1:7]))
                moves = args[7:]

            for move in moves:
                m = Move.from_string(board, move)
                board.move(m)
            self.board = board
        elif cmdname == 'go':
            self._go_command(args)
        elif cmdname == 'stop':
            self.engine.stop()
        elif cmdname == 'ponderhit':
            # TODO: handle ponder
            pass
        elif cmdname == 'quit':
            self.engine.stop()
            self._quit = True
        else:
            log.warning('Unknown command: %s' % cmdname)

    def _go_command(self, args):
        # TODO: parse arguments
        move, score = self.engine.bestmove(self.board)
        self.write('info cp %s' % score)
        self.write('bestmove %s' % move.str_simple())
