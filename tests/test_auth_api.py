import json
import unittest
from unittest.mock import patch

from auth_api import _access_api_call, AccessTokensRequest, test_auth_base_uri
from errors import AngelError


def access_token_json_response_f():
    # Mocking Altitude Angel API reponse.
    return {
        'access_token': '67582121212aaa',
        'token_type': '',
        'expires_in': 123456789,
        'refresh_token': 'jhjdksjfhskjdhf119119',
    }


class TestAccessTokenAPI(unittest.TestCase):

    def setUp(self):
        self.valid_get_access_token_req = {
            'client_id': 'client1',
            'client_secret': 'client1_secret',
            'grant_type': "client_credentials",
            'scope': "surveillance_api",
            'token_format': 'jwt',
            'redirect_uri': 'redirect_1',
            'device_id': 'device_id_1',
            'state': 'state_a'
        }
        self.non_valid_get_access_token_req = {
            'client_id': 'client1',
            # missing required value
            # 'client_secret': 'client1_secret',
            'grant_type': "client_credentials",
            'scope': "surveillance_api",
            'token_format': 'jwt',
            'redirect_uri': 'redirect_1',
            'device_id': 'device_id_1',
            'state': 'state_a'
        }
        self.get_access_token_response = access_token_json_response_f

    @patch('httpx.post')
    def test__access_api_call_success(self, post_mock):
        """
        Test getting access_token with success
        :param post_mock: mocked httpx.post method
        :return:
        """
        post_mock.return_value.status_code = 200
        post_mock.return_value.json = self.get_access_token_response

        resp = _access_api_call(self.valid_get_access_token_req, AccessTokensRequest)

        assert post_mock.called
        post_mock.assert_called_once_with(f"{test_auth_base_uri}/oauth/v2/token",
                                          headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                          data={'client_id': 'client1', 'client_secret': 'client1_secret',
                                                   'grant_type': 'client_credentials', 'scope': 'surveillance_api',
                                                   'token_format': 'jwt', 'redirect_uri': 'redirect_1',
                                                   'device_id': 'device_id_1', 'state': 'state_a'})
        self.assertIsNotNone(resp)
        self.assertEqual(resp.access_token, '67582121212aaa')
        self.assertEqual(resp.expires_in, 123456789)
        self.assertEqual(resp.refresh_token, 'jhjdksjfhskjdhf119119')

    def test__access_api_call_req_validation_error(self):
        """
        Test request data validation error. Should return AngelError.
        :return:
        """
        with self.assertRaises(AngelError) as cm:
            _access_api_call(self.non_valid_get_access_token_req, AccessTokensRequest)

        the_exception = cm.exception
        self.assertEqual(the_exception.status_code, 400)
        exception_msg = json.loads(the_exception.args[0])
        self.assertEqual(exception_msg[0]['loc'], ['client_secret'])
        self.assertEqual(exception_msg[0]['msg'], 'field required')
        self.assertEqual(exception_msg[0]['type'], 'value_error.missing')

    @patch('httpx.post')
    def test__access_api_call_altitudeangel_error_response(self, post_mock):
        """
        Test getting access_token - http response 401 (not 200) from altitudeangel API. Should return AngelError.
        :return:
        """
        post_mock.return_value.status_code = 401
        post_mock.return_value.text = "User not authorized"

        with self.assertRaises(AngelError) as cm:
            _access_api_call(self.valid_get_access_token_req, AccessTokensRequest)

        assert post_mock.called
        post_mock.assert_called_once_with(f"{test_auth_base_uri}/oauth/v2/token",
                                          headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                          data={'client_id': 'client1', 'client_secret': 'client1_secret',
                                                   'grant_type': 'client_credentials', 'scope': 'surveillance_api',
                                                   'token_format': 'jwt', 'redirect_uri': 'redirect_1',
                                                   'device_id': 'device_id_1', 'state': 'state_a'})
        the_exception = cm.exception
        self.assertEqual(the_exception.status_code, 401)
        self.assertEqual(the_exception.args[0], "User not authorized")

