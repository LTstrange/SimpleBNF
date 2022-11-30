# -*- coding: utf-8 -*-
# @Time    : 2022/11/30 15:10
# @Author  : LTstrange

import re

ID_pattern = r"[A-Za-z_]+"


class Analyzer:
    """
    Build AST from plain text, and store into json file.
    """

    def __init__(self):
        self.__lexer = Lexer()
        self.__grammar = BNF()

    def set_lexer_from_text(self, text: str):
        self.__lexer.set_from_text(text)

    def set_grammar_from_text(self, text):
        self.__grammar.set_from_text(text)


class Lexer:
    def __init__(self):
        self._terminals = dict()

    def set_from_text(self, text: str):
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue
            ID = re.match(ID_pattern, line).group()
            body = line[line.find("=") + 1:].strip()
            self._terminals[ID] = body


class BNF:
    def __init__(self):
        ...
    
    def set_from_text(self, text):
        print(text)