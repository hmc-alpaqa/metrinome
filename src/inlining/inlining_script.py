"""Adds always inline attribute to C Files."""

import re

from utils import show_func_defs


def get_lines(file: str) -> list[str]:
    """Obtain the lines we should write to the new file."""
    function_calls_dict = show_func_defs(file)

    # Store the line numbers.
    lines_to_inline = []
    for val in function_calls_dict.values():
        lines_to_inline.append(re.split('[-:]', val)[-2])
    lines_to_inline.pop()  # pop off main's line number

    lines = []
    # Open the file that needs to be inlined.
    with open(file, 'r') as old_f:
        line_num = 0
        for line in old_f:
            line_num += 1
            if str(line_num) in lines_to_inline:
                lines.append("__attribute__((always_inline)) inline " + line)
            else:
                lines.append(line)

    return lines


def in_lining(file: str) -> None:
    """Create inlined version of existing C file."""
    # Open new file to write in-lined version into.
    with open((file.split('.')[0]) + "-auto-inline.c", "w") as new_f:
        new_f.writelines(get_lines(file))


def main() -> None:
    """Create inline versions of all test files."""
    files_to_inline = ['test-40-un-inlined.c']

    for file in files_to_inline:
        in_lining(f"/app/code/tests/cFiles/inlining_tests/{file}")


if __name__ == "__main__":
    main()
