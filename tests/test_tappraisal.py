import unittest
from tappraisal import TestData, QuestionRepository, TestQuestion, load_questions, AppraisalDirector, \
    get_survey_structure, SurveyStructurePsychoSafety


def _test_data( answers):
    return TestData("01", "01",answers)


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


def _save_mock(data, survey_name):
    pass


class Test_AppraisalDirector(unittest.TestCase):

    def setUp(self):
        self.director = AppraisalDirector(get_survey_structure(load_questions()), save_method=_save_mock)

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


class Test_SurveyStructureRadar9(unittest.TestCase):

    def setUp(self):
        self.ss = get_survey_structure(load_questions())

    def test_factor_next_question(self):
        data = _test_data("A034B135")
        question = self.ss.next_question(data)
        self.assertEqual("C", question.category())

    def test_factor_last_question(self):
        data = _test_data("A035B033C032C065D121D023E075F053G022")
        factor = self.ss.next_question(data)
        self.assertIsNone(factor)

    def test_num_of_questions(self):
        self.assertEqual(9, self.ss.num_of_questions())


class Test_SurveyStructurePsychoSafety(unittest.TestCase):

    def setUp(self):
        self.ss = SurveyStructurePsychoSafety(load_questions())
        self._sp01 = ["C01", "C02", "C03", "C04", "C05", "C06", "C07", "C16"]
        self._sp02 = ["C08", "C09", "C10", "C11"]

    def test_factor_first_question(self):
        data = _test_data("")
        question = self.ss.next_question(data)
        self.assertEqual("C", question.category())
        self.assertIn(question.code(), self._sp01)

    def test_factor_question_same_car(self):
        data = _test_data("C011")
        question = self.ss.next_question(data)
        self.assertIn(question.code(), self._sp01)

    def test_no_repeated_question(self):
        data = _test_data("C011")
        self.assertEqual(1, data.len_questions())
        for _ in range(0, 50):
            question = self.ss.next_question(data)
            self.assertNotEqual("C01", question.code())

    def test_question_next_car(self):
        data = _test_data("C011C022")
        question = self.ss.next_question(data)
        self.assertIn(question.code(), self._sp02)

    def test_last_question(self):
        data = _test_data("C011C022C083C134C185C036C047")
        self.assertEqual(7, data.len_questions())
        question = self.ss.next_question(data)
        self.assertIsNone(question)


if __name__ == '__main__':
    unittest.main()
