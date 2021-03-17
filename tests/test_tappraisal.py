import unittest
from tappraisal import TestData, QuestionRepository, TestQuestion, load_questions, AppraisalDirector, SurveyStructure, \
    build_survey_structure


def _test_data( answers):
    return TestData(None, None, answers)


class Test_TestData(unittest.TestCase):

    def test_one_valid_question(self):
        data = _test_data("A032")
        self.assertEqual(data.len_questions(), 1)

    def test_less_that_4_chars_is_no_question(self):
        data = _test_data("A03")
        self.assertEqual(data.len_questions(), 0)

    def test_ids_set(self):
        data = _test_data("A034B135")
        self.assertIn("A03", data.ids_set())
        self.assertIn("B13", data.ids_set())
        self.assertNotIn("A04", data.ids_set())


class Test_QuestionRepository(unittest.TestCase):

    def setUp(self):
        self.repo = load_questions()

    def test_get_question(self):
        question_obj = self.repo.get_question("B01")
        expected = "B01:Siento que estoy preparado para hacer el trabajo que hago ahora mismo.:P"
        self.assertEqual(expected, str(question_obj))

    def test_commit_question(self):
        question = self.repo.commit_question("A01:Considero que mi sueldo actual no afecta a mi desempeño del trabajo.:P")
        self.assertEqual("A01", question.code())
        self.assertTrue(question.is_positive())

    def test_get_category(self):
        question_obj = self.repo.get_question("B01")
        expected = "-P02. Precondiciones. Capacitación."
        self.assertEqual(expected, question_obj.category_name())



def _save_mock(data):
    pass


class Test_AppraisalDirector(unittest.TestCase):

    def setUp(self):
        self.director = AppraisalDirector(load_questions(), save_method=_save_mock)

    def test_next_question(self):
        data = _test_data("A034A015")
        question = self.director.next_question(data)
        self.assertEqual('B', question.category())

    def test_last_question(self):
        data = _test_data("A035B033C032C065D121D023E075F053G022")
        question = self.director.next_question(data)
        self.assertIsNone(question)

    def test_ever_repeat_a_question(self):
        data = _test_data("A035B033C032")
        for index in range(0, 100):
            question = self.director.next_question(data)
            self.assertNotEqual("C03", question.code())
            #print(question.code())


class Test_SurveyStructure(unittest.TestCase):

    def setUp(self):
        self.ss = build_survey_structure(survey_name = "RADAR-9")

    def test_factor_next_question(self):
        data = _test_data("A034B135")
        factor = self.ss.factor_next_question(data)
        self.assertEqual("C", factor)

    def test_factor_last_question(self):
        data = _test_data("A035B033C032C065D121D023E075F053G022")
        factor = self.ss.factor_next_question(data)
        self.assertIsNone(factor)

    def test_num_of_questions(self):
        self.assertEqual(9, self.ss.questions())



if __name__ == '__main__':
    unittest.main()
