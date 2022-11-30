import re
from analyzer import Analyzer
from utils import *


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


if __name__ == '__main__':
    with open("files/BNF.bnf") as f:
        plain_text = f.read()

    # print(plain_text)

    # FIRST: remove comment
    plain_text = remove_comment(plain_text)
    # print(plain_text)

    # SECOND: separate out lexer part
    lexer_content = separate_parts(plain_text, "lexer")
    # print(lexer_content)

    # THIRD: separate out grammar part
    grammar_content = separate_parts(plain_text, "grammar")
    # print(grammar_content)

    analyzer = Analyzer()

    analyzer.set_lexer_from_text(lexer_content)
