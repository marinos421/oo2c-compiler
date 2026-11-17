
import unittest

from tests.test_semantic_variables import analyze


class TestSemanticObjectReceivers(unittest.TestCase):

    def test_undeclared_receiver(self):
        source = """
class main:
    def main(self):-
        missing.run();;
"""
        errors = analyze(source)

        self.assertTrue(
            any(
                "Undeclared variable 'missing'" in error
                for error in errors
            )
        )
        

    
    def test_declared_receiver(self):
        source = """
    class Person:
        def __init__(self): Person
        ;;

        def run(self): -
        ;;

    class main:
        def main(self): -
            Person obj;;
            obj.run();;
    """
        errors = analyze(source)

        self.assertEqual(errors, [])


    def test_method_name_not_treated_as_variable(self):
        source = """
class main:
    def main(self):-
        int obj;;
        obj.calculate(10);;
"""
        errors = analyze(source)

        self.assertFalse(
            any(
                "Undeclared variable 'calculate'" in error
                for error in errors
            )
        )
    
    
    def test_integer_receiver_rejected(self):
        source = """
    class main:
        def main(self):-
            int obj;;
            obj.run();;
    """
        errors = analyze(source)

        self.assertTrue(
            any(
                "Invalid method receiver" in error
                for error in errors
            )
        )
    
    
    def test_unknown_method_rejected(self):
        source = """
class Person:
    def __init__(self): Person
    ;;

    def run(self): -
    ;;

class main:
    def main(self): -
        Person obj;;
        obj.fly();;
"""
        errors = analyze(source)

        self.assertTrue(
            any(
                "Unknown method 'fly'" in error
                for error in errors
            )
        )

    
    def test_method_wrong_argument_count(self):
        source = """
class Person:
    def __init__(self): Person
    ;;

    def add(self, int x, int y): int
        return x + y
    ;;

class main:
    def main(self): -
        Person p;;
        p.add(10);;
"""
        errors = analyze(source)

        self.assertTrue(
            any(
                "Argument count mismatch" in error
                for error in errors
            )
        )

    
    def test_method_correct_argument_count(self):
        source = """
class Person:
    def __init__(self): Person
    ;;

    def add(self, int x, int y): int
        return x + y
    ;;

class main:
    def main(self): -
        Person p;;
        p.add(10, 20);;
"""
        errors = analyze(source)

        self.assertEqual(errors, [])


    def test_method_wrong_argument_type(self):
        source = """
class Person:
    def __init__(self): Person
    ;;

    def setAge(self, int age): -
    ;;

class main:
    def main(self): -
        Person p;;
        p.setAge(p);;
"""
        errors = analyze(source)

        self.assertTrue(
            any(
                "Argument type mismatch" in error
                for error in errors
            )
        )




if __name__ == "__main__":
    unittest.main()
