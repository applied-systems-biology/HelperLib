import unittest

from ddt import ddt, data

from helper_lib.filelib import _is_in_extensions as f


@ddt
class TestIsInExtensions(unittest.TestCase):
    def test_arguments(self):
        self.assertRaises(TypeError, f)

    def test_return_type(self):
        self.assertIsInstance(f("Cell00.tif", []), bool)

    @data(
        ('cell00.tif', [], False),
        ('input_45.png', ['tif', 'png'], True),
        ('input_46.0', ['tif', 'png'], False),
        ('cell23.tif', ['tif', 'png'], True),
        ('cell23.tif', ['csv', 'png'], False)
    )
    def test_extensions(self, case):
        input_name, ext, result = case
        self.assertEqual(f(input_name, ext), result)

if __name__ == '__main__':
    unittest.main()
