import numpy
import xlwings as xw
from tappraisal import load_questions, _get_full_filename
from analysis import RadarAnalysis, _load_answers


class Sheet(object):

    def __init__(self):
        self._wb = xw.Book()  # this will create a new workbook
        self._sht = self._wb.sheets[0]
        self._x = 1

        #self._areas = [[1, 1], [1, 8], [1, 14]]
        self._areas = [[1, 1], [10, 1], [1, 15]]
        self._current_area = 0
        self._y = self._areas[self._current_area][1]

    def _write(self, *content):
        self._sht.range((self._x, self._y)).value = content
        self._sht.range((self._x, self._y)).expand().value
        #self._x += len(content) + 1

    def set_y(self, y_val):
        self._y = y_val

    def writeln(self, *content):
        self._x = self._areas[self._current_area][0]

        #for c in content:
        self._write(content)
        #self._y += 1
        #self._x -= len(content) - 1
        self._areas[self._current_area][0] += 1
        self._y = self._areas[self._current_area][1]

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
        self._y = self._areas[self._current_area][1]

    def move_column(self, column_index):
        val = self._areas[column_index][0]
        for x_val in self._areas:
            if x_val[0] > val:
                val = x_val[0]
        self._areas[column_index][0] = val


def load_question_cat(repo):
    question_cat = dict()
    cat_questions = dict()

    for _, question in repo.as_dict().items():
        question_cat[question.code()] = question.category_name()
        if question.category_name() not in cat_questions:
            cat_questions[question.category_name()] = list()
        cat_questions[question.category_name()].append(question.code())

    return question_cat, cat_questions

# Este código ya está en TestResult
def filter_surveys(surveys, project, team):
    result = list()
    for survey in surveys:
        #print(survey)
        if survey.project_id() == project and survey.team_id() == team:
            #print(survey.year(), survey.month())
            if survey.year() == 2021 and survey.month() == 3:
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


def categories_titles(sheet):
    #sheet.move_column(0)
    sheet.set_column(1)
    sheet.writeln("")
    sheet.writeln("Respuestas por categorías")
    #sheet.set_y(2)
    sheet.writeln("Pregunta", "Respuestas adaptadas")


def analize_categories( surveys, sheet):
    answers = list()
    for survey in surveys:
        answers.extend(survey.answers())

    answers_org, answers_adp = get_answers_by_id(answers)
    answers_dict = {a.id(): a for a in answers}
    cats, cat_questions = load_question_cat(questions_repo)

    categories_titles(sheet)
    for cat, questions_id in cat_questions.items():
        print("--", cat)
        #sheet.set_y(1)
        #sheet.writeln(cat)
        answers_in_cat = list()
        for q_id in questions_id:
            if q_id in answers_dict:
                print(str(answers_dict[q_id].question_obj()), answers_adp[q_id])
                #sheet.set_y(2)
                answers_in_cat.extend(answers_adp[q_id])
                sheet.writeln(str(answers_dict[q_id].question_obj()), str(answers_adp[q_id]))

        if len(answers_in_cat) > 0:
            media = numpy.mean(answers_in_cat)
            desviacion = numpy.std(answers_in_cat)
            sheet.set_y(1)
            sheet.writeln(cat, "Respuestas:" + str(len(answers_in_cat)), "Media:" + str(media), "Desviación:" + str(desviacion))


# Valorar meterlas en la sheet.
def search_by_answer(results, answer_id, value):
    for survey in results.get_surveys():
        for answer in survey.answers():
            if answer.id() == answer_id and answer.original_answer() == value:
                #print("Survey: ", survey)
                print("+ Answers: ", survey.answers_as_string())
                break


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
project = "IWT2"
team = "T01"

"""
Ver cómo aplicamos esto.
https://statisticsbyjim.com/hypothesis-testing/t-tests-excel/#:~:text=t%20Critical%20values.-,If%20the%20p%2Dvalue%20is%20less%20than%20your%20significance%20level,means%20in%20only%20one%20direction.
"""
sheet = Sheet()
questions_repo = load_questions()
#print("GIMO-PD", "T01")
results = _load_answers(questions_repo, "IWT2_reports\\202103 - IWT2_Fixed")
surveys = filter_surveys(results.get_surveys(), project, team)
#print(surveys)


ra = RadarAnalysis()
#df = results.create_dataframe()
data_report = ra.generate_report(results, project, team)

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

print("Preguntas y respuestas:")
#q_a_v = results.question_answers_to_view(project, team, year="2021", month="03") # Year, month
sheet.set_column(2)
sheet.writeln("", "Id", "Pregunta", "Respuestas org", "Respuestas adap", "Media", "Desviación")

# Debería usar q_a_view de TestResult.
for key, _ in data_report.iter_factors():
    answer_obj, answer_original_anwers, answer_answers  = answers_by_factor(surveys, key)
    sheet.writeln(key)
    for a_id, answer in answer_obj.items():
        q_obj = answer.question_obj()
        means = numpy.mean(answer_answers[a_id])
        mads = numpy.std(answer_answers[a_id])
        #print(q_obj, answer_original_anwers[a_id])
        #print("Media", means , "Desviación estándar", mads)
        sheet.writeln("", q_obj.code(), q_obj.text(), str(answer_original_anwers[a_id]), str(answer_answers[a_id]), str(means), str(mads))

print("------------------------------")

print("Search A03 5:")
print("Búsquedas del informe IWT2:")
print("B08: 4")
search_by_answer(results, "B08", 4)
print("A02: 2")
search_by_answer(results, "A02", 2)
print("D06: 4")
search_by_answer(results, "D06", 4)
print("F05: 2")
search_by_answer(results, "F05", 2)

print("-----------------------------")
print("Categorías de cada factor")
#surveys = filter_surveys(results.get_surveys(), project, team)
#analize_categories(surveys, sheet)


sheet.save()
#profile()




