# -*- coding: utf-8 -*-
# @Time    : 2022/12/4 13:47
# @Author  : LTstrange
import re

from .CONST import *


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
