import unittest
from analysis import TestsResult, RadarAnalysis, questions_answers, _load_answers
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



class TestRadarAnalysis(unittest.TestCase):

    def _get(self, data, key1, key2 = None):
        val = data[key1]
        if key2 is not None:
            val = val[key2]
        return str(val)

    def test_analysis(self): # Este etst es muy frágil, poner solo los valores.
        analisis = RadarAnalysis()
        results = TestsResult(q_repo=load_questions())  # Evitar esta dependencia
        results.add_test_answer("2021-01-28 17:08:00.482801/01/01/A021B012C121C105D065D135E062F051G055")
        results.add_test_answer("2021-01-28 17:08:02.912267/01/01/A012B044C042C015D135D101E022F045G055")
        # crear el databrame directaente.
        df = results.create_dataframe()
        data = analisis.analyze(df, "01", "01")
        #print(data)
        expected = "({'Precondiciones': {'answer': [[1, 2], [2, 2]], 'mean': ['1.5', '2.0'], 'mad': ['0.5', '0.0'], 'analysis': 'La media indica que la mayoría de las repsuestas están en los valores inferiores. recomenamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo.'}, 'Seguridad sicológica': {'answer': [[1, 1], [2, 1]], 'mean': ['1.5', '1.0'], 'mad': ['0.5', '0.0'], 'analysis': 'La media indica que la mayoría de las repsuestas están en los valores inferiores. recomenamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo.'}, 'Dependabilidad': {'answer': [[1, 1], [1, 1]], 'mean': ['1.0', '1.0'], 'mad': ['0.0', '0.0'], 'analysis': 'La media indica que la mayoría de las repsuestas están en los valores inferiores. recomenamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo.'}, 'Estructura y claridad': {'answer': [[2], [2]], 'mean': ['2.0'], 'mad': ['0.0'], 'analysis': 'La media indica que la mayoría de las repsuestas están en los valores inferiores. recomenamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo.'}, 'Significado': {'answer': [[1], [1]], 'mean': ['1.0'], 'mad': ['0.0'], 'analysis': 'La media indica que la mayoría de las repsuestas están en los valores inferiores. recomenamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo.'}, 'Impacto': {'answer': [[1], [1]], 'mean': ['1.0'], 'mad': ['0.0'], 'analysis': 'La media indica que la mayoría de las repsuestas están en los valores inferiores. recomenamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo.'}}, {'year': 2021, 'month': 1})"
        self.assertEqual(expected, str(data))
        expected = "['1.5', '2.0']"
        self.assertEqual(expected, self._get(data[0], "Precondiciones", "mean"))

    def test_result_has_month_and_year(self): # Este etst es muy frágil, poner solo los valores.
        analisis = RadarAnalysis()
        results = TestsResult(q_repo=load_questions())  # Evitar esta dependencia
        results.add_test_answer("2021-01-28 17:08:00.482801/01/01/A021B012C121C105D065D135E062F051G055")
        results.add_test_answer("2021-01-28 17:08:02.912267/01/01/A012B044C042C015D135D101E022F045G055")
        # crear el databrame directaente.
        data = analisis.analyze(results.create_dataframe(), "01", "01")
        #print(data)
        expected = "{'year': 2021, 'month': 1}"
        self.assertEqual(expected, str(data[1]))


    def test_return_original_anser_for_questions(self):
        results = _load_answers(load_questions())
        answers = questions_answers(results, "APP-IMEDEA", None) # Evitar esta dependencia
        expected = "G05.Impacto. Creo que no puedo conseguir ningún avance significativo con mi trabajo.:[5, 5]"
        self.assertEqual(expected, answers[-1])



if __name__ == '__main__':
    unittest.main()
