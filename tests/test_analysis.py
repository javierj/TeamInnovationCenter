import unittest
from analysis import TestsResult, RadarAnalysis, _load_answers, surveys_overview, load_test_results
from tappraisal import load_questions


class TestTestsResult(unittest.TestCase):

    def setUp(self):
        self.results = TestsResult(q_repo=load_questions()) # Evitar esta dependencia

    def test_process_one_answer(self):
        self.results.add_test_answer("2020-12-23 15:24:17.008097/01/01/A035B033C032C065D121D023E075F053G022")
        actual = str(self.results)
        expected = "[{1: 1, 2: 3, 3: 2, 4: 1, 5: 1, 6: 3, 7: 5, 8: 3, 9: 2, 'datetime': '2020-12-23 15:24:17.008097', 'project_id': '01', 'team_id': '01'}]"
        self.assertEqual(actual, expected)

    def test_process_tokens(self): # Cambiar este test para que no use un método interno
        actual = str(self.results._extract_ids("A035B033C032C065D121D023E075F053G022"))
        expected = "['A03', 'B03', 'C03', 'C06', 'D12', 'D02', 'E07', 'F05', 'G02']"
        self.assertEqual(expected, actual)

    def test_generate_view(self):
        self.results.add_test_answer("2020-12-23 15:24:17.008097/01/01/A035B033C032C065D121D023E075F053G022")
        qav = self.results.question_answers_to_view("01", "01")

        self.assertTrue(qav.has_answers())
        self.assertEqual(6, len(qav.categories()))
        #print(qav)

    def test_select_answers_in_view(self):
        self.results.add_test_answer("2020-12-23 18:08:00.482801/01/01/A035B033C032C065D121D023E075F053G022")
        self.results.add_test_answer("2021-01-23 17:08:00.482801/01/01/A055B033C032C065D121D023E075F053G022")
        qav = self.results.question_answers_to_view("01", "01", year=2020, month=1)
        self.assertFalse(qav.has_answers())
        qav = self.results.question_answers_to_view("01", "01", year='2020', month='12')

        #print("test_select_answers_in_view \n", qav)
        self.assertTrue(qav.has_answers())
        self.assertEqual(6, len(qav.categories()))
        self.assertTrue(qav.contains("A03"))
        self.assertFalse(qav.contains("A05"))
        #print(qav)

    def test_select_all_answers(self):
        self.results.add_test_answer("2020-12-23 18:08:00.482801/01/01/A035B033C032C065D121D023E075F053G022")
        self.results.add_test_answer("2021-01-23 17:08:00.482801/01/01/A055B033C032C065D121D023E075F053G022")
        qav = self.results.question_answers_to_view("01", "01") # No year or month

        #print(qav)
        self.assertTrue(qav.has_answers())
        self.assertTrue(qav.contains("A05"))
        self.assertTrue(qav.contains("A03"))
        #print(qav)

    def test_create_dataframe(self):
        self.results.add_test_answer("2020-12-23 15:24:17.008097/01/01/A035B033C032C065D121D023E075F053G022")
        self.results.add_test_answer("2020-12-23 15:24:17.008097/01/02/A035B033C032C065D121D023E075F053G022")
        self.results.add_test_answer("2021-01-23 15:24:17.008097/02/02/A035B033C032C065D121D023E075F053G022")
        df = self.results.create_dataframe()
        self.assertEqual(3, len(df))
        df = self.results.create_dataframe(project="01")
        self.assertEqual(2, len(df))
        df = self.results.create_dataframe(project="01", group="02")
        self.assertEqual(1, len(df))
        df = self.results.create_dataframe(month="12", year="2020")
        self.assertEqual(2, len(df))
        df = self.results.create_dataframe(month="12", year="2021")
        self.assertEqual(0, len(df))
        df = self.results.create_dataframe(project="01", group="02", month="12", year="2020")
        self.assertEqual(1, len(df))

    def test_return_original_answer_for_questions(self):
        self.results = load_test_results(load_questions(), "APP-IMEDEA", "T01")
        answers = self.results.question_answers_to_view("APP-IMEDEA", None)
        #print("test_return_original_answer_for_questions \n", answers)
        cat = answers.categories()[-1]
        id = answers.questions_id(cat)[-1]
        text = answers.question_text(id)
        self.assertEqual("Creo que no puedo conseguir ningún avance significativo con mi trabajo.", text)
        resuts = answers.question_answers(id)
        self.assertEqual([5, 5], resuts)


