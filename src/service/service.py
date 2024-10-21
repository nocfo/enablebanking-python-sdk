from datetime import datetime, timezone, timedelta
from typing import Optional


from src.constants.psu_type import PSUType


from src.models.aspsp import (
    AspspData,
    EnableBankingStartAuthorizationRequest,
    EnableBankingStartAuthorizationResponse,
    EnableBankingAuthorizeSessionResponse,
    Transaction,
    AspspsResponse,
    EnableBankingAccess,
)
from src.models.balances import AccountBalances
from src.service.integration import EnableBankingIntegration


class EnableBankingService:
    integration: EnableBankingIntegration

    def __init__(
        self,
        integration: EnableBankingIntegration,
    ):
        self.integration = integration

    def get_aspsps(
        self,
        country: str = "FI",
        psu_type: PSUType = PSUType.BUSINESS,
    ) -> list[AspspData]:
        response = self.integration.get_aspsps(
            country=country,
            psu_type=psu_type,
        )

        return AspspsResponse.parse_obj(response).aspsps

    def start_user_session(
        self,
        aspsp: AspspData,
        state: str,
        redirect_url: str,
        language: str,
        psu_type: PSUType,
        psu_id: Optional[str] = None,
    ) -> EnableBankingStartAuthorizationResponse:
        request = EnableBankingStartAuthorizationRequest(
            aspsp=aspsp,
            state=state,
            psu_type=psu_type,
            psu_id=psu_id,
            redirect_url=redirect_url,
            language=language,
            access=EnableBankingAccess(
                valid_until=(
                    datetime.now(timezone.utc)
                    + timedelta(seconds=aspsp.maximum_consent_validity)
                ).isoformat(),
            ),
        )
        response = self.integration.start_user_session(
            request.model_dump(exclude_none=True)
        )
        return EnableBankingStartAuthorizationResponse.parse_obj(response)

    def authorize_user_session(
        self, code: str
    ) -> EnableBankingAuthorizeSessionResponse:
        data = self.integration.authorize_user_session(code)
        return EnableBankingAuthorizeSessionResponse.parse_obj(data)

    def delete_user_session(self, session_id: str, psu_headers: dict) -> None:
        self.integration.delete_user_session(session_id, psu_headers=psu_headers)

    def get_account_transactions(
        self,
        account_uid: str,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        psu_headers: Optional[dict] = None,
    ) -> list[Transaction]:
        transactions = []

        continuation_key = None
        while True:
            data = self.integration.get_account_transactions(
                account_uid=account_uid,
                date_from=date_from,
                date_to=date_to,
                psu_headers=psu_headers,
                continuation_key=continuation_key,
            )
            transactions += data["transactions"]

            # CASE: Fetch more transaction if continuation key is provided
            if (continuation_key := data.get("continuation_key")) is None:
                break

        return [Transaction.parse_obj(transaction) for transaction in transactions]

    def get_account_balances(
        self,
        account_uid: str,
        psu_headers: Optional[dict] = None,
    ) -> AccountBalances:
        data = self.integration.get_account_balances(
            account_uid=account_uid,
            psu_headers=psu_headers,
        )
        return AccountBalances.parse_obj(data)
