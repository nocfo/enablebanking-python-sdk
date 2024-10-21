from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, Field

from src.constants.account_balance_type import AccountBalanceType
from src.models.aspsp import AmountType


class BalanceResource(BaseModel):
    name: str
    balance_amount: AmountType
    balance_type: AccountBalanceType
    last_change_date_time: Optional[datetime] = Field(default=None)
    reference_date: Optional[date] = Field(default=None)
    last_committed_transaction: Optional[str] = Field(default=None)


class AccountBalances(BaseModel):
    balances: list[BalanceResource]
