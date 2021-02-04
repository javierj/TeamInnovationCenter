
import random

# Candidato a refactorizarlo a otro sitio.
def _get_full_filename(filename):
    import os
    base_path = os.path.dirname(os.path.abspath(__file__))
    my_path = os.path.join(base_path, filename)
    return my_path


def _save_data(data):
    import datetime

    now = datetime.datetime.now()
    filename = _get_full_filename("data.txt")
    with open(filename, "a") as myfile:
        myfile.write(str(now)+"/"+str(data) + "\n")


# renombrar a WebTestInfo o algo así
# como lo crea Bottle, es pisible que tenga que estar en su módulo y no aquí.
class TestData(object):

    # ToDo
    def __init__(self, org_id, project_id, questions):
        self._answers = 0
        self._questions = dict()
        self._parse_questions_url(questions)
        self._url_questions = questions
        self._org_id = org_id
        self._project_id = project_id

    def __str__(self):
        return self._org_id+"/" + self._project_id+"/" + self._url_questions

    def _parse_questions_url(self, q_url):
        question_answer = dict()
        self._answers = 0

        answer_len = int( len(q_url) / 4 )
        for i in range(0, answer_len):
            tmp = q_url[(4*i):(4*i)+4]
            q_id = tmp[0:3]
            answer = tmp[3]
            category = q_id[0]

            if category not in self._questions:
                self._questions[category] = list()
            self._questions[category].append(q_id[1:3])
            self._answers += 1

    def len_questions(self):
        return self._answers

    def len_questions_in(self, category):
        if category not in self._questions:
            return 0
        return len(self._questions[category])

    def questions_as_list(self):
        """
        Not in use. Analysis duplicates this code.
        :return:
        """
        question_list = list()
        for _, value in self._questions:
            question_list.extend(value)
        return question_list


class TestQuestion(object):

    def __init__(self, text, code="", valoration=""):
        self.text_question = text
        self._code = code
        self._valoration=valoration

    def text(self):
        return self.text_question

    def category(self):
        return self._code[0]

    def code(self):
        return self._code

    def is_positive(self):
        return self._valoration == "P"


class AppraisalDirector(object):

    def __init__(self, repo = None):
        pass
        self._questions_repo = repo

    def next_question(self, data):
        """
        Veo las pregunats que ya se han hecho y busco y envío la siguiente pregunta a preguntar en el test
        o None si ya se han terminado las preguntas.
        :param data:
        :return:
        """

        if data.len_questions() == 9: # 9 preguntas
            _save_data(data)
            return None

        if data.len_questions_in("A") == 0:
            return self._questions_repo.random_question_from("A")
        if data.len_questions_in("B") == 0:
            return self._questions_repo.random_question_from("B")
        if data.len_questions_in("C") < 2:
            return self._questions_repo.random_question_from("C")
        if data.len_questions_in("D") < 2:
            return self._questions_repo.random_question_from("D")
        if data.len_questions_in("E") < 1:
            return self._questions_repo.random_question_from("E")
        if data.len_questions_in("F") < 1:
            return self._questions_repo.random_question_from("F")
        if data.len_questions_in("G") < 1:
            return self._questions_repo.random_question_from("G")

        question = TestQuestion("05. ERROR")
        return question

    # this method if a bad smell but botttle needs it to call bottle.
    def get_repo(self):
        return self._questions_repo


class QuestionRepository(object):

    def __init__(self):
        self._questions = dict()

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
        if '#' in s_line:
            return None

        elements = s_line.split(':')
        question = TestQuestion(code=elements[0].strip(), text=elements[1].strip(), valoration=elements[2].strip())

        self._append(question)

    def random_question_from(self, category):
        index = random.randint(0, len(self._questions[category])-1)
        print("Random question from", category, "max questions ", len(self._questions[category]), "index:", index)
        return self._questions[category][index]

    def get_question(self, category, code):
        #print("Searching:", category, code)
        questions = self._questions[category]
        for question in questions:
            #print("Code found: ", question.code())
            if question.code() == code:
                return question
        return None

    def as_dict(self):
        """
        :return: A dict Code :  Questionobject.
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
    questions = list()
    for line in file:
        repo.commit_question(line)
        #print("áéÍÓñÑ: " + line)
    file.close()

    return repo
