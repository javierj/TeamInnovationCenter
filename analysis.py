import pandas as pd
from tappraisal import _get_full_filename, load_questions, get_test_structure
from view import QuestionsAnswersView
from datetime import datetime


class TestsResult(object):

    def __init__(self, questions_number = 9, q_repo = None):
        self._questions = dict() # avoid duplicates
        self._answers = list()
        self._original_answers = list()
        self._answers_id = list()
        self._q_repo = q_repo
        self._answers_number = questions_number

    def add_test_answer(self, result_line):
        """
        TODO: evitar el código duplicado
        :param result_line:
        :return:
        """
        data = result_line.split('/')
        answers_list = self._extract_answers(data[3])
        original_answers_list = self._extract_original_answers(data[3])

        if len(answers_list) < self._answers_number:
            #print("No hay las suficientes repsuestas")
            return

        # Todo evitar esta duplicidad.
        #
        answers_dict = {k: answers_list[k-1] for k in range(1, len(answers_list)+1) }
        answers_dict['datetime'] = data[0]
        answers_dict['project_id'] = data[1]
        answers_dict['team_id'] = data[2]
        self._answers.append(answers_dict)

        answers_dict = {k: original_answers_list[k-1] for k in range(1, len(original_answers_list)+1) }
        answers_dict['datetime'] = data[0]
        answers_dict['project_id'] = data[1]
        answers_dict['team_id'] = data[2]
        #print(answers_dict)
        self._original_answers.append(answers_dict)

        answers_id_list = self._extract_ids(data[3])
        answers_dict = {k: answers_id_list[k - 1] for k in range(1, len(answers_id_list) + 1)}
        answers_dict['datetime'] = data[0]
        answers_dict['project_id'] = data[1]
        answers_dict['team_id'] = data[2]
        self._answers_id.append(answers_dict)

    def _get_answer_value(self, value_str, category, code):
        value = int(value_str)
        question = self._q_repo.get_question(category, code)
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
        for token in self._extract_tokens(q_url):
            q_id = token[0:3]
            category = q_id[0]
            answer_value = self._get_answer_value(token[3], category, q_id)
            #answer_value = token[3]

            if q_id not in self._questions:
                self._questions[q_id] = list()
            self._questions[q_id].append(answer_value)

            answers.append(answer_value) # Cambiar esto por si la pregunta es negativa
        return answers

    def _extract_original_answers(self, q_url):
        """
        TODO. evitar esta duplicidad de código
        :param q_url:
        :return:
        """
        answers = list()
        for token in self._extract_tokens(q_url):
            q_id = token[0:3]
            category = q_id[0]
            #answer_value = self._get_answer_value(token[3], category, q_id)
            answer_value = int(token[3])

            if q_id not in self._questions:
                self._questions[q_id] = list()
            self._questions[q_id].append(answer_value)

            answers.append(answer_value) # Cambiar esto por si la pregunta es negativa
        return answers

    def _extract_ids(self, q_url):
        tokens = self._extract_tokens(q_url)
        return [token[0:3] for token in tokens]

    def __str__(self):
        return str(self._answers)

    def create_dataframe(self, project= None, group = None, data = None):
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
        df_tmp = pd.DataFrame(data)
        if project is None:
            return df_tmp

        df_tmp = df_tmp[ df_tmp['project_id'] == project ]

        if group is None:
            return df_tmp

        return df_tmp[ df_tmp['team_id'] == group ]

    def create_ids_dataframe(self, project = None, group = None):
        """
        T    1    2    3    4  ...    9                    datetime project_id team_id
0  A06  B08  C09  C12  ...  G01  2021-02-08 17:39:16.088294    GIMO-PD     T01
1  A06  B07  C13  C12  ...  G02  2021-02-08 17:39:16.090003    GIMO-PD     T01

        :return: a dataframe with de ids of the questions instead their answer.
        """

        #df_tmp = pd.DataFrame(self._answers_id)
        #if project is None:
            #return df_tmp
        #return df_tmp[df_tmp['project_id'] == project]
        return self.create_dataframe(project, group, self._answers_id)

    def question_answers(self, project = None):
        """
        :param project:
        :return: A dict. Keys are questions as string and values the list of original answers. Example:
            {'A06.Precondiciones. Estoy en este trabajo porque me gusta, no por el sueldo que me pagan.': [5, 5]}
        """
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

    def question_answers_to_view(self, project, team):
        """
        :param project:
        :return:
        """
        questions_answers_view = QuestionsAnswersView()
        # Esto tiene que estar fuera
        test_struct = get_test_structure()
        df_tmp = self.create_ids_dataframe(project)
        df_ids = df_tmp[df_tmp.columns[0:self._answers_number]]
        #print(df_ids)
        #print(self._original_answers)

        df_tmp = self.create_dataframe(project, data= self._original_answers)
        #print(project, "\n", df_tmp)
        df_qs = df_tmp[df_tmp.columns[0:self._answers_number]]

        questions = self._q_repo.as_dict()
        for i in range(0,len(df_ids)):
            for j in range(0, 9):
                ansewr = df_qs.iloc[i].iat[j]
                id = df_ids.iloc[i].iat[j]
                #print("-", test_struct[questions[id].category()]+". "+questions[id].text()+str(ansewr))
                questions_answers_view.add(id, test_struct[questions[id].category()], questions[id].text(), ansewr)

        return questions_answers_view


    def original_answers(self):
        return self._original_answers

    def id_quesions(self):
        return self._answers_id

    def years_months(self, project_id, group_id):
        df = self.create_dataframe(project_id, group_id)
        result = dict() # dict of dcit
        datetimes = list(df['datetime'])
        for dt_string in datetimes:
            #print(datetime.fromisoformat(dt_string))
            dt = datetime.fromisoformat(dt_string)
            year = dt.year
            month = dt.month
            if year not in result:
                result[year] = dict()
            result[year][month] = month

        y_m = dict()
        for k, v in result.items():
            y_m[k] = list(v)
        return y_m


