from app.domain.user import User


def test_create_user():
    user = User(
        id=1,
        name="test_name",
        email="test_email@example.com",
        hashed_password="hashed_password",
    )
    assert user.id == 1
    assert user.name == "test_name"
    assert user.email == "test_email@example.com"
    assert user.hashed_password == "hashed_password"
    assert user.is_active is True
