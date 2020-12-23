from bottle import route, run, template, request, static_file, redirect
from tappraisal import AppraisalDirector, TestData, load_questions

director = None

@route('/')
def home():
    print('Home is Working')
    #return template('Home is Working')
    #return "Home is Working"
    redirect("/static/index.html")

@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./static')

# ver la manera de hacer estos dos métodos mejor.

@route('/stylesheets/<filename:path>')
def stylesheets_static(filename):
    return redirect("/static/stylesheets/"+filename)

@route('/images/<filename:path>')
def stylesheets_static(filename):
    return redirect("/static/images/"+filename)

@route('/get_data')
def get_data():
    return static_file("data.txt", root='.')

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
    print( "Recibido: ", org_id, project_id, questions )

    data = TestData(org_id, project_id, questions)
    question = director.next_question(data)

    if question == None:
        redirect("/static/end.html")


    #print('Working: ' + question.text())
    return template('question_template', question=question.text(), base_url = request.url, question_code = question.code())


@route('/test/<org_id>/<project_id>')
@route('/test/<org_id>/<project_id>/')
def first_question(org_id, project_id):
    return question(org_id, project_id)


def set_up():
    global director
    director = AppraisalDirector(load_questions())
    #repo =
    #print("Questions: \n", str(repo))
    print("Set up ok!")

set_up()
run(host='localhost', port=8080)