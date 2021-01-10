"""Adds always inline attribute to C Files."""
from typing import List, Tuple


def get_lines(file: str) -> Tuple[bool, List[str]]:
    """Obtain the lines we should write to the new file."""
    # Open the file that needs to be inlined.
    num = 0
    has_recursion = False
    lines = []
    # Get the lines for the new file.
    with open(file, 'r') as old_f:
        for line in old_f:
            prefixes = ('int', 'void', 'double', 'bool', 'float', 'char', 'static',
                        'extern', 'unsigned char', 'uint_fast32_t', 'enum', 'struct',
                        'Line_ptr')
            excludes = (' main', ' = ')
            if 'inline' in line:
                lines.append("__attribute__((always_inline)) " + line)
                num += 1
            elif any(line.startswith(prefix) for prefix in prefixes) and \
                    all(exclude not in line for exclude in excludes) and \
                    ('_GL_ATTRIBUTE' in line or 'ATTRIBUTE_' in line):
                lines.append("__attribute__((always_inline)) inline " + line)
                num += 1
            elif any(line.startswith(prefix) for prefix in prefixes) and ('(' in line) and \
                    not (('{' in line) ^ (')' in line)) and \
                    all(exclude not in line for exclude in excludes):
                lines.append("__attribute__((always_inline)) inline " + line)
                num += 1
            elif any(line.startswith(prefix) for prefix in prefixes) and ('(' in line) and \
                    (')' in line) and \
                    all(exclude not in line for exclude in excludes):
                lines.append("__attribute__((always_inline)) inline " + line)
                num += 1
            else:
                lines.append(line)

            if ('recurse' in line) or ('recursion' in line) or ('recursive' in line):
                has_recursion = True

    return has_recursion, lines


def in_lining(file: str) -> bool:
    """Create inlined version of existing C file."""
    has_recursion, lines = get_lines(file)

    # Open new file to write in-lined version into.
    with open(file.split('.')[0] + "-auto-inline.c", "w") as new_f:
        new_f.writelines(lines)

    return has_recursion


def main() -> None:
    """Create inline versions of all test files."""
    files_to_inline = ['04_prime_helper.c']

    for file in files_to_inline:
        in_lining(f"/app/code/tests/cFiles/in_lining_tests_on_fse/{file}")


if __name__ == "__main__":
    main()
