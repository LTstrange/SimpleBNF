from analyzer import Analyzer

if __name__ == '__main__':
    with open("files/BNF.bnf", "r") as f:
        plain_text = f.read()

    analyzer = Analyzer(plain_text)

    with open("files/test.file", "r") as f:
        content = f.read()
        print(content)
