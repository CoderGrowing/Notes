#!/usr/bin/env python3

# Add space between CJK and Latin characters according to
# https://open.leancloud.cn/copywriting-style-guide.html. Mainly used for
# cleanning up Markdown documents.
#
# SYNOPSIS
#   add-space-between-latin-and-cjk input_file [out_file]
#
# CAUTION
#   If output_file is not provided, input_file is changed in-place.
import os
import sys
import functools

def is_latin(c):
    return ord(c) < 256

# Some characters should not have space on either side.
def allow_space(c):
    return not c.isspace() and not (c in '，。；「」：《》『』、[]（）*_')

def add_space_at_boundry(prefix, next_char):
    if len(prefix) == 0:
        return next_char
    if is_latin(prefix[-1]) != is_latin(next_char) and \
            allow_space(next_char) and allow_space(prefix[-1]):
        return prefix + ' ' + next_char
    else:
        return prefix + next_char


BASE_DIR = "."

md_filenames = []

for root, _, files in os.walk(BASE_DIR):
    for name in files:
        if os.path.splitext(name)[1] == ".md":
            md_filenames.append(os.path.join(root, name))

for md_file in md_filenames:
    print(md_file)
    infile = open(md_file, 'r', encoding="UTF-8")
    instr = infile.read()
    infile.close()

    outstr = functools.reduce(add_space_at_boundry, instr, '')
    print("add space for" + os.path.basename(md_file) + "...")

    with open(md_file, 'w', encoding="UTF-8") as outfile:
        outfile.write(outstr)

print("done!")