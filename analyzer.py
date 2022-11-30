# -*- coding: utf-8 -*-
# @Time    : 2022/11/30 15:10
# @Author  : LTstrange

from utils import *

ID_pattern = r"[A-Za-z_]+"


class Analyzer:
    """
    Build AST from plain text, and store into json file.
    """

    def __init__(self, bnf_text: str):
        self.__lexer = Lexer()
        self.__grammar = BNF()

        self.set_from_text(bnf_text)

    def set_from_text(self, text: str):
        # FIRST: remove comment
        plain_text = remove_comment(text)

        # SECOND: separate out lexer part
        lexer_content = separate_parts(plain_text, "lexer")

        # THIRD: separate out grammar part
        grammar_content = separate_parts(plain_text, "grammar")

        self.set_lexer_from_text(lexer_content)

        self.set_grammar_from_text(grammar_content)

    def set_lexer_from_text(self, text: str):
        self.__lexer.set_from_text(text)

    def set_grammar_from_text(self, text):
        self.__grammar.set_from_text(text)


class Lexer:
    """
    Lexer
    """

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
    """
    Grammar
    """

    def __init__(self):
        self._definitions = dict()

    def set_from_text(self, text: str):
        # FIRST: get each definition
        # merge multi line def into one line

        lines = [line.strip() for line in text.split("\n") if line.strip()]
        ID = ""
        for line in lines:
            result = re.match(ID_pattern, line)
            if result:
                # means this is a new definition
                ID = result.group()
                line = line[result.span()[1]:].lstrip()
                if not line.startswith("::="):
                    raise Exception("BNF grammar Error!!!: Missing \"::=\"")

                body = line.lstrip("::=")
                self._definitions[ID] = body.strip()
            else:
                # means this line need to attach to previous def
                self._definitions[ID] += " " + line.strip()

        # self.show_definitions()

    def show_definitions(self):
        for key, value in self._definitions.items():
            print(key, end="\t->\t")
            print(value)
