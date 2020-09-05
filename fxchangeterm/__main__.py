import sys
import concurrent.futures
from argparse import ArgumentParser

from fxchangeterm.main import load_parser
from fxchangeterm.main import rich_formater
from fxchangeterm.main import TransactionType
from fxchangeterm.main import Currency
from fxchangeterm.main import SetCurrencyAction




def _validate_input_args(args):
    if args.transaction_option is None:
        err_msg = ('One of these arguments must be used: '
                   '-p/--payoneer, -pp/--paypal, -s/--skrill,'
                   '-pm/--perfect_money, -n/--neteller, -b/--bitcoin')

        print(f'{argparser.prog}: error: {err_msg}', file=sys.stderr)
        sys.exit()

parsers = load_parser.load('./fxchangeterm/parsers')


argparser = ArgumentParser(
    prog='fxchangeterm',
    description='Foreign exchange rate for freelancers on terminal')

required = argparser.add_argument_group('required arguments')
required.add_argument('-p', '--parser',
    choices=parsers.keys(),
    required=False,
    dest='parser',
    help=('Specify which parser is going to be used to '
           'scrape foreign exchanger information.'))

currency_values = [name.lower() for name, value in Currency.__members__.items()]

argparser.add_argument('-c', '--currency',
    choices=currency_values,
    required=False,
    action=SetCurrencyAction,
    default=Currency.USD,
    dest='currency',
    help=('Specify the currency that will be used to display '
    'the fxchange rate.'))


argparser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s 1.0')


argparser.add_argument('-b', '--bitcoin',
                       dest='transaction_option',
                       action='store_const',
                       const=TransactionType.BITCOIN,
                       help='Shows the fxchange rate for bitcoin')


argparser.add_argument('-n', '--neteller',
                       dest='transaction_option',
                       action='store_const',
                       const=TransactionType.NETELLER,
                       help='Shows the fxchange rate for neteller')

argparser.add_argument('-s', '--skrill',
                       dest='transaction_option',
                       action='store_const',
                       const=TransactionType.SKRILL,
                       help='Shows the fxchange rate for skrill')

argparser.add_argument('-pm', '--perfect_money',
                       dest='transaction_option',
                       action='store_const',
                       const=TransactionType.PERFECT_MONEY,
                       help='Shows the fxchange rate for perfect money')

argparser.add_argument('-pp', '--paypal',
                       dest='transaction_option',
                       action='store_const',
                       const=TransactionType.PAYPAL,
                       help='Shows the fxchange rate for paypal')

argparser.add_argument('-py', '--payoneer',
						dest='transaction_option',
						action='store_const',
						const=TransactionType.PAYONEER,
						help='Shows the fxchange rate for payoneer')



args = argparser.parse_args()
_validate_input_args(args)
rich_display = {}



del parsers['MytopExchangeParser']




with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = {executor.submit(_parser().run, args):key for key, _parser in parsers.items()}
    
    for future in concurrent.futures.as_completed(futures):
      rich_display.update({futures[future]:future.result()})
      

rich_formater.format_table(args, rich_display)

# cls = parsers[args.parser]

# parser = cls()
# results = parser.run(args)

# for result in results:
#     print(result)