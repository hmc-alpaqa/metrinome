"""Adds always inline attribute to C Files."""


def in_lining(file):
    """Create inlined version of existing C file."""
    # open the file that needs to be inlined
    num = 0
    with open(file, 'r') as old_f:
        # open new file to write in-lined version into
        with open((file.split('/')[-1]).split('.')[0] + "-auto-inline.c", "w") as new_f:
        #with open(file + "-auto-inline.c", "w") as new_f:
            # write the new file
            for line in old_f:
                prefixes = ('int', 'void', 'double', 'bool', 'float', 'char', 'static', 'extern')
                if ('inline' in line):
                   new_f.write("__attribute__((always_inline)) " + line)
                   num += 1
                   print(num)
                elif any(line.startswith(prefix) for prefix in prefixes) and \
                   (('(' in line) and (('{' not in line) and (')' not in line) or (('{' in line) and (')' in line))))and \
                   ('main' not in line) and ('=' not in line):
                   new_f.write("__attribute__((always_inline)) inline " + line)
                   num += 1
                   print(num)
                else:
                    new_f.write(line)


def main():
    """Create inline versions of all test files."""
    # files_to_inline = ['test-01-un-inlined.c', 'test-02-un-inlined.c', 'test-03-un-inlined.c',
    #                    'test-04-un-inlined.c', 'test-05-un-inlined.c', 'test-06-un-inlined.c',
    #                    'test-07-un-inlined.c', 'test-08-un-inlined.c', 'test-09-un-inlined.c',
    #                    'test-10-un-inlined.c', 'test-11-un-inlined.c', 'test-12-un-inlined.c']

    # files_to_inline = ['test-20-un-inlined.c', 'test-21-un-inlined.c', 'test-22-un-inlined.c',
    #                    'test-23-un-inlined.c', 'test-25-un-inlined.c']

    files_to_inline = ['basename.c', 'basenc.c', 'cat.c', 'chcon.c', 'chgrp.c', 'chmod.c', 'chown-core.c', 'chown.c', 'chroot.c',
    'cksum.c', 'comm.c', 'copy.c', 'cp-hash.c', 'cp.c', 'csplit.c', 'cut.c', 'date.c', 'dd.c', 'df.c', 'dircolors.c', 'dirname.c', 'du.c']

    for file in files_to_inline:
        print(file)
        in_lining(f"/app/code/tests/cFiles/coreutils-8.32/src/{file}")
        #in_lining(f"/app/code/tests/cFiles/inlining_tests/{file}")
\


if __name__ == "__main__":
    main()
