import random
import string
from fixtures import *


def test_retrieving_correct_user_names():
    # Default out-of-the-box users
    assert set(manager.users.usernames) == {'root', 'daemon', 'network', 'ftp', 'nobody'}


def test_creating_and_deleting_users():
    name = 'test_user'
    manager.users.create_user(name)
    assert name in manager.users.usernames
    manager.users.delete_user(name)
    assert name not in manager.users.usernames


def test_changing_and_checking_passwords():
    test_user = 'daemon'

    # Generate a random password
    password = ''.join(random.choice(string.lowercase + string.uppercase + string.digits) for _ in range(10))

    assert not manager.users.check_password(test_user, password)

    manager.users.change_password(test_user, password)

    assert manager.users.check_password(test_user, password)
