from auth_api import get_access_token


class AngelError(Exception):
    status_code: int


def get_test_tokens():
    data = {
        'client_id': 'RziveGzb0G4z6M-1cFQkE6MRhTVtWX2U8pna0klD0',
        'client_secret': 'RziveGzb0G4z6M-1cFQkE6MRhTVtWX2U8pna0klD0',
        'redirect_uri': "localhost",
        'device_id': "DroneTag"
    }

    return get_access_token(**data)

if __name__ == '__main__':
    # The access and refresh tokens should ideally be stored on the client to prevent the user having to authenticate
    # repeatedly. How to store these is beyond the scope of this tutorial, but a client-side cookie, local storage
    # etc could be used.

    try:
        tokens = get_test_tokens()
    except AngelError as e:
        print(e.status_code)
        print(e.json())

    print(tokens.dict())
    print(tokens.access_token)




