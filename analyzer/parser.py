# -*- coding: utf-8 -*-
# @Time    : 2022/12/4 13:46
# @Author  : LTstrange


class BNF:
    """
    Grammar
    """

    def __init__(self):
        self._definitions = Definitions()
        self._terminals: [str] = []

    def set_from_text(self, grammar_content: [(str, str)], terminals: [str]):
        self._terminals = terminals

        # FIRST: get each definition
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

    def process(self, tokens, rule_ind=0):
        current_rule = self._definitions[rule_ind]
        print(current_rule)
        ind = 0
        ast = [current_rule[0], []]

        for lexeme in current_rule[1]:
            # Here has Four scenario
            # 1. match a terminal. ( Which means we need to capture it )
            # 2. match an un-terminal. ( Which means we need to get deeper )
            # 3. not match. ( This is not an Error, just because the current rule is failed )
            # 4. appear a lexeme, which not a rule and not in lexer's terminal. ( This is Error )

            if (sub_rule := self._definitions.has_this_rule(lexeme)) \
                    and sub_rule != -1:  # means this is a un-terminal rule
                if sub_ast := self.process(tokens[ind], sub_rule):
                    ast[-1].append(sub_ast)
            elif lexeme in self._terminals:  # match terminal
                if tokens[ind][0] == lexeme:  # matched
                    ast[-1].append(tokens[ind])
                else:  # not match
                    return None
            else:
                raise

        return ast

    def show(self):
        self._definitions.show()


class Definitions:
    def __init__(self):
        self.__rules: [(str, [str])] = []

    def add_def(self, lhs: str, rhs: list[str]):
        self.__rules.append((lhs, rhs))

    def show(self):
        for rule in self.__rules:
            print(f"{rule[0]}\t::= \t", end='')
            for value in rule[1]:
                print(value, end=' ')
            print('\b')

    def has_this_rule(self, rule_name: str) -> int:
        ind = -1
        for i, n in self.__rules:
            if n == rule_name:
                ind = i
        return ind

    def __getitem__(self, ind) -> (str, [str]):
        return self.__rules[ind]
