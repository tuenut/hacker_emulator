import re

from termcolor import colored

MAGENTA_WORDS = re.compile(r'(#define|#include|if|while|return|case|else)')
BLUE_WORDS = re.compile(r'(static|inline|bool|int|const|void|char|enum)')
HEX = re.compile(r'(0x\w*|\d)')


def coloring_line(line, pattern, color):
    return re.sub(pattern, r'\1'.join(colored(' ', color=color).split()), line)

file_path = "/home/tuenut/Downloads/linux-5.1/arch/x86/boot/a20.c"
with open(file_path, 'r') as file:
    for line in file.readlines():
        line = coloring_line(line, MAGENTA_WORDS, 'magenta')
        line = coloring_line(line, BLUE_WORDS, 'blue')
        line = coloring_line(line, HEX, 'green')

        print(line)
