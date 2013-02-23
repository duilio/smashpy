MAT_SCORES = {
    'p': 10,
    'n': 30,
    'b': 30,
    'r': 50,
    'q': 80,
    }

INF = 100000

for p in 'PNBRQ':
    MAT_SCORES[p] = MAT_SCORES[p.lower()]


def evaluate(board):
    """Evaluates a board static position

    Returns a score relative to the `stm`.
    
    """
    b = board.raw
    white_score, black_score = evaluate_material(b)

    if board.stm == 'w':
        return white_score - black_score
    else:
        return black_score - white_score


def evaluate_material(b):
    """Evaluates the material

    Returns a tuple ``white_score, black_score``

    """
    white_score = _evaluate_material(b, 'PNBRQ')
    black_score = _evaluate_material(b, 'pnbrq')
    return white_score, black_score


def _evaluate_material(b, pieces):
    score = 0
    for p in pieces:
        score += (b == p).sum() * MAT_SCORES[p]
    return score
