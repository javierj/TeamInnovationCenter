

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


def _save_text(filename, text_string, basedir = None, backup=True):
    if basedir is not None:
        full_filename = _get_full_filename(filename, basedir)
    else:
        full_filename = filename
    _save_text_full_filename(full_filename, text_string)
    if backup:
        _save_backup(filename, text_string)


def _save_text_full_filename(full_filename, text_string):
    with open(full_filename, "w", encoding="utf-8") as myfile:
        #myfile.write(text_string)
        for line in text_string.split('\n'):
            myfile.write(line.strip() + '\n')


def _save_backup(filename, text_string):
    full_filename=_backup_time() + "_" + filename
    _save_text(full_filename, text_string, basedir="backups", backup=False)


def file_exists(full_filename):
    import os
    return os.path.isfile(full_filename)


def load_text_file(full_filename):
    with open(full_filename, encoding="utf-8") as f:
        lines = f.readlines()
    return lines



#### Date utilities

def _backup_time():
    import datetime
    now = datetime.datetime.now()
    time_string = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "_" + str(now.hour) + "-" + str(now.minute)
    return time_string