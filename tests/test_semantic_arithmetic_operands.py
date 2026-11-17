
import unittest

from tests.test_semantic_variables import analyze


PERSON_CLASS = """
class Person:
    def __init__(self): Person
    ;;
"""


def main_program(declarations, statement):
    return f"""
{PERSON_CLASS}
class main:
    def main(self):-
        {declarations};;
        {statement};;
"""


class TestSemanticArithmeticOperands(unittest.TestCase):

    def test_valid_addition(self):
        source = main_program(
            "int x",
            "x = 10 + 20"
        )
        self.assertEqual(analyze(source), [])

    def test_valid_multiplication(self):
        source = main_program(
            "int x, y",
            "x = y * 5"
        )
        self.assertEqual(analyze(source), [])

    def test_invalid_addition(self):
        source = main_program(
            "Person p; int x",
            "x = p + 5"
        )
        errors = analyze(source)

        self.assertTrue(
            any("Arithmetic operators require int" in e
                for e in errors)
        )

    def test_invalid_multiplication(self):
        source = main_program(
            "Person p; int x",
            "x = p * 2"
        )
        errors = analyze(source)

        self.assertTrue(
            any("Arithmetic operators require int" in e
                for e in errors)
        )

    def test_invalid_unary_minus(self):
        source = main_program(
            "Person p; int x",
            "x = -p"
        )
        errors = analyze(source)

        self.assertTrue(
            any("Arithmetic operators require int" in e
                for e in errors)
        )

    def test_valid_class_expression(self):
        source = main_program(
            "Person p, q",
            "p = q"
        )
        self.assertEqual(analyze(source), [])

    def test_invalid_parenthesized_expression(self):
        source = main_program(
            "Person p; int x",
            "x = (p + 5) * 2"
        )
        errors = analyze(source)

        arithmetic_errors = [
            e for e in errors
            if "Arithmetic operators require int" in e
        ]

        self.assertEqual(len(arithmetic_errors), 1)
        
    


if __name__ == "__main__":
    unittest.main()
