import pandas as pd
from tappraisal import _get_full_filename,  load_questions

class TestsResult(object):

    def __init__(self, questions_number = 9, q_repo = None):
        self._questions = dict() # deprecate
        self._answers = list()
        self._q_repo = q_repo
        self._answers_numer = questions_number

    def add_test_answer(self, result_line):
        data = result_line.split('/')
        #datetime = data[0]
        #project_id = data[1]
        #team_id = data[2]
        #self._add_answers(data[3])
        answers_list = self._extract_answers(data[3])
        if len(answers_list) < self._answers_numer:
            #print("No hay las suficientes repsuestas")
            return
        answers_dict = {k: answers_list[k-1] for k in range(1, len(answers_list)+1) }
        answers_dict['datetime'] = data[0]
        answers_dict['project_id'] = data[1]
        answers_dict['team_id'] = data[2]
        self._answers.append(answers_dict)

    # Deprecated. Testing a diferent approach.
    def _add_answers(self, q_url):
        self._answers = 0
        answer_len = int(len(q_url) / 4)
        for i in range(0, answer_len):
            tmp = q_url[(4 * i):(4 * i) + 4]
            q_id = tmp[0:3]
            answer = tmp[3]
            category = q_id[0]

            if category not in self._questions:
                self._questions[category] = list()
                self._answers[category] = list()
            self._questions[category].append(q_id[1:3])
            self._answers[category].append(answer)
            self._answers += 1

    def _get_answer_value(self, value_str, category, code):
        value = int(value_str)
        question = self._q_repo.get_question(category, code)
        if question.is_positive():
            return value
        return 5 - value

    def _extract_answers(self, q_url):
        answers = list()
        answer_len = int(len(q_url) / 4)
        for i in range(0, answer_len):
            tmp = q_url[(4 * i):(4 * i) + 4]
            q_id = tmp[0:3]
            category = q_id[0]
            answer_value = self._get_answer_value(tmp[3], category, q_id)
            answers.append(answer_value) # Cambiar esto por si la pregunta es negativa
        return answers

    # Deprecated
    def categories(self):
        return self._questions.keys()

    def __str__(self):
        return str(self._answers)

    def create_dataframe(self):
        return pd.DataFrame(self._answers)


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
                return "La media y la desviación indica que, aunque la mayoría del equipo se muestra disconforme, hay un pequeño número de personas que están contentas. Recomendamos alguna actividad de grupo dónde estas personas puedan comaprtir sus visiones y se planteen soluciones que cuenten con el consenso de todos, para intentar aumentar el número de personas con una valoración positiva."
            return "Los resultados son demasiado variables para poder extraer una conclusión. Recomendamos realizar actividades de equipo para marcar objetivos comunes y volver a repetir las encuestas para ver su progresión."
        if self._all_under(mad, 1):
            if self._all_over(mean, 2.5):
                return "La media indica que la mayoría de las respuestas están en los valores superiores. Continuad trabajando de esta manera."
            if  self._all_under(mean, 2.5):
                return "La media indica que la mayoría de las repsuestas están en los valores inferiores. recomenamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo."
            return "El equipo está en un nivel intermedio, ni bien ni mal. Puedes aprovechar este estado para meorar otro factor que esté por detrás o seguir trabajando en actividades para potenciar este factor."
        # Never reached.
        return "Las desviaciones indican que las preguntas de un mismo factor no son consistentes. Se recomienda repetir la encuesta en unas semanas."

    def _filter(self, dataframe, id_proj, id_team):
        import datetime
        dataframe['month'] = dataframe['datetime'].apply(lambda x: datetime.datetime.fromisoformat(x).month)
        dataframe['year'] = dataframe['datetime'].apply(lambda x: datetime.datetime.fromisoformat(x).year)

        proj_df = dataframe[ dataframe['project_id'] == id_proj ]
        team_df = proj_df[ proj_df['team_id'] == id_team ]

        max_year = team_df['year'].max()
        max_month = team_df[team_df['year'] == max_year]['month'].max()
        self._date_info = dict()
        self._date_info['year'] = max_year
        self._date_info['month'] = max_month

        dated_df = team_df[(team_df['year'] == max_year) & (team_df['month'] == max_month)]

        return dated_df

    def analyze(self, p_dataframe, id_proj, id_team):
        """
        Formato del dataframe de entrada
            1  2  3  4  5  6  7  8  9                    datetime project_id team_id
            0  0  3  2  0  1  2  5  3  2  2020-12-23 15:24:17.008097         01      01
            1  4  2  0  1  5  1  2  2  0  2021-01-09 20:19:47.775812         01      01
            2  5  5  5  5  0  0  5  5  5  2021-01-09 20:23:14.744930         01      01

        :param dataframe:
        :return:
        Data { característica: {espuestas: [[.....], [....]], mean [...] mad [...] analysis: "......" } }
        """
        self._result = dict()
        dataframe = self._filter(p_dataframe, id_proj, id_team)
        self._has_answers = len(dataframe) > 0
        for k, v in self._test_struct.items():
            self._result[k] = dict()
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

    def has_answers(self,):
        return self._has_answers


def _load_answers(questions_repo):
    answers = TestsResult(q_repo = questions_repo)

    file_name = _get_full_filename("data.txt")
    file = open(file_name, encoding="utf-8") # No: encoding="latin-1" encoding="ascii"
    for line in file:
        answers.add_test_answer(line)

    file.close()
    return answers


def generate_report(questions_repo, id_proj, id_team):
    test_results = _load_answers(questions_repo)
    df = test_results.create_dataframe()
    ra = RadarAnalysis()
    data_report, date_info = ra.analyze(df, id_proj, id_team)
    return data_report, date_info, ra.has_answers()


# Test
"""
questions_repo = load_questions()
test_results = _load_answers(questions_repo)
print(test_results)
df = test_results.create_dataframe()
print("-------------------------------")
#print(len(df))

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

ra = RadarAnalysis()
print(ra.analyze(df))
"""
# Hacer un listado con todas las preguntas que han aparecido en los test y sus repsuestas.

"""
for i in range(0, len(df)):
    print(df.iloc[i])
print(type(df.iloc[0]))
"""