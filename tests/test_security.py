from app.security import hash_password, verify_password


def test_hash_and_verify_password():
    password = "secret"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("badpass", hashed) is False
