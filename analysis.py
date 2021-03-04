import pandas as pd
import numpy
from tappraisal import _get_full_filename, get_test_structure
from view import QuestionsAnswersView, ReportView
from datetime import datetime


class DF(object):
    """
    Encapsulates a panda dataframe
    """

    def __init__(self):
        self._df = None

    @staticmethod
    def create(data):
        df = DF()
        df._df = pd.DataFrame(data)
        return df

    @staticmethod
    def c_dataframe(dataframe):
        df = DF()
        df._df = pd.DataFrame(dataframe)
        return df

    def copy(self):
        return DF.c_dataframe(self._df)

    def view(self, columns):
        df = DF()
        df._df = self._df[columns]
        return df

    def _set_month_year(self):
        if 'year' not in self._df:
            self._df['month'] = self._df['datetime'].apply(lambda x: datetime.fromisoformat(x).month)
            self._df['year'] = self._df['datetime'].apply(lambda x: datetime.fromisoformat(x).year)

    def f_year_month(self, year = None, month = None):
        if year is not None:
            year = int(year)
            month = int(month)

            self._set_month_year()
            #print("year", year, "month", month, "\n", df_tmp)
            self._df = self._df[(self._df['year'] == year) & (self._df['month'] == month)]
            #print("df_tmp", df_tmp)

    def f_by(self, column, value):
        #print("column", column, value)
        #print("Before", self._df)
        self._df = self._df[self._df[column] == value]
        #print("After", self._df)

    def f_project(self, id_proj, team_id):
        self.f_by('project_id', id_proj)
        self.f_by('team_id', team_id)

    def dataframe(self):
        return self._df

    def max_year_month(self):
        self._set_month_year()
        year = self._df['year'].max()
        month = self._df[self._df['year'] == year]['month'].max()
        return year, month

    def years_months(self, project_id, group_id):
        self.f_project(project_id, group_id)
        result = dict() # dict of dcit
        #self._set_month_year()
        datetimes = list(self._df['datetime'])
        for dt_string in datetimes:
            #print(datetime.fromisoformat(dt_string))
            dt = datetime.fromisoformat(dt_string)
            year = dt.year
            month = dt.month
            if year not in result:
                result[year] = dict()
            result[year][month] = month

        return {k:list(v) for k, v in result.items()}

    def size(self):
        return len(self._df)

    def means(self):
        ser_mean = self._df.mean(axis=0).round(2)
        return ser_mean.to_list(), numpy.format_float_positional(ser_mean.mean(axis=0), precision=3)

    def mads(self):
        ser_mean = self._df.mad(axis=0).round(2)
        return ser_mean.to_list(), numpy.format_float_positional(ser_mean.mean(axis=0), precision=3)

    def unique(self, key):
        return self._df[key].unique()

    def __str__(self):
        return str(self._df)


# Not in use
class Survey(object):

    def __init__(self, date_time, project_id, group_id):
        self._date_time = datetime.fromisoformat(date_time)
        self._project_id = project_id
        self._group_id = group_id
        self._a_qs = list()

    def project_id(self):
        return self._project_id

    def team_id(self):
        return self._group_id

    def year(self):
        return self._date_time.year

    def month(self):
        return self._date_time.month

    """
    @staticmethod
    def create_surveis(a_q_list):
        result = dict()
        for a_q in a_q_list:
            a_q_id =  a_q.id()
            if a_q_id not in result:
                result[a_q_id] = Survey()
            result[a_q_id].add_a_q(a_q)
        return result
    """

    def add_a_q(self, a_q):
        self._a_qs.append(a_q)

    def answers(self):
        return self._a_qs

    def __str__(self):
        return self._project_id +" / "+ self._group_id + " / " + str(self._date_time)


class AnsweredQuestion(object):

    def __init__(self, _answer, _original_answer):
        self._question_object = None
        self._original_answer = _original_answer
        self._adapted_answer = _answer
        self._factor = None
        self._survey_id = None

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

    def set_survey_id(self, _id):
        self._survey_id = _id

    def survey_id(self):
        return self._survey_id

    def set_factor(self, factor):
        self._factor = factor

    def factor(self):
        return self._factor

    def __str__(self):
        return self._factor+ ". " + str(self._question_object) + " " + str(self._original_answer) + "/" + str(self._adapted_answer)


