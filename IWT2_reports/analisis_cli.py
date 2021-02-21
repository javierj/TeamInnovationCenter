import pandas as pd
from tappraisal import load_questions
from analysis import RadarAnalysis, _load_answers, TestsResult, questions_answers

questions_repo = load_questions()
#results = _load_answers(questions_repo, "IWT2_reports\\022021 - GIMO-PD.txt")
#print(results.create_ids_dataframe())
#results = _load_answers(questions_repo, "IWT2_reports\\072021 - APPIMEDEA.txt")
#results = _load_answers(questions_repo, "IWT2_reports\\012021 - AIRPA")
#results = _load_answers(questions_repo, "IWT2_reports\\022021 - G7D.txt")
results = _load_answers(questions_repo, "IWT2_reports\\data.txt")

ra = RadarAnalysis()
#data_report, date_info = ra.analyze(results.create_dataframe(), "AIRPA", "T01")
df = results.create_dataframe()
data_report = ra.analyze(df, "01", "01")
#print( data_report)

for key, factor in data_report.iter_factors():
    #means = [float(v) for v in value['mean'] ]
    print(key, "Respuestas:", "Means:", factor.means(), "MADS:", factor.mads(), "Media means:", factor.total_mean(), "Media mads:", factor.total_mad())
    #total = sum(means)
    #print("Media de", key, "=", (total / len(means)))

print("------------------------------")
test_struct = {'A': "Precondiciones",'B': "Precondiciones", 'C': "Seguridad sicológica", 'D': "Dependabilidad",
               'E': "Estructura y claridad", 'F':"Significado", 'G': "Impacto"}

#print(df) # Necesito un dataframe con el código de las repsuestas

# Ahora tengo que combinar ambos dataframes d emanera que saque las preguntas del primero y las repsuestas del segundo.


"""
questions = questions_repo.as_dict()

questios_report = list()

for key, value in results.question_anwsers().items():
    answer = key+':'+test_struct[questions[key].category()]+". "+questions[key].text()+ str(value)
    questios_report.append(answer)

questios_report.sort()
for answer_line in questios_report:
    #print(answer_line)
    pass
"""

# Quiero poner a que tipo es cada pregunta


df_ids = results.create_ids_dataframe()
#print(df.columns[0:9])
#print(df[df.columns[0:9]])

df_questions = df[df.columns[0:9]]
df_id_questions = df_ids[df_ids.columns[0:9]]

"""
question_answers = dict()
for i in range(0,len(df_questions)):
    #print(df_questions.iloc[i])
    #print(df_id_questions.iloc[i])
    #for elem in df_questions.iloc[i]:
    for j in range(0, 9):
        ansewr = df_questions.iloc[i].iat[j]
        id = df_id_questions.iloc[i].iat[j]
        #print(test_struct[questions[id].category()]+". "+questions[id].text()+str(ansewr))
        key = id+"."+test_struct[questions[id].category()]+". "+questions[id].text()
        if key in question_answers:
            question_answers[key].append(ansewr)
        else:
            question_answers[key] = list()
            question_answers[key].append(ansewr)

"""

print(results.question_answers("GIMO-PD"))
"""
#results = TestsResult(q_repo = questions_repo )
q_a_dict = results.question_answers("APP-IMEDEA")
sorted_keys = sorted(q_a_dict.keys())
for key in sorted_keys:
    print(key+":"+str(q_a_dict[key]))
"""
print("-----------------------------")
for line in questions_answers(results, "GIMO-PD", None):
    print(line)

# El problema e sque no salen las repsuestas originales aquí.


print("-----------------------------")
import datetime
df['month'] = df['datetime'].apply(lambda x: datetime.datetime.fromisoformat(x).month)
df['year'] = df['datetime'].apply(lambda x: datetime.datetime.fromisoformat(x).year)

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
