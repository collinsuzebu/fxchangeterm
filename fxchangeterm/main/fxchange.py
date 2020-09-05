from datetime import date
from .transaction_type import TransactionType
from .currency import Currency


class FxChangeData:
	def __init__(
		self, 
		buying_rate, 
		selling_rate,
		info='',
		symbol='',
		website='',
		currency=Currency.NGN,
		transaction_type=TransactionType.PAYONEER):

		self._buying_rate = buying_rate
		self._selling_rate = selling_rate
		self._info = info
		self._symbol = symbol
		self._website = website
		self._currency = currency
		self._transaction_type = transaction_type
		self._current_date = date.today()
		self._naira = '{}'.format(u"\N{naira sign}")

	@property
	def info(self):
		return self._info

	@property
	def naira(self):
		return self._naira

	@property
	def website(self):
		return self._website

	@property
	def buying_rate(self):
		return self._buying_rate
	
	@property
	def selling_rate(self):
		return self._selling_rate

	@property
	def currency(self):
		return self._currency

	@property
	def symbol(self):
		return self._symbol
	
	@property
	def transaction_type(self):
		return self._transaction_type.value

	@property
	def current_date(self):
		return self._current_date

	def __str__(self):
		return (f'{"-"*70}\n'
				f'{self._current_date}\n'
				f'{self._transaction_type.value}\n'
				f'Buy @ {self._naira}{self._buying_rate}/{self._symbol}\n'
				f'Sell @ {self._naira}{self._selling_rate}/{self._symbol}\n'
				f'\n'
				f'Phone: {self._info[0]}\n'
				f'Email: {self._info[1]}\n'
				f'Address: {self._info[2]}\n')