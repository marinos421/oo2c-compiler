
import unittest

from tests.test_semantic_variables import analyze


def program(method):
    return f"""
class Person:
    def __init__(self): Person
    ;;

    {method}
    ;;

class main:
    def main(self):-
    ;;
"""


class TestSemanticReturns(unittest.TestCase):

    def test_valid_integer_return(self):
        source = program("""
def calculate(self): int
    return 10
""")
        self.assertEqual(analyze(source), [])

    def test_valid_arithmetic_return(self):
        source = program("""
def calculate(self): int
    int x;;
    return x + 5
""")
        self.assertEqual(analyze(source), [])

    def test_valid_class_return(self):
        source = program("""
def getPerson(self): Person
    Person p;;
    return p
""")
        self.assertEqual(analyze(source), [])

    def test_invalid_class_returning_integer(self):
        source = program("""
def getPerson(self): Person
    return 10
""")
        errors = analyze(source)

        self.assertTrue(
            any("Return type mismatch" in e for e in errors)
        )

    def test_invalid_integer_returning_class(self):
        source = program("""
def calculate(self): int
    Person p;;
    return p
""")
        errors = analyze(source)

        self.assertTrue(
            any("Return type mismatch" in e for e in errors)
        )


if __name__ == "__main__":
    unittest.main()
