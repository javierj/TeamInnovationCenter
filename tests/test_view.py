import unittest

from analysis import surveys_from_poll
from tappraisal import TestQuestion
from view import QuestionsAnswersView, ReportView, HierarchicalGroups


class TestQuestionsAnswersView(unittest.TestCase):

    def test_add_one_question(self):
        qav = QuestionsAnswersView()
        question = TestQuestion("Estoy en este trabajo porque me gusta, no por el sueldo que me pagan.", "A06", "P")
        qav.add(question, "Precondiciones", 5)

        self.assertEqual(["Precondiciones"], qav.categories())
        self.assertEqual(["A06"], qav.questions_id("Precondiciones"))
        self.assertEqual("Estoy en este trabajo porque me gusta, no por el sueldo que me pagan.", qav.question_text("A06"))
        self.assertEqual([5], qav.question_answers("A06"))

    def test_add_three_questions(self):
        qav = QuestionsAnswersView()
        qav.add(TestQuestion("Estoy en este trabajo porque me gusta, no por el sueldo que me pagan.", "A06", "P"), "Precondiciones", 5)
        qav.add(TestQuestion("Estoy en este trabajo porque me gusta, no por el sueldo que me pagan.", "A06", "P"), "Precondiciones", 3)
        qav.add(TestQuestion("Me diento seguro para dar mis ideas.", "B16", "P"), "Seguridad sicológica", 3)

        self.assertEqual(["Precondiciones", "Seguridad sicológica"], qav.categories())
        self.assertEqual(["A06"], qav.questions_id("Precondiciones"))
        self.assertEqual(["B16"], qav.questions_id("Seguridad sicológica"))
        self.assertEqual("Estoy en este trabajo porque me gusta, no por el sueldo que me pagan.", qav.question_text("A06"))
        self.assertEqual("Me diento seguro para dar mis ideas.", qav.question_text("B16"))
        self.assertEqual([5, 3], qav.question_answers("A06"))
        self.assertEqual([3], qav.question_answers("B16"))

    def test_has_no_answers(self):
        qav = QuestionsAnswersView()
        self.assertFalse(qav.has_answers())


class TestReportView(unittest.TestCase):

    def test_has_answers(self):
        report = ReportView()
        self.assertFalse(report.has_answers())
        report.with_factor("factor").add_means(list(), "1.0")
        self.assertTrue(report.has_answers())


class TestHierarchicalGroups(unittest.TestCase):

    def setUp(self):
        self._root = HierarchicalGroups()

    def test_root_level(self):
        self._root.begin().add_group('2021')
        result = self._root.begin().keys()
        self.assertEqual(['2021'], result)

    def test_several_groups(self):
        self._root.begin().add_group('2021')
        self._root.begin().group('2021').add_group('1')
        self._root.begin().group('2021').group('1').add_group('RADAR-9')
        result = self._root.begin().group('2021').group('1').keys()
        self.assertEqual(['RADAR-9'], result)

    def test_add_several_groups(self):
        self._root.begin().add_group('2021').add_group('1').add_group('RADAR-9')
        result = self._root.begin().group('2021').group('1').keys()
        self.assertEqual(['RADAR-9'], result)

    def test_empty(self):
        result = self._root.begin().keys()
        self.assertEqual([], result)

    def test_repeat_groups(self):
        self._root.begin().add_group('2021')
        self._root.begin().group('2021').add_group('1')
        self._root.begin().group('2021').group('1').add_group('RADAR-9')

        self._root.begin().add_group('2021')
        result = self._root.begin().group('2021').group('1').keys()
        self.assertEqual(['RADAR-9'], result)

    def test_several_values(self):
        self._root.begin().add_group('2021').add_group('1')
        #self._root.begin().group('2021').add_group('1')
        self._root.begin().group('2021').add_group('2')
        self._root.begin().group('2021').add_group('3')
        result = self._root.begin().group('2021').keys()
        self.assertEqual(['1', '2', '3'], result)

    def test_counter(self):
        self._root.begin().add_group('2021')
        self._root.begin().group('2021').add_group('1')
        self._root.begin().group('2021').group('1').add_group('RADAR-9')
        self._root.begin().group('2021').group('1').group('RADAR-9').inc_counter()
        self._root.begin().group('2021').group('1').group('RADAR-9').inc_counter()
        self._root.begin().group('2021').group('1').group('RADAR-9').inc_counter()
        self.assertEqual(3, self._root.begin().group('2021').group('1').group('RADAR-9').counter())


    def test_counter_2(self): # Useless test
        s_overview = surveys_from_poll("SoftIA", filename="tests/data_test.txt")
        #print(s_overview)
        #self.assertEqual(3, s_overview.begin().group('2023').counter())
        years = len(s_overview.begin().keys())
        #print(s_overview.begin().keys())
        self.assertEqual(1, years)
        months = len(s_overview.begin().group(2023).keys())
        self.assertEqual(2, months)


if __name__ == '__main__':
    unittest.main()
