import random

# Candidato a refactorizarlo a otro sitio.
def _get_full_filename(filename):
    import os
    base_path = os.path.dirname(os.path.abspath(__file__))
    my_path = os.path.join(base_path, filename)
    return my_path


def _save_data(data, survey_name, filename = "data.txt"):
    import datetime

    now = datetime.datetime.now()
    filename = _get_full_filename(filename)
    with open(filename, "a") as myfile:
        myfile.write(str(now)+"/"+str(data) + "/"+survey_name+"\n")


# renombrar a WebTestInfo o algo así
# como lo crea Bottle, es pisible que tenga que estar en su módulo y no aquí.
class TestData(object):

    def __init__(self, org_id, project_id, questions):
    #def __init__(self,  questions):
        self._questions = dict()
        self._id_set = dict()
        self._parse_questions_url(questions)
        self._url_questions = questions
        self._org_id = org_id
        self._project_id = project_id

    def __str__(self):
        return self._org_id+"/" + self._project_id+"/" + self._url_questions
        #return self._url_questions

    def _parse_questions_url(self, q_url):
        self._answers = 0

        answer_len = int( len(q_url) / 4 )
        for i in range(0, answer_len):
            tmp = q_url[(4*i):(4*i)+4]
            q_id = tmp[0:3]
            #answer = tmp[3]
            category = q_id[0]

            if category not in self._questions:
                self._questions[category] = list()
            self._questions[category].append(q_id[1:3])
            self._id_set[q_id] = q_id

    def len_questions(self):
        return len(self.ids_set())

    def len_questions_in(self, category):
        if category not in self._questions:
            return 0
        return len(self._questions[category])

    def ids_set(self):
        return self._id_set


class TestQuestion(object):

    def __init__(self, text, code="", valoration="", cat_name = ""):
        self._text_question = text
        self._code = code
        self._valoration=valoration
        self._cat_name = cat_name.strip()

    def text(self):
        return self._text_question

    def category(self):
        return self._code[0]

    def code(self):
        return self._code

    def is_positive(self):
        return self._valoration == "P"

    def category_name(self):
        return self._cat_name

    def __str__(self):
        return self._code+":"+self._text_question+":"+self._valoration


class AppraisalDirector_old(object):

    def __init__(self, repo = None, save_method = _save_data):
        self._questions_repo = repo
        self._save_data_method = save_method

    def _random_question_from(self, cat, data):
        ids = data.ids_set()
        question = self._questions_repo.random_question_from(cat)
        while question.code() in ids:
            question = self._questions_repo.random_question_from(cat)
        return question

    def next_question(self, data):
        """
        Veo las pregunats que ya se han hecho y busco y envío la siguiente pregunta a preguntar en el test
        o None si ya se han terminado las preguntas.
        :param data: TestData object
        :return:
        """

        if data.len_questions() == 9: # 9 preguntas
            self._save_data_method(data)
            return None

        if data.len_questions_in("A") == 0:
            return self._random_question_from("A", data)
        if data.len_questions_in("B") == 0:
            return self._random_question_from("B", data)
        if data.len_questions_in("C") < 2:
            return self._random_question_from("C", data)
        if data.len_questions_in("D") < 2:
            return self._random_question_from("D", data)
        if data.len_questions_in("E") < 1:
            return self._random_question_from("E", data)
        if data.len_questions_in("F") < 1:
            return self._random_question_from("F", data)
        if data.len_questions_in("G") < 1:
            return self._random_question_from("G", data)

        question = TestQuestion("05. ERROR")
        return question


class AppraisalDirector(object):

    def __init__(self, survey_struct, save_method = _save_data):
        self._survey_struct = survey_struct
        self._save_data_method = save_method

    def next_question(self, data):
        question = self._survey_struct.next_question(data)

        if question is None:
            self._save_data_method(data, self._survey_struct.name())

        return question


