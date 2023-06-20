####################################
# Controlers
from analysis import load_test_results, CVSResults, surveys_from_poll
from tappraisal import TestStructsCache
from utilities import _get_full_filename, _save_text, file_exists, load_text_file
from view import HierarchicalGroups


def _get_struct(poll_name):
    return TestStructsCache.get_struct(poll_name)


def _from_request(_key, request):
    return request.forms.get(_key)

######


def answers_as_cvs_in_file(poll_id, survey_type):
    struct = _get_struct(survey_type)
    if struct is None:
        return None
    test_results = load_test_results(struct.questions_repo(), poll_id, poll_id, survey_name = struct.name())
    CVS = CVSResults()

    # Grabar en fichero
    full_filename = _get_full_filename("CVS_tmp.cvs")
    _save_text(full_filename,CVS.results_to_cvs(struct, test_results) )

    return full_filename



def get_surveys_from_poll(survey_type):
    s_overview = surveys_from_poll(survey_type)
    cvs_keys = HierarchicalGroups()
    for year in s_overview.begin().keys():
        cvs_keys.begin().add_group(year)
        for month in s_overview.begin().group(year).keys():
            for project_id in s_overview.begin().group(year).group(month).keys():
                cvs_keys.begin().group(year).add_group(project_id)
    #print(cvs_keys)
    return s_overview, cvs_keys


#########


def load_questions_if_exist(poll_name):
    struct = _get_struct(poll_name)
    if struct is None:
        return None

    questions_txt = ""
    filename = struct.questions_filename()
    full_filename = _get_full_filename(filename, "polls")
    #print("file to found: ", full_filename)
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

    questions_txt = _from_request("questions_text", request)
    filename = struct.questions_filename()
    full_filename = _get_full_filename(filename, "polls")
    _save_text(full_filename, questions_txt)
    return "Not None"




#######################

def poll_exists(poll_name):
    struct = _get_struct(poll_name)
    return struct is not None

