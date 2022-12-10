# -*- coding: utf-8 -*-
# @Time    : 2022/12/5 14:42
# @Author  : LTstrange
from .predict_table import PredictTable
from .utils import *


class Definitions:
    def __init__(self):
        self.__top_rule = ""
        self.__rule_names: dict[str, int] = dict()
        self.__rules: list[list[list]] = []
        self.__first_set: list[set] = []
        self.__follow_set: list[set] = []

        self.__selections: list = []
        self.__select_set: list[set] = []

        self.__predict_table: PredictTable = PredictTable()

    @property
    def top_rule(self):
        return self.__top_rule

    def add_def(self, lhs: str, rhs: [str]):
        if self.__top_rule == "":
            self.__top_rule = lhs
        self.__rule_names[lhs] = len(self.__rules)

        # Turn EBNF to BNF
        rules = ebnf_2_bnf(len(self.__rules), rhs)
        self.__rules.extend(rules)

    def process_def(self):
        # Turn Un-Terminal to integer
        self.__Turn_UnTerminal2Int()

        # THIRD: Eliminate left recursion (indirect and direct)
        self.__eliminate_left_recursion()

        # FOURTH: remove redundant rule
        # Some rule's rhs contain only one Un-terminal
        # single selection, single lexeme, and is an Un-terminal
        self.__remove_redundant_rule()

        # FIFTH: reduce common prefix
        self.__reduce_common_prefix()

        # SIXTH: reduce rules
        # There will have some rules, which no other rule can access them
        # We need to reduce them.
        self.__reduce_unused_rules()

        # SEVENTH: calculate predict table
        self.__predict_table.calculate_predict_table(self.__rules)

        return self.__predict_table

    def select(self, un_terminal: int, terminal: str):
        output = self.__predict_table.select(un_terminal, terminal)
        if type(output) == int:
            output = self.__rules[un_terminal][output]
        return output
    
    def __Turn_UnTerminal2Int(self):
        rule_names = set(self.__rule_names.keys())
        for i in range(len(self.__rules)):
            rule_i = self.__rules[i]
            for s in range(len(rule_i)):
                selection = rule_i[s]
                for l in range(len(selection)):
                    lexeme = selection[l]
                    if lexeme in rule_names:
                        self.__rules[i][s][l] = self.__rule_names[lexeme]

    def __eliminate_left_recursion(self):
        # Here is some discussion, in case I forgot it in the future.
        # Q: Do we really need to store rule_i?
        # A: First, we can. Because when rule_j replace rule_i,(j < i).
        #    There has not direct recursion in rule_j, because we eliminate it before.( # FOURTH )
        #    So it will have no left.
        #    Second, If we don't store rule_i, there will have a risk of out of control. 
        #    Because we are modify an array, and read our modification at same time, It's so bug-ly.

        for i in range(len(self.__rules)):  # <-This is necessary, because we need to modify self.__rules[i] in process.
            for j in range(i):
                rule_i = self.__rules[i]  # It needs to be here, because we change rule_i in this "for j loop".
                rule_j = self.__rules[j]
                for s in range(len(rule_i)):
                    select_i = rule_i[s]  # for each selection
                    if select_i[0] == j:  # if that selection is start by rule_j, so there has an indirect recursion
                        # 1. remove that selection
                        self.__rules[i][s] = None
                        # 2. replace that rule_j lexeme by rule_j's each selection 
                        # and each one create a new selection in rule_i
                        for select_j in rule_j:
                            new_select = select_j + select_i[1:]
                            self.__rules[i].append(new_select)
                self.__rules[i] = [select for select in self.__rules[i] if select is not None]

            # FOURTH: Eliminate direct left recursion for rule_i
            rule_i = self.__rules[i]
            beta = []  # not start with rule_i
            alpha = []  # start with rule_i
            for select in rule_i:
                if select[0] == i:
                    alpha.append(select[1:])
                else:
                    beta.append(select)

            if len(alpha) == 0:  # Means there has no direct left recursion
                continue

            # There must have at least one beta selection, otherwise, the grammar has a circle
            if len(beta) == 0:
                raise "ERROR!!! Defined grammar has a circle!!!"

            new_rule_ind = len(self.__rules)
            beta = [select + [new_rule_ind] for select in beta]
            alpha = [select + [new_rule_ind] for select in alpha if select is not None]
            alpha.append([None])
            self.__rules.append(alpha)
            self.__rules[i] = beta

    def __reduce_unused_rules(self):
        accessible = {0}  # find accessible
        queue = [0]
        while len(queue) != 0:
            rule = self.__rules[queue.pop(0)]
            for selection in rule:
                un_terminals = set([lexeme for lexeme in selection if type(lexeme) == int])
                un_terminals.difference_update(accessible)
                accessible.update(un_terminals)
                queue.extend(un_terminals)
        rules = []
        for i, r in enumerate(self.__rules):  # this make sure the new rules' order is same as old one.
            if i in accessible:
                rules.append(r)
        # match the index number of rules
        accessible = sorted(list(accessible))
        for rule in rules:
            for s in range(len(rule)):
                selection = list(map(lambda x: accessible.index(x) if type(x) == int else x, rule[s]))
                rule[s] = selection  # <-this work
        k = list(self.__rule_names.keys())
        v = list(self.__rule_names.values())
        for acc in accessible:
            if acc in v:
                self.__rule_names[k[v.index(acc)]] = accessible.index(acc)

        self.__rules = rules

    def __reduce_common_prefix(self):
        rule_ind = 0
        # Process each rule, including newly added
        while rule_ind < len(self.__rules):
            # find common prefix
            self.__extract_prefix(rule_ind)
            rule_ind += 1

    def __extract_prefix(self, rule_ind):
        rule = self.__rules[rule_ind]
        # 1. find same prefix length 1
        prefixes = dict()
        for i, select in enumerate(rule):
            if select[0] not in prefixes.keys():
                prefixes[select[0]] = []
            prefixes[select[0]].append(i)

        # 2. add new rule
        for key, value in list(prefixes.items()):
            if len(value) == 1:
                del prefixes[key]
                continue
            new_rule = []
            for v in value:
                new_rule.append(rule[v][1:])

            i = 0
            # all selection has suffix
            if len([select for select in new_rule if len(select) == 0]) == 0:
                while all([select[i] == new_rule[0][i] for select in new_rule[1:]]):  # they have same prefix
                    i += 1
            else:
                new_rule = [[None] if len(select) == 0 else select for select in new_rule]

            # adjust select length of old rule and new rule
            old_rule_remain = rule[value[0]][:i + 1]
            new_rule = [select[i:] for select in new_rule]
            rule.append([*old_rule_remain, len(self.__rules)])
            self.__rules.append(new_rule)

        # 3. remove old one
        for key, value in prefixes.items():
            rule = [None if s in value else rule[s] for s in range(len(rule))]

        rule = [rule[s] for s in range(len(rule)) if rule[s] is not None]
        self.__rules[rule_ind] = rule

    def __remove_redundant_rule(self):
        for r, rule in enumerate(self.__rules):
            if rule is None:
                continue
            if len(rule) == 1 and len(rule[0]) == 1 and type(rule[0][0]) == int:
                # single selection, single lexeme, and is an Un-terminal
                need_move_ind = rule[0][0]
                need_move_rule = self.__rules[need_move_ind]

                self.__rules[need_move_ind] = [[None]]
                self.__rules[r] = need_move_rule

                self.__rules = update_index(self.__rules, need_move_ind, r)

    def show(self):
        names = list(self.__rule_names.keys())
        indexes = list(self.__rule_names.values())
        width = 10
        num_width = (len(self.__rules) - 1) // 10 + 1
        for ind, rule in enumerate(self.__rules):
            print(f"{ind:>{num_width}}:", end='')
            a = names[indexes.index(ind)] if ind in indexes else ''
            print(f"{a:{width}} ->\t\t", end='')
            for select in rule:
                for lexeme in select:
                    if type(lexeme) == int and lexeme in indexes:
                        lexeme = f"{lexeme}:{names[indexes.index(lexeme)]}"
                        # print(lexeme)
                    print(f"{str(lexeme):<{width}}", end='')
                print('|', end=' ' * (width - 1))
            print('\b' * width)
