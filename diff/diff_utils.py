import tokenize

from io import BytesIO
from token import tok_name

KEYWORDS = ['def', 'for', 'while', 'class', 'pass',
            'if', 'import', 'in', 'return']


def tokenize_file(filename):
    tokenized_file = []
    for line in open(filename, 'r'):
        tokens = tokenize.tokenize(BytesIO(line.encode('utf-8')).readline)
        result = [{'kind': tok_name[x[0]], 'token': x[1]}
                  for x in tokens if x[1] not in ('utf-8', '', '\n')]
        tokenized_file.append(result)
    return tokenized_file


def get_similarity(similarities, line1, line2, i, j, mode='fast'):
    if similarities[i][j] != -1:
        return similarities[i][j]
    else:
        if mode == 'fast':
            similarity = calculate_fast_similarity(line1, line2)
        else:
            similarity = calculate_slow_similarity(line1, line2)
        similarities[i][j] = similarity
        return similarity


def calculate_slow_similarity(line1, line2):
    """
    Uses the algorithm LCS (longest common subsequence)
    """
    if not line1 or not line2:
        return 0.0
    x, xs, y, ys = line1[0], line1[1:], line2[0], line2[1:]
    if x['token'] == y['token']:
        return 1.0 + calculate_slow_similarity(xs, ys)
    elif x['kind'] == 'NAME' and y['kind'] == 'NAME':
        if x['token'] not in KEYWORDS:
            return 0.5 + calculate_slow_similarity(xs, ys)
        else:
            return calculate_slow_similarity(xs, ys)
    else:
        return max(calculate_slow_similarity(line1, ys),
                   calculate_slow_similarity(xs, line2))


def calculate_fast_similarity(line1, line2):
    i = 0
    j = 0
    similarity = 0.0

    if len(line1) != len(line2):
        similarity -= 1.0

    while i < len(line1) and j < len(line2):
        word1, word2 = line1[i], line2[j]

        if word1['token'] == word2['token']:
            similarity += 1.0
            i += 1
            j += 1
            continue

        # Adds 0.5, if lines have different indents
        if word1['kind'] == 'INDENT':
            similarity -= 0.5
            i += 1
            continue

        if word2['kind'] == 'INDENT':
            similarity -= 0.5
            j += 1
            continue

        if word1['kind'] == 'NAME' and word2['kind'] == 'NAME':
            if word1['token'] not in KEYWORDS:
                similarity += 0.5

        i += 1
        j += 1
    return similarity


def get_context_similarity(similarities, old_file, new_file,
                           i, j, n, mode='fast'):
    similarity = 0.0
    start = -n
    finish = n + 1
    if i - n < 0 or j - n < 0:
        start = max(-i, -j)
    if len(old_file) <= i + n or len(new_file) <= j + n:
        finish = min(len(old_file) - i, len(new_file) - j)

    for k in range(start, finish):
        similarity += get_similarity(similarities,
                                     old_file[i + k], new_file[j + k],
                                     i + k, j + k, mode=mode)
    return similarity
