import pandas as pd

from analysis import TestsResult
from tappraisal import load_questions
from view import HierarchicalGroups

data = [['2020', '12', 'RADAR-9', 4, 5, 3],
 ['2020', '12', 'RADAR-9', 4, 5, 3],
 ['2021', '1', 'RADAR-9', 4, 5, 3],
 ['2021', '2', 'RADAR-9', 4, 5, 3]]
columns = ['year', 'month', 'survey_type', '1', '2', '3']
df = pd.DataFrame(data = data, columns = columns)
print(df)

df_grouped = df.groupby(['year', 'month', 'survey_type'])
#print(df_grouped[['1', '2']])
#print(df_grouped['1', '2'].mean(axis=0, skipna=True))

for name, group in df_grouped:
    #print('ID: ' + str(name))
    year = group['year'].iloc[0]
    print(year)
    print(group[['1', '2']].mean().mean())
    print(group[['3']].mean().iloc[0])
    print("\n")

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

results = TestsResult(q_repo=load_questions())
results.add_test_answer("2021-01-28 17:08:00.482801/01/01/A021B012C121C105D065D135E062F051G055")
results.add_test_answer("2021-01-28 17:08:02.912267/01/01/A012B044C042C015D135D101E022F045G055")
results.add_test_answer("2021-02-28 17:08:02.912267/01/01/A012B044C042C015D135D101E022F045G055")
results.add_test_answer("2021-03-28 17:08:02.912267/01/01/A012B044C042C015D135D101E022F045G055")

surveys = results.get_surveys()
# ['year', 'month', 'survey_type', '1', '2', '3']
data = list()
factors = HierarchicalGroups()
for survey in surveys:
    s_list = list()
    s_list.append(survey.year())
    s_list.append(survey.month())
    s_list.append("Radar-9")
    for index in range(0, 3):
        answer = survey.answers()[index]
        s_list.append(answer.adapted_answer())
        factors.begin().add_group(answer.factor()).add_in_bag(index)
    data.append(s_list)

print(data)
print(factors)

df = pd.DataFrame(data = data, columns = columns)
df_grouped = df.groupby(['year', 'month', 'survey_type']) # <- No necesitamos agrupar por survey_type, sino filtrar.

for name, group in df_grouped:
    #print('ID: ' + str(name))
    year = group['year'].iloc[0]
    print(year)
    for factor in factors.begin().keys():
        index_list = list()
        for index in factors.begin().group(factor).bag():
            index_list.append(index)
        print(factor, index_list)
    print(group[['1', '2']].mean().mean())
    print(group[['3']].mean().iloc[0])
    print("\n")

# ¿Dónde guardamos los datos históricos?
