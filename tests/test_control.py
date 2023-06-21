import unittest

from control import _check_error, _get_struct
from view import PollStructView


class TestStructForm(unittest.TestCase):
    def test_error(self):
        struct_view = PollStructView()
        errors = _check_error(struct_view)
        self.assertIn("questions_file", errors)  # add assertion here
        #self.assertIn("questions_in_categories", errors)  # add assertion here
        #self.assertEqual("You must use pairs \"key\": \"value\".", errors["questions_in_categories"])

    def test_error_pairs_empty(self):
        struct_view = PollStructView()
        struct_view._questions_in_categories=""
        errors = _check_error(struct_view)
        self.assertEqual("You must indicate the questions in each category.", errors["questions_in_categories"])

    def test_no_errors(self):
        struct_view = PollStructView(_get_struct("radar9"))
        errors = _check_error(struct_view)
        #print(errors)
        self.assertEqual(0, len(errors))


if __name__ == '__main__':
    unittest.main()
