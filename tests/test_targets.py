# test targets
from ngehtutil.target import get_target_list, get_target_info
import unittest


class TestClass(unittest.TestCase):
    def test_target_list(self):
        a = get_target_list()
        self.assertEqual(type(a),list)
        self.assertTrue(len(a)>0)


    def test_target_info(self):
        sl = get_target_list()
        info = get_target_info(sl[0])
        self.assertEqual(type(info),dict)

        with self.assertRaises(ValueError):
            info = get_target_info('aaron')

