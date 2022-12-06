# -*- coding: utf-8 -*-
# @Time    : 2022/12/4 13:47
# @Author  : LTstrange

from analyzer.utils import *


class Lexer:
    """
    Lexer
    """

    def __init__(self):
        self._regexes: [(str, str)] = []
        self._symbols: [(str, str)] = []

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
                # value = value[1:-1]
                self._symbols.append((value[1:-1], value))
            ind += 1

    @property
    def terminals(self) -> [str]:
        terminals = []
        for sym in self._symbols:
            terminals.append(sym[0])
        for regex in self._regexes:
            terminals.append(regex[0])
        return terminals

    def process(self, content: str) -> [(str, str)]:
        regexes = [value for name, value in self._regexes]
        symbols = [name for name, value in self._symbols]
        tokens = match_token_by_token(content, regexes, symbols)
        len_reg = len(regexes)
        stream = []
        for i, token in tokens:
            if i < len_reg:
                name = self._regexes[i][0]
                if self._regexes[i][0] == 'ID':  # keyword scenario
                    if token in symbols:
                        name = token
            else:
                i -= len_reg
                name = token

            stream.append((name, token))
        return stream

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
