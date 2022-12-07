# -*- coding: utf-8 -*-
# @Time    : 2022/12/4 13:46
# @Author  : LTstrange

from .definitions import Definitions


class BNF:
    """
    Grammar
    """

    def __init__(self):
        self._definitions = Definitions()
        self._terminals: [str] = []

    def set_from_text(self, grammar_content: [(str, str)], terminals: [str]):
        self._terminals = terminals

        # FIRST: merge multi line definition
        rules = [[]]
        for n, v in grammar_content:
            if v == '::=':
                lhs = rules[-1].pop()
                rules.append([lhs])
            if n not in ['\n', '{', '}']:
                rules[-1].append(v)
        for rule in rules[1:]:
            lhs = rule[0]
            rhs = rule[2:]
            self._definitions.add_def(lhs, rhs)

        self._definitions.process_def()

    def show(self):
        self._definitions.show()
