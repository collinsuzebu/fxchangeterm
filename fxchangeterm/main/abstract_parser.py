from abc import ABC, abstractmethod


class AbstractBaseParser(ABC):
	"""All parser inherit from AbstractBaseParser"""

	def _skrill_transaction(self, args):
		'''Retrieve data from command line and parse using skrill'''
		pass

	def _perfect_money_transaction(self, args):
		'''Retrieve data from command line and parse using perfect money'''
		pass

	def _neteller_transaction(self, args):
		'''Retrieve data from command line and parse using neteller'''
		pass

	@abstractmethod
	def _bitcoin_transaction(self, args):
		'''Retrieve data from command line and parse using bitcoin'''
		pass

	@abstractmethod
	def _payoneer_transaction(self, args):
		'''Retrieve data from command line and parse using payoneer'''
		pass

	@abstractmethod
	def _paypal_transaction(self, args):
		'''Retrieve data from command line and parse using paypal'''
		pass

	@abstractmethod
	def run(self, args):
		'''Run the parser using the entered arguments from cli'''
		pass

	@abstractmethod
	def default_transaction(self, args):
		'''Sets the default return result when no data is available'''
		pass