class QuestionRepository(object):

    def __init__(self):
        self._questions = dict() # Key factor, Value list of questions
        self._tmp_cat = ""

    def __str__(self):
        return str(self._questions)

    def _append(self, question):
        category = question.category()
        if category not in self._questions:
            self._questions[category] = list()

        self._questions[category].append(question)

    def commit_question(self, line):
        s_line = line.strip()
        if s_line == "":
            return None
        if s_line.startswith("#-"):
            tokens = s_line.split('#')
            #print("tokens", tokens)
            self._tmp_cat = tokens[1]+'.'+tokens[2]
            return None
        if '#' in s_line:
            return None

        elements = s_line.split(':')
        question = TestQuestion(code=elements[0].strip(), text=elements[1].strip(), valoration=elements[2].strip(), cat_name= self._tmp_cat)

        self._append(question)
        return question

    def random_question_from(self, category):
        index = random.randint(0, len(self._questions[category])-1)
        #print("Random question from", category, "max questions ", len(self._questions[category]), "index:", index)
        return self._questions[category][index]

    def get_question(self, code):
        """
        :param code:
        :return: A TestQuestion object
        """
        #print("Searching:", category, code)
        for _, questions in self._questions.items():
            for question in questions:
                #print("Code found: ", question.code())
                if question.code() == code:
                    return question
        return None

    def get_questions(self):
        return self._questions

    def as_dict(self):
        """
        :return: A dict { Code :  Questionobject }.
        """
        result = dict()
        for questions in self._questions.values():
            for question in questions:
                result[question.code()] = question
        return result


def load_questions():
    repo = QuestionRepository()
    file_name = _get_full_filename("preguntas.txt")
    file = open(file_name, encoding="utf-8") # No: encoding="latin-1" encoding="ascii"
    for line in file:
        repo.commit_question(line)
        #print("áéÍÓñÑ: " + line)
    file.close()

    return repo

##--- Aún no está en uso -------------------------------

class SurveyStructureRadar9(object):

    def __init__(self, _questions_repo):
        """
        self._structure = {'A': 1, 'B': 2, 'C': 3, 'D': 4,
                       'E': 5, 'F': 6, 'G': 1}
        self._questions_x_factor = {'A': 1, 'B':1, 'C':2, 'D':2, 'E':1, 'F':1, 'G': 1} # Test original
        self._factor_names = ["Precondiciones", "Precondiciones", "Seguridad sicológica", "Compromiso con el trabajo",
                       "Perfiles y responsabilidad", "Resultados significativos",  "Propósito e impacto"]
        self._questions = sum(self._questions_x_factor.values())
        """
        self._questions_repo = _questions_repo

    """
    def _set(self, questions_x_factor):

            #self._structure = {'A': 1, 'B': 2, 'C': 3, 'D': 4,
                               #'E': 5, 'F': 6, 'G': 1}
        self._questions_x_factor = questions_x_factor
            #self._factor_names = ["Precondiciones", "Precondiciones", "Seguridad sicológica",
                               #   "Compromiso con el trabajo",
                               #   "Perfiles y responsabilidad", "Resultados significativos", "Propósito e impacto"]
        self._questions = sum(self._questions_x_factor.values())

    def factor_next_question(self, data):
        for name, question_num in self._questions_x_factor.items():
            if data.len_questions_in(name) < question_num:
                return name
        return None
    """

    def num_of_questions(self):
        return 9

    def _random_question_from(self, cat, data):
        ids = data.ids_set()
        question = self._questions_repo.random_question_from(cat)
        while question.code() in ids:
            question = self._questions_repo.random_question_from(cat)
        return question

    def next_question(self, data):
        if data.len_questions_in("A") == 0:
            return self._random_question_from("A", data)
        if data.len_questions_in("B") == 0:
            return self._random_question_from("B", data)
        if data.len_questions_in("C") < 2:
            return self._random_question_from("C", data)
        if data.len_questions_in("D") < 2:
            return self._random_question_from("D", data)
        if data.len_questions_in("E") < 1:
            return self._random_question_from("E", data)
        if data.len_questions_in("F") < 1:
            return self._random_question_from("F", data)
        if data.len_questions_in("G") < 1:
            return self._random_question_from("G", data)
        return None

    def name(self):
        return "RADAR-9"

    def get_groups(self):
        return {"Precondiciones": [1,2], "Seguridad sicológica": [3, 4], "Compromiso con el trabajo": [5, 6],
                             "Perfiles y responsabilidad":[7], "Resultados significativos": [8], "Propósito e impacto": [9]}


