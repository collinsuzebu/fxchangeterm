from fxchangeterm.main import TransactionType
from fxchangeterm.main import FxChangeData
from fxchangeterm.main import WebRequest
from fxchangeterm.main import Currency
from fxchangeterm.main import CurrencyConverter
from fxchangeterm.main import BaseParser

import re
import bs4
from bs4 import BeautifulSoup


class HolarexParser(BaseParser):
	"""docstring for HolarexParser"""
	def __init__(self):
		super(HolarexParser, self).__init__()

		self._base_url = "https://holarex.net"
		self._request = WebRequest(self._base_url)


	def _transaction_helper(self):

		criteria = {
			"perfectmoneybuy": "span",
			"perfectmoneysell": "span",
			
			"bitcoinbuy": "span",
			"bitcoinsell": "span",
			
			"ethereumbuy": "span",
			"ethereumsell": "span",
			
			"bitcoincashbuy": "span",
			"bitcoincashsell": "span",
		}

		content = self._request.fetch_data()
		content = content.replace("&#8358", "#")  # remove Naira Symbol

		self._bs = BeautifulSoup(content, "html.parser")

		container = self._bs.find("table", class_="table plan-table")


		if container is not None:

			transaction_offers = self._parse(container, criteria, method="id")

			if len(transaction_offers) < 1:
				raise Exception("Could not parse any transaction")

		else:
			transaction_offers = [{"padding: 10px;":''}] * 5

		return transaction_offers


	def _get_additional_info(self):
		container = self._bs.find_all("ul", class_="listitem-list")[-1]
		container = container.find_all("li")

		info = [i.get_text().strip() for i in container]
		email = container[1].find("span", class_="__cf_email__")["data-cfemail"]


		phone = self.strip_whitespace(info[2])
		email = self.decode_email(email)
		address = info[0]

		return phone, email, address

	def _payoneer_transaction(self, args):
		return None

	def _bitcoin_transaction(self, args):
		return None
	
	def _paypal_transaction(self, args):
		transaction_offer = self._transaction_helper()[0]
		
		sell_at = transaction_offer["perfectmoneybuy"]
		buy_at = transaction_offer["perfectmoneysell"]

		phone, email, address = self._get_additional_info()

		self._currency_converter._new_currency = args.currency

		perfect_money_rate = FxChangeData(
			self._currency_converter.convert(buy_at),
			self._currency_converter.convert(sell_at),
			info=[phone, email, address],
			website=self._base_url,
			transaction_type=TransactionType.PERFECT_MONEY,
			symbol=self._currency_converter._new_currency.value,
		)

		return perfect_money_rate


	def _bitcoin_transaction(self, args):
		transaction_offer = self._transaction_helper()[0]
		
		sell_at = transaction_offer["bitcoinbuy"]
		buy_at = transaction_offer["bitcoinsell"]

		phone, email, address = self._get_additional_info()

		self._currency_converter._new_currency = args.currency

		bitcoin_rate = FxChangeData(
			self._currency_converter.convert(buy_at),
			self._currency_converter.convert(sell_at),
			info=[phone, email, address],
			website=self._base_url,
			transaction_type=TransactionType.BITCOIN,
			symbol=self._currency_converter._new_currency.value,
		)

		return bitcoin_rate
	

	def default_transaction(self, args):
		transaction_offer = self._transaction_helper()
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