# -*- coding: utf-8 -*-
# @Time    : 2022/12/4 13:49
# @Author  : LTstrange

"""
THIS is the lexer for BNF
"""
ID_pattern = r"[A-Za-z_]+"
REGEXES = [
    ('ID', r"[A-Za-z_]+"),
    # ('COMMENT', r"//.*?(?=\n)"),
    ('HEAD', r"%.*?%"),
    ('REGEX_DEF', r"r(['\"])([^\1\\]|\\.)*?\1"),
    ('STR', r"(['\"])([^\1\\]|\\.)*?\1"),
]
LEN_REGEXES = len(REGEXES)
SYMBOLS = [
    "{", "}", "=", '::=', '(', ')', '|', '*', '\n'
]

EXCLUDE = [r'[^(\S|\n)]+', r"//.*?\n"]
EOF = '<EOF>'
