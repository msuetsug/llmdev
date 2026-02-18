import pytest
from authenticator import Authenticator

@pytest.fixture
def authenticator():
    auth = Authenticator()
    yield auth

# ユーザの登録 - ユーザー名とパスワードを登録できること
@pytest.mark.parametrize("username, password, expected", [
    ("Alice", "P@ssword", "P@ssword"),
    ("Bob", "12345678", "12345678"),
    ("Carol", "qwertyui", "qwertyui"),
])

def test_register(authenticator, username, password, expected):
    authenticator.register(username, password)
    assert authenticator.users[username] == expected

# ユーザの登録 - すでに存在するユーザー名で登録した場合、エラーメッセージが出力されること
def test_duplicate_register(authenticator):
    authenticator.register("Alice", "P@ssword")
    with pytest.raises(ValueError, match="エラー: ユーザーは既に存在します。"):
        authenticator.register("Alice", "P@ssword")

# ログイン - ユーザー名とパスワードでログインできること
@pytest.mark.parametrize("username, password", [
    ("Alice", "P@ssword"),
    ("Bob", "12345678"),
    ("Carol", "qwertyui"),
])
def test_login(authenticator, username, password):
    authenticator.register(username, password)
    result = authenticator.login(username, password)
    assert result == "ログイン成功"

# ログイン - 誤ったパスワードでログインした場合、エラーメッセージが出力されること
def test_incorrect_password(authenticator):
    authenticator.register("Alice", "P@ssword")
    with pytest.raises(ValueError, match="エラー: ユーザー名またはパスワードが正しくありません。"):
        authenticator.login("Alice", "Test")
