from bottle import route, template, request, static_file, redirect, default_app
from tappraisal import AppraisalDirector, TestData, load_questions
from analysis import generate_report, _load_answers
import os

director = None
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
    #data_file = _get_full_filename("data.txt")
    global BASE_DIR
    return static_file("data.txt", root=BASE_DIR)

# Reducir el código de este método
@route('/test/<org_id>/<project_id>/<questions>')
def question(org_id, project_id, questions=""):
    """
    Usamos la palabra test en el url para diferenciarla d ela página base y que muestre información.
    :param org_id:
    :param project_id:
    :param questions:
    :return:
    """
    global director
    #print( "Recibido: ", org_id, project_id, questions )

    data = TestData(org_id, project_id, questions)
    question = director.next_question(data)

    if question is None:
        #print("Server URL: ", _server_url(request.url))
        return template('end_template', base_url=_server_url())

    return template('question_template', question=question.text(), base_url = request.url, question_code = question.code(), question_index = data.len_questions() + 1)

#@route('/test/<org_id>/<project_id>')
@route('/test/<org_id>/<project_id>/')
def first_question(org_id, project_id):
    return question(org_id, project_id)

# Aún no funciona, hay que añadir id de poryecto y equipo
#@route('/report/<org_id>/<project_id>')
@route('/report/<org_id>/<project_id>/')
def all_report(org_id, project_id):
    return report(org_id, project_id, None, None)

@route('/report/<org_id>/<project_id>/<year>/<month>/')
def report(org_id, project_id, year, month):
    global director
    test_results = _load_answers(director.get_repo())
    report = generate_report(test_results, org_id, project_id, year=year, month=month)
    q_a_v = test_results.question_answers_to_view(org_id, project_id, year=year, month=month)
    if report.has_answers():
        return template('report_template', report=report, question_answer=q_a_v)
    return template('noanswers_template', org_id=org_id, project_id = project_id)

@route('/selector/<org_id>/<project_id>/')
def report_selector(org_id, project_id):
    global director
    test_results = _load_answers(director.get_repo())
    month_year = test_results.years_months(org_id, project_id)  # "{'2020':[12], '2021': [1]}"
    base_url = _server_url()+"/report/"+org_id+"/"+project_id
    return template('report_selector', org_id=org_id, project_id=project_id, month_year=month_year, base_url = base_url)

def set_up():
    global director
    repo = load_questions()
    #print("Questions: \n", str(repo))
    director = AppraisalDirector(repo)
    #print("Set up ok!")

set_up()
#run(host='0.0.0.0', port=8080)
application = default_app()
#application.run() # Comentar esta líena para despliege en pythonanywhere