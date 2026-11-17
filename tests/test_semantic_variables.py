
import unittest

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

    if parser.getNumberOfSyntaxErrors() != 0:
        raise AssertionError("Test input contains syntax errors")

    collector = SymbolCollector()
    walker = ParseTreeWalker()
    walker.walk(collector, tree)

    analyzer = SemanticAnalyzer(collector)
    walker.walk(analyzer, tree)

    return analyzer.errors


class TestSemanticVariables(unittest.TestCase):

    def test_declared_variable(self):
        source = """
class main:
    def main(self):-
        int x;;
        x = 10;;
"""
        self.assertEqual(analyze(source), [])

    def test_undeclared_assignment(self):
        source = """
class main:
    def main(self):-
        x = 10;;
"""
        errors = analyze(source)

        self.assertTrue(
            any("Undeclared variable 'x'" in e for e in errors)
        )

    def test_undeclared_in_expression(self):
        source = """
class main:
    def main(self):-
        int x;;
        x = y + 1;;
"""
        errors = analyze(source)

        self.assertTrue(
            any("Undeclared variable 'y'" in e for e in errors)
        )

    def test_undeclared_in_print(self):
        source = """
class main:
    def main(self):-
        print missing;;
"""
        errors = analyze(source)

        self.assertTrue(
            any("Undeclared variable 'missing'" in e for e in errors)
        )

    def test_field_visible_in_method(self):
        source = """
class main:
    int x;;
    def main(self):-
        x = 10;;
"""
        self.assertEqual(analyze(source), [])


if __name__ == "__main__":
    unittest.main()
