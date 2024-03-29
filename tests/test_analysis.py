import unittest
from analysis import TestsResult, RadarAnalysis, surveys_overview, load_test_results, \
    HistoricDataAnalysis, RawAnswer, generate_report, Survey, AnsweredQuestion, CVSResults, surveys_from_poll
from control import _get_struct
from tappraisal import get_survey_structure, QuestionRepository, TestQuestion
from utilities import _get_full_filename


def load_questions(file_name="preguntas.txt"):
    repo = QuestionRepository()

    # Cambiado para softIA
    file_name = _get_full_filename(file_name)
    file = open(file_name, encoding="utf-8") # No: encoding="latin-1" encoding="ascii"
    for line in file:
        repo.commit_question(line)
        #print("áéÍÓñÑ: " + line)
    file.close()

    return repo

def _load_softIA_struct():
    survey_structure = get_survey_structure(load_questions("preguntas_sofia.txt"), survey_name="softia")
    return survey_structure


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

    def test_select_all_answers(self):
        self.results.add_test_answer("2020-12-23 18:08:00.482801/01/01/A035B033C032C065D121D023E075F053G022")
        self.results.add_test_answer("2021-01-23 17:08:00.482801/01/01/A055B033C032C065D121D023E075F053G022")
        qav = self.results.question_answers_to_view("01", "01") # No year or month

        #print(qav)
        self.assertTrue(qav.has_answers())
        self.assertTrue(qav.contains("A05"))
        self.assertTrue(qav.contains("A03"))

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

    def test_result_safety_test(self):
        questions = load_questions()
        test_struct = get_survey_structure(questions, "SAFETY")
        results = TestsResult(q_repo=questions, questions_number=test_struct.num_of_questions())
        results.add_test_answer("2021-03-19 18:42:14.254246/01/01/C055C075C105C145C195C205C185/SAFETY")
        results.add_test_answer("2021-03-19 18:58:31.121013/01/01/C055C065C095C135C195C085C125/SAFETY")

        self.assertEqual(2, len(results.get_surveys()))

    def test_take_num_questions_from_struct(self):
        self.assertEqual(9, self.results.t_answers_number())
        self.results = TestsResult(q_repo=load_questions())
        self.repo = load_questions("preguntas_sofia.txt")
        survey_structure = _load_softIA_struct()
        self.results = TestsResult(q_repo=self.repo, _survey_struct=survey_structure)
        self.assertEqual(survey_structure.num_of_questions(), self.results.t_answers_number())


