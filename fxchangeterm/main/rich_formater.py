
from rich.console import Console
from rich.table import Column, Table
from fxchangeterm.main import TransactionType

console = Console()
HEADER = '\n\n'

def format_table(args, tdata):

	title = f'{HEADER}[bold]{args.transaction_option}[/bold]'
	
	table = Table(title=title, show_header=True,
				  header_style="bold magenta",
				  show_lines=True,
				  caption="Trade with care")

	table.add_column("", width=12, overflow='fold')
	table.add_column("Date", style="dim", width=10)
	table.add_column("We sell@", justify="right",)
	table.add_column("We buy@", justify="right",)
	table.add_column("Phone", justify="right",)
	table.add_column("Email", justify="right", width=12, overflow='fold')
	table.add_column("Website", justify="right", overflow='fold')
	table.add_column("Address", justify="right", width=16, overflow='fold')

	for key, data in tdata.items():

		table.add_row(
			f'{clear_parser(key)}',
			f'{data.current_date}',
			f'{data.naira}{data.buying_rate}/{data.symbol}',
			f'{data.naira}{data.selling_rate}/{data.symbol}',
			f'{data.info[0]}',
			f'{data.info[1]}',
			f'{data.website}',
			f'{data.info[2]}',
		)

	console.print(table, justify="center")


def clear_parser(string):
	return string.replace('Parser', '')