from enum import StrEnum


class AccountBalanceType(StrEnum):
    # (ISO20022 Closing Available) Closing available balance
    CLAV = "CLAV"
    # (ISO20022 ClosingBooked) Accounting Balance
    CLBD = "CLBD"
    # (ISO20022 ForwardAvailable) Balance that is at the disposal of account holders on the date specified
    FWAV = "FWAV"
    # (ISO20022 Information) Balance for informational purposes
    INFO = "INFO"
    # (ISO20022 InterimAvailable) Available balance calculated in the course of the day
    ITAV = "ITAV"
    # (ISO20022 InterimBooked) Booked balance calculated in the course of the day
    ITBD = "ITBD"
    # (ISO20022 OpeningAvailable) Opening balance that is at the disposal of account holders at the beginning of the
    # date specified
    OPAV = "OPAV"
    # (ISO20022 OpeningBooked) Book balance of the account at the beginning of the account reporting period. It always
    # equals the closing book balance from the previous report
    OPBD = "OPBD"
    # Other Balance
    OTHR = "OTHR"
    # (ISO20022 PreviouslyClosedBooked) Balance of the account at the end of the previous reporting period
    PRCD = "PRCD"
    # Value-date balance
    VALU = "VALU"
    # (ISO20022 Expected) Instant Balance
    XPCD = "XPCD"
