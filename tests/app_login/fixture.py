import pytest
from django.contrib.auth.hashers import make_password

from app_login.models import User

# テストユーザ情報
def get_user_info_fixture():

    user_info = [
        {'username': 'a-pompom0107'},
        {'username': 'johnDoe__9807'},
        {'username': 'pompomPurin0001'},
    ]
    return user_info

# テストユーザをfixtureで生成
@pytest.fixture()
def multiple_users():
    user_info = get_user_info_fixture()

    return tuple(
        User.objects.create(
            username=user_dict['username'],
        ) for user_dict in user_info
    )