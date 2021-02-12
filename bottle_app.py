from bottle import route, template, request, static_file, redirect, default_app
from tappraisal import AppraisalDirector, TestData, load_questions
from analysis import generate_report, _load_answers
import os

director = None
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _server_url(request_url):
    return request_url.split('/')[0]

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
    base_url = request.url

    """
    if base_url.endswith('/') == False:
        base_url += "/"
    """

    if question is None:
        #print("Server URL: ", _server_url(request.url))
        return template('end_template', base_url=_server_url(base_url))

    #print("áéÍÓñÑ: " + question.text())
    return template('question_template', question=question.text(), base_url = base_url, question_code = question.code(), question_index = data.len_questions() + 1)

#@route('/test/<org_id>/<project_id>')
@route('/test/<org_id>/<project_id>/')
def first_question(org_id, project_id):
    return question(org_id, project_id)

@route('/report_test')
def report_test():
    data_report = {'Precondiciones': {'answer': [[0, 3], [4, 2], [5, 5]], 'mean': ['3.0', '3.333'], 'mad': ['2.0', '1.111']}, 'Seguridad sicológica': {'answer': [[2, 0], [0, 1], [5, 5]], 'mean': ['2.333', '2.0'], 'mad': ['1.777', '2.0']}, 'Dependabilidad': {'answer': [[1, 2], [5, 1], [0, 0]], 'mean': ['2.0', '1.0'], 'mad': ['2.0', '0.666']}, 'Estructura y claridad': {'answer': [[5], [2], [5]], 'mean': ['4.0'], 'mad': ['1.333']}, 'Significado': {'answer': [[3], [2], [5]], 'mean': ['3.333'], 'mad': ['1.111']}, 'Impacto': {'answer': [[2], [0], [5]], 'mean': ['2.333'], 'mad': ['1.777']}}
    return template('report_template', data_report=data_report)

# Aún no funciona, hay que añadir id de poryecto y equipo
#@route('/report/<org_id>/<project_id>')
@route('/report/<org_id>/<project_id>/')
def report(org_id, project_id):
    global director
    test_results = _load_answers(director.get_repo())
    data_report, date_info, has_answers = generate_report(test_results, org_id, project_id)
    #q_a_list = questions_answers(test_results, org_id, project_id)
    q_a_v = test_results.question_answers_to_view(org_id, project_id) # Necsita el sgeundo valor
    #print(q_a_v)
    if has_answers:
        return template('report_template', data_report=data_report, date_info = date_info, question_answer=q_a_v)
    return template('noanswers_template', org_id=org_id, project_id = project_id)

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