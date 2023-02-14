import unittest
import sys
sys.path.append('$pwd')
from module.toolbox import format, distance


class TestOutils(unittest.TestCase):

	def test_format(self):
		self.assertEqual(format(1.6666667), "1.67")

	def test_distance(self):
		self.assertAlmostEqual(distance(0, 1, 4, 7), 7.2111026)

if __name__ == '__main__':
	unittest.main()