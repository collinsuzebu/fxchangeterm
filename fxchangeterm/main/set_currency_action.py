from argparse import Action
from fxchangeterm.main import Currency


class SetCurrencyAction(Action):
	def __call__(self, parser, namespace, values, option_string=None):
		currency = Currency[values.upper()]
		setattr(namespace, self.dest, currency)