class TestRadarAnalysis(unittest.TestCase):

    def _get_historical_data(self):
        d_a = HistoricDataAnalysis()
        return d_a.historical_data(self.results, get_survey_structure(self.repo))

    def setUp(self):
        self.repo = load_questions()
        self.analisis = RadarAnalysis(get_survey_structure(self.repo))
        #self.analisis = RadarAnalysis()
        self.results = TestsResult(q_repo=self.repo)  # Evitar esta dependencia
        self._historical_diciembre = (2020, "diciembre", 1, 1.5, 0.0)

    def test_analysis(self): # Este etst es muy frágil, poner solo los valores.
        self.results.add_test_answer("2021-01-28 17:08:00.482801/01/01/A021B012C121C105D065D135E062F051G055")
        self.results.add_test_answer("2021-01-28 17:08:02.912267/01/01/A012B044C042C015D135D101E022F045G055")

        report = self.analisis.generate_report(self.results, "01", "01", 2021, 1)
        #print(report)
        #expected = "{'Precondiciones': {'answer': [[1, 2], [2, 2]], 'mean': ['1.5', '2.0'], 'mad': ['0.5', '0.0'], 'analysis': 'La media indica que la mayoría de las repsuestas están en los valores inferiores. Recomendamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo.'}, 'Seguridad sicológica': {'answer': [[1, 1], [2, 1]], 'mean': ['1.5', '1.0'], 'mad': ['0.5', '0.0'], 'analysis': 'La media indica que la mayoría de las repsuestas están en los valores inferiores. Recomendamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo.'}, 'Dependabilidad': {'answer': [[1, 1], [1, 1]], 'mean': ['1.0', '1.0'], 'mad': ['0.0', '0.0'], 'analysis': 'La media indica que la mayoría de las repsuestas están en los valores inferiores. Recomendamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo.'}, 'Estructura y claridad': {'answer': [[2], [2]], 'mean': ['2.0'], 'mad': ['0.0'], 'analysis': 'La media indica que la mayoría de las repsuestas están en los valores inferiores. Recomendamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo.'}, 'Significado': {'answer': [[1], [1]], 'mean': ['1.0'], 'mad': ['0.0'], 'analysis': 'La media indica que la mayoría de las repsuestas están en los valores inferiores. Recomendamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo.'}, 'Impacto': {'answer': [[1], [1]], 'mean': ['1.0'], 'mad': ['0.0'], 'analysis': 'La media indica que la mayoría de las repsuestas están en los valores inferiores. Recomendamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo.'}}"
        self.assertEqual(6, len(report.factors()))
        # Ya no da medias por pregunta
        #self.assertEqual([1.5, 2.0], report.with_factor("Precondiciones").means())
        self.assertEqual([1.75], report.with_factor("Precondiciones").means())
        #self.assertEqual([0.5, 0.0], report.with_factor("Precondiciones").mads())
        self.assertEqual([0.25], report.with_factor("Precondiciones").mads())

    def test_analysis_2(self):
        #self.analisis = RadarAnalysis(get_survey_structure(load_questions()))
        self.results.add_test_answer("2021-01-28 17:08:00.482801/01/01/A021B012C121C105D065D135E062F051G055")
        self.results.add_test_answer("2021-01-28 17:08:02.912267/01/01/A012B044C042C015D135D101E022F045G055")
        report = self.analisis.generate_report(self.results, "01", "01", 2021, 1)

        # print(report)
        # expected = "{'Precondiciones': {'answer': [[1, 2], [2, 2]], 'mean': ['1.5', '2.0'], 'mad': ['0.5', '0.0'], 'analysis': 'La media indica que la mayoría de las repsuestas están en los valores inferiores. Recomendamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo.'}, 'Seguridad sicológica': {'answer': [[1, 1], [2, 1]], 'mean': ['1.5', '1.0'], 'mad': ['0.5', '0.0'], 'analysis': 'La media indica que la mayoría de las repsuestas están en los valores inferiores. Recomendamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo.'}, 'Dependabilidad': {'answer': [[1, 1], [1, 1]], 'mean': ['1.0', '1.0'], 'mad': ['0.0', '0.0'], 'analysis': 'La media indica que la mayoría de las repsuestas están en los valores inferiores. Recomendamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo.'}, 'Estructura y claridad': {'answer': [[2], [2]], 'mean': ['2.0'], 'mad': ['0.0'], 'analysis': 'La media indica que la mayoría de las repsuestas están en los valores inferiores. Recomendamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo.'}, 'Significado': {'answer': [[1], [1]], 'mean': ['1.0'], 'mad': ['0.0'], 'analysis': 'La media indica que la mayoría de las repsuestas están en los valores inferiores. Recomendamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo.'}, 'Impacto': {'answer': [[1], [1]], 'mean': ['1.0'], 'mad': ['0.0'], 'analysis': 'La media indica que la mayoría de las repsuestas están en los valores inferiores. Recomendamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo.'}}"
        self.assertEqual(6, len(report.factors()))
        self.assertEqual([1.75], report.with_factor("Precondiciones").means())
        self.assertEqual([0.25], report.with_factor("Precondiciones").mads())

    def test_report_info_month_year_and_answers(self):
        self.results.add_test_answer("2020-12-28 17:08:00.482801/01/01/A021B012C121C105D065D135E062F051G055")
        self.results.add_test_answer("2021-01-28 17:08:02.912267/01/01/A012B044C042C015D135D101E022F045G055")
        #report = self.analisis.analyze(self.results.create_dataframe(), "01", "01", "2020", "12")
        report = self.analisis.generate_report(self.results, "01", "01", "2020", "12")
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
        expected = (2021, "enero", 1, 2.0, 0.0)
        self.assertEqual(expected, report.with_factor("Precondiciones").get_historical_serie(1))

    def test_historical_data_2(self):
        self.analisis = RadarAnalysis(get_survey_structure(self.repo))
        self.results.add_test_answer("2020-12-28 17:08:00.482801/01/01/A021B012C121C105D065D135E062F051G055")
        self.results.add_test_answer("2021-01-28 17:08:02.912267/01/01/A012B044C042C015D135D101E022F045G055")
        #report = self.analisis.analyze(self.results.create_dataframe(), "01", "01", "2020", "12")
        report = self.analisis.generate_report(self.results, "01", "01", 2020, 12)

        self.assertEqual(2, report.with_factor("Precondiciones").historical_series())
        self.assertEqual((2020, "diciembre", 1, 1.5, 0.0), report.with_factor("Precondiciones").get_historical_serie(0))
        expected = (2021, "enero", 1, 2.0, 0.0)
        self.assertEqual(expected, report.with_factor("Precondiciones").get_historical_serie(1))

    def test_historical_data_uses_all_data(self):
        self.results.add_test_answer("2020-12-28 17:08:00.482801/01/01/A021B012C121C105D065D135E062F051G055")
        self.results.add_test_answer("2021-01-28 17:08:02.912267/02/01/A012B044C042C015D135D101E022F045G055")
        #report = self.analisis.analyze(self.results.create_dataframe(), "01", "01", "2020", "12")
        report = self.analisis.generate_report(self.results, "01", "01", "2020", "12")
        #print(data)
        self.assertEqual(2, report.with_factor("Precondiciones").historical_series())
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
        expected = (2021, "enero", 1, 3.5, 0.0)
        self.assertEqual(expected, report.with_factor("Precondiciones").get_historical_serie(1))

    def test_question_answers_to_view(self):
        self.results.add_test_answer("2020-12-28 17:08:00.482801/01/01/A021B012C121C105D065D135E062F051G055")
        self.results.add_test_answer("2020-12-28 17:08:00.482801/01/01/A022B012C121C105D065D135E062F051G055")
        q_a_view = self.results.question_answers_to_view("01", "01", 2020, 12)
        self.assertTrue(q_a_view.has_answers())

        q_id = q_a_view.questions_id("Precondiciones")[0]
        self.assertEqual("Pienso que mi sueldo actual es adecuado.", q_a_view.question_text(q_id) )
        self.assertEqual([1, 2], q_a_view.question_answers(q_id))

    def test_report_empty_if_year_does_not_exists(self):
        report = self.analisis.generate_report(self.results, None, None, 2000, 13)
        self.assertFalse(report.has_answers())


