
# 0 not in use

MONTHS =("", "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")


class QuestionsAnswersView(object):

    def __init__(self): # TODO use quetsion object
        self._cats = dict()
        self._texts = dict()
        self._answers = dict()
        self._questions = dict()

    def add(self, question_obj, category, answer):
        if category not in self._cats:
            self._cats[category] = dict()
        self._cats[category][question_obj.code()] = question_obj.code()
        self._texts[question_obj.code()] = question_obj.text()
        if question_obj.code() not in self._answers:
            self._answers[question_obj.code()] = list()
        self._answers[question_obj.code()].append(answer)
        self._questions[question_obj.code()] = question_obj

    def categories(self):
        return list(self._cats.keys())

    def questions_id(self, category):
        return list(self._cats[category].keys())

    def question_text(self, p_id):
        return self._texts[p_id]

    def question_answers(self, p_id):
        return self._answers[p_id]

    def question_obj(self, p_id):
        return self._questions[p_id]

    def has_answers(self):
        return len(self._cats) > 0

    def contains(self, id):
        return id in self._questions

    def __str__(self):
        return str(self._cats) + " Answers: " + str(len(self._answers))


class _Factor(object):
    def __init__(self):
        self._means = None
        self._total_mean = None
        self._mads = None
        self._total_mad = None
        self._analysis_text = None
        self._his_year = list()
        self._his_month = list()
        self._his_answers_num = list()
        self._his_mean = list()
        self._his_mad = list()

    def add_means(self, means_list, final_mean = None):
        self._means = means_list
        self._total_mean = final_mean

    def means(self):
        return self._means

    def total_mean(self):
        return self._total_mean

    def add_mads(self, mads_list, final_mad = None):
        self._mads = mads_list
        self._total_mad = final_mad

    def mads(self):
        return self._mads

    def total_mad(self):
        return self._total_mad

    def add_analysis(self, anallysis_text):
        self._analysis_text = anallysis_text

    def get_analysis(self):
        return self._analysis_text

    def add_historical_serie(self, year, month, answer_num, mean, mad):
        self._his_year.append(year)
        self._his_month.append(month)
        self._his_answers_num.append(answer_num)
        self._his_mean.append(mean)
        self._his_mad.append(mad)

    def historical_series(self):
        return len(self._his_year)

    def get_historical_serie(self, index):
        global MONTHS
        #print(int(self._his_month[index]))
        return self._his_year[index], MONTHS[ int(self._his_month[index]) ], self._his_answers_num[index], self._his_mean[index], self._his_mad[index]


class ReportView(object):

    def __init__(self):
        self._factors = dict()
        self._year = None
        self._month = None
        self._answers_len = None
        self._project_id = None
        self._group_id = None
        self._struct_name = None

    def with_factor(self, factor_name):
        if factor_name not in self._factors:
            self._factors[factor_name] = _Factor()

        return self._factors[factor_name]

    def factors(self):
        return self._factors

    def iter_factors(self):
        return self._factors.items()

    def year(self, p_year):
        self._year = p_year

    def month(self, p_month):
        self._month = p_month

    def project_id(self, p_month):
        self._project_id = p_month

    def group_id(self, p_month):
        self._group_id = p_month

    def struct_name(self, p_month):
        self._struct_name = p_month

    def answers_len(self, answers_num):
        self._answers_len = answers_num

    def get_year(self):
        return self._year

    def get_month(self):
        global MONTHS
        return MONTHS[ self._month ]

    def get_answers_len(self):
        return self._answers_len

    def get_project_id(self):
        return self._project_id

    def get_group_id(self):
        return self._group_id

    def get_struct_name(self):
        return self._struct_name

    def has_answers(self):
        if len(self._factors) == 0:
            return False
        value = next(iter(self._factors.values()))
        return value.total_mean() is not None

    def __str__(self):
        return str(self._factors)