class TestsResult(object):

    def __init__(self, questions_number = 9, q_repo = None):
        """
        :param questions_number:
        :param q_repo: tappraisal::QuestionRepository object
        """
        #self._questions = dict() # avoid duplicates
        self._answers = list()
        #self._original_answers = list()
        self._answers_id = list()
        self._q_repo = q_repo
        self._answers_number = questions_number
        self._url_answers = list() #A013B021C114...
        self._answered_questions = list()
        self._surveys = list() # Survey objects

    def url_answers(self):
        return self._url_answers

    def add_test_answer(self, result_line):
        """
        TODO: evitar el código duplicado
        :param result_line:
        :return:
        """
        data = result_line.split('/')
        self._url_answers.append(data[3])
        answers_list, original_answers_list = self._extract_answers(data[3]) # Cambiar esto

        if len(answers_list) < self._answers_number:
            #print("No hay las suficientes repsuestas")
            return

        # Prueba
        survey = Survey(data[0], data[1], data[2]) # not in use yet
        self._surveys.append(survey)
        answers_id_list = self._extract_ids(data[3])
        questions_dict = self._q_repo.as_dict()
        test_struct = get_test_structure()
        for answer_index in range(0, len(answers_list)):
            aq = AnsweredQuestion(answers_list[answer_index], original_answers_list[answer_index])
            aq.set_question(questions_dict[answers_id_list[answer_index]])
            aq.set_factor(test_struct[aq.id()[0]])
            #aq.set_survey_id(int(len( self._answered_questions ) / self._answers_number))
            self._answered_questions.append(aq) # Esto tiene que ser un survey
            survey.add_a_q(aq)

        # Todo evitar esta duplicidad.
        #
        answers_dict = {k: answers_list[k-1] for k in range(1, len(answers_list)+1) }
        answers_dict['datetime'] = data[0]
        answers_dict['project_id'] = data[1]
        answers_dict['team_id'] = data[2]
        self._answers.append(answers_dict)

        #answers_dict = {k: original_answers_list[k-1] for k in range(1, len(original_answers_list)+1) }
        #answers_dict['datetime'] = data[0]
        #answers_dict['project_id'] = data[1]
        #answers_dict['team_id'] = data[2]
        #print(answers_dict)
        #self._original_answers.append(answers_dict)

        answers_id_list = self._extract_ids(data[3])
        answers_dict = {k: answers_id_list[k - 1] for k in range(1, len(answers_id_list) + 1)}
        answers_dict['datetime'] = data[0]
        answers_dict['project_id'] = data[1]
        answers_dict['team_id'] = data[2]
        self._answers_id.append(answers_dict)


    def _get_answer_value(self, value_str, code):
        value = int(value_str)
        question = self._q_repo.get_question(code)
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

    def get_answered_questions_dict(self):
        return {answer.id(): answer for answer in self._answered_questions}

    """
    def get_answered_questions(self):
        return self._answered_questions
    """

    def get_surveys(self):
        return self._surveys

    def create_dataframe(self, project= None, group = None, data = None, year=None, month=None):
        """
        Creates a dataframe like this:

           1  2  3  4  5  6  7  8  9                    datetime project_id team_id
            0  5  5  5  5  5  5  5  5  4  2021-02-08 17:39:16.088294    GIMO-PD     T01
            1  5  5  1  5  5  3  4  5  5  2021-02-08 17:39:16.090003    GIMO-PD     T01

        :param project:
        :param group:
        :param data:
        :return:
        """
        if data is None:
            data = self._answers
            #print(data)

        df = DF.create(data)
        #print("DF:", df.dataframe())
        df.f_year_month(year, month)

        if project is None:
            return df.dataframe()
        df.f_by('project_id', project)
        #print("DF:", df.dataframe())

        if group is None:
            return df.dataframe()
        df.f_by('team_id', group)

        return df.dataframe()

    def create_ids_dataframe(self, project = None, group = None, year=None, month=None):
        """
        T    1    2    3    4  ...    9                    datetime project_id team_id
        0  A06  B08  C09  C12  ...  G01  2021-02-08 17:39:16.088294    GIMO-PD     T01
        1  A06  B07  C13  C12  ...  G02  2021-02-08 17:39:16.090003    GIMO-PD     T01

        :return: a dataframe with de ids of the questions instead their answer.
        """
        return self.create_dataframe(project, group, self._answers_id, year=year, month=month)

    """ # Deprecated
    def question_answers(self, project = None):
       
        :param project:
        :return: A dict. Keys are questions as string and values the list of original answers. Example:
            {'A06.Precondiciones. Estoy en este trabajo porque me gusta, no por el sueldo que me pagan.': [5, 5]}
   
        # Esto tiene que estar fuera
        test_struct = get_test_structure()
        df_tmp = self.create_ids_dataframe(project)
        df_ids = df_tmp[df_tmp.columns[0:self._answers_number]]

        #print(self._original_answers)

        df_tmp = self.create_dataframe(project, data= self._original_answers)
        #print(df_tmp)
        df_qs = df_tmp[df_tmp.columns[0:self._answers_number]]

        questions = self._q_repo.as_dict()
        question_answers = dict()
        for i in range(0,len(df_ids)):
            for j in range(0, 9):
                ansewr = df_qs.iloc[i].iat[j]
                id = df_ids.iloc[i].iat[j]
                #print(test_struct[questions[id].category()]+". "+questions[id].text()+str(ansewr))
                key = id+"."+test_struct[questions[id].category()]+". "+questions[id].text()
                if key in question_answers:
                    question_answers[key].append(ansewr)
                else:
                    question_answers[key] = list()
                    question_answers[key].append(ansewr)
        return question_answers
    """

    def question_answers_to_view(self, project, team, year=None, month=None):
        """
        Returns original ansers, true value for negative questions.
        :param project:
        :param team:
        :param year:
        :param month:
        :return:
        """
        questions_answers_view = QuestionsAnswersView()
        # Esto tiene que estar fuera
        test_struct = get_test_structure()
        answers_dict = self.get_answered_questions_dict()

        df_tmp = self.create_ids_dataframe(project, team, year, month)
        df_ids = df_tmp[df_tmp.columns[0:self._answers_number]]

        for i in range(0, len(df_ids)):
            for j in range(0, 9):
                id_answer = df_ids.iloc[i].iat[j]
                answer_obj = answers_dict[id_answer]
                questions_answers_view.add(answer_obj.question_obj(), test_struct[answer_obj.category()], answer_obj.original_answer())

        return questions_answers_view

    """
    def old_question_answers_to_view(self, project, team, year=None, month=None):

        :return: A View::QuestionsAnswersView object
        
        questions_answers_view = QuestionsAnswersView()
        # Esto tiene que estar fuera
        test_struct = get_test_structure()
        df_tmp = self.create_ids_dataframe(project, team, year, month)
        #print("df_tmp\n", df_tmp)
        df_ids = df_tmp[df_tmp.columns[0:self._answers_number]]
        #print("df_ids\n", df_ids)
        #print("_original_answers", self._original_answers)

        df_tmp = self.create_dataframe(project, group = team, year=year, month=month, data= self._original_answers)
        #print("project:", project, "\n", df_tmp)
        df_qs = df_tmp[df_tmp.columns[0:self._answers_number]]

        questions = self._q_repo.as_dict()
        for i in range(0,len(df_ids)):
            for j in range(0, 9):
                ansewr = df_qs.iloc[i].iat[j]
                id = df_ids.iloc[i].iat[j]
                #print("-", test_struct[questions[id].category()]+". "+questions[id].text()+str(ansewr))
                questions_answers_view.add(questions[id], test_struct[questions[id].category()],  ansewr)

        #print("questions_answers_view", questions_answers_view)
        return questions_answers_view
    """

    def original_answers(self):
        return self._original_answers

    def id_quesions(self):
        return self._answers_id

    def years_months(self, project_id, group_id):
        df = DF.c_dataframe(self.create_dataframe(project_id, group_id))
        return df.years_months(project_id, group_id)


