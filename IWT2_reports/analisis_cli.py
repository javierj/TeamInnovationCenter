import pandas as pd
import numpy
import xlwings as xw
from tappraisal import load_questions, _get_full_filename
from analysis import RadarAnalysis, _load_answers, DF


class Sheet(object):

    def __init__(self):
        self._wb = xw.Book()  # this will create a new workbook
        self._sht = self._wb.sheets[0]
        self._x = 1
        self._y = 1
        #self._areas = [[1, 1], [1, 8], [1, 14]]
        self._areas = [[1, 1], [10, 1], [1, 15]]
        self._current_area = 0

    def _write(self, *content):
        self._sht.range((self._x, self._y)).value = content
        self._sht.range((self._x, self._y)).expand().value
        #self._x += len(content) + 1

    def writeln(self, *content):
        self._x = self._areas[self._current_area][0]
        self._y = self._areas[self._current_area][1]
        #for c in content:
        self._write(content)
        #self._y += 1
        #self._x -= len(content) - 1
        self._areas[self._current_area][0] += 1

    def writelst(self, conten_list):
        self._x = self._areas[self._current_area][0]
        self._y = self._areas[self._current_area][1]
        for c in conten_list:
            self._write(c)
            self._y += 1
        self._areas[self._current_area][0] += 1

    def save(self):
        self._wb.save('demo.xlsx')

    def set_column(self, column_index):
        self._current_area = column_index

    def move_column(self, column_index):
        val = self._areas[column_index][0]
        for x_val in self._areas:
            if x_val[0] > val:
                val = x_val[0]
        self._areas[column_index][0] = val


def profile():
    print("--- Profilinig ----")
    import cProfile
    import pstats
    # from pstats import SortKey, pstats
    import io
    # cProfile.run('ra.analyze(df, "01", "01")')
    pr = cProfile.Profile()
    pr.enable()
    ra.analyze(df, "01", "01")
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s)
    ps.sort_stats(pstats.SortKey.CUMULATIVE).print_stats(10)
    print(s.getvalue())
    # 20210226 - 190686 function calls (187522 primitive calls) in 0.102 seconds
    # 20210227 - 208663 function calls (205144 primitive calls) in 0.127 seconds
    # 20210228 - 208561 function calls (205024 primitive calls) in 0.115 seconds
    # 20210302 - 263969 function calls (259795 primitive calls) in 0.147 seconds
    # 20210304 - 263969 function calls (259795 primitive calls) in 0.147 seconds
    # 20210304 - 216839 function calls (213195 primitive calls) in 0.117 seconds


def load_question_cat(): # TODO Añadir esto al main.
    file_name = _get_full_filename("preguntas.txt")
    file = open(file_name, encoding="utf-8") # No: encoding="latin-1" encoding="ascii"
    question_cat = dict()
    cat_questions = dict()
    cat = ""
    for line in file:
        s_line = line.strip()
        if s_line.startswith("#-"):
            tokens = s_line.split('#')
            #print("tokens", tokens)
            cat = tokens[1]+'.'+tokens[2]
        if s_line == "" or '#' in s_line:
            continue

        elements = s_line.split(':')
        code = elements[0].strip()
        question_cat[code] = cat
        if cat not in cat_questions:
            cat_questions[cat] = list()
        cat_questions[cat].append(code)

    file.close()

    return question_cat, cat_questions


# Deprecated
def analize_categories(result):
    q_a_v = result.question_answers_to_view("01", "01", year=2021, month=2)
    cats, cat_questions = load_question_cat()
    #answers_org, answers_adp = results.get_answers_by_id()

    for cat, questions_id in cat_questions.items():
        #print("questions_id", questions_id)
        print("--", cat)
        answers_concat = list()
        for id in questions_id:
            #print(q_a_v)
            if q_a_v.contains(id):
                #print(id, q_a_v.question_text(id), q_a_v.question_answers(id), answers_org[id], answers_adp[id])
                print(id, q_a_v.question_text(id), q_a_v.question_answers(id))
                answers_concat.extend(q_a_v.question_answers(id))
        if len(answers_concat) > 0:
            df = DF.create({cat: answers_concat})
            print("Incorrectos - Media:", df.means(), "Desviación:", df.mads())
            # Estos datos son incorrectos porque usa q_a_v y ahí están las repsuestas originales, no adaptadas


