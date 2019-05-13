import re
import string

from termcolor import colored
from copy import deepcopy


class Colors:
    def __init__(self):
        self.green = r'\1'.join(colored(' ', color='green').split())
        self.magenta = r'\1'.join(colored(' ', color='magenta').split())
        self.blue = r'\1'.join(colored(' ', color='blue').split())
        self.start_comment = '\x1b[2m\x1b[37m' + r'\1'
        self.end_comment = '\x1b[0m'



class SyntaxHighlighter:
    MAGENTA_WORDS = re.compile(r'(#define|#include|if|while|return|case|else)')
    BLUE_WORDS = re.compile(r'(unsigned|static|inline|bool|int|const|void|char|enum|long)')
    HEX = re.compile(r'(?<!\w)(0x\w*|\d)(?!\w)')
    START_COMMENT = re.compile(r'(/\*)')
    END_COMMENT = re.compile(r'(\*/)')
    SEPARATORS = re.compile('(\s)$')

    @property
    def output(self):
        output = self.__output
        self.__end_of_word = False
        self.__output_value = ''
        self.__word = ''
        return output

    @property
    def end_of_word(self):
        return self.__end_of_word

    @property
    def colors(self):
        return self.__colors

    @property
    def __output(self):
        return self.__output_value

    @__output.setter
    def __output(self, value):
        self.__line += self.__word

        if self.__word.endswith('\n'):
            self.__output_value = '\x1b[1A\x1b[{}C{}'.format(len(self.__line) - len(self.__word), value)
            self.__line = ''
        else:
            self.__output_value = '\x1b[{}D{}'.format(len(self.__word), value)

    def __init__(self):
        self.__comment_state = False
        self.__end_of_word = False
        self.__output_value = ''
        self.__word = ''
        self.__line = ''
        self.__colors = Colors()

    def highlight(self, symbol, ):
        self.__word += symbol

        if self.__parse_comment():
            return
        elif re.search(self.SEPARATORS, self.__word):
            self.__parse()


    def __parse(self):
        if self.__comment_state:
            return

        __output = re.sub(self.HEX, self.colors.green, self.__word)
        __output = re.sub(self.MAGENTA_WORDS, self.colors.magenta, __output)
        __output = re.sub(self.BLUE_WORDS, self.colors.blue, __output)

        if __output != self.__word:
            self.__output = __output
        else:
            self.__output = self.__word

        self.__end_of_word = True


    def __parse_comment(self):
        if re.findall(self.START_COMMENT, self.__word):
            self.__comment_state = True
            self.__end_of_word = True
            self.__output = re.sub(self.START_COMMENT, self.colors.start_comment, self.__word)
            return True

        elif re.findall(self.END_COMMENT, self.__word):
            self.__comment_state = False
            self.__end_of_word = True
            self.__output = self.colors.end_comment
            return True

        else:
            return False
