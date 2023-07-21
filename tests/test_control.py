import unittest

from control import _check_error, _get_struct, get_template_name
from tappraisal import TestStructsCache
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


class FakeResquest():
    def __init__(self):
        self.lang = ""

class FakeQuestion():
    def category(self):
        return '0'

class TestTemplateName(unittest.TestCase):
    def test_default(self):
        template_name = get_template_name("report", "default", FakeResquest())
        self.assertEqual("default", template_name)
        template_name = get_template_name("question", "default")
        self.assertEqual("default", template_name)
        template_name = get_template_name("no_exists", "default", FakeResquest())
        self.assertEqual("default", template_name)


    def test_english_template(self):
        request = FakeResquest()
        request.lang = "en"
        template_name = get_template_name("report", "default", request)
        self.assertEqual("default_en", template_name)

    def test_request_in_question_template(self):
        request = FakeResquest()
        request.lang = "en"
        template_name = get_template_name("question", "question_template", request)
        self.assertEqual("question_template_en", template_name)

    def test_personalizated_template(self):
        sofia_struct = TestStructsCache.get_struct("softia")
        template_name = get_template_name("question", "question_template", survey_struct=sofia_struct, question=FakeQuestion())
        self.assertEqual("softia_gender_question_template", template_name)


if __name__ == '__main__':
    unittest.main()
