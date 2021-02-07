from typing import Callable, Any
import pytest
from _pytest.fixtures import SubRequest

from app_login.backend import AuthBackend
from common.exception.app_exception import LoginFailureException
from app_login.models import User

from .backend_data import ParamGetUser, ParamAuthenticate, data_get_user, data_authenticate, MOCK_USER_UUID

PARAM_GET_USER = 'param_get_user'
PARAM_AUTHENTICATE = 'param_authenticate'
sut = AuthBackend()

# 前処理 事前に認証処理で扱うユーザをDBへ登録
create_user: Callable[[str], Any] = lambda username: User.objects.create(user_id=MOCK_USER_UUID, username=username)

@pytest.fixture
def param_get_user(request: SubRequest) -> ParamGetUser:
    param: ParamGetUser = request.param
    create_user(param)

    return param

@pytest.fixture
def param_authenticate(request: SubRequest) -> ParamAuthenticate:
    param: ParamAuthenticate = request.param
    r, username, get_user = param
    create_user(username)

    return param


@pytest.mark.django_db(transaction=False)
class TestAuthBackend:

    # PKによるユーザ取得
    class Test__get_user:
        
        @pytest.mark.parametrize(
            PARAM_GET_USER, [
                pytest.param(data_get_user.get_alpha_numeric_username(), id='alpha_numeric'),
                pytest.param(data_get_user.get_unicode_username(), id='unicode'),
            ],
            indirect=[PARAM_GET_USER]
        )
        def test__exists_user(self, param_get_user: str):
            # WHEN
            actual = sut.get_user(MOCK_USER_UUID)
            expected = User.objects.get(user_id=MOCK_USER_UUID)
            print(actual)
            print(expected)
            # THEN
            assert actual == expected

        def test__no_exists_user(self):
            # GIVEN
            invalid_user_id = 'a47f5ff0-32cc-4059-b5c9-a54b9f1ae2ee'
            # WHEN
            actual = sut.get_user(invalid_user_id)
            # THEN
            assert actual is None
        
    # 認証処理
    class Test__authenticate:

        @pytest.mark.parametrize(
            PARAM_AUTHENTICATE,
            [
                pytest.param(data_authenticate.get_user(), id='simple')
            ],
            indirect=[PARAM_AUTHENTICATE]
        )
        def test__success_authenticate(self, param_authenticate: ParamAuthenticate):
            # GIVEN
            request, username, get_expected = param_authenticate
            # WHEN
            actual = sut.authenticate(request, username)
            # THEN
            assert actual == get_expected()

        def test__failure_authenticate(self):
            # GIVEN
            request, username, get_expected = data_authenticate.get_user()
            # THEN
            with pytest.raises(LoginFailureException):
                # WHEN
                sut.authenticate(request, username='nobody')
