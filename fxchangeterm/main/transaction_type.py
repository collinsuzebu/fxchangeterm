
from enum import unique, auto
from .base_enumeration import BaseEnum


@unique
class TransactionType(BaseEnum):
	PAYONEER = auto()
	PAYPAL = auto()
	NETELLER = auto()
	SKRILL = auto()
	PERFECT_MONEY = auto()
	BITCOIN = auto()
