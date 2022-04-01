from auth_api import get_device_token


class AngelError(Exception):
    pass


def get_test_tokens():
    data = {
        'client_id': 'RziveGzb0G4z6M-1cFQkE6MRhTVtWX2U8pna0klD0',
        'client_secret': "vXBk/5yO1tx9eH9BLMNpJn403CJariLJ3eL8umy8Ucl1EZn/j6GkoA==",
        'grant_type': "client_credentials",
        'scope': "surveillance_api",
        'token_format': 'jwt',
        'redirect_uri': "localhost",
        'device_id': "DroneTag"
    }

    return get_device_token(data)


if __name__ == '__main__':


    # The access and refresh tokens should ideally be stored on the client to prevent the user having to authenticate
    # repeatedly. How to store these is beyond the scope of this tutorial, but a client-side cookie, local storage
    # etc could be used.

    tokens = get_test_tokens()

    print(tokens.dict())
    print(tokens.access_token)

