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
        # self._definitions = dict()
        self._definitions = Definitions()

    def set_from_text(self, grammar_content: [(str, str)]):
        # FIRST: get each definition
        print(grammar_content)
        rules = [[]]
        for n, v in grammar_content:
            if v == '::=':
                lhs = rules[-1].pop()
                rules.append([lhs])
            if n not in ['\n', '{', '}']:
                if n == 'STR':
                    v = v[1:-1]
                rules[-1].append(v)
        for rule in rules[1:]:
            lhs = rule[0]
            rhs = rule[2:]
            self._definitions.add_def(lhs, rhs)
        self._definitions.show()
        exit()

    def show_definitions(self):
        for key, value in self._definitions.items():
            print(key, end="\t->\t")
            print(value)

    def process(self, tokens):
        ast = dict()
        a = self._definitions.items()
        print(a)


class Definitions:
    def __init__(self):
        self.__rules: [(str, list)] = []

    def add_def(self, lhs: str, rhs: list[str]):
        self.__rules.append((lhs, rhs))

    def show(self):
        for rule in self.__rules:
            print(f"{rule[0]}\t::= \t", end='')
            for value in rule[1]:
                print(value, end=' ')
            print()
