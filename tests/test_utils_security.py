import pytest
import time
from datetime import timedelta
from app.utils.security import hash_password, verify_password, generate_jwt_token, decode_jwt_token, generate_api_key

def test_hash_password():
    plain_pwd = '123456'
    hash_pwd = hash_password(plain_pwd)
    assert plain_pwd != hash_pwd, 'hashed password should be different'
    hash_pwd_2 = hash_password(plain_pwd)
    assert hash_pwd != hash_pwd_2, 'hashed password should be salted, and different for each hash'
    assert verify_password(hash_pwd, plain_pwd), 'password can not be verified'
    assert verify_password(hash_pwd_2, plain_pwd), 'password can not be verified'
    assert not verify_password(plain_pwd, plain_pwd), 'password can not be verified'

def test_jwt_token():
    data = {'user_id': 1}
    jwt_token = generate_jwt_token(data, timedelta(seconds=3))
    payload = decode_jwt_token(jwt_token)
    assert payload['user_id'] == 1, 'jwt token incorrect'
    time.sleep(3)
    payload = decode_jwt_token(jwt_token)
    assert payload is None, 'jwt should expired'


def test_generate_api_key():
    apikey = generate_api_key()
    assert len(apikey) >= 32
    apikey2 = generate_api_key()
    assert apikey != apikey2