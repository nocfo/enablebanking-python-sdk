from requests.exceptions import HTTPError


class EnableBankingException(HTTPError):
    pass
