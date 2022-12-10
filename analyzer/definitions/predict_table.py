# -*- coding: utf-8 -*-
# @Time    : 2022/12/10 14:21
# @Author  : LTstrange

from .utils import *


class PredictTable:
    def __init__(self):
        self.__first_set: list[set] = []
        self.__follow_set: list[set] = []
        self.__select_set: list[set] = []

        self.__selections: list = []

    def calculate_predict_table(self, rules):
        self.calculate_first_set(rules)
        self.calculate_follow_set(rules)
        self.calculate_select_set(rules)

    def select_next_rule(self, un_terminal, terminal):
        ...

    def calculate_first_set(self, rules):
        self.__first_set = [set() for _ in range(len(rules))]
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
                        if type(lexeme) == str and lexeme not in self.__first_set[r]:
                            # terminal
                            self.__first_set[r].add(lexeme)
                            has_newly_added = True
                        elif lexeme is None and lexeme not in self.__first_set[r]:
                            has_none = True
                        elif type(lexeme) == int and \
                                len(self.__first_set[lexeme].difference(self.__first_set[r])) != 0:
                            # Un terminal
                            self.__first_set[r].update(self.__first_set[lexeme])
                            has_newly_added = True
                        l += 1
                    if has_none:
                        self.__first_set[r].add(None)

    def calculate_follow_set(self, rules):
        self.__follow_set = [set() for _ in range(len(rules))]
        self.__follow_set[0].add('EOF')

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
                            if len(self.__follow_set[r].difference(self.__follow_set[lexeme])) != 0:
                                self.__follow_set[lexeme].update(self.__follow_set[r])
                                has_newly_added = True
                        elif l + 1 < len(select):  # have suffix
                            suffix_ind = l + 1
                            has_none = True
                            while has_none and suffix_ind < len(select):
                                has_none = False
                                suffix = select[l + 1]
                                if type(suffix) == int:
                                    # suffix is an un-terminal
                                    if None in self.__first_set[suffix]:  # include empty
                                        # we need to see if there has newly added after a has none suffix.
                                        # because, maybe after that has something updated.
                                        has_none = True
                                    exclude_none = self.__first_set[suffix].difference([None])
                                    if len(exclude_none.difference(self.__follow_set[lexeme])) != 0:
                                        self.__follow_set[lexeme].update(exclude_none)
                                        has_newly_added = True
                                elif type(suffix) == str:
                                    # suffix is a terminal
                                    if suffix not in self.__follow_set[lexeme]:
                                        self.__follow_set[lexeme].add(suffix)
                                        has_newly_added = True
                                suffix_ind += 1
                            if has_none and len(self.__follow_set[r].difference(self.__follow_set[lexeme])) != 0:
                                self.__follow_set[lexeme].update(self.__follow_set[r])
                                has_newly_added = True

    def calculate_select_set(self, rules):
        for r, rule in enumerate(rules):
            for select in rule:
                self.__select_set.append(set())
                self.__selections.append(select)
                first_lexeme = select[0]

                if type(first_lexeme) == str:
                    self.__select_set[-1].add(first_lexeme)
                elif type(first_lexeme) == int:
                    self.__select_set[-1].update(self.__first_set[first_lexeme])
                elif first_lexeme is None:
                    self.__select_set[-1].update(self.__follow_set[r])
            # check LL(1)
            if len(rule) == 1:
                continue
            same_lhs_selections = self.__select_set[-len(rule):]
            result = same_lhs_selections[0]
            for s, select in enumerate(same_lhs_selections[1:]):
                result = result.intersection(select)
            if len(result) != 0:
                raise "Not a LL(1) grammar!!!"
