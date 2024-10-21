import re
from typing import List, Optional

from pydantic import BaseModel, Field

from src.constants.psu_type import PSUType
from src.constants.authentication_approach import AuthenticationApproach
from src.models.eb_party import PartyIdentification

_RE_COMBINE_WHITESPACE = re.compile(r"\s+")


class Aspsp(BaseModel):
    name: str
    country: str


class Credential(BaseModel):
    name: str
    title: str
    required: bool
    description: Optional[str] = Field(default=None)
    template: Optional[str] = Field(default=None)


class AuthMethod(BaseModel):
    psu_type: PSUType
    approach: AuthenticationApproach
    hidden_method: bool
    name: Optional[str] = Field(default=None)
    title: Optional[str] = Field(default=None)
    credentials: list[Credential] = Field(default_factory=list)


class AspspData(Aspsp):
    maximum_consent_validity: int
    logo: str
    beta: bool = Field(default=False)
    bic: Optional[str] = None
    required_psu_headers: List[str] = Field(default_factory=list)
    psu_types: List[PSUType] = Field(default_factory=list)
    auth_methods: List[AuthMethod] = Field(default_factory=list)


class EnableBankingAccountOtherIdentification(BaseModel):
    identification: str
    scheme_name: str
    issuer: Optional[str] = Field(default=None)


class EnableBankingAccountIdentification(BaseModel):
    iban: Optional[str] = Field(default=None)
    other: Optional[EnableBankingAccountOtherIdentification] = Field(default=None)


class EnableBankingAccess(BaseModel):
    valid_until: str
    balances: Optional[bool] = Field(default=None)
    transactions: Optional[bool] = Field(default=None)
    accounts: Optional[list[EnableBankingAccountIdentification]] = Field(default=None)


class EnableBankingStartAuthorizationRequest(BaseModel):
    aspsp: Aspsp
    redirect_url: str
    language: str
    state: str
    access: EnableBankingAccess
    psu_id: Optional[str] = Field(default=None)
    psu_type: Optional[str] = Field(default="business")
    auth_method: Optional[str] = Field(default=None)


class EnableBankingStartAuthorizationResponse(BaseModel):
    url: str
    authorization_id: str
    psu_id_hash: Optional[str] = Field(default=None)


class EnableBankingAccount(BaseModel):
    uid: str
    currency: str
    identification_hashes: List[str]
    identification_hash: str
    cash_account_type: str
    account_id: Optional[EnableBankingAccountIdentification] = Field(default=None)
    name: Optional[str] = Field(default=None)


class EnableBankingAuthorizeSessionResponse(BaseModel):
    session_id: str
    accounts: List[EnableBankingAccount]
    aspsp: Aspsp
    psu_type: str
    access: EnableBankingAccess


class AmountType(BaseModel):
    amount: float
    currency: str


class Transaction(BaseModel):
    transaction_amount: AmountType
    credit_debit_indicator: str
    status: str

    entry_reference: Optional[str] = Field(default=None)
    merchant_category_code: Optional[str] = Field(default=None)
    creditor: Optional[PartyIdentification] = Field(default=None)
    debtor: Optional[PartyIdentification] = Field(default=None)

    booking_date: Optional[str] = Field(default=None)
    value_date: Optional[str] = Field(default=None)
    transaction_date: Optional[str] = Field(default=None)

    balance_after_transaction: Optional[AmountType] = Field(default=None)
    reference_number: Optional[str] = Field(default=None)
    remittance_information: Optional[List[str]] = Field(default=None)
    note: Optional[str] = Field(default=None)


class AspspsResponse(BaseModel):
    aspsps: List[AspspData]
