import sys

from argparse import ArgumentParser


class SpoonInterpreter(object):
    TRANSLATE = {
        '1': 'incValue',
        '000': 'decValue',
        '010': 'nextCell',
        '011': 'prevCell',
        '00100': 'startCycle',
        '0011': 'endCycle',
        '0010110': 'readValue',
        '001010': 'printValue'
    }

    def interpret(self, code):
        translated_code = self.translate_code(code)
        self.run(translated_code)

    def translate_code(self, code):
        result = []
        symbol = ''
        length = 0
        for ch in code:
            length += 1
            symbol += ch
            if symbol in self.TRANSLATE:
                result.append(self.TRANSLATE[symbol])
                symbol = ''
                length = 0
        return result

    def run(self, code):
        cells = [0] * 30000
        j = 0
        brc = 0

        i = 0
        l = len(code)
        while i < l:
            comand = code[i]
            if comand == 'nextCell':
                j += 1
            elif comand == 'prevCell':
                j -= 1
            elif comand == 'incValue':
                cells[j] += 1
            elif comand == 'decValue':
                cells[j] -= 1
            elif comand == 'printValue':
                print(chr(cells[j]), end='')
            elif comand == 'readValue':
                symbol = sys.stdin.read(1)
                if symbol == '':
                    cells[j] = 0
                else:
                    cells[j] = ord(symbol)
            elif comand == 'startCycle':
                if cells[j] == 0:
                    i += 1
                    while brc > 0 or code[i] != 'endCycle':
                        if code[i] == 'startCycle':
                            brc += 1
                        if code[i] == 'endCycle':
                            brc -= 1
                        i += 1
            elif comand == 'endCycle':
                if cells[j] != 0:
                    i -= 1
                    while brc > 0 or code[i] != 'startCycle':
                        if code[i] == 'endCycle':
                            brc += 1
                        if code[i] == 'startCycle':
                            brc -= 1
                        i -= 1
                    i -= 1
            i += 1


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("filename", help="Spoon code filename")
    args = parser.parse_args()
    return args


def get_code_from_file(filename):
    with open(filename, mode='r') as f:
        code = f.readline()
        if code[-1] == '\n':
            code = code[:-1]
    return code


if __name__ == '__main__':
    args = parse_args()
    filename = args.filename
    code = get_code_from_file(filename)

    spoon_interpreter = SpoonInterpreter()
    spoon_interpreter.interpret(code)
