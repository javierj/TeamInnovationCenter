from analysis import _load_answers, TestsResult
from tappraisal import load_questions, _save_data

"""
Script para cmabiar las respuestas de encuestas, cambia los 1 por 5, 2 por 4, etc.
Esto es necesario proque las isntrucciones estaban mal y puntuaban 1 como la mejor cuando es la peor.
"""

questions_repo = load_questions()
results = _load_answers(questions_repo, "IWT2_reports\\022021 - GIMO-PD.txt")

answers = results.original_answers()
ids = results.id_quesions()

for index in range(0, len(answers)):
    answer = answers[index]
    id = ids[index]
    line = answer['project_id']+"/"+answer['team_id']+'/'
    for i_answer in range(1, 10):
        line += str(id[i_answer])+str(6 - answer[i_answer])
    print(line)
    _save_data(line, "GIMO-PD")

