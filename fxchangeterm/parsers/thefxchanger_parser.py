from fxchangeterm.main import TransactionType
from fxchangeterm.main import FxChangeData
from fxchangeterm.main import WebRequest
from fxchangeterm.main import Currency
from fxchangeterm.main import CurrencyConverter
from fxchangeterm.main import BaseParser

import re
import bs4
from bs4 import BeautifulSoup

class TheFxChangerParser(BaseParser):
	"""docstring for TheFxChangerParser"""
	def __init__(self):
		super(TheFxChangerParser, self).__init__()

		self._base_url = 'http://thefxchanger.com'
		self._request = WebRequest(self._base_url)
	

	def _get_data(self, dom, search_items, method):
		scraped_data = {}

		for key, value in search_items.items():
			
			if method == 'img':
				result = dom.find(value, class_=key)
				data = None if result is None else self._get_transaction_type(result.attrs['src'])
			
			if method == 'class':
				result = dom.find(value, class_=key)
				data = None if result is None else result.get_text()
		
			if data is not None:
				scraped_data[key] = data
		return scraped_data


	def _get_transaction_type(self, src):
		t = src.split('/')[-1]
		return re.search(r'\w+', t).group().upper()

	
	def _offers_getter(self):

		price_criteria = {'penci-ibox-content':'p'}
		img_criteria = {re.compile(r"wp-image-\d+ aligncenter"):'img'}
		
		content = self._request.fetch_data()
		self._bs = BeautifulSoup(content, 'html.parser')

		container = self._bs.find('div', id="rate")
		
		price_offers = self._parse(container, price_criteria, method='class')
		tranc_offers = self._parse(container, img_criteria, method='img')

		if len(price_offers)  != len(tranc_offers):
			raise Exception('Could not parse any transaction')

		return price_offers, tranc_offers
	

	def _get_details_string(self, transaction_offer):
		return self._get_information(transaction_offer['penci-ibox-content'])


	def _get_information(self, text):
		sell_regex = re.compile(r'sell\:?\s?\@?\s?#?\s?\s+(\d+)', re.I)
		buy_regex = re.compile(r'buy\:?\s?\@?\s?#?\s?\s+(\d+)', re.I)
		transaction_regex = re.compile(r'(\w+\s?\w+).?', re.I)

		buy = buy_regex.search(text).groups()[0]
		sell = sell_regex.search(text).groups()[0]

		return buy, sell
	

	def _get_additional_info(self):


		address = self._bs.find("h3", class_="penci-ibox-title", 
								  string="ADDRESS").next_sibling.text

		email = self._bs.find("h3", class_="penci-ibox-title", 
						  string="EMAIL").next_sibling.text

		phone = self._bs.find("h3", class_="penci-ibox-title", 
								  string="PHONE").next_sibling.text

		return phone, email, address


	def _payoneer_transaction(self, args):

		price_offer = self._offers_getter()[0][1]
		tranc_offer = self._offers_getter()[1][1]

		sell_at, buy_at = self._get_details_string(price_offer)
		phone, email, address = self._get_additional_info()

		self._currency_converter._new_currency = args.currency

		payoneer_rate = FxChangeData(
				self._currency_converter.convert(buy_at),
				self._currency_converter.convert(sell_at),
				info = [phone, email, address],
				website = self._base_url,
				symbol = self._currency_converter._new_currency.value

			)

		return payoneer_rate


	def _paypal_transaction(self, args):
		
		price_offer = self._offers_getter()[0][2]
		tranc_offer = self._offers_getter()[1][1]

		sell_at, buy_at = self._get_details_string(price_offer)
		phone, email, address = self._get_additional_info()

		self._currency_converter._new_currency = args.currency

		paypal_rate = FxChangeData(
				self._currency_converter.convert(buy_at),
				self._currency_converter.convert(sell_at),
				info = [phone, email, address],
				website = self._base_url,
				symbol = self._currency_converter._new_currency.value

			)

		return paypal_rate


	def _bitcoin_transaction(self, args):
		
		price_offer = self._offers_getter()[0][0]

		sell_at, buy_at = self._get_details_string(price_offer)
		phone, email, address = self._get_additional_info()

		self._currency_converter._new_currency = args.currency

		bitcoin_rate = FxChangeData(
				self._currency_converter.convert(buy_at),
				self._currency_converter.convert(sell_at),
				info = [phone, email, address],
				website = self._base_url,
				symbol = self._currency_converter._new_currency.value

			)

		return bitcoin_rate


	def default_transaction(self, args):
		price_offer = self._offers_getter()
		phone, email, address = self._get_additional_info()
		self._currency_converter._new_currency = args.currency

		# website has no data
		default_rate = FxChangeData(
			self._currency_converter.convert(0),
			self._currency_converter.convert(0),
			info=[phone, email, address],
			website=self._base_url,
			transaction_type=args.transaction_option,
			symbol=self._currency_converter._new_currency.value,
		)

		return default_rate


	def run(self, args):
		self._transaction_type = args.transaction_option
		transaction_function = self._transaction[args.transaction_option]
		transc = transaction_function(args)

		if transc is None:
			return self.default_transaction(args)

		return transc