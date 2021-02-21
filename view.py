

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
        return self._his_year[index], self._his_month[index], self._his_answers_num[index], self._his_mean[index], self._his_mad[index]

class ReportView(object):

    def __init__(self):
        self._factors = dict()
        self._year = None
        self._month = None
        self._answers_len = None

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

    def answers_len(self, answers_num):
        self._answers_len = answers_num

    def get_year(self):
        return self._year

    def get_month(self):
        return self._month

    def get_answers_len(self):
        return self._answers_len

    def has_answers(self):
        if len(self._factors) == 0:
            return False
        value = next(iter(self._factors.values()))
        return value.total_mean() is not None

    def __str__(self):
        return str(self._factors)