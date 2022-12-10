# -*- coding: utf-8 -*-
# @Time    : 2022/12/4 13:46
# @Author  : LTstrange
from .CONST import EOF
from .definitions import Definitions
from .definitions import PredictTable


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
            if n == 'STR':
                v = f"'{v[1:-1]}'"
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

    def process(self, tokens):
        token_ind = 0
        stack = []
        stack.append(EOF)
        stack.append(0)  # start rule
        while (token := tokens[token_ind])[0] != EOF:
            if stack[-1] == token[0]:
                # print(stack[-1])
                stack.pop()
                token_ind += 1
            elif stack[-1] in self._terminals:
                raise
            else:
                output = self._definitions.select(stack[-1], token[0])
                if output is None:
                    raise "error"
                elif output == 'sync':
                    raise "sync"
                else:
                    print(f"{stack[-1]}->{output}")
                    stack.pop()
                    if output != [None]:
                        stack.extend(output[::-1])

    def show(self):
        self._definitions.show()
