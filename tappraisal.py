import random

# Candidato a refactorizarlo a otro sitio.
from utilities import Cache, _get_full_filename, file_exists


def _save_data(data, survey_name, filename = "data.txt"):
    """
    No tests for this method. Should writ some.
    :param data: TestData object
    :param survey_name:
    :param filename:
    :return: nothing
    """
    import datetime

    if data.is_mock():
        return

    now = datetime.datetime.now()
    filename = _get_full_filename(filename)
    with open(filename, "a") as myfile:
        myfile.write(str(now)+"/"+str(data) + "/"+survey_name.upper()+"\n")


# renombrar a WebTestInfo o algo así
# como lo crea Bottle, es pisible que tenga que estar en su módulo y no aquí.
class TestData(object):

    def __init__(self, org_id, project_id, questions):
    #def __init__(self,  questions):
        self._questions = dict()
        self._id_set = dict()
        self._url_questions = questions
        self._org_id = org_id
        self._project_id = project_id
        self._parse_questions_url()

    def __str__(self):
        return self._org_id+"/" + self._project_id+"/" + self._url_questions
        #return self._url_questions

    def _parse_questions_url(self):
        self._answers = 0
        q_url = self._url_questions

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
        questions = len(self.ids_set())
        if self.is_mock():
            return questions-1
        return questions

    def len_questions_in(self, category):
        if category not in self._questions:
            return 0
        return len(self._questions[category])

    def ids_set(self):
        return self._id_set

    def is_mock(self):
        return  self._url_questions[0:4] == "0000"


class TestQuestion(object):

    def __init__(self, text, code="", valoration="", cat_name=""):
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


class AppraisalDirector(object):

    def __init__(self, survey_struct, save_method = _save_data):
        self._survey_struct = survey_struct
        self._save_data_method = save_method

    def next_question(self, data):
        """

        :param data:
        :return: objeto TestQuestion
        """
        question = self._survey_struct.next_question(data)

        if question is None:
            self._save_data_method(data, self._survey_struct.name())

        return question


class QuestionRepository(object):

    def __init__(self):
        self._questions = dict() # Key factor, Value list of questions (objects of TestQuestion)
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


def load_questions(filename="preguntas_sofia.txt", basedir=None):
    """
    :param filename:
    :param basedir:
    :return: None if file with questions does not exists.
    """
    repo = QuestionRepository()

    # Cambiado para softIA
    # file_name = _get_full_filename("preguntas.txt")
    file_name = _get_full_filename(filename, basedir)
    if not file_exists(file_name):
        return None

    file = open(file_name, encoding="utf-8") # No: encoding="latin-1" encoding="ascii"
    for line in file:
        repo.commit_question(line)
        #print("áéÍÓñÑ: " + line)
    file.close()

    return repo


################################################
# Structures


class SurveyStructure(object):
    def __init__(self):
        self._name = "NOSET"
        self._questions_filename = "NOSET"
        self._num_of_questions = -1
        self._questions_in_categories = None
        self._questions_repo = None # It has to come from the outside
        self._poll_structure = None
        self._question_groups = None
        self._description_dict = None

    def name(self):
        return self._name

    def num_of_questions(self):
        return  self._num_of_questions

    def questions_in_categories(self):
        return self._questions_in_categories

    def get_test_structure(self):
        return self._poll_structure

    def get_groups(self):
        return self._question_groups

    def questions_filename(self):
        return self._questions_filename

    def _random_question_from(self, cat, data):
        ids = data.ids_set()
        question = self._questions_repo.random_question_from(cat)
        while question.code() in ids:
            question = self._questions_repo.random_question_from(cat)
        return question

    def set_questions_repo(self, repo):
        self._questions_repo = repo

    def questions_repo(self):
        return self._questions_repo

    def description_dict(self):
        return self._description_dict

    def next_question(self, data):
        for key, value in self._questions_in_categories.items():
            if data.len_questions_in(key) < value:
                return self._random_question_from(key, data)
        # Poll is over.
        return None

    def load_json(self, raw_json):
        self._name = raw_json["poll_name"]
        self._questions_filename =raw_json["questions_file"]
        self._num_of_questions = int(raw_json["num_of_questions"])
        self._questions_in_categories = raw_json["questions_in_categories"]
        self._poll_structure = raw_json["poll_structure"]
        self._question_groups = raw_json["groups"]
        self._description_dict = raw_json["descriptions"]

    @staticmethod
    def _from_string_to_dict(raw_string):
        # Deprecated, solo se usa en casos de prueba.
        result = dict()

        for pair in raw_string.split(","):
            tuple = pair.split(":")
            if len(tuple) != 2:
                print("_from_string_to_dict: pair has worng lenght ", pair)
                continue
            key = tuple[0].strip()
            value = tuple[1].strip()

            result[key] = value

        return result

    @staticmethod
    def translate_to_json(form_request):
        # Deprecated. Usamos eld e la view
        """
        Las { hay que ponerlas en el formulario, roque si no,
        al cargar datos para editarlo, als vuelve a poner.
        """
        test_json = " {\"questions_file\": \"" \
                    + form_request.forms.get('questions_file') \
                    + "\", \"poll_name\": \"" + form_request.forms.get('poll_name') \
                    + "\", \"num_of_questions\":" + form_request.forms.get('num_of_questions') \
                    + ", \"questions_in_categories\": " + form_request.forms.get('questions_in_categories').replace("'", "\"") \
                    + ", \"poll_structure\": " + form_request.forms.get('poll_structure') \
                    + ", \"groups\":" + form_request.forms.get('groups') \
                    + ", \"descriptions\":" + form_request.forms.get('descriptions') \
                    +"}"
        #print("translate_to_json ", test_json)
        #import json
        #raw_json = json.loads(test_json)
        #print(raw_json)
        return test_json


