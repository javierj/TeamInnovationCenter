import unittest
from tappraisal import TestData, QuestionRepository, TestQuestion, AppraisalDirector, \
    get_survey_structure, SurveyStructurePsychoSafety, _get_full_filename, SurveyStructureLoader, SurveyStructure
from view import PollStructView


def load_questions():
    repo = QuestionRepository()
    file_name = _get_full_filename("preguntas.txt")
    file = open(file_name, encoding="utf-8") # No: encoding="latin-1" encoding="ascii"
    for line in file:
        repo.commit_question(line)
    file.close()
    return repo


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

    def test_mock_data(self):
        data = _test_data("A034B135")
        self.assertFalse(data.is_mock())
        data = _test_data("0000B135")
        self.assertTrue(data.is_mock())


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

    def test_commit_worng_question(self):
        question = self.repo.commit_question("A01;Considero que mi sueldo actual no afecta a mi desempeño del trabajo.:P")
        self.assertIsNone(question)

    def test_commit_comment(self):
        question = self.repo.commit_question("# Considero que mi sueldo actual no afecta a mi desempeño del trabajo.:P")
        self.assertIsNone(question)
        question = self.repo.commit_question("A01:Considero que mi sueldo actual # no afecta a mi desempeño del trabajo.:P")
        self.assertIsNone(question)

    def test_get_category(self):
        question_obj = self.repo.get_question("B01")
        expected = "-P02. Precondiciones. Capacitación."
        self.assertEqual(expected, question_obj.category_name())

    def test_as_dict(self):
        questions_dict = self.repo.as_dict()
        self.assertIn("B01", questions_dict)
        question_obj = self.repo.get_question("B01")
        self.assertEqual(question_obj.text(), questions_dict["B01"].text())
        self.assertEqual("Siento que estoy preparado para hacer el trabajo que hago ahora mismo.", questions_dict["B01"].text())
        self.assertEqual(83, len(questions_dict))

########

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


####
# Not in use.

class Test_PollStructure(unittest.TestCase):

    def setUp(self):
        self.poll_json = """[{"name": "Radar Classic", "#":"Comentario", "#":"Comentario","number of questions": "9", "questions": [ { "block": "Seguridad sicologica", "category": "C"}, { "block": "Seguridad sicologica", "category": "C"} ], "blocks": [ {"Seguridad sicologica": "Descripcion"} ]}]"""
        self.poll_json2 = """{"name": "Radar Classic", "#":"Comentario", "#":"Comentario","number of questions": "9", "questions": [ { "block": "Seguridad sicologica", "category": "C"}, { "block": "Seguridad sicologica", "category": "C"} ], "blocks": [ {"Seguridad sicologica": "Descripcion"} ]}"""

    def test_from_josn_to_dict(self):
        import json
        list_data = json.loads(self.poll_json)
        self.assertEqual(1, len(list_data))
        first_dict = list_data[0]
        self.assertIn('name', first_dict)
        self.assertEqual(2, len(first_dict['questions']))

    def test_from_josn_to_dict_2(self):
        import json
        list_data = json.loads(self.poll_json2)
        self.assertIn('name', list_data)
        self.assertEqual(2, len(list_data['questions']))



###############################################

class FakeForm(object):
    def __init__(self):
        self.data = {'questions_file': "preguntas_sofia.txt", "poll_name": "Borrar", "questions_in_categories": "\"A\":1", "poll_structure": "\"A\":1", "groups":"\"A\":1", "descriptions":"\"A\":1"}

    def get(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return "\"Key not found\""


class FakeRequest(object): # Esto ya no lo uso, pero puede ser útil para pruebas de control o view
    def __init__(self):
        self.forms = FakeForm()


class Test_LoadPollStructureFromFile(unittest.TestCase):

    def setUp(self):
        self.loader = SurveyStructureLoader()
        self.structure = self.loader.load_structure("softia.txt")

    def test_load_name(self):
        self.assertEqual("SoftIA", self.structure.name())

    def test_load_nun_of_questions(self):
        self.assertEqual(33, self.structure.num_of_questions())

    def test_load_questions_in_categories(self):
        self.assertIsNotNone(self.structure.questions_in_categories())
        self.assertEqual(1, self.structure.questions_in_categories()["0"])

    def test_dont_change_quotes(self):
        self.structure = self.loader.load_structure("radar9.txt")
        struct_view = PollStructView(self.structure)
        self.loader.save_structure(struct_view.filename(), struct_view.to_json())
        self.structure = self.loader.load_structure("RADAR-9.txt")
        struct_view = PollStructView(self.structure)
        self.loader.save_structure(struct_view.filename(), struct_view.to_json())
        self.structure = self.loader.load_structure("RADAR-9.txt")
        struct_view = PollStructView(self.structure)
        #print(struct_view.to_json())
        self.assertIn("\"poll_name\": \"RADAR-9\"", struct_view.to_json())


class Test_SurveyStructure(unittest.TestCase):

    def setUp(self):
        loader = SurveyStructureLoader()
        self.structure = loader.load_structure("radar9.txt")
        self.structure.set_questions_repo(load_questions())
        self._sp01 = ["A01", "A02", "A03", "A04", "A05", "A06", "A07"]
        self._sp02 = ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "BL1", "BL2", "BL3", "BL4", "BL5"]

    def test_first_question(self):
        data = _test_data("")
        question = self.structure.next_question(data)
        self.assertEqual("A", question.category())
        self.assertIn(question.code(), self._sp01)

    def test_second_question(self):
        data = _test_data("A011")
        question = self.structure.next_question(data)
        self.assertEqual("B", question.category())
        self.assertIn(question.code(), self._sp02)

    def test_last_question(self):
        data = _test_data("A011B022C083C134D185D036E047F011G011")
        self.assertEqual(self.structure.num_of_questions(), data.len_questions())
        question = self.structure.next_question(data)
        self.assertIsNone(question)

"""
    def test_from_string_to_dict(self):
        result = SurveyStructure._from_string_to_dict("0:Género,1:Titulación necesaria,A:Formación")
        self.assertTrue( len(result) > 0 )
        print("test_from_string_to_dict", result)
        self.assertEqual(result["0"], "Género")
"""

if __name__ == '__main__':
    unittest.main()
