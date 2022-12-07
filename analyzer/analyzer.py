# -*- coding: utf-8 -*-
# @Time    : 2022/12/4 13:52
# @Author  : LTstrange

from analyzer.utils import *
from .parser import BNF
from .scanner import Lexer
from .CONST import *


class Analyzer:
    """
    Build AST from plain text, and store into json file.
    """

    def __init__(self, bnf_text: str):
        self.__scanner = Lexer()
        self.__parser = BNF()

        self.set_from_text(bnf_text)

    def set_from_text(self, bnf_text: str):
        tokens = match_token_by_token(bnf_text, [regex for name, regex in REGEXES], SYMBOLS, exclude=EXCLUDE)
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

        # FIRST: separate out each part
        parts = separate_each_part(stream)
        lexer_content = parts['%lexer%']
        grammar_content = parts['%grammar%']

        # SECOND: set scanner(lexer) and parser(bnf)
        self.__scanner.set_from_text(lexer_content, grammar_content)

        self.__parser.set_from_text(grammar_content, self.__scanner.terminals)

    def scanning(self, content) -> [(str, str)]:
        tokens = self.__scanner.process(content)
        return tokens

    def parsing(self, tokens):
        ast = self.__parser.process(tokens)
        return ast

    def show(self):
        print(f"{'LEXER':-^50}:")
        self.__scanner.show()
        print()
        print(f"{'BNF':-^50}:")
        self.__parser.show()


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