class SurveyStructureLoader(object):

    def load_structure(self, filename, basedir="polls"):
        poll_structure = SurveyStructure()
        file_name = _get_full_filename(filename, basedir)

        import json
        file = open(file_name, encoding="utf-8")  # No: encoding="latin-1" encoding="ascii"
        raw_json = json.load(file)
        #print("load_structure", raw_json)
        file.close()

        poll_structure.load_json(raw_json)

        return poll_structure

    #def save_structure(self, form_request, basedir="polls"):
    def save_structure(self, filename, json_raw, basedir="polls"):
        #json_raw = SurveyStructure.translate_to_json(form_request)
        #filename = form_request.forms.get('poll_name') + ".txt"
        file_name = _get_full_filename(filename, basedir)

        #import json
        file = open(file_name, "w", encoding="utf-8")  # No: encoding="latin-1" encoding="ascii"
        #json.dump(json_raw, file)
        file.write(json_raw)
        file.close()

##

class SurveyStructureRadar9(object):

    def __init__(self, _questions_repo):
        self._questions_repo = _questions_repo

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

    def description_dict(self):
        """ Usado por la plantilla que muestra el informe. """
        defs = dict()
        defs['Precondiciones'] = "Recoge todos los factores higiénicos de motivación (motivaciçon extrínseca)."
        defs['Seguridad sicológica'] = "Poder asumir riesgos sin miedo a represalias."
        defs['Compromiso con el trabajo'] = "Las personas de las que depende mi trabajo adquieren compromisos y los cumplen."
        defs['Perfiles y responsabilidad'] = "Toma de decisiones clara, responsables definidas y tareas claras."
        defs['Resultados significativos'] = "Me importa mi trabajo y me siento implicado haciéndolo."
        defs['Propósito e impacto'] = "El trabajo que realizo tiene una utilidad y un impacto."
        return defs


    def get_test_structure(self):
        # RADAR-9
        return {'A': "Precondiciones", 'B': "Precondiciones", 'C': "Seguridad sicológica", 'D': "Compromiso con el trabajo",
                       'E': "Perfiles y responsabilidad", 'F': "Resultados significativos", 'G': "Propósito e impacto"}


class SurveyStructureRadarClassic(object):

    def __init__(self, _questions_repo):
        self._questions_repo = _questions_repo

    def num_of_questions(self):
        return 9

    def _random_question_from(self, cat, data):
        ids = data.ids_set()
        question = self._questions_repo.random_question_from(cat)
        while question.code() in ids:
            question = self._questions_repo.random_question_from(cat)
        return question

    def next_question(self, data):
        if data.len_questions_in("C") < 2:
            return self._random_question_from("C", data)
        if data.len_questions_in("D") < 2:
            return self._random_question_from("D", data)
        if data.len_questions_in("E") < 2:
            return self._random_question_from("E", data)
        if data.len_questions_in("F") < 2:
            return self._random_question_from("F", data)
        if data.len_questions_in("G") < 1:
            return self._random_question_from("G", data)
        return None

    @staticmethod
    def name():
        return "CLASSIC"

    def get_groups(self):
        return {"Seguridad sicológica": [1, 2], "Compromiso con el trabajo": [3, 4],
                             "Perfiles y responsabilidad":[5, 6], "Resultados significativos": [7, 8], "Propósito e impacto": [9]}

    def description_dict(self):
        """ Usado por la plantilla que muestra el informe. """
        defs = dict()
        defs['Seguridad sicológica'] = "Poder asumir riesgos sin miedo a represalias."
        defs['Compromiso con el trabajo'] = "Las personas de las que depende mi trabajo adquieren compromisos y los cumplen."
        defs['Perfiles y responsabilidad'] = "Toma de decisiones clara, responsables definidas y tareas claras."
        defs['Resultados significativos'] = "Me importa mi trabajo y me siento implicado haciéndolo."
        defs['Propósito e impacto'] = "El trabajo que realizo tiene una utilidad y un impacto."
        return defs


