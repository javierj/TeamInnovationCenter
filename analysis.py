import pandas as pd
import numpy

from assistants import FactorAnalysisAssistant
from tappraisal import _get_full_filename, get_test_structure, load_questions, get_survey_structure
from view import QuestionsAnswersView, ReportView, HierarchicalGroups
from datetime import datetime


class Survey(object):

    def __init__(self, date_time, project_id, group_id):
        self._date_time = datetime.fromisoformat(date_time)
        self._project_id = project_id
        self._group_id = group_id
        self._a_qs = list() # list of AnsweredQuestion

    def date_time(self):
        return self._date_time

    def project_id(self):
        return self._project_id

    def team_id(self):
        return self._group_id

    def year(self):
        return self._date_time.year

    def month(self):
        return self._date_time.month

    def add_a_q(self, a_q):
        """
        :param a_q: object of type AnsweredQuestion
        :return: no return
        """
        self._a_qs.append(a_q)

    def answers(self):
        return self._a_qs

    """ Sólo se usa en analisis_clie
    def answers_as_string(self):
        result = ""
        for answer in self._a_qs:
            result += str(answer.id()) + ":" + str(answer.original_answer()) + " "
        return result
    """

    def __str__(self):
        return self._project_id +" / "+ self._group_id + " / " + str(self._date_time)


class AnsweredQuestion(object):

    def __init__(self, _answer, _original_answer):
        self._question_object = None
        self._original_answer = _original_answer
        self._adapted_answer = _answer
        self._factor = None

    def set_question(self, question_obj):
        self._question_object = question_obj

    def id(self):
        return self._question_object.code()

    def adapted_answer(self):
        return self._adapted_answer

    def category(self):
        return self._question_object.category()

    def question_obj(self):
        return self._question_object

    def original_answer(self):
        return self._original_answer

    def set_factor(self, factor):
        self._factor = factor

    def factor(self):
        return self._factor

    def __str__(self):
        return self._factor+ ". " + str(self._question_object) + " " + str(self._original_answer) + "/" + str(self._adapted_answer)


