# -*- coding: utf-8 -*-
# @Time    : 2022/11/30 16:19
# @Author  : LTstrange
import re


def get_corresponding_one(text: str, target: (str, str), search_start: int) -> (int, int):
    """
    Get the corresponding bracket in <<text>>,
    Give back the first appear position and the following corresponding one's position
    :param text: The text need to search
    :param target: The target bracket, [0] for left, [1] for right
    :param search_start: Start position for search
    :return: Tuple(start, end), this "start" is the first appear one's position
    """
    l, r = target
    # find the first bracket
    start = search_start
    while text[start] != l:
        start += 1

    stack = []  # use a stack to find corresponding curly bracket
    for i in range(start, len(text)):
        if text[i] == l:
            stack.append(i)
        elif text[i] == r:
            if len(stack) == 1:
                span = stack[0], i + 1
                break
            else:
                stack.pop()
    else:
        raise Exception("could not find the corresponding one!")

    return span


def remove_comment(text: str) -> str:
    lines = text.splitlines()

    result = []
    for line in lines:
        if line.startswith("//"):
            continue
        else:
            result.append(line)

    return "\n".join(result)


def separate_parts(text: str, target: str) -> str:
    target = target.lower()

    # 1. Find "%{target}%" Position
    text_l = text.lower()
    _, search_start = re.search(rf"%{target}%", text_l).span()
    # 2. Get {target} Body
    start, end = get_corresponding_one(text, ("{", "}"), search_start)

    return text[start + 1:end - 1].strip()


def eat_token_by_token(text: str, regexes: list[str], symbols: list[str], exclude=None) -> list[str]:
    if exclude is None:
        exclude = [r"[\s]"]
    tokens: list[str] = []
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
        for pat in regexes:
            if out := re.match(pat, content):
                matches.append((out.group(), out.end()))  # matched string and string's length

        # THIRD: match symbol
        for sym in symbols:
            if content.startswith(sym):
                matches.append((sym, len(sym)))
        assert len(matches) != 0, f"No Match!!! Rest text:\n{content[:20]}..."
        max_match_ind = -1
        max_length = 0
        for i, match in enumerate(matches):
            if match[1] > max_length:
                max_match_ind = i
                max_length = match[1]

        tokens.append(matches[max_match_ind][0])
        ind += matches[max_match_ind][1]

    return tokens
