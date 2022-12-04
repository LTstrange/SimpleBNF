# -*- coding: utf-8 -*-
# @Time    : 2022/12/4 13:46
# @Author  : LTstrange
import re

from .CONST import *


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

    def process(self, tokens):
        ast = dict()
        a = self._definitions.items()
        print(a)