class TestsResult(object):

    def __init__(self, questions_number = 9, q_repo = None, _survey_struct = None): # _survey_struct es el nombre, cambiarlo
        self._answers = list()
        self._answers_id = list()
        self._q_repo = q_repo
        self._answers_number = questions_number
        self._answered_questions = list()
        self._surveys = list() # Survey objects
        if _survey_struct is None:
            self.test_struct = get_test_structure()
        else:
            self.test_struct = _survey_struct.get_test_structure()

    def add_test_answer(self, result_line):
        """
        TODO: quitar en un futuro
        :param result_line:
        :return:
        """
        #data = result_line.split('/')
        self.add_raw_answer(RawAnswer.create(result_line))

    def add_raw_answer(self, raw_answer):
        #self._url_answers.append(data[3])
        answers_list, original_answers_list = self._extract_answers(raw_answer.raw_data()) # Cambiar esto

        if len(answers_list) < self._answers_number:
            print("Answers ", len(answers_list), " Expected: ", self._answers_number, " Discarted: ", str(answers_list))
            return

        survey = Survey(raw_answer.date_time_str(), raw_answer.project_id(), raw_answer.team_id()) # not in use yet
        self._surveys.append(survey)
        answers_id_list = self._extract_ids(raw_answer.raw_data())
        questions_dict = self._q_repo.as_dict()

        for answer_index in range(0, len(answers_list)):
            aq = AnsweredQuestion(answers_list[answer_index], original_answers_list[answer_index])
            aq.set_question(questions_dict[answers_id_list[answer_index]])

            _key = aq.id()[0]
            if _key not in self.test_struct:
                print("Id ", aq.id())
                print("Key ", _key)
                print(" Not in ", self.test_struct)

            aq.set_factor(self.test_struct[_key])

            #aq.set_survey_id(int(len( self._answered_questions ) / self._answers_number))
            self._answered_questions.append(aq) # Esto tiene que ser un survey
            survey.add_a_q(aq)

        # Todo evitar esta duplicidad.
        #
        answers_dict = {k: answers_list[k-1] for k in range(1, len(answers_list)+1) }
        answers_dict['datetime'] =raw_answer.date_time_str()
        answers_dict['project_id'] = raw_answer.project_id()
        answers_dict['team_id'] = raw_answer.team_id()
        self._answers.append(answers_dict)

        answers_id_list = self._extract_ids(raw_answer.raw_data())
        answers_dict = {k: answers_id_list[k - 1] for k in range(1, len(answers_id_list) + 1)}
        answers_dict['datetime'] = raw_answer.date_time_str()
        answers_dict['project_id'] = raw_answer.project_id()
        answers_dict['team_id'] = raw_answer.team_id()
        self._answers_id.append(answers_dict)


    # Mover esto al repo - No puedo ir al report porque no sé su value
    def _get_answer_value(self, value_str, code):
        value = int(value_str)
        question = self._q_repo.get_question(code)
        if question is None:
            print("Question is None from value, code:", value, code)
        if question.is_positive():
            return value
        return 6 - value

    def _extract_tokens(self, q_url):
        answers = list()
        answer_len = int(len(q_url) / 4)
        for i in range(0, answer_len):
            tmp = q_url[(4 * i):(4 * i) + 4]
            answers.append(tmp) # Cambiar esto por si la pregunta es negativa
        return answers

    def _extract_answers(self, q_url):
        answers = list()
        org_answers = list()
        for token in self._extract_tokens(q_url):
            q_id = token[0:3]
            answer_value = self._get_answer_value(token[3], q_id)
            org_answer_value = int(token[3])

            answers.append(answer_value) # Cambiar esto por si la pregunta es negativa
            org_answers.append(org_answer_value) # Cambiar esto por si la pregunta es negativa
        return answers, org_answers

    def _extract_ids(self, q_url):
        tokens = self._extract_tokens(q_url)
        return [token[0:3] for token in tokens]

    def __str__(self):
        return str(self._answers)

    def get_surveys(self):
        return self._surveys

    def question_answers_to_view(self, project, team, year=None, month=None):
        """
        Returns  answers objects
        WARNING. this method does not filter by project or group.
        you shouls use load_results..(), so results are filtered
        :return: questions_answers_view object
        """
        questions_answers_view = QuestionsAnswersView()

        filtered_surveys = self._surveys
        if year is not None:
            filtered_surveys = list()
            for survey in self._surveys:
                if str(survey.year()) == str(year) and str(survey.month()) == str(month):
                    filtered_surveys.append(survey)

        for survey in filtered_surveys:
            for answer in survey.answers():
                questions_answers_view.add(answer.question_obj(), answer.factor(), answer.original_answer())

        return questions_answers_view



class HistoricDataAnalysis:

    def _create_data_for_dataframe(self, surveys):
        data = list()
        num_questions  = len(surveys[0].answers())
        for survey in surveys:
            s_list = list()
            s_list.append(survey.year())
            s_list.append(survey.month())
            #s_list.append("Radar-9")
            for index in range(0, num_questions):
                answer = survey.answers()[index]
                s_list.append(answer.adapted_answer())
                #factors.begin().add_group(answer.factor()).add_in_bag(index)
            data.append(s_list)
        return data

    def _create_column_for_dataframe(self, surveys):
        columns = ['year', 'month']
        questions = len(surveys[0].answers())
        for ind in range(0, questions):
            columns.append((ind+1))
        return columns

    def historical_data(self, results, survey_struct): # Necesito los dos objetos ?
        h_data = HierarchicalGroups()

        surveys = results.get_surveys()
        if len(surveys) == 0:
            return h_data

        data = self._create_data_for_dataframe(surveys)
        columns = self._create_column_for_dataframe(surveys)

        #print(data)
        #print(columns)
        df = pd.DataFrame(data=data, columns=columns)
        #print(df)
        df_grouped = df.groupby(['year', 'month'])

        data_groups = survey_struct.get_groups()

        for name, group in df_grouped:
            # print('ID: ' + str(name))
            year = group['year'].iloc[0]
            month = group['month'].iloc[0]

            #print(year, month)
            for group_name, column_list in data_groups.items():
                #print(year, month, group_name, column_list, group)
                #print(group[column_list])
                #print("Mean", group[column_list].mean())
                #print("Final mean", group[column_list].mean().mean())
                mean = group[column_list].mean().mean()
                mad = group[column_list].mad().mean() # Cambiar
                h_data.begin().add_group(year).add_group(month).add_value(len(group))
                h_data.begin().add_group(year).add_group(month).add_group(group_name).add_value((mean, mad))

        #print("h_data \n", h_data)
        return h_data


