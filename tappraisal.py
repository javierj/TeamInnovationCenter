
import random


def _save_data(data):
    import datetime

    now = datetime.datetime.now()
    with open("data.txt", "a") as myfile:
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


class TestQuestion(object):

    def __init__(self, text, code="", valoration=""):
        self.text_question = text
        self._code = code

    def text(self):
        return self.text_question

    def category(self):
        return self._code[0]

    def code(self):
        return self._code


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

        if data.len_questions() == 9:
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

        question = TestQuestion("05. Duño en expresar ideas que se alejan de lo que piensan los demás")
        return question


class QuestionRepository(object):

    def __init__(self):
        self._questions = dict()

    def __str__(self):
        return str(self._questions)

    def append(self, question):
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

        self.append(question)

    # Unused
    def len_questions_in(self, category):
        if category not in self._questions:
            return 0
        return len(self._questions[category])

    def random_question_from(self, category):
        index = random.randint(0, len(self._questions[category])-1)
        print("Random question from", category, "max questions ", len(self._questions[category]), "index:", index)
        return self._questions[category][index]


def load_questions():
    repo = QuestionRepository()
    file_name = "./preguntas.txt"
    file = open(file_name)
    questions = list()
    for line in file:
        repo.commit_question(line)
    file.close()
    return repo