def filter_surveys(surveys):
    result = list()
    for survey in surveys:
        #print(survey)
        if survey.project_id() == "01" and survey.team_id() == "01":
            #print(survey.year(), survey.month())
            if survey.year() == 2021 and survey.month() == 2:
                #print(survey)
                result.append(survey)
    return result


def get_answers_by_id(answers):
    result_original = dict()
    result_adapted = dict()
    for a_question in answers:
        key = a_question.id()
        if key not in result_original:
            result_original[key] = list()
            result_adapted[key] = list()
        result_original[key].append(a_question.original_answer())
        result_adapted[key].append(a_question.adapted_answer())
    return result_original, result_adapted


def analize_categories_2(results):
    surveys = filter_surveys(results.get_surveys())
    answers = list()
    for survey in surveys:
        answers.extend(survey.answers())

    answers_org, answers_adp = get_answers_by_id(answers)
    answers_dict = {a.id(): a for a in answers}
    cats, cat_questions = load_question_cat()

    for cat, questions_id in cat_questions.items():
        print("--", cat)
        for q_id in questions_id:
            if q_id in answers_dict:
                #print("questions_id", questions_id)
                print(str(answers_dict[q_id].question_obj()), answers_org[q_id], answers_adp[q_id])

        """
        answers_concat = list()
        for id in questions_id:
            #print(q_a_v)
            if q_a_v.contains(id):
                print(id, q_a_v.question_text(id), q_a_v.question_answers(id))
                answers_concat.extend(q_a_v.question_answers(id))
        if len(answers_concat) > 0:
            df = DF.create({cat: answers_concat})
            print("Incorrectos - Media:", df.means(), "Desviación:", df.mads())
            # Estos datos son incorrectos porque usa q_a_v y ahí están las repsuestas originales, no adaptadas
        """

# Deprecated
def search_by_answer(results, answer):
    urls = results.url_answers()
    for url in urls:
        if answer in url:
            print(answer, "in", url)

def search_by_answer_2(results, answer_id, value):
    ansers = results.get_answered_questions()
    survey_id = list()
    for answer in ansers:
        #print(answer.id(), answer_id, answer.original_answer(), value)
        #print(type(answer.id()), type(answer_id), type(answer.original_answer()), type(value))
        if answer.id() == answer_id and answer.original_answer() == value:
            survey_id.append(answer.survey_id())

    #print(survey_id)
    for s_id in survey_id:
        print("Survey", s_id)
        for answer in ansers:
            if answer.survey_id() == s_id:
                print(answer)





def answers_by_factor(surveys, factor):
    answer_answers = dict()
    answer_original_anwers = dict()
    answer_obj = dict()
    for survey in surveys:
        for answer in survey.answers():  # .answers_by_cat(key):
            if factor == answer.factor():
                a_id = answer.id()
                answer_obj[a_id] = answer
                if a_id not in answer_answers:
                    answer_answers[a_id] = list()
                answer_answers[a_id].append(answer.adapted_answer())
                if a_id not in answer_original_anwers:
                    answer_original_anwers[a_id] = list()
                answer_original_anwers[a_id].append(answer.original_answer())
    return answer_obj, answer_original_anwers, answer_answers


# Main

"""
Ver cómo aplicamos esto.
https://statisticsbyjim.com/hypothesis-testing/t-tests-excel/#:~:text=t%20Critical%20values.-,If%20the%20p%2Dvalue%20is%20less%20than%20your%20significance%20level,means%20in%20only%20one%20direction.
"""
sheet = Sheet()
questions_repo = load_questions()
#results = _load_answers(questions_repo, "IWT2_reports\\022021 - GIMO-PD.txt")
#print(results.create_ids_dataframe())
#results = _load_answers(questions_repo, "IWT2_reports\\072021 - APPIMEDEA.txt")
#results = _load_answers(questions_repo, "IWT2_reports\\012021 - AIRPA")
#results = _load_answers(questions_repo, "IWT2_reports\\022021 - G7D.txt")
results = _load_answers(questions_repo, "IWT2_reports\\data.txt")
surveys = filter_surveys(results.get_surveys())
#print(surveys)


