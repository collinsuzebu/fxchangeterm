import os
import re
import importlib
import inspect



def _get_all_parsers(dirname):
	files = [f.replace('.py', '') 
			for f in os.listdir(dirname) 
			if not f.startswith('__')]
	return files


def _import_parsers(parserfiles):
	pattern = re.compile('.+parser$', re.I)

	parsers = [
		importlib.import_module('.'+parser, package='fxchangeterm.parsers')
		for parser in parserfiles
		]

	_classes = dict()

	for parser in parsers:
		_classes.update({k: v for k, v in inspect.getmembers(parser) 
						if inspect.isclass(v) and pattern.match(k)
						and not k.lower().startswith('abstract')
						and not k.lower().startswith('base')})

	return _classes


def load(dirname):
	parserfiles = _get_all_parsers(dirname)
	return _import_parsers(parserfiles)
	