class HierarchicalGroups(object):

    def __init__(self):
        self._root = dict()
        self._actual = None # User must call begin

    def begin(self):
        self._actual = self._root
        return self

    def add_group(self, g_key):
        if g_key not in self._actual:
            self._actual[g_key] = dict()
        return self.group(g_key)

    def group(self, g_key):
        self._actual = self._actual[g_key]
        return self

    def inc_counter(self):
        if '_inc' not in self._actual:
            self._actual['_inc'] = 1
            return 1
        self._actual['_inc'] = + self._actual['_inc'] + 1

    def keys(self):
        #return list(self._actual.keys())
        result = list()
        for key in self._actual.keys():
            if str(key).startswith("_") is False:
                result.append(key)
        return result

    def counter(self):
        return self._actual['_inc']

    def add_in_bag(self, attrib):
        if '_attrib_list' not in self._actual:
            self._actual['_attrib_list'] = dict()
        self._actual['_attrib_list'][attrib] = attrib

    def bag(self):
        return self._actual['_attrib_list']

    def add_value(self, value):
        self._actual['_value'] = value

    def value(self):
        return self._actual['_value']

    def __str__(self):
        return str(self._root)


class PollStructView(object):

    def __init__(self, survey_structure=None):
        if survey_structure is not None:
            self._name = survey_structure.name()
            self._questions_filename = survey_structure.questions_filename()
            self._num_of_questions = survey_structure.num_of_questions()
            self._questions_in_categories = survey_structure.questions_in_categories()
            self._poll_structure = survey_structure.get_test_structure()
            self._question_groups = survey_structure.get_groups()
            self._description_dict = survey_structure.description_dict()
        else:
            self._name = ""
            self._questions_filename = ""
            self._num_of_questions = ""
            self._questions_in_categories = """Example: {"A":3, "B":1}"""
            self._poll_structure = """Example: {"A":"Formación", "B":"Flexibilidad"} """
            self._question_groups = """Example: {"Formación":[3], "Flexibilidad":[4]}"""
            self._description_dict = """Example: {"Formación":"Formación.", "Flexibilidad": "Flexibilidad."} """

    def name(self):
        return self._name

    def num_of_questions(self):
        return self._num_of_questions

    def questions_in_categories(self):
        return self._questions_in_categories

    def get_test_structure(self):
        return self._poll_structure

    def get_groups(self):
        return self._question_groups

    def questions_filename(self):
        return self._questions_filename

    def description_dict(self):
        return self._description_dict

    def filename(self):
        return self.name() + ".txt"

    @staticmethod
    def from_request(form_request):
        poll_view = PollStructView()

        poll_view._name = form_request.forms.get('poll_name').strip()
        poll_view._questions_filename = form_request.forms.get('questions_file').strip()
        poll_view._num_of_questions = form_request.forms.get('num_of_questions').strip()
        poll_view._questions_in_categories = form_request.forms.get('questions_in_categories').strip()
        poll_view._poll_structure = form_request.forms.get('poll_structure').strip()
        poll_view._question_groups = form_request.forms.get('groups').strip()
        poll_view._description_dict = form_request.forms.get('descriptions').strip()

        return poll_view

    def to_json(self):
        # Deprecated. Usamos eld e la view
        """
        Las { hay que ponerlas en el formulario, roque si no,
        al cargar datos para editarlo, als vuelve a poner.
        """
        test_json = " {\"questions_file\": \"" \
                    + self.questions_filename() \
                    + "\", \"poll_name\": \"" + self.name() \
                    + "\", \"num_of_questions\": \"" + str(self.num_of_questions()) \
                    + "\", \"questions_in_categories\": \"" + str(self.questions_in_categories()) \
                    + "\", \"poll_structure\": \"" + str(self.get_test_structure()) \
                    + "\", \"groups\": \"" + str(self.get_groups()) \
                    + "\", \"descriptions\": \"" + str(self.description_dict()) \
                    +"\"}"
        #print("translate_to_json ", test_json)
        #import json
        #raw_json = json.loads(test_json)
        #print(raw_json)
        return test_json