import argparse


def parse_args(argsline):
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--count", action="store_true",
                        help='prefix lines by the number of occurrences')
    parser.add_argument("-d", "--repeat", action="store_true",
                        help='only print duplicate lines, one for each group')
    parser.add_argument("-i", "--ignore-case", action="store_true",
                        help='ignore differences in case when comparing')
    parser.add_argument("-u", "--unique", action="store_true",
                        help='only print unique lines')
    args = parser.parse_args(argsline)
    return args


def resolve(old_string, number_of_lines):
    if (not unique and not repeat) \
            or (unique and number_of_lines == 1) \
            or (repeat and number_of_lines > 1):
        result_string = ''
        if count:
            result_string += str(number_of_lines) + ' '
        result_string += old_string
        return result_string


if __name__ == '__main__':
    argsline = input().split(' ')
    args = parse_args(argsline)
    count = args.count
    repeat = args.repeat
    ignore_case = args.ignore_case
    unique = args.unique

    number_of_lines = 1
    result = []
    n = int(input())
    old_string = input()
    new_string = ''
    for i in range(n - 1):
        new_string = input()
        if new_string == old_string \
                or (ignore_case and new_string.lower() == old_string.lower()):
            number_of_lines += 1
        else:
            result_string = resolve(old_string, number_of_lines)
            if result_string:
                result.append(result_string)
            old_string = new_string
            number_of_lines = 1
    result_string = resolve(old_string, number_of_lines)
    if result_string:
        result.append(result_string)
    print('\n'.join(result))
