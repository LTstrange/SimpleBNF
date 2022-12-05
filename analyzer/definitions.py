# -*- coding: utf-8 -*-
# @Time    : 2022/12/5 14:42
# @Author  : LTstrange
import pprint


def parse_def(tokens: list[str]) -> (int, list[str]):
    ind = 0
    body = []
    body_type = 'stream'  # stream or select

    def gen_out(bt: str, b: list[str]) -> list[str]:
        if bt == 'select':
            b = tuple(b)
        return b

    while ind < len(tokens):
        token = tokens[ind]
        ind += 1
        if token == '(':
            sub_ind, sub_body = parse_def(tokens[ind:])
            ind += sub_ind
            body.append(sub_body)
        elif token == ')':
            return ind, gen_out(body_type, body)
        elif token == '|':
            if body_type == 'stream':
                body_type = 'select'
                body = [body]
            body.append([])
        else:
            if body_type == 'select':
                body[-1].append(token)
            else:
                body.append(token)
    return ind, gen_out(body_type, body)


class Definitions:
    def __init__(self):
        self.__top_rule = ""
        self.__rules: dict = dict()

    @property
    def top_rule(self):
        return self.__top_rule

    def add_def(self, lhs: str, rhs: [str]):
        if self.__top_rule == "":
            self.__top_rule = lhs

        l, rhs = parse_def(rhs)
        print(rhs)
        self.__rules[lhs] = rhs

    def show(self):
        for name, body in self.__rules.items():
            print(f"{name}\t::= \t", end='')
            print(body)

    def has_this_rule(self, rule_name: str) -> bool:
        return rule_name in self.__rules

    def __getitem__(self, rule_name: str) -> [str]:
        return self.__rules[rule_name]