class TestHistoricDataAnalysis_2(unittest.TestCase):
    # Merge qwith te main class

    def _get_historical_data(self):
        return self.d_a.historical_data(self._raw_answers, get_survey_structure(self.repo))

    def setUp(self):
        self.repo = load_questions("preguntas_sofia.txt")
        survey_structure = get_survey_structure(self.repo, survey_name = "softia")
        #print("Name survey struct: ", survey_structure.name())
        self.analysis = RadarAnalysis(survey_structure)
        self._raw_answers = TestsResult(q_repo=self.repo, _survey_struct = survey_structure)  # Evitar esta dependencia
        #self._historical_diciembre = (2020, "diciembre", 1, 1.5, 0.0)
        self.d_a = HistoricDataAnalysis()

    def test_diferent_number_of_answers(self):
        self._raw_answers.add_test_answer("2023-06-12 08:38:38.638461/01/01/00121023A014A035A024B023B014B033C014C023C033D055D015D022D044D035E021E033E013F043F025F054F033F015G114G014H055H042H033H025H014I014I035I025/SOFTIA")
        self._raw_answers.add_test_answer("2023-07-02 09:56:12.321417/01/01/00111023A035A014A024B023B035C035C015C025D022D055D035D042D015E023E033E013F055F043F015F025F033G014G114H055H043H025H015H034I035I015I024/SOFTIA")
        result = self._get_historical_data()
        #print(result)
        self.assertIsNotNone(result)

    def test_flag_when_diferent_answers(self):
        self._raw_answers.add_test_answer(
            "2023-06-12 08:38:38.638461/01/01/00121023A014A035A024B023B014B033C014C023C033D055D015D022D044D035E021E033E013F043F025F054F033F015G114G014H055H042H033H025H014I014I035I025/SOFTIA")
        self._raw_answers.add_test_answer(
            "2023-07-02 09:56:12.321417/01/01/00111023A035A014A024B023B035C035C015C025D022D055D035D042D015E023E033E013F055F043F015F025F033G014G114H055H043H025H015H034I035I015I024/SOFTIA")
        _ = self._get_historical_data()
        flags = self.d_a.result_flag()
        #print(flags)
        self.assertIsNotNone(flags)
        self.assertNotIn("Zero_Surveys", flags)
        self.assertTrue(flags["Diff_Num_of_Answers"])


