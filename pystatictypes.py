from inspect import signature, Parameter, _empty
from collections import OrderedDict

def _bad_pos_type(pos, func_name):
	return TypeError('received unexpected type for parameter at position %d in %s' % (pos + 1, func_name))

def _bad_key_type(key, func_name):
	return TypeError('received unexpected type for parameter with key "%s" in %s' % (key, func_name))

def _missing_annotation(pos, func_name):
	return SyntaxError('missing annotation for parameter at position %d in %s' % (pos + 1, func_name))

"""
List of known issues:
	- NoneType annotations not parsed properly
	- Some weird behaviour with running the function too early when
	positional kwargs are used
"""

#next upgrade will be for statically typing elements of containers
#cheating for error handling when receiving weird arguments, just call the function and it will handle the error pythonically
def typed(func):
	def rv(*args, **kwargs):
		if len(args) < len(rv._pos_types):
			return func(*args, **kwargs)
		if not rv._has_var_pos_args and len(args) != len(rv._pos_types) + rv._pos_kw_overlap_len:
			return func(*args, **kwargs)
		#impossible to have a parameter be both kw and positional if there is a var_pos argument
		#so ignoring that case is reasonable
		if len(kwargs) < len(rv._kw_types) - rv._pos_kw_overlap_len:
			return func(*args, **kwargs)
		if rv._has_var_pos_args:
			if not rv._has_var_kw_args and len(kwargs) > len(rv._kw_types):
				return func(*args, **kwargs)
		elif not rv._has_var_kw_args and len(kwargs) > len(rv._kw_types) + len(rv._pos_types) - len(args):
			return func(*args, **kwargs)
		for i in range(len(rv._pos_types)):
			#placeholder until parsing annotations done properly
			#similarly for all type checking
			if type(args[i]) != rv.pos_types[i]:
				raise _bad_pos_type(i, func.__name__)
		kw_iterable = iter(rv._kw_types)
		visited_keys = set()
		for i in range(len(rv._pos_types), len(rv._pos_types) + rv._pos_kw_overlap_len):
			key = next(kw_iterable)
			if key in visited_keys:
				return func(*args, **kwargs)
			if (type(args[i]) != rv._kw_types[key]):
				raise _bad_pos_type(i + len(rv._pos_types), func.__name__)
			visited_keys.add(key)
		for key in kwargs:
			if key in visited_keys:
				return func(*args, **kwargs)
			if key not in rv._kw_types and not rv._has_var_kw_args:
				return func(*args, **kwargs)
			if key in rv._kw_types:
				if(type(kwargs[key]) != rv.kw_types[key]):
					raise _bad_key_type(key, func.__name__)
		func_rv = func(*args, **kwargs)
		if type(func_rv) != rv._rv_type:
			raise TypeError(func.__name__, 'evaluated to unexpected return type', type(func_rv))
		return func_rv

	#2 containers for parameters
	#positional, keyword
	#positional is list
	#keyword is ordered dict
	#also type the return annotation
	#also contatins booleans for if variadic positional arguments and/or keyword arguments are allowed
	#finally contains length of positional/keyword intersection in kw_types
	rv._pos_types = []
	rv._kw_types = OrderedDict()
	rv._has_var_pos_args = False
	rv._has_var_kw_args = False
	rv._pos_kw_overlap_len = 0
	sig = signature(func)
	parameters = sig.parameters
	if sig.return_annotation == _empty:
		raise SyntaxError('missing return type annotation for function', func.__name__)
	rv._rv_type = sig.return_annotation
	param_iter = iter(parameters)
	for i in range(len(parameters)):
		key = next(param_iter)
		param = parameters[key]
		if param.kind == Parameter.POSITIONAL_ONLY:
			#placeholder until parsing annotations done properly
			#similarly for storing any annotation
			#TODO error out if annotation is not a type
			if param.annotation == _empty:
				raise _missing_annotation(i, func.__name__)
			rv._pos_types.append(param.annotation)
		elif param.kind == Parameter.POSITIONAL_OR_KEYWORD:
			if param.annotation == _empty:
				raise _missing_annotation(i, func.__name__)
			rv._kw_types[key] = param.annotation
			rv._pos_kw_overlap_len += 1
		elif param.kind == Parameter.VAR_POSITIONAL:
			rv._has_var_pos_args = True
		elif param.kind == Parameter.KEYWORD_ONLY:
			if param.annotation == _empty:
				raise _missing_annotation(i, func.__name__)
			rv._kw_types[key] = param.annotation
		else:
			rv._has_var_kw_args = True
	return rv
