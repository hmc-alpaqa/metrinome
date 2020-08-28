"""Adds always inline attribute to C Files."""
INPUT_PATH = "/app/code/tests/cFiles/coreutils-8.32/src/"
DESTINATION_PATH = "/app/code/tests/cFiles/coreutils-inlined-heuristic/"


def in_lining(file: str) -> bool:
    """Create inlined version of existing C file."""
    # open the file that needs to be inlined
    num = 0
    has_recursion = False
    with open(file, 'r') as old_f:
        # open new file to write in-lined version into
        # with open(DESTINATION_PATH + file.split('.')[0] + "-auto-inline.h", "w") as new_f:
        with open(file.split('.')[0] + "-auto-inline.c", "w") as new_f:
            # write the new file
            for line in old_f:
                prefixes = ('int', 'void', 'double', 'bool', 'float', 'char', 'static',
                            'extern', 'unsigned char', 'uint_fast32_t', 'enum', 'struct',
                            'Line_ptr')
                excludes = (' main', ' = ')
                if 'inline' in line:
                    new_f.write("__attribute__((always_inline)) " + line)
                    num += 1
                elif any(line.startswith(prefix) for prefix in prefixes) and \
                        all(exclude not in line for exclude in excludes) and \
                        ('_GL_ATTRIBUTE' in line or 'ATTRIBUTE_' in line):
                    new_f.write("__attribute__((always_inline)) inline " + line)
                    num += 1
                elif any(line.startswith(prefix) for prefix in prefixes) and ('(' in line) and \
                        not (('{' in line) ^ (')' in line)) and \
                        all(exclude not in line for exclude in excludes):
                    new_f.write("__attribute__((always_inline)) inline " + line)
                    num += 1
                elif any(line.startswith(prefix) for prefix in prefixes) and ('(' in line) and \
                        (')' in line) and \
                        all(exclude not in line for exclude in excludes):
                    new_f.write("__attribute__((always_inline)) inline " + line)
                    num += 1
                else:
                    new_f.write(line)

                if ('recurse' in line) or ('recursion' in line) or ('recursive' in line):
                    has_recursion = True

            # print(file, num, has_recursion)

    return has_recursion


def main() -> None:
    """Create inline versions of all test files."""
    # files_to_inline = ['test-01-un-inlined.c', 'test-02-un-inlined.c', 'test-03-un-inlined.c',
    #                    'test-04-un-inlined.c', 'test-05-un-inlined.c', 'test-06-un-inlined.c',
    #                    'test-07-un-inlined.c', 'test-08-un-inlined.c', 'test-09-un-inlined.c',
    #                    'test-10-un-inlined.c', 'test-11-un-inlined.c', 'test-12-un-inlined.c']

    files_to_inline = ['test-30-un-inlined.c', 'test-31-un-inlined.c', 'test-32-un-inlined.c',
                       'test-33-un-inlined.c']

    # files_to_inline = ['basenc.c', 'cat.c', 'chcon.c', 'chgrp.c', 'chmod.c',
    #                    'chown-core.c', 'chown.c']

    # for file in os.listdir(INPUT_PATH):
    #     # if file.endswith(".h"):
    #     if file.endswith(".c"):
    #         in_lining(file)

    for file in files_to_inline:
        in_lining(f"/app/code/tests/cFiles/inlining_tests/{file}")


if __name__ == "__main__":
    main()
