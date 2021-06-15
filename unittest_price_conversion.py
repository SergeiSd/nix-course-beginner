import unittest
import price_conversion as ps


class TestConversion(unittest.TestCase):

    def test_conversion(self):
        self.assertEqual(ps.conversion(22.32131), 22.32)
        self.assertEqual(ps.conversion(58.60125), 58.6)
        self.assertEqual(ps.conversion(34.0), 34)


if __name__ == '__main__':
    unittest.main()
