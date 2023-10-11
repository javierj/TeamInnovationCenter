####################################
# Controlers

from analysis import load_test_results, CVSResults, surveys_from_poll, generate_report
from tappraisal import TestStructsCache, SurveyStructureLoader
from utilities import _get_full_filename, _save_text, file_exists, load_text_file, _save_text_full_filename
from view import HierarchicalGroups, PollStructView


def _get_struct(poll_name):
    return TestStructsCache.get_struct(poll_name)


######


def answers_as_cvs_in_file(poll_id, survey_type):
    struct = _get_struct(survey_type)
    if struct is None:
        return None
    test_results = load_test_results(struct.questions_repo(), poll_id, poll_id, survey_struct=struct)
    CVS = CVSResults()

    # Grabar en fichero
    full_filename = _get_full_filename("CVS_tmp.cvs")
    _save_text_full_filename(full_filename, CVS.results_to_cvs(struct, test_results) )

    return full_filename


def get_surveys_from_poll(survey_type):
    s_overview = surveys_from_poll(survey_type)
    cvs_keys = HierarchicalGroups()
    for year in s_overview.begin().keys():
        cvs_keys.begin().add_group(year)
        for month in s_overview.begin().group(year).keys():
            for project_id in s_overview.begin().group(year).group(month).keys():
                cvs_keys.begin().group(year).add_group(project_id)
    #print(s_overview)
    #print(cvs_keys)
    return s_overview, cvs_keys


########
# Templates:


def question_template_name(default_template, lang, survey_struct, question):
    if survey_struct is not None:
        #print("Survey name: ", survey_struct.name())
        if survey_struct.name().lower() == "softia" or survey_struct.name().lower() == "softia_en":
            if question.category() == '0':
                return 'softia_gender_question_template'
            if question.category() == '1':
                return 'softia_course_question_template'
        if survey_struct.lang() != "":
            return default_template + "_" + survey_struct.lang()

    if lang != "":
        return default_template + "_" + lang

    return default_template


def get_template_name(template_id, default_template, request_query=None, survey_struct=None, question=None):
    if request_query is None:
        lang = ""
    else:
        lang = request_query.lang

    if template_id == "report":
        if lang != "":
            return default_template + "_" + lang

    #print("get_template_name() - template_id ", template_id)
    if template_id == "question":
        return question_template_name(default_template, lang, survey_struct, question)

    return default_template

########


def _start_with_double_quote(text):
    if type(text) is dict:
        return True
    return text.strip().startswith("\"")


def _check_error(struct_view):
    errors = dict()

    if struct_view.questions_filename() == "":
        errors["questions_file"] = "You must indicate a name for the file of the questions."
    if struct_view.name() == "":
        errors["poll_name"] = "You must indicate a name for the struct."
    if struct_view.num_of_questions() == "":
        errors["num_of_questions"] = "You must indicate the number of questions of the poll."

    if struct_view.questions_in_categories() == "":
        errors["questions_in_categories"] = "You must indicate the questions in each category."
    if struct_view.get_test_structure() == "":
        errors["poll_structure"] = "You must indicate the structure of the poll."
    if struct_view.get_groups() == "":
        errors["groups"] = "You must indicate the groups of the poll."
    if struct_view.description_dict() == "":
        errors["descriptions"] = "You must indicate the description of the categories."

    return errors


def save_struct_from_request(request):
    struct_view = PollStructView.from_request(request)
    errors = _check_error(struct_view)
    if len(errors) == 0:
        saver = SurveyStructureLoader()
        saver.save_structure(struct_view.filename(), struct_view.to_json())
    return struct_view, errors

#########


def load_questions_if_exist(poll_name):
    struct = _get_struct(poll_name)
    if struct is None:
        return None

    questions_txt = ""
    filename = struct.questions_filename()
    full_filename = _get_full_filename(filename, "polls")
    if file_exists(full_filename):
        lines = load_text_file(full_filename)
        for line in lines:
            questions_txt += line
    else:
        print("load_questions_if_exist() - file not found: ", full_filename)
    #print("After: ", questions_txt)
    return questions_txt


def save_questions(poll_name, request):
    struct = _get_struct(poll_name)
    if struct is None:
        return None

    #questions_txt = _from_request("questions_text", request)
    questions_txt = request.forms.questions_text
    print(questions_txt)
    filename = struct.questions_filename()
    #full_filename = _get_full_filename(filename, "polls")
    _save_text(filename, questions_txt, basedir = "polls")
    return "Not None"


#######################

def poll_exists(poll_name):
    struct = _get_struct(poll_name)
    return struct is not None


####################

def get_report_data(survey_struct, org_id, project_id, year, month):
    test_results = load_test_results(survey_struct.questions_repo(),
                                     org_id, project_id,
                                     survey_name = survey_struct.name().upper(),
                                     survey_struct=survey_struct)
    poll_report, flags = generate_report(test_results, org_id, project_id, year=year, month=month, survey_struct=survey_struct)
    if poll_report.has_answers():
        q_a_v = test_results.question_answers_to_view(org_id, project_id, year=year, month=month)  # Método independiente, como generate_report
        notes = ""
        if flags is not None:
            if flags["Diff_Num_of_Answers"] is True:
                notes = "Warning. Diferent number of anwsers for some surveys."
                print("control:: get_report_data. ", notes)
        return poll_report, q_a_v, notes

    return None
