from bottle import route, template, request, static_file, redirect, default_app
from tappraisal import AppraisalDirector, TestData, load_questions, get_survey_structure, TestStructsCache, \
    SurveyStructure, SurveyStructureLoader
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


@route('/softia')
def iwt2_static():
    return redirect("/static/softia.html")


@route('/get_data')
def get_data():
    global BASE_DIR
    return static_file("data.txt", root=BASE_DIR)


@route('/get_questions')
@route('/get_questions/')
def get_questions():
    global BASE_DIR
    return static_file("preguntas.txt", root=BASE_DIR)


@route('/test/<org_id>/<project_id>/<questions>')
def question_radar9(org_id, project_id, questions=""):
    return question("RADAR-9", org_id, project_id, questions)


@route('/test/<org_id>/<project_id>/')
def first_question_radar9(org_id, project_id):
    return question("RADAR-9", org_id, project_id)


@route('/safety/<org_id>/<project_id>/<questions>')
def question_safety(org_id, project_id, questions=""):
    return question("SAFETY", org_id, project_id, questions)


@route('/safety/<org_id>/<project_id>/')
def first_question_safety(org_id, project_id):
    return question("SAFETY", org_id, project_id)


@route('/classic/<org_id>/<project_id>/<questions>')
def question_classic(org_id, project_id, questions=""):
    return question("CLASSIC", org_id, project_id, questions)


@route('/classic/<org_id>/<project_id>/')
def first_question_classic(org_id, project_id):
    return question("CLASSIC", org_id, project_id)


###

@route('/softia/<org_id>/<project_id>/<questions>')
def question_sofia(org_id, project_id, questions=""):
    return question("SoftIA", org_id, project_id, questions)


@route('/softia/<org_id>/<project_id>/')
def first_question_sofia(org_id, project_id):
    return question("SoftIA", org_id, project_id)

###


def _softia_get_template_name(question):
    """
    Esto se ha hecho para SoftIA para poder implementar lapregunta de género
    y de titulación
    :param question: objeto de tipo TestQuestion
    :return:
    """
    if question.category() == '0':
        return 'softia_gender_question_template'
    if question.category() == '1':
        return 'softia_course_question_template'

    return 'question_template'


def question(test, org_id, project_id, questions=""):
    global question_repo # Tenemos que cargar aquí el director según el tipo de test

    data = TestData(org_id, project_id, questions)
    director = AppraisalDirector(get_survey_structure(question_repo, test))
    next_question = director.next_question(data)

    if next_question is None:
        #print("Server URL: ", _server_url(request.url))
        return template('end_template', base_url=_server_url())

    template_name = _softia_get_template_name(next_question)
    return template(template_name, question=next_question.text(), base_url = request.url, question_code = next_question.code(), question_index = data.len_questions() + 1)


########
# Alternativa para cargar una estructura a partir de un fichero.

@route('/poll/<poll_name>/<group_id>/<questions>')
def question_poll(poll_name, group_id, questions=""):
    struct = TestStructsCache.get_struct(poll_name)
    if struct is not None:
        return poll_question(struct, group_id, questions)

    # TODO: redirigir a una página de error.
    return template('error_template', base_url=request.url)


@route('/poll/<poll_name>/<group_id>/')
def first_question_poll(poll_name, group_id):
    struct = TestStructsCache.get_struct(poll_name)
    if struct is not None:
        return poll_question(struct, group_id)

    # TODO: redirigir a una página de error.
    return template('error_template', base_url=request.url)


def poll_question(struct, group_id, questions=""):
    data = TestData(group_id, group_id, questions)
    director = AppraisalDirector(struct) # Appraisaldirector s epodríaquitar y llamar directamente al next de la estructura
    next_question = director.next_question(data)

    if next_question is None:
        #print("Server URL: ", _server_url(request.url))
        return template('end_template', base_url=_server_url())

    # Hacer esto más genérico
    # template_name = _softia_get_template_name(next_question)
    return template('question_template',
                    question=next_question.text(), base_url=request.url, question_code=next_question.code(), question_index = data.len_questions() + 1)


###

@route('/report/<org_id>/<project_id>/<year>/<month>/')
def report_radar9(org_id, project_id, year, month):
    return report(org_id, project_id, year, month, "RADAR-9")


@route('/report/<org_id>/<project_id>/<year>/<month>/<survey_type>/')
def report(org_id, project_id, year, month, survey_type):
    global question_repo
    upper_survey_type = survey_type.upper()
    test_results = load_test_results(question_repo, org_id, project_id, survey_name = upper_survey_type) # Poner los ids y filtrar por ellos
    report = generate_report(test_results, org_id, project_id, year=year, month=month, survey= upper_survey_type)
    if report.has_answers():
        q_a_v = test_results.question_answers_to_view(org_id, project_id, year=year, month=month)  # Método independiente, como generate_report
        desc = get_survey_structure(question_repo, upper_survey_type).description_dict()
        return template('report_template', report=report, question_answer=q_a_v, defs = desc)
    return template('noanswers_template', org_id=org_id, project_id = project_id)


@route('/selector/<org_id>/<project_id>/')
def report_selector(org_id, project_id):
    s_overview = surveys_overview(org_id, project_id)
    base_url = _server_url()+"/report/"+org_id+"/"+project_id
    return template('report_selector', org_id=org_id, project_id=project_id, surveys_overview=s_overview, base_url = base_url)


### Form para crear una nueva estructura de encuesta

@route('/newpoll')
def login():
    return template('form_create_struct')


def check_error(request):
    # ToDo
    return None


@route('/newpoll', method='POST')
def do_new_poll():
    #username = request.forms.get('username')
    #password = request.forms.get('password')
    if check_error(request) is None:
        #print("bottle_app. ", request.forms.get('questions_file'))
        #result = SurveyStructure.translate_to_json(request)
        saver = SurveyStructureLoader()
        saver.save_structure(request) # corregir esto, no hacer las dos cosas aquí.
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Form has errors.</p>"


#--- URLs erróneas ----------------------

@route('/report/<org_id>/<project_id>')
@route('/report/<org_id>/<project_id>/')
@route('/test/<org_id>/<project_id>')
def error_url(org_id, project_id):
    return template('error_template', base_url = request.url)


def set_up():
    global question_repo
    question_repo = load_questions()

set_up()
#run(host='0.0.0.0', port=8080)
application = default_app()
application.run() # Comentar esta líena para despliege en pythonanywhere