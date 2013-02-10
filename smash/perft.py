from smash.movegen import gen_moves


def perft(board, depth, ply):
    count = 0
    for m in gen_moves(board):
        board.move(m)
        if board.is_legal():
            if depth == 1:
                count += 1
            else:
                count += perft(board, depth-1, ply+1)
        board.undo()
    return count
