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


def calculate_first_set(rules: list[list[list]]) -> list[set]:
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


def calculate_follow_set(rules: list[list[list]], first_set: list[set]) -> list[set]:
    follow_set = [set() for _ in range(len(rules))]
    follow_set[0].add('EOF')

    has_newly_added = True
    while has_newly_added:
        has_newly_added = False
        for r, rule in enumerate(rules):
            for select in rule:
                for l, lexeme in enumerate(select):
                    if type(lexeme) != int:  # ignore terminal
                        continue
                    # un terminal
                    if l + 1 == len(select):  # at bottom
                        # add follow[r] in lexeme
                        if len(follow_set[r].difference(follow_set[lexeme])) != 0:
                            follow_set[lexeme].update(follow_set[r])
                            has_newly_added = True
                    elif l + 1 < len(select):  # have suffix
                        suffix_ind = l + 1
                        has_none = True
                        while has_none and suffix_ind < len(select):
                            has_none = False
                            suffix = select[l + 1]
                            if type(suffix) == int:
                                # suffix is an un-terminal
                                if None in first_set[suffix]:  # include empty
                                    # we need to see if there has newly added after a has none suffix.
                                    # because, maybe after that has something updated.
                                    has_none = True
                                exclude_none = first_set[suffix].difference([None])
                                if len(exclude_none.difference(follow_set[lexeme])) != 0:
                                    follow_set[lexeme].update(exclude_none)
                                    has_newly_added = True
                            elif type(suffix) == str:
                                # suffix is a terminal
                                if suffix not in follow_set[lexeme]:
                                    follow_set[lexeme].add(suffix)
                                    has_newly_added = True
                            suffix_ind += 1
                        if has_none and len(follow_set[r].difference(follow_set[lexeme])) != 0:
                            follow_set[lexeme].update(follow_set[r])
                            has_newly_added = True
    return follow_set


def calculate_select_set(rules, first_set, follow_set) -> (list[set], list):
    select_set: list[set] = []
    selections: list = []
    for r, rule in enumerate(rules):
        for select in rule:
            select_set.append(set())
            selections.append(select)
            first_lexeme = select[0]

            if type(first_lexeme) == str:
                select_set[-1].add(first_lexeme)
            elif type(first_lexeme) == int:
                select_set[-1].update(first_set[first_lexeme])
            elif first_lexeme is None:
                select_set[-1].update(follow_set[r])
        # check LL(1)
        if len(rule) == 1:
            continue
        same_lhs_selections = select_set[-len(rule):]
        result = same_lhs_selections[0]
        for s, select in enumerate(same_lhs_selections[1:]):
            result = result.intersection(select)
        if len(result) != 0:
            raise "Not a LL(1) grammar!!!"
    
    return select_set, selections