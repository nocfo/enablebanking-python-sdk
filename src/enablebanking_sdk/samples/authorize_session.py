import os
from uuid import uuid4

from ..constants import PSUType
from ..service import EnableBankingService, EnableBankingIntegration


EB_BASE_URL = os.getenv("ENABLEBANKING_BASE_URL", "")
EB_APP_ID = os.getenv("ENABLEBANKING_APP_ID", "")
EB_CERTIFICATE = os.getenv("ENABLEBANKING_CERTIFICATE", "")
EB_REDIRECT_URL = os.getenv("ENABLEBANKING_REDIRECT_URL", "")


eb_service = EnableBankingService(
    integration=EnableBankingIntegration(
        base_url=EB_BASE_URL,
        app_id=EB_APP_ID,
        certificate=EB_CERTIFICATE,
    )
)


# List ASPSPs and select one to authorize
aspsps = eb_service.get_aspsps(country="FI", psu_type=PSUType.BUSINESS)
aspsp = next(aspsp for aspsp in aspsps if aspsp.name == "Holvi")

# Start user session authorization
start_session_response = eb_service.start_user_session(
    aspsp=aspsp,
    state=uuid4().hex,  # Internal state param will be returned in the redirect URL as a query parameter
    redirect_url=EB_REDIRECT_URL,
    psu_type=PSUType.BUSINESS,
    psu_id="1234567890",
    language="en",
)

# Redirect PSU to the session URL. PSU will complete the authorization and will
# be redirected to the redirect URL with the code and state query parameters
print("Open the following URL in your browser to authorize the session:")
print(start_session_response.url)
code = input("Enter the authorization code (from redirect url param):\n")

# Finalize the session authorization using the code
authorize_session_response = eb_service.authorize_user_session(code)

# Session is now authorized and ready to be used
print(f"Session ID: {authorize_session_response.session_id}")