class _FactorAnalisys(object):

    def _all_over(self, values, limit):
        for v in values:
            if v <= limit:
                return False
        return True

    def _all_under(self, values, limit):
        for v in values:
            if v >= limit:
                return False
        return True

    def stats_analysis(self, mean, mad):
        if self._all_over(mad, 1):
            if self._all_over(mean, 2.9):
                return "La media y la desviación indica que, aunque la mayoría del equipo tiene una buena opinión, hay una minoría de personas disconformes. Recomendamos conversaciones uno a uno para identificar a las personas con las valoraciones más bajas y concoer cuáles son sus motivos e intentar solucionarlos."
            if self._all_under(mean, 2.1):
                return "La media y la desviación indica que, aunque la mayoría del equipo se muestra disconforme, hay un pequeño número de personas que están contentas. Recomendamos alguna actividad de grupo dónde estas personas puedan compartir sus visiones y se planteen soluciones que cuenten con el consenso de todos, para intentar aumentar el número de personas con una valoración positiva."
            return "Los resultados son demasiado variables para poder extraer una conclusión. Recomendamos realizar actividades de equipo para marcar objetivos comunes y volver a repetir las encuestas para ver su progresión."
        if self._all_under(mad, 1):
            if self._all_over(mean, 2.5):
                return "La media indica que la mayoría de las respuestas están en los valores superiores. Continuad trabajando de esta manera."
            if  self._all_under(mean, 2.5):
                return "La media indica que la mayoría de las repsuestas están en los valores inferiores. Recomendamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo."
            return "El equipo está en un nivel intermedio, ni bien ni mal. Puedes aprovechar este estado para mejorar otro factor que esté por detrás o seguir trabajando en actividades para potenciar este factor."
        # Never reached.
        return "Las desviaciones indican que las preguntas de un mismo factor no son consistentes. Se recomienda repetir la encuesta en unas semanas."


