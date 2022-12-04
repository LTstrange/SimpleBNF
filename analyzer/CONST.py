# -*- coding: utf-8 -*-
# @Time    : 2022/12/4 13:49
# @Author  : LTstrange

ID_pattern = r"[A-Za-z_]+"
REGEXES = [
    ('ID', r"[A-Za-z_]+"),
    ('COMMENT', r"//.*?(?=\n)"),
    ('HEAD', r"%.*?%"),
    ('REGEX_DEF', r'r".*?"'),
    ('STR', r"(['\"])([^\1\\]|\\.)*?\1"),
]
LEN_REGEXES = len(REGEXES)
SYMBOLS = [
    "{", "}", "=", '::=', '(', ')', '|', '*', '\n'
]

EXCLUDE = [r'[^(\S|\n)]']
