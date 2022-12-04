# -*- coding: utf-8 -*-
# @Time    : 2022/12/4 13:47
# @Author  : LTstrange

from .CONST import *
from utils import *


class Lexer:
    """
    Lexer
    """

    def __init__(self):
        self._regexes: [(str, str)] = []
        self._symbols: [str] = []

    def set_from_text(self, lexer_content: [(str, str)], grammar_content: [(str, str)]):
        # Named Terminals
        ind = 0
        while ind < len(lexer_content):
            name, value = lexer_content[ind]
            if name == 'ID' and lexer_content[ind + 1][0] == '=' and \
                    lexer_content[ind + 2][0] in ["REGEX_DEF", 'STR']:
                lhs = value
                rhs = lexer_content[ind + 2][1]
                if lexer_content[ind + 2][0] == "REGEX_DEF":
                    self._regexes.append((lhs, rhs[2:-1]))
                elif lexer_content[ind + 2][0] == "STR":
                    self._symbols.append((lhs, rhs[1:-1]))
            ind += 1

        # Unnamed Terminals
        for name, value in grammar_content:
            if name == 'STR':
                value = value[1:-1]
                self._symbols.append((value, value))
            ind += 1

        # self.show()

    def process(self, content: str) -> list[tuple[str, str]]:
        # for each char
        ind = 0
        tokens = []
        while ind < len(content):
            # check which pattern it match
            matches = []
            for key, value in self._terminals.items():
                if value.startswith("r"):
                    # regex match
                    if out := re.match(value[1:].strip('"'), content[ind:]):  # matched
                        matches.append((key, out.group(), ind + out.end()))
                else:
                    # direct match
                    value = value.strip('"')
                    if content[ind:].startswith(value):
                        matches.append((key, value, ind + len(value)))
            if len(matches) == 1:
                match = matches[0]
                tokens.append(match[:-1])
                ind = match[-1]
            else:
                raise Exception(f"Lexer Match Error!!!\nmatches : {matches}\nresume:\n\"{content[ind:]}\"")

        return tokens

    def show(self):
        print("REGEXES:")
        for key, value in self._regexes:
            print(end='\t')
            print(key, end="\t->\t")
            print(value)
        print("SYMBOLS:")
        for key, value in self._symbols:
            print(end='\t')
            print(key, end="\t->\t")
            print(value)
