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


def calculate_first_set(rules):
    first_set = [set() for _ in range(len(rules))]
    has_newly_added = True
    while has_newly_added:
        has_newly_added = False
        for r, rule in enumerate(rules):
            for select in rule:
                has_none = True
                l = 0
                while has_none and l < len(select):
                    has_none = False
                    lexeme = select[l]
                    if type(lexeme) == str and lexeme not in first_set[r]:
                        # terminal
                        first_set[r].add(lexeme)
                        has_newly_added = True
                    elif lexeme is None and lexeme not in first_set[r]:
                        has_none = True
                    elif type(lexeme) == int and \
                            len(first_set[lexeme].difference(first_set[r])) != 0:
                        # Un terminal
                        first_set[r].update(first_set[lexeme])
                        has_newly_added = True
                    l += 1
                if has_none:
                    first_set[r].add(None)
    return first_set
