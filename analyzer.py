# -*- coding: utf-8 -*-
# @Time    : 2022/11/30 15:10
# @Author  : LTstrange
import re


class Analyzer:
    """
    Build AST from plain text, and store into json file.
    """

    def __init__(self):
        self.__lexer = Lexer()

    def set_lexer_from_text(self, text: str):
        self.__lexer.set_from_text(text)


class Lexer:
    def __init__(self):
        self._terminals = dict()

    def set_from_text(self, text: str):
        lines = text.split("\n")
        lines = [line.strip() for line in lines]

        print(lines)
