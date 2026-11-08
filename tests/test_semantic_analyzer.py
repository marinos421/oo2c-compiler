
from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker

from oosLexer import oosLexer
from oosParser import oosParser
from symbol_collector import SymbolCollector
from semantic_analyzer import SemanticAnalyzer


def analyze(source):
    lexer = oosLexer(InputStream(source))
    tokens = CommonTokenStream(lexer)
    parser = oosParser(tokens)

    tree = parser.startRule()
    assert parser.getNumberOfSyntaxErrors() == 0

    walker = ParseTreeWalker()

    collector = SymbolCollector()
    walker.walk(collector, tree)

    analyzer = SemanticAnalyzer(collector)
    walker.walk(analyzer, tree)

    return analyzer.errors


def test_unknown_type():
    source = """
class Person:
    Car vehicle;;

    def __init__(self): Person
        self.vehicle = 1;;

class main:
    def main(self): -
        print 1;;
"""

    errors = analyze(source)

    assert any(
        "Unknown type 'Car'" in error
        for error in errors
    )


def test_valid_type():
    source = """
class Person:
    int age;;

    def __init__(self): Person
        self.age = 10;;

class main:
    def main(self): -
        print 1;;
"""

    errors = analyze(source)

    assert errors == []


if __name__ == "__main__":
    test_unknown_type()
    test_valid_type()
    print("Semantic analyzer tests passed!")
