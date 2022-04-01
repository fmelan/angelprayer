from typing import Optional

import httpx
from pydantic import BaseModel, ValidationError

from main import AngelError

test_surveillance_base_uri = "https://surveillance-api.sit.altitudeangel.io"
test_auth_base_uri = "https://auth.sit.altitudeangel.io"


class DeviceTokensResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str


class DeviceTokensRequest(BaseModel):
    client_id: str
    client_secret: str
    grant_type: str
    scope: str
    token_format: str
    redirect_uri: str
    device_id: str
    state: Optional[str]


def get_device_token(request_data):
    """
    https://docs.altitudeangel.com/docs/altitude-angel-identity-provider

    Before this call, users must have pre-registered their local unique sensor IDs by creating a support ticket.
    Function will call API to obtain standard OAuth v2 response with access_token and refresh_token. Both these
    tokens will be returned by the function. The access_token should be then used to communicate with the
    Surveillance API.
    :return: tuple containing access_token and refresh_token
    """
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    # TODO common request calls in one method

    try:
        device_token_req = DeviceTokensRequest(**request_data)
    except ValidationError as e:
        raise AngelError(e.json())

    r = httpx.post(f"{test_auth_base_uri}/oauth/v2/token", headers=headers, data=device_token_req.dict())

    if r.status_code != 200:
        raise AngelError(r.text)

    return DeviceTokensResponse(**r.json())


def refresh_device_token():
    pass