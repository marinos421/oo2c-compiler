
import unittest

from tests.test_semantic_variables import analyze


class TestSemanticScopes(unittest.TestCase):

    def test_field_visible_in_method(self):
        source = """
class Box:
    int value;;

    def __init__(self): Box
    ;;

    def get(self): int
        return value
    ;;

class main:
    def main(self):-
    ;;
"""
        self.assertEqual(analyze(source), [])

    def test_local_variable_not_visible_in_other_method(self):
        source = """
class Box:
    def __init__(self): Box
    ;;

    def first(self): int
        int secret;;
        secret = 10
    ;;

    def second(self): int
        return secret
    ;;

class main:
    def main(self):-
    ;;
"""
        errors = analyze(source)

        self.assertTrue(
            any(
                "Undeclared variable 'secret'" in e
                for e in errors
            )
        )

    def test_parameter_visible_in_own_method(self):
        source = """
class Box:
    def __init__(self): Box
    ;;

    def calculate(self, int number): int
        return number
    ;;

class main:
    def main(self):-
    ;;
"""
        self.assertEqual(analyze(source), [])

    def test_parameter_not_visible_in_other_method(self):
        source = """
class Box:
    def __init__(self): Box
    ;;

    def first(self, int number): int
        return number
    ;;

    def second(self): int
        return number
    ;;

class main:
    def main(self):-
    ;;
"""
        errors = analyze(source)

        self.assertTrue(
            any(
                "Undeclared variable 'number'" in e
                for e in errors
            )
        )


if __name__ == "__main__":
    unittest.main()
