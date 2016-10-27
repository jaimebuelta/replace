'''
Perform multiline replacements in files

Limitations:
    Only literals
    Only full lines

TO DO:
    Patterns (using python parse module for clarity)


'''
import os
import argparse


def check_file(filepath, input_pattern):
    '''
    Check the file contains the input_pattern, returns true if so
    '''
    # print filepath, input_pattern
    with open(filepath) as fp:
        to_check = 0
        pattern_len = len(input_pattern)
        for line in fp:
            # print 'line', line, to_check
            clean_line = line.lstrip(' ')
            # print 'clean_line', repr(clean_line)
            if clean_line == input_pattern[to_check].lstrip(' '):
                # print 'checking', to_check
                to_check += 1
                if to_check == pattern_len:
                    # We have a match!
                    return True
            else:
                to_check = 0

    return False


def get_files(directory, input_pattern):
    to_replace = []
    for root, sub_folders, files in os.walk(directory, topdown=True):
        for filename in files:
            # Open the file and check the input pattern
            path = os.path.join(root, filename)
            if check_file(path, input_pattern):
                to_replace.append(path)

    return to_replace


def replace_files(filepaths, input_pattern, output_pattern):
    for filepath in filepaths:
        with open(filepath) as fp:
            new_file = replace_file(fp, input_pattern,
                                    output_pattern)
        with open(filepath, 'w') as fp:
            fp.write(new_file)


def replace_file(fp, input_pattern, output_pattern):

    output_file = []
    to_check = 0
    pattern_len = len(input_pattern)
    replace_lines = []
    indent_level = -1
    for line in fp:
        clean_line = line.lstrip(' ')
        replace_lines.append(line)

        if clean_line == input_pattern[to_check].lstrip(' '):
            if to_check == 0:
                # Store the indentation level
                indent_level = len(line) - len(clean_line)
            # Possible part of a replacement
            to_check += 1
            if to_check == pattern_len:
                # Bingo, replace the lines
                replace_lines = [' ' * indent_level + line
                                 for line in output_pattern]
                to_check = 0

        else:
            output_file.extend(replace_lines)
            to_check = 0
            replace_lines = []

    return ''.join(output_file)


def main_replace(input_file, output_file, dir):
    with open(input_file) as fp:
        input_pattern = [line for line in fp]
    with open(output_file) as fp:
        output_pattern = [line for line in fp]

    to_replace = get_files(dir, input_pattern)
    # print 'Files to replace:', to_replace
    replace_files(to_replace, input_pattern, output_pattern)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Perform simple multiline replacements'
    )

    parser.add_argument('dir', nargs='?',
                        help='Directory to search', default='.')
    parser.add_argument('input_file',
                        help='File with the pattern to be replaced')
    parser.add_argument('output_file',
                        help='File with the replacement pattern')
    args = parser.parse_args()
    main_replace(args.input_file, args.output_file, args.dir)
