####################################
# Controlers
from analysis import load_test_results, CVSResults
from tappraisal import TestStructsCache
from utilities import _get_full_filename, _save_text


def answers_as_cvs_in_file(poll_id, survey_type):
    struct = TestStructsCache.get_struct(survey_type)
    if struct is None:
        return None
    test_results = load_test_results(struct.questions_repo(), poll_id, poll_id, survey_name = struct.name())
    CVS = CVSResults()

    # Grabar en fichero
    full_filename = _get_full_filename("CVS_tmp.cvs")
    _save_text(full_filename,CVS.results_to_cvs(struct, test_results) )

    return full_filename

