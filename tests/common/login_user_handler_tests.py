import pytest
from rest_framework import status
from common.login_user_handler import LoginUserHandlerMixin

from .login_user_handler_data import data_get_login_user_id, data_get_initial
from common.exception_handler import UnAuthorizedException

class TestLoginUserHandler:
    """ ログインユーザハンドラ テストコード
    """

    class TestGetLoginUserId:

        def test_リクエストのユーザからユーザIDが取得できること(self):

            # GIVEN
            sut = LoginUserHandlerMixin()
            request, expected = data_get_login_user_id.get_specified_user_request()

            # WHEN
            actual = sut.get_login_user_id(request)

            # THEN
            assert actual == expected

        def test_リクエストの匿名ユーザからNoneが取得できること(self):

            # GIVEN
            sut = LoginUserHandlerMixin()
            request, expected = data_get_login_user_id.get_anonymous_user_request()

            # WHEN
            actual = sut.get_login_user_id(request)

            # THEN
            assert actual is expected

    class TestInitial:

        def test_ログイン済ユーザでinitialを実行するとNoneが得られること(self):
            
            # GIVEN
            view, request = data_get_initial.get_specified_user_request()

            # WHEN
            actual = view.initial(request)

            # THEN
            assert actual is None

        def test_未ログインユーザでinitialを実行するとUnAuthorizedExceptionが送出されること(self):

            # GIVEN
            view, request = data_get_initial.get_anonymous_user_request()

            # THEN
            with pytest.raises(UnAuthorizedException):
                # WHEN
                view.initial(request)