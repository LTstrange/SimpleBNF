# -*- coding: utf-8 -*-
# @Time    : 2022/12/5 14:42
# @Author  : LTstrange


def ebnf_2_bnf(base_ind, rhs):
    rules = [[]]
    append_ind = 0
    # when meat a bracket, find corresponding one, extract content, and add a rule with that content
    for ind, lexeme in enumerate(rhs):
        if lexeme == '(':
            rules.append([])
            append_ind += 1
        elif lexeme == ')':
            append_ind -= 1
            rules[append_ind].append(append_ind + 1 + base_ind)
        elif lexeme == '*':
            # pop out the star affect lexeme, and move them all to a new rule
            previous_lexeme = rules[append_ind].pop()
            new_rule_ind = len(rules) + base_ind
            rules.append([previous_lexeme, new_rule_ind, '|', None])
            rules[append_ind].append(new_rule_ind)
        else:
            # normal lexeme
            rules[append_ind].append(lexeme)
    
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
        self._rule_names: list[str] = []
        self.__rules: list = []

    @property
    def top_rule(self):
        return self.__top_rule

    def add_def(self, lhs: str, rhs: [str]):
        if self.__top_rule == "":
            self.__top_rule = lhs
        # self._rule_names.append(lhs)

        # FIRST: Turn EBNF to BNF
        self.parse_def(rhs)
        # SECOND: Eliminate common prefix
        

    def parse_def(self, rhs):
        rules = ebnf_2_bnf(len(self.__rules), rhs)
        self.__rules.extend(rules)
            

    def show(self):
        for ind, rule in enumerate(self.__rules):
            print(f"{ind}\t -> \t", end='')
            print(rule)

    def has_this_rule(self, rule_name: str) -> bool:
        return rule_name in self.__rules

    def __getitem__(self, rule_name: str) -> [str]:
        return self.__rules[rule_name]
