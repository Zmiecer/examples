import argparse

from diff_utils import get_context_similarity, tokenize_file


class Diff(object):
    MAX_LINES_COUNT = 5000

    def __init__(self, old_file_name, new_file_name, context_count=1,
                 visibility=MAX_LINES_COUNT, mode='fast'):
        """
        :param old_file_name: Name of the file from old revision.
        :param new_file_name: Name of the file from new revision.
        :param context_count: Length of contexts: number of lines before and
        after line to calculate similarity.
        :param visibility: Number of lines before and after current
        to compare with.
        :param mode: Calculating mode. Module has two modes:
        'fast' (uses brute-force) and 'slow' (uses LCS algorithm).
        """
        self.old_file = []
        self.new_file = []
        self.accordance = []

        self.context_count = context_count
        self.visibility = visibility
        self.mode = mode

        self.check_args(old_file_name, new_file_name)
        self.preprocess(old_file_name, new_file_name)

    def check_args(self, old_file_name, new_file_name):
        if not old_file_name.endswith('.py') \
                or not new_file_name.endswith('.py'):
            raise ValueError("Not valid filename")
        if self.context_count < 0:
            raise ValueError("Context count should be positive, you typed {}"
                             .format(self.context_count))
        if self.visibility < 0:
            raise ValueError("Visibility should be positive, you typed {}"
                             .format(self.visibility))
        if self.mode not in ('fast', 'slow'):
            raise ValueError("Mode should be 'fast' or 'slow', you typed {}"
                             .format(self.mode))

    def read_files(self, old_file_name, new_file_name):
        self.old_file = tokenize_file(old_file_name)
        self.new_file = tokenize_file(new_file_name)
        self.accordance = [-1 for _ in range(len(self.new_file))]

    def calculate_max_similarities(self):
        similarities = [[-1 for _ in range(len(self.old_file))]
                        for _ in range(len(self.new_file))]
        max_similarities = [{'index': -1, 'similarity': -1}
                            for _ in range(len(self.new_file))]
        for j in range(len(self.new_file)):
            max_similarity, max_index = -1, -1
            start, finish = 0, len(self.old_file)

            if self.visibility < self.MAX_LINES_COUNT:
                start = max(0,
                            min(j - self.visibility, len(self.old_file) - 1))
                finish = min(finish, j + self.visibility + 1)

            for i in range(start, finish):
                similarity = get_context_similarity(similarities,
                                                    self.new_file,
                                                    self.old_file,
                                                    j,
                                                    i,
                                                    self.context_count,
                                                    mode=self.mode)
                if similarity > max_similarity:
                    max_similarity, max_index = similarity, i

            max_similarities[j] = {'index': max_index,
                                   'similarity': max_similarity}
        return max_similarities

    def calculate_accordance(self, max_similarities):
        # Accord the most similar lines
        similar = [{'index': -1, 'similarity': -1}
                   for _ in range(len(self.old_file))]
        for i, item in enumerate(max_similarities):
            old_index = item['index']
            if similar[old_index]['similarity'] < item['similarity']:
                prev_index = similar[old_index]['index']
                similar[old_index] = {'index': i,
                                      'similarity': item['similarity']}
                self.accordance[prev_index] = -1
                self.accordance[i] = old_index

        # Set indexes of new blocks to the line before the block
        last_index = -1
        for i, accord in enumerate(self.accordance):
            if accord == -1:
                self.accordance[i] = last_index
            else:
                last_index = accord

    def preprocess(self, old_file_name, new_file_name):
        self.read_files(old_file_name, new_file_name)
        max_similarities = self.calculate_max_similarities()
        self.calculate_accordance(max_similarities)

    def check_pos(self, index):
        if index <= 0:
            raise ValueError("Minimum line number is 1, you typed {}"
                             .format(index))
        if index > len(self.new_file):
            raise ValueError("New file has {} lines, you typed {}"
                             .format(len(self.new_file), index))

    def pos(self, index):
        self.check_pos(index)
        index -= 1
        return self.accordance[index] + 1


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('old_file_name', metavar='Old file name', type=str,
                        help='Name of file of old revision')
    parser.add_argument('new_file_name', metavar='New file name', type=str,
                        help='Name of file from new revision')
    parser.add_argument('line_number', metavar='Line number', type=int,
                        help='Number of the line in the new file')
    parser.add_argument('--context_count', metavar='Context count', default=1,
                        type=int, help='Number of contexts to compare')
    parser.add_argument('--visibility', metavar='Visibility', default=5000,
                        type=int, help='Number of lines to compare with')
    parser.add_argument('--mode', metavar='Calculating mode', default='fast',
                        type=str, help='Calculating mode')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    diff = Diff(
        old_file_name=args.old_file_name,
        new_file_name=args.new_file_name,
        context_count=args.context_count,
        visibility=args.visibility,
        mode=args.mode
    )
    line_number = args.line_number
    print(diff.pos(line_number))