class TestRadarAnalysis_SafetyTest(unittest.TestCase):

    def setUp(self):
        self.repo = load_questions()
        self.test_struct = get_survey_structure(self.repo, "SAFETY")
        self.results = TestsResult(q_repo=self.repo, questions_number=7)
        self.analisis = RadarAnalysis(get_survey_structure(self.repo, survey_name = "SAFETY"))

    def test_analysis_safety_test(self):
        self.results.add_test_answer("2021-03-19 18:42:14.254246/01/01/C055C075C105C145C195C205C185/SAFETY")
        self.results.add_test_answer("2021-03-19 18:58:31.121013/01/01/C055C065C095C135C195C085C125/SAFETY")
        self.assertEqual(2, len(self.results.get_surveys()))

        report = self.analisis.generate_report(self.results, "01", "01", 2021, 3)
        self.assertTrue(report.has_answers())
        #print(report)
        #print(report.factors().keys())
        expected = "dict_keys(['SP01. Feedback', 'SP02. Preguntar y expresar ideas divergentes', 'SP03. Compartir ideas', 'SP04. Errores', 'Miscelanea'])"
        self.assertEqual(expected, str(report.factors().keys()))
    """
    def test_load_safety_test_from_file(self):
        results = load_test_results(self.repo, "01", "01", survey_name="SAFETY", filename="IWT2_reports\\safety.txt")
        #print(results.get_surveys())
        self.assertEqual(2, len(results.get_surveys()))
    

    def test_analyze_safety_test_from_file(self):
        results = load_test_results(self.repo, "01", "01", survey_name="SAFETY", filename="IWT2_reports\\safety.txt")
        #print(results.get_surveys())
        self.assertEqual(2, len(results.get_surveys()))
        report = generate_report(results, "01", "01", year=2021, month=3, survey="SAFETY")
        #print(report)
        self.assertTrue(report.has_answers())
        # print(report.factors().keys())
        expected = "dict_keys(['SP01. Feedback', 'SP02. Preguntar y expresar ideas divergentes', 'SP03. Compartir ideas', 'SP04. Errores', 'Miscelanea'])"
        self.assertEqual(expected, str(report.factors().keys()))
    """

    def test_flags(self):
        _ = self.analisis.generate_report(self.results, "01", "01", 2021, 3)
        flags = self.analisis.result_flag()
        #print(flags)
        self.assertTrue(flags["Zero_Surveys"])

        self.results.add_test_answer("2021-03-19 18:42:14.254246/01/01/C055C075C105C145C195C205C185/SAFETY")
        _ = self.analisis.generate_report(self.results, "01", "01", 2021, 3)
        flags = self.analisis.result_flag()
        self.assertEqual(len(flags), 0)


class Test_SurveysOverview(unittest.TestCase):

    def test_surveys_overview(self):
        s_overview = surveys_overview("01", "01", filename="tests/data_test.txt")
        #print(s_overview)
        expected = "{2020: {12: {'RADAR-9': {'_inc': 1}}}, 2021: {1: {'RADAR-9': {'_inc': 3}}, 2: {'RADAR-9': {'_inc': 2}}}, 2023: {6: {'CREWRADARSATISFACCION': {'_inc': 2}}}}"
        self.assertEqual(expected, str(s_overview))

    def test_surveys_from_poll(self):
        s_overview = surveys_from_poll("SoftIA", filename="tests/data_test.txt")
        expected = "{2023: {6: {'S1': {'_inc': 2}}, 7: {'S1': {'_inc': 1}, 'S2': {'_inc': 1}}}}"
        self.assertEqual(expected, str(s_overview))


class Test_RawAnswer(unittest.TestCase):

    def test_avoid_new_line_at_the_end(self):
        line_no_new_line = "2021-03-24 15:20:50.278679/01/01/A045BL45C085C195D065D055E035F045G055/RADAR-9"
        line_new_line = "2021-03-24 15:20:50.278679/01/01/A045BL45C085C195D065D055E035F045G055/RADAR-9\n"
        raw_answer = RawAnswer.create(line_no_new_line)
        self.assertEqual("RADAR-9", raw_answer.test_type())
        raw_answer = RawAnswer.create(line_new_line)
        self.assertEqual("RADAR-9", raw_answer.test_type())