class RadarAnalysis(object):

    def __init__(self, survey_structure):
        """

        :param survey_structure: stringwith the name of the survey
        """
        self._survey_structure = survey_structure
        self._factor_analisys = FactorAnalysisAssistant()

    def _historical_data(self, results):
        d_a = HistoricDataAnalysis()
        return d_a.historical_data(results, self._survey_structure)

    def _add_historical_data(self, report, h_data):
        #print("hist_data:", h_data)
        years = h_data.begin().keys()
        for year in years:
            months = h_data.begin().group(year).keys()
            for month in months:
                answers = h_data.begin().group(year).group(month).value()
                factors = h_data.begin().group(year).group(month).keys()
                for factor_name in factors:
                    stats = h_data.begin().group(year).group(month).group(factor_name).value()
                    mean = stats[0]
                    mad = stats[1]
                    report.with_factor(factor_name).add_historical_serie(year, month, answers, mean, mad)

    def generate_report(self, results, id_proj, id_team, year, month):
        year = int(year)
        month = int(month)
        historical_data = self._historical_data(results)

        report = ReportView()
        report.project_id(id_proj)
        report.group_id(id_team)
        report.struct_name(self._survey_structure.name())

        if year not in historical_data.begin().keys():
            return report
        if month not in historical_data.begin().group(year).keys():
            return report

        #print(year, month)
        #print(historical_data)
        report.answers_len(historical_data.begin().group(year).group(month).value())

        #factor_data = historical_data.begin().group(year).group(month)
        keys = historical_data.begin().group(year).group(month).keys()

        for factor in keys:
            #print(keys, factor)
            stats = historical_data.begin().group(year).group(month).group(factor).value()
            mean = stats[0]
            mad = stats[1]
            report.with_factor(factor).add_means([mean], mean)
            report.with_factor(factor).add_mads([mad], mad)
            report.with_factor(factor).add_analysis(self._factor_analisys.stats_analysis([mean], [mad]))

        report.year(year)
        report.month(month)

        # Meter los datos históricos en el report.
        self._add_historical_data(report, historical_data)

        return report


class RawAnswer(object):
    def __init__(self):
        self._test_type = None
        self._date_time = None
        self._project_id = None
        self._team_id = None
        self._raw_data = None
        #self._date_time = None

    @staticmethod
    def create(line):
        raw_answer = RawAnswer()
        data = line.split('/')
        if len(data) >= 5:
            raw_answer._test_type = data[4].strip()
        else:
            raw_answer._test_type = "RADAR-9"
        raw_answer._date_time = datetime.fromisoformat(data[0])
        #print(data[0], raw_answer._date_time)
        #raw_answer._date_time = data[0]
        raw_answer._project_id = data[1]
        raw_answer._team_id = data[2]
        raw_answer._raw_data = data[3]
        return raw_answer

    def project_id(self):
        return self._project_id

    def team_id(self):
        return self._team_id

    def year(self):
        return self._date_time.year

    def month(self):
        return self._date_time.month

    def test_type(self):
        return self._test_type

    def raw_data(self):
        return self._raw_data

    def date_time_str(self):
        return str(self._date_time)


#####

