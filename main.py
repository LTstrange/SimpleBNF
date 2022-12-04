from analyzer import Analyzer

if __name__ == '__main__':
    with open("files/BNF.bnf", "r") as f:
        plain_text = f.read()

    analyzer = Analyzer(plain_text)

    with open("files/test.file", "r") as f:
        content = f.read()

    tokens = analyzer.scanning(content)
    print(tokens := [token for token in tokens if token[0] != 'space'])

    # todo: grammar analyze
    analyzer.parsing(tokens)
