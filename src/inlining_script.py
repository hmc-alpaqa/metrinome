"""Adds always inline attribute to C Files."""

import utils
import re
from utils import show_func_defs

def in_lining(file):
    function_calls_dict = show_func_defs(file)

    # store the line numbers of 
    lines_to_inline = []
    for x in function_calls_dict.values():
        x = re.split('[-:]', x)
        lines_to_inline.append(x[-2])
    lines_to_inline.pop()  # pop off main's line number 

    # open the file that needs to be inlined 
    f = open(file, 'r')

    # open new file to write in-lined version into 
    new_f = open((file.split('.')[0])+"-auto-inline.c", "w")

    # write the new file 
    line_num = 0
    for line in f:
        line_num += 1
        if (str(line_num) in lines_to_inline):
            new_f.write("__attribute__((always_inline)) inline " + line)
        else:
            new_f.write(line)
    f.close()
    new_f.close()

def main():
    in_lining('inlining-test.c')

if __name__ == "__main__":
    main()