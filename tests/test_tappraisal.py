import unittest
from tappraisal import TestData


class Test_TestData(unittest.TestCase):

    def _test_data(self, answers):
        return TestData(None, None, answers)

    def test_one_valid_question(self):
        data = self._test_data("A032")
        self.assertEqual(data.len_questions(), 1)

    def test_less_that_4_chars_is_no_question(self):
        data = self._test_data("A03")
        self.assertEqual(data.len_questions(), 0)


if __name__ == '__main__':
    unittest.main()
