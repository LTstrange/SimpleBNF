# -*- coding: utf-8 -*-
# @Time    : 2022/12/5 14:42
# @Author  : LTstrange


def ebnf_2_bnf(base_ind, rhs):
    rules = [[]]
    stack = [0]
    # when meat a bracket, find corresponding one, extract content, and add a rule with that content
    for ind, lexeme in enumerate(rhs):
        if lexeme == '(':
            # push a stack
            stack.append(len(rules))
            rules.append([])
        elif lexeme == ')':
            # pop a stack
            new_rule_ind = stack.pop()
            rules[stack[-1]].append(new_rule_ind + base_ind)
        elif lexeme == '*':
            # pop out the star affect lexeme, and move them all to a new rule
            previous_lexeme = rules[stack[-1]].pop()
            new_rule_ind = len(rules) + base_ind
            rules.append([previous_lexeme, new_rule_ind, '|', None])
            rules[stack[-1]].append(new_rule_ind)
        else:
            # normal lexeme
            rules[stack[-1]].append(lexeme)

    bnf_rules = []
    for rule in rules:
        bnf_rules.append([])
        # each rule has multiple( or one) selection
        selection = []
        for lexeme in rule:
            if lexeme == '|':
                # sealed a selection, and prepared next one
                bnf_rules[-1].append(tuple(selection))
                selection = []
            else:
                selection.append(lexeme)
        bnf_rules[-1].append(tuple(selection))
    return bnf_rules


class Definitions:
    def __init__(self):
        self.__top_rule = ""
        self.__rule_names: dict[str, int] = dict()
        self.__rules: list = []

    @property
    def top_rule(self):
        return self.__top_rule

    def add_def(self, lhs: str, rhs: [str]):
        if self.__top_rule == "":
            self.__top_rule = lhs
        self.__rule_names[lhs] = len(self.__rules)

        # FIRST: Turn EBNF to BNF
        rules = ebnf_2_bnf(len(self.__rules), rhs)
        self.__rules.extend(rules)
        # SECOND: Eliminate common prefix

    def process_def(self):
        pass

    def show(self):
        names = list(self.__rule_names.keys())
        indexes = list(self.__rule_names.values())
        for ind, rule in enumerate(self.__rules):
            print(f"{ind:<4}", end='')
            a = names[indexes.index(ind)] if ind in indexes else ''
            print(f"{a:7} ->\t\t", end='')
            for select in rule:
                for lexeme in select:
                    print(f"{str(lexeme):<8}", end='')
                print('|', end=' ' * 7)
            print('\b' * 8)

    def has_this_rule(self, rule_name: str) -> bool:
        return rule_name in self.__rule_names

    @property
    def rule_names(self):
        return tuple(self.__rule_names)
