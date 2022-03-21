# test arrays
from multiprocessing.sharedctypes import Value
from ngehtutil.source import Source
import unittest
import PIL


def get_default_source():
    return Source.get_source_list()[0]

class TestClass(unittest.TestCase):
    def test_source_list(self):
        a = Source.get_list()
        self.assertEqual(type(a),list)
        self.assertTrue(len(a)>0)


    def test_source_info(self):
        sl = Source.get_list()
        info = Source.from_name(sl[0])
        self.assertEqual(type(info),Source)

        with self.assertRaises(KeyError):
            info = Source.from_name('aaron')


    def test_source_description(self):
        sl = Source.get_list()
        s = Source.from_name(sl[0])
        desc = s.description
        self.assertEqual(type(desc),str)


    def test_source_image(self):
        sl = Source.get_list()
        s = Source.from_name(sl[0])
        im = s.picture(230)
        self.assertEqual(type(im), PIL.PngImagePlugin.PngImageFile)

        with self.assertRaises(ValueError):
            info = s.picture(999)


    def test_source_data_file(self):
        sl = Source.get_list()
        s = Source.from_name(sl[0])

        f = s.fits(230)
        self.assertEqual(type(f), str)

        with self.assertRaises(ValueError):
            f = s.fits(999)


    def test_default_source(self):
        s = Source.get_default()
        self.assertEqual(type(s),Source)