# -*- coding: utf-8 -*-
# @Time    : 2022/12/4 13:52
# @Author  : LTstrange

from utils import *
from .parser import BNF
from .scanner import Lexer
from .CONST import *

import pprint


class Analyzer:
    """
    Build AST from plain text, and store into json file.
    """

    def __init__(self, bnf_text: str):
        self.__lexer = Lexer()
        self.__parser = BNF()

        self.set_from_text(bnf_text)

    def set_from_text(self, text: str):
        tokens = eat_token_by_token(text, [regex for name, regex in REGEXES], SYMBOLS, exclude=EXCLUDE)
        stream = []
        for i, t in tokens:
            if i < LEN_REGEXES:
                name = REGEXES[i][0]
                value = t
            else:
                i -= LEN_REGEXES
                name = SYMBOLS[i]
                value = t
            stream.append((name, value))

        # FIRST: remove comment
        stream = [token for token in stream if token[0] != 'COMMENT']
        # print(stream)
        # exit()

        # SECOND: separate out each part
        parts = separate_each_part(stream)
        lexer_content = parts['%lexer%']
        grammar_content = parts['%grammar%']

        self.__lexer.set_from_text(lexer_content, grammar_content)

        self.__parser.set_from_text(grammar_content)

    def scanning(self, content) -> list[tuple[str, str]]:
        tokens = self.__lexer.process(content)
        return tokens

    def parsing(self, tokens):
        self.__parser.show_definitions()
        self.__parser.process(tokens)


def separate_each_part(tokens: [(str, str)]) -> dict[str, list]:
    parts = dict()
    previous_part = ""
    stack = 0
    for name, value in tokens:
        if previous_part != "":
            parts[previous_part].append((name, value))
            if name == '{':
                stack += 1
            elif name == '}':
                stack -= 1
                if stack == 0:  # means this part is end.
                    previous_part = ""
        elif name == "HEAD":
            previous_part = value
            parts[value] = []
            continue
    return parts