class Test_HistoricDataAnalysis(unittest.TestCase):

    def setUp(self):
        self.repo = load_questions()
        self.results = TestsResult(q_repo=self.repo)
        self.results.add_test_answer("2021-01-28 17:08:00.482801/01/01/A021B012C121C105D065D135E062F051G055")
        self.results.add_test_answer("2021-01-28 17:08:02.912267/01/01/A012B044C042C015D135D101E022F045G055")
        self.results.add_test_answer("2021-02-28 17:08:02.912267/01/01/A012B044C042C015D135D101E022F045G055")
        self.results.add_test_answer("2021-03-28 17:08:02.912267/01/01/A012B044C042C015D135D101E022F045G055")

        self.d_a = HistoricDataAnalysis()
        self.result = self.d_a.historical_data(self.results, get_survey_structure(self.repo))

    def test_historical_data(self):
        expected = "{2021: {1: {'_value': 2, 'Precondiciones': {'_value': (1.75, 0.25)}, 'Seguridad sicológica': {'_value': (1.25, 0.25)}, 'Compromiso con el trabajo': {'_value': (1.0, 0.0)}, 'Perfiles y responsabilidad': {'_value': (2.0, 0.0)}, 'Resultados significativos': {'_value': (1.0, 0.0)}, 'Propósito e impacto': {'_value': (1.0, 0.0)}}"
        #print(result)
        self.assertTrue(str(self.result).startswith(expected))

    def test_answer_number(self):
        self.assertEqual(2, self.result.begin().group(2021).group(1).value())
        self.assertEqual(1, self.result.begin().group(2021).group(2).value())
        self.assertEqual(1, self.result.begin().group(2021).group(3).value())

    def test_no_surveys(self):
        results = TestsResult(q_repo=self.repo)
        self.result = self.d_a.historical_data(results, get_survey_structure(self.repo))
        self.assertEqual(0, len(self.result.begin().keys()))

    def test_safety_test(self):
        test_struct = get_survey_structure(self.repo, "SAFETY")
        self.results = TestsResult(q_repo=self.repo, questions_number=test_struct.num_of_questions())
        self.results.add_test_answer("2021-03-19 18:42:14.254246/01/01/C055C075C105C145C195C205C185/SAFETY")
        self.results.add_test_answer("2021-03-19 18:58:31.121013/01/01/C055C065C095C135C195C085C125/SAFETY")
        self.assertEqual(2, len(self.results.get_surveys()))
        result = self.d_a.historical_data(self.results, get_survey_structure(self.repo, survey_name = "SAFETY"))
        #print(result)
        self.assertIn(2021, result.begin().keys())
        self.assertIn(3, result.begin().group(2021).keys())
        self.assertEqual(5, len(result.begin().group(2021).group(3).keys()))


class Test_Survey_And_AnsweredQuestion(unittest.TestCase):

    def setUp(self):
        self.survey = Survey("2020-12-23 15:24:17.008097", "01", "01")
        self.survey.add_a_q(AnsweredQuestion("1", "5"))

    def test_create_survey(self):
        self.assertEqual(2020, self.survey.year()) # int
        self.assertEqual(12, self.survey.month()) # int

    def test_answered_question(self):
        answer = self.survey.answers()[0]
        answer.set_question(TestQuestion("text", "code", "valoration", "cat_name"))
        self.assertEqual("code", answer.id())
        self.assertEqual("1", answer.adapted_answer())
        self.assertEqual("5", answer.original_answer())


class Test_CVSResults(unittest.TestCase):

    def setUp(self):
        self.results = TestsResult(q_repo=load_questions()) # Evitar esta dependencia
        self.results.add_test_answer("2020-12-23 15:24:17.008097/01/01/A035B033C032C065D121D023E075F053G022")
        self.cvs = CVSResults()

    def test_results_to_cvs(self):
        cvs_text = self.cvs._results_to_cvs(self.results.get_surveys(), {'A01':"", 'A02':"", 'A03':""})
        self.assertEqual("1, 2020, 12, , , 5, \n", cvs_text)

    def test_header_cvs(self):
        cvs_text = self.cvs._header({'A01':"", 'A02':"", 'A03':""})
        self.assertEqual("Question, Year, Month, A01, A02, A03, \n", cvs_text)



class Test_surveys_from_poll(unittest.TestCase):

    def setUp(self):
        pass

    def test_crewradarsatisfaction(self):
        groups = surveys_from_poll("CrewRadarSatisfaccion")
        self.assertNotEqual("{}", str(groups))

    def test_load_test_results(self):
        struct = _get_struct("CrewRadarSatisfaccion")
        # Cambiar el fichero para que nos e cmabien los datos: , filename="IWT2_reports\\safety.txt"
        #print("\n\n\n--- Failed test ------")
        results = load_test_results(None, "01", "01", survey_struct=struct, filename = "tests\\data_test.txt")
        self.assertEqual(2, len(results.get_surveys()))

if __name__ == '__main__':
    unittest.main()
