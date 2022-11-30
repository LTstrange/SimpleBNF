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

        self.__set_lexer_from_text(lexer_content, grammar_content)

        self.__set_grammar_from_text(grammar_content)

    def __set_lexer_from_text(self, lexer_content: str, grammar_content: str):
        self.__lexer.set_from_text(lexer_content, grammar_content)

    def __set_grammar_from_text(self, text):
        self.__grammar.set_from_text(text)

    def lexer(self, content) -> list[tuple[str, str]]:
        tokens = self.__lexer.process(content)
        return tokens


class Lexer:
    """
    Lexer
    """

    def __init__(self):
        self._terminals: dict[str, str] = dict()

    def set_from_text(self, lexer_content: str, grammar_content: str):
        # Named Terminals
        lines = lexer_content.split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue
            ID = re.match(ID_pattern, line).group()
            body = line[line.find("=") + 1:].strip()
            self._terminals[ID] = body

        # Unnamed Terminals
        ind = 0
        while ind < len(grammar_content):
            out = re.search(r'\".*?\"', grammar_content[ind:])
            self._terminals[out.group()] = out.group()
            ind += out.end()

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

    def show_terminals(self):
        for key, value in self._terminals.items():
            print(key, end="\t->\t")
            print(value)


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