class SurveyStructurePsychoSafety(object):

    def __init__(self, _questions_repo):
        """
        self._structure = {'A': 1, 'B': 2, 'C': 3, 'D': 4,
                       'E': 5, 'F': 6, 'G': 1}
        self._questions_x_factor = {'A': 1, 'B':1, 'C':2, 'D':2, 'E':1, 'F':1, 'G': 1} # Test original
        self._factor_names = ["Precondiciones", "Precondiciones", "Seguridad sicológica", "Compromiso con el trabajo",
                       "Perfiles y responsabilidad", "Resultados significativos",  "Propósito e impacto"]
        self._questions = sum(self._questions_x_factor.values())
        """
        self._questions_repo = _questions_repo
        self._questions_x_cat = dict()
        self._category_list = None # not in use
        self._all_questions = list()

        self._questions_per_category()
        for question_set in self._questions_x_cat.values():
            self._all_questions.extend(question_set)

        self.SP02 = "-SP02. Bloque 2. Pregunta original: Hesitance around expressing divergent ideas and asking 'silly' questions"
        self.SP03 = "-SP03. Bloque 3. Pregunta original: 'Do all team members feel comfortable brainstorming in front of each other?'"
        self.SP04 = "-SP04. Bloque 4. Errores."

    def _questions_per_category(self):
        #print(self._questions_repo.get_questions())
        safety_questions_list = self._questions_repo.get_questions()['C']
        category_set = dict()
        for question in safety_questions_list:
            category = question.category_name()
            if category not in self._questions_x_cat:
                self._questions_x_cat[category] = list()
            self._questions_x_cat[category].append(question)
            category_set[category] = category
        self._category_list = list(category_set.keys())
        #print("_questions_x_cat:", self._questions_x_cat)

    def num_of_questions(self):
        return 7

    def _random_question_from(self, cat, data):
        return self._random_question(self._questions_x_cat[cat], data)

    def _random_question(self, questions_list, data):
        ids = data.ids_set()
        index = random.randint(0, len(questions_list) - 1)
        selected_question = questions_list[index]
        #print("Selected", selected_question.code(), "IDS", ids)
        while selected_question.code() in ids:
            index = random.randint(0, len(questions_list) - 1)
            selected_question = questions_list[index]
        return selected_question

    def next_question(self, data):
        """
        SP01: 2, SP02: 1, SP03: 1, SP04: 1 y 2 más de todos los SP.
        :param data:
        :return:
        """
        ids = data.ids_set()
        questions = self._questions_repo.as_dict()
        num_questions_x_cat = dict()

        for id in ids:
            question = questions[id]
            if  question.category_name() not in num_questions_x_cat:
                num_questions_x_cat[question.category_name()] = 1
            else:
                num_questions_x_cat[question.category_name()] += 1

        #print(num_questions_x_cat)
        if "-SP01. Feedback" not in num_questions_x_cat or num_questions_x_cat["-SP01. Feedback"] < 2:
            return self._random_question_from("-SP01. Feedback", data)
                             # "-SP02. Bloque 2. Pregunta original: Hesitance around expressing divergent ideas and asking 'silly' questions"
        if self.SP02 not in num_questions_x_cat or num_questions_x_cat[self.SP02] < 1:
            return self._random_question_from(self.SP02, data)
        if self.SP03 not in num_questions_x_cat or num_questions_x_cat[self.SP03] < 1:
            return self._random_question_from(self.SP03, data)
        if self.SP04 not in num_questions_x_cat or num_questions_x_cat[self.SP04] < 1:
            return self._random_question_from(self.SP04, data)
        if data.len_questions() < 7:
            return self._random_question(self._all_questions, data)

        return None

    def name(self):
        return "SAFETY"

    def get_groups(self): # Implementar !!!!
        return {"Precondiciones": [1,2], "Seguridad sicológica": [3, 4], "Compromiso con el trabajo": [5, 6],
                             "Perfiles y responsabilidad":[7], "Resultados significativos": [8], "Propósito e impacto": [9]}

# Esto debe desaparecer
def get_test_structure():
    # RADAR-9
    return {'A': "Precondiciones", 'B': "Precondiciones", 'C': "Seguridad sicológica", 'D': "Compromiso con el trabajo",
                       'E': "Perfiles y responsabilidad", 'F': "Resultados significativos", 'G': "Propósito e impacto"}
    """
    # Esto también hay que gestionarlo de alguna manera
    self._test_struct = {"Precondiciones": [1,2], "Seguridad sicológica": [3, 4], "Compromiso con el trabajo": [5, 6],
                             "Perfiles y responsabilidad":[7], "Resultados significativos": [8], "Propósito e impacto": [9]}
    """


def get_survey_structure(question_repo, survey_name = "RADAR-9"):
    if survey_name.upper() == "RADAR-9" or survey_name.upper() == "TEST":
        #ss._set({'A': 1, 'B': 1, 'C': 2, 'D': 2, 'E': 1, 'F': 1, 'G': 1})
        return SurveyStructureRadar9(question_repo)
    if survey_name.upper() == "SAFETY":
        return SurveyStructurePsychoSafety(question_repo)
    return None
