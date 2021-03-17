from analysis import _load_answers, TestsResult
from tappraisal import load_questions, _save_data

"""
Script para cmabiar las respuestas de encuestas, cambia los 1 por 5, 2 por 4, etc.
Esto es necesario proque las isntrucciones estaban mal y puntuaban 1 como la mejor cuando es la peor.
"""

questions_repo = load_questions()
results = _load_answers(questions_repo, "IWT2_reports\\202103 - IWT2")

#answers = results.original_answers()
#ids = results.id_quesions()

#for index in range(0, len(answers)):
for survey in results.get_surveys():
    #answer = answers[index]
    #id = ids[index]
    line = survey.project_id()+"/"+survey.team_id()+'/'
    i_answer = 1
    for answer in survey.answers():
        line += answer.id()+str(6 - answer.original_answer())
        i_answer +=1
    print(line)
    _save_data(line, "IWT2_reports\\202103 - IWT2_Fixed")