class RadarAnalysis(object):

    def __init__(self):
        self._test_struct = {"Precondiciones": [1, 2], "Seguridad sicológica": [3, 4],
                             "Compromiso con el trabajo": [5, 6],
                             "Perfiles y responsabilidad": [7], "Resultados significativos": [8],
                             "Propósito e impacto": [9]}
        self._date_info= None
        self._factor_analisys = _FactorAnalisys()
        self._df = None
        self._results = None

    def _historic_data(self, factor_name, factor, report, df, years):
        #print("Years:", years)
        for year in years:
            df_tmp = df.copy()
            df_tmp.f_by('year', year)
            #print("months", df_tmp.unique('month'))
            months = df_tmp.unique('month')
            for month in months:
                df_month = df_tmp.copy()
                df_month.f_year_month(year, month)
                df_view = df_month.view(factor)
                report.with_factor(factor_name).add_historical_serie(year, month, df_view.size(), df_view.means()[1], df_view.mads()[1])

    def generate_report(self, results, id_proj, id_team, year = None, month = None):
        self._results = results
        df = results.create_dataframe(project=id_proj, group=id_team, year = year, month = month)
        return self.analyze(df, id_proj, id_team, year = None, month = None)

    # Move to inner
    def analyze(self, p_dataframe, id_proj, id_team, year = None, month = None):
        """
        Formato del dataframe de entrada
            1  2  3  4  5  6  7  8  9                    datetime project_id team_id
            0  0  3  2  0  1  2  5  3  2  2020-12-23 15:24:17.008097         01      01
            1  4  2  0  1  5  1  2  2  0  2021-01-09 20:19:47.775812         01      01
            2  5  5  5  5  0  0  5  5  5  2021-01-09 20:23:14.744930         01      01

        :param dataframe:
        :return: ReportView object
        """
        report = ReportView()
        df_org = DF.c_dataframe(p_dataframe)
        df_org.f_project(id_proj, id_team)
        df = df_org.copy()

        if year is None or month is None:
        # print("Is None")
            year, month = df.max_year_month()
            df.f_year_month(year, month)

        report.answers_len(df.size())
        # print("Dataframe: \n", dataframe)
        df_all = self._results.create_dataframe(project=id_proj, group=id_team)
        df_object = DF.c_dataframe(df_all)
        df_object._set_month_year()
        years = df_object.unique('year')
        for k, v in self._test_struct.items():
            # print("V ", v,"\n Dataframe: \n", dataframe)
            df_factor = df.view(v)
            # print("--", k)
            mean_list, mean = df_factor.means()
            report.with_factor(k).add_means(mean_list, mean)

            mad_list, mad = df_factor.mads()
            report.with_factor(k).add_mads(mad_list, mad)

            # print("Desviaciones medias:\n",ser_mad)
            report.with_factor(k).add_analysis(self._factor_analisys.stats_analysis(mean_list, mad_list))

            self._historic_data(k, v, report, df_object, years)

        report.year(year)
        report.month(month)

        return report


def _load_answers(questions_repo, filename = "data.txt"):
    answers = TestsResult(q_repo = questions_repo)

    file_name = _get_full_filename(filename)
    file = open(file_name, encoding="utf-8") # No: encoding="latin-1" encoding="ascii"
    for line in file:
        answers.add_test_answer(line)

    file.close()
    return answers


## Facade methods

def generate_report(test_results, id_proj, id_team, year, month):
    #df = test_results.create_dataframe()
    ra = RadarAnalysis()
    #data_report, date_info = ra.analyze(df, id_proj, id_team, year, month)
    #return ra.analyze(df, id_proj, id_team, year, month)
    return ra.generate_report(test_results, id_proj, id_team, year, month)

#Deprecated
"""
def questions_answers(test_results, id_proj, id_team):

    :param test_results:
    :param id_proj:
    :param id_team:
    :return: A list of strings like this:
        'G02.Impacto. Siento que tenemos los suficientes objetivos para poder estar centrados.:[5]'

    #test_results = _load_answers(questions_repo)
    q_a_dict = test_results.question_answers(id_proj)
    sorted_keys = sorted(q_a_dict.keys())
    q_a_list = list()
    for key in sorted_keys:
        q_a_list.append(key + ":" + str(q_a_dict[key]))
    return q_a_list
"""
