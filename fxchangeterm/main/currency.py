from enum import auto, unique
from .base_enumeration import BaseEnum


@unique
class Currency(BaseEnum):
	USD = auto()
	EUR = auto()
	GBP = auto()
	NGN = auto()