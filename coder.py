import re
import math
import random
from time import sleep

from coloring import SyntaxHighlighter


class CodePrinter:
    PRINT_SPEED = 600           # speed in characters per minute
    SPEED_VARIABILITY = 0.5     # speed variability for each character
    REPEATED_SYMBOL_SPEED = 1200
    SPEED_MULTIPLIER = 1
    SEPARATOR_SYMBOLS = ''

    @property
    def char_delay(self):
        try:
            speed_const = self.__char_speed_const
            speed_var = self.__char_speed_var
        except AttributeError:
            speed_const = self.__char_speed_const = 60 / (self.PRINT_SPEED * self.SPEED_MULTIPLIER)
            speed_var = self.__char_speed_var =  math.floor(speed_const * self.SPEED_VARIABILITY * self.SPEED_MULTIPLIER)

        if speed_var:
            return speed_const + random.randint(-speed_var, speed_var)
        else:
            return speed_const

    @property
    def repeated_char_delay(self):
        try:
            return self.__repeated_char_delay
        except AttributeError:
            self.__repeated_char_delay = 60 / (self.REPEATED_SYMBOL_SPEED * self.SPEED_MULTIPLIER)

        return self.__repeated_char_delay

    @property
    def file_path(self):
        return self.__file_path

    @file_path.setter
    def file_path(self, value):
        if value:
            try:
                with open(value, 'r') as file:
                    self.code = file.readlines()
            except:
                raise

        self.__file_path = value

    def __init__(self, file_path=None):
        self.syntax = SyntaxHighlighter()
        self.file_path = file_path

    def print(self):
        __prev_symbol = ''

        for line in self.code:
            sleep(0.05)

            line = re.sub(r'(?<=^)(\t)|(?<=\t)(\t)', r'    ', line)
            line = re.sub(r'\t', r' ', line)

            for symbol in line:
                print(symbol, end='', flush=True)

                sleep(self.char_delay if symbol != __prev_symbol else self.repeated_char_delay)

                self.syntax.highlight(symbol)
                if self.syntax.end_of_word:
                    print(self.syntax.output, end='', flush=True)