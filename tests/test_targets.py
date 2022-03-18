# test targets
from ngehtutil.target import Target
import unittest


class TestClass(unittest.TestCase):
    def test_target_list(self):
        a = Target.get_target_list()
        self.assertEqual(type(a),list)
        self.assertTrue(len(a)>0)


    def test_target_info(self):
        a = Target.get_target_list()
        info = Target.get(a[0])
        self.assertEqual(type(info),Target)

        with self.assertRaises(KeyError):
            info = Target.get('aaron')

