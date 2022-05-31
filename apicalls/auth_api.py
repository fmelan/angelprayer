# https://docs.altitudeangel.com/docs/altitude-angel-identity-provider

from typing import Optional

import httpx
from pydantic import BaseModel, ValidationError

from errors import AngelError

# Data Models
from settings import settings


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
    state: Optional[str]


class RefreshAccessTokenRequest(BaseModel):
    client_id: str
    client_secret: str
    grant_type: str
    refresh_token: str
    state: Optional[str]


# API Calls


def get_access_token(
    client_id: str,
    client_secret: str,
    redirect_uri: str,
    device_id: str,
    state: str = None,
) -> AccessTokensResponse:
    """
    Before this call, users must have pre-registered their local unique sensor IDs by
    creating a support ticket. Function will call API to obtain standard OAuth v2
    response with access_token and refresh_token. Both these tokens will be returned
    by the function. The access_token should be then used to communicate with the
    Surveillance API.
    :return: instance of AccessTokensResponse
    """
    request_data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
        "scope": "surveillance_api",
        "token_format": "jwt",
        "redirect_uri": redirect_uri,
        "device_id": device_id,
    }
    if state:
        request_data["state"] = state

    return _access_api_call(request_data, AccessTokensRequest)


def refresh_access_token(client_id, client_secret, refresh_token, state=None):
    """
    For every request made to the Altitude Angel API with a bearer access token,
    you must check the response code for an 401 Access Denied error.

    When this is received and using a previously valid access token, you should
    make a request for a new access token.

    Once a new access token is received then retry the failed request using the
    new access token. If this also results in the same response code then
    an error should be returned to the user.
    :return: instance of AccessTokensResponse
    """
    request_data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    if state:
        request_data["state"] = state

    return _access_api_call(request_data, RefreshAccessTokenRequest)


def _access_api_call(request_data, req_class):
    """
    Internal function for obtaining and refreshing access tokens. Should not be used
    outside this package. If the request_data are not valid, it raises AngelError with
    a message specifying the error. If the Altitude Angel API responds with different
    HTTP code than 200, then it raises AngelError with corresponding status_code and
    the response as error message.
    :param request_data: request data
    :param req_class: AccessTokensRequest or RefreshAccessTokenRequest
    :return: instance of AccessTokensResponse
    """
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        access_token_req = req_class(**request_data)
    except ValidationError as e:
        ae = AngelError(e.json())
        ae.status_code = 400
        raise ae

    resp = httpx.post(
        f"{settings.auth_base_uri}/oauth/v2/token",
        headers=headers,
        data=access_token_req.dict(),
    )

    if resp.status_code != 200:
        err = AngelError(resp.text)
        err.status_code = resp.status_code
        raise err

    return AccessTokensResponse(**resp.json())
