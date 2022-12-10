# -*- coding: utf-8 -*-
# @Time    : 2022/12/10 13:19
# @Author  : LTstrange


def Turn_UnTerminal2Int(rules: list[list[list]], rule_names: dict[str, int]) -> list[list[list]]:
    result = rules.copy()
    rule_name_keys = set(rule_names.keys())
    for i in range(len(rules)):
        rule_i = rules[i]
        for s in range(len(rule_i)):
            selection = rule_i[s]
            for l in range(len(selection)):
                lexeme = selection[l]
                if lexeme in rule_name_keys:
                    result[i][s][l] = rule_names[lexeme]
    return result
