import re
import string

from termcolor import colored
from copy import deepcopy


class SyntaxHighlighter:
    MAGENTA_WORDS = re.compile(r'(#define|#include|if|while|return|case|else)')
    BLUE_WORDS = re.compile(r'(unsigned|static|inline|bool|int|const|void|char|enum|long)')
    HEX = re.compile(r'(0x\w*|\d)')
    START_COMMENT = re.compile(r'(/\*)')
    END_COMMENT = re.compile(r'(\*/)')
    SEPARATORS = re.compile(r'(?:\%|\&|\+|\-|\=|\/|\||\.|\*|\:|>|<|\!|\?|~|\^|\(|\)|;|\{|\}|\s)$')

    @property
    def output(self):
        output = self.__output
        self.__end_of_word = False
        self.__output = ''
        self.__word = ''
        return output

    @property
    def end_of_word(self):
        return self.__end_of_word

    def __init__(self):
        self.__comment_state = False
        self.__output = ''
        self.__word = ''
        self.__end_of_word = False
        self.__line_length = 0

    def highlight(self, symbol, ):
        self.__word += symbol

        if self.__parse_comment():
            return True
        elif re.search(self.SEPARATORS, self.__word):
            self.__parse()

            self.__end_of_word = True

            if self.__output.endswith('\n'):
                self.__output = '\x1b[1A\x1b[{}C{}'.format(self.__line_length-len(self.__word), self.__output)
            else:
                self.__output = '\x1b[{}D{}'.format(len(self.__word), self.__output)
                self.__line_length += len(self.__output)

            return True

        else:
            return False

    def __parse(self):
        self.__output = re.sub(self.HEX, r'\1'.join(colored(' ', color='green').split()), self.__word)
        self.__output = re.sub(self.MAGENTA_WORDS, r'\1'.join(colored(' ', color='magenta').split()), self.__output)
        self.__output = re.sub(self.BLUE_WORDS, r'\1'.join(colored(' ', color='blue').split()), self.__output)

    def __parse_comment(self):
        if re.findall(self.START_COMMENT, self.__word):
            self.__comment_state = True
            self.__end_of_word = True
            self.__output = re.sub(self.START_COMMENT, '\x1b[2m\x1b[37m' + r'\1', self.__word)
            return True

        elif not re.findall(self.END_COMMENT, self.__word) and self.__comment_state:
            return True

        elif re.findall(self.END_COMMENT, self.__word):
            self.__comment_state = False
            self.__end_of_word = True
            self.__output = re.sub(self.END_COMMENT, r'\1' + '\x1b[0m', self.__word)
            return True

        else:
            return False