from typing import Optional

import httpx
from pydantic import BaseModel, ValidationError

from main import AngelError

test_surveillance_base_uri = "https://surveillance-api.sit.altitudeangel.io"
test_auth_base_uri = "https://auth.sit.altitudeangel.io"


class AccessTokensRequest(BaseModel):
    client_id: str
    client_secret: str
    grant_type: str
    scope: str
    token_format: str
    redirect_uri: str
    device_id: str
    state: Optional[str]


class AccessTokensResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    refresh_token: str
    state: Optional[str]


class RefreshAccessTokenRequest(BaseModel):
    client_id: str
    client_secret: str
    grant_type: str
    refresh_token: str
    state: Optional[str]


def access_api_call(request_data, req_class):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    try:
        access_token_req = req_class(**request_data)
    except ValidationError as e:
        raise AngelError(e.json())

    resp = httpx.post(f"{test_auth_base_uri}/oauth/v2/token", headers=headers, data=access_token_req.dict())

    if resp.status_code != 200:
        err = AngelError(resp.text)
        err.status_code = resp.status_code
        raise err

    return AccessTokensResponse(**resp.json())


def get_access_token(client_id, client_secret, redirect_uri, device_id, state=None):
    """
    Before this call, users must have pre-registered their local unique sensor IDs by creating a support ticket.
    Function will call API to obtain standard OAuth v2 response with access_token and refresh_token. Both these
    tokens will be returned by the function. The access_token should be then used to communicate with the
    Surveillance API.
    :return: tuple containing access_token and refresh_token
    """
    request_data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': "client_credentials",
        'scope': "surveillance_api",
        'token_format': 'jwt',
        'redirect_uri': redirect_uri,
        'device_id': device_id
    }
    if state:
        request_data['state'] = state

    return access_api_call(request_data, AccessTokensRequest)


def refresh_access_token(client_id, client_secret, refresh_token, state=None):
    """
    For every request made to the Altitude Angel APIs with a bearer access token, you must check the response code for
    an 401 Access Denied error.

    When this is received and using a previously valid access token, you should make a request for a new access token.

    Once a new access token is received then retry the failed request using the new access token. If this also results
    in the same response code then an error should be returned to the user.
    :return:
    """
    request_data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': "refresh_token",
        'refresh_token': refresh_token,
    }
    if state:
        request_data['state'] = state

    return access_api_call(request_data, RefreshAccessTokenRequest)
