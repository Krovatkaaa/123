import unittest

from calculator import calculate, format_number


class CalculatorTests(unittest.TestCase):
    def test_supported_operations(self):
        self.assertEqual(calculate(7, "+", 5), 12)
        self.assertEqual(calculate(7, "-", 5), 2)
        self.assertEqual(calculate(7, "*", 5), 35)
        self.assertEqual(calculate(7, "/", 2), 3.5)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calculate(7, "/", 0)

    def test_unknown_operator(self):
        with self.assertRaises(ValueError):
            calculate(7, "%", 5)

    def test_number_formatting(self):
        self.assertEqual(format_number(12.0), "12")
        self.assertEqual(format_number(3.5), "3.5")
        self.assertEqual(format_number(-0.0), "0")

    def test_long_result_is_compact(self):
        self.assertEqual(format_number(1 / 3), "0.333333333333")


if __name__ == "__main__":
    unittest.main()
