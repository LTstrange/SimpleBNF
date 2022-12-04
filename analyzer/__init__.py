# -*- coding: utf-8 -*-
# @Time    : 2022/11/30 15:10
# @Author  : LTstrange

from utils import *
from parser import BNF
from scanner import Lexer


class Analyzer:
    """
    Build AST from plain text, and store into json file.
    """

    def __init__(self, bnf_text: str):
        self.__lexer = Lexer()
        self.__parser = BNF()

        self.set_from_text(bnf_text)

    def set_from_text(self, text: str):
        # FIRST: remove comment
        plain_text = remove_comment(text)

        # SECOND: separate out lexer part
        lexer_content = separate_parts(plain_text, "lexer")

        # THIRD: separate out grammar part
        grammar_content = separate_parts(plain_text, "grammar")

        self.__set_lexer_from_text(lexer_content, grammar_content)

        self.__set_grammar_from_text(grammar_content)

    def __set_lexer_from_text(self, lexer_content: str, grammar_content: str):
        self.__lexer.set_from_text(lexer_content, grammar_content)

    def __set_grammar_from_text(self, text):
        self.__parser.set_from_text(text)

    def scanning(self, content) -> list[tuple[str, str]]:
        tokens = self.__lexer.process(content)
        return tokens

    def parsing(self, tokens):
        self.__parser.show_definitions()
        self.__parser.process(tokens)
