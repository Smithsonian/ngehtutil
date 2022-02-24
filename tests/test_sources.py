# test arrays
from ngehtutil.sourcemodel.sources import get_source_description, get_source_list, \
    get_default_source, get_source_info, get_source_image
import unittest
import PIL
import numpy

class TestClass(unittest.TestCase):
    def test_source_list(self):
        a = get_source_list()
        self.assertEqual(type(a),list)
        self.assertTrue(len(a)>0)

    def test_default_source(self):
        d = get_default_source()
        self.assertEqual(type(d),str)

    def test_source_info(self):
        sl = get_source_list()
        info = get_source_info(sl[0])
        self.assertEqual(type(info),dict)

    def test_source_description(self):
        sl = get_source_list()
        desc = get_source_description(sl[0])
        self.assertEqual(type(desc),str)

    def test_source_image(self):
        im = get_source_image(get_default_source(),230)
        self.assertEqual(type(im), PIL.PngImagePlugin.PngImageFile)
