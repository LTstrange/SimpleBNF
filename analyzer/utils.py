# -*- coding: utf-8 -*-
# @Time    : 2022/11/30 16:19
# @Author  : LTstrange
import re


def match_token_by_token(text: str, regexes: [str], letters: [str], exclude=None) -> [(int, str)]:
    if exclude is None:  # default exclude set
        exclude = [r"[\s]+"]
    tokens: [(int, str)] = []
    ind = 0
    while ind < len(text):
        content = text[ind:]  # For the remaining characters in text
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

        # SECOND: regex match
        for i, pat in enumerate(regexes):
            if out := re.match(pat, content):
                matches.append((i, out.group()))  # matched string and string's length
        reg_len = len(regexes)

        # THIRD: direct match
        for i, sym in enumerate(letters):
            if content.startswith(sym):
                matches.append((i + reg_len, sym))
        # todo: we need a panic mode to recover from Error
        assert len(matches) != 0, f"No Match!!! Rest text:\n{content[:20]}..."

        # if there has multiple match, select the longest one
        max_match_ind = -1
        max_length = 0
        for i, match in enumerate(matches):
            if (l := len(match[1])) > max_length:
                max_match_ind = i
                max_length = l

        assert max_match_ind != -1
        match = matches[max_match_ind]

        tokens.append(match)
        ind += max_length  # move ind to match next token

    return tokens
