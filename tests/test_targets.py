# test targets
from ngehtutil.target import Target
import unittest


class TestClass(unittest.TestCase):
    def test_target_list(self):
        a = Target.get_list()
        self.assertEqual(type(a),list)
        self.assertTrue(len(a)>0)


    def test_target_info(self):
        a = Target.get_list()
        info = Target.from_name(a[0])
        self.assertEqual(type(info),Target)

        with self.assertRaises(KeyError):
            info = Target.from_name('aaron')

    def test_default_target(self):
        t = Target.get_default_target()
        self.assertEqual(type(t),Target)