class RadarAnalysis(object):

    def __init__(self):
        self._test_struct = {"Precondiciones": [1,2], "Seguridad sicológica": [3, 4], "Dependabilidad": [5, 6],
                             "Estructura y claridad":[7], "Significado": [8], "Impacto": [9]}
        self._result = None
        self._date_info= None
        self._has_answers = False

    def _add_result(self, main_key, sub_key, float_list):
        trunc_list = [str(n)[:5] for n in float_list]
        self._result[main_key][sub_key] = trunc_list

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

    def _stats_analysis(self, mean, mad):
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

    def _filter(self, dataframe, id_proj, id_team, year = None, month = None):
        import datetime
        dataframe['month'] = dataframe['datetime'].apply(lambda x: datetime.datetime.fromisoformat(x).month)
        dataframe['year'] = dataframe['datetime'].apply(lambda x: datetime.datetime.fromisoformat(x).year)

        proj_df = dataframe[ dataframe['project_id'] == id_proj ]
        team_df = proj_df[ proj_df['team_id'] == id_team ]

        if year is None:
            year = team_df['year'].max()
        else:
            year = int(year)

        if month is None:
            month = team_df[team_df['year'] == year]['month'].max()
        else:
            month = int(month)

        self._date_info = dict()
        self._date_info['year'] = year
        self._date_info['month'] = month

        dated_df = team_df[(team_df['year'] == year) & (team_df['month'] == month)]

        return dated_df

    def analyze(self, p_dataframe, id_proj, id_team, year = None, month = None):
        """
        Formato del dataframe de entrada
            1  2  3  4  5  6  7  8  9                    datetime project_id team_id
            0  0  3  2  0  1  2  5  3  2  2020-12-23 15:24:17.008097         01      01
            1  4  2  0  1  5  1  2  2  0  2021-01-09 20:19:47.775812         01      01
            2  5  5  5  5  0  0  5  5  5  2021-01-09 20:23:14.744930         01      01

        :param dataframe:
        :return:
        Data { característica: {espuestas: [[.....], [....]], mean [...] mad [...] analysis: "......" } }
        ¿Qué es date info?
        """
        self._result = dict()
        dataframe = self._filter(p_dataframe, id_proj, id_team, year, month)
        #print("Dataframe: \n", dataframe)
        self._has_answers = len(dataframe) > 0
        for k, v in self._test_struct.items():
            self._result[k] = dict()
            #print("V ", v,"\n Dataframe: \n", dataframe)
            df_factor = dataframe[v]

            answers = list()
            for i in range(0, len(df_factor)):
                answers.append(df_factor.iloc[i]. to_list())
            self._result[k]['answer'] = answers

            #print("--", k)
            ser_mean = df_factor.mean(axis=0)
            self._add_result(k,'mean', ser_mean.to_list())
            #print("Medias:\n", ser_mean)
            ser_mad = df_factor.mad(axis=0)
            self._add_result(k,'mad', ser_mad.to_list())
            #print("Desviaciones medias:\n",ser_mad)
            self._result[k]['analysis'] = self._stats_analysis(ser_mean, ser_mad)

        return self._result, self._date_info

    def has_answers(self):
        return self._has_answers


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
    #test_results = _load_answers(questions_repo)
    df = test_results.create_dataframe()
    ra = RadarAnalysis()
    data_report, date_info = ra.analyze(df, id_proj, id_team, year, month)
    return data_report, date_info, ra.has_answers()


def questions_answers(test_results, id_proj, id_team):
    """

    :param test_results:
    :param id_proj:
    :param id_team:
    :return: A list of strings like this:
        'G02.Impacto. Siento que tenemos los suficientes objetivos para poder estar centrados.:[5]'
    """
    #test_results = _load_answers(questions_repo)
    q_a_dict = test_results.question_answers(id_proj)
    sorted_keys = sorted(q_a_dict.keys())
    q_a_list = list()
    for key in sorted_keys:
        q_a_list.append(key + ":" + str(q_a_dict[key]))
    return q_a_list

# Test
"""
questions_repo = load_questions()
test_results = _load_answers(questions_repo)
print(test_results)
df = test_results.create_dataframe()
print("-------------------------------")
print(len(df))

import datetime
#df['obj_datetime'] = df['datetime'].apply(lambda x: datetime.datetime.fromisoformat(x))
df['month'] = df['datetime'].apply(lambda x: datetime.datetime.fromisoformat(x).month)
df['year'] = df['datetime'].apply(lambda x: datetime.datetime.fromisoformat(x).year)

print(df.head())
max_year = df['year'].max()
print(max_year)
print(df[ df['year'] == max_year ]['month'].max())
"""

# A partir de aquí hacer el análisis.
#print(df[(1, 2)])
"""
print(df.mean(axis=0))
print("-------------")
print(df.mad(axis=0))
print("-------------")
print(df.mean(axis=0).mean())
"""
#ra = RadarAnalysis()
#print(ra.analyze(df, "01", "01"))

# Hacer un listado con todas las preguntas que han aparecido en los test y sus repsuestas.

"""
for i in range(0, len(df)):
    print(df.iloc[i])
print(type(df.iloc[0]))
"""