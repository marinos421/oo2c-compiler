from antlr4 import (
    InputStream,
    CommonTokenStream,
    ParseTreeWalker
)

from oosLexer import oosLexer
from oosParser import oosParser
from symbol_collector import SymbolCollector


def test_collect_symbols():
    source = """
class Person:
int age;;
def __init__(self, int initial): Person
self.age = initial;;

class main:
def main(self): -
print 1;;
"""

    lexer = oosLexer(InputStream(source))
    tokens = CommonTokenStream(lexer)
    parser = oosParser(tokens)

    tree = parser.startRule()

    assert parser.getNumberOfSyntaxErrors() == 0

    collector = SymbolCollector()
    walker = ParseTreeWalker()
    walker.walk(collector, tree)

    assert collector.errors == []

    global_scope = collector.table.global_scope

    assert "Person" in global_scope.symbols
    assert "main" in global_scope.symbols

    person_scope = collector.class_scopes["Person"]

    assert "age" in person_scope.symbols
    assert "__init__" in person_scope.symbols

    constructor_scope = collector.method_scopes[
        ("Person", "__init__")
    ]

    assert "self" in constructor_scope.symbols
    assert "initial" in constructor_scope.symbols

    assert constructor_scope.symbols["initial"].type_name == "int"
    
if __name__ == "__main__":
    test_collect_symbols()
    print("Symbol collector tests passed!")