ra = RadarAnalysis()
df = results.create_dataframe()
data_report = ra.generate_report(results, "01", "01")

print("-----------------------")
print("Surveys analizadas:", len(surveys))
sheet.writeln("Surveys analizadas:", len(surveys))
sheet.writeln("Factor", "Media", "Desviación final", "Medias x pregunta", "Desviaciones x preguntas", )
sheet.set_column(1)
sheet.writeln("Datos históricos:")
sheet.writeln("Fecha", "Respuestas", "Media", "Desviación")
sheet.set_column(0)
for key, factor in data_report.iter_factors():
    print(key)
    print("Means:", factor.means(), "MADS:", factor.mads(), "Media means:", factor.total_mean(), "Media mads:", factor.total_mad())
    sheet.writeln(key, factor.total_mean(), factor.total_mad(), str(factor.means()), str(factor.mads()))

    print("Datos históricos:") # No sé si me aporta mostrarlos en pantalla, ya los analizo en la Excel.
    sheet.set_column(1)
    sheet.writeln(key+":")
    for index in range(0, factor.historical_series()):
        #print(factor.get_historical_serie(index))
        serie = factor.get_historical_serie(index)
        sheet.writeln(str(serie[0]) + '-' + str(serie[1]), serie[2], serie[3], serie[4] )
        #pass
    sheet.set_column(0)

print("------------------------------")

# Lo repito para qu se vea más claro
print("Preguntas y respuestas:")
q_a_v = results.question_answers_to_view("01", "01", year="2021", month="02") # Year, month
sheet.set_column(2)
sheet.writeln("Id", "Pregunta", "Respuestas", "Media", "Mediana")

for key, _ in data_report.iter_factors():
    answer_obj, answer_original_anwers, answer_answers  = answers_by_factor(surveys, key)

    for a_id, answer in answer_obj.items():
        q_obj = answer.question_obj()
        means = numpy.mean(answer_answers[a_id])
        mads = numpy.std(answer_answers[a_id])
        print(q_obj, answer_original_anwers[a_id])
        print("Media", means , "Desviación estándar", mads)
        sheet.writeln(q_obj.code(), q_obj.text(), str(answer_original_anwers[a_id]), str(means), str(mads))

    """
    for question_id in q_a_v.questions_id(key):
        #print(question_id)
        print(key, question_id, q_a_v.question_text(question_id), q_a_v.question_answers(question_id))
        sheet.writeln(question_id, q_a_v.question_text(question_id), str(q_a_v.question_answers(question_id)))
        # Estos datos NO son correctos porque tenemos als repsuestas originales
        # sin aplicar la modifcación negativa
        # Debería pode robtener los dos conjuntos de respuestas
        print("Incorrecto - Media", numpy.mean(q_a_v.question_answers(question_id)), "Desviación estándar", numpy.std(q_a_v.question_answers(question_id)))
        # Ver cómo solucionar esto
"""
print("------------------------------")

print("Search A03 5:")
#search_by_answer(results, "A035")
#search_by_answer_2(results, "A03", 5) # Rehaer

print("-----------------------------")
analize_categories(results)
analize_categories_2(results)


sheet.save()
profile()

"""
import datetime
print(('month' in df))
df['month'] = df['datetime'].apply(lambda x: datetime.datetime.fromisoformat(x).month)
df['year'] = df['datetime'].apply(lambda x: datetime.datetime.fromisoformat(x).year)
print(('month' in df))

print("Years", df['year'].unique())
for year in df['year'].unique():
    df_month = df[ df['year'] == year]
    print(year, ":", df_month.month.unique())

print("-------------------------------------")
df_grouped = df.groupby(["year", "month"])
print("index", df_grouped.as_index)

df_means = df_grouped.mean()
print("df", df_means, type(df_means))
print(df_means.index)
for index in df_means.index:
    print(index)
df_reset = df_means.reset_index()
for i in range(0, len(df_reset)):
    print(i, df_reset.iloc[i])
    print(i, df_reset.iloc[i]['year'])
"""



