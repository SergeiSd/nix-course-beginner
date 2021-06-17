import unittest
import chunked_list as cl


class TestConversion(unittest.TestCase):

    def test_chunked(self):
        self.assertEqual(cl.chunked(lst=[1, 2, 3, 4], n=1),
                         [[1, 2, 3, 4]])
        self.assertEqual(cl.chunked(lst=[1, 2, 3, 4], n=2),
                         [[1, 2], [3, 4]])
        self.assertEqual(cl.chunked(lst=[1, 2, 3, 4], n=3),
                         [[1], [2, 3], [4]])
        self.assertEqual(cl.chunked(lst=[1, 2, 3, 4], n=4),
                         [[1], [2], [3], [4]])
        self.assertEqual(cl.chunked(lst=[1, 2, 3, 4], n=5), None)
        self.assertEqual(cl.chunked(lst=[1, 2, 3, 4], n=-1), None)


if __name__ == '__main__':
    unittest.main()
