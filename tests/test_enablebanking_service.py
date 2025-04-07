import unittest
from datetime import date, datetime
from unittest import mock

from src.enablebanking_sdk.constants import PSUType
from src.enablebanking_sdk.constants.transaction_fetch_strategy import TransactionsFetchStrategy
from src.enablebanking_sdk.models import AspspData, Transaction
from src.enablebanking_sdk.service import EnableBankingService, EnableBankingIntegration
from tests.utils import get_json_fixtures


class EnableBankingServiceTest(unittest.TestCase):
    service: EnableBankingService

    def setUp(self):
        self.service = EnableBankingService(
            integration=EnableBankingIntegration(
                base_url="https://mock.url", app_id="12345", certificate="mock-cert"
            )
        )

    @mock.patch.object(EnableBankingIntegration, "_request")
    def test_get_aspsps(self, request_mock):
        request_mock.side_effect = get_json_fixtures("aspsps_response.json")

        aspsps = self.service.get_aspsps(country="FI", psu_type=PSUType.BUSINESS)

        self.assertEqual(len(aspsps), 24)
        self.assertEqual(aspsps[0].name, "Aktia")
        self.assertEqual(aspsps[0].country, "FI")
        self.assertEqual(aspsps[0].maximum_consent_validity, 3600)

    @mock.patch.object(EnableBankingIntegration, "_request")
    def test_get_start_user_session(self, request_mock):
        request_mock.side_effect = get_json_fixtures(
            "start_user_session_response.json",
        )

        session = self.service.start_user_session(
            aspsp=AspspData(
                name="Test",
                country="FI",
                maximum_consent_validity=86400,
                logo="https://test.com/logo.png",
                bic="TESTBIC",
                required_psu_headers=["test_header"],
            ),
            state="mock-state",
            language="en",
            redirect_url="https://mock.url/redirect",
            psu_type=PSUType.BUSINESS,
            psu_id="user-id-123",
        )

        self.assertEqual(
            session.url,
            "https://tilisy.enablebanking.com/ais/start?sessionid=7b8b53ae-d2bc-4482-9e08-7c1bc5e5da8d&locale=FI",
        )
        self.assertEqual(
            session.authorization_id, "7b8b53ae-d2bc-4482-9e08-7c1bc5e5da8d"
        )
        self.assertEqual(
            session.psu_id_hash,
            "a73e18791266b4525b75e08995447e3cc2dca30c522091fa283220e769b05b80",
        )

    @mock.patch.object(EnableBankingIntegration, "_request")
    def test_authorize_user_session(self, request_mock):
        request_mock.side_effect = get_json_fixtures(
            "authorize_user_session_response.json",
        )

        session = self.service.authorize_user_session(
            "6cc44479-7e7f-4f1b-90a3-11cc183670cf"
        )
        self.assertEqual(session.session_id, "6cc44479-7e7f-4f1b-90a3-11cc183670cf")

    @mock.patch.object(EnableBankingIntegration, "_request")
    def test_get_account_transactions(self, request_mock):
        request_mock.side_effect = get_json_fixtures(
            "account_transactions_1_response.json",
            "account_transactions_2_response.json",
        )

        transactions = self.service.get_account_transactions(
            account_uid="test_uid",
            date_from=datetime.combine(
                date(2024, 1, 1),
                datetime.min.time(),
            ),
            strategy=TransactionsFetchStrategy.DEFAULT,
            psu_headers={"test_header": "test_value"},
        )

        self.assertEqual(len(transactions), 3)
        self.assertEqual(transactions[0].transaction_amount.amount, 5.20)

    @mock.patch.object(EnableBankingIntegration, "_request")
    def test_get_account_balances(self, request_mock):
        request_mock.side_effect = get_json_fixtures(
            "account_balances_response.json",
        )

        data = self.service.get_account_balances(
            "account_uid",
            psu_headers={"test_header": "test_value"},
        )

        self.assertEqual(len(data.balances), 2)
        self.assertEqual(data.balances[0].balance_amount.amount, 2107.45)
        self.assertEqual(data.balances[0].balance_amount.currency, "EUR")
