# -*- coding: utf-8 -*-
# @Time    : 2022/11/30 16:19
# @Author  : LTstrange
import re


def eat_token_by_token(text: str, regexes: [str], symbols: [str], exclude=None) -> [(int, str)]:
    if exclude is None:
        exclude = [r"[\s]+"]
    tokens: [(int, str)] = []
    ind = 0
    while ind < len(text):
        content = text[ind:]
        matches = []
        # FIRST: exclude
        has_exclude = False
        for exc in exclude:
            if out := re.match(exc, content):
                ind += out.end()
                has_exclude = True
                break
        if has_exclude:
            continue

        # SECOND: match regex
        for i, pat in enumerate(regexes):
            if out := re.match(pat, content):
                matches.append((i, out.group()))  # matched string and string's length
        reg_len = len(regexes)

        # THIRD: match symbol
        for i, sym in enumerate(symbols):
            if content.startswith(sym):
                matches.append((i + reg_len, sym))
        assert len(matches) != 0, f"No Match!!! Rest text:\n{content[:20]}..."
        max_match_ind = -1
        max_length = 0
        for i, match in enumerate(matches):
            if (l := len(match[1])) > max_length:
                max_match_ind = i
                max_length = l

        assert max_match_ind != -1
        match = matches[max_match_ind]

        tokens.append(match)
        ind += max_length

    return tokens
