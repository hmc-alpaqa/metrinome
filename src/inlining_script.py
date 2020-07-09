"""Adds always inline attribute to C Files."""

import re
from utils import show_func_defs


def in_lining(file):
    """Create inlined version of existing C file."""
    function_calls_dict = show_func_defs(file)

    # store the line numbers
    lines_to_inline = []
    for val in function_calls_dict.values():
        val = re.split('[-:]', val)
        lines_to_inline.append(val[-2])
    lines_to_inline.pop()  # pop off main's line number

    # open the file that needs to be inlined
    with open(file, 'r') as old_f:
        # open new file to write in-lined version into
        with open((file.split('.')[0]) + "-auto-inline.c", "w") as new_f:
            # write the new file
            line_num = 0
            for line in old_f:
                line_num += 1
                if str(line_num) in lines_to_inline:
                    new_f.write("__attribute__((always_inline)) inline " + line)
                else:
                    new_f.write(line)


def main():
    """Create inline versions of all test files."""
    files_to_inline = ['test-20-un-inlined.c', 'test-21-un-inlined.c', 'test-22-un-inlined.c',
                       'test-23-un-inlined.c']

    # files_to_inline = ['test-01-un-inlined.c', 'test-02-un-inlined.c', 'test-03-un-inlined.c',
    #                    'test-04-un-inlined.c', 'test-05-un-inlined.c', 'test-06-un-inlined.c',
    #                    'test-07-un-inlined.c', 'test-08-un-inlined.c', 'test-09-un-inlined.c',
    #                    'test-10-un-inlined.c', 'test-11-un-inlined.c', 'test-12-un-inlined.c']

    for file in files_to_inline:
        print(file)
        in_lining(f"/app/code/tests/cFiles/inlining_tests/{file}")
        # in_lining('/app/code/tests/cFiles/inlining_tests/'+str(file))


if __name__ == "__main__":
    main()