class TestRadarAnalysis(unittest.TestCase):

    def setUp(self):
        self.analisis = RadarAnalysis()
        self.results = TestsResult(q_repo=load_questions())  # Evitar esta dependencia
        self._historical_diciembre = (2020, "diciembre", 1, '1.5', '0.')

    def test_analysis(self): # Este etst es muy frágil, poner solo los valores.
        self.results.add_test_answer("2021-01-28 17:08:00.482801/01/01/A021B012C121C105D065D135E062F051G055")
        self.results.add_test_answer("2021-01-28 17:08:02.912267/01/01/A012B044C042C015D135D101E022F045G055")
        # crear el databrame directaente.
        #df = self.results.create_dataframe()
        #report = self.analisis.analyze(df, "01", "01")
        report = self.analisis.generate_report(self.results, "01", "01")

        #print(report)
        #expected = "{'Precondiciones': {'answer': [[1, 2], [2, 2]], 'mean': ['1.5', '2.0'], 'mad': ['0.5', '0.0'], 'analysis': 'La media indica que la mayoría de las repsuestas están en los valores inferiores. Recomendamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo.'}, 'Seguridad sicológica': {'answer': [[1, 1], [2, 1]], 'mean': ['1.5', '1.0'], 'mad': ['0.5', '0.0'], 'analysis': 'La media indica que la mayoría de las repsuestas están en los valores inferiores. Recomendamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo.'}, 'Dependabilidad': {'answer': [[1, 1], [1, 1]], 'mean': ['1.0', '1.0'], 'mad': ['0.0', '0.0'], 'analysis': 'La media indica que la mayoría de las repsuestas están en los valores inferiores. Recomendamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo.'}, 'Estructura y claridad': {'answer': [[2], [2]], 'mean': ['2.0'], 'mad': ['0.0'], 'analysis': 'La media indica que la mayoría de las repsuestas están en los valores inferiores. Recomendamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo.'}, 'Significado': {'answer': [[1], [1]], 'mean': ['1.0'], 'mad': ['0.0'], 'analysis': 'La media indica que la mayoría de las repsuestas están en los valores inferiores. Recomendamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo.'}, 'Impacto': {'answer': [[1], [1]], 'mean': ['1.0'], 'mad': ['0.0'], 'analysis': 'La media indica que la mayoría de las repsuestas están en los valores inferiores. Recomendamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo.'}}"

        self.assertEqual(6, len(report.factors()))
        self.assertEqual([1.5, 2.0], report.with_factor("Precondiciones").means())
        self.assertEqual([0.5, 0.0], report.with_factor("Precondiciones").mads())
        #expected = "['1.5', '2.0']"


    def test_result_has_lastest_month_and_year(self): # Este etst es muy frágil, poner solo los valores.
        self.results.add_test_answer("2020-01-01 17:08:00.482801/01/01/A021B012C121C105D065D135E062F051G055")
        self.results.add_test_answer("2021-01-28 17:08:02.912267/01/01/A012B044C042C015D135D101E022F045G055")
        # crear el databrame directaente.
        #report = self.analisis.analyze(self.results.create_dataframe(), "01", "01")
        report = self.analisis.generate_report(self.results, "01", "01")

        # expected = "{'year': 2021, 'month': 1, 'answers_num': 1}"
        self.assertEqual(2021, report.get_year())
        self.assertEqual("enero", report.get_month())
        self.assertEqual(1, report.get_answers_len())

    def test_report_info_month_year_and_answers(self):
        self.results.add_test_answer("2020-12-28 17:08:00.482801/01/01/A021B012C121C105D065D135E062F051G055")
        self.results.add_test_answer("2021-01-28 17:08:02.912267/01/01/A012B044C042C015D135D101E022F045G055")
        # crear el databrame directaente.
        #report = self.analisis.analyze(self.results.create_dataframe(), "01", "01", "2020", "12")
        report = self.analisis.generate_report(self.results, "01", "01", "2020", "12")
        #print(data)
        #expected = "{'year': 2020, 'month': 12, 'answers_num': 1}"
        self.assertEqual("2020", str(report.get_year()))
        self.assertEqual("diciembre", str(report.get_month()))
        self.assertEqual("1", str(report.get_answers_len()))

    def test_historical_data(self):
        self.results.add_test_answer("2020-12-28 17:08:00.482801/01/01/A021B012C121C105D065D135E062F051G055")
        self.results.add_test_answer("2021-01-28 17:08:02.912267/01/01/A012B044C042C015D135D101E022F045G055")
        #report = self.analisis.analyze(self.results.create_dataframe(), "01", "01", "2020", "12")
        report = self.analisis.generate_report(self.results, "01", "01", "2020", "12")
        self.assertEqual(2, report.with_factor("Precondiciones").historical_series())

        self.assertEqual(self._historical_diciembre, report.with_factor("Precondiciones").get_historical_serie(0))
        expected = (2021, "enero", 1, '2.', '0.')
        self.assertEqual(expected, report.with_factor("Precondiciones").get_historical_serie(1))

    def test_historical_data_for_my_project_only(self):
        self.results.add_test_answer("2020-12-28 17:08:00.482801/01/01/A021B012C121C105D065D135E062F051G055")
        self.results.add_test_answer("2021-01-28 17:08:02.912267/02/01/A012B044C042C015D135D101E022F045G055")
        #report = self.analisis.analyze(self.results.create_dataframe(), "01", "01", "2020", "12")
        report = self.analisis.generate_report(self.results, "01", "01", "2020", "12")
        #print(data)
        self.assertEqual(1, report.with_factor("Precondiciones").historical_series())
        self.assertEqual(self._historical_diciembre, report.with_factor("Precondiciones").get_historical_serie(0))

    def test_historical_data_until_date(self):
        self.results.add_test_answer("2020-12-28 17:08:00.482801/01/01/A021B012C121C105D065D135E062F051G055")
        self.results.add_test_answer("2021-01-28 17:08:02.912267/01/01/A012B041C042C015D135D101E022F045G055")
        #B04 is negative question

        #report = self.analisis.analyze(self.results.create_dataframe(), "01", "01", "2020", "12")
        report = self.analisis.generate_report(self.results, "01", "01", "2020", "12")
        #print(data)
        self.assertEqual(2, report.with_factor("Precondiciones").historical_series())

        self.assertEqual(self._historical_diciembre, report.with_factor("Precondiciones").get_historical_serie(0))
        expected = (2021, "enero", 1, '3.5', '0.')
        self.assertEqual(expected, report.with_factor("Precondiciones").get_historical_serie(1))

    def test_question_answers_to_view(self):
        self.results.add_test_answer("2020-12-28 17:08:00.482801/01/01/A021B012C121C105D065D135E062F051G055")
        self.results.add_test_answer("2020-12-28 17:08:00.482801/01/01/A022B012C121C105D065D135E062F051G055")
        q_a_view = self.results.question_answers_to_view("01", "01", 2020, 12)
        self.assertTrue(q_a_view.has_answers())

        q_id = q_a_view.questions_id("Precondiciones")[0]
        self.assertEqual("Pienso que mi sueldo actual es adecuado.", q_a_view.question_text(q_id) )
        self.assertEqual([1, 2], q_a_view.question_answers(q_id))


class Test_LoanSurveysOverview(unittest.TestCase):

    def test_surveys_overview(self):
        s_overview = surveys_overview("01", "01", filename="tests/data_test.txt")
        #print(s_overview)
        expected = "{2020: {12: {'RADAR-9': {'inc': 1}}}, 2021: {1: {'RADAR-9': {'inc': 3}}, 2: {'RADAR-9': {'inc': 2}}}}"
        self.assertEqual(expected, str(s_overview))
        # Esto fallará cuando cambie data.txt


if __name__ == '__main__':
    unittest.main()
