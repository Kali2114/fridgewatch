from app.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_hash_and_verify_password():
    password = "secret"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("badpass", hashed) is False


def test_create_and_decode_access_token():
    token = create_access_token(5)

    assert isinstance(token, str)
    assert decode_access_token(token) == 5