class SurveyStructurePsychoSafety(object):

    def __init__(self, _questions_repo):
        self._questions_repo = _questions_repo
        self._questions_x_cat = dict()
        self._category_list = None # not in use
        self._all_questions = list()

        # Creo que este c´´oigo no hace nada
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

    def get_groups(self):
        return {"SP01. Feedback": [1,2],
                "SP02. Preguntar y expresar ideas divergentes": [3],
                "SP03. Compartir ideas": [4],
                "SP04. Errores":[5],
                "Miscelanea": [6, 7]}

    def description_dict(self):
        """ Usado por la plantilla que muestra el informe. """
        defs = dict()
        defs['SP01. Feedback'] = "ToDo."
        defs["SP02. Preguntar y expresar ideas divergentes"] = "ToDo."
        defs["SP03. Compartir ideas"] = "ToDo"
        defs["SP04. Errores"] = "ToDo"
        defs["Miscelanea"] = "ToDo"
        return defs

    def get_test_structure(self):
        # RADAR-9
        return {'A': "Precondiciones", 'B': "Precondiciones", 'C': "Seguridad sicológica", 'D': "Compromiso con el trabajo",
                       'E': "Perfiles y responsabilidad", 'F': "Resultados significativos", 'G': "Propósito e impacto"}


#########

class SurveyStructureSoftIA(object):

    def __init__(self, _questions_repo):
        self._questions_repo = _questions_repo

    def num_of_questions(self):
        return 34

    def _random_question_from(self, cat, data):
        ids = data.ids_set()
        question = self._questions_repo.random_question_from(cat)
        while question.code() in ids:
            question = self._questions_repo.random_question_from(cat)
        return question

    def next_question(self, data):
        if data.len_questions_in("0") < 1:
            return self._random_question_from("0", data)
        if data.len_questions_in("1") < 1:
            return self._random_question_from("1", data)

        if data.len_questions_in("A") < 3:
            return self._random_question_from("A", data)
        if data.len_questions_in("B") < 3:
            return self._random_question_from("B", data)
        if data.len_questions_in("C") < 3:
            return self._random_question_from("C", data)
        if data.len_questions_in("D") < 5:
            return self._random_question_from("D", data)
        if data.len_questions_in("E") < 3:
            return self._random_question_from("E", data)
        if data.len_questions_in("F") < 5:
            return self._random_question_from("F", data)
        if data.len_questions_in("G") < 2:
            return self._random_question_from("G", data)
        if data.len_questions_in("H") < 5:
            return self._random_question_from("H", data)
        if data.len_questions_in("I") < 3:
            return self._random_question_from("I", data)
        return None

    @staticmethod
    def name():
        return "SOFTIA"

    def get_groups(self):
        return {
            "Género": [1],
            "Titulación": [2],
            "Formación": [3],
                "Flexibilidad": [4],
                "Errores": [5],
                "Automatización": [6],
                "Herramientas": [7],
                "Satisfacción": [8],
                "Planificación y formación": [9],
                "Desarrollo del proyecto": [10],
                "Resultados": [11],
                }

    def description_dict(self):
        """ Usado por la plantilla que muestra el informe. """
        defs = dict()
        defs['Género'] = "Género."
        defs['Titulación'] = "Titulación."
        defs['Formación'] = "Formación."
        defs['Flexibilidad'] = "Flexibilidad."
        defs['Errores'] = "Errores."
        defs['Automatización'] = "Automatización."
        defs['Herramientas'] = "Herramientas."
        defs['Satisfacción'] = "Satisfacción."
        defs['Planificación y formación'] = "Planificación y formación."
        defs['Desarrollo del proyecto'] = "Desarrollo del proyecto."
        defs['Resultados'] = "Resultados."
        return defs

    def get_test_structure(self):
        return {
            '0': "Género",
            '1': "Titulación",
            'A': "Formación",
                'B': "Flexibilidad",
                'C': "Errores",
                'D': "Automatización",
                       'E': "Herramientas",
                'F': "Satisfacción",
                'G': "Planificación y formación",
                'H': "Desarrollo del proyecto",
                'I': "Resultados",
                }

#########

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
    if survey_name.upper() == SurveyStructureRadarClassic.name():
        return SurveyStructureRadarClassic(question_repo)

    if survey_name.upper() == SurveyStructureSoftIA.name():
        return SurveyStructureSoftIA(question_repo)

    print("WARNING. Unkown: " + survey_name)
    return None


## Cache

class TestStructsCache(object):

    @staticmethod
    def _load_struct(struct_name):
        loader = SurveyStructureLoader()
        return loader.load_structure(struct_name + ".txt")

    @staticmethod
    def _load_questions_repo(struct):
        repo = load_questions(struct.questions_filename(), "polls")
        if repo is None:
            print("TestStructsCache::_load_questions_repo Error, questions repo is none, ", struct.questions_filename())
        struct.set_questions_repo(repo)

    @staticmethod
    def get_struct(struct_name):
        struct = Cache.get(struct_name)
        if struct is not None:
            return struct

        struct = TestStructsCache._load_struct(struct_name)
        if struct is None:
            print("TestStructsCache::get_struct - error loading ", struct_name)
            return None
        Cache.put(struct_name, struct)
        if struct.questions_repo() is None:
            TestStructsCache._load_questions_repo(struct)

        return struct