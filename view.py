

class QuestionsAnswersView(object):

    def __init__(self):
        self._cats = dict()
        self._texts = dict()
        self._answers = dict()

    def add(self, question_id, questions_category, question_text, answer):
        if questions_category not in self._cats:
            self._cats[questions_category] = dict()
        self._cats[questions_category][question_id] = question_id
        self._texts[question_id] = question_text
        if question_id not in self._answers:
            self._answers[question_id] = list()
        self._answers[question_id].append(answer)

    def categories(self):
        return list(self._cats.keys())

    def questions_id(self, category):
        return list(self._cats[category].keys())

    def question_text(self, p_id):
        return self._texts[p_id]

    def question_answers(self, p_id):
        return self._answers[p_id]

    def has_answers(self):
        return len(self._cats) > 0

    def __str__(self):
        return str(self._cats)