# -*- coding: utf-8 -*-
# @Time    : 2022/12/10 13:19
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
                bnf_rules[-1].append(selection)
                selection = []
            else:
                selection.append(lexeme)
        bnf_rules[-1].append(selection)
    return bnf_rules


def update_index(rules, from_ind: int, to_ind: int) -> list[list[list]]:
    for rule in rules:
        if rule is None:
            continue
        for select in rule:
            for l, lexeme in enumerate(select):
                if lexeme == from_ind:
                    select[l] = to_ind
    return rules
