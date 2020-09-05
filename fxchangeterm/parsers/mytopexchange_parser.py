from fxchangeterm.main import TransactionType
from fxchangeterm.main import FxChangeData
from fxchangeterm.main import WebRequest
from fxchangeterm.main import Currency
from fxchangeterm.main import CurrencyConverter
from fxchangeterm.main import BaseParser

import re
import bs4
from bs4 import BeautifulSoup


class MytopExchangeParser(BaseParser):
	"""docstring for MytopExchangeParser"""
	def __init__(self):
		pass


	def _payoneer_transaction(self, args):
		pass


	def _paypal_transaction(self, args):
		pass


	def _skrill_transaction(self, args):
		pass


	def _perfect_money_transaction(self, args):
		pass


	def _neteller_transaction(self, args):
		pass


	def _bitcoin_transaction(self, args):
		pass


	def run(self, args):
		return ['result']