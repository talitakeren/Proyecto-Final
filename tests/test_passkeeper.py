import pytest
from src.logica.gestor_passkeeper import PassKeeper

@pytest.fixture
def passkeeper():
    return PassKeeper(db_path=':memory:')

def test_add_password(passkeeper):
    passkeeper.add_password("Email", "user@example.com", "secure123")
    passwords = passkeeper.view_passwords()
    assert len(passwords) == 1
    assert passwords[0][0] == "Email"

def test_edit_password(passkeeper):
    passkeeper.add_password("Email", "user@example.com", "secure123")
    passkeeper.edit_password("Email", "newsecure456")
    passwords = passkeeper.view_passwords()
    assert passwords[0][2] == "newsecure456"

def test_delete_password(passkeeper):
    passkeeper.add_password("Email", "user@example.com", "secure123")
    passkeeper.delete_password("Email")
    passwords = passkeeper.view_passwords()
    assert len(passwords) == 0
