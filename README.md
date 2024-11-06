# Enable Banking Python SDK

The Banking Python SDK is a Python library that enables you to easily work with the Banking API. The SDK helps take the complexity out of coding by providing Python classes for all API endpoints. It provides a simple way to interact with the Banking API using Python.

## Getting started

### Installation

```sh
pip install enablebanking_sdk
```

### Examples

Examples can be found in the [examples](./src/enablebanking_sdk/samples/) directory.

### EnableBankingService

# EnableBankingService Documentation

| Method                     | Arguments & Return Type                                                                                                                                                                                                                                                                                                                                                       | Description                                                                                                                                                  |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `__init__`                 | **Arguments**:<br>- `integration` (EnableBankingIntegration): The integration instance to interact with the EnableBanking API.<br>**Returns**: None                                                                                                                                                                                                                           | Initializes the `EnableBankingService` with the provided integration instance.                                                                               |
| `get_aspsps`               | **Arguments**:<br>- `country` (str): The country code.<br>- `psu_type` (PSUType): The type of PSU (default: `PSUType.BUSINESS`).<br>**Returns**: `list[AspspData]`                                                                                                                                                                                                            | Fetches a list of ASPSPs (Account Service Payment Service Providers) for a given country and PSU type.                                                       |
| `start_user_session`       | **Arguments**:<br>- `aspsp` (AspspData): The ASPSP information.<br>- `state` (str): The state of the session.<br>- `redirect_url` (str): The URL to redirect the user.<br>- `language` (str): Preferred language.<br>- `psu_type` (PSUType): The type of PSU.<br>- `psu_id` (Optional[str]): The PSU ID (optional).<br>**Returns**: `EnableBankingStartAuthorizationResponse` | Starts a new user session with the given parameters and returns the authorization response.                                                                  |
| `authorize_user_session`   | **Arguments**:<br>- `code` (str): The authorization code.<br>**Returns**: `EnableBankingAuthorizeSessionResponse`                                                                                                                                                                                                                                                             | Authorizes a user session using the provided code, returning the session response.                                                                           |
| `delete_user_session`      | **Arguments**:<br>- `session_id` (str): The session ID to delete.<br>- `psu_headers` (dict): Headers for the PSU (Payment Services User) details.<br>**Returns**: None                                                                                                                                                                                                        | Deletes the specified user session by ID, with optional headers for PSU details.                                                                             |
| `get_account_transactions` | **Arguments**:<br>- `account_uid` (str): The unique identifier for the account.<br>- `date_from` (Optional[datetime]): Start date for transactions.<br>- `date_to` (Optional[datetime]): End date for transactions.<br>- `psu_headers` (Optional[dict]): Optional headers for PSU details.<br>**Returns**: `list[Transaction]`                                                | Retrieves a list of transactions for the specified account, optionally within a date range. Handles pagination if a continuation key is provided by the API. |
| `get_account_balances`     | **Arguments**:<br>- `account_uid` (str): The unique identifier for the account.<br>- `psu_headers` (Optional[dict]): Optional headers for PSU details.<br>**Returns**: `AccountBalances`                                                                                                                                                                                      | Retrieves the balances of the specified account, optionally with headers for PSU details.                                                                    |

### EnableBankingIntegration

The `EnableBankingIntegration` class is used to interact with the EnableBanking API, managing authorization tokens and providing methods to perform requests for banking operations. Initialization requires specific credentials and configuration parameters.

`__init__(self, base_url: str, app_id: str, certificate: str, auth_token_lifespan_sec: int = 3600)`

| Parameter                 | Type  | Default | Description                                                                           |
| ------------------------- | ----- | ------- | ------------------------------------------------------------------------------------- |
| `base_url`                | `str` | None    | The base URL for the EnableBanking API (e.g., `"https://api.enablebanking.com"`).     |
| `app_id`                  | `str` | None    | The application ID issued by EnableBanking, used in the JWT token header as `kid`.    |
| `certificate`             | `str` | None    | A private key certificate for signing JWT tokens, allowing secure access to the API.  |
| `auth_token_lifespan_sec` | `int` | 3600    | The lifespan of the authorization token in seconds. Default is 3600 seconds (1 hour). |

The constructor initializes an instance of `EnableBankingIntegration` with the required API credentials and configuration. It configures the base URL for API requests, sets up the JWT certificate for token generation, and defines the token expiration time.

Upon initialization, the class is ready to manage and refresh authorization tokens automatically and provides methods for performing operations such as retrieving ASPSPs, managing user sessions, and accessing account transactions and balances.

### Exceptions

| Exception                                             | Description                                                                     |
| ----------------------------------------------------- | ------------------------------------------------------------------------------- |
| `enablebanking_sdk.exceptions.EnableBankingException` | Will be raised for all API exceptions. Based on `requests.exceptions.HTTPError` |