class CVSResults(object):

    def _ids_from_answer(self, survey):
        answer_ids = dict()
        for answer in survey.answers():
            answer_ids[answer.id()] = answer.original_answer()
        return answer_ids

    def _header(self, questions_list):
        cvs_content = "Question, Year, Month, "
        #cvs_content = "Question, "
        for q_id in questions_list:
            cvs_content += str(q_id) + ", "
        cvs_content += '\n'
        return cvs_content

    def _results_to_cvs(self, survey_list, questions_list):
        cvs_content = ""
        index = 1
        for survey in survey_list:
            answer_ids = self._ids_from_answer(survey)
            cvs_line = str(index) + ", " + str(survey.year()) + ", " + str(survey.month()) + ", "
            for question_id in questions_list:
                if question_id in answer_ids:
                    cvs_line += str(answer_ids[question_id]) + ", "
                else:
                    cvs_line += ", "
            cvs_content += cvs_line + '\n'
            index += 1
        return cvs_content

    def results_to_cvs(self, poll_struct, test_results):
        questions_repo = poll_struct.questions_repo()

        if questions_repo is None:
            print("CVSResults, error obtaining the ids from questions.")

        questions_id = questions_repo.as_dict().keys()

        return self._header(questions_id) + self._results_to_cvs(test_results.get_surveys(), questions_id)







## Facade methods

# Depretace, intenta no usarla
# Usa load_test_results en su lugar
def _load_answers(questions_repo, filename = "data.txt"):
    answers = TestsResult(q_repo = questions_repo)
    file_name = _get_full_filename(filename)
    file = open(file_name, encoding="utf-8") # No: encoding="latin-1" encoding="ascii"
    for line in file:
        answers.add_test_answer(line)

    file.close()
    return answers


def generate_report(test_results, id_proj, id_team, year, month, survey = "RADAR9"):
    ra = RadarAnalysis(get_survey_structure(load_questions(), survey_name= survey)) # Quitar estas referencias para que venga de fuera
    return ra.generate_report(test_results, id_proj, id_team, year, month)


def surveys_overview(project_id, team_id, filename = "data.txt"):
    s_overview = HierarchicalGroups()
    file_name = _get_full_filename(filename)
    file = open(file_name, encoding="utf-8") # No: encoding="latin-1" encoding="ascii"
    for line in file:
        raw_answer = RawAnswer.create(line)
        if project_id == raw_answer.project_id() and team_id == raw_answer.team_id():
            s_overview.begin().add_group(raw_answer.year()).add_group(raw_answer.month()).add_group(raw_answer.test_type()).inc_counter()
            #surveys_overview.begin().add_group(survey.year()).add_group(MONTHS[survey.month()]).add_group(test_type).inc_counter()
            # si lo pongo con nombre, en vez de número, no genera bien la URL para acceder al report.

    file.close()
    return s_overview


def load_test_results(questions_repo, project_id, team_id, survey_name="RADAR-9", filename = "data.txt"):
    survey_struct = get_survey_structure(questions_repo, survey_name)
    results = TestsResult(q_repo = questions_repo,
                          questions_number= survey_struct.num_of_questions(),
                          _survey_struct = survey_struct)
    file_name = _get_full_filename(filename)
    file = open(file_name, encoding="utf-8") # No: encoding="latin-1" encoding="ascii"
    for line in file:
        raw_answer = RawAnswer.create(line)
        if project_id == raw_answer.project_id() \
                and team_id == raw_answer.team_id() \
                and raw_answer.test_type().upper() == survey_name.upper():
            results.add_raw_answer(raw_answer)
        else:
            #print("project_id == raw_answer.project_id()", project_id, raw_answer.project_id())
            #print("team_id == raw_answer.team_id()", team_id , raw_answer.team_id())
            #print("raw_answer.test_type() == survey_type", raw_answer.test_type(), survey_name)
            #print("Descartada: ", line)
            pass

    file.close()
    #print("Surveys: \n", results.get_surveys())
    return results
