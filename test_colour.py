import unittest
from colour import Color


class TestColor(unittest.TestCase):

    def test_hex_builtin_on_color(self):
        c = Color('red')
        self.assertEqual('#ff0000', hex(c))

        c = Color(rgb=(0, 0.5, 1))
        self.assertEqual('#007fff', hex(c))


if __name__ == '__main__':
    unittest.main()
