import re
import string

from termcolor import colored
from copy import deepcopy
from collections import Counter


class SyntaxHighlighter:
    MAGENTA_WORDS = re.compile(r'(#define|#include|if|while|return|case|else)')
    BLUE_WORDS = re.compile(r'(unsigned|static|inline|bool|int|const|void|char|enum|long)')
    HEX = re.compile(r'(0x\w*|\d*)')
    START_COMMENT = re.compile(r'(/\*)$')
    END_COMMENT = re.compile(r'(\*/)$')
    SEPARATORS = re.compile(r'(?:\%|\&|\+|\-|\=|\/|\||\.|\*|\:|>|<|\!|\?|~|\^|\(|\)|;|\{|\}|\s)(\w|\s)$')

    @property
    def output(self):
        output = self.__output
        self.__end_of_word = False
        self.__output = ''
        self.__word = ''
        return output

    @property
    def __output(self):
        return self.__output_value

    @__output.setter
    def __output(self, value):
        self.__output_value = value
        self.__line_length += len(self.__output_value)

    @property
    def end_of_word(self):
        return self.__end_of_word

    def __init__(self):
        self.__comment_state = False
        self.__output_value = ''
        self.__word = ''
        self.__end_of_word = False
        self.__line_length = 0

        self.__init_colors()

    def __init_colors(self):
        """Init patterns for re.sub"""
        self.__green = r'\1'.join(colored(' ', color='green').split())
        self.__magenta = r'\1'.join(colored(' ', color='magenta').split())
        self.__blue = r'\1'.join(colored(' ', color='blue').split())

        self.__start_comment = '\x1b[2m\x1b[37m' + r'\1'
        self.__end_comment = r'\1' + '\x1b[0m'

    def highlight(self, symbol, ):
        self.__word += symbol

        self.__parse_comment()
        self.__parse()

    def __replace_text(self):
        # if self.__word.endswith('\n'):
        #     lines = Counter(self.__output)['\n']
        #     pos = self.__line_length - len(self.__word)
        #     self.__output = '\x1b[{}A\x1b[{}C{}'.format(lines, pos, self.__output)
        #     self.__line_length = 0
        # else:
        self.__output = '\x1b[{}D{}'.format(len(self.__word), self.__output)

    def __parse(self):
        if self.__comment_state:
            return
        elif re.search(self.SEPARATORS, self.__word):
            self.__end_of_word = True
            self.__output = re.sub(self.HEX, self.__green, self.__word)
            self.__output = re.sub(self.MAGENTA_WORDS, self.__magenta, self.__output)
            self.__output = re.sub(self.BLUE_WORDS, self.__blue, self.__output)
            self.__replace_text()

    def __parse_comment(self):
        if re.findall(self.START_COMMENT, self.__word):
            self.__comment_state = True
            self.__end_of_word = True
            self.__output = re.sub(self.START_COMMENT, self.__start_comment, self.__word)
            self.__replace_text()

        elif re.findall(self.END_COMMENT, self.__word):
            self.__comment_state = False
            self.__end_of_word = True
            self.__output = self.__end_comment.replace(r'\1', '')
            self.__replace_text()