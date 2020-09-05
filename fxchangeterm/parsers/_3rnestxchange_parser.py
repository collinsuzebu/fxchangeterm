from fxchangeterm.main import TransactionType
from fxchangeterm.main import FxChangeData
from fxchangeterm.main import WebRequest
from fxchangeterm.main import Currency
from fxchangeterm.main import CurrencyConverter
from fxchangeterm.main import BaseParser

import re
import bs4
from bs4 import BeautifulSoup


class RnestxchangeParser(BaseParser):
    """docstring for RnestxchangeParser"""

    def __init__(self):
        super(RnestxchangeParser, self).__init__()

        self._base_url = "https://3rnestxchange.com"
        self._request = WebRequest(self._base_url)


    def _transaction_helper(self):

        criteria = {
            "padding: 10px;": "span",
        }

        content = self._request.fetch_data()
        content = content.replace("&#8358", "#")  # remove Naira Symbol

        self._bs = BeautifulSoup(content, "html.parser")

        container = self._bs.find("marquee", scrollamount="3")

        if container is not None:

            transaction_offers = self._parse(container, criteria, method="style")

            if len(transaction_offers) < 1:
                raise Exception("Could not parse any transaction")

        else:
            transaction_offers = [{"padding: 10px;":''}] * 5

        return transaction_offers

    def _details_helper(self, transaction_offer):
        return self._get_information(transaction_offer["padding: 10px;"])

    def _addendum(self):

        criteria = {
            "fa fa-phone": "i",
            "fa fa-envelope": "i",
            "fa fa-map-marker": "i",
        }
        container = self._bs.find("div", class_="foot-contact")
        additional_info = [{'false':'false'}]

        if container:
            additional_info = self._parse(container, criteria, method="class")
        
        return self._get_additional_info(additional_info[0])

    def _get_information(self, text):
        sell_regex = re.compile(r"sell\s?\@?\s?#?\s?\s+(\d+)", re.I)
        buy_regex = re.compile(r"buy\s?#?\s?\s+(\d+)", re.I)
        transaction_regex = re.compile(r"(\w+\s?\w+).?", re.I)

        if not text:
            return (0,0,'N/A')

        buy = buy_regex.search(text).groups()[0]
        sell = sell_regex.search(text).groups()[0]
        transaction = transaction_regex.search(text).group().strip()

        return buy, sell, transaction

    def _get_additional_info(self, info):
        phone = info.get("fa fa-phone")
        email = info.get("fa fa-envelope")
        address = info.get("fa fa-map-marker")

        return phone, email, address

    def _payoneer_transaction(self, args):

        transaction_offer = self._transaction_helper()[2]
        sell_at, buy_at, transac = self._details_helper(transaction_offer)
        phone, email, address = self._addendum()

        self._currency_converter._new_currency = args.currency

        payoneer_rate = FxChangeData(
            self._currency_converter.convert(buy_at),
            self._currency_converter.convert(sell_at),
            info=[phone, email, address],
            website=self._base_url,
            symbol=self._currency_converter._new_currency.value,
        )

        return payoneer_rate

    def _paypal_transaction(self, args):

        transaction_offer = self._transaction_helper()[1]
        sell_at, buy_at, transac = self._details_helper(transaction_offer)
        phone, email, address = self._addendum()

        self._currency_converter._new_currency = args.currency

        paypal_rate = FxChangeData(
            self._currency_converter.convert(buy_at),
            self._currency_converter.convert(sell_at),
            info=[phone, email, address],
            website=self._base_url,
            transaction_type=TransactionType.PAYPAL,
            symbol=self._currency_converter._new_currency.value,
        )

        return paypal_rate

    def _skrill_transaction(self, args):
        transaction_offer = self._transaction_helper()[0]
        sell_at, buy_at, transac = self._details_helper(transaction_offer)
        phone, email, address = self._addendum()

        self._currency_converter._new_currency = args.currency

        skrill_rate = FxChangeData(
            self._currency_converter.convert(buy_at),
            self._currency_converter.convert(sell_at),
            info=[phone, email, address],
            website=self._base_url,
            transaction_type=TransactionType.SKRILL,
            symbol=self._currency_converter._new_currency.value,
        )

        return skrill_rate

    def _perfect_money_transaction(self, args):

        transaction_offer = self._transaction_helper()[3]
        sell_at, buy_at, transac = self._details_helper(transaction_offer)
        phone, email, address = self._addendum()

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

    def _neteller_transaction(self, args):

        transaction_offer = self._transaction_helper()[1]
        sell_at, buy_at, transac = self._details_helper(transaction_offer)
        phone, email, address = self._addendum()

        self._currency_converter._new_currency = args.currency

        netteller_rate = FxChangeData(
            self._currency_converter.convert(buy_at),
            self._currency_converter.convert(sell_at),
            info=[phone, email, address],
            website=self._base_url,
            transaction_type=TransactionType.NETELLER,
            symbol=self._currency_converter._new_currency.value,
        )

        return netteller_rate

    def _bitcoin_transaction(self, args):

        transaction_offer = self._transaction_helper()[4]
        sell_at, buy_at, transac = self._details_helper(transaction_offer)
        phone, email, address = self._addendum()

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
        phone, email, address = self._addendum()
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
