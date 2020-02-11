import sys
import unittest

from pystatictypes import typed

@typed
def test1(a:int, b:int) -> int:
	return a + b

class Test1(unittest.TestCase):

	def test_expected(self):
		self.assertEqual(test1(1, 2), 3)

	def test_wrong_type_arg1(self):
		self.assertRaises(TypeError, test1, 'a', 2)

	def test_too_few_args(self):
		self.assertRaises(TypeError, test1, 'a')

	def test_too_few_args(self):
		self.assertRaises(TypeError, test1, 2)

	def test_expected_kwargs(self):
		self.assertEqual(test1(1, b=2), 3)

	def test_unexpected_kwarg_val(self):
		self.assertRaises(TypeError, test1, 1, b='a')

	def test_unexpected_kwarg(self):
		self.assertRaises(TypeError, test1, b=1, c=3)

	def test_duplicate_vals(self):
		self.assertRaises(TypeError, test1, 1, a=2)

def test2(a, b) ->int:
	return a + b

class Test2(unittest.TestCase):

	def test_no_param_annotation(self):
		self.assertRaises(SyntaxError, typed, test2)

@typed
def test3(a:int, b:int) -> None:
	pass

class Test3(unittest.TestCase):

	def test_expected(self):
		self.assertEqual(test3(1, 2), None)

class FooType:
	def __init__(self, data):
		self.data = data

	def __eq__(self, other):
		if type(other) == FooType:
			return self.data == other.data
		return self.data == other

@typed
def test4(a:int, b:int) -> FooType:
	return FooType(max(a, b))

class Test4(unittest.TestCase):

	def test_expected(self):
		self.assertEqual(test4(4, 5), 5)


unittest.main()
