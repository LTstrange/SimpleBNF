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
        if text[i] == "{":
            stack.append(i)
        elif text[i] == "}":
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
