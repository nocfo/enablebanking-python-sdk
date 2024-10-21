from enum import StrEnum


class SchemeName(StrEnum):
    ARNU = ("ARNU",)  # AlienRegistrationNumber
    BANK = (
        "BANK",
    )  # BankPartyIdentification. Unique and unambiguous assignment made by a specific bank or similar financial institution to identify a relationship as defined between the bank and its client.
    BBAN = (
        "BBAN",
    )  # Basic Bank Account Number. Represents a country-specific bank account number.
    BGNR = (
        "BGNR",
    )  # Swedish BankGiro account number. Used in domestic swedish giro payments
    CCPT = ("CCPT",)  # PassportNumber
    CHID = ("CHID",)  # Clearing Identification Number
    COID = (
        "COID",
    )  # CountryIdentificationCode. Country authority given organisation identification (e.g., corporate registration number)
    CPAN = ("CPAN",)  # Card PAN (masked or plain)
    CUSI = (
        "CUSI",
    )  # CustomerIdentificationNumberIndividual. Handelsbanken-specific code
    CUST = ("CUST",)  # CorporateCustomerNumber
    DRLC = ("DRLC",)  # DriversLicenseNumber
    DUNS = ("DUNS",)  # Data Universal Numbering System
    EMPL = ("EMPL",)  # EmployerIdentificationNumber
    GS1G = ("GS1G",)  # GS1GLNIdentifier
    IBAN = (
        "IBAN",
    )  # International Bank Account Number (IBAN) - identification used internationally by financial institutions to uniquely identify the account of a customer.
    MIBN = ("MIBN",)  # Masked IBAN
    NIDN = (
        "NIDN",
    )  # NationalIdentityNumber. Number assigned by an authority to identify the national identity number of a person.
    OAUT = (
        "OAUT",
    )  # OAUTH2 access token that is owned by the PISP being also an AISP and that can be used in order to identify the PSU
    OTHC = ("OTHC",)  # OtherCorporate. Handelsbanken-specific code
    OTHI = ("OTHI",)  # OtherIndividual. Handelsbanken-specific code
    PGNR = (
        "PGNR",
    )  # Swedish PlusGiro account number. Used in domestic swedish giro payments
    SOSE = ("SOSE",)  # SocialSecurityNumber
    SREN = (
        "SREN",
    )  # The SIREN number is a 9 digit code assigned by INSEE, the French National Institute for Statistics and Economic Studies, to identify an organisation in France.
    SRET = (
        "SRET",
    )  # The SIRET number is a 14 digit code assigned by INSEE, the French National Institute for Statistics and Economic Studies, to identify an organisation unit in France. It consists of the SIREN number, followed by a five digit classification number, to identify the local geographical unit of that entity.
    TXID = ("TXID",)  # TaxIdentificationNumber
