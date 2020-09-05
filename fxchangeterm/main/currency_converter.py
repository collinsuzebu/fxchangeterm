
import json

from .currency import Currency

class CurrencyConverter:
	def __init__(self, default_currency, new_currency=None):
		self._default_currency = default_currency
		self._new_currency = new_currency

		self._converters = {
			Currency.USD: self._to_usd,
			Currency.EUR: self._to_eur,
			Currency.GBP: self._to_gbp,
			Currency.NGN: self._to_ngn,
		}


	def convert(self, currency):

		try:
			currency = float(currency)
		except ValueError:
			return 0

		if (self._new_currency == self._default_currency or 
				self._new_currency is None):
			return self.format_currency(currency)

		func = self._converters[self._new_currency]
		result = func(currency)

		return self.format_currency(result)
		

	def format_currency(self, value):
		return int(value) if value.is_integer() else f'{value:,.2f}'


	def currency_rate(self, currency):
		from fxchangeterm.main import WebRequest

		req = WebRequest("https://api.exchangeratesapi.io/latest?base=USD")
		data = json.loads(req.fetch_data())
		rates = data["rates"]

		return rates[currency]

	def _to_usd(self, usd):
		return usd
	
	def _to_eur(self, usd):
		result = usd / self.currency_rate("EUR")
		return result

	def _to_gbp(self, usd):
		result = usd / self.currency_rate("GBP")
		return result

	def _to_ngn(self, usd):
		return usd