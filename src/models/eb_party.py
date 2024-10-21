from typing import Optional

from pydantic import BaseModel, Field

from src.constants.address_type import AddressType
from src.constants.scheme_name import SchemeName


class PostalAddress(BaseModel):
    address_type: Optional[AddressType] = Field(default=None)
    department: Optional[str] = Field(default=None)
    sub_department: Optional[str] = Field(default=None)
    street_name: Optional[str] = Field(default=None)
    building_number: Optional[str] = Field(default=None)
    post_code: Optional[str] = Field(default=None)
    added: Optional[str] = Field(default=None)
    town_name: Optional[str] = Field(default=None)
    country_sub_division: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    address_line: Optional[list[str]] = Field(default_factory=list)


class GenericIdentification(BaseModel):
    identification: str
    scheme_name: SchemeName
    issuer: Optional[str] = Field(default=None)


class ContactDetails(BaseModel):
    email_address: Optional[str] = Field(default=None)
    phone_number: Optional[str] = Field(default=None)


class PartyIdentification(BaseModel):
    name: Optional[str] = Field(default=None)
    postal_address: Optional[PostalAddress] = Field(default=None)
    organisation_id: Optional[GenericIdentification] = Field(default=None)
    private_id: Optional[GenericIdentification] = Field(default=None)
    contact_details: Optional[ContactDetails] = Field(default=None)
