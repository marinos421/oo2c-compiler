
import unittest
from tests.test_semantic_variables import analyze


class TestSemanticTypes(unittest.TestCase):

    def test_int_assignment(self):
        source = """
class main:
    def main(self):-
        int x;;
        x = 10;;
"""
        self.assertEqual(analyze(source), [])

    def test_int_to_int(self):
        source = """
class main:
    def main(self):-
        int x, y;;
        x = y;;
"""
        self.assertEqual(analyze(source), [])

    def test_class_variable_assigned_integer(self):
        source = """
class Person:
    def __init__(self): Person
    ;;

class main:
    def main(self):-
        Person p;;
        p = 10;;
"""
        errors = analyze(source)

        self.assertTrue(
            any("Type mismatch" in e for e in errors)
        )

    
    def test_class_variable_assigned_int_variable(self):
        source = """
class Person:
    def __init__(self): Person
    ;;

class main:
    def main(self):-
        Person p; int x;;
        p = x;;
"""
        errors = analyze(source)

        self.assertTrue(
            any("Type mismatch" in e for e in errors)
        )


    def test_same_class_assignment(self):
        source = """
class Person:
    def __init__(self): Person
    ;;

class main:
    def main(self):-
        Person p, q;;
        p = q;;
"""
        self.assertEqual(analyze(source), [])


if __name__ == "__main__":
    unittest.main()
