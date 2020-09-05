from fxchangeterm.main import Currency
from fxchangeterm.main import TransactionType
from fxchangeterm.main import CurrencyConverter
from fxchangeterm.main import AbstractBaseParser

import bs4


class BaseParser(AbstractBaseParser):
	def __init__(self):
		self._transaction = {
			TransactionType.PAYONEER: self._payoneer_transaction,
			TransactionType.PAYPAL: self._paypal_transaction,
			TransactionType.SKRILL: self._skrill_transaction,
			TransactionType.BITCOIN: self._bitcoin_transaction,
			TransactionType.NETELLER: self._neteller_transaction,
			TransactionType.PERFECT_MONEY: self._perfect_money_transaction,
			
		}
		self._currency_converter = CurrencyConverter(Currency.USD)

	
	def strip_whitespace(self, string):
		return string.replace(" ", "")


	def decode_email(self, email):
	    binr = int(email[:2], 16)
	    decoded_email = ""

	    for i in range(2, len(email)-1, 2):
	        decoded_email += chr(int(email[i:i+2], 16)^binr)

	    return decoded_email

	
	def _get_data(self, dom, search_items, method='class'):
		scraped_data = {}

		for key, value in search_items.items():
			
			if method == 'style':
				result = dom.find(value, style=key)
				data = None if result is None else result.get_text()
			
			if method == 'class':
				result = dom.find(value, class_=key)
				data = None if result is None else result.next_sibling.get_text()

			if method == 'id':
				result = dom.find(value, id=key)
				data = None if result is None else result.get_text()
		
			if data is not None:
				scraped_data[key] = data
		return scraped_data


	def _parse(self, dom, criteria, method):
		results = [self._get_data(item, criteria, method) 
					for item in dom.children 
					if not isinstance(item, bs4.element.NavigableString)]
		
		return [result for result in results if result]