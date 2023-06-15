

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


