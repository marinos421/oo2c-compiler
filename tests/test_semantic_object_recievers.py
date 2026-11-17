
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
class main:
    def main(self):-
        int obj;;
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


if __name__ == "__main__":
    unittest.main()
