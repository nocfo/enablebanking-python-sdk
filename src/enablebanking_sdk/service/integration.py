import logging
from datetime import datetime, timedelta
from typing import Optional, Tuple
from requests.exceptions import HTTPError

import jwt
import requests

from ..constants.transaction_fetch_strategy import TransactionsFetchStrategy
from ..exceptions import EnableBankingException


logger = logging.getLogger(__name__)


class EnableBankingIntegration:
    token: str
    token_expiration: Optional[datetime] = None

    base_url: str
    app_id: str
    certificate: str
    auth_token_lifespan_sec: int

    def __init__(
        self,
        base_url: str,
        app_id: str,
        certificate: str,
        auth_token_lifespan_sec: int = 3600,
    ):
        self.certificate = certificate
        self.base_url = base_url
        self.app_id = app_id
        self.auth_token_lifespan_sec = auth_token_lifespan_sec

    def _generate_authorization_token(self) -> Tuple[str, datetime]:
        now = datetime.now()
        exp = now + timedelta(seconds=self.auth_token_lifespan_sec)

        return (
            jwt.encode(
                {
                    "iss": "enablebanking.com",
                    "aud": "api.enablebanking.com",
                    "iat": int(now.timestamp()),
                    "exp": int(exp.timestamp()),
                },
                self.certificate,
                algorithm="RS256",
                headers={"kid": self.app_id},
            ),
            exp,
        )

    def _get_token(self) -> str:
        # CASE: No token generated
        # > Perform initial token generation
        if self.token_expiration is None:
            logger.debug("Generating initial authorization token")
            self.token, self.token_expiration = self._generate_authorization_token()
            return self.token

        # CASE: Token about to expire
        # > Generate new token
        if datetime.now() + timedelta(seconds=60) >= self.token_expiration:
            logger.debug("Generating new authorization token")
            self.token, self.token_expiration = self._generate_authorization_token()
            return self.token

        logger.debug("Using existing authorization token")
        return self.token

    def _request(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        headers: dict | None = None,
        json: dict | None = None,
        timeout: int = 30,
    ) -> dict:
        response = requests.request(
            method,
            self.base_url + path,
            params=params,
            headers={
                "Authorization": f"Bearer {self._get_token()}",
                "Content-Type": "application/json",
                **(headers if headers else {}),
            },
            json=json,
            timeout=timeout,
        )

        try:
            response.raise_for_status()
            return response.json()

        except HTTPError as err:
            raise EnableBankingException(
                err,
                request=err.request,
                response=err.response,
            ) from err

    def get_aspsps(self, country: str, psu_type: str) -> dict:
        return self._request(
            method="GET",
            path="/aspsps",
            params={
                "country": country,
                "psu_type": psu_type,
            },
        )

    def start_user_session(self, request: dict) -> dict:
        return self._request(
            method="POST",
            path="/auth",
            json=request,
        )

    def delete_user_session(self, session_id: str, psu_headers: dict):
        return self._request(
            method="DELETE",
            path=f"/sessions/{session_id}",
            headers=psu_headers,
        )

    def authorize_user_session(self, code: str) -> dict:
        return self._request(
            method="POST",
            path="/sessions",
            json={"code": code},
        )

    def get_account_transactions(
        self,
        account_uid: str,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        strategy: TransactionsFetchStrategy | None = None,
        psu_headers: dict | None = None,
        continuation_key: str | None = None,
    ) -> dict:
        def _fmt_dt(date: Optional[datetime]) -> Optional[str]:
            return date.replace(tzinfo=None).strftime("%Y-%m-%d") if date else None

        return self._request(
            method="GET",
            path=f"/accounts/{account_uid}/transactions",
            headers=psu_headers,
            params={
                "date_from": _fmt_dt(date_from),
                "date_to": _fmt_dt(date_to),
                "strategy": strategy,
                "continuation_key": continuation_key,
            },
        )

    def get_account_balances(
        self,
        account_uid: str,
        psu_headers: Optional[dict] = None,
    ) -> dict:
        return self._request(
            method="GET",
            path=f"/accounts/{account_uid}/balances",
            headers=psu_headers,
        )
