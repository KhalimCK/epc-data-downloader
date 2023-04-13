import pytest
from api.exceptions import MissingAuth
from api.client import EpcClient
import base64


def test_failed_init_all_args_null():
    # No credentials supplied, should error
    with pytest.raises(MissingAuth) as _:
        EpcClient()


def test_successful_init_auth_token():

    # Auth token supplied, should be successful
    test_auth_token = base64.b64encode(b"test@user.com:<api_key>")

    client = EpcClient(auth_token=test_auth_token)
    assert client.auth_token == test_auth_token

    assert client.api_key is None
    assert client.user_email is None


def test_failed_init_just_email():
    # Just user email supplied, needs api key
    test_user_email = "test@user.com"

    with pytest.raises(MissingAuth) as _:
        EpcClient(user_email=test_user_email)


def test_failed_init_just_api_key():
    # Just user email supplied, needs api key
    test_api_key = "testapikey"

    with pytest.raises(MissingAuth) as _:
        EpcClient(api_key=test_api_key)


def test_successful_init():

    test_user_email = "test@user.com"
    test_api_key = "testapikey"
    expected_auth_token = base64.b64encode(":".join([test_user_email, test_api_key]).encode("utf-8"))

    client = EpcClient(user_email=test_user_email, api_key=test_api_key)

    assert client.auth_token is not None
    assert client.user_email is not None
    assert client.api_key is not None
    assert client.auth_token == expected_auth_token

    # Check headers
    assert isinstance(client.headers, dict)
    assert set(client.headers.keys()) == {"Accept", "Authorization"}