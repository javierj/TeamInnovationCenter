import unittest

from tappraisal import _get_full_filename
from utilities import Cache


class Test_Get_Full_Filename(unittest.TestCase):

    def test_filename_without_basedir(self):
        filename = _get_full_filename("data.txt")
        #print(filename)
        self.assertEqual("G:\code\python\TeamInnovationCenter\data.txt", filename)  # add assertion here

    def test_filename_with_basedir(self):
        filename = _get_full_filename("radar9.txt", "polls")
        #print(filename)
        self.assertEqual("G:\code\python\TeamInnovationCenter\polls\\radar9.txt", filename)  # add assertion here


class Test_Cache(unittest.TestCase):

    def test_key_not_in_cache(self):
        result = Cache.get("No exist")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
