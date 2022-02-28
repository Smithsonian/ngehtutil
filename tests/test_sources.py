# test arrays
from multiprocessing.sharedctypes import Value
from ngehtutil.source import get_source_description, get_source_list, \
    get_source_info, get_source_image, get_source_data_file
import unittest
import PIL


def get_default_source():
    return get_source_list()[0]


class TestClass(unittest.TestCase):
    def test_source_list(self):
        a = get_source_list()
        self.assertEqual(type(a),list)
        self.assertTrue(len(a)>0)


    def test_source_info(self):
        sl = get_source_list()
        info = get_source_info(sl[0])
        self.assertEqual(type(info),dict)

        with self.assertRaises(ValueError):
            info = get_source_info('aaron')


    def test_source_description(self):
        sl = get_source_list()
        desc = get_source_description(sl[0])
        self.assertEqual(type(desc),str)

        with self.assertRaises(ValueError):
            info = get_source_description('aaron')


    def test_source_image(self):
        im = get_source_image(get_default_source(),230)
        self.assertEqual(type(im), PIL.PngImagePlugin.PngImageFile)

        with self.assertRaises(ValueError):
            info = get_source_image('aaron',230)

        with self.assertRaises(ValueError):
            info = get_source_image('M87',999)


    def test_source_data_file(self):
        f = get_source_data_file(get_default_source(),230)
        self.assertEqual(type(f), str)

        with self.assertRaises(ValueError):
            f = get_source_data_file('aaron',230)

        with self.assertRaises(ValueError):
            f = get_source_data_file('M87',999)

