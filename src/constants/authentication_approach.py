from enum import StrEnum


class AuthenticationApproach(StrEnum):
    # fmt: off
    DECOUPLED = "DECOUPLED"
    EMBEDDED  = "EMBEDDED"
    REDIRECT  = "REDIRECT"
    # fmt: on
