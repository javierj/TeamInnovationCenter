import unittest

from view import QuestionsAnswersView, ReportView


class TestQuestionsAnswersView(unittest.TestCase):

    def test_add_one_question(self):
        qav = QuestionsAnswersView()
        qav.add("A06", "Precondiciones", "Estoy en este trabajo porque me gusta, no por el sueldo que me pagan.", 5)

        self.assertEqual(["Precondiciones"], qav.categories())
        self.assertEqual(["A06"], qav.questions_id("Precondiciones"))
        self.assertEqual("Estoy en este trabajo porque me gusta, no por el sueldo que me pagan.", qav.question_text("A06"))
        self.assertEqual([5], qav.question_answers("A06"))

    def test_add_three_questions(self):
        qav = QuestionsAnswersView()
        qav.add("A06", "Precondiciones", "Estoy en este trabajo porque me gusta, no por el sueldo que me pagan.", 5)
        qav.add("A06", "Precondiciones", "Estoy en este trabajo porque me gusta, no por el sueldo que me pagan.", 3)
        qav.add("B16", "Seguridad sicológica", "Me diento seguro para dar mis ideas.", 3)

        self.assertEqual(["Precondiciones", "Seguridad sicológica"], qav.categories())
        self.assertEqual(["A06"], qav.questions_id("Precondiciones"))
        self.assertEqual(["B16"], qav.questions_id("Seguridad sicológica"))
        self.assertEqual("Estoy en este trabajo porque me gusta, no por el sueldo que me pagan.", qav.question_text("A06"))
        self.assertEqual("Me diento seguro para dar mis ideas.", qav.question_text("B16"))
        self.assertEqual([5, 3], qav.question_answers("A06"))
        self.assertEqual([3], qav.question_answers("B16"))

    def test_has_no_anseers(self):
        qav = QuestionsAnswersView()
        self.assertFalse(qav.has_answers())


class TestReportView(unittest.TestCase):

    def test_has_answers(self):
        report = ReportView()
        self.assertFalse(report.has_answers())
        report.with_factor("factor").add_means(list(), "1.0")
        self.assertTrue(report.has_answers())



if __name__ == '__main__':
    unittest.main()
