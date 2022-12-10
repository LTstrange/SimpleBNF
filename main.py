from analyzer import Analyzer

if __name__ == '__main__':
    with open("files/BNF.bnf", "r") as f:
        bnf_text = f.read()

    analyzer = Analyzer(bnf_text)

    analyzer.show()

    with open("files/test.file", "r") as f:
        plain_text = f.read()

    tokens = analyzer.scanning(plain_text)
    print(tokens)

    ast = analyzer.parsing(tokens)
    print(ast)
