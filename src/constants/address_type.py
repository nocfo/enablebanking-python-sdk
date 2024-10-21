from enum import StrEnum


class AddressType(StrEnum):
    # fmt: off
    BUSINESS       = "Business"
    CORRESPONDENCE = "Correspondence"
    DELIVERY_TO    = "DeliveryTo"
    MAIL_TO        = "MailTo"
    PO_BOX         = "POBox"
    POSTAL         = "Postal"
    RESIDENTIAL    = "Residential"
    STATEMENT      = "Statement"
    # fmt: on
