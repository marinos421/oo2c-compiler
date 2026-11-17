
import unittest

from tests.test_semantic_variables import analyze


class TestSemanticExpressions(unittest.TestCase):

    def test_addition(self):
        source = """
class main:
    def main(self):-
        int x;;
        x = 10 + 20;;
"""
        self.assertEqual(analyze(source), [])

    def test_multiplication_with_variable(self):
        source = """
class main:
    def main(self):-
        int x, y;;
        x = y * 2;;
"""
        self.assertEqual(analyze(source), [])

    def test_parenthesized_expression(self):
        source = """
class main:
    def main(self):-
        int x, y;;
        x = (y + 5) * 3;;
"""
        self.assertEqual(analyze(source), [])

    def test_negative_variable(self):
        source = """
class main:
    def main(self):-
        int x, y;;
        x = -y;;
"""
        self.assertEqual(analyze(source), [])

    def test_class_assigned_arithmetic_expression(self):
        source = """
class Person:
    def __init__(self): Person
    ;;

class main:
    def main(self):-
        Person p;;
        p = 10 + 20;;
"""
        errors = analyze(source)

        self.assertTrue(
            any("Type mismatch" in e for e in errors)
        )


if __name__ == "__main__":
    unittest.main()
