import sys
import unittest

sys.path.append('./../')
from pystatictypes import typed

@typed
def foo(a:int, b:int) -> int:
	return a + b

class Test1(unittest.TestCase):

	def test_expected(self):
		self.assertEqual(foo(1, 2), 3)

	def test_wrong_type_arg1(self):
		self.assertRaises(TypeError, foo, 'a', 2)

	def test_too_few_args(self):
		self.assertRaises(TypeError, foo, 'a')

	def test_too_few_args(self):
		self.assertRaises(TypeError, foo, 2)

	def test_expected_kwargs(self):
		self.assertEqual(foo(1, b=2), 3)

	def test_duplicate_vals(self):
		self.assertRaises(TypeError, foo, 1, a=2)

unittest.main()
