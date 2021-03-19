from bottle import route, template, request, static_file, redirect, default_app
from tappraisal import AppraisalDirector, TestData, load_questions, get_survey_structure
from analysis import generate_report, surveys_overview, load_test_results
import os

question_repo = None
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def _server_url():
    return request.url.split('/')[0]


@route('/')
def home():
    #print('Home is Working')
    redirect("/static/index.html")


@route('/static/<filename:path>')
def send_static(filename):
    global BASE_DIR
    #base_path = os.path.dirname(os.path.abspath(__file__))
    my_path = os.path.join(BASE_DIR, 'static')
    #print("Statyic path: ", my_path, "Base:", BASE_DIR)
    return static_file(filename, root=my_path)

# ver la manera de hacer estos dos métodos mejor.


@route('/stylesheets/<filename:path>')
def stylesheets_static(filename):
    return redirect("/static/stylesheets/"+filename)


@route('/images/<filename:path>')
def images_static(filename):
    return redirect("/static/images/"+filename)

@route('/iwt2')
@route('/IWT2')
@route('/iwt2/')
@route('/IWT2/')
def iwt2_static():
    return redirect("/static/iwt2.html")


@route('/get_data')
def get_data():
    global BASE_DIR
    return static_file("data.txt", root=BASE_DIR)


@route('/get_questions')
def get_questions():
    global BASE_DIR
    return static_file("preguntas.txt", root=BASE_DIR)


@route('/test/<org_id>/<project_id>/<questions>')
def question_radar9(org_id, project_id, questions=""):
    return question("RADAR-9", org_id, project_id, questions)

#@route('/test/<org_id>/<project_id>')
@route('/test/<org_id>/<project_id>/')
def first_question_radar9(org_id, project_id):
    return question("RADAR-9", org_id, project_id)

@route('/safety/<org_id>/<project_id>/<questions>')
def question_safety(org_id, project_id, questions=""):
    return question("SAFETY", org_id, project_id, questions)

@route('/safety/<org_id>/<project_id>/')
def first_question_safety(org_id, project_id):
    return question("SAFETY", org_id, project_id)


def question(test, org_id, project_id, questions=""):
    global question_repo # Tenemos que cargar aquí el director según el tipo de test

    data = TestData(org_id, project_id, questions)
    director = AppraisalDirector(get_survey_structure(question_repo, test))
    next_question = director.next_question(data)

    if next_question is None:
        #print("Server URL: ", _server_url(request.url))
        return template('end_template', base_url=_server_url())

    return template('question_template', question=next_question.text(), base_url = request.url, question_code = next_question.code(), question_index = data.len_questions() + 1)


# Aún no funciona, hay que añadir id de poryecto y equipo
#@route('/report/<org_id>/<project_id>')
@route('/report/<org_id>/<project_id>/')
def all_report(org_id, project_id):
    return report(org_id, project_id, None, None)


@route('/report/<org_id>/<project_id>/<year>/<month>/')
def report(org_id, project_id, year, month):
    global question_repo
    test_results = load_test_results(question_repo, org_id, project_id) # Poner los ids y filtrar por ellos
    report = generate_report(test_results, org_id, project_id, year=year, month=month)
    q_a_v = test_results.question_answers_to_view(org_id, project_id, year=year, month=month) # Método independiente, como generate_report
    if report.has_answers():
        return template('report_template', report=report, question_answer=q_a_v)
    return template('noanswers_template', org_id=org_id, project_id = project_id)


@route('/selector/<org_id>/<project_id>/')
def report_selector(org_id, project_id):
    s_overview = surveys_overview(org_id, project_id)
    base_url = _server_url()+"/report/"+org_id+"/"+project_id
    return template('report_selector', org_id=org_id, project_id=project_id, surveys_overview=s_overview, base_url = base_url)


def set_up():
    global question_repo
    question_repo = load_questions()
    #print("Questions: \n", str(repo))

    #print("Set up ok!")

set_up()
#run(host='0.0.0.0', port=8080)
application = default_app()
#application.run() # Comentar esta líena para despliege en pythonanywhere