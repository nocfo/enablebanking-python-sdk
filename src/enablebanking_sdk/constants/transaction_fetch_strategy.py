from enum import StrEnum


class TransactionsFetchStrategy(StrEnum):
    DEFAULT = "default"
    LONGEST = "longest"
