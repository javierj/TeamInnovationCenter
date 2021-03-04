import unittest
from tappraisal import TestData, QuestionRepository, TestQuestion, load_questions, AppraisalDirector


class Test_TestData(unittest.TestCase):

    def _test_data(self, answers):
        return TestData(None, None, answers)

    def test_one_valid_question(self):
        data = self._test_data("A032")
        self.assertEqual(data.len_questions(), 1)

    def test_less_that_4_chars_is_no_question(self):
        data = self._test_data("A03")
        self.assertEqual(data.len_questions(), 0)

    def test_ids_set(self):
        data = self._test_data("A034B135")
        self.assertIn("A03", data.ids_set())
        self.assertIn("B13", data.ids_set())
        self.assertNotIn("A04", data.ids_set())


class Test_QuestionRepository(unittest.TestCase):

    def test_get_question(self):
        repo = load_questions()
        question_obj = repo.get_question("B01")
        expected = "B01:Siento que estoy preparado para hacer el trabajo que hago ahora mismo.:P"
        self.assertEqual(expected, str(question_obj))


class Test_AppraisalDirector(unittest.TestCase):

    def test_next_question(self):
        director = AppraisalDirector(load_questions())
        data = TestData(None, None, "A034A015")
        question = director.next_question(data)
        self.assertEqual('B', question.category())


if __name__ == '__main__':
    unittest.main()
