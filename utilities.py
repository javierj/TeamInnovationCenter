

class Cache(object):

    cache = dict()

    @staticmethod
    def get(key):
        if not Cache.key_in(key):
            return None
        return Cache.cache[key]

    @staticmethod
    def key_in(key):
        return key in Cache.cache

    @staticmethod
    def put(key, value):
        Cache.cache[key] = value


##############################
# file utilities

def _get_full_filename(filename, basedir = None):
    import os
    base_path = os.path.dirname(os.path.abspath(__file__))
    if basedir is not None:
        my_path = os.path.join(base_path, basedir)
        my_path = os.path.join(my_path, filename)
    else:
        my_path = os.path.join(base_path, filename)
    return my_path


def _save_text(full_filename, text_string):
    """
    Call _get_full_filename for obtain the right full_filename
    """
    with open(full_filename, "w") as myfile:
        myfile.write(text_string